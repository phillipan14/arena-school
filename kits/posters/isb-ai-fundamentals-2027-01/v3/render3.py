"""Render v3 posters @2x: python3 render3.py [en cn]. Needs ../../serve.py on :8795 (serves out/, falls back to live site)."""
import sys
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1600}, device_scale_factor=2)
    for name in sys.argv[1:] or ['en', 'cn']:
        pg.goto(f'http://127.0.0.1:8795/_v3/{name}.html', wait_until='load', timeout=90000); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(1500)
        over = pg.evaluate("""[...document.querySelectorAll('#poster *')].filter(e=>e.scrollWidth>e.clientWidth+1&&e.clientWidth>0).map(e=>(e.className||e.tagName)+':'+e.textContent.slice(0,30))""")
        el = pg.locator('#poster'); print(name, 'height', round(el.bounding_box()['height']), 'overflow', over)
        el.screenshot(path=f'out-{name}.png')
        im = Image.open(f'out-{name}.png').convert('RGB'); im.save(f'AI-Fundamentals-{name.upper()}.jpg', quality=90)
        im.resize((540, im.height // 4)).save(f'prev-{name}.png')
    b.close()
