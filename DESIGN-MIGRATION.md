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
| Home | phones (≤760px) | phone layer | not yet (phone layer) | |
| App Design Workshop, College Portfolio Workshop, Entrepreneurship & AI Intensive, Year-Long Project Mentorship, AI Advantage Bootcamp (EN + CN) | sections, heads, FAQ | program-pages.css, pages.css | yes: ds-section, ds-head, ds-faq (tools/page_ds.py programs); steppers, stats and forms keep their components | f6d3080 |
| AI for Educators (teachers), Technology teams, Conferences, Community Dialogues (EN + CN) | sections, heads, FAQ | elegance.css, program-pages.css | yes: ds-section, ds-head, ds-faq (tools/page_ds.py teachers); tabs, steps and proof rows keep their components | 7c5552b |
| Schools (leaders), Partnerships, Results (EN + CN) | sections, heads, FAQ | pages.css, elegance.css | yes: ds-section, ds-head, ds-faq (tools/page_ds.py schools); case studies and tabs keep their components | chunk 4 |
| About, Contact, Enroll (EN + CN) | sections, heads | pages.css | yes: ds-section, ds-head (tools/page_ds.py about); forms keep their components | chunk 5 |
| Events (winter, ACAMIS, parent coffee) | all | program-pages.css, events | not yet | |
| CN twins | follow their EN page | | | |
