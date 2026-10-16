import { chromium } from 'playwright';
import { readdirSync } from 'fs';
const root = '/Users/phillipan/arena-elegance';
const lang = process.argv[2] || 'en';
const pages = [...readdirSync(root).filter(f => f.endsWith('.html')), ...['programs', 'events', 'schools', 'card'].flatMap(d => readdirSync(`${root}/${d}`).filter(f => f.endsWith('.html')).map(f => `${d}/${f}`))]
  .filter(p => lang === 'cn' ? p.endsWith('-cn.html') : !p.endsWith('-cn.html'));
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
for (const pg of pages) {
  await p.goto(`http://127.0.0.1:8931/${pg}`, { waitUntil: 'networkidle' });
  await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
  const r = await p.evaluate(() => {
    const W = innerWidth, out = { hscroll: document.documentElement.scrollWidth > W + 1, wide: [], clip: [], tap: [] };
    for (const el of document.querySelectorAll('main *, footer *')) {
      const cs = getComputedStyle(el); if (cs.display === 'none' || cs.visibility === 'hidden') continue;
      const rc = el.getBoundingClientRect(); if (!rc.width || !rc.height) continue;
      let anc = el.parentElement, scroller = false; while (anc && anc !== document.body) { const a = getComputedStyle(anc); if (/(auto|scroll|hidden|clip)/.test(a.overflowX) && anc.getBoundingClientRect().width <= W + 1) { scroller = true; break; } anc = anc.parentElement; }
      if (!scroller && (rc.right > W + 2 || rc.left < -2) && !el.closest('[aria-hidden="true"], .cine-media, .cine-dots, .cine-shade, .cine-caps')) out.wide.push(el.tagName.toLowerCase() + '.' + [...el.classList].slice(0, 2).join('.') + ' ' + Math.round(rc.left) + '..' + Math.round(rc.right));
      if (el.children.length === 0 && el.textContent.trim().length > 2 && el.scrollWidth > el.clientWidth + 2 && /(hidden|clip)/.test(cs.overflowX) && cs.textOverflow !== 'ellipsis') out.clip.push(el.tagName.toLowerCase() + '.' + [...el.classList].slice(0, 2).join('.') + ' "' + el.textContent.trim().slice(0, 30) + '"');
      if ((el.tagName === 'A' || el.tagName === 'BUTTON' || el.tagName === 'SUMMARY') && rc.height < 32 && rc.width < 200 && !el.closest('p, li p, .ds-stat-src, nav.ap-toc') && el.textContent.trim()) out.tap.push(el.tagName.toLowerCase() + ' "' + el.textContent.trim().slice(0, 24) + '" ' + Math.round(rc.width) + 'x' + Math.round(rc.height));
    }
    out.wide = [...new Set(out.wide)].slice(0, 6); out.clip = [...new Set(out.clip)].slice(0, 5); out.tap = [...new Set(out.tap)].slice(0, 6);
    return out;
  });
  const issues = (r.hscroll ? 1 : 0) + r.wide.length + r.clip.length + r.tap.length;
  if (issues) console.log(`${pg}${r.hscroll ? ' HSCROLL' : ''}\n  wide: ${r.wide.join(' | ')}\n  clip: ${r.clip.join(' | ')}\n  tap: ${r.tap.join(' | ')}`);
  else console.log(`${pg}: ok`);
}
await b.close();
