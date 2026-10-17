"""Sweep every slide for off-center text inside boxed elements (cards, panes, pills, chips, list rows).
For each visible boxed element (has a fill, a border, or a radius), measures the text-ink gaps to its box
edges by hiding the element's own text and diffing. Flags |top-bottom| > TOL px (vertical) for elements whose
text is meant to be centered (single-line pills/chips/buttons: both axes).
Usage: python3 tools/sweep.py [first-last] [--tol 2]"""
import sys, io, json
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
from _serve import serve, open_export, goto
rng=sys.argv[1] if len(sys.argv)>1 and '-' in sys.argv[1] else '1-28'; a0,a1=map(int,rng.split('-'))
TOL=float(sys.argv[sys.argv.index('--tol')+1]) if '--tol' in sys.argv else 2.0
K=2; url=serve()
JS=r"""(n)=>{const S=document.querySelectorAll('section.s')[n];const out=[];let i=0;
for(const e of S.querySelectorAll('*')){const c=getComputedStyle(e);if(c.display==='none'||c.visibility==='hidden'||+c.opacity===0)continue;
 const R=e.getBoundingClientRect();if(R.width<24||R.height<16||R.height>700)continue;
 const boxed=(c.backgroundColor!=='rgba(0, 0, 0, 0)'&&c.backgroundColor!=='transparent')||parseFloat(c.borderTopWidth)>0||c.boxShadow.includes('inset')||parseFloat(c.borderTopLeftRadius)>6;
 if(!boxed)continue; if(!e.textContent.trim())continue; if(e.closest('svg'))continue; if(['IMG','svg','SECTION'].includes(e.tagName))continue;
 if(e.classList.contains('w')||e.classList.contains('bd'))continue;
 const pill=R.height<70&&R.width<420&&parseFloat(c.borderTopLeftRadius)>=R.height/2-2;
 e.dataset.sw=String(i);out.push([i,R.x,R.y,R.width,R.height,pill,e.className.toString().slice(0,40),e.textContent.trim().replace(/\s+/g,' ').slice(0,36)]);i++}
return out}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=K)
    open_export(pg,url)
    for n in range(a0,a1+1):
        goto(pg,n); els=pg.evaluate(JS,n-1)
        for i,x,y,w,h,pill,cls,txt in els:
            q=f"document.querySelectorAll('section.s')[{n-1}].querySelector('[data-sw=\"{i}\"]')"
            A=np.array(Image.open(io.BytesIO(pg.screenshot(clip={'x':x,'y':y,'width':w,'height':h}))).convert('L')).astype(int)
            pg.evaluate(f"(()=>{{const e={q};[e,...e.querySelectorAll('*')].forEach(c=>{{c.dataset.swc=c.style.cssText;c.style.setProperty('color','transparent','important');c.style.setProperty('-webkit-text-fill-color','transparent','important')}})}})()")
            B=np.array(Image.open(io.BytesIO(pg.screenshot(clip={'x':x,'y':y,'width':w,'height':h}))).convert('L')).astype(int)
            pg.evaluate(f"(()=>{{const e={q};[e,...e.querySelectorAll('*')].forEach(c=>{{c.style.cssText=c.dataset.swc||''}})}})()")
            if A.shape!=B.shape: continue
            d=np.abs(A-B)>40; ys=np.where(d.any(axis=1))[0]; xs=np.where(d.any(axis=0))[0]
            if not len(ys): continue
            top=ys.min()/K; bot=(A.shape[0]-1-ys.max())/K; lf=xs.min()/K; rt=(A.shape[1]-1-xs.max())/K
            flag=abs(top-bot)>TOL or (pill and abs(lf-rt)>TOL)
            if flag: print(f'slide {n:2d} {"PILL" if pill else "box "} {cls[:28]:28} {txt[:30]!r:34} top {top:5.1f} bot {bot:5.1f} dv {top-bot:+5.1f}'+(f' | lf {lf:5.1f} rt {rt:5.1f} dh {lf-rt:+5.1f}' if pill else ''))
    b.close()
