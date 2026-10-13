---
name: format-audit
description: Strict formatting and design audit for Arena School work (the arenaschool.org website, the parent-talk deck and its PDFs and phone reader, one-pagers, posters), or any page or deck JJ asks to audit. Every slide or page, every element, both languages, every breakpoint or build step, two full loops. Use when JJ says "format audit", "design audit", "formatting check", "audit the slides/site for formatting", "check centering/spacing", or asks for a final pass before something ships.
---

# Format audit

JJ is extremely detail-oriented. She has rejected work for misalignments of 2–5px, text that wraps when it doesn't need to, cramped cards, cut-off logos, and awkward empty space. This checklist is the standard: every item, every element, every time. "Looks fine" is not a result; measurements are.

## 0. Scope and setup
- **Audit everything in scope, not a sample:**
  - Deck: every slide, at every build step (step through with the arrow key), in live mode, export mode (what the PDF renders), and the phone reader.
  - Website: every page in scope, at 390, 768, 1280, and 1440px wide, plus WeChat/WebKit on phone.
- **Both languages** (EN and 中文), as separate passes. Chinese is never a mirror of the English layout; check it on its own.
- **Only touch what you were asked to audit.** Before any commit, `git diff --name-only` must list only in-scope files (for the deck: `decks/` and `talk/`). Never run site-wide scripts during a deck audit. Phillip edits other parts of the site in parallel.
- **Two full loops.** Loop 1: audit and fix everything. Loop 2: re-screenshot and redo the whole audit from the first slide or page with the same rigor. Fixes routinely break neighbors, so loop 2 is not optional.

## 1. Line breaks (priority 1)
- [ ] No line wraps when there is plenty of empty space beside it. If the container, or the free space next to it, could hold the text on fewer lines without crowding, remove whatever forces the break (manual `<br>`, `max-width`, `text-wrap: balance` squeezing, narrow column).
- [ ] No orphans. English: the last line has at least two words. Chinese: the last line has at least three characters.
- [ ] Never break inside a name, title, number range, date, URL, or term ("Claude / Opus 4.6", "Y / Combinator", "34% to / 140%", "AI-Powered / Lawyering", 主动/性, 哈/佛). Use non-breaking spaces or hyphens, `.nw` / `white-space: nowrap` spans, or a word segmenter.
- [ ] Chinese: no line starts with punctuation (，。、：；？！）」), no 1–2 character lines, no break inside a word or an embedded Latin term.
- [ ] Sibling cards with the same structure have the same number of lines per row. Rebalance the copy or width rather than letting one card run long.
- [ ] Titles: at most 2 lines, broken at a natural phrase boundary.

## 2. Margins and breathing room (priority 2)
- [ ] Slide or page margins are consistent: the same side gutters and the same title position on every content slide or section.
- [ ] Every card: at least 24px of inner padding, with nothing within 24px of its border. Text never looks pressed against an edge.
- [ ] Every pill or chip: equal left and right padding (ink to border), comfortable height, text not touching the ends.
- [ ] Sibling cards have equal padding and equal heights; gaps between siblings are equal.
- [ ] If text is cramped, first give it room (taller or wider container). If there isn't room, step the type down one size within the type scale. Never shrink below the scale minimums.

## 3. Centering: vertical and horizontal (priority 3; vertical is the one always missed)
- [ ] **Measure by ink, not by box.** Take a 2× screenshot and scan pixel rows and columns for the first and last inked pixel, or use canvas `measureText` actual bounds. A line box includes ascender and descender slack, so box-centered text usually looks too high or too low.
- [ ] Check every pill, card, button, icon-in-circle, number-in-shape, logo tile, list row, table cell, and band. Space above the ink must equal space below within 1px (rendered). Do the same left and right where centering is intended.
- [ ] Big numbers: their optical left edge (the ink, after side bearing) lines up with the caption or heading below. The number is centered on any pill or shape beside it.
- [ ] Rows of logos or icons share one optical center line and equal spacing.
- [ ] Multi-column blocks: each column's content is centered in the card on its own; the label block and the body text are both centered.

## 4. Negative space (no awkward blank areas)
- [ ] No large empty band that reads as a mistake: between the title and the content, at the bottom of a card, beside short text in a wide card, or under a one-line title in space reserved for two lines.
- [ ] Fix awkward space by giving content the space (taller cards, a larger type step, less reserved title height, content moved up to the standard title gap), or by adding a meaningful element. Never pad with decoration.
- [ ] Intentional space is allowed and must look intentional: statement slides, a section opener, a held click-reveal state. Note it in the report so it isn't "fixed" later.
- [ ] Sibling cards don't mix one dense card with one mostly empty card. Rebalance the content, or size each card to its content with aligned rows.

## 5. Assets: logos, images, video
- [ ] No cut-off logos: no straight clipped edges, missing corners, a mark touching its tile edge, or a stroke clipped by a rounded mask. Compare against the official mark.
- [ ] No blurry or low-resolution assets. Source pixel size must be at least the rendered size × device scale. The deck exports at 1.32× its CSS px and the PDFs at about 2448–2880px wide; phones run at 2–3×. Replace anything soft with an official higher-resolution or vector asset.
- [ ] No white boxes, halos, fringes, or double outlines around transparent logos. Logos sit on the background cleanly.
- [ ] Consistent logo height and baseline within a row; equal visual weight.
- [ ] Photos: cropped to the subject (e.g. into the projected screen, not the room), centered in their frame, no distortion. Video poster frames are crisp and the video plays.

## 6. Alignment, spacing, and consistency
- [ ] Shared left edges: titles, kickers, card labels, and body text align to the grid.
- [ ] Equal sibling heights and equal gaps. Dividers and rules line up across sibling cards.
- [ ] Arrows, connector lines, timeline dots, and chart points are exactly on what they connect. A dot is centered on its line; an arrow points at the visual middle of its target (e.g. the letters of a wordmark, not the top of its image box).
- [ ] Charts are drawn to scale, every chart has its axes, points sit on the curve, labels name values the chart reaches, and labels never collide with lines. Illustrations that are not data say so.
- [ ] Nothing overlaps: logos versus big numbers, labels versus curves, text versus images.
- [ ] Borders are on theme: soft hairline borders on paper cards (the deck's `--edge`), never stray thick navy outlines. Colors come from the theme tokens only; highlights use the theme accent unless JJ asked otherwise.

## 7. Text rules (every surface)
- [ ] American spelling only (-ize, -yze, -or, -er, license, traveled, enrollment, program, judgment, gray).
- [ ] The Oxford comma in every list of three or more, including titles, captions, alt text, notes, and sources.
- [ ] Body sentences end with a period; labels, stat captions, and source lines follow the surface's convention consistently.
- [ ] No em dashes. No space between Chinese and "AI". Chinese never says "X年级".
- [ ] No unintended brand mentions (e.g. no "Arena" pitch in the parent-talk deck beyond the allowed logo, speaker titles, and URLs).

## 8. Animation and interaction (decks and interactive pages)
- [ ] Check every animation mid-flight (capture several frames): no jumps, reflow, clipping, or overlap at any frame.
- [ ] The final state is the clean, intended layout. Export/PDF, `?read`, reduced motion, and the phone view all show the final state.
- [ ] Click gates and reveals: arrival state, each click, going back, and rapid clicks all behave. No page errors (listen for `pageerror` while stepping through everything and back).

## 9. Tools (arena-school repo)
- **Deck:**
  - `python3 decks/src/build.py`
  - `python3 decks/src/contain.py --georgia`: must report 0 outside containers and 0 size/empty problems, under web fonts and the Georgia fallback.
  - `python3 decks/src/export.py`: aborts if a slide exceeds 1080px; also writes the PDFs and the /talk gallery.
  - `python3 decks/src/reader_check.py`: the phone reader at 390×844 and 844×390.
  - Revert build outputs before committing unless you are publishing.
- **Website:**
  - `python3 tools/content_lint.py` (content rules).
  - The phone-preview checks (`arena-school-tools/phone-preview`: `checks.py`, `deskdiff.py`).
  - Playwright screenshots at 390, 768, 1280, and 1440px.
- **Measuring:** Playwright `getBoundingClientRect` for boxes, plus pixel scans of 2× screenshots for ink. Record the before and after numbers.

## 10. Report
For each loop, a table with one row per issue:

| Slide/page | Language | Element | Problem (with measurement) | Fix |
|---|---|---|---|---|

After the tables:
- **Not fixed, and why:** intentional space, deck-wide conventions, out of scope.
- **Wording changes:** each one with its reason.
- **Contact sheets:** screenshots of every slide or page after loop 2.
- **Checks:** the commit hash and the result of every check.
