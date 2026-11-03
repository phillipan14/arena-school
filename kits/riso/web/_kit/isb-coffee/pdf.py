# Vector PDF (live text, embedded images) for Canva import. Applies the same optical nudges as audit.py.
import io, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
import pathlib
O=str(pathlib.Path(__file__).resolve().parents[4]/'posters'/'isb-parent-coffee-2026-10-14')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1527},device_scale_factor=2)
    for n in ['en','cn']:
        pg.goto(f'http://127.0.0.1:8781/_kit/isb-coffee/{n}.html',wait_until='networkidle'); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        pg.evaluate("document.querySelectorAll('.q').forEach(e=>e.style.setProperty('--qy','1.5px'))")
        pg.add_style_tag(content='.box::before,.box>i{visibility:hidden!important}')
        bx=pg.locator('.box')
        for i in range(bx.count()):
            el=bx.nth(i); bb=el.bounding_box(); arr=np.array(Image.open(io.BytesIO(el.screenshot(scale='device'))).convert('RGB')).astype(int)
            H=arr.shape[0]; bg=arr[H//2,3]; w=arr.shape[1]; sub=arr[:,int(w*.12):int(w*.9)]
            rows=np.where((np.abs(sub-bg).sum(2)>110).any(1))[0]; off=round(((H-1-rows.max())-rows.min())/2/(H/bb['height']),2)
            el.locator('.t-in').evaluate('(e,o)=>e.style.setProperty("--oy",o+"px")',off)
        pg.evaluate("document.querySelectorAll('style').forEach(s=>{if(s.textContent.includes('visibility:hidden!important'))s.remove()})")
        pg.add_style_tag(content='@page{size:1080px 1527px;margin:0} html,body{background:none!important;margin:0} .poster{margin:0!important}')
        out=f'{O}/ISB-Parent-Coffee-{n.upper()}-for-Canva.pdf'
        pg.pdf(path=out,width='1080px',height='1527px',print_background=True,margin={'top':'0','right':'0','bottom':'0','left':'0'})
        print('wrote',out)
    b.close()
