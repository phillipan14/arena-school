# Measure the ink box of each .box's text and return the offset that centers it vertically.
import io, json
import numpy as np
from PIL import Image
def measure(pg, apply=None):
    pg.add_style_tag(content=".box::before,.box>i{visibility:hidden!important}")
    res=[]
    boxes=pg.locator('.box')
    for i in range(boxes.count()):
        el=boxes.nth(i); bb=el.bounding_box()
        png=el.screenshot(scale='device'); a=np.array(Image.open(io.BytesIO(png)).convert('RGB')).astype(int)
        H=a.shape[0]; bg=a[H//2, 2]  # edge pixel = background
        # inner area only (skip rounded corners): middle 70% width
        w=a.shape[1]; sub=a[:, int(w*.15):int(w*.85)]
        diff=np.abs(sub-bg).sum(axis=2)>90
        rows=np.where(diff.any(axis=1))[0]
        top=rows.min(); bot=H-1-rows.max(); scale=H/bb['height']
        off=(bot-top)/2/scale
        res.append(dict(i=i, cls=el.get_attribute('class'), top_px=top/scale, bottom_px=bot/scale, shift=round(off,2)))
    pg.evaluate("document.querySelectorAll('style').forEach(s=>{if(s.textContent.includes('visibility:hidden!important'))s.remove()})")
    return res
