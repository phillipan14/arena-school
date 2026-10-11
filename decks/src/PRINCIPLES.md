# Slide principles for the parent talk

A short checklist for writing and laying out this deck. Every rule here comes from a named source and has been adapted to this deck: a 20-minute talk to ISB parents, most of them not specialists, read in English and Chinese, then shared as a PDF. House rules in `/DESIGN.md` and `/CONTENT-RULES.md` still apply and win any conflict.

Units: deck CSS px render ×1.32 at 1920×1080, and a 1920px slide is 960pt wide. So **CSS px × 0.66 ≈ pt**.

## 1. Storyline

- [ ] **Lead with the answer.** The deck has one governing thought, and each section supports it with claims, not topics. The talk opens with the situation, then the complication, then the question; the sections give the answer. *(Minto, Pyramid Principle and SCQA)*
- [ ] **Groups of three.** Each level has about three supports that don't overlap and leave nothing out (MECE). This deck: work is already changing / three skills matter more / small habits help at home. *(Minto; BCG and Bain practice)*
- [ ] **Write the titles first.** Draft the action titles as a "ghost deck" before building slides. Read them in order: alone, they must tell the whole story (the horizontal test). *(McKinsey practice: Slideworks, Arcdeck)*
- [ ] **Each title is proved by its own slide.** Everything below the title supports it, and anything that doesn't is cut (the vertical test). *(Slideworks; Alley)*
- [ ] **Contrast what is with what could be.** Move between the change at work and what a family can do about it. End on what the audience can do. *(Duarte, Resonate)*
- [ ] **Concrete beats abstract.** Use named jobs, a real hiring story, and real student projects, rather than trends. Avoid the curse of knowledge: no jargon, and statistics told at human scale ("1 in 3"). Every slide names a real company, job, person, or number; a slide a parent could only paraphrase as "things are changing" gets cut. *(Heath and Heath, Made to Stick)*
- [ ] **Pace like a talk, not a report.** Short statement slides (the question, a quote, the start of each part, the close) alternate with evidence slides, so the room gets a breath between proofs. *(Phillip's showcase-wrap deck; Duarte, Resonate)*

## 2. Each slide

- [ ] **Action title.** One full sentence that states the takeaway in plain words, about 15 words at most and two lines at most, left-aligned. Never a label like "How wide it is." No pronoun without a clear noun in the same line ("it", "this"). *(Alley, assertion-evidence; Slideworks)*
- [ ] **Kicker.** One short uppercase line above the title that sets the scene: who, where, or when ("149 US employers, spring 2026"). Never a topic label. *(Phillip's showcase-wrap deck)*
- [ ] **One message per slide.** A reader should be able to say the point back within about 10 seconds; the glance test is about 3 seconds. *(BCG "smart simplicity"; Duarte, HBR glance test)*
- [ ] **Evidence, not bullets.** Below the title, show the proof: a number, a comparison, a before/after, or a photo. Lists have 2–4 items, all parallel. *(Alley and Garner: better comprehension and recall than bullet slides)*
- [ ] **Few words.** No paragraphs. Every item uses the same grammar and the same tense. Don't put on the slide the sentence the speaker will say (the redundancy effect). *(Mayer, redundancy and coherence; Reynolds)*
- [ ] **Labels sit next to what they label.** No legends and no cross-referencing. A source sits on the slide it supports. *(Mayer, spatial contiguity; Tufte)*
- [ ] **A takeaway box only when it adds something.** Use one "so what" line at the foot only when the slide needs it, and never to repeat the title. *(Bumper box: Vini Sammon; Mayer, coherence)*
- [ ] **Source on every evidence slide.** A small numbered footnote at the bottom, in short form; the full list goes in the appendix. *(McKinsey and BCG conventions)*

## 3. Design

- [ ] **One grid, one rhythm.** The same margins and the same title position on every content slide. Elements align to the columns. White space is part of the design. *(Duarte, Slide:ology; Reynolds: contrast, repetition, alignment, proximity)*
- [ ] **Four levels of type, always the same.** Title 50, subtitle and body 26, card heading 32, labels, kickers, and sources 15–16 (CSS px); statement slides use a 72px title. That is about 33 / 17 / 21 / 10pt, inside Alley's ranges for titles and body. Source lines are for the PDF reader, not the room. *(Alley; Kawasaki 10/20/30 as the ceiling to aim toward)*
- [ ] **Big numbers are the biggest thing on the slide** (128–168px) when the slide is about a number. One callout, not several. *(BCG callout; Knaflic, focus)*
- [ ] **Signal over noise.** Cut chips, extra labels, decorative icons, and uneven boxes. Use rules and white space before borders. Every mark must carry information. *(Tufte, data-ink and chartjunk; Knaflic, clutter; Reynolds, signal-to-noise)*
- [ ] **One accent color, used to point.** Navy for text; the accent blue only for the key phrase or number. Ask "where are your eyes drawn?" and make the answer the point. *(Knaflic, preattentive attributes; Tufte, smallest effective difference)*
- [ ] **The same component for the same job.** Job cards, pillars, and habits share one card layout. Logos share one height and one baseline. *(Reynolds, repetition; Duarte, unity)*
- [ ] **Contrast is readable.** Body text at least 4.5:1 and large text at least 3:1. Meaning never depends on color alone. *(WCAG 2.2, 1.4.3; WebAIM)*
- [ ] **Location in the talk is always visible.** Each part opens on a navy statement slide whose kicker names it ("Part 2 · Skills"), the agenda links to those slides, and every slide carries a page number. This replaced the section tracker (10-11), which read as a label and took the title's space. *(Phillip's showcase-wrap deck; Mayer, signaling and segmenting)*

## 4. Parents and two languages

- [ ] **One idea, one example, one action.** Parents remember the story and the one thing they can do tonight. *(Heath and Heath; Duarte)*
- [ ] **Calm, credible numbers.** Give the share and the comparison; never alarm. Say the limits of a dataset where a reader could misread it. *(Heath, credible; CONTENT-RULES §5a)*
- [ ] **English and Chinese say the same thing,** and each reads naturally rather than as a translation. Chinese lines run about 17–40 characters, never fewer than about 10. Never break inside an embedded Latin name. *(W3C clreq #555 and #545; WCAG 1.4.8)*
- [ ] **No orphans.** English ends on two or more words; Chinese ends on three or more characters (guard.js and `.nw`). *(DESIGN.md §4.6)*

## 5. Review before shipping

- [ ] Read only the titles, top to bottom. Is it one story?
- [ ] Read only the kickers. Does each one say who, where, or when, rather than name a topic?
- [ ] For each slide, cover the title. Does the body prove it? Is anything left that doesn't?
- [ ] Squint at the screenshot. Is the first thing you see the point? Are edges aligned, cards equal, logos level?
- [ ] Every slide fits 1920×1080 in export mode, and no type was shrunk to make it fit.

## Sources

- Barbara Minto, *The Pyramid Principle*: [barbaraminto.com](https://barbaraminto.com/); summary, [BA Strategy Toolkit](https://thebastrategytoolkit.com/frameworks/pyramid-principle/)
- Michael Alley, assertion-evidence guidelines: [writing.engr.psu.edu](http://www.writing.engr.psu.edu/guidelines_AE_slides.pdf); Garner and Alley, comprehension study: [ae_comprehension.pdf](https://writing.engr.psu.edu/ae_comprehension.pdf)
- McKinsey practice: [action titles](https://slideworks.io/resources/how-to-write-action-titles-like-mckinsey), [how consultants build decks](https://slideworks.io/resources/how-mckinsey-consultants-make-presentations), [Arcdeck guide](https://arcdeck.ai/guides/mckinsey-style-presentation), [AutoPresent](https://www.autopresent.ing/blog/mckinsey-slide-decks/)
- BCG and Bain conventions: [Perceptis](https://perceptis.ai/blog/how-to-create-a-slide-like-mckinsey-or-bcg); bumper box: [Vini Sammon](https://vinisammon.com/the-management-consulting-presentation-framework.html)
- Nancy Duarte: [glance test, HBR](https://hbr.org/2012/10/do-your-slides-pass-the-glance-test); [Resonate sparkline](https://www.duarte.com/blog/ultimate-guide-to-contrast/); [Slide:ology, arrangement](https://www.oreilly.com/library/view/slide-ology/9780596522346/chapter-11.html)
- Garr Reynolds, *Presentation Zen*: [design tips](https://www.garrreynolds.com/design-tips)
- Edward Tufte, *The Visual Display of Quantitative Information*: [edwardtufte.com](https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/)
- Cole Nussbaumer Knaflic, *Storytelling with Data*: [declutter and focus](https://www.storytellingwithdata.com/blog/two-tips-for-better-graphs); [where are your eyes drawn](https://www.storytellingwithdata.com/blog/whereareyoureyesdrawn)
- Guy Kawasaki, [the 10/20/30 rule](https://guykawasaki.com/the_102030_rule/)
- Richard Mayer, multimedia learning principles: coherence, signaling, redundancy, spatial contiguity, and segmenting (*Cambridge Handbook of Multimedia Learning*)
- Chip and Dan Heath, *Made to Stick*: [summary](https://readingraphics.com/book-summary-made-to-stick/)
- W3C: [WCAG 2.2, contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html); [clreq #555, Chinese line length](https://github.com/w3c/clreq/issues/555)
