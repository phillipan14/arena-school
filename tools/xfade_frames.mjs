// Frame capture for the homepage hero's rotating word (XFADE): screenshots of the word slot as fast as the
// browser allows (about every 50ms) across three word changes, plus the headline box per frame.
//   node tools/xfade_frames.mjs OUT_DIR [PAGE WIDTH ...]     then: python3 tools/xfade_check.py OUT_DIR
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'fs';
const [,, out, ...rest] = process.argv;
const runs = rest.length ? rest.reduce((a, x, i) => (i % 2 ? a[a.length - 1].push(+x) : a.push([x]), a), []) : [['index.html', 1440], ['index-cn.html', 1440], ['index.html', 390], ['index-cn.html', 390]];
const b = await chromium.launch();
for (const [pg, W] of runs) {
  const dir = `${out}/${pg.replace('.html', '')}-${W}`; mkdirSync(dir, { recursive: true });
  const p = await b.newPage({ viewport: { width: W, height: W < 500 ? 844 : 900 }, isMobile: W < 500, deviceScaleFactor: 1, reducedMotion: process.env.REDUCE ? 'reduce' : 'no-preference' });
  await p.goto('http://127.0.0.1:8931/' + pg, { waitUntil: 'networkidle' });
  await p.waitForTimeout(1800);
  const geo = () => p.evaluate(() => { const h = document.querySelector('.cine-hero h1').getBoundingClientRect(), r = document.querySelector('[data-rot]').getBoundingClientRect();
    return { h1: [h.left, h.top, h.width, h.height].map(Math.round), slot: [r.left, r.top, r.width, r.height].map(Math.round), on: document.querySelector('[data-rot] .is-on')?.textContent || '' }; });
  const g0 = await geo();
  const widest = await p.evaluate(() => Math.max(...[...document.querySelector('[data-rot]').children].map(s => s.scrollWidth)));
  const pad = 6, clip = { x: Math.max(0, g0.slot[0] - pad), y: g0.slot[1] - pad, width: Math.max(g0.slot[2], widest) + pad * 2, height: g0.slot[3] + pad * 2 };
  const frames = []; const t0 = Date.now(); let n = 0;
  while (Date.now() - t0 < 9600) {
    const t = Date.now() - t0;
    await p.screenshot({ path: `${dir}/f${String(n).padStart(3, '0')}.png`, clip, animations: 'allow' });
    frames.push({ n, t, ...(await geo()) }); n++;
  }
  // empty-slot reference: the same clip with every word hidden
  await p.evaluate(() => document.querySelectorAll('[data-rot] > *').forEach(s => s.style.setProperty('visibility', 'hidden', 'important'))); await p.waitForTimeout(100);
  await p.screenshot({ path: `${dir}/empty.png`, clip });
  writeFileSync(`${dir}/frames.json`, JSON.stringify({ pg, W, clip, frames }, null, 1));
  console.log(pg, W, frames.length, 'frames, mean interval', Math.round(9600 / frames.length), 'ms, words seen:', [...new Set(frames.map(f => f.on))].join(' '));
  await p.close();
}
await b.close();
