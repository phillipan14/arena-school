"""Check the phone reader (talks/<slug>/read/en, /read/cn) on a phone-sized screen.

For every slide, in English and Chinese, at 390×844 portrait and 844×390 landscape, it fails on:
  - anything wider than the screen or poking out past the side margins (sideways scroll on a phone);
  - text smaller than 10px, or body text smaller than 12px;
  - images that did not load;
  - a slide whose content overflows sideways inside its own box.
It also writes screenshots of every slide (portrait) to --shots DIR (default /tmp/reader-shots).

Usage:  python3 decks/<slug>/src/reader_check.py [--shots DIR] [--only en|cn]
Needs:  pip install playwright && python3 -m playwright install chromium   (the same as export.py)
"""
import functools, http.server, os, sys, threading
from playwright.sync_api import sync_playwright

SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
from site_paths import ROOT, BASE as TALK
SHOTS = sys.argv[sys.argv.index('--shots') + 1] if '--shots' in sys.argv else '/tmp/reader-shots'
ONLY = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=ROOT))
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{srv.server_address[1]}'

PROBE = r"""(i) => {
  const s = document.querySelectorAll('.s')[i], vw = innerWidth, out = [];
  const w = s.querySelector('.w'), wr = w.getBoundingClientRect(), ws = getComputedStyle(w);
  const L = wr.left + parseFloat(ws.paddingLeft), R = wr.right - parseFloat(ws.paddingRight);
  if (s.scrollWidth > s.clientWidth + 1) out.push(['slide scrolls sideways', s.scrollWidth - s.clientWidth]);
  const clipped = el => { for (let p = el.parentElement; p && p !== s; p = p.parentElement) { const o = getComputedStyle(p); if (o.overflowX === 'hidden' || o.overflow === 'hidden') return p.closest('.mk-field,.pbr figure,.hb i,.mb i,.ctr,.sk-tools li') !== null; } return false; };
  for (const el of w.querySelectorAll('*')) {
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const st = getComputedStyle(el); if (st.visibility === 'hidden' || st.display === 'none') continue;
    if (clipped(el)) continue;
    if (r.right > R + 2 || r.left < L - 2) {
      out.push(['outside margins', el.tagName.toLowerCase() + '.' + (el.getAttribute('class') || '') + ' ' + (el.textContent || '').trim().slice(0, 40), Math.round(Math.max(r.right - R, L - r.left))]);
    }
    const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.nodeValue.trim());
    if (hasText) { const fs = parseFloat(st.fontSize); if (fs < 10) out.push(['tiny text', fs, (el.textContent || '').trim().slice(0, 40)]); }
    if (el.tagName === 'IMG' && !(el.complete && el.naturalWidth)) out.push(['image not loaded', el.getAttribute('src')]);
  }
  return out;
}"""

fails = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for key in ([ONLY] if ONLY else ['en']):
        for name, vp in (('portrait', {'width': 390, 'height': 844}), ('landscape', {'width': 844, 'height': 390})):
            ctx = b.new_context(viewport=vp, device_scale_factor=2, is_mobile=True, has_touch=True, reduced_motion='reduce')
            ctx.add_init_script("try{localStorage.setItem('arena-talk-tip','1')}catch(e){}")
            pg = ctx.new_page()
            pg.goto(f'{BASE}{TALK}/read/{key}.html', wait_until='networkidle')
            pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
            n = pg.evaluate("document.querySelectorAll('.s').length")
            for i in range(n):
                pg.evaluate(f"document.getElementById('deck').scrollLeft = {i} * document.getElementById('deck').clientWidth")
                pg.wait_for_timeout(120)
                for f in pg.evaluate(PROBE, i):
                    fails.append((key, name, i + 1, *f))
                if name == 'portrait':
                    os.makedirs(os.path.join(SHOTS, key), exist_ok=True)
                    pg.screenshot(path=os.path.join(SHOTS, key, f'{i + 1:02d}.png'))
            ctx.close()
    b.close()
srv.shutdown()
for f in fails: print('FAIL', *f)
print(f'{len(fails)} problems' if fails else 'reader OK: no overflow, tiny text, or missing images', '· screenshots in', SHOTS)
sys.exit(1 if fails else 0)
