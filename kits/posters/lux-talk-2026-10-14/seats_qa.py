import io, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
def gaps(pg):
    card=pg.locator('.loc'); cb=card.bounding_box(); seats=pg.locator('.loc .seats'); sb=seats.bounding_box()
    shot=pg.screenshot(clip={'x':sb['x'],'y':sb['y']+1,'width':sb['width'],'height':cb['y']+cb['height']-sb['y']-1},scale='device')
    a=np.array(Image.open(io.BytesIO(shot)).convert('RGB')).astype(int); bg=a[2,2]
    ink=np.where((np.abs(a-bg).sum(axis=2)>60).any(axis=1))[0]
    sc=a.shape[0]/(cb['y']+cb['height']-sb['y']-1)
    return (ink.min()+1)/sc, (a.shape[0]-1-ink.max())/sc
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1600},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8780/_kit/lux-poster/index.html',wait_until='networkidle'); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
    top,bot=gaps(pg); print('line→text %.1f  text→card bottom %.1f'%(top,bot))
    shift=(bot-top)/2; print('shift',round(shift,2))
    b.close()
