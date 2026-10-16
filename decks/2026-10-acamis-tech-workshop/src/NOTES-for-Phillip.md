# Notes for Phillip: ACAMIS deck restructure (Oct 16)

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
