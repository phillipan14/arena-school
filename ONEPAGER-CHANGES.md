# One-pager: what changed (FLUENCY-BRIEF 2 and UPDATE, Oct 17, 2026)

Files replaced in place, same paths and names, so every link and the gated download (onepager.js, the `#onepager`
form on program and school pages) keep working: `onepager/arena-school-one-pager-{en,cn}.pdf` and the 520px `.jpg`
thumbnails. Link cache stamps moved from `?v=20261002` to `?v=20261017` on every page so browsers fetch the new files.
Source: `tools/one-pager/build.py` (writes `tools/one-pager/onepager-{en,cn}.html`, renders with Chrome headless to A4,
fails unless the PDF is exactly one page and nothing is clipped). The old source (`riso-v2/site-preview/_kit/`) is not
in this repo; the old PDFs were the base.

## Kept from the old version
- Structure: headline and mission, the three skills (agency, taste, craft), the team's schools and employers, programs
  by audience, "What we've run" with ISB, Bodley Academy, and Schwarzman College, and a closing "Bring Arena to your
  school" band.
- One A4 page, EN and CN.

## Changed
- **Design:** from the cream riso style (watermark, dotted grid, tinted cards, highlighted keywords) to the site's design
  system: a navy header with the ivory wordmark and one real photo (presenting at demo day, Beijing 2026), white
  ground, Newsreader and Geist, hairlines, one accent blue, greyscale logo rows, and the framework wheel.
- **Credibility:** added "A member of" with the Anthropic Startup Program and OpenAI Partner Network, exactly as on the
  site; team logos split into "Our team studied at" and "Worked at" rows; Kimi is the wordmark without the K icon.
- **Programs:** grouped as on the site's nav: for students; for teachers and schools (AI for Educators, Technology
  teams, School leaders, Conferences); for families (Mentorship, Community Dialogues, AI Fundamentals for Students @
  International School of Beijing); college and early career (AI Advantage Bootcamp).
- **New panels:** Learning approach (the wheel, "Learners decide. AI builds. Real people judge.", the four strands);
  AI fluency for the whole staff (the five levels); Student data comes first ("whose account is it?" and four
  commitments).
- **Selected programs:** copy now matches the site's case cards word for word.
- **Removed:** the "9.5/10 NPS" figure (no stats on the one-pager), per-program grade/length chips (folded into one
  line each), and the program descriptions that no longer match the site.
- **Contact:** phillip@arenaschool.org and arenaschool.org (was contact@arenaschool.org and a LinkedIn path that did
  not match the site's).
- **Links to it:** a "Download one-pager" link in the footer (partials, EN + CN), the phone footer, the About page's
  closing section, and beside the Schools page's Programs heading; all go to the existing gated form (`/schools#onepager`).

## v3 (Oct 17 pm): rebuilt after Phillip's review, plus teacher and parent one-pagers
Phillip: "too much white space, no structure, diagrams, just a bunch of text"; then "abstract it away" (programs) and
"merge offer and proof". Source: `tools/one-pager/build.py` (HTML in `tools/one-pager/`).

**What changed (general):** short header band instead of a hero photo; one thin credentials strip (member of, studied at,
worked at, each one line); numbered sections on a strict 12-column grid; the program list is replaced by four audience
tiles (icon, label, one line, formats in a few words; no grades, dates, or program names) that each carry real partner
logos as proof; How we teach as a diagram row (framework wheel, the three skills, the four strand goals); the fluency
staircase; a personal vs school account mini-diagram with three commitments. Paragraph case cards removed.

**New:** `onepager/arena-school-teacher-one-pager-{en,cn}.pdf` (who we work with: teachers, technology teams, school
leaders, conferences; the staircase and how each group moves up; how a teacher moves up one level in four steps; the four
learning outcomes; student data guardrails) and `onepager/arena-school-parent-one-pager-{en,cn}.pdf` (hands-on workshops,
intensives, year-long mentorship, parent talks; the mentorship milestone ladder; how your child learns; safety and student
data; two ways to start). No staff fluency or procurement content on the parent page; no family or student-only programs
on the teacher page. Each with a 520px .jpg.

**Programs shown (abstracted, as audiences):** general: students (workshops, intensives, mentorship), teachers and schools
(sessions, workshops, school-wide), families (1:1 mentorship, parent talks), university and career (bootcamp). Teacher:
teachers, technology teams, school leaders, conferences. Parent: hands-on workshops, intensives, year-long mentorship,
parent talks.

**Logos used (all existing repo files):** proof: `logos/cred/isb.png` (International School of Beijing),
`logos/cred/tsinghua-lockup.png` (Tsinghua, for Schwarzman College staff training), `decks/img/conversation/pta-logo.png`
(ISB PTA), `logos/lux/lux-navy-horizontal.png` (Lux Scholar); Bodley Academy and ACAMIS appear as plain text labels (no
logo file in the repo). Strip: `logos/partners/anthropic.svg`, `logos/partners/openai.svg`; `logos/cred/` caltech, harvard,
brown, tsinghua-lockup, isb, mckinsey, goldman, yc, apple, microsoft-ai, deloitte, kimi-wordmark.

**Wiring:** the gated form on Teachers (EN + CN) now offers the teacher one-pager; Mentorship and Community Dialogues
(EN + CN) offer the parent one-pager; everywhere else the general one. Link stamps `?v=20261017b`.

## v4 (Oct 17 pm): Phillip's review of v3
- **Header:** the v2 photo header is back on all three: navy band, wordmark, large headline with an italic accent, a
  short intro, and the demo-day photo on the right, captioned "Demo day, Beijing, 2026" (CN 路演日，北京，2026年).
- **Three sections per variant** (content cut, not crammed): general: who we serve, how we teach, student data;
  teacher: five levels of AI fluency, moving up a level, student data; parent: what your child does, the milestone ladder,
  safety and student data.
- **Design:** chosen direction B: alternating full-bleed bands with a large accent numeral and a serif title, even
  rhythm, bigger type (body 8.2pt, titles 14.5pt), fewer grey lines. Staircases give every level room (names on the steps,
  descriptions below). Proof logos at one optical height; Bodley Academy and ACAMIS as plain serif labels. Icons inline
  with names, one size. Equal-height cards per row, 12-column grid verified by overlay and by the build.
- **Credentials strip** (A member of, Our team studied at, Worked at) moved to the bottom, directly above the contact
  footer, each row on one line.
- Same file paths; link stamps `?v=20261017c`.
- **v4.1 (review 1):** even staircase steps; wheel without the unreadable ring labels, strands in their own row; Brown and
  Harvard logos matched in weight; one-line tile titles; skills on the 12-column thirds; header copy fits its band;
  legible photo caption. Stamps `?v=20261017d`.
- **v4.2 (review 2):** data cards and commitments on the 12-column grid; the parent Workshops card shows "2 days" (a site
  fact) in its proof slot; staircase descriptions aligned to each step's inner padding. Stamps `?v=20261017e`.

## v5 (Oct 17 pm, ONEPAGER4-BRIEF)
- **Parent:** student data section removed. Now: what your child does (three tiles with real proof), skills your child
  builds (agency, taste, craft, and practical skills: building with AI, talking to users, pitching, research and
  judgment), what they walk away with (the milestone ladder plus a live product, a documented record, people who know
  their work, experience presenting it; with the site's no-promise admissions line).
- **All six:** "Team from" (团队来自) replaces "studied at" and "worked at": twelve marks on two balanced lines of six
  (Caltech, Harvard, Brown, Tsinghua, ISB, Apple / McKinsey, Goldman Sachs, Y Combinator, Microsoft AI, Deloitte, Kimi).
- **Polish:** the photo starts at column 8 with a clean edge, so text never sits near it; general How we teach without
  the dead gap (wheel sized to the content block, strands as one line); no vs badge; equal-height commitment rows aligned
  to the account cards; teacher and parent tiles on the thirds, every tile with a real proof line; fewer type sizes.
- Stamps `?v=20261017f`.
- **v5.1 (review):** credentials on one shared 6-column grid (two lines of six, centred); "Cleared for student data" on
  one line; tile proof slots aligned across rows; parent keep row with more presence. Stamps `?v=20261017g`.

## v5.2 (Oct 17, SCHWARZMAN-BRIEF + UPDATE)
- **Schwarzman proof:** wherever a proof line says "Staff training, Schwarzman College" (general Educators tile,
  teacher "Teachers & tech teams" tile; EN + CN), the Tsinghua University logo now sits beside the official Schwarzman
  Scholars logo (shield and wordmark), one optical height, the same greyscale treatment. Logo file: the repo's existing
  `logos/cred/schwarzman.png` (in use on the site since Sep 30, 2026, commit aabca87), not a new download. The repo's
  `logos/schwarzman.svg` is plain typeset text, not the official mark, so it is not used.
- **"A member of"** moved to a slim strip directly under the photo header, styled like the homepage strip (small
  centred label, Anthropic Startup Program and OpenAI Partner Network). "Team from" stays at the bottom.
- **Header photo:** no hard seam; the photo fades in from the navy (solid behind the headline, clear by the students'
  faces), as on the site's hero.
- Stamps `?v=20261017h`.
- **v5.3 (CAPTION-BRIEF):** header photo caption "Demo day at the International School of Beijing, 2026" (fits one line),
  CN "北京顺义国际学校路演日" (JJ review comment in the source); one line checked by the build. Stamps `?v=20261017i`.
- **v5.4 (EDGES-BRIEF):** "Team from" marks sized by measured ink area (equal visual mass; Harvard, Brown, Tsinghua,
  ISB raised to a legible minimum; Apple matched), all one greyscale darkness, 6 + 6 on shared columns with the outer
  columns on the content edges. One left and one right content edge for header text, member strip, section headers,
  cards, data list, Team-from label and logos, footer text and contact (Team-from label now above the grid). The build
  checks all of these edges on every page. Stamps `?v=20261017j`.
- **v5.5 (TEAMROW-BRIEF):** bottom row relabelled "Built by a team from" (CN 团队成员来自, JJ review), label on the left in
  the same column as "A member of", logos on the right in a 2 x 6 grid of equal cells (each mark centred) ending on the
  right content edge. 3 x 4 was tried and dropped (a third row, a floating label, and the parent EN page went over).
  Stamps `?v=20261017k`.

## v6 (Oct 17 pm, MESSAGING-BRIEF): concrete messaging per audience (see ONEPAGER-POSITIONING.md)
- **Headers say who we are, concretely:** parent "Your child builds and launches a real AI product", with the mentoring
  team named (Harvard, Caltech, Tsinghua, McKinsey, Goldman Sachs, Y Combinator, Apple, Microsoft AI); teacher "Every
  teacher confident with AI, inside your school's rules", each teacher leaves with a working tool, from the team that
  trained staff at Schwarzman College; general "Students, teachers, and families build real things with AI", with where
  we have run it.
- **Agency, taste, craft in plain words** (from the approach page): choose a real problem and pitch it; test with real
  users and judge which version works; launch at a live link and explain every decision.
- **Parent:** Why it matters now (RAND: over 80% of students not taught to use AI, 54% already use it, 61% of parents
  worried about critical thinking; sources printed); What your child builds and learns; What it leads to (milestone
  ladder, what they keep for college, summer, and internship applications, proof: ISB demo day judges from Harvard,
  Stanford, Y Combinator, and AI labs; a sign-language-to-speech app launched in five days at Bodley Academy); the
  site's no-promise admissions line. No student data section.
- **Teacher:** Why now (RAND 53% of teachers use AI; 1 in 2 districts trained; Gallup 5.9 hours a week saved), five
  levels with one session, one working tool; student data.
- **General:** each audience tile states that audience's motivation.
- Stamps `?v=20261017l`.

## v7 (Oct 17, 9:40pm, PARENT2-BRIEF)
- **Headlines (literal):** parent "Hands-on AI programs where students build and launch a real product" (CN 动手实践的AI项目，
  学生亲手做出并上线真实的产品); teacher "Hands-on AI training where each teacher builds a tool for their class" (CN
  动手实践的AI培训，每位老师为自己的课堂做一个工具); general "Hands-on AI programs for students, teachers, and families" (CN
  面向学生、老师和家庭的动手实践AI项目).
- **Memberships** (Anthropic Startup Program, OpenAI Partner Network) sit beside the Arena School wordmark in the header;
  the separate strip is gone.
- **One hero stat per page, no citation line** (source in STATS-SOURCES.md): parent `rand-students` (80%+ not explicitly
  taught), teacher `rand-use` (53% of teachers), general `rand-students-use` (54% of students).
- **Diagrams:** parent, the five-day Entrepreneurship & AI Intensive as a framed day-by-day timeline from its program
  page (launch on day 3, pitch on day 5; traction, revenue, impact, recognition as stretch goals in year-long mentorship),
  with the page's typical tools (ChatGPT, Claude, DeepSeek, Kimi, Figma, Canva). **20+ tools:** not used on the parent
  page; the site's "More than twenty AI tools" is said of the seven-day AI Advantage Bootcamp (zero-to-launch), not the
  intensive. Teacher, the session flow (before, show, make, keep) and the five fluency levels. General, the four audience
  offers.
- **Proof as logos only:** "Programs run at" ISB and Bodley Academy (parent), Tsinghua, Schwarzman, ISB (teacher), all four
  (general). The ISB-judges and sign-language example cards are removed.
- **Team row:** "Coached by a team from" (CN 导师团队来自, JJ review), the balanced 2 x 6 grid.
- Stamps `?v=20261017m`.
- **v7.1 (PARENT2-REVIEW):** compact "Why now" bands (number and sentence side by side, band only as tall as its
  content); the space goes to bigger diagrams: general "Who we serve" as a framed who / why they come / format / what they
  make diagram, teacher session flow and fluency levels in one shared frame. "Programs run at" logos in the same equal
  cells and grey as the team row, label in columns 1-3. Team rows spread evenly across columns 4-12 (outer columns on
  the edges). Parent day 5 (Demo day) in navy as the climax; tools row labelled "AI tools they use" (CN 孩子用的AI工具).
  Stamps `?v=20261017n`.
- **v8 parent (PARENT3-BRIEF):** outcomes lead. 01 "What your child walks away with": a navy 80%+ stat panel beside four
  numbered outcome frames, then "Programs run at" ISB and Bodley (larger, on the grid) and the admissions line. 02 "How
  they get there": the five-day timeline in its frame, then two rows: AI tools they use (named) and stretch goals in
  year-long mentorship. Direction B of three (see DEPTH-LOG.md). Stamps `?v=20261017o`.
- **v9 (BUILD-A-BRIEF, Oct 18, 2026): concept A's system on all six.** Header: a full-bleed real photo poster with a navy
  fade; "A member of" Anthropic + OpenAI right beside the wordmark; literal headline; mentors line. Parent (outcomes
  first, per the standing rule): 01 what they keep, four compact cards; 02 the five days as an icon-led timeline (no
  photos; circles joined by arrowed lines; Day 3 Launch, Day 5 Pitch filled navy); 03 the AI tools they learn, eight
  tools each with a skill label; Programs run at ISB + Bodley; the admissions line. Teacher: the session flow as the
  same icon-led timeline, the five fluency levels, Programs run at, student data, a tools row. General: four audience
  cards with icon nodes, Programs run at, the three moves (wheel), a tools row. No stat on any page (the poster needs
  the space; the brief allows dropping it). Photos: parent pitch-duo (ISB demo day), teacher mentor-feedback (caption
  as on the site), general isb-pitch-gesture (ISB demo day).
  **Tool sources (only tools the site lists):**
  - Parent grid (the five-day intensive): ChatGPT, DeepSeek, Perplexity, Claude, Kimi Code, Vercel, Figma, Canva, all
    on `programs/product-intensive.html` (tool strip; Kimi Code in "Typical tools include..."). Skill labels follow
    that page's "AI assistants for research, AI coding tools to build, and design tools for the brand".
  - Teacher row: ChatGPT, Claude, DeepSeek, Kimi, Perplexity, Canva: `programs/teacher-training.html` ("Tools we often
    work with").
  - General row: ChatGPT, Claude, DeepSeek, Kimi, Figma, Canva: `schools.html` ("Tools students and staff have learned").
  - **Claude Code is not named on any site page**, so it is not on the one-pager; Claude is shown with "Build apps"
    (Claude is on the intensive's list of tools, which includes "AI coding tools to build"). Cursor appears only on
    `events/isb-winter-2027.html`, not on the intensive page. No tool count: the site states none for the intensive.
    Adding "Claude Code" to the intensive page would let it go on the one-pager.
