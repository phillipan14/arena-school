// Full-page screenshots of every site page with motion frozen, for before/after pixel diffs (tools/pixel_diff.py).
//   node tools/pixel_shots.mjs OUT_DIR WIDTH        (needs the local server on 127.0.0.1:8931)
import { chromium } from 'playwright';
import { readdirSync, mkdirSync } from 'fs';
const root = new URL('..', import.meta.url).pathname;
const [,, out, width = '1440'] = process.argv;
const W = +width; mkdirSync(out, { recursive: true });
const pages = [...readdirSync(root).filter(f => f.endsWith('.html')), ...['programs', 'events', 'schools', 'card'].flatMap(d => readdirSync(root + d).filter(f => f.endsWith('.html')).map(f => `${d}/${f}`))];
const FREEZE = `*,*::before,*::after{animation-play-state:paused!important;animation-delay:0s!important;animation-duration:0s!important;transition:none!important;caret-color:transparent!important}
.reveal,[data-reveal]{opacity:1!important;transform:none!important}video{visibility:hidden!important}`;
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: W, height: W < 500 ? 844 : 900 }, deviceScaleFactor: 1, isMobile: W < 500, hasTouch: W < 500, reducedMotion: 'reduce' });
for (const pg of pages) {
  const p = await ctx.newPage();
  await p.addInitScript(() => { Math.random = () => 0.42; const t0 = 1792166400000; Date.now = () => t0; });
  await p.goto('http://127.0.0.1:8931/' + pg, { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: FREEZE });
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); await document.fonts.ready; });
  await p.evaluate(() => document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; }));
  await p.waitForLoadState('networkidle'); await p.waitForTimeout(500);
  await p.screenshot({ path: `${out}/${pg.replace(/\//g, '_').replace('.html', '')}.png`, fullPage: true, animations: 'disabled' });
  await p.close();
}
await b.close(); console.log(`${pages.length} pages at ${W}`);
