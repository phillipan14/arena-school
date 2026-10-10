"""Finalize step: export the deck to PDF and refresh the /talk page.

Run ONLY once the slides are final (see README.md). It overwrites:
  talk/Arena-Parent-Conversation-EN.pdf   (download button on /talk)
  talk/Arena-Parent-Conversation-CN.pdf
  talk/slides/{en,cn}/NN.jpg              (swipe gallery on /talk)
  talk/index.html data-n-en / data-n-cn   (slide counts)
and, for presenting, decks/src/exports/Arena-Parent-Conversation-EN-Presenting.pdf (with QR, not deployed).

Usage:  python3 decks/src/export.py            (from anywhere; rebuilds the deck first)
        python3 decks/src/export.py --out DIR  (write everything to DIR instead, for a dry run)
Needs:  pip install playwright pillow pypdf && python3 -m playwright install chromium
"""
import functools, http.server, io, os, re, subprocess, sys, threading
from playwright.sync_api import sync_playwright
from PIL import Image
from pypdf import PdfReader

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SRC, '..', '..'))
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
TALK = OUT or os.path.join(ROOT, 'talk')
PRESENT = OUT or os.path.join(SRC, 'exports')
MAX_MB = 6

subprocess.run([sys.executable, os.path.join(SRC, 'build.py')], check=True)

# serve the repo root so the deck's absolute paths (/fonts, /logos, /photos) resolve
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
Handler = functools.partial(Quiet, directory=ROOT)
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{srv.server_address[1]}'

JOBS = [  # (deck, pdf path, hide QR, gallery folder, JPEG quality: download PDFs are lighter for phones)
    ('conversation', os.path.join(PRESENT, 'Arena-Parent-Conversation-EN-Presenting.pdf'), False, None, 92),
    ('conversation', os.path.join(TALK, 'Arena-Parent-Conversation-EN.pdf'), True, 'en', 80),
    ('conversation-cn', os.path.join(TALK, 'Arena-Parent-Conversation-CN.pdf'), True, 'cn', 80),
]
counts = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for deck, out, noqr, gal, q in JOBS:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        pg = b.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1.5)
        pg.goto(f'{BASE}/decks/{deck}.html', wait_until='networkidle')
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
        pg.evaluate("document.documentElement.classList.add('export')" + (";document.documentElement.classList.add('noqr')" if noqr else '') + ';window.__space()')
        pg.wait_for_timeout(400)
        # every slide must fit the 1080px page in export mode, or the PDF would cut it off
        tall = pg.evaluate("[...document.querySelectorAll('section.s')].map((s,i)=>[i+1,Math.max(s.offsetHeight,s.scrollHeight)]).filter(x=>x[1]>1080)")
        if tall:
            b.close(); sys.exit(f'ABORT {deck}: slides taller than 1080px in export mode (slide, px): {tall}')
        n = pg.evaluate("document.querySelectorAll('section.s').length"); pages = []
        for i in range(n):
            pg.evaluate(f"document.getElementById('deck').scrollTop=document.querySelectorAll('section.s')[{i}].offsetTop"); pg.wait_for_timeout(200)
            pages.append(Image.open(io.BytesIO(pg.screenshot())).convert('RGB'))
        pages[0].save(out, save_all=True, append_images=pages[1:], resolution=216.0, quality=q)
        mb = os.path.getsize(out) / 1e6
        print(f'{os.path.relpath(out, ROOT) if not OUT else out}: {len(PdfReader(out).pages)} pages, {mb:.1f} MB')
        if gal and mb > MAX_MB: print(f'  WARNING: over {MAX_MB} MB, slow on phones / WeChat')
        if gal:
            d = os.path.join(TALK, 'slides', gal); os.makedirs(d, exist_ok=True)
            for f in os.listdir(d):
                if f.endswith('.jpg'): os.remove(os.path.join(d, f))
            for i, im in enumerate(pages, 1):
                im.resize((1600, 900), Image.LANCZOS).save(os.path.join(d, f'{i:02d}.jpg'), quality=82, optimize=True, progressive=True)
            counts[gal] = n
        pg.close()
    b.close()
srv.shutdown()

if not OUT:
    f = os.path.join(TALK, 'index.html'); t = open(f, encoding='utf-8').read()
    for k, n in counts.items():
        t = re.sub(rf'data-n-{k}="\d+"', f'data-n-{k}="{n}"', t)
    open(f, 'w', encoding='utf-8').write(t)
    print('talk/index.html slide counts:', counts)
print('Done. Check /talk locally, then commit and push.')
