# Notes for Phillip: ACAMIS deck restructure (Oct 16)

## Pass 4 (Oct 16, evening): compress, one case, unblur, narrative

This section supersedes the running order, the "cases 2 and 3" and "prize amount" items, and the timing risk further down.

**What changed**
- **Framework block, 6 slides down to 3:** philosophy (6), the framework as the "where AI comes in" swimlane (8), and **one new slide (9) merging outcomes and assessment**: one outcome per strand plus the evidence band (process journal, drafts, recorded defense; used at ISB). The wheel, the full outcomes list, the rubric, and the programs map moved to backup.
- **One case study:** Bodley is the case (14), retitled "The case · where it started". The placeholder cases 2 and 3 are deleted, not moved, since they had no content.
- **Winner photo:** the deck uses the original `isb-winners-1400.webp` again, and the blurred copy is deleted.
- **Repetition cut:** the About slide no longer names agency, taste, and craft (slide 6 does that, once). The founders' bios moved to backup, so slide 4's logo strip and its notes are the only "who we are" moment. "Week analysis", "build loop", and "where AI helps" moved to backup because they re-explained the three skills or the build steps.
- **Part 4** is now "Start small, and start on Monday." The tracker label and agenda item 4 match. The close slide's three points are reordered to follow the takeaways (design decides, students can ship, start small), and "one project" became "one tool".
- **Speaker notes:** all 25 main slides are rewritten so each ends by setting up the next one.

**Running order: 25 main slides (20 before the build), then 11 backup slides**

## The four takeaways
1. **Design decides.** With AI, learners still have to do the thinking (agency, taste, and craft), and whether AI helps or hurts depends on how the work is designed.
2. **Students can ship.** A five-day program inside a school took students with no coding background to live products that real users and judges tried.
3. **Teachers can build too.** AI gives teachers time back, and in plain English you can build a tool for your own class. The build session proves it in the room.
4. **Start small on Monday.** You become the coach who asks three questions: one tool, one class. Arena can help you go further.

## Narration arc, one line per slide
| # | Slide | Takeaway | The one point, and the handoff |
|---|---|---|---|
| 1 | Cover | | A case study from ISB; scan for the resources. "Here is the hour." |
| 2 | Contents | | Four parts, and the build is the main event. |
| 3 | Part 1 | 1 | Who we are, and the one idea behind everything. |
| 4 | About Arena | 1 | Hands-on programs where learners decide and AI builds; credibility strip; Jing Jing's homecoming. "It starts from one question." |
| 5 | The question | 1 | When AI can do all of this, what must students still learn? "Here is our answer." |
| 6 | Philosophy | 1 | Three human skills: agency, taste, and craft (named once, here). "And this isn't only our opinion." |
| 7 | Research | 1 | Same AI, opposite results (−17% vs 2×): the design decides. "That's what our framework is for." |
| 8 | Framework | 1 | Four strands as a cycle: AI does the making, the learner decides, the teacher asks. |
| 9 | Outcomes and assessment | 1 | One outcome per strand, assessed on the process. "So what does this look like in a real school?" |
| 10 | Part 2 | 2 | The framework running for real at ISB. |
| 11 | The program | 2 | Five days, grades 7 to 12, no coding, a live product by Friday. |
| 12 | Day by day | 2 | Each day trains one skill and ends with something real. |
| 13 | The tools | 2 | 200+ tools; they learned the habit of choosing, not the list. "Here's one student." |
| 14 | Bodley case | 2 | An 11-year-old's sign-language app: chose it, built it, revised it for his grandmother. Three outcomes from slide 9. |
| 15 | Demo day | 2 | Judges tried every product; same tools, and the three skills made the difference. "None of it works without teachers." |
| 16 | Part 3 | 3 | Now it's about you. |
| 17 | Pain points | 3 | Teachers lack time, approved tools, and a place to start. "Let's start with time." |
| 18 | Time back | 3 | 31% and 5.9 hours; the grading timer. AI handles the housekeeping, and the teacher keeps the judgment. |
| 19 | Teachers build | 3 | Literary devices and simulations, in plain English. "That's what we'll do now." |
| 20 | Build session | 3 | Name it, build it, judge it, the same loop students run. **Then the 30-minute build.** |
| 21 | Part 4 | 4 | Back to Monday. |
| 22 | Coach | 4 | From the person with the answers to the coach with three questions. |
| 23 | What we offer | 4 | Three programs on the same framework, for when one hour isn't enough. |
| 24 | Close | 1, 2, 4 | Design decides; students can ship; start small. "You already know how to coach." |
| 25 | Q&A | | Resources and contacts. |

**Backup (26 to 36):** framework wheel · all learning outcomes · assessment rubric · programs map · what the week trained (three-skill analysis) · build session as the framework loop · where AI helps · founders' bios · what parents asked · is it cheating? · planning checklist. Every backup kicker starts with "Backup ·". Agenda links are now `data-go` 2, 9, 15, 20.

**Timing:** 20 slides before the build, at about 75 seconds each, comes to about 25 minutes, then 30 for the build and about 5 for slides 21 to 25. If you're running long before the build, skip 13 (tools) or 7 (research) first.

## Pass 4: open items
- **Bodley first sketch:** optional, as before.
- **Founders' bios:** I moved them to backup because slide 4 already covers the team, and after a 30-minute build the closing minutes are better spent on Monday. If you want them on screen, pull slide 33 forward to sit after slide 4, and drop the logo strip on slide 4 so the two don't repeat.
- **Demo-day analysis:** this is now one spoken line on slide 15, taken from the old slide 21 text ("every team had the same tools; the three skills made the difference"). Real judging criteria would make it stronger.
- **Public results page:** it still shows the winner photo with the amount visible (`results.html`). With the blur dropped, this no longer conflicts with the deck. Note that the deck's own rule ("no prize amounts") applies to text, and the cheque is legible in the photo at full size.

---

## Earlier passes (1 to 3)

Branch `deck-edits-acamis`, four commits, **not pushed**. `main` and the live site are untouched.

| Commit | Pass |
|---|---|
| `2f45170` | 1. Restructure into the four agreed parts |
| `b13a350` | 2. Formal diagrams |
| `ec590ab` | 3. Visual design, plus a trial palette |
| (last) | Prize amount blurred out of the winner photo; these notes |

To preview: `python3 -m http.server 8780` from the repo root, then open `/talks/2026-10-acamis-tech-workshop/deck.html`. Add `?theme=acad` to see the trial palette and `?notes` for speaker notes.

After every pass, all checks passed: `contain.py --georgia` is 0 on every line, `reader_check.py` says "reader OK", and `shots.py` reports no slide taller than 1080 and no page errors. I did **not** run `export.py`, because it rewrites the public PDF, the slide images, and the slide count on the session page. Run it once the placeholders are filled.

## The new running order (37 slides: 34 main, then 3 backup)

**Part 1 · Who we are and how we teach** (slides 3 to 12)
3 Part divider · 4 About Arena · 5 The question · 6 Philosophy · 7 Research (moved here as "why the design matters") · 8 Framework wheel · **9 NEW: where AI comes in** (swimlane: the learner decides / AI helps / the teacher asks, for each strand, with the cycle drawn) · 10 Outcomes · 11 Assessment rubric · **12 NEW: programs map** (the framework mapped onto the student short course, AI for Educators, and curriculum design, with a "learners leave with" band)

**Part 2 · Case study, ISB AI Founders week** (13 to 21)
13 Divider · 14 Program overview · **15 Day by day, rebuilt as a timeline** (stages, main tools, skill trained, and output for each day) · 16 Tools by job · **17 to 19 Cases on one template** (found the problem, sketched it, built it, changed it, then the learning outcomes it shows). Case 1 is Bodley; **cases 2 and 3 are placeholders.** · 20 Demo day, now with the winning-team photo · 21 Analysis (the "each skill got a moment" slide, reframed as looking back)

**Part 3 · Let's build together** (22 to 27)
22 Divider · **23 NEW: teachers' pain points** (four concerns from our own website FAQs) · 24 Time back (31%, 5.9 hours, grading timer) · 25 Tools teachers build · **26 NEW: the build session as the framework loop** · 27 The build brief

**Part 4 · Wrap-up** (28 to 34)
28 Divider · **29 NEW: where AI helps** students, teachers, and schools, each tied to an outcome · 30 Coach and three questions · 31 What we offer (retitled "three programs, one framework") · **32 NEW: founder bios** with photos · 33 Close · 34 Q&A, now with both of your emails

**Backup** (35 to 37): parents survey, "Is it cheating?", and the planning checklist. They are kept for questions, and their kickers start with "Backup ·".

The agenda links (`data-go` 2, 12, 21, 27), the part trackers, and the slide comments are all renumbered.

## Missing assets and placeholders (marked in orange and dashed on the slides)

1. **Cases 2 and 3 (slides 18 and 19): all the content.** For each of two ISB teams I need how they found the problem, the first sketch or wireframe, what they built and with which tools, what changed after users tried it, and which three learning outcomes it shows. I also need a **wireframe or sketch image** and a **screenshot of the product**. Rules still apply: no student names, no product names, no cohort size.
2. **Bodley first sketch (slide 17, step 2), optional.** If we have his sketch, it can replace the one-line idea.
3. **Demo-day analysis (slide 21).** The brief asks for an analysis of the pitches. I have no facts on what the judges rewarded or what set the winning team apart, so for now the slide reuses the "each skill got a moment" content. A real analysis needs your input, for example the judging criteria and what the strongest pitches did.
4. **Prize amount: please check this.** The full-resolution winner photo shows "¥ 8,888" on the cheque. I made a copy with the amount and the amount-in-words line blurred (`photos/isb-hq/isb-winners-noamount-1400.webp`), and the deck uses that copy. **The original, with the amount visible, is still on the public results page** (`results.html`, `isb-winners-800.webp`). That's outside this deck, so I left it alone.

## Calls I made that you should confirm

- **Framework strand names.** The brief says "inquiry, build, feedback, reflect". I kept the deck's existing four strands (inquiry and planning, research and evaluation, creating and communicating, collaboration and reflection), because the wheel, the outcomes, and `research/` all use them. Renaming would mean changing all three.
- **Slide 9, the "AI helps" row and the fourth teacher question** ("What would you do differently?"). This wording is new and comes from no existing source. The first three questions also differ slightly from slide 30's three coaching questions, which follow agency, taste, and craft rather than the strands.
- **Slide 12 cells.** These are drawn from the website copy for the intensive, AI for Educators, and the curriculum design offer (`teacher-training.html`, `schools.html`). "Map where AI fits in each course" and "A plan and rubrics the faculty owns" are my phrasing of "where AI fits in your courses, and how to assess it".
- **Slide 15, skill trained by day** (Agency, Taste, Taste, Craft, Craft). I inferred this from slide 21's text, which puts agency on day one, taste from midweek, and craft at the fixed stop hour and on demo day. The day 5 output, "a two-minute pitch", comes from the old speaker notes.
- **Slide 17 (Bodley).** The stats strip (20 students, 5 days, 9.5/10) left the slide to make room for the outcomes row. The 9.5/10 is still in the speaker notes. Say if you want it back on the slide.
- **Slide 23.** The four concerns are our own website FAQs, framed as "What teachers ask us". They aren't quotes from named people, so they stay within the private-conversation rule.
- **Slides 4 and 32 overlap.** The About slide has the founding-team logo strip and slide 32 has the full bios. You could drop the logo strip, or say only "Arena was founded by…" on slide 4.

## Timing risk (please read)

There are 34 main slides, and the build session needs about 30 of the 60 minutes. That leaves about 28 slides for roughly 25 minutes, which is tight. If you need to cut, these are the first candidates: slide 7 (research, already cited on the site), slide 11 (rubric), slide 16 (tools: the timeline on 15 already shows the main tools by day), and slide 25 (overlaps with the build). Once the build starts, the slides drop away anyway.

## Palette: Arena vs. neutral academic

A side-by-side image is at `src/exports/palette-arena-vs-academic.png` (git-ignored). The trial is opt-in through `?theme=acad`, and you can delete it with two files: `css/s99zzzzzzzzzzzzzzzzzzzzzzz-theme.css` and `js/zzz-theme.html`.

- **Arena (navy on warm cream, dot texture). This is my recommendation for Sunday.** It matches arenaschool.org, the session page the QR codes open, the tool guide PDF, the phone reader, and the navy logos. JJ has pixel-checked it, and the conference also markets Arena, so it should look like Arena.
- **Neutral academic (ivory, charcoal, slate blue, no texture).** It looks crisper and more like a journal, and it reads as more institutional and "legitimate" to a skeptical teacher audience. The costs: it drifts from the brand two days before the talk, the phone reader stays in the Arena palette, and every slide would need another pixel pass from JJ. If you like it, it's better used for the next deck than switched in now.

On legitimacy, the bigger levers were structural rather than color: formal diagrams, one template for the case studies, outcomes tied to every case, the founder bios, and both contacts on the last slide.

## Housekeeping

- `README.md` still says "29 slides" and "work on main", and the session page will show the old slide count until `export.py` runs. I left them for the merge.
- New CSS lives in `css/s99zzzzzzzzzzzzzzzzzzzzz-r7.css` (pass 1) and `css/s99zzzzzzzzzzzzzzzzzzzzzz-r7b.css` (pass 2 and 3). New components use the `nx-` prefix. Their phone-reader rules are appended to `reader/reader.css`.
- `BRIEF.md` is still untracked and not committed.
