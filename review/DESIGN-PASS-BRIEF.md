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

## DIRECTION CHANGE (Sept 29, founder) — overrides anything above
The founder compared our redesign to the currently deployed arenaschool.org (see `git show origin/main:index.html`,
`origin/main:programs/website-portfolio-workshop.html`) and judged the LIVE site **more professional and trustworthy**.
Ours is "too playful" and "too salesy/pitchy". Goal: **build trust** with school leaders, counselors, and parents.
- Visual reference = the live site and the new `index.html` (rebuilt on the live layout): calm riso hero, plain cards with
  thin borders, generous whitespace, real photos, logo wall. Restraint over spectacle.
- **Remove:** pinned scroll stories (`.pp-sc` / data-scrolly), fake product mockups (LunchLine, phones, browser sites,
  pitch slides, osmosis sims, chat/invite cards), numbered pins, animated counters, gradients, badges. Replace with real
  photos from `photos/isb-hq/*-800.webp|*-1400.webp`, `photos/isb-*.jpg`, `photos/mix/*`, or with nothing.
- **Copy tone: neutral, factual, informative**, like a school program catalogue: what it is, who it's for, what students
  do each day, what the school provides, logistics. Persuasive through clarity and facts, never marketing hype. No
  "Show their dream school who they really are", no "stand out", no exclamation, no second-person selling. Headlines
  plain (e.g. "Admissions Portfolio Workshop" + one factual sentence).
- "Who teaches it": **no founder photo/profile cards**. At most one line "Designed and taught by Arena's founding team"
  plus the institution logo row.
- Keep: facts strip, how-it-runs steps (as simple numbered text + real photos), FAQ, one-pager form, contact CTA.

## CLARITY PRINCIPLE (Sept 30, founder) — the metric for this pass
Maximum value per word; minimum clicks and scrolls to understand the offer; lowest cognitive load.
For every page, a skeptical principal or parent should grasp in ~10 seconds: what it is, who it's for, what
students/teachers get, logistics (length, grades, where), and the next step. Score each page on:
(a) words per idea (cut filler, merge duplicate sections, one idea per sentence, plain headlines that say the thing),
(b) scroll depth to understand the offer (key facts above the fold; fewer, denser sections),
(c) clicks to act (clear primary CTA, no dead ends), (d) scannability (labels, parallel card copy, consistent structure),
plus formality/trust. Cut or merge anything that doesn't earn its space. Keep verified facts only. EN and CN together.
Titles and card descriptions must be parallel and self-explanatory (e.g. label = audience, title = program, one line =
what they get). Iterate: screenshot → score each dimension critically → cut/merge/rewrite → rescore, until ≥ 9.5.

## FINAL CRITICAL LOOP (Sept 30) — per SECTION, not per page
- Grade EVERY SECTION of every page (EN and CN, 1440 and 390) on: hierarchy, typography, alignment/grid, spacing,
  background/color, imagery fit, copy clarity & substance, credibility/trust, interaction/hover, motion, mobile.
  Log a table: page › section › each dimension score › fix made › new score. A section is done only at ≥9.5 on all.
- Be adversarial: assume the first pass is wrong. Check that CSS actually applies (a section rendering as plain
  bullets/unstyled = a bug: check class names, selectors, cache-bust ?v= on links; bump ?v= if you change CSS).
- Substance matters (founder): keep the "why it matters", matched step photos, tools, what students make. Low
  cognitive load ≠ cutting substance.
- PHOTOS: prefer OUR OWN photos and videos (photos/isb-hq/, photos/isb-*.jpg, photos/isb-2026/, photos/mix/ incl.
  pilot-collab/hands mp4s). Replace stock (photos/stock/) with ours wherever ours plausibly fits the step. Keep stock
  only where nothing of ours fits AND it matches the warm, restrained paper/navy look; never staged-corporate.
- Program names: App Design Workshop, College Portfolio Workshop, Entrepreneurship & AI Intensive, Year-Long Project
  Mentorship, AI Advantage Bootcamp, AI for Educators, Community dialogues (parent education series).
  CN: 应用设计工作坊, 升学作品集工作坊, 创业与AI集训营, 学年项目导师计划, AI职场先发营, 教育者AI培训, 社区对话.

## ROUND 5 (Oct 1, founder feedback) — apply everywhere, EN + CN
- Remove every "Illustrative" / "示意图" tag on stock photos.
- Steps ("How it runs"): make them more cinematic and interactive (e.g. a step selector/timeline where the active step
  swaps a large photo or video with a smooth crossfade, progress indicator, keyboard accessible; reduced-motion safe).
  Formal, not playful.
- Proof/case studies: NEVER "6 of 6", never "100% launched/shipped" (not impressive; it's the program's purpose).
  Use stronger verified proof: 9.5/10 NPS (Hong Kong, 20 students), US$1,980 real seed money (HK pitch winners),
  ¥8,888 final prize (Beijing), judged by founders/operators from Harvard, Y Combinator and AI labs, a 10-year-old
  launched a sign-language-to-speech app in five days, Tsinghua Schwarzman College staff training.
- Results/case studies are "three examples of programs we've run", NOT the only three. Frame as selected examples.
- Remove ANY mention of tuition/fees/pricing amounts.
- Year-Long Project Mentorship: NOT "October to March". Describe as "6 months to a year of continued, personalized
  1:1 mentorship"; rolling start. CN: 六个月到一年、持续的一对一个性化导师指导.
- Team framing: never imply a two-person company. Structure = "Our team comes from" (institution logos, the whole
  team) + a separate "Co-founders" section: Jing Jing Yang FIRST, then Phillip An.
