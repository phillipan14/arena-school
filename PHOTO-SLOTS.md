# Photo slots (pro pass, 2026-10-16)

Every slot uses one component: `.pro-photo` in `css/pro.css` (3:2, 12px radius, 1px hairline). Only real photos already in the repo; no stock, no AI-generated people. An empty slot is a neutral dashed block preceded by an HTML comment `TODO-PHOTO: <subject>`.

| Page (EN + CN) | Section | Slot | Photo | Caption (EN) |
|---|---|---|---|---|
| School leaders `/schools` | How a partnership works, under the steps ("ending with families in the room") | Filled | `photos/isb-2026/parents-audience-800.webp` (+1600) | Families at demo day, Beijing 2026 |
| Winter program `/events/isb-winter-2027` | The four days, Day 04 tab | Filled (existing) | `photos/isb-hq/isb-team-stage-800.webp` (+1400) | (alt only) ISB students presenting on stage, Beijing 2026 |
| Winter program `/events/isb-winter-2027` | Who teaches it | Filled (existing headshots) | `photos/jing-jing-yang-640.webp`, `photos/phillip-an-640.webp` | none |

Pre-existing homepage photos, unchanged by this pass: the gallery strip (Beijing 2026 and Hong Kong 2025 program photos) and the four program-card photos. Note for review: the gallery's "Hands-on session" photo (`photos/mix/pilot-classroom-800.webp`) shows another organization's name on the room screen.

Open questions for the team:
- `photos/isb-hq/isb-judges-test.jpg` and `photos/isb-2026/mentors-laptop.jpg` are two crops of the same scene, labeled "Judges test the products" in one place and "Educators/Mentors working at a laptop" in another. The Technology caption is kept neutral until someone confirms who is in it.
- Teachers, Conferences, the AI Advantage Bootcamp, and the parent coffee need real photos (TODOs in the table below).

## Site hero (cine4, approved Oct 16, 2026; FINAL-BRIEF.md)
Every site page except decks/, talks/, the four business cards (`card/*`), and the payment page now opens on the cine4 hero: a full-bleed crossfade of 1 to 4 real photos with a slow zoom, a navy gradient, a faint light particle field, and the crest above the headline. Markup comes from `tools/hero_markup.py` (the photo list per page lives there), behavior from `cine.js`, styles from `css/cine.css`. Photos follow `PHOTO-PICKS.md`: no cohort group shot, no prize cheques, no other organizations' names on screen. Each photo has a desktop and a phone focal point so faces stay in frame at 390px.

The large photo bands that the photo-led pass put under each program hero are gone: the hero itself is now the photo. The earlier homepage side photo is hidden.

| Page (EN + CN) | Hero photos, in order | Status |
|---|---|---|
| Homepage `/` | pitch-duo, isb-pitch-gesture, mentor-feedback, collab-stage-poster (Hong Kong 2025) | Relevant real photos |
| Teachers `/programs/teacher-training` | collab-stage-poster (Hong Kong 2025), mentor-feedback | **Fallback**: TODO-PHOTO: Teachers at a hands-on Arena session, making a tool on their own laptops |
| Technology staff `/schools/technology` | collab-stage-poster (Hong Kong 2025), mentor-feedback | **Fallback**: TODO-PHOTO: Tech coaches and IT staff at an Arena session, working on the school’s approved tools |
| School leaders `/schools` | pitch-duo, isb-pitch-gesture, mentor-feedback | Relevant real photos |
| Winter program `/events/isb-winter-2027` | pitch-duo, isb-pitch-gesture, collab-stage-poster (Hong Kong 2025) | Relevant real photos |
| ACAMIS workshop `/events/acamis-tech-2026` | isb-pitch-gesture, pitch-duo | Relevant real photos |
| ISB PTA parent coffee `/events/isb-parent-coffee` | mentor-feedback, pitch-duo | **Fallback**: TODO-PHOTO: ISB PTA parent coffee on Oct 14, 2026: Jing Jing Yang and Phillip An with parents |
| Entrepreneurship & AI Intensive `/programs/product-intensive` | isb-pitch-gesture, pitch-duo, collab-stage-poster (Hong Kong 2025) | Relevant real photos |
| App Design Workshop `/programs/remake-your-favorite-app` | collab-stage-poster (Hong Kong 2025), pitch-duo | Relevant real photos |
| College Portfolio Workshop `/programs/website-portfolio-workshop` | pitch-duo, collab-stage-poster (Hong Kong 2025) | Relevant real photos |
| Community Dialogues `/programs/community-dialogues` | mentor-feedback, pitch-duo | **Fallback**: TODO-PHOTO: A Community Dialogues parent talk: families in conversation with the Arena team |
| Conferences `/programs/conferences` | isb-pitch-gesture, mentor-feedback | **Fallback**: TODO-PHOTO: The Arena team leading a hands-on conference workshop for teachers |
| Year-Long Project Mentorship `/mentorship` | mentor-feedback, isb-pitch-gesture | Relevant real photos |
| Mentorship enrollment `/enroll` | mentor-feedback, pitch-duo | Relevant real photos |
| AI Advantage Bootcamp `/zero-to-launch` | collab-stage-poster (Hong Kong 2025), isb-pitch-gesture | **Fallback**: TODO-PHOTO: College students and early-career professionals building with AI (first AI Advantage Bootcamp cohort) |
| About `/about` | mentor-feedback, collab-stage-poster (Hong Kong 2025) | Relevant real photos |
| Approach `/approach` | collab-stage-poster (Hong Kong 2025), isb-pitch-gesture | Relevant real photos |
| Results `/results` | pitch-duo, isb-pitch-gesture, collab-stage-poster (Hong Kong 2025) | Relevant real photos |
| Partners `/partnerships` | collab-stage-poster (Hong Kong 2025), pitch-duo | Relevant real photos |
| Contact `/contact` | mentor-feedback, pitch-duo | **Fallback**: TODO-PHOTO: The Arena team, smiling, ready to talk (a team photo) |

Fallback pages show the best general bright photos until a fitting real photo exists; each carries a `<!-- TODO-PHOTO: ... -->` comment in its hero. Still in place below the hero: the School leaders families photo, the winter Day 04 and team photos, and the Conferences format-card placeholders.

## Hero photo set (RES-BRIEF, Oct 16, 2026)
Every hero now rotates the same three photos (in a page-specific order): `pitch-duo`, `isb-pitch-gesture`, and `mentor-feedback`, served from `photos/hero/` as AVIF/WebP/JPEG. The Hong Kong hands-on still (`collab-stage-poster`) was dropped from every hero: it is a 1024px video frame (HERO-RES.md). Pages marked Fallback above keep their TODO-PHOTO comments.
