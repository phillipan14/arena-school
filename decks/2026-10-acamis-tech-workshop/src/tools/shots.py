"""Screenshot slides in their final (export) state and report any slide taller than 1080px.
Usage: python3 tools/shots.py OUTDIR [7,25]      (no list = every slide)"""
import sys, os
from playwright.sync_api import sync_playwright
from _serve import serve, open_export, goto
out=sys.argv[1]; only=[int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else None
os.makedirs(out,exist_ok=True); url=serve()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080}); errs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); open_export(pg,url)
    n=pg.evaluate("document.querySelectorAll('section.s').length")
    tall=pg.evaluate("[...document.querySelectorAll('section.s')].map((s,i)=>[i+1,Math.max(s.offsetHeight,s.scrollHeight)]).filter(x=>x[1]>1080)")
    print('slides',n,'| taller than 1080:',tall or 'none','| page errors:',errs or 'none')
    for i in range(1,n+1):
        if only and i not in only: continue
        goto(pg,i); pg.screenshot(path=f'{out}/{i:02d}.png')
    b.close()
