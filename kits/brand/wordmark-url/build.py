import sys, json, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
def render(pg, c, ink, bg, out, **kw):
    qs='&'.join(f'{k}={v}' for k,v in dict(c=c,ink=ink.replace('#','%23'),bg=bg.replace('#','%23'),**kw).items())
    pg.goto('http://127.0.0.1:8780/_kit/wordmark-url/?'+qs, wait_until='networkidle')
    pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    pg.locator('#lk').screenshot(path=out, omit_background=(bg=='transparent'))
def ink_rows(path, x0, x1):
    a=np.array(Image.open(path).convert('RGBA')); al=a[:,x0:x1,3]
    r=np.where((al>100).any(axis=1))[0]; return r.min(), r.max()
