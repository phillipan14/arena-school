"""Measure ink centering inside boxes: the gap from each box edge to the first visible pixel.
JJ checks centering by ink, not by CSS boxes; aim for |diff| <= 1.5px.
Usage: python3 tools/ink.py SLIDE "CSS selector" [--inset 30]
  --inset skips N screen px at each edge (use ~30 to skip a card's own border/shadow, ~8 for thin panes).
Numbers are in screen px at 1920x1080 (CSS px x 1.32 inside .w)."""
import sys, io, json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
from _serve import serve, open_export, goto
slide=int(sys.argv[1]); sel=sys.argv[2]; inset=int(sys.argv[sys.argv.index('--inset')+1]) if '--inset' in sys.argv else 30
url=serve(); K=3; I=inset*K//3
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=K)
    open_export(pg,url); goto(pg,slide)
    rs=pg.evaluate(f"[...document.querySelectorAll('section.s')[{slide-1}].querySelectorAll({json.dumps(sel)})].map(e=>{{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height,e.textContent.trim().slice(0,30)]}})")
    shot=np.array(Image.open(io.BytesIO(pg.screenshot())).convert('L')).astype(int)
    for x,y,w,h,t in rs:
        X,Y,W,H=[round(v*K) for v in (x,y,w,h)]
        c=shot[Y+I:Y+H-I,X+I:X+W-I]; ink=np.abs(c-np.median(c))>45
        ys=np.where(ink.any(axis=1))[0]; xs=np.where(ink.any(axis=0))[0]
        if not len(ys): print(repr(t),'no ink'); continue
        top=(ys.min()+I)/K; bot=(H-ys.max()-I)/K; lf=(xs.min()+I)/K; rt=(W-xs.max()-I)/K
        print(f'{t!r:34} top {top:6.1f} bottom {bot:6.1f} diff {top-bot:+5.1f} | left {lf:6.1f} right {rt:6.1f} diff {lf-rt:+5.1f}')
    b.close()
