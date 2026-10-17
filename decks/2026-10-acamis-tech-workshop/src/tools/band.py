"""Ink centering in a band between two edges: from the top of BOX to the top of a divider/next element.
Usage: python3 tools/band.py SLIDE "top-edge selector" "bottom-edge selector" [top-edge: top|bottom] [bottom-edge: top|bottom]"""
import sys, io, json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
from _serve import serve, open_export, goto
slide=int(sys.argv[1]); s1=sys.argv[2]; s2=sys.argv[3]; e1=sys.argv[4] if len(sys.argv)>4 else 'top'; e2=sys.argv[5] if len(sys.argv)>5 else 'bottom'
K=3; url=serve()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=K)
    open_export(pg,url); goto(pg,slide)
    r=pg.evaluate(f"(()=>{{const S=document.querySelectorAll('section.s')[{slide-1}];const a=S.querySelector({json.dumps(s1)}).getBoundingClientRect(),c=S.querySelector({json.dumps(s2)}).getBoundingClientRect();return [a.x,a.{e1},a.width,c.{e2}]}})()")
    x,y0,w,y1=[v*K for v in r]
    im=np.array(Image.open(io.BytesIO(pg.screenshot())).convert('L')).astype(int)
    c=im[round(y0)+4:round(y1)-4,round(x)+40:round(x+w)-40]; ink=np.abs(c-np.median(c))>45
    ys=np.where(ink.any(axis=1))[0]
    top=(ys.min()+4)/K; bot=(round(y1)-round(y0)-4-ys.max())/K
    print(f'band {(y1-y0)/K:.1f}px: ink top gap {top:.1f}, bottom gap {bot:.1f}, diff {top-bot:+.1f}')
    b.close()
