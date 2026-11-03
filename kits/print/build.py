"""Render an Arena print document (A4, one or many .pg pages) to PDF.
Usage: python3 build.py <doc.html> <out.pdf>   (writes page PNGs to <doc dir>/review/)
The HTML references assets from the web root (/fonts/gf.css, /arena-print.css, /logos/..., /photos/...), served from
print-kit/site. Fails if any page's content runs into the running footer or off the page."""
import http.server, threading, functools, pathlib, sys
from playwright.sync_api import sync_playwright
KIT = pathlib.Path(__file__).parent
src, out = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
_txt = src.read_text()
_left = _txt.count('class="ph"') + _txt.count('{{')
if _left and '--allow-placeholders' not in sys.argv:
    sys.exit(f'{_left} unfilled placeholder(s) ([Write: ...] or {{{{...}}}}) in {src.name}; fill them, or pass --allow-placeholders for a sample render.')
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
H = functools.partial(Q, directory=str(KIT / 'site'))
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 794, 'height': 1123}, device_scale_factor=2)
    pg.goto(f'http://127.0.0.1:{port}/fonts/gf.css'); pg.set_content(src.read_text(), wait_until='networkidle')
    pg.emulate_media(media='print'); pg.evaluate('document.fonts.ready')
    print('fonts:', pg.evaluate("['Geist','Newsreader'].map(f=>f+'='+document.fonts.check('12px '+f))"))
    rows = pg.evaluate("""[...document.querySelectorAll('.pg')].map((s,i)=>{
      const r=s.getBoundingClientRect(), f=(s.querySelector('.rf')||s.lastElementChild).getBoundingClientRect();
      const inn=s.querySelector(':scope > .in');
      if (inn && inn.scrollHeight > inn.clientHeight + 1) return {page:i+1, ok:false, clearance:-(inn.scrollHeight-inn.clientHeight)};
      const kids=inn ? [...inn.children] : [...s.children].filter(c=>!c.classList.contains('rf'));
      const last=Math.max(...kids.map(c=>c.getBoundingClientRect().bottom));
      return {page:i+1, ok: f.bottom<=r.bottom+0.5, clearance: Math.round(f.top-last)}})""")
    for r in rows:
        ok = r['ok'] and r['clearance'] >= 8; bad += not ok
        print(('OK  ' if ok else 'FIX ') + f"page {r['page']}: free space above footer {r['clearance']}px")
    rev = src.parent / 'review'; rev.mkdir(exist_ok=True)
    for i, el in enumerate(pg.query_selector_all('.pg')):
        el.screenshot(path=str(rev / f'page-{i+1}.png'))
    pg.pdf(path=str(out), prefer_css_page_size=True, print_background=True, margin={'top':'0','right':'0','bottom':'0','left':'0'})
    b.close()
srv.shutdown()
from pypdf import PdfReader
print('pdf pages:', len(PdfReader(str(out)).pages), '->', out)
sys.exit(1 if bad else 0)
