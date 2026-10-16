# Notes for Phillip: ACAMIS deck restructure (Oct 16)

## Pass 8 (Oct 16, late night): diagrams instead of text tables

Your note: the slides should be designed more visually, with more diagrams instead of just text. This pass redraws every text-heavy main slide as a visual. The running order, headlines, numbers, slide copy, and click counts are unchanged, and the Pass 6 look is kept: white and off-white grounds, navy accents, Newsreader, line icons in hairline circles, and the same 600ms fade for every build step. All new styles are in `css/s99zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz-p8.css`, with a matching Pass 8 block at the end of `reader/reader.css` for the phone reader.

**What changed, slide by slide**
- **2, Contents:** a four-stop route. Each part gets an icon node on one line, and Part 3 is the filled navy node, labelled "the main event". The descriptions are shortened a little. The agenda links (`data-go` 2, 9, 16, 21) still work.
- **4, About:** the three text cards are now icon cards. "How we teach" is a three-step flow (learners make every decision, AI does the building, real work for a real audience), and "Who we work with" has an icon per group. The logo rows are unchanged.
- **6, Philosophy:** a chain, Agency → Taste → Craft, each with a large icon (compass, eye, hammer) and a verb (choose, judge, finish, the words slide 24 already uses). "Without it" sits under a dashed rule. The same three icons come back on slide 23.
- **7, Two studies:** two charts. On the left, a zero line with three columns: without AI, plain ChatGPT (a bar dropping to −17%), and the hints-not-answers tutor (a check mark on the line, "largely avoided the drop"). On the right, two bars on one scale: an active-learning class (1×) and the AI tutor built on the same methods (2×). The footnote is unchanged.
- **8, Framework:** a cycle. The four strands sit around a ring (01 top left, then clockwise) with arrows between them, and the center reads "The learner decides". In each card, icons mark the three rows: the learner decides, AI helps, the teacher asks. "Then the next question starts the cycle again" sits under the ring.
- **9, Assessment:** an iceberg. Above the waterline is the tip, "The product: what AI can polish". Below it, a navy panel holds "The thinking behind it: what we assess", the four outcomes with their icons, and the evidence (process journal, drafts, recorded defense). "In practice: used with ISB students, summer 2026" now sits at the top right of the panel.
- **14, Bodley case:** the four steps are a path of icon nodes (found, sketched, built, changed), with a dashed loop from "Changed it" back to "Built it" to show the revision. The learning outcomes are now three icon chips, using the icons from slide 9.
- **16, Learning goals (the slide you sent):** a five-day journey. Across the top are days 1 to 5, with their icons and slide 12's day names. Each learning goal is one row: a bar spans the days that built it (pick a problem and a plan on day 1, test with users on days 1 to 3, ship on day 2 and price on day 4, rebuild on day 3 and defend on day 5), and an artifact card on the right shows what students showed. The closing line is unchanged.
- **18, Teachers' questions:** each question is a speech bubble with its icon, answered underneath next to a check mark.
- **19, Time back:** 31% is a bar chart of planning time, without AI and with AI, with the cut 31% shown dashed. 5.9 hours sits beside six calendar icons for "about six weeks a school year". The grading-timer card is unchanged.
- **23, Coach:** the role shift is drawn as two icon states (a book for "the person with the answers", speech bubbles for "the coach who asks the questions") with an arrow between them. Each question card has its skill icon from slide 6.
- **24, The big picture:** the four takeaways are four stops on one line (scale, presentation, hammer, calendar). Start on Monday is the filled navy stop.
- **Not redrawn:** 1, 3, 10, 17, and 22 (the photo cover and Part slides), 5 (the question), 11 and 15 (photo slides), 12 (already a timeline), 13 (the tool map), 20 (already a mock-up of each tool), 21 (already a three-step flow with a Claude Code mock-up), 25 (contact), and the backup slides.

**Speaker notes.** Three notes described the old column layout, so I changed only those words: slide 8 "Read each column top to bottom" became "Read each card top to bottom", and "In every column" became "In every card". Slide 16 "one per column" became "one per row, and the days of the week that built each one". Nothing else in the notes changed.

**Rules held.** No new numbers. The charts plot only the deck's existing −17%, 2×, 31%, and 5.9 hours, and the tutor column has no number, because the paper says only "largely mitigated". There are no em dashes, no cohort size, no new photos, and no new names. Six Lucide icons were added to `icons/`: calendar, eye, check, arrow-right, arrow-down, and monitor.

**Checks.** `contain.py --georgia` is 0 on every line, including the phone letterbox and phone type-size passes. `reader_check.py` says "reader OK", and I looked at every redrawn slide on the phone. `shots.py` reports no slide taller than 1080 and no page errors. One change to a check script: `contain.py` now treats the slide 8 ring like the existing `.ring2` diagram, so the center disk sitting on the ring isn't counted as an overlap. **`export.py --out /tmp/p8export` (a dry run) succeeded:** both PDFs are 36 pages. The presenting PDF is 5.6 MB, and `slides-en.pdf` is 5.9 MB, right at the cap. The real `export.py` was **not** run, so the public PDF and slide images still show Pass 7. Run it before deploying. (On this machine, only `/usr/bin/python3` has `pypdf`.)

**Calls to confirm**
- **Slide 7's tutor column** is a check mark on the zero line, not a bar, so it doesn't imply a number the paper doesn't give. Say if you'd rather drop that column.
- **Slide 2** now labels Part 3 "the main event", which the notes already say. Easy to remove.
- **Slide 16's research row** runs across days 1 to 3, as the old table said, with one label in the middle.

## Pass 6 (Oct 16, late): the Arena "pro" design system

This is a visual pass only. Pass 5's structure, running order, headlines, and narrative are unchanged. The only copy edits are the slide 4 logo labels and the slide 15 photo caption, plus the two speaker-note lines that describe them.

**Source.** Everything is ported from `~/arena-elegance` (branch `dev`, commit c8d8822): the `css/pro.css` tokens and type scale, the `css/cine.css` hero, the `PHOTO-PICKS.md` photos, the `LOGOS.md` logo rules, and the gentle reveal timing. All of it is copied into one new deck file, `css/s99zzzzzzzzzzzzzzzzzzzzzzzzzzzzz-p6.css`, plus a Pass 6 block at the end of `reader/reader.css`. Nothing in `~/arena-elegance` was edited.

**What changed**
- **Grounds and color:** cream and the dot grid are gone. Slides are white, the alternate slides are cool off-white (#F5F7FA), and navy is the accent. Cards are white with a 1px hairline, and the navy cards stay navy. The deck's own tokens (`--paper`, `--paper-hi`, `--beige`, `--line`, `--edge`) are recolored, so every slide picks this up.
- **Type:** content headlines use one restrained clamp() scale (`--p6-h2`, which comes out at 46 slide px instead of 50) in the same Newsreader serif. Every small-caps label (kickers, "Without it", "Agency" tags, and so on) is now the site's quiet Geist sans eyebrow. The halftone highlight bands (the cover's "to Classroom" and slide 5's rotating phrase) are removed, so accents are italic only.
- **Cover (slide 1), built like the site hero:** a full-bleed crossfade of the four PHOTO-PICKS photos (pitch-duo, isb-pitch-gesture, mentor-feedback, collab-stage-poster), 7 seconds each with a slow 1.02 to 1.1 zoom, under the site's navy gradient. The ivory crest sits above the headline, a faint dot texture fades toward the photo side, the white type and ISB logo are reversed out, and the QR sits on a white tile. Small captions match the site's ("Presenting at demo day, Beijing 2026" and so on). In export, the PDF, the phone reader under reduced motion, and prefers-reduced-motion, it shows the first photo, still.
- **Part slides (3, 10, 17, 22) and the big picture (24)** are no longer full navy. The part slides are off-white with a navy numeral and rule, and slide 24 is white with navy numerals. Navy is now an accent, not a ground. The navy slide-change curtain is now off-white to match.
- **Photos:** the winner photo (prize cheque) is gone from slide 15, replaced by `isb-pitch-gesture` with the caption "Teams defended their choices live". The note now reads "And every team defended its choices live, in front of the panel." On slide 11, `demo-laptop` (neutral faces) became `pitch-duo`, the happier frame of the same demo moment. The caption is unchanged.
- **Logos:** slide 4's strip is now two labelled rows, "Our team studied at" (ISB, Brown, Caltech, Harvard, Tsinghua) and "Our team worked at" (McKinsey, Goldman Sachs, Y Combinator, Apple, Microsoft AI, Deloitte, Kimi), in the LOGOS.md set and order. Each row is a slow marquee (44s and 58s) with faded edges. The static row is kept for export and reduced motion. In the note, "on this line" became "on these two rows". All logos in the deck (team, judges, "Selected for", tool icons on slides 12, 13, and 21) are greyscale, at the existing optical heights, which already follow the site's proportions.
- **Motion:** one gentle reveal everywhere, a 600ms ease-out fade with a 12px rise. The scale "pops" are removed (day dots on slide 12, timeline dots), and so is the photo settle-zoom. The marquee and the cover crossfade are the only continuous motion, and both stop under reduced motion.
- **Phone reader:** same palette, a full-bleed photo cover with the crest (a dark top bar on that slide), light part slides, greyscale logos, and static logo rows. The `theme-color` values in `build.py` and `reader.js` are now white, off-white, and navy instead of cream.
- **Check script:** `contain.py`'s live pass now also ignores overlaps between the scrolling marquee logos and their row label, because the strip clips them by design. The export pass still checks the static rows.

**Checks:** `contain.py --georgia` is 0 on every line. `reader_check.py` says "reader OK". `shots.py` reports no slide taller than 1080 and no page errors. In motion mode, the cover crossfades and both logo rows scroll, with no page errors. **`export.py --out /tmp/p6export` (a dry run) succeeded:** both PDFs are 36 pages and 5.6 MB, under the 5.9 MB cap, and I opened and checked the slide images. The real `export.py` (which overwrites the public PDF, slide images, and slide count in `talks/`) was **not** run. Run it before deploying, so the public PDF picks up the new look.

**Calls to confirm**
- **"No other organization's name on screen."** I applied this to photos: no photo shows another organization's name. The deck still names other organizations as content: the judges' affiliations on slide 15 (headline and logo strip), the team logos on slide 4, and the Anthropic and OpenAI "Selected for" box. I left those, because changing them is a content call. Tell me if you meant to remove them.
- **Program name.** The deck calls the case the "ISB AI Founders Program, August 5–9, 2026". "AI Fundamentals for Students @ International School of Beijing" (the winter program's name on the site) doesn't appear in the deck, and I didn't add or rename anything.
- **Slide 18** says "Use only the tools your school approves, with no student data in them." That's advice to teachers rather than a claim about a tool, so I left it. If it's too close to the "no student data" claims we avoid, a rewording would be "and keep student data out of them."
- **Slide 15, `isb-judges-test`.** PHOTO-PICKS notes that who is in this photo is unconfirmed. It's still on the slide, captioned "Judges test each product before scoring". Please confirm those are judges.
- **Part slides have no photos.** There are only four approved bright photos, and they're already used on the cover, 11, and 15, so photos on the part slides would mean repeats. If you'd like photo-led part slides anyway, it's a quick add.
- **Not restyled:** the session page (`talks/<slug>/index.html`, hand-edited) and the backup slides, beyond what the shared tokens change. No Ben tool examples appear in the deck.

## Pass 5 (Oct 16, night): summaries, contact, motion, stronger headlines

This section supersedes the Pass 4 running order for slides 15 to 25. Slides 1 to 15 and the backup keep their places.

**What changed**
- **New slide 16, "How the week built each learning goal"** (end of the student part). It uses the same swimlane as slide 8, so the audience sees the framework return filled in. There are four columns (one per strand), and each has three rows: the learning goal, how the week built it (by day), and what students showed. It closes on "No worksheet and no quiz. The evidence is the work itself."
- **Slide 24, "The big picture"** (the grand summary at the end of the educator part). It replaces the old close: "AI can do the making. The thinking is still ours to teach.", followed by all four takeaways. The old close was missing takeaway 3, "Teachers can build". It ends on "You don't need to code. You already know how to coach."
- **Slide 25, "Let's build this at your school"** (the final slide, which also hosts Q&A). It merges the old "What we offer" slide with the old Q&A slide. Three ways to collaborate (train your teachers, run a student week, design your curriculum), then a card for each of you with a photo, your WeChat ID (phgan14, jj-xiaohan), and a WhatsApp QR code (wa.me links). A navy card carries today's slides QR and arenaschool.org. There is no cal.com link and no "book a call" QR. The emails are gone from this slide, but they're still on the founders backup slide.
- **Logo marquee (slide 4):** the founding-team logos now scroll as a slow, continuous carousel with soft faded edges, and the strip pauses on hover. Export, the PDF, the phone reader, and prefers-reduced-motion all show the original static row, because the second copy of the logos is hidden there.
- **Entrance motion:** on slide 12, the timeline axis draws across and each day's dot pops in as it builds. On slides 8 and 16, the highlighted swimlane band sweeps in. The demo-day and program photos settle from a slight zoom as they appear. On slide 24, each numeral rises a beat ahead of its line. On slide 25, the three ways arrive one after another, then the people. All of this runs under `html.motion`, so export and reduced-motion get the finished slide.
- **Headlines, rewritten to be shorter and to claim more:**
  - 3: "We teach the part of learning that AI can't do for you."
  - 4: "AI tools change every week. We teach learners to make the calls." (This is the uniqueness line. The mission line moved to the notes.)
  - 6: "Three human skills AI can't supply. Without them, AI does the thinking."
  - 7: "Same AI, opposite results. The design decides."
  - 8: "AI helps at every step of the cycle. Every decision stays with the learner."
  - 9: "When AI can polish the product, we assess the thinking behind it."
  - 12: "Ten stages in five days, and every day ends with something real."
  - 20: "Teachers don't need to code to build for their own class."
  - 2 and 22: the agenda and the Part 4 subtitle now read "the big picture … how to work with us".
- **Speaker notes** for 15, 16, 23, 24, and 25 are rewritten so that each one hands off to the next. The line "None of it works without teachers" moved from 15 to 16.

**Running order: 25 main slides, then 11 backup slides (26 to 36)**
1 to 15 as in Pass 4 · **16 How the week built each learning goal** · 17 Part 3 · 18 Pain points · 19 Time back · 20 Teachers build · 21 Build session · 22 Part 4 · 23 Coach · **24 The big picture** · **25 Let's build this at your school**. Agenda links are `data-go` 2, 9, 16, 21.

**Narration arc for the new and changed slides**
| # | The one point, and the handoff |
|---|---|
| 15 | Judges tried every product; students can ship. "Did a week of building teach what we set out to teach?" |
| 16 | Every learning goal was practiced on real work, and the evidence is the work itself. "None of it works without teachers." |
| 23 | Three coaching questions for Monday. "Let me pull the whole hour together." |
| 24 | AI does the making, the thinking is ours to teach: the four takeaways. "Here is how to reach us." |
| 25 | Three ways to work together, then WeChat and WhatsApp. Then Q&A. |

**Calls to confirm**
- **Slide 16 rows** are drawn from the deck's own day-by-day slide (12) and the backup slide on what the week trained. "Choices backed by what users did" is my phrasing of the day 1 to 3 validation and user-testing stages. Please check that it matches what students actually showed.
- **Slide 4 headline.** "AI tools change every week. We teach learners to make the calls." is the strongest uniqueness claim in the deck. If you'd rather keep "Helping students, families, educators, and schools thrive in the age of AI," it's one line to swap back.
- **Phone number privacy.** The WhatsApp QR codes encode your phone numbers, and slide 25 is also published in the public PDF and the phone reader once `export.py` runs. The numbers are not printed as text on the slide.
- **"What we offer" no longer has its own slide.** The "Selected work" proof (the ISB, Bodley, and Tsinghua logos, and the results link) went with it. Slide 4's marquee and slide 15's judges carry the credibility now. If you want the proof back, it could be a slim marquee under the slide 25 cards.

**Checks:** `contain.py --georgia` is 0 on every line, `reader_check.py` says "reader OK", and `shots.py` reports no slide taller than 1080 and no page errors. `contain.py` now skips the marquee strip in its live pass, because the strip scrolls inside a clipping frame by design; the export pass still checks it as a static row. Slide 25 got its own phone-reader layout. I verified the marquee in motion mode (it scrolls, with no page errors), and both WhatsApp QR images match a fresh encoding of their wa.me links. `export.py` was not run, as before.

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
