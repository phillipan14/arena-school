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
| Learning approach (new, EN + CN) | all | n/a | yes: ds-section, ds-head, ds-grid, ds-card, ds-mx, ds-ic | chunk 1 |
| Approach (EN + CN) | three skills, pointer | approach-extra.css, pages.css cards | yes: ds-section, ds-head, ds-card | chunk 1 |
| Home (EN + CN) | film | film.css head | yes: ds-section, ds-head.is-center | chunk 1 |
| Home | partner strip, photo gallery | ai-band.css, index.css gallery | kept (their own components) | n/a |
| Home | programs: head, doors, cards | index.css, styles.css | yes: ds-head, ds-doors, ds-grid, ds-card.is-media | chunk 1 |
| Home | where each program fits | grades.css pill/Gantt lanes | yes: ds-mx (ds-gmx), tools/grade_matrix.py; dead lane CSS removed | chunk 1 |
| Home | our team | index.css hp-cred, hp-cf | partly: ds-section, ds-head, ds-logos (leader cards keep their own styles) | chunk 1 |
| Home | what we teach | index.css pillars | yes: ds-head, ds-grid, ds-card | chunk 1 |
| Home | what's next | styles.css cf-evs | yes: ds-list | chunk 1 |
| Home | contact | index.css partners | partly: ds-section, ds-stack heading (form keeps its styles) | chunk 1 |
| Home | phones (≤760px) | phone layer | not yet (phone layer) | |
| Programs (4 student programs) | all | program-pages.css | not yet | |
| Teachers, technology, conferences, community dialogues | all | elegance.css, program-pages.css | not yet | |
| Schools, partnerships, results, about, contact, enroll | all | pages.css, elegance.css | not yet | |
| Events (winter, ACAMIS, parent coffee), mentorship, bootcamp | all | program-pages.css, events | not yet | |
| CN twins | follow their EN page | | | |
