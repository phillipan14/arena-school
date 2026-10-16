# Design-system migration (MIGRATION-BRIEF, Oct 16, 2026)

Moving every page from the legacy layers (styles.css, riso-theme.css, program-pages.css, index.css, page CSS) onto
the design system: tokens in `css/pro.css`, components in `css/ds.css` (spec: `DESIGN-SYSTEM.md`). Pages keep the
legacy classes their scripts rely on; the ds classes are added beside them and win above 760px. At 760px and below
the phone layer (`phone.css`, from `phone/*.css`) keeps its own layout until a page group's phone pass.
Before/after shots: `/tmp/pro-pass/mig-<page>-{before,after}-{1440,390}.png`.

Sitewide in chunk 1: spacing tokens and the whitespace pass (section rhythm, head margins, measure, grid gaps) on every
page above 760px; `ds.css` linked on every page; "Learning approach" added to the About menu and footer (EN + CN).

| Page | Section | Old | Migrated | Commit |
|---|---|---|---|---|
| Learning approach (new, EN + CN) | all | n/a | yes: ds-section, ds-head, ds-grid, ds-card, ds-mx, ds-ic | 11079d9 |
| Approach (EN + CN) | three skills, pointer | approach-extra.css, pages.css cards | yes: ds-section, ds-head, ds-card | 11079d9 |
| Home (EN + CN) | film | film.css head | yes: ds-section, ds-head.is-center | 11079d9 |
| Home | partner strip, photo gallery | ai-band.css, index.css gallery | kept (their own components) | n/a |
| Home | programs: head, doors, cards | index.css, styles.css | yes: ds-head, ds-doors, ds-grid, ds-card.is-media | 11079d9 |
| Home | where each program fits | grades.css pill/Gantt lanes | yes: ds-mx (ds-gmx), tools/grade_matrix.py; dead lane CSS removed | 11079d9 |
| Home | our team | index.css hp-cred, hp-cf | partly: ds-section, ds-head, ds-logos (leader cards keep their own styles) | 11079d9 |
| Home | what we teach | index.css pillars | yes: ds-head, ds-grid, ds-card | 11079d9 |
| Home | what's next | styles.css cf-evs | yes: ds-list | 11079d9 |
| Home | contact | index.css partners | partly: ds-section, ds-stack heading (form keeps its styles) | 11079d9 |
| All pages | phone base (≤760px): tokens, type, buttons, gutters | phone/00-base.css own --ph-* values | yes: --ph-* now alias the ds tokens (colour, --space-*, --radius-*, --tap); spacing and type snapped to the scale (tools/tokenize_css.py --snap); buttons 8px radius like desktop | chunk P1 |
| Home, sticky bar, lead form | phones | phone/20-home.css, 90-lead.css | yes: on tokens (same tool) | chunk P1 |
| Program pages (phones) | phone/30-program: tokens, buttons, hero facts card, team logos | own values, pills, alternating indents, a scrolling logo strip | yes: tokens (tools/tokenize_css.py --snap); facts rows even; the page's logo grid kept (css/cred.css) | e850585 |
| Special pages, pages (phones) | phone/40-special, 50-pages | own values | yes: tokens (same tool) | e850585 |
| App Design Workshop, College Portfolio Workshop, Entrepreneurship & AI Intensive, Year-Long Project Mentorship, AI Advantage Bootcamp (EN + CN) | sections, heads, FAQ | program-pages.css, pages.css | yes: ds-section, ds-head, ds-faq (tools/page_ds.py programs); steppers, stats and forms keep their components | f6d3080 |
| AI for Educators (teachers), Technology teams, Conferences, Community Dialogues (EN + CN) | sections, heads, FAQ | elegance.css, program-pages.css | yes: ds-section, ds-head, ds-faq (tools/page_ds.py teachers); tabs, steps and proof rows keep their components | 7c5552b |
| Schools (leaders), Partnerships, Results (EN + CN) | sections, heads, FAQ | pages.css, elegance.css | yes: ds-section, ds-head, ds-faq (tools/page_ds.py schools); case studies and tabs keep their components | 540ed98 |
| About, Contact, Enroll (EN + CN) | sections, heads | pages.css | yes: ds-section, ds-head (tools/page_ds.py about); forms keep their components | 05ae5ed |
| AI Fundamentals @ ISB (winter), ACAMIS session, ISB parent coffee (EN + CN) | sections, heads, FAQ | program-pages.css, events | yes: ds-section, ds-head, ds-faq (tools/page_ds.py events) | ae2bf12 |
| CN twins | follow their EN page; Chinese headings measure in em | | yes, with each group | chunks 1 to 6 |
| Teachers (AI for Educators), EN + CN | depth pass: pressures, research, cases, tools, FAQ | thin (5 sections) | yes: ds-ps, ds-stats, ds-cases, ds-tools (tools/depth.py teachers); log in DEPTH-LOG.md | 4a1c1f9 |
| Technology teams, EN + CN | depth pass: risks, research, cases, tools, FAQ; hero photos | thin proof row | yes: tools/depth.py technology; hero laptop/mentors/duo | 165c2c3 |
| Credibility strip (every page that carries it) | logo rows | mixed sizes, marquee | yes: css/cred.css from tools/cred_css.py | 165c2c3 |
| Schools (leaders), EN + CN | depth pass: constraints, research, cases, tools, FAQ | no evidence | yes: tools/depth.py schools | 3d94ced |
| Partnerships, EN + CN | depth pass: concerns, research, cases, tools, new FAQ | 4 sections | yes: tools/depth.py partnerships | 575749f |
| Conferences, EN + CN | depth pass: needs, research, cases, tools, FAQ; format photos filled | empty photo slots | yes: tools/depth.py conferences | f0cd74b |
| Community Dialogues, EN + CN | depth pass: worries, research, cases, tools, FAQ | empty proof band | yes: tools/depth.py community | 7cb25d5 |
| Photo rules (sitewide) | banned photos | cohort and prize photos on 11 pages | yes: tools/photo_rules.py (0 left) | 7cb25d5 |
| Entrepreneurship & AI Intensive, EN + CN | depth pass: gaps, research, cases, tools | thin stats row | yes: tools/depth.py | e0d1bfb |
| App Design Workshop, EN + CN | depth pass: gaps, research, cases, tools | thin stats row | yes: tools/depth.py | 20cfa08 |
| College Portfolio Workshop, EN + CN | depth pass: gaps, research, cases, tools | thin stats row | yes: tools/depth.py | 2a430bc |
| Year-Long Project Mentorship, EN + CN | depth pass: gaps, research, cases, tools | thin stats row | yes: tools/depth.py | bfdaafd |
| AI Advantage Bootcamp, EN + CN | depth pass: gaps, research, cases, tools | thin stats row | yes: tools/depth.py | 9da1055 |
| About, EN + CN | depth pass sized to the page | thin | yes: tools/depth.py | d5f0fa8 |
| Results, EN + CN | depth pass sized to the page | thin | yes: tools/depth.py | 863c1dc |
| Contact, EN + CN | depth pass sized to the page | thin | yes: tools/depth.py | 185402c |
| AI Fundamentals @ ISB (winter), EN + CN | depth pass sized to the page | thin | yes: tools/depth.py | 45c3a59 |
| ACAMIS session, EN + CN | depth pass sized to the page | thin | yes: tools/depth.py | 379d301 |
| ISB parent coffee, EN + CN | depth pass sized to the page | thin | yes: tools/depth.py | 6495559 |
| All pages with a depth FAQ (phones) | FAQ rows | browser default disclosure triangles | yes: ds-faq phone rules in css/ds.css | f859817 |
| All pages, 390 audit (EN all, CN all, automated + visual) | overflow, clipping, tap targets | About leader logos cut off; Results stats crowded; event speaker links 19px; card language pill 30px | fixed (tools/audit390.mjs) | 65ae4bc |
