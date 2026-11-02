"""Strict layout audit for the v3 posters. python3 audit3.py [en cn]
Measures from rendered pixels and the DOM:
  1. phone size: every text run's on-screen size in a WeChat chat (poster 1080px shown 390pt wide), WCAG contrast
  2. centering: ink box inside pills/cards/rows (cap-to-baseline for pills: descender rows ignored)
  3. alignment: left ink edge of every block vs the margin
  4. line breaks: lines per text block, short last lines (EN < 3 words, CN < 5 chars)"""
import sys, io, json, numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
SCALE = 390 / 1080  # iPhone width in pt / poster width in CSS px

JS_TEXT = r"""
() => {
  const out = [];
  const lum = c => { const m = c.match(/[\d.]+/g).map(Number); const f = v => { v/=255; return v<=.03928? v/12.92 : Math.pow((v+.055)/1.055,2.4) }; return [.2126*f(m[0])+.7152*f(m[1])+.0722*f(m[2]), m[3]===undefined?1:m[3]] };
  const bgOf = el => { let e = el; while (e) { const c = getComputedStyle(e).backgroundColor; if (c && !/rgba\(0, 0, 0, 0\)|transparent/.test(c)) return c; e = e.parentElement } return 'rgb(255,255,255)' };
  const blocks = [...document.querySelectorAll('#poster h1, #poster h2, #poster p, #poster b, #poster .k, #poster .tag, #poster .v, #poster .h1b')].filter(e=>!e.closest('.ct-links') && !e.classList.contains('ct-links'));
  for (const el of blocks) {
    if (!el.textContent.trim()) continue;
    const cs = getComputedStyle(el);
    const r = document.createRange(); r.selectNodeContents(el);
    const rects = [...r.getClientRects()].filter(x => x.width > 2);
    const tops = [...new Set(rects.map(x => Math.round(x.top / 4)))];
    // last line text
    let lastLine = '';
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    const lastTop = Math.max(...rects.map(x => x.top));
    let n; while ((n = walker.nextNode())) { for (let i = 0; i < n.length; i++) { const rr = document.createRange(); rr.setStart(n, i); rr.setEnd(n, i + 1); const b = rr.getBoundingClientRect(); if (b.width && Math.abs(b.top - lastTop) < 6) lastLine += n.data[i] } }
    const [fl] = lum(cs.color), [bl] = lum(bgOf(el));
    const contrast = (Math.max(fl, bl) + .05) / (Math.min(fl, bl) + .05);
    const box = el.getBoundingClientRect();
    out.push({ tag: el.tagName.toLowerCase(), cls: el.className, text: el.textContent.trim().slice(0, 50), px: parseFloat(cs.fontSize), lines: tops.length, last: lastLine.trim(), contrast: +contrast.toFixed(2), left: Math.round(rects.length ? Math.min(...rects.map(x => x.left)) : box.left) });
  }
  return out;
}"""

def ink(img, thr=40, bg=None):
    a = img.astype(int); bgc = a[3, 3] if bg is None else np.array(bg)
    m = np.abs(a - bgc).sum(2) > thr
    return m

def gaps(m, optical=True):
    m = m.copy(); h, w = m.shape
    m[m.sum(1) > 0.6 * w] = False          # drop hairlines / rules
    if optical:
        rows = m.sum(1); mx = rows.max() if rows.max() else 1
        dense = np.where(rows > 0.22 * mx)[0]
        ys0 = np.where(rows > 0)[0]
        xs0 = np.where(m.sum(0) > 0)[0]
        if not len(ys0): return None
        return dict(top=ys0.min() / 2, bottom=(h - 1 - dense.max()) / 2, left=xs0.min() / 2, right=(w - 1 - xs0.max()) / 2)
    ys, xs = np.where(m)
    if not len(ys): return None
    h, w = m.shape
    return dict(top=ys.min() / 2, bottom=(h - 1 - ys.max()) / 2, left=xs.min() / 2, right=(w - 1 - xs.max()) / 2)

def capband(m):
    # cap/ascender top = first ink row; baseline = last row of the dense x-height band (descenders ignored)
    rows = m.sum(1); mx = rows.max(); idx = np.where(rows > mx * 0.22)[0]; ink_rows = np.where(rows > 0)[0]
    return ink_rows.min(), idx.max()

def run(name):
    rep = {}
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1600}, device_scale_factor=2)
        pg.goto(f'http://127.0.0.1:8795/_v3/{name}.html', wait_until='networkidle'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(600)
        texts = pg.evaluate(JS_TEXT)
        # 1 phone size
        small = [t for t in texts if t['px'] * SCALE < 9.0]
        body_min = min(t['px'] for t in texts if t['tag'] == 'p') * SCALE
        lowc = [t for t in texts if t['contrast'] < 4.5]
        rep['phone'] = dict(min_pt=round(min(t['px'] for t in texts) * SCALE, 1), body_min_pt=round(body_min, 1), under9pt=[(t['text'], round(t['px'] * SCALE, 1)) for t in small], low_contrast=[(t['text'], t['contrast']) for t in lowc])
        # 4 line breaks
        orph = []
        for t in texts:
            if t['lines'] < 2: continue
            short = (len(t['last'].split()) < 3) if name == 'en' else (len(t['last'].replace(' ', '')) < 5)
            if short: orph.append((t['text'], t['lines'], t['last']))
        rep['breaks'] = dict(multiline=[(t['text'][:30], t['lines']) for t in texts if t['lines'] > 1], short_last=orph)
        # 3 alignment: block left edges
        lefts = {}
        for t in texts:
            lefts.setdefault(t['left'], []).append(t['text'][:24])
        rep['lefts'] = {k: v[:4] for k, v in sorted(lefts.items())}
        # 2 centering
        cen = {}
        for i in range(pg.locator('.tag').count()):
            el = pg.locator('.tag').nth(i); im = np.array(Image.open(io.BytesIO(el.screenshot())).convert('RGB'))
            h, w, _ = im.shape; m = ink(im[4:h - 4, int(h * .4):w - int(h * .4)])
            t0, t1 = capband(m); cen[f'pill{i}'] = round((t0 + 4) / 2 - (h - 5 - (t1 + 4)) / 2, 1)
        for sel in ['.founders', '.cta']:
            el = pg.locator(sel).first; im = np.array(Image.open(io.BytesIO(el.screenshot())).convert('RGB'))
            h, w, _ = im.shape; bgc = im[h // 2, 10]
            mv = ink(im[6:h - 6, 40:w - 40], bg=bgc); gv = gaps(mv)
            mh = ink(im[40:h - 40, 6:w - 6], bg=bgc); gh = gaps(mh)
            g = dict(top=gv['top'] + 3, bottom=gv['bottom'] + 3, left=gh['left'] + 3, right=gh['right'] + 3)
            if sel == '.cta': g['right'] = None
            cen[sel] = dict(tb=round(g['top'] - g['bottom'], 1), top=g['top'], bottom=g['bottom'], left=g['left'], right=g['right'])
        # CTA text column vs QR: vertical centers
        cta = pg.locator('.cta').bounding_box(); ct = pg.locator('.cta .ct').bounding_box(); qr = pg.locator('.cta .qw').bounding_box()
        im = np.array(Image.open(io.BytesIO(pg.locator('.cta .ct').screenshot())).convert('RGB')); g = gaps(ink(im, bg=(11, 26, 74)))
        ct_ink_c = ct['y'] + (g['top'] + (ct['height'] - g['bottom'])) / 2
        cen['cta_text_vs_qr'] = round(ct_ink_c - (qr['y'] + qr['height'] / 2), 1)
        cen['qr_in_cta'] = round((qr['y'] - cta['y']) - (cta['y'] + cta['height'] - qr['y'] - qr['height']), 1)
        # facts rows: label and value share a baseline; text centered in the row
        rows = []
        for i in range(pg.locator('.fr').count()):
            el = pg.locator('.fr').nth(i); im = np.array(Image.open(io.BytesIO(el.screenshot())).convert('RGB'))
            m = ink(im, bg=im[im.shape[0] // 2, 2]); g = gaps(m); rows.append(round(g['top'] - g['bottom'], 1))
        cen['facts_rows_tb'] = rows
        # .do blocks: equal spacing above each label
        # grid: numeral left ink vs title left ink in each cell; even-column inset equal to odd-column inset
        cells = []
        for i in range(pg.locator('.grid4 li').count()):
            li = pg.locator('.grid4 li').nth(i); lb = li.bounding_box()
            def leftink(sel):
                el = li.locator(sel); bb = el.bounding_box()
                im = np.array(Image.open(io.BytesIO(el.screenshot())).convert('L'))
                xs = np.where((im < 170).any(0))[0]; return bb['x'] + xs.min() / 2
            cells.append(dict(title_x=round(leftink('b'), 1), body_x=round(leftink('p'), 1), title_vs_body=round(leftink('b') - leftink('p'), 1)))
        cen['grid_cells'] = cells
        rep['center'] = cen
        b.close()
    return rep

for n in sys.argv[1:] or ['en', 'cn']:
    print('=====', n); print(json.dumps(run(n), ensure_ascii=False, indent=1))
