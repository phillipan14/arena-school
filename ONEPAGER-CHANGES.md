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
