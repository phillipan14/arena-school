import sys, json
from playwright.sync_api import sync_playwright
from center import measure
out=sys.argv[1] if len(sys.argv)>1 else 'poster.png'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1600},device_scale_factor=2)
    pg.goto('http://127.0.0.1:8780/_kit/lux-poster/index.html',wait_until='networkidle')
    pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(700)
    m=measure(pg)
    for r in m: print('before', r)
    # apply optical shift to each box's text
    if False: pg.evaluate("""(m)=>{const bs=document.querySelectorAll('.box');m.forEach(r=>{const t=bs[r.i].querySelector('.t-in');if(t)t.style.setProperty('--oy',r.shift+'px')})}""", m)
    pg.wait_for_timeout(200)
    for r in measure(pg): print('after ', r)
    json.dump({str(r['i']):r['shift'] for r in m}, open('shifts.json','w'))
    el=pg.locator('#poster'); print('size',el.bounding_box()['height'])
    over=pg.evaluate("""[...document.querySelectorAll('#poster *')].filter(e=>e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!=='hidden'&&e.clientWidth>0).map(e=>e.className||e.tagName)""")
    print('overflowing',over[:10])
    el.screenshot(path=out); b.close()
