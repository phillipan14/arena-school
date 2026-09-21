# Arena — R2 Design Brief

R1 nailed the visual system. What it did not do is land the **philosophy**. The page right now shows the structure (mornings, afternoons), the pilot proof, and the deliverables (the open-source protocol three-card section). But it never tells a reader *why* the architecture of school stopped working, *why* AI changes the calculus, or *what* agency and taste and craft actually mean and why a school has to be built around them now.

R2 is a content-and-structure pass, not a polish pass. The visual system, motion, and color tokens all hold. The page flow needs to change. Four new sections need to be added. One existing section gets deleted. One gets dropped.

## New page flow

```
1.  Nav (with live status band)
2.  Hero — unchanged
3.  Pilot proof — unchanged
4.  [NEW] Why school exists the way it does
5.  [NEW] What AI changed
6.  [NEW] What's left for humans
7.  The structure — unchanged
8.  Hubs map (dark) — unchanged
9.  Manifesto (dark) — unchanged
10. [REPLACES the three-card protocol section] One quiet line on open-sourcing
11. The bet — unchanged
12. Cohort Zero strip — unchanged
13. [DROP] For operators — out entirely, it's a v2 audience
14. Closing CTA (dark) — unchanged
15. Footer
```

## The four new philosophy sections

Voice is drawn from the user's existing 3,200-word education manifesto (`tomyfuture.kids` / "A Manifesto Rant on Education") and the EV proposal. Use the copy below as canonical. Light edits to fit the page are fine; do not rewrite the substance.

### Section 4 — Why school exists the way it does

Paper background. Two-column on desktop (heading left, body right), stacked on mobile.

**Heading (Newsreader italic, h2 scale):**
*The architecture was built for a world that no longer exists.*

**Body, three short paragraphs (Geist 19-22px editorial):**

> School wasn't designed to produce great thinkers. It was designed, two hundred years ago, to produce compliant industrial workers. Everything about its architecture reinforces this. The ringing bells signaling shifts. The fixed class periods. The regimented schedules. The requirement to raise your hand just to use the bathroom. Bells were factory whistles. Rows of desks were assembly lines. Tests were quality control.
>
> It conditions kids to internalize the rules of smallness. Don't stand out. Don't question. Don't be too passionate, too curious, too loud, too different. Just follow the script, hit the rubric, and keep your head down.
>
> The real world doesn't reward rule-followers. It rewards builders, risk-takers, people who can decide what to make next. School teaches the opposite. And then we wonder why ambitious kids spend their twenties undoing it.

**Inline factoid, top right of the body column (Geist Mono 11px tracked, thin saffron line beneath):**
`200 years` · `architecture unchanged`

---

### Section 5 — What AI changed

Paper-soft alternate background. Single-column, centered, ~720px container. Tighter and faster than section 4.

**Heading (Newsreader italic, h2):**
*A tutor with infinite patience just went to roughly free.*

**Body, two paragraphs:**

> A kid today can ask an AI any question and get a patient, correct, personalized answer. At 2am, in their language, without being made to feel stupid. The single scarcest resource in all of education — a tutor who has infinite time for you — just stopped being scarce. School has spent twelve years drilling the one thing AI now does better than any teacher. And it has spent almost no time on the things that actually decide a life.
>
> The temptation is to treat this as a feature. Add an AI sidebar to the existing curriculum. Let kids use ChatGPT for homework. That's the patch most schools are debating. But a patch on the wrong architecture is still the wrong architecture. The question isn't whether kids should use AI in school. It is: what should school look like when every kid already has a tutor smarter than their teacher in their pocket?

**Pulled stat in a small inset card beneath the body, saffron border:**
`2.6×` · *faster learning, Alpha School, two hours a day on AI-adaptive tools.*

---

### Section 6 — What's left for humans

Paper background. Three-column on desktop, stacked on mobile. Each column is a single concept with a one-line definition and a sentence of texture. Editorial, restrained.

**Heading (Newsreader italic, h2):**
*The day school never had time for.*

**Three columns:**

**Agency**
The discipline to decide what to build next.
Not "follow the assignment." Not "pick the right answer." Look at the world and pick what to make.

**Taste**
Knowing when the thing you made is good.
A rubric can tell you if you hit a target. Taste tells you if the target was worth hitting.

**Craft**
The patience to finish, and to make it good.
The hardest gap to close. AI gives you a first draft instantly. Craft is what you do with the next twenty drafts.

**Full-width closing line beneath the columns (Newsreader italic, ~22-28px):**
*None of these are taught in any school I know.*

---

## What to delete

### The "Open-source protocol" three-card section (R1 section 7) — DELETE

The entire three-card block (ArenaTutor v0, Free Virtual Cohort, Arena Protocol) goes. The word "protocol" reads as jargon to a parent or a 16-year-old considering applying. The artifacts matter, but they are not the pitch.

**Replace it with one quiet sentence.** Paper background, centered, ~640px container, Newsreader italic ~22-26px:

> *Arena is open-source from day one. The model, the curriculum, the playbooks — anyone can fork it. We aren't building another prestige school. We are building a new default.*

Beneath that line, a single row of three small Geist Mono 11px tracked labels, separated by middle dots and centered:

`Open base model` · `Full curriculum` · `Mentor playbook`

That's it. No cards. No GitHub badges on the public homepage. The deliverables get a real treatment later, on a separate page or in the footer. The homepage should make people *care* first.

### "For operators" section (R1 section 10) — DROP

Delete entirely. The homepage is recruiting Cohort Zero applicants. Operators are a v2 audience. Adding them dilutes the page. Move the operator pitch to a separate `/operators` page later.

## Carry-over from the previous brief (still apply these)

- **Footer (was R1 7.9):** monogram echo above wordmark, four-column link reorganization (Learn / Cohorts / Open-source / Meta), mono license line "Arena Protocol is MIT-licensed. Fork it."
- **Hubs map mobile (was R1 7):** vertical-stack variant under 520px with a thin saffron line that animates top-to-bottom on scroll.
- **Cohort Zero strip motion (was R1 7):** add the 80ms staggered reveal-up the other sections use.
- **Nav (was R1 7):** add the live status band above the fold — saffron pulse dot, Geist Mono 11px, `LIVE  -  Cohort Zero applications open  -  closes August 15, 2026`. Dismissable. Hides when nav goes sticky.
- **Hero monogram polish:** three small hub-dots arranged in a triangle (SF top, Shenzhen right, Bali left) connected by thin lines, slow 60s rotation, single saffron stroke.
- **Manifesto attribution:** replace "Phillip An, founder" with a Geist Mono line linking out, `Read the full essay at tomyfuture.kids ->` with a saffron arrow and a 2px hover lift.

## Keep these unchanged

- Hero headline and the inversion thesis paragraph.
- Pilot proof numbers (9.5/10 NPS, 5 days, two students to Stanford and elite UK boarding schools).
- Manifesto dark-band paragraph copy verbatim (the parents-bet-on-education arc).
- The bet section's four count-up stats (10 / 1,000+ / 50+ / 4).
- Closing dark band: "Build it with us."

## Deliverables

- Updated `index.html`, `styles.css`, `motion.js` with new sections + deletions applied.
- Updated `AUDIT.md` with R2 per-section scores. Add rows for the three new philosophy sections (4, 5, 6). Remove the protocol-cards row and the operators row. Target overall average ≥9.0.
- A short paragraph in `AUDIT.md` on what the philosophy pass changed: the page stopped being a brochure and started being an argument.

Voice in the new philosophy sections is honest and literary, not snarky. The user wrote these ideas because he believes them, not because they sound clever. Match that.
