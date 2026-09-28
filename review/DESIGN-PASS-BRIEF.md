# Arena site design pass: shared brief for every agent

Worktree: `/Users/phillipan/arena-school/.claude/worktrees/programs-coherence` (branch `design/programs-coherence`).
Local preview (clean URLs like Vercel): http://localhost:8793/ (server already running; if it's down run
`python3 /Users/phillipan/.claude/jobs/ee490048/tmp/serve.py /Users/phillipan/arena-school/.claude/worktrees/programs-coherence &`).
Screenshots: Python Playwright (`from playwright.async_api import async_playwright`), 1440x900 and 390x844. Save under
`/Users/phillipan/.claude/jobs/ee490048/tmp/agents/<your-name>/`. Add `document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))`
before full-page shots, and scroll through the page first so lazy content loads.

## Audience and tone (founder direction, non-negotiable)
Parents, heads of school, and educators. The site must look **professional, organized, credible, and legit**, never casual,
playful, or toy-like. Elegant and cinematic, but restrained. Think a top independent school or a serious education brand,
not a startup landing page. Prefer real photos and institution logos over cartoon-ish illustrations. Handwritten fonts,
sticky-note clutter, emoji, and cute mockups read as unprofessional: replace or refine them.

## Brand system (read before editing)
- `DESIGN.md` (riso system, inks, type), `CONTENT-RULES.md` (voice, claims, Oxford comma, no em dashes, AI aids people).
- Inks: `--ink #0B1A4A`, `--ink-2 #2F55A8`, `--coral #E59375`, paper `#EFE3D4`/`#FCF3ED`. Newsreader headlines, Geist body.
- Logo rule: official lockup PNGs only. Institution logos live in `logos/cred/` (caltech, harvard, brown, tsinghua-lockup,
  mckinsey, goldman, deloitte, apple, microsoft-ai, yc, kimi, kimi-wordmark).
- Photos: `photos/isb-2026/*-800.webp` (Beijing 2026), `photos/mix/pilot-*-800.webp` + 2 short mp4s (Hong Kong 2025),
  `photos/samples/*` (stock, illustrative only). Never name real students. Use WebP.

## Verified facts only (from results.html / CLAIMS)
Hong Kong 2025 (Bodley Academy): 20 students, 5 days, NPS 9.5/10, pitch winners US$1,980 seed money, a 10-year-old launched a
sign-language-to-speech app in 5 days. Beijing 2026 (ISB): grades 7–12, 100% of teams launched a live product, ¥8,888 final
prize, judged by founders and operators from Harvard, Y Combinator, and AI labs; 6 of 6 surveyed asked to continue.
Tsinghua: AI training for Schwarzman College staff. Never state the Beijing student count. Do not invent numbers.

## Shared components (reuse, don't fork)
`css/program-pages.css` + `pp-*.js` (program pages), `css/journey.css` (grade 6–12 timeline), `css/index.css` (homepage),
`riso-theme.css` + `styles.css` (global). **File ownership is strict (parallel agents):** only edit the files your task
assigns you. If you need a shared style, add it to the CSS file you own, scoped under a page/body class.

## Scoring rubric (score every page, every dimension, out of 10)
1. Visual hierarchy  2. Typography  3. Alignment and grid  4. Spacing and rhythm  5. Section backgrounds and color
6. Imagery and graphics quality (professional, not playful)  7. Copy clarity and credibility  8. Interaction and hover
9. Animation and scroll motion (smooth, purposeful, reduced-motion safe)  10. Mobile (390px: no overflow, readable, tidy)
Be harsh: 9.5 means a senior designer at a top studio would ship it untouched. Loop: screenshot → score → fix the
lowest dimensions → re-screenshot → rescore, until **every dimension ≥ 9.5** or you are stuck on something only the
founder can supply (say so). Verify: no console errors, no horizontal overflow at 390px, all links resolve (server returns 200).

## Deliver
Do NOT git commit (the lead commits). Return: files changed, final score table per page, and anything blocked.
