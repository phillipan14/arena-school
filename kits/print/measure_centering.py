"""Measure optical centering of digits inside .num squares and ol.num-list circles (ink bbox vs shape bbox)."""
import http.server, threading, functools, pathlib, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
KIT = pathlib.Path(__file__).parent; src = pathlib.Path(sys.argv[1]).resolve()
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Q, directory=str(KIT / 'site')))
threading.Thread(target=srv.serve_forever, daemon=True).start()
S = 4
def ink_box(img, fg):
    W, H = img.size; xs = []; ys = []
    px = img.load()
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y][:3]
            if fg(r, g, b): xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 794, 'height': 1123}, device_scale_factor=S)
    pg.goto(f'http://127.0.0.1:{srv.server_address[1]}/fonts/gf.css'); pg.set_content(src.read_text(), wait_until='networkidle')
    pg.emulate_media(media='print'); pg.evaluate('document.fonts.ready')
    shapes = pg.evaluate("""(()=>{const out=[];const mm=96/25.4;
      document.querySelectorAll('.num').forEach(e=>{const r=e.getBoundingClientRect();out.push({k:'square '+e.textContent,x:r.x,y:r.y+scrollY,w:r.width,h:r.height})});
      document.querySelectorAll('ol.num-list li').forEach((e,i)=>{const r=e.getBoundingClientRect();out.push({k:'circle '+(e.parentElement.children.length)+'-'+([...e.parentElement.children].indexOf(e)+1),x:r.x,y:r.y+scrollY+0.15*mm,w:4.6*mm,h:4.6*mm})});
      return out})()""")
    full = Image.open(io.BytesIO(pg.screenshot(full_page=True))).convert('RGB')
    for sh in shapes:
        x0, y0, w, h = [round(v * S) for v in (sh['x'], sh['y'], sh['w'], sh['h'])]
        ins = round(min(w, h) * 0.18)
        crop = full.crop((x0 + ins, y0 + ins, x0 + w - ins, y0 + h - ins))
        if sh['k'].startswith('square'):
            fg = lambda r, g, b: r > 170 and g > 170 and b > 170
        else:
            fg = lambda r, g, b: b > 120 and r < 110
        bb = ink_box(crop, fg)
        if not bb: print(sh['k'], 'no ink'); continue
        cw, ch = crop.size
        dx = ((bb[0] + bb[2]) / 2 - (cw - 1) / 2) / S; dy = ((bb[1] + bb[3]) / 2 - (ch - 1) / 2) / S
        print(f"{sh['k']:<14} ink offset from center: dx {dx:+.2f}px  dy {dy:+.2f}px (CSS px)")
    b.close()
srv.shutdown()
