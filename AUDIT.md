# Arena — Homepage Audit

**Round:** R2 (content-and-structure pass)
**Date:** 2026-05-29
**Scope:** `index.html` + `styles.css` + `motion.js`
**What changed this round:** added three philosophy sections (Why school exists / What AI changed / What's left for humans); deleted the three-card open-source "protocol" block and replaced it with one quiet line; dropped the "For operators" section entirely; plus the carry-over polish (live status ticker, triangle hero monogram, mobile hubs timeline, cohort reveals + count-ups, footer monogram + four-column reorg, manifesto essay link).

Scoring is 1–10 per dimension, per section. Target ≥9.0 average.

---

## Per-section scores

| # | Section | Hierarchy | Whitespace | Voice | Concreteness | Motion | Mobile | Density | Avg |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | Nav + status ticker | 9 | 9 | 9 | 9 | 9 | 9 | 9 | **9.0** |
| 2 | Hero | 9 | 9 | 9 | 9 | 9 | 9 | 8 | **8.9** |
| 3 | Pilot proof | 9 | 9 | 9 | 10 | 9 | 9 | 8 | **9.0** |
| 4 | Why school exists *(new)* | 9 | 9 | 10 | 9 | 8 | 9 | 9 | **9.0** |
| 5 | What AI changed *(new)* | 9 | 10 | 10 | 9 | 8 | 9 | 9 | **9.1** |
| 6 | What's left for humans *(new)* | 9 | 9 | 10 | 8 | 8 | 9 | 9 | **8.9** |
| 7 | The structure | 9 | 9 | 9 | 9 | 8 | 9 | 9 | **8.9** |
| 8 | Rotating hubs map | 9 | 9 | 9 | 8 | 9 | 9 | 9 | **8.9** |
| 9 | Manifesto | 9 | 10 | 10 | 8 | 8 | 9 | 8 | **8.9** |
| 10 | Open-source (one line) | 9 | 10 | 10 | 8 | 8 | 9 | 8 | **8.9** |
| 11 | The bet | 9 | 9 | 8 | 10 | 9 | 9 | 8 | **8.9** |
| 12 | Cohort Zero strip | 9 | 9 | 9 | 10 | 9 | 9 | 9 | **9.1** |
| 13 | Closing CTA | 9 | 10 | 9 | 8 | 9 | 9 | 8 | **8.9** |
| 14 | Footer | 9 | 9 | 8 | 8 | 8 | 9 | 9 | **8.6** |

**R2 overall average: ~8.9** (R1 was ~8.4)

*Removed from the rubric vs R1:* the three-card "Open-source protocol" row and the "For operators" row — both sections no longer exist.

---

## What the philosophy pass changed

R1 was a brochure: it showed the structure, the proof, and the deliverables, but it never made the argument. R2 turns the page into an argument. The reader now walks a line of reasoning before they ever reach the structure — **why** the architecture of school was built for a world that's gone, **what** AI actually changed (a tutor with infinite patience went to roughly free), and **what's left** that no school has time for (agency, taste, craft). Only then does the page show how Arena's day is built, so the structure reads as a *consequence* of the argument rather than a feature list. Deleting the "protocol" cards and the operators pitch removed the two most brochure-like, jargon-heavy blocks; the homepage now makes a parent or a sixteen-year-old *care* first, and leaves the artifacts and the operator funnel for dedicated pages later.

## Carry-over polish landed
- **Status ticker** — saffron pulse dot + mono line, dismissable, retracts when the nav goes sticky (nav rises to top in concert).
- **Hero monogram** — now three hub-dots in a triangle (SF top, Shenzhen right, Bali left) on a slow 60s rotation, single saffron stroke.
- **Hubs mobile** — under 520px the SVG arc swaps to a vertical timeline with a saffron line that draws top-to-bottom on scroll; desktop arc unchanged.
- **Cohort Zero** — eligibility rows and seat counts now reveal with the page's 80ms stagger and count up.
- **Footer** — monogram echo, MIT line in mono, four columns (Learn / Cohorts / Open-source / Meta).
- **Manifesto** — attribution replaced with a mono essay link (saffron arrow, 2px hover lift).

## Push for R3
1. **Footer (8.6)** is still the floor — voice and concreteness are thin. Consider a one-line mission restatement and a real "applications close" countdown rather than a static date.
2. **What's left for humans (concreteness 8)** — the three concepts are strong but abstract; a single concrete example under each (a real student project that demanded agency / taste / craft) would ground them. Needs real material from the user.
3. **Motion on the philosophy sections (8)** — currently the standard reveal-up. A subtle per-line or per-clause reveal on the Why-section prose could reward reading without drifting gimmicky.
4. **The bet voice (8)** — the stat labels are slightly flat next to the literary sections around them; tighten the copy.
5. Real assets still pending: pilot photo (drag-and-drop slot), finalized wordmark, real apply URL (currently `mailto:`).

## Notes
- Count-ups: `9.5/10`, `5`, `2` (pilot); `50`, `4`, `12`, `25`, `250` (cohort); `10 / 1,000+ / 50+ / 4` (the bet). The `2.6×` and `200 years` figures are set type, not animated.
- Dates remain placeholders: applications close **15 August 2026**, program **Fall 2026**.
- All reveal/draw motion is guarded by `prefers-reduced-motion`.
