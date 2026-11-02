import io, sys, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1600},device_scale_factor=2)
    for n in sys.argv[1:] or ['en','cn']:
        pg.goto(f'http://127.0.0.1:8795/_v3/{n}.html',wait_until='networkidle'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
        rects=pg.evaluate("""(()=>{const h=document.querySelector('h1');const r=document.createRange();r.selectNodeContents(h);
          const ls={};for(const x of r.getClientRects()){if(x.width<3)continue;const k=Math.round(x.top/10);(ls[k]=ls[k]||[]).push(x)}
          return Object.values(ls).map(a=>({top:Math.min(...a.map(x=>x.top)),bottom:Math.max(...a.map(x=>x.bottom))}))})()""")
        for i,r in enumerate(rects):
            y0=r['top']+r['height']*0 if False else r['top']; h=r['bottom']-r['top']
            im=np.array(Image.open(io.BytesIO(pg.screenshot(clip={'x':0,'y':y0+h*.15,'width':400,'height':h*.6}))).convert('L'))
            xs=np.where((im<160).any(0))[0]; print(n,'h1 line',i,'left ink',xs.min()/2)
    b.close()
