"""Exact text centering inside a box: screenshot, hide only the text of each match (color: transparent),
screenshot again, and diff. The difference is the text's ink, nothing else (no borders, fills, or icons).
Usage: python3 tools/textbox.py SLIDE "selector" [--box "ancestor selector"]
  Without --box, the gaps are measured to the element's own border box (pills, buttons, cards).
  With --box, to the nearest ancestor matching that selector.
Reports gaps in screen px at 1920x1080: top/bottom and left/right, and the differences."""
import sys, io, json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
from _serve import serve, open_export, goto
slide=int(sys.argv[1]); sel=sys.argv[2]; box=sys.argv[sys.argv.index('--box')+1] if '--box' in sys.argv else None
K=3; url=serve()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=K)
    open_export(pg,url); goto(pg,slide)
    n=pg.evaluate(f"document.querySelectorAll('section.s')[{slide-1}].querySelectorAll({json.dumps(sel)}).length")
    for i in range(n):
        q=f"document.querySelectorAll('section.s')[{slide-1}].querySelectorAll({json.dumps(sel)})[{i}]"
        r=pg.evaluate(f"(()=>{{const e={q};const t={json.dumps(box)}?e.closest({json.dumps(box)}):e;const R=t.getBoundingClientRect();return [R.x,R.y,R.width,R.height,e.textContent.trim().slice(0,28)]}})()")
        a=np.array(Image.open(io.BytesIO(pg.screenshot())).convert('L')).astype(int)
        pg.evaluate(f"(()=>{{const e={q};e.dataset.tbc=e.style.cssText;e.style.setProperty('color','transparent','important');e.querySelectorAll('*').forEach(c=>{{c.dataset.tbc=c.style.cssText;c.style.setProperty('color','transparent','important');c.style.setProperty('-webkit-text-fill-color','transparent','important')}});e.style.setProperty('-webkit-text-fill-color','transparent','important')}})()")
        pg.wait_for_timeout(80)
        c=np.array(Image.open(io.BytesIO(pg.screenshot())).convert('L')).astype(int)
        pg.evaluate(f"(()=>{{const e={q};[e,...e.querySelectorAll('*')].forEach(c=>{{c.style.cssText=c.dataset.tbc||''}})}})()")
        x,y,w,h,t=[v*K if isinstance(v,(int,float)) else v for v in r]
        X,Y,W,H=round(x),round(y),round(w),round(h)
        d=np.abs(a-c)[Y:Y+H,X:X+W]>40
        ys=np.where(d.any(axis=1))[0]; xs=np.where(d.any(axis=0))[0]
        if not len(ys): print(repr(t),'no text ink'); continue
        top=ys.min()/K; bot=(H-1-ys.max())/K; lf=xs.min()/K; rt=(W-1-xs.max())/K
        print(f'{t!r:30} top {top:6.1f} bottom {bot:6.1f} diff {top-bot:+5.1f} | left {lf:6.1f} right {rt:6.1f} diff {lf-rt:+5.1f}')
    b.close()
