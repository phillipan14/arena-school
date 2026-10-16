# Photo slots (pro pass, 2026-10-16)

Every slot uses one component: `.pro-photo` in `css/pro.css` (3:2, 12px radius, 1px hairline). Only real photos already in the repo; no stock, no AI-generated people. An empty slot is a neutral dashed block preceded by an HTML comment `TODO-PHOTO: <subject>`.

| Page (EN + CN) | Section | Slot | Photo | Caption (EN) |
|---|---|---|---|---|
| Homepage `/` | Hero, right column | Filled | `photos/isb-2026/demo-laptop-800.webp` (+1600) | Demo day, Beijing 2026 |
| School leaders `/schools` | How a partnership works, under the steps ("ending with families in the room") | Filled | `photos/isb-2026/parents-audience-800.webp` (+1600) | Families at demo day, Beijing 2026 |
| Winter program `/events/isb-winter-2027` | The four days, Day 04 tab | Filled (existing) | `photos/isb-hq/isb-team-stage-800.webp` (+1400) | (alt only) ISB students presenting on stage, Beijing 2026 |
| Winter program `/events/isb-winter-2027` | Who teaches it | Filled (existing headshots) | `photos/jing-jing-yang-640.webp`, `photos/phillip-an-640.webp` | none |

Pre-existing homepage photos, unchanged by this pass: the gallery strip (Beijing 2026 and Hong Kong 2025 program photos) and the four program-card photos. Note for review: the gallery's "Hands-on session" photo (`photos/mix/pilot-classroom-800.webp`) shows another organization's name on the room screen.

Open questions for the team:
- `photos/isb-hq/isb-judges-test.jpg` and `photos/isb-2026/mentors-laptop.jpg` are two crops of the same scene, labeled "Judges test the products" in one place and "Educators/Mentors working at a laptop" in another. The Technology caption is kept neutral until someone confirms who is in it.
- Teachers, Conferences, the AI Advantage Bootcamp, and the parent coffee need real photos (TODOs in the table below).

## Photo-led program heroes (added 2026-10-16, 5:11pm brief)
Every program page hero now ends in one large photo band (`.pro-hero-media` > `.pro-photo.is-wide`: 2:1 on desktop, 3:2 on phones, focal point per photo). On the audience and winter pages this band replaces the smaller right-column hero photo; the facts panel stays at the top right. UI mockups and logo strips sit lower on the page.

| Page (EN + CN) | Hero band | Photo or TODO subject | Caption (EN) |
|---|---|---|---|
| Teachers `/programs/teacher-training` | **TODO** | Teachers at a hands-on Arena session, making a tool on their own laptops (real session photo, faces with consent) | none |
| Technology staff `/schools/technology` | Real | `photos/isb-2026/mentors-laptop` | Working through a task together, Beijing 2026 |
| School leaders `/schools` | Real | `photos/isb-2026/pitch-team` | Final pitch, Beijing 2026 |
| Entrepreneurship & AI Intensive `/programs/product-intensive` | Real | `photos/isb-hq/isb-team-stage` | Students presenting on stage, Beijing 2026 |
| App Design Workshop `/programs/remake-your-favorite-app` | Real | `photos/mix/pilot-cohort` | Our Hong Kong cohort, 2025 |
| College Portfolio Workshop `/programs/website-portfolio-workshop` | Real | `photos/mix/pilot-sticky` | Mapping problems worth solving, Hong Kong 2025 |
| Community Dialogues `/programs/community-dialogues` | Real | `photos/isb-2026/parents-audience` | Families at demo day, Beijing 2026 |
| Conferences `/programs/conferences` | **TODO** | Arena team leading a hands-on conference workshop for teachers (e.g., ACAMIS 2026) | none |
| Year-Long Project Mentorship `/mentorship` | Real | `photos/isb-2026/mentor-feedback` | Mentors respond to a student’s work, Beijing 2026 |
| AI Advantage Bootcamp `/zero-to-launch` | **TODO** | College students and early-career professionals building with AI (first cohort, Guangzhou) | none |
| Winter program `/events/isb-winter-2027` | Real | `photos/isb-hq/isb-cohort` | ISB students with their projects, Beijing 2026 |
| ACAMIS workshop `/events/acamis-tech-2026` | Real | `photos/isb-hq/isb-pitch-mic` | The ISB case: a student presents her team’s product, Beijing 2026 |
| ISB PTA parent coffee `/events/isb-parent-coffee` | **TODO** | ISB PTA parent coffee on Oct 14, 2026: Jing Jing Yang and Phillip An with parents | none |

Section images: Conferences used three stock photos in its format cards (`photos/stock/educators-talk`, `breakout-circle`, `panel-stage`). They are now `TODO-PHOTO` placeholders: a talk to educators at a conference; teachers in a small-group discussion during an Arena workshop; the Arena team on a conference panel. No site page loads `photos/stock/` any more.

Captions say where each photo was taken; a photo from another program (for example, Hong Kong 2025 on the App Design and Portfolio pages) is labeled as such and never presented as that program.

Totals: 9 of these 13 pages (each EN + CN) have a real hero photo; 4 are placeholders: Teachers, Conferences, AI Advantage Bootcamp, and the ISB PTA parent coffee.
