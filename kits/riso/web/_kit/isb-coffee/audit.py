# Audit: stray last words, overflow, small text, QR decodability on a phone-sized image.
import sys, cv2, numpy as np
from playwright.sync_api import sync_playwright
JS=r"""()=>{
 const out={orphans:[],overflow:[],small:[]};
 const blocks=[...document.querySelectorAll('#poster h1,#poster p,#poster li,#poster .big,#poster .time,#poster .lab,#poster .role,#poster .nm b,#poster .alt,#poster .tag,#poster .chip,#poster .fmt,#poster .event b,#poster .event span,#poster .foot span')];
 for(const el of blocks){
   const r=document.createRange(); r.selectNodeContents(el);
   const rects=[...r.getClientRects()].filter(x=>x.width>1);
   const fs=parseFloat(getComputedStyle(el).fontSize);
   const tops=[]; rects.map(x=>x.top+x.height/2).sort((p,q)=>p-q).forEach(t=>{if(!tops.length||t-tops[tops.length-1]>fs*0.7)tops.push(t)}); const lines=tops.length; if(fs<23.5) out.small.push(el.className+' '+fs+'px: '+el.textContent.trim().slice(0,30));
   if(lines>1){
     const lastMid=tops[tops.length-1]; const lastRects=rects.filter(x=>Math.abs(x.top+x.height/2-lastMid)<fs*0.7);
     const w=lastRects.reduce((a,x)=>a+x.width,0); const full=el.getBoundingClientRect().width;
     if(w<full*0.22) out.orphans.push(`${lines} lines, last line ${Math.round(w)}/${Math.round(full)}px: ${el.textContent.trim().slice(0,60)}`);
   }
   const box=el.closest('.card')||document.getElementById('poster'); const b=box.getBoundingClientRect(), e=el.getBoundingClientRect();
   const tr=Math.max(...rects.map(x=>x.right)); if(el.scrollWidth>el.clientWidth+1 && el.clientWidth>0 || (box.id!=='poster' && tr>b.right-10) || e.left<b.left) out.overflow.push(el.textContent.trim().slice(0,40)+` (text right ${Math.round(tr)}, card right ${Math.round(b.right)})`);
 }
 return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1600},device_scale_factor=2)
    for n in sys.argv[1:]:
        pg.goto(f'http://127.0.0.1:8781/_kit/isb-coffee/{n}.html',wait_until='networkidle'); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        # optical centering of pill/badge text: measure ink rows, shift so ink is centered in the pill
        pg.add_style_tag(content='.box::before,.box>i{visibility:hidden!important}')
        bx=pg.locator('.box'); shifts=[]
        for i in range(bx.count()):
            el=bx.nth(i); bb=el.bounding_box(); import io; from PIL import Image as _I
            arr=np.array(_I.open(io.BytesIO(el.screenshot(scale='device'))).convert('RGB')).astype(int)
            H=arr.shape[0]; bg=arr[H//2,3]; w=arr.shape[1]; sub=arr[:,int(w*.12):int(w*.9)]
            rows=np.where((np.abs(sub-bg).sum(2)>110).any(1))[0]; sc=H/bb['height']
            off=round(((H-1-rows.max())-rows.min())/2/sc,2); shifts.append(off)
            el.locator('.t-in').evaluate('(e,o)=>e.style.setProperty("--oy",o+"px")',off)
        pg.evaluate("document.querySelectorAll('style').forEach(s=>{if(s.textContent.includes('visibility:hidden!important'))s.remove()})")
        # question tiles: center the text ink (number hidden) inside each tile
        pg.add_style_tag(content='.q .n{visibility:hidden!important}')
        qt=pg.locator('.q'); qsh=[]
        for i in range(qt.count()):
            el=qt.nth(i); bb=el.bounding_box()
            arr=np.array(_I.open(io.BytesIO(el.screenshot(scale='device'))).convert('RGB')).astype(int)
            H=arr.shape[0]; bg=arr[H//2,6]; w=arr.shape[1]; sub=arr[:,int(w*.08):int(w*.95)]
            rows=np.where((np.abs(sub-bg).sum(2)>110).any(1))[0]; sc=H/bb['height']
            off=round(((H-1-rows.max())-rows.min())/2/sc+2,2); qsh.append(off)  # +2px optical bias: text reads high when exactly centered
            el.evaluate('(e)=>e.style.setProperty("--qy","1.5px")')  # flex centers; fixed optical nudge (ink-measuring misread card-edge pixels)
        pg.evaluate("document.querySelectorAll('style').forEach(s=>{if(s.textContent.includes('visibility:hidden!important'))s.remove()})")
        print('  pill shifts (px):',[float(x) for x in shifts],' tile shifts (px):',[float(x) for x in qsh])
        res=pg.evaluate(JS); h=pg.locator('#poster').bounding_box()['height']
        print(f'== {n}: {1080}x{round(h)} (ratio {h/1080:.2f}; A4=1.41)')
        for k,v in res.items(): print(f'  {k}: {len(v)}'); [print('    -',x) for x in v]
        pg.locator('#poster').screenshot(path=f'out-{n}.png')
        img=cv2.imread(f'out-{n}.png'); ph=cv2.resize(img,(1170,int(img.shape[0]*1170/img.shape[1])),interpolation=cv2.INTER_AREA)
        print('  QR at phone width (1170px):', cv2.QRCodeDetector().detectAndDecode(ph)[0][:45] or 'NOT DECODED')
    b.close()
