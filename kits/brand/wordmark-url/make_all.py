import json, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
from build import render
S,T,F,TR,W=open('params.txt').read().split(); S,T,F=int(S),int(T),int(F)
C=json.load(open('_parts/colors.json')); inks=C['inks']; bgs=C['bgs']
variants=[(f'{c}-transparent',c,inks[c],'transparent') for c in ['navy','beige','ivory','white']]+\
         [('navy-on-white','navy',inks['navy'],bgs['navy-on-white']),('navy-on-ivory','navy',inks['navy'],bgs['navy-on-ivory']),
          ('navy-on-beige','navy',inks['navy'],bgs['navy-on-beige']),('beige-on-navy','beige',inks['beige'],bgs['beige-on-navy'])]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':7452,'height':1130})
    for name,c,ink,bg in variants:
        pg.goto('about:blank'); out=f'arena-wordmark-url-{name}.png'
        render(pg,c,ink,bg,out,shift=S,f=F,tr=TR,top=T,w=W)
        im=Image.open(out).convert('RGBA')
        if bg=='transparent':
            a=np.array(im); a[:,:,3][a[:,:,3]<=8]=0; im=Image.fromarray(a); im.save(out)
        im.resize((1600,round(1130*1600/7452)),Image.LANCZOS).save(out.replace('.png','-1600.png'))
    b.close()
sheet=Image.new('RGB',(1640,8*290+20),(200,200,200))
order=[('navy-transparent',(243,233,221)),('beige-transparent',(21,38,54)),('ivory-transparent',(21,38,54)),('white-transparent',(90,90,90)),
       ('navy-on-white',None),('navy-on-ivory',None),('navy-on-beige',None),('beige-on-navy',None)]
for i,(n,bgc) in enumerate(order):
    im=Image.open(f'arena-wordmark-url-{n}-1600.png').convert('RGBA')
    tile=Image.new('RGBA',(1600,270),bgc+(255,) if bgc else (255,255,255,0)); tile.alpha_composite(im,(0,(270-im.height)//2))
    sheet.paste(tile.convert('RGB'),(20,20+i*290))
sheet.save('REVIEW-all-colorways.png'); print('done')
