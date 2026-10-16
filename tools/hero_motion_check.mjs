// Hero photo motion check (HERO2-BRIEF B): at 1440, frames 2s apart (0, 2, 4, 6s) on a page in both motion
// modes; records which photo is on screen, its zoom, and sharpness (source px per CSS px at the max zoom).
//   node tools/hero_motion_check.mjs OUT_DIR PAGE [PAGE ...]     then: python3 tools/hero_motion_check.py OUT_DIR
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'fs';
const [,, out, ...pages] = process.argv; mkdirSync(out, { recursive: true });
const b = await chromium.launch(); const res = [];
for (const pg of pages) for (const mode of ['no-preference', 'reduce']) {
  const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, reducedMotion: mode });
  await p.goto('http://127.0.0.1:8931/' + pg, { waitUntil: 'networkidle' }); await p.waitForTimeout(1000);
  const name = pg.replace('.html', '').replace(/\//g, '_');
  for (const t of [0, 2, 4, 6]) {
    if (t) await p.waitForTimeout(2000);
    const s = await p.evaluate(async () => {
      const slides = [...document.querySelectorAll('section.cine-hero .cine-slide')];
      const op = slides.map(x => +getComputedStyle(x).opacity);
      const k = op.indexOf(Math.max(...op)); const img = slides[k].querySelector('img');
      const m = new DOMMatrix(getComputedStyle(img).transform); const base = img.offsetWidth;
      // the file's own pixel width (naturalWidth on a srcset image is corrected by the sizes value)
      const raw = new Image(); raw.src = img.currentSrc; await raw.decode().catch(() => {});
      return { on: k, op: op.map(v => v.toFixed(2)).join('/'), scale: +m.a.toFixed(3), tx: Math.round(m.e), ty: Math.round(m.f), base, natural: raw.naturalWidth, src: (img.currentSrc || '').split('/').pop() };
    });
    await p.screenshot({ path: `${out}/${name}-${mode === 'reduce' ? 'reduce' : 'nopref'}-${t}s.png`, clip: { x: 0, y: 0, width: 1440, height: 900 } });
    res.push({ page: pg, mode, t, ...s });
  }
  await p.close();
}
writeFileSync(`${out}/motion.json`, JSON.stringify(res, null, 1)); await b.close();
