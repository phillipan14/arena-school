# Performance (RES-BRIEF, Oct 16, 2026)

Lighthouse 12.6.0, mobile preset (simulated 4x CPU, slow 4G), one run at a time, performance category only.

**Served compressed** (`npx serve`, gzip), like production: before = the site at `f17ac84`, after = this commit.

| Page | Score before → after | LCP before → after | CLS before → after | TBT before → after |
|---|---|---|---|---|
| Home | 62 → 87 | 6.0 s → 3.7 s | 0.182 → 0.053 | 20 ms → 20 ms |
| Teachers | 72 → 75 | 5.3 s → 4.7 s | 0.05 → 0.003 | 0 ms → 0 ms |
| Winter | 69 → 72 | 6.1 s → 5.1 s | 0.05 → 0 | 0 ms → 0 ms |

Also measured on an uncompressed local server (`python3 -m http.server`), which inflates every CSS cost:

| Page | Score before → after | LCP before → after | CLS before → after | TBT before → after |
|---|---|---|---|---|
| Home | 37 → 67 | 9.0 s → 6.2 s | 0.049 → 0.053 | 1,120 ms → 20 ms |
| Teachers | 63 → 60 | 9.0 s → 7.9 s | 0.05 → 0.003 | 10 ms → 0 ms |
| Winter | 58 → 59 | 9.5 s → 8.3 s | 0.05 → 0 | 10 ms → 10 ms |

## What changed
- Hero photos: AVIF/WebP/JPEG `<picture>` (AVIF about a third of the old WebP+JPEG bytes at the same size); only the first photo is preloaded (`fetchpriority=high`), the others load after it.
- The decorative particle field starts on `requestIdleCallback` after `load` (it was a 1.1s long task inside first load on the homepage) and draws fewer dots on phones; skipped on data saver.
- Removed scripts whose targets no longer exist on the 40 hero pages: `riso-field.js`, `hero-options.js`, `riso-interact.js`, `riso-particles.js` (loaded on demand now).
- Below-the-fold `<img>` get `loading="lazy" decoding="async"`; the crest uses the 256px file instead of 512px; logo strips use 64px WebP copies (`logos/cred/sm`, `logos/tools/sm`) instead of 60–100KB PNGs.
- Layout shift: the winter banner's 40px is reserved from the first paint (`html.promo-pending`, set by a tiny inline head script) and the hero photo starts under the nav from the first paint; the rotating word ends its line, so resizing it moves no other text.

## Still open
- Render-blocking CSS is the biggest remaining cost (about 600KB uncompressed across `program-pages.css`, `phone.css`, `styles.css`, `riso-theme.css`; Lighthouse estimates 1.3s). Splitting critical CSS or pruning dead rules is the next step.
- Home CLS 0.053 on phones comes from the headline web font swapping in (Lighthouse names the hero lede). Within the "good" range (<0.1); a metric-matched fallback font would remove it.
- Teachers and winter LCP (4.7s, 5.1s) are render-delay bound by that CSS, not by the photo.
