# ACAMIS Tech workshop deck: rules for Claude Code

Read `README.md` in this folder for the files, tools, and the edit → check → export → deploy steps. Work on `main` in this folder only; it is the single copy of the deck.

## Audience and tone

- International school teachers, tech and innovation coaches, and IT staff; mostly US-trained, English-speaking, not technical, and wary of AI. Give unfamiliar names a short label ("Claude Code, an AI tool that builds web apps from plain English").
- It's a peer case study that also markets Arena School: Arena name and logo drops and arenaschool.org links are welcome; a hard sell is not.

## Wording

- **"Learners"** is the deck's word for whoever an Arena program serves: students, teachers, school leaders, or parents. Use it wherever the deck describes Arena's own philosophy, framework, outcomes, or assessment (slides 3 and 6 to 9).
- **"Students"** only when it's literal: the ISB students, research study participants, or the audience's own students.
- The hands-on segment is a **build session** or walkthrough, never a "live build" or "live demo" (we may not have a network).
- American spelling, Oxford comma, no em dashes. No orphans: an English line ends with at least two words (`&nbsp;` before the last word, or `<span class="nw">`).

## Facts

- Never state the ISB cohort size. No student names, student product names, prize amounts, or fees.
- Never call Bodley Academy a "pilot" (it's "Where it started").
- Don't name or quote people or schools from private conversations, on slides, in notes, or on the session page. Ask JJ if unsure.
- Every new statistic is checked at its source and recorded in `research/` first. Keep to one or two numbers per slide.

## Layout (JJ checks to the pixel)

- Every slide fits 1920×1080 in export mode. Fix overflow with spacing or copy, never by shrinking type below the deck's scale.
- Center by ink, not by box: measure with `tools/ink.py` (within about 1.5px). Sibling cards share heights and baselines. No empty bands or awkward gaps.
- CSS px inside `.w` render ×1.32. Deck rules like `.ae .bd p` beat plain selectors: scope as `.ae.<slide-class> .bd …`.
- Same component for the same job; theme colors only (`var(--ink)`, `var(--ink2)`, `var(--paper-hi)`, `var(--edge)`, `var(--muted)`).
- Reveals use `data-s="1"`, `data-s="2"`…; entrance reveals use `.r` with `style="--d:.1s"`.
- After adding or removing a slide, renumber the `<!-- n · … -->` comments and fix the agenda links (`data-go` is the 0-based index of each Part slide).
- For a full pass, use the repo's `format-audit` skill (`/.claude/skills/format-audit`).
