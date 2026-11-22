import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1600},device_scale_factor=2)
    for name in sys.argv[1:]:
        pg.goto(f'http://127.0.0.1:8781/_kit/isb-coffee/{name}.html',wait_until='networkidle'); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(600)
        over=pg.evaluate("""[...document.querySelectorAll('#poster *')].filter(e=>e.scrollWidth>e.clientWidth+1&&e.clientWidth>0&&!e.closest('.ph')).map(e=>(e.className||e.tagName)+':'+e.textContent.slice(0,30))""")
        el=pg.locator('#poster'); print(name,'height',el.bounding_box()['height'],'overflow',over)
        el.screenshot(path=f'out-{name}.png')
    b.close()
