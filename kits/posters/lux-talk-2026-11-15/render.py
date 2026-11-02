import sys
from playwright.sync_api import sync_playwright
out=sys.argv[1] if len(sys.argv)>1 else 'poster.png'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8781/_kit/lux-poster-1115/index.html',wait_until='networkidle')
    pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(700)
    over=pg.evaluate("""[...document.querySelectorAll('#poster *')].filter(e=>e.scrollWidth>e.clientWidth+1&&e.clientWidth>0).map(e=>e.className||e.tagName)""")
    print('overflowing',over[:10])
    print('poster height', pg.evaluate("document.getElementById('poster').getBoundingClientRect().height"))
    print('TALK vs logo centers', pg.evaluate("""(()=>{const l=document.querySelector('.mod img').getBoundingClientRect(),t=document.querySelector('.mod .t-in').getBoundingClientRect();return [l.top+l.height/2,t.top+t.height/2]})()"""))
    pg.locator('#poster').screenshot(path=out); b.close()
