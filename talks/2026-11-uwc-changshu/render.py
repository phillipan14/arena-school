"""Regenerate presentation exports from the single canonical deck.html."""
from pathlib import Path
import html
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

P = Path(__file__).resolve().parent
soup = BeautifulSoup((P / 'deck.html').read_text(), 'html.parser')
slides = soup.select('#stage > section')
assert slides, 'No slides found in deck.html'
(P / 'slides').mkdir(exist_ok=True)
with sync_playwright() as w:
    browser = w.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce')
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto((P / 'deck.html').as_uri())
    page.evaluate('document.fonts.ready')
    for i in range(len(slides)):
        page.evaluate('show(' + str(i) + ')')
        page.locator('section.active').screenshot(path=str(P / 'slides' / f'{i+1:02}.png'))
    assert not errors, errors
    page.pdf(path=str(P / 'slides.pdf'), print_background=True, prefer_css_page_size=True)
    page.goto((P / 'student-guide.html').as_uri())
    page.evaluate('document.fonts.ready')
    page.add_style_tag(content='@media print{body{margin:0;padding:0;font-size:11pt}h1{font-size:28pt}h2{font-size:19pt;break-after:avoid}h3{break-after:avoid}tr,blockquote{break-inside:avoid}header{margin-bottom:20px}a{overflow-wrap:anywhere}}')
    page.pdf(path=str(P / 'student-guide.pdf'), format='A4', margin={'top':'16mm','bottom':'16mm','left':'15mm','right':'15mm'}, print_background=True)
    browser.close()
# Remove obsolete generated pages only if the slide count was reduced.
for f in (P / 'slides').glob('*.png'):
    if f.stem.isdigit() and int(f.stem) > len(slides):
        f.unlink()
reader = BeautifulSoup((P / 'read.html').read_text(), 'html.parser')
for section in reader.select('section'):
    section.decompose()
container = reader.body or reader
for i, slide in enumerate(slides):
    title = slide.h1.get_text(' ', strip=True)
    body = slide.select_one('.content').decode_contents()
    fragment = BeautifulSoup(f'<section><h2>{i+1:02}. {html.escape(title)}</h2><img loading="lazy" src="slides/{i+1:02}.png" alt="{html.escape(title, quote=True)}"><details><summary>Read slide text</summary>{body}</details></section>', 'html.parser')
    container.append(fragment)
(P / 'read.html').write_text(str(reader))
print(f'Exported {len(slides)} slides, PDF, mobile reader, and student-guide PDF.')
