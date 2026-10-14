"""Finalize step: export the Lux Scholar info-session deck (Chinese only) to PDF and slide images (talks/<slug>/, see site_paths.py).

Run ONLY once the slides are final (see README.md). It overwrites:
  talks/<slug>/slides-cn.pdf               (the whole deck as a PDF)
  talks/<slug>/slides/cn/NN.jpg            (slide images: the phone reader, read/cn, shows these)

Usage:  python3 decks/<slug>/src/export.py            (from anywhere; rebuilds the deck first)
        python3 decks/<slug>/src/export.py --out DIR  (write everything to DIR instead, for a dry run)
Needs:  pip install playwright pillow pypdf && python3 -m playwright install chromium
"""
import functools, http.server, io, os, re, subprocess, sys, threading
from playwright.sync_api import sync_playwright
from PIL import Image
from pypdf import PdfReader

SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
from site_paths import ROOT, OUT as TALK_OUT, BASE, SLUG
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
TALK = OUT or TALK_OUT
PRESENT = OUT or os.path.join(SRC, 'exports')
MAX_MB = 5.9
MIN_Q = 56

subprocess.run([sys.executable, os.path.join(SRC, 'build.py')], check=True)

# serve the repo root so the deck's absolute paths (/fonts, /logos, /photos) resolve
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
Handler = functools.partial(Quiet, directory=ROOT)
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
SERVER = f'http://127.0.0.1:{srv.server_address[1]}'

JOBS = [  # (deck, pdf path, hide QR, gallery folder, JPEG quality: download PDFs are lighter for phones)
    ('deck', os.path.join(TALK, 'slides-cn.pdf'), True, 'cn', 80),
]
counts = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for deck, out, noqr, gal, q in JOBS:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        pg = b.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1.5)
        pg.goto(f'{SERVER}{BASE}/{deck}.html?stage', wait_until='networkidle')
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
        pg.evaluate("document.documentElement.classList.add('export')" + (";document.documentElement.classList.add('noqr')" if noqr else '') + ';window.__space()')
        pg.wait_for_timeout(400)
        # every slide must fit the 1080px page in export mode, or the PDF would cut it off
        tall = pg.evaluate("[...document.querySelectorAll('section.s')].map((s,i)=>[i+1,Math.max(s.offsetHeight,s.scrollHeight)]).filter(x=>x[1]>1080)")
        if tall:
            b.close(); sys.exit(f'ABORT {deck}: slides taller than 1080px in export mode (slide, px): {tall}')
        # every converted shape, picture, and text box must stay on the 1920×1080 page
        loose = pg.evaluate("[...document.querySelectorAll('section.s')].flatMap((s,i)=>{const o=s.getBoundingClientRect();return [...s.querySelectorAll('.lx-el')].map(e=>{const r=e.getBoundingClientRect();return [i+1,e.dataset.n||e.alt,r.left-o.left,r.top-o.top,r.right-o.left,r.bottom-o.top]}).filter(x=>x[2]<-.5||x[3]<-.5||x[4]>1920.5||x[5]>1080.5)})")
        if loose:
            b.close(); sys.exit(f'ABORT {deck}: off the page (slide, element, box): {loose}')
        n = pg.evaluate("document.querySelectorAll('section.s').length"); pages = []
        for i in range(n):
            pg.evaluate(f"document.getElementById('deck').scrollTop=document.querySelectorAll('section.s')[{i}].offsetTop"); pg.wait_for_timeout(200)
            pages.append(Image.open(io.BytesIO(pg.screenshot())).convert('RGB'))
        # every PDF must stay under MAX_MB for phones and WeChat: step the JPEG quality down, then the resolution
        q0 = q
        for scale in (1, .85, .72):
            w, h = round(2880 * scale), round(1620 * scale)
            imgs = pages if scale == 1 else [im.resize((w, h), Image.LANCZOS) for im in pages]
            q = q0
            while True:
                imgs[0].save(out, save_all=True, append_images=imgs[1:], resolution=216.0 * scale, quality=q, subsampling=2, optimize=True)
                mb = os.path.getsize(out) / 1e6
                if mb < MAX_MB or q <= MIN_Q: break
                q -= 4
            if mb < MAX_MB: break
        print(f'{os.path.relpath(out, ROOT) if not OUT else out}: {len(PdfReader(out).pages)} pages, {mb:.1f} MB, JPEG quality {q}, {w}×{h}')
        if mb >= MAX_MB: print(f'  WARNING: over {MAX_MB} MB even at quality {MIN_Q}, slow on phones / WeChat')
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

if not OUT and os.path.exists(os.path.join(TALK, 'index.html')):
    f = os.path.join(TALK, 'index.html'); t = open(f, encoding='utf-8').read()
    for k, n in counts.items():
        t = re.sub(rf'data-n-{k}="\d+"', f'data-n-{k}="{n}"', t)
    open(f, 'w', encoding='utf-8').write(t)
    print(os.path.relpath(f, ROOT) + ' slide counts:', counts)
print('Done. Check ' + BASE + ' locally, then commit and push.')
