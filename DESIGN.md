# Arena School design system

**This file is the single source of truth for how Arena School looks: the website, decks, one-pagers and infographics, social posts, and documents.**

- **Supersedes** the September 28 version of this file, the design sections of `review/DESIGN-PASS-BRIEF.md`, and the palette and fonts lines in the Drive Logos README.
- **Covers** visuals and layout only. Copy, voice, claims, and the page structure live in `CONTENT-RULES.md`.
- **Keep it current.** Any change to how something looks updates this file in the same commit. Founder decisions are dated (YYYY-MM-DD). When two rules conflict, the later dated decision wins.
- **Tags:** web-only rules are marked **[Web]**, print and presentation rules **[Print]**. Untagged rules apply everywhere.

Last full audit: 2026-10-01. That covers the live site at `7ef560c` (computed in a browser on 19 pages at 1440 and 390px), the deck source in `arena-school-tools/deck-src/`, the one-pager source in `riso-v2/site-preview/_kit/`, and 504 founder messages from Sept 21 to Oct 1.

---

## 1. Principles

1. **Formal, calm, and credible.** The audience is parents, heads of school, and educators. The look should be that of a serious independent school or education brand, never a tech startup. "Too startup-y" (meeting, 09-21); "frame this as a friendly partner, not a tech startup" (09-28).
2. **Designed, not generated.** No "vibe-coded", "Claude-style", or "AI website" look (09-24, 09-27, 09-28, 09-30): no generic rounded-card grids with colored side bars, and no default shadows. References: editorial print, Canva and Dribbble infographics, riso prints.
3. **Restraint.** Emphasize a few words, not whole sentences ("overkill… you're practically highlighting the entire text", 09-28). Use one accent device at a time.
4. **Space before size.** When something feels cramped, add space or widen the container first. Enlarge text only where a layout is clearly empty ("the previous text sizes were fine, I just needed you to space it out more", 09-30; "+2pt where slides have a lot of space", 10-01).
5. **Save vertical space.** Lay things out horizontally first. Keep pages and slides short. Put depth behind hover, tap, or accordions (see CONTENT-RULES §4).
6. **Detail matters.** Columns align, margins are equal, gaps are consistent, and no line ends with an orphan. Founder reviews happen at the pixel level.

---

## 2. Brand and logo

- **Official lockup only.** Use the seal plus the "ARENA SCHOOL" wordmark as one image. **Never** put the seal next to typed text (09-28). This applies to the website, decks, social posts, and documents.
  - Web files: `logos/arena/wordmark-navy-1600.png` on light backgrounds, `wordmark-ivory-1600.png` on dark ones.
  - Seal alone: `seal-navy-*` and `seal-ivory-*` (256/512/1024).
  - Master files: Drive › 04 Marketing, Brand & Media › Logos › 01 Arena School.
- **Lockup with web address: image posters only** (2026-10-01).
  - **What it is:** the seal, "ARENA SCHOOL", and `www.arenaschool.org` underneath in Newsreader 400. The address is left-aligned to the "A", and the two-line block is centered on the crest.
  - **When to use it:** **only** on posters or graphics sent out as images, where nothing can be linked (WeChat or Xiaohongshu posters, printed flyers, co-marketing images).
  - **Everywhere else** (website, decks, documents, email, social posts that carry a link): use the standard lockup above or the seal alone.
  - **Web files:** `logos/arena/wordmark-url-navy-1600.png` (light backgrounds) and `wordmark-url-ivory-1600.png` (dark backgrounds).
  - **Master files:** all 8 colorways at full size, in Drive › Logos › 01 Arena School › `wordmark-url (image posters only)`, named `arena-wordmark-url-<colorway>.png`.
  - **Co-branded posters:** the partner logo goes in one top corner and this lockup in the other, at equal height, with no "×" between them.
- **Seal alone** is fine as a mark or watermark: the hero medallion, the one-pager watermark (large and partly cropped off the page, 09-28), the inner-page header watermark, and the favicon.
- **Favicon:** the navy seal on a **circular** ivory disc, transparent outside the circle (09-24).
- **Over art or photos:** put a beige underlay beneath the navy logo so it stays legible (09-24). The logo must never collide with UI such as buttons or the nav (09-28).
- **Logo files:** any beige inside a logo must be the paper color `#EFE3D4`. The darker sand `#EBCDA4` is retired (09-28).
- **Deriving new PNGs:** the source transparent PNGs carry roughly 1% alpha haze, so clear alpha values of 8 or below first.
- **Light branding in parent-facing decks:** the Arena lockup is the first logo in the logo wall, with no big brand slide (09-30).
- **Partner logos** (for example Lux Scholar): transparent background, navy text only, never white text (09-27). Lux Scholar appears only on the bootcamp pages.

---

## 3. Color

### 3.1 Core tokens (shared by web and print)
| Token | Hex | Role |
|---|---|---|
| `--ink` | `#0B1A4A` | Navy ink: headings, card titles, stat numbers, eyebrow chips, the navy band |
| `--ink-2` | `#2F55A8` | Accent blue: italic key words, labels in print, step numerals, focus rings, small accents |
| `--bg-paper` (beige) | `#EFE3D4` | Main page background (web); alternate slides, tags, and sub-boxes (print) |
| `--paper-hi` (ivory) | `#FCF3ED` | Card surfaces, light bands, the hero paper |
| Header paper | `#F3E9DD` | Inner-page header (web); slide and page background (print). Tinted because pure ivory is "too jarring" (09-28) |
| `--bg-paper-soft` | `#E6D4C1` | Darker alternate band (web `.section-alt`) |
| `--border-paper` | `#D4C0AA` | Default 1px rule and border color |
| `--text-ink` | `#101A2E` | Body text and h2 (web) |
| `--text-ink-soft` | `#3E4660` | Secondary text: ledes, card body, nav links |
| Body text (print) | `#26304F` | Body copy in decks and one-pagers; hero ledes on the web |
| `--text-ink-muted` | `#5B5B6B` | Labels, sources, captions, notes |

### 3.2 Web-only colors [Web]
| Hex | Role |
|---|---|
| `#22458A` (`--riso-blue` / `--accent`), hover `#183366` | **Buttons, `.tlink` links, and the active language pill** |
| `#0E1729` | Footer background (links `#F4ECE0`, text `#A9AEC0`, rules `#26324F`) |
| `#FBF6EF` / `#FFFFFF` | Homepage card surface / FAQ, co-founder card, and form surface (see Open decisions D4) |
| `#A6482A` (`--coral-deep`) | Small uppercase kickers, I/II/III and 01–03 numerals, the FAQ "+" |
| `#E59375` (`--coral`) | Quote left rule, high-school rule and bootcamp bar on the grade map, bullets, selection color |
| `#F2A98E` (`--coral-light`) | Meta text on the navy band |

### 3.3 Print-only colors [Print]
| Value | Role |
|---|---|
| `rgba(255,255,255,.45)` | **Translucent pane**: any text sitting on the dotted background |
| `#FFF9F4` | Card fill when opened or hovered (deck) |
| `#3B4C7E` | One-pager CTA card: a muted navy, after "way too bright… lessen the opacity" (09-28). See D3. |
| `rgba(47,85,168,.13)` | One-pager keyword highlight |
| `#C9D2EC` | Placeholder under video and screenshot frames |
| `rgba(11,26,74,.16)` (`--edge`) | Hairline edge on parent-talk deck cards, rows, and the ivory pair card (10-11) |
| `#2F55A8` / `#B3BFDB` (`--data` / `--data-2`) | Chart bars: the bar that makes the point / context bars (10-11) |
| `rgba(11,26,74,.07)` (`--track`) | The 0–100% track behind share bars (10-11) |
| `rgba(11,26,74,.15)` (`--dots`) | Deck dot grid, lighter than the web grid so charts stay calm (10-11) |
| `#A9BEEA` / `#C9D6F2` | Light blue on navy: kickers, italic key words, big numbers, and agenda subtitles on navy slides (10-11) |

### 3.4 Brand-package colors (logo files and social art)
Navy `#152636`, beige `#EFE3D4`, ivory `#F6F0E5`, bronze `#7E6238` (meander border). These are the colors of the logo artwork itself. The website and print ink is `#0B1A4A` (see D1). Social riso art pairs navy ink and cream paper with **one** coral accent.

### 3.5 Color rules
- One accent device per element. Blue italic **or** a highlight, never bold plus highlight together (09-28).
- Text on navy uses `#FCF3ED`, with secondary text at 70–86% opacity.
- Credential logos are single-color navy on the page (see §6.9).
- Photo tone: warm, slightly more contrast, never washed out or green-cast. Match skin tones across headshots (09-27, 09-28).

---

## 4. Typography

### 4.1 Families
| Use | Font |
|---|---|
| Display / headings, all media | **Newsreader** (self-hosted; roman 200–600, italic 200–500). Never request weight 700: it renders as 600. |
| Body [Web] | **Geist** 300–700 |
| Body [Print] | **Newsreader**. Decks and one-pagers use **one serif stack only**: `'Newsreader','Songti SC','Noto Serif SC','Source Han Serif SC',Georgia,serif` (09-30) |
| Chinese display [Web] | `'Arena Serif SC'`: a self-hosted subset of 思源宋体 (Source Han Serif) in `fonts/zh/`, with Noto Serif SC slices as fallback. Rebuild the subset when Chinese copy changes. |
| Chinese body [Web] | `'Arena Sans SC Punct'` (full-width punctuation) → Geist → PingFang SC / Hiragino / Noto Sans SC |
| Chinese [Print] | Songti SC / Noto Serif SC through the serif stack |
| **Monospace / typewriter** | **Banned in all print, decks, and social posts** (09-30). On the web it survives only on `.eyebrow` chips, through `--font-typewriter`; see D2. |
| Handwriting fonts | Banned |

Fonts are always self-hosted. Google Fonts and other CDNs are blocked in mainland China.

### 4.2 Web type scale [Web] (computed, 1440 → 390)
| Style | Spec |
|---|---|
| Homepage h1 | Newsreader 500, 50 → 34px, line-height 1.04 (Chinese 1.16), tracking −0.028em, `--ink`. The key word is italic `#2F55A8` with the riso marker (§6.4). |
| Inner h1 | 500, 63 → 40px, line-height 1.04, tracking −0.028em; `em` italic `#2F55A8` with the marker |
| h2 | Newsreader **300**, 46 → 28px, line-height 1.04, tracking −0.026em, `#101A2E`; `em` italic in the same color |
| h3 / card title | Newsreader 400–500, 19–22px, line-height 1.2–1.25, `--ink` |
| Lede | Geist 400, 16.5–20px, line-height 1.5, `#3E4660` (hero `#26304F`), max about 64ch |
| Body | Geist 17px / 1.6; card body 14.5–15.5px / 1.5–1.6 |
| Kicker / label | Geist 500, 10.5px (11–11.5px minimum on mobile), uppercase, 0.12–0.16em tracking, muted or `#A6482A` |
| Eyebrow chip | 600, 11px, 0.16em tracking, uppercase, `#FCF3ED` on `#0B1A4A` (§6.3) |
| Stat number | Newsreader 400, 34–44px (28px mobile), line-height 1, `--ink`; suffix at 0.5em, muted |
| Button | Geist 500, 15px (nav 14px) |
| Nav link | Geist 400, 14.5px, `#3E4660` |
| Quote | Newsreader italic 400, 24px / 1.42, `--ink`, 2px coral left rule (Chinese: upright sans 19px / 1.75) |

### 4.3 Deck type scale [Print] (CSS px at 1920; everything renders ×1.32 via `--z`)
| Role | Spec |
|---|---|
| h1 | 88 / 1.05 / 500 / −0.025em, balanced wrap; second line 0.5em, weight 400 |
| h2 | 58 (dense slides 48) / 1.05 / 500 / −0.025em |
| Stat number | 74 (small 54) / 1 / 400, `--ink-2`, tabular figures |
| Quote | 34 / 1.3 / 400 |
| Card h3 | 27 / 1.2 / 500 (30 on roomy slides) |
| Lede / takeaway | 22 / 1.6 (roomy 25) |
| Card body | 15.5 / 1.6; opened detail 15 / 1.55 |
| Source | italic 13 / 1.45, muted |
| Labels | **uppercase serif**, 600, 11.5–12.5px, 0.14–0.15em tracking. Never mono. |

**Parent-talk deck (`.ae` slides, 10-11):** kicker 16 caps / 600 / 0.14em, `--ink-2` (Chinese 18); action title 50 / 1.12 (Chinese 46 / 1.3); statement-slide title 72 / 1.08 (Chinese 62 / 1.32; the closing line 62, Chinese 56); statement subline 30 / 1.45; card heading 32; body 26; labels and sources 15; big numbers 128–168 at **weight 300**, `--ink-2` (light blue on navy). Chinese emphasis is color only, never a slanted fake italic.

### 4.4 One-pager type scale [Print] (pt, English / Chinese)
| Role | English | Chinese |
|---|---|---|
| Body | 8.6 / 1.42 | 9.6 / 1.55 |
| h1 | 19 / 1.08 / 500 / −0.02em | 21 |
| Section label | 9pt, 600, caps, 0.14em, `--ink-2`, dotted underline | 10.4pt / 900 / 0.06em |
| Program name | 10pt / 500 | Songti 900, 10.8pt |
| Tag | 6.4pt / 600 / caps / 0.05em | 7.4pt / 900 |
| Card title | 10.4pt | Songti 700 |
| Card / case label | 6.4–6.6pt / 600 / caps / 0.14em | 7.4pt / 0.04em |

Chinese body runs about 1.12× the English size, labels about 1.16×. Chinese tracking is about a third of the English value.

### 4.5 Emphasis
- **Italic accent words:** `em` in italic `--ink-2` inside headings. Keep italic words short.
- **Spacing after italics:** a space follows an italic word unless punctuation follows. Never leave a highlighted trailing space with no word after it (09-28).
- **Riso marker highlight** (the founder's favorite device, 09-28): a halftone dotted band behind a key word, using `art/riso-hl.png`.
  - Web: `.rh` on the homepage, and `.hw-m` on inner headers, which sweeps in and repeats every 7s or on hover.
  - Print: static, 5–6px.
  - Use it on **single key words** only (agency, taste, craft, the hero verb). It replaces icons (09-28).
- **Bold plus highlight together is banned.** Highlight a few phrases at most (09-28).
- **Typography details:** curly quotes and apostrophes (’ “ ”) in all English. Real arrows (→), never `->` (09-28). Lining numerals; tabular figures for stats.
- **Capitalization:** program names in Title Case. "Community Dialogues" is capitalized in the menu and footer (10-01). College majors are capitalized (09-27).

### 4.6 Chinese and bilingual typography
- **No fake italics in Chinese.** `em` and italic headings render upright in Chinese; carry emphasis with color or the marker.
- **Tracking:** Chinese labels and eyebrows use `letter-spacing: .04em` (web) or .04–.1em (print). Chinese headings use 0 tracking and line-height 1.15–1.16.
- **Weights:** Chinese needs its own type scale, never the English one scaled down. Tags and subheadings are larger, and first-column program names are bold Songti (09-28). Adjusting Chinese must not change the English (09-28).
- **No orphans.** The last line never holds 1–2 Chinese characters. Deck: `guard.js` binds the last 3 characters plus punctuation. Web and one-pager: `.nw` nowrap spans.
- **Wrapping:** use `line-break: strict` and balanced headings. A Chinese line never starts with punctuation.
- **Copy conventions** that affect layout (see CONTENT-RULES §10):
  - 初中生 / 高中生 / 初高中学生, never "X年级", except on a grade axis.
  - No space between Chinese and "AI" or digits.
  - Full-width punctuation.
- **Bilingual deck [Print]:**
  - English dominant. Chinese sits under each English element as a block at 0.83em, 60% opacity, weight 400, no caps, no italic (09-30).
  - Short labels and chips carry the Chinese inline at 0.95em.
  - The same bullet holds both languages, separated by a line break (09-30).
  - Open question: see D6.
- **Names in Chinese materials:** 羊筱涵 (Jing Jing Yang) is listed first, then 安广宁 (Phillip An). "ISB ’19" in English, "ISB 2019 届" in Chinese.

---

## 5. Layout, spacing, and alignment

### 5.1 Grid
- **Web:**
  - Container max 1240px, padding `clamp(24px,4vw,80px)`.
  - Section padding `clamp(56px,6.5vw,92px)` (homepage sections 72–132px; mobile 48–80px).
  - Grids are 3-up or 4-up with 12–18px gaps (16px typical).
  - Main breakpoints: 1080 (hamburger menu), 900 (stacking), 760 (phone), 560 (phone header and footer).
- **Deck:**
  - 1920×1080 at `--z:1.32`; 75px side margins.
  - Top and bottom margins `clamp(26px,5.5vh,64px)`.
  - Columns `.g2/.g3/.g5` with gap `clamp(18px,2vw,28px)`.
  - Think of every slide as a well-spaced section of a website, not a dense document (09-30).
- **One-pager:**
  - A4, 210×297mm, with 12mm side margins.
  - **Equal top and bottom margins** (8.75mm; logo-to-top equals CTA-to-bottom, 09-28).
  - The fixed mm spacing set is 0.8, 1.6, 2.6, 3, 3.4, 4, 7mm, with consistent gaps between sections.

### 5.2 Alignment
- **Desktop web:** left-aligned. Centered only for the team head, the proof band, and the credentials head.
- **Phones:** headings, ledes, and CTAs are centered wherever that reads better (09-30). See D5 for the per-page drift.
- **Hero:** the mark and the copy are vertically centered against each other (09-24).
- **Tables and multi-column rows:** the **first lines of text align optically across columns**, so measure the rendered ink, not the boxes (09-28). The one-pager uses per-column `padding-top` offsets: English +2.9 / +1.8 / +0.65px, Chinese +2.55 / +1.2 / +1.35px.
- **Equal heights:** cards in a row share a height, and tags and links pin to the bottom with `margin-top:auto`.

### 5.3 Line breaks
- **Five-word rule:** a subtitle or lede whose last line has fewer than 5 words, where there is room, gets a wider box first (09-27).
- **No early paragraph breaks** in body text (09-28). No `<br>` that only works at desktop width.
- **No broken phrases:** headings never split a phrase such as a program name or "从容走进AI时代". English never hyphen-splits a word.
- **Widen before wrapping:** if a card's content almost fits on one line, widen the card ("make this card wider so that everything falls under one line", 10-01).

### 5.4 Breathing room
- Never let text touch a card edge ("hitting the border", 09-27). Pills need visible inner padding ("a tiny bit cramped", 09-28).
- Hints and captions keep clear space from the graphic they describe (09-28).
- Avoid oversized cards with too much negative space (09-28) as well as cramped ones.

---

## 6. Components

### 6.1 Cards
| Card | Spec |
|---|---|
| **Web inner-page card** (`.pg` / `.pc`) | `#FCF3ED`, 1px border (`#D4C0AA` or `rgba(11,26,74,.16)`), **radius 12**, padding about 26px, no shadow. Hover: the border darkens (`.pc` → `#2F55A8`), with **no lift**. |
| **Web homepage card** (program, pillar, co-founder) | `#FBF6EF` (co-founder white), 1px `#D4C0AA`, **radius 16**. Hover: −2 to −3px lift plus a soft shadow (§7.2). |
| **Deck card** [Print] | `#FCF3ED`, **1px navy border**, radius 12, padding `clamp(22..30px)`, no shadow. Open or hover: `#2F55A8` border and `#FFF9F4` fill. The parent-talk deck has no open/hover cards, so its cards use the hairline `--edge` instead of navy (10-11). |
| **Expandable card** [Print] (`.rv`) | A "+" (24px, `--ink-2`) top-right rotates 45° when open. Detail opens with a 0fr→1fr grid animation after a 28×3px dot rule. Closed cards in a row share a height. Opening pushes following content down (it slides), never covers it (10-01). |
| **One-pager card** [Print] | `#FCF3ED`, radius 6, **no border**, no shadow, padding 2.6×3.2mm (borders removed to save space, 09-28) |
| **Sub-card** | Must look subordinate: smaller, lighter fill (`#EFE3D4`), and visually inside its parent (09-28) |

### 6.2 Translucent pane (text on a patterned background)
Any non-heading text sitting on the dotted background goes inside a pane (09-30): `rgba(255,255,255,.45)`, **no border, no side bar**, radius 12, padding about 28×40px.
- Uses: ledes, takeaways, agenda, quote band, QR blocks, captions, sources, and any "floating sentence that has no home" (09-30).
- Headings stay on the paper.
- Hover popovers [Print] use `rgba(252,243,237,.95)` with 6px blur and a 2px `--ink-2` top rule.

### 6.3 Pills, chips, tags, and labels
- **Text inside every pill, chip, and tag must be optically centered vertically** (10-01).
  - Uppercase text sits high in its line box, so use slightly heavier top padding, or `display:inline-flex; align-items:center; line-height:1`.
  - Check at 2× zoom in both languages before shipping.
- **Eyebrow chip** [Web]:
  - Navy fill, `#FCF3ED` text, 600, 11px, uppercase, 0.16em tracking.
  - Padding `.5em .85em .45em`, radius 2px, **no shadow**.
  - Always `inline-flex`, with a 6px `--ink-2` dot ringed in 1.5px paper. It inverts on dark bands.
- **Eyebrow chip** [Print, deck]:
  - Same look, padding `.66em .95em .6em`, **serif** caps.
  - It currently has a 2px offset `--ink-2` shadow (see D2).
- **One-pager section label** [Print]: no chip. `--ink-2` caps with a dotted underline, made larger and bolder on 09-28.
- **Tags:**
  - Web `.pc-tag`: 1px `#D4C0AA` border, radius 4, padding 3/7, 10px caps.
  - Print: `#EFE3D4` fill, radius 3, padding 1px 4px, no border.
  - **Tag order:** duration first, then level, then format, plus "One-on-one" where it applies (09-28).
  - Allowed set: middle school, high school, college, early career, in-person, hybrid, 1–2 days, 5 days, 1–2 weeks.
- **Pill buttons** (language switch, "See it live"):
  - Radius 999px, with padding so the text has clear room.
  - The language toggle is visually separate from the nav links (09-24).
  - The Contact us pill matches the toggle's scale and is never oversized (09-28).
- **Promises or disclaimers** ("we reply within 3 days", etc.): small fine print, **not** shaded pills (09-28).

### 6.4 Keyword highlight
See §4.5. This is the sanctioned way to make agency, taste, and craft stand out, in place of icons, bold, or boxes. "Highlight agency, taste, and craft more" (10-01) means a marker highlight on those words plus an italic `--ink-2` name, not extra cards.

### 6.5 Buttons and links [Web]
- **`.btn`:** inline-flex, padding 14×22px, 54px tall, radius 999px. The "→" nudges 3–4px on hover.
  - **Primary:** `#22458A` fill, `#F7F1E7` text, hover `#183366`.
  - **Ghost:** transparent with a 1px `rgba(16,26,46,.22)` border.
  - **On navy:** primary inverts to paper fill with ink text.
  - **Nav CTA:** 44px tall, 14px text.
  - **Mobile:** full width, 52px tall.
- **`.tlink`:** `#22458A`, weight 500, ending in a "→" glyph; a 1px underline draws in on hover.
- **Print CTA:** a white pill button (radius 999, padding 3×5mm, navy 9pt) on the CTA card.

### 6.6 Stats and numbers
Stats are a plain row with thin 1px rules, **never boxed**. Numbers: Newsreader 400, `--ink` (web) or `--ink-2` (print). Logos can stand in for numbers (judges' institutions).
- **Deck big numbers** (parent talk, 10-11): weight 300, 128–168px, one per slide; an earlier value beside it is muted `#5B5B6B`, and the change is drawn as an arrow with the time span under it ("Six months").
- **Deck charts:** horizontal bars only. Shares sit on a 0–100% track and counts on a zero baseline with no track, so bar length is the value itself. Every bar is labeled with its exact value. Only the bar that makes the title's point uses `--data`; the rest use `--data-2`. A reference line (such as "Half of jobs") is one 1.5px navy tick across the bars, labeled once.

### 6.7 Sequences: steps, timelines, and grade map
- **Horizontal tracks**, never vertical lists (09-27). One schedule per program.
- **Deck step track:**
  - Four columns with a 2px `--line` rail, filled in `--ink-2` up to the active step.
  - 56px circular dots with a 1.5px navy border.
  - Step titles on panes; one shared note panel follows the active step.
- **Web step selector (`.pc-sel`):** a photo stage plus a tab list with a 2px progress bar; auto-advances every 6.5s.
- **Grade map:** 8 columns; 2px stage rules (middle school blue at 0.4 opacity, high school coral at 0.6); 46px pill bars in a navy gradient. Numbers appear only on this axis.
- **Precision:** the dots and the line align exactly, with no jitter and no gratuitous motion (09-27).

### 6.8 Quotes and callouts
- **Web quote:** Newsreader italic with a 2px coral left rule.
- **Print quote band:** a pane laid out as `max-content | 1fr`, source right-aligned in italic 13px muted.
- **Callouts never use a colored border plus a side bar** ("very AI-coded", 09-30). Use a pane or plain text.

### 6.9 Logo walls (credentials and institutions)
- **Transparent single-color navy marks. Never in cards, tiles, or on white** (09-24, 09-27).
- **Equal visual weight:**
  - Size each logo by eye to the same optical weight, using a per-logo `height` rather than a formula (09-24, 09-27).
  - Web reference heights at 1440: ISB 46, Tsinghua 44, Harvard 40, Brown 40, Apple 38, YC 38, Goldman 36, Caltech 30, Microsoft 30, Kimi 24, McKinsey 22, Deloitte 22px.
- **Even spacing:**
  - The gaps look even (09-28), and the row fills its container.
  - Web: grayscale at 0.82 opacity, color on hover.
  - Print: 0.85–0.9 opacity.
- **Order:** education then work, as separate rows on the web (09-24) and in bios, schools first (09-27). On the deck, one single row that starts with the Arena lockup (09-30).
- **Correct marks:**
  - Kimi is the official **wordmark only**, with no "K" glyph (09-28). Not Moonshot AI as the main mark.
  - Tsinghua uses the official lockup file.
  - Harvard and Tsinghua match Brown's crest-plus-name style.
  - CICC uses its official mark.

### 6.10 Photos, screenshots, and video
- **Photos:**
  - Content only (galleries, portraits, step stages), **never section backgrounds** (09-27).
  - Real program photos over illustrations.
  - High quality and dynamic (teamwork, presentations), not repetitive, never blurry (09-28).
  - Radius 8–14 depending on context; mostly 4:3.
  - Don't crop faces or cut images off badly (09-28); shorten text to make room instead.
- **Headshots:** heads the same size and centered across people; warm, with balanced contrast (09-27).
- **Screenshots and product UI:**
  - **No border.** The corner radius must match the real device or window curvature (09-30).
  - Must be sharp: rebuild them at 2× rather than upscaling (10-01).
  - Prefer short looping videos of the tool working (09-30).
  - Frames are 16:10 with a placeholder underneath; the poster image replaces the video in PDFs.

### 6.11 Forms [Web]
- Inputs: radius 6–8, 44–48px tall, font 16px or larger on mobile (prevents iOS zoom).
- Focus: `#2F55A8` border plus a 3px `rgba(47,85,168,.12)` ring.
- Labels are always visible.
- Never rename `name=` attributes.

### 6.12 CTA card [Print]
- One per one-pager, at the bottom: a muted navy (`#3B4C7E`) card, radius 8.
- Headline "Bring Arena to your school", one supporting line, and a white pill button.
- A links row (website left, email center, LinkedIn right) under a 1px `rgba(255,255,255,.3)` rule (09-28).

### 6.13 QR block [Print]
QR on a `#FCF3ED` square with 10px padding, inside a pane. Caps caption, with the URL in italic below on a single unbroken line.

### 6.14 Icons
**No decorative icons.** The line-drawing curriculum icons were retired ("really low quality… we don't need icons", 09-28). Allowed: functional glyphs (→, +, chevrons, the LinkedIn and email icons on founder links), the small 22px label icons on deck comparison cards, and an 18px line person glyph before a role label ("Doctor", "Lawyer") in deck workflows, where it separates the person's step from AI's (10-11).

### 6.15 Parent-talk deck layouts [Print] (10-11)
Modeled on Phillip's showcase-wrap deck (portal.arenaschool.org/decks/showcase-wrap.html). Each layout does one job; reuse it rather than inventing a new one.
- **Kicker:** one uppercase serif line above every title. It is concrete context or a mini-takeaway ("149 US employers, spring 2026", "Other companies retrain first"), never a topic label. It replaces the section tracker.
- **Statement slide (`.st.nv`):** navy `#0B1A4A`, no dots, the ivory seal at 5% cropped bottom right. Kicker, one large title with one light-blue italic phrase, and at most one subline or one big number. Used to open each part, for the question that frames the talk, the quote, and the close. Text sits directly on navy: the pane rule (§6.2) is for patterned backgrounds.
- **Rows (`.rows`):** one ivory row per example. Logo plus field label, AI's step, an arrow, the person's step, and a navy date pill on the right.
- **Flow:** before and after for one workplace. The old step on a pane, a dashed divider, AI's draft in a dashed-blue box, an arrow, and the person's check on ivory.
- **Chain:** three steps in order with arrows, each labeled with when it happens ("First", "Then", "Only if needed").
- **Arc:** two big numbers with the time between them, each with its own 0–100% bar.
- **Pair:** the same tool used two ways. An ivory card and a navy card, each with a pill label, a quoted request in large italic, and one line on what happens.
- **Growth columns (10-13):** a value over time is a column chart on one navy baseline. Bar height is the value; a year with no value is a ring on the axis. The value sits above its bar, the date, name, and one line below the axis. Only the title's bar uses `--data` (Cursor, slide 30).
- **Grouped row (10-13):** when some items in a set are ours and some come from a source, they share one row and a labeled rule groups them above; the sourced group uses dashed card edges and a muted label (five skills, slide 18).
- **Case strip (10-13 round 2):** a first-hand story as situation → what was built → what happened: two ivory cards and a navy outcome card joined by arrows, each with a caps label, a 32px heading, and one line under a hairline; one italic line below carries the point (Kimi, slide 27).
- **Proof row (10-13 round 2):** one real team as problem → build → result, three photo cards with the program day under each label and the pillar it practiced at the foot. Program photos only from the program named on the slide: on ISB slides use `photos/isb-2026/` and `photos/isb-hq/` only; `photos/mix/pilot-*` and `decks/img/conversation/hands-stage*` are Hong Kong 2025 (slide 32).
- **Speakers (10-13 round 2):** two ivory cards on a shared subgrid so the portrait, the one-line role, and the logo rows align across both people; 118px portraits with a paper ring, 38px names, logos sized by eye with no per-row labels beyond Studied and Worked (slide 3).
- **Close (10-13 round 2):** navy, three numbered takeaways (120px light-blue numerals, 36px heading, one sourced line each) divided by hairlines, then the line to remember under a rule (slide 33).
- **Photo cards (10-13):** project photos run edge to edge across the card top; the project name leads, and the skill it shows sits under a hairline at the card foot, aligned across the row.

---

## 7. Borders and shadows

### 7.1 When to use a border
| Use a border | Never use a border |
|---|---|
| Web cards: 1px `#D4C0AA` or `rgba(11,26,74,.16)` | Screenshots, product windows, and video frames |
| Deck cards and comparison cards: 1px navy | Panes and any translucent element |
| Inputs, the language toggle, ghost buttons | One-pager cards and panels (removed to save space, 09-28) |
| Table row dividers and stat dividers: 1px `#D4C0AA` | Photo galleries and strips ("hate this border", 09-28) |
| Section seams: 1px top rule | Headshots (no colored rings; a plain white ring at most) |
| | Logos (no tiles or cards around them) |
| | Callouts (no border plus colored side bar) |

- **Border width** is 1px. 2px only for step rails, grade-map stage rules, and progress bars. Navy borders are for interactive or highlighted states.
- **Radius scale:**

  | Radius | Use |
  |---|---|
  | 2 | Eyebrow chip |
  | 3–4 | Tags |
  | 6 | Inputs; one-pager cards |
  | 8 | Photos; CTA card |
  | 12 | Web inner cards; deck cards and panes |
  | 16 | Web homepage cards, FAQ, dropdown |
  | 999 | Pills and buttons |

### 7.2 Shadows
- **No solid offset ("misregistration") shadows anywhere** on cards, buttons, eyebrows, or pins (09-28 formal tone; deck card offsets removed 09-30). The one remaining exception, the deck eyebrow chip, is open decision D2.
- **Allowed soft shadows [Web]:**

  | Use | Shadow |
  |---|---|
  | Card hover | `0 18px 40px -22px rgba(11,26,74,.38)` |
  | Homepage cards | `0 22px 44px -28px rgba(11,26,74,.45)` |
  | Forms | `0 30px 60px -40px rgba(11,26,74,.35)` |
  | Dropdown | `0 24px 50px -20px …` |
  | Scrolled nav | `0 8px 24px -18px …` |

- **Small elements** (chips, tags, pills) get no shadow.
- **Print has zero drop shadows.** Use rings only (photo ring, focus ring).

---

## 8. Backgrounds and texture

- **Riso dot grid, the shared texture:**

  | Medium | Dots |
  |---|---|
  | Web | `radial-gradient(rgba(11,26,74,.22–.28) 1.1px, transparent 1.4px)` on a 24px grid |
  | Deck | the same at 0.15 opacity (`--dots`, 10-11) |
  | One-pager | 0.16 opacity, 0.9px dots, 14px grid |

  Plus the seal watermark: about 7–8.5% opacity, large, partly cropped.
- **Inner-page header [Web]** (chosen 09-28, the "social kit", option A):
  - `#F3E9DD` with the dot grid and a seal watermark at 8.5% opacity, top right.
  - The headline marker sweeps on the italic words.
  - Navy nav. 1px `#D4C0AA` bottom rule.
- **Homepage hero [Web]:**
  - `#FCF3ED` with a live riso-dot field that blends into the header with no hard line (09-30).
  - Current direction: slow, gentle flowing dots with **no cursor reaction** (09-30, supersedes the 09-27 cursor ombré). The code still reacts to the cursor; see Known drift.
- **Behind anything the reader must parse** (timelines, steps, stats, forms, tables): plain paper, no dots (09-27).
- **Dots stay on the halftone grid.** Never random speckle or splatter ("looks like Pollock", 09-27). No speckle on darker beige.
- **Deck slides alternate** between dotted `#F3E9DD` and plain `#EFE3D4`. In the parent talk, navy statement slides (§6.15) sit between the parts and carry no dots (10-11).
- **Phone reader and `/talk` chooser: no dots anywhere** (2026-10-13, Phillip on iPhone: "a lot of the background has dots"). Slides are flat `#F3E9DD` / `#EFE3D4` / navy, the chooser and resources header are flat paper with the seal watermark only, and charts use solid tints, never hatching. The desktop deck keeps its dot grid.
- **Midjourney riso art** (Drive › 04 › social-media-resources) is used **as still images only**: social covers and occasional illustrations. Never animated, never as a moving website background (09-27).

---

## 9. Motion

- **Purpose only, subtle, and always respect `prefers-reduced-motion`** (every animation has a static fallback).
- **Web:**
  - Scroll reveal: fade from 24px below over 560ms `cubic-bezier(.2,0,0,1)`, 80ms stagger.
  - Hover lift: −2 to −3px on homepage cards only.
  - Buttons: 0.2s transitions.
- **Headline marker:** sweeps 0.55s per word and repeats every 7s or on hover (09-28).
- **Homepage rotating audience word:** about 2s per word, "slightly faster but still readable" (09-30). On mobile this is the only animation that matters.
- **Hero dots:** gentle flow, no fast or drastic movement, no cursor effect (09-30).
- **Deck:**
  - Cards open in place and push following content down with a 300ms ease (10-01).
  - Count-up stats on screen only.
  - **Step builds** (parent talk, 10-11): when a slide is reached with the arrow keys it opens on its title, and each press reveals the next part (`data-s`), fading up 10px over about 0.5s while bars grow from zero. Back hides them again. Slides reached any other way (scroll, dots, agenda, phone, `?read`, export, and PDF) always show in full, and reduced motion keeps the steps but drops the movement.
  - Use transitions or interactivity to lighten text-heavy slides (09-30).
  - **One build per card (10-13):** a step (`data-s`) always sits on the element that fades, never on a `display:contents` wrapper, which cannot animate. Then/now builds old card → arrow draws → new card slides across; growth columns rise from the axis, then the value lands; how → what lists the old work, turns the arrow, then slides the new work across.
  - **Market map (10-13, revised 10-13 round 2):** the six known agents sit in one row; below them a field of 200 named tools (listed in `shared.js`) lights up one by one in a scattered order on an accelerating curve, each name flashing `--ink-2` then settling to 50%, while a counter runs from 0 to 200; the sourced Hugging Face figure lands last and counts up. About 4s; a tap finishes it at once. Only sourced numbers appear, with the source on the slide.
- **Banned:** morphing or "AI reshaping" art, animated Midjourney images, jittery timelines, spinning or bouncing decorative elements. The inner-header seal turns once every 4 minutes, which is the only allowed rotation (see D7).

---

## 10. Medium-specific rules

### 10.1 Website [Web]
- **Load order** (later rules win):
  1. `styles.css`
  2. `riso-theme.css`
  3. (Chinese only) `fonts/zh/zh.css`, then `zh-fallback.css`
  4. `mobile.css`
  5. `css/*.css` (page families: `index.css`, `pages.css` for About, Approach, Results, Schools, Contact, Partnerships, Enroll, Mentorship, and Bootcamp; `program-pages.css` for `programs/*`)
  6. each page's `<style data-mobile>` block
- **Edit rules:** edit English and Chinese together. Bump `?v=` cache-busting on any changed CSS, JS, or asset.
- **Phones (760px and below):** no sideways scroll, body text 15px or larger, tap targets 44px or larger, solid nav when scrolled, centered headings and CTAs, menus with no awkward breaks (09-30, 10-01).

### 10.2 Decks [Print]
- **Source:** `decks/src/` in this repo (`body-en.html`, `body-cn.html`, `shared.css`, `shared.js`) → `build.py` → `decks/conversation{,-cn}.html` → `export.py` → `talk/*.pdf` + the /talk gallery. Workflow in `decks/src/README.md`. The bilingual deck is retired.
- **Size checks:**
  - 16:9 at 1920×1080.
  - Every slide must fit 1080px in export mode; `pdf.py` aborts otherwise.
  - Check at both 1920×1080 and 1440×900, with every card opened.
- **Type:** serif only (§4.1). The parent-talk deck is lightly branded.
- **Wording:** no first or third person on slides (09-30). Contact info is neutral ("Contact information"). Exception (10-11, Phillip): the parent-talk speakers slide may say why the speakers are credible in the first person ("We use AI at work…"), within CONTENT-RULES (no builder or startup vocabulary).
- **Appendix:** appendix slides (such as Sources) come after the contact/Q&A slide.
- **Every screen shows the real slide (10-11, Phillip):** the deck never reflows. In a top-level window it runs as a player: the 1920×1080 slide loads in a frame (`?stage`), is scaled uniformly to fit, and is letterboxed in navy, on phones exactly as on desktop. Swipe or tap advances on touch screens. Export and the /talk thumbnails load `?stage` directly.
- **Phone reader (2026-10-13, Phillip):** the QR target `/talk` opens on phones with a one-tap English / 中文 chooser, then a phone-first reader at `/talk/en` and `/talk/cn`, built from the same slide source (`decks/src/reader/`). The deck itself still never reflows; the reader is a separate view. It keeps the deck's tokens, navy statement slides, and one-accent rule, uses Newsreader for titles and numbers with Geist (Chinese: PingFang) for small text at phone sizes, stacks rows into one column, turns timelines vertical, and keeps charts as horizontal bars. Controls sit in the thumb zone (52px buttons at the bottom, safe areas respected). Each slide builds once on arrival; reduced motion shows it built. Polish pass (2026-10-13): flat backgrounds (§8); on content slides the title stays at the top and the chart or cards sit just above the centre of the free height, with the source line pinned to the bottom; a slide that scrolls fades into the bottom bar behind the "more" arrow; the bottom counter's part name wraps to two lines rather than being cut off; logos on navy cards sit on an ivory chip; in landscape the top and bottom bars line up with the 760px slide column.
- **Speaker notes:** each slide may carry an `<aside class="notes">`. Hidden on screen and in the PDF; shown in a bar along the bottom with `?notes`.
- **PDF size:** each exported PDF stays under 6 MB (`export.py` steps JPEG quality down until it fits).
- **Pacing (parent talk, 10-11):** one main point per slide, and a single big number or quote gets its own slide. This is a judgment call, not a rule: keep evidence and comparisons on screen when parents should read or photograph them.
- **Text with no home:** every floating sentence goes into a pane or card (09-30), except on navy statement slides, which have no pattern behind the text (§6.15).
- **Agenda:** the title-slide agenda is a solid navy pane with ivory text; its links jump to each part's statement slide.
- **Licensed photos:** a stock photo is allowed only when no program photo fits the slide. The credit goes on the slide's source line and in the appendix (photographer, site, and photo link).

### 10.3 One-pagers and infographics [Print]
- **Source:** `riso-v2/site-preview/_kit/onepager.html` / `onepager-cn.html` (canonical).
- **Export:** Playwright `pdf(format='A4', print_background=True, margin=0)`, plus a 2× PNG and a 520×735 JPG for the site. Must be **exactly one page**: `.page` scrollHeight equals clientHeight.
- **Default recipe for a new one-pager or infographic** (unless the brief says otherwise):
  1. **Paper:** `#F3E9DD` with the 14px dot grid at 0.16 opacity, plus the large cropped seal watermark at about 7% opacity.
  2. **Header:** the official lockup top-left, then h1 in Newsreader 500 with one italic `--ink-2` accent phrase carrying the marker.
  3. **Sections:** labeled with `--ink-2` caps plus a dotted underline. No chips.
  4. **Content blocks:** borderless `#FCF3ED` cards, radius 6, with consistent mm gaps. Tables use 1px `#D4C0AA` row dividers only, with optical top-alignment across columns.
  5. **Tags:** `#EFE3D4`, radius 3, ordered duration → level → format.
  6. **Credentials row:** navy logos sized by optical weight with even gaps.
  7. **Footer:** the muted-navy CTA card with website, email, and LinkedIn.
  8. **Chinese twin:** its own type scale (§4.4), with no orphan lines.
  9. **Checks:** equal top and bottom margins; serif only; curly quotes; links live (program names link to arenaschool.org pages).

### 10.4 Social (Xiaohongshu and similar) [Print]
- **Format:** 3:4 (1080×1440). Fully simplified Chinese; agency, taste, and craft also carry the English terms.
- **Cover:** a riso print from `social-media-resources`, cropped so the top, bottom, and side borders are equally thick (09-28).
- **Logo and label:** the logo lockup and the category label sit directly on the art, with **no box or white background** (09-28).
- **Type:** titles in a thicker serif; professional but aesthetic, "not basic". The marker highlight on key characters.
- **Pills:** normal pill tags, no dashes.
- **Windows and screenshots:** no border.

### 10.5 Documents (Google Docs and email)
- **Arena doc house style:**
  - Arial; body `#1F2937` 11pt.
  - Heading2 in rust `#C2410C`.
  - Orange summary callout; tables with a `#1F2937` header row.
  - Full spec in memory and `drive/04…/_source marketing plan/build.py`.
- **Gmail:** the founder's compose font, real bullets, real attachments.

---

## 11. Rejected directions (do not reintroduce)
- Logos in cards or tiles, on white backgrounds, or with white partner text.
- The Kimi "K" glyph; Moonshot AI as the main Kimi mark.
- Animated or morphing Midjourney art.
- Procedural knot, tube, ribbon, fabric, or blob art.
- Pollock-style random speckle; speckle on darker beige.
- Inverted heavy-navy inner headers (09-28). The `hero-inv` markup remains only as a no-JavaScript fallback.
- Photos as section backgrounds.
- Shaded promise pills; an oversized Contact us pill.
- Bold plus highlight together; over-highlighting.
- Solid offset shadows on cards; bordered callouts with a blue side bar.
- Borders on screenshots, galleries, or headshots.
- Mixed fonts, monospace, or typewriter fonts in decks and print; handwriting fonts.
- Making text bigger instead of fixing spacing.
- "Claude-style" generic cards and buttons; boxes behind social cover logos.
- Low-quality decorative icons; jittery timeline motion.

---

## 12. Open decisions (need founder sign-off)

| # | Conflict | Current state | Recommendation |
|---|---|---|---|
| D1 | **Navy.** Ink `#0B1A4A` (web and print), brand-package navy `#152636` (logo files), credential-logo navy `#1B2540`, footer `#0E1729` | Four navies; never chosen deliberately | Keep `#0B1A4A` as the one UI ink. Recolor credential logos to `#0B1A4A`. Keep `#152636` only inside the logo artwork. Keep the footer as is. |
| D2 | **Monospace eyebrow chips on the web** (Geist Mono via `--font-typewriter`), while print bans mono. The deck chip also keeps a 2px offset shadow that §7.2 bans. | Phillip planned to drop the typewriter font (09-30); only eyebrows still use it | Switch web eyebrows to uppercase serif or Geist caps to match print; remove the deck chip's offset shadow |
| D3 | **CTA card color** `#3B4C7E` exists only on the one-pager | One-off color | Keep it as the official "muted navy" print token, or change it to `--ink` at reduced opacity |
| D4 | **Card system drift [Web].** Three surfaces (`#FCF3ED` / `#FBF6EF` / `#FFF`), radius 12 vs 16, two link blues (`#22458A` vs `#2F55A8`), hover lift on the homepage only | Grew from two parallel page families | One card spec: `#FCF3ED`, radius 12, 1px `#D4C0AA`, border-darken hover. Links `#22458A`; `#2F55A8` only for accents. |
| D5 | **Phone alignment** differs page by page (some centered, some left-aligned) | Decided page by page in the mobile pass | Pick one rule: center hero, section heads, and CTAs; left-align body and cards |
| D6 | **Bilingual deck format** (10-01): drop Chinese in examples, use small unaligned Chinese, or an English deck with a QR code to the Chinese deck | In progress | Founder to decide |
| D7 | **Rotating seal watermark** on inner headers versus the formal-tone ban on "spinning seals" | Rotates once every 240s | Keep it (too slow to read as spinning) or make it static |
| D8 | **Coral accent on the web** (kickers, quote rules, high-school band) while print uses none; social allows "one coral accent" | Present on the web | Decide whether coral stays a web and social accent or is removed for one blue system |
| D9 | **Pillar names** have three treatments on the web (roman 26px; italic `#2F55A8` 38px; italic 30–36px) | Drift | One treatment: italic `--ink-2` Newsreader with the marker on the key word |

---

## 13. Known drift and bugs (fix when next touched; not design rules)
- **Footer:** the Chinese footer tagline renders as synthetic italic at desktop width (`mobile.css:177` fixes it only below 560px).
- **Footer:** link hover color `#22458A` on `#0E1729` is nearly invisible.
- **Homepage hero:** the canvas still reacts to the cursor; the 09-30 direction is no cursor effect.
- **Dead CSS** (no live page uses these):
  - `index.css`: about 12 retired blocks.
  - `riso-theme.css` §21 is duplicated.
  - `riso-interact.js` targets.
  - `.partners-trust`, `.ic` icons, `.fp-*`.
- **Dead assets:** `riso-interact.js` still loads on every page; `fonts/gf.css` is unused.
- **`--font-mono`** is now an alias for the sans, so its name misleads.
- **One-pager:** the English version uses straight apostrophes (what's, it's, we've); change to curly.
- **Bilingual deck:** as of 2026-10-01 15:10, slide 13 measured 1147px after the 10-01 "+text" edit, so the export guard would fail until it's re-laid out.
- **Older materials:** `decks/bwya*.html`, `meeting-kit/onepager*.html`, and `curriculum-one-pager*` still use Geist and Geist Mono and offset shadows. Treat them as superseded and don't copy from them.

---

## 14. File map
| What | Where |
|---|---|
| This design system | `DESIGN.md` (repo root), the only source |
| Copy, voice, claims, page order, Chinese style, confirmed facts | `CONTENT-RULES.md` |
| Web CSS | `styles.css`, `riso-theme.css`, `css/*.css`, `mobile.css`, `fonts/zh/zh.css` |
| Logos (web) | `logos/arena/`, `logos/cred/` |
| Logos (masters), patterns, social sizes | Drive › Arena AI › 04 Marketing, Brand & Media › Logos (README there covers files only and points here) |
| Riso art for social | Drive › 04 › social-media-resources |
| Deck source and tools | `~/Desktop/projects/arena-school-tools/deck-src/` (local, not in repo) |
| One-pager source | `~/Desktop/projects/arena-school-tools/riso-v2/site-preview/_kit/` (local); live PDFs and JPGs in the repo at `/onepager/` |

## Phones (≤760px) and Arena Notes (added 2026-10-13)

**Phone layer.** Everything phone-only lives in `phone/*.css|js` partials (built by `tools/phone_build.py` into `/phone.css` + `/phone.js`, linked LAST on every page by `tools/phone_markup.py`). Every rule sits inside `@media (max-width:760px)`; desktop renders exactly as before. Edit a partial, then run `python3 tools/newsletter_markup.py && python3 tools/phone_markup.py`.
- Grammar: the digital business card (`/card/*`): grouped rows on Arena paper (surface #FBF6EF, hairline rgba(11,26,74,.12), radius 16), 56px rows with chevrons, full-width 56px pill buttons, press (`:active`) states, one clear action per screen. No decorative icon bubbles; logos never in tiles or on white.
- No hover on phones: phone.js removes every `:hover` rule at ≤760px and blocks mouse-hover listeners. Design every interaction tap-only.
- Heroes: short and centered; one primary pill, the second action as a text link; "at a glance" facts as label/value rows. Homepage: crest + headline + one line + two actions, no eyebrow chip.
- Section titles left-aligned (iOS large-title style); body and lists left-aligned.
- Type: body 16px (EN 1.6, CN 1.75), secondary 15–15.5px, labels ≥12px EN / ≥13px CN; Chinese letter-spacing ≤ .04em, no faux italic; no `text-wrap: pretty` on Chinese pages (crashes iOS 26 WebKit on the homepage).
- Line breaks: buttons, pills, chips, and tabs never wrap (use phone-only shorter wording, logged in `phone/WORDING-*.md`); no orphans (phone.js keeps the last words / a Chinese word together); Chinese text is segmented into words so lines never break mid-word.
- No big expansions: anything that would open more than about half a screen of non-essential content links to the page that holds it (e.g., founder bios → /about#jing-jing-yang). FAQ answers stay inline.
- Frame: 56px nav that hides on scroll down; bottom action bar (the page's main action) after the hero, hidden near closing forms; compact footer (`.ph-foot`) instead of the desktop footer.
- Diagrams each have a deliberate phone form (grade map as rows without the axis header, step selectors and ladders as vertical timelines, segmented controls on Approach and Conferences, swipe strips with a visible peek).
- Review tool: `arena-school-tools/phone-preview` (live phones, before/after, checks for wrapped labels, orphans, readability, spacing, tap targets).

**Arena Notes (newsletter).** `newsletter.js` + `newsletter.css`, endpoint `api/subscribe.js` (Resend). Shows only when the deployment has `RESEND_API_KEY` and `RESEND_SEGMENT_ID` (GET /api/subscribe reports `configured`). Welcome email is sent only when `RESEND_FROM` is set (domain verified).
- Placements: homepage band after "Upcoming programs" + a one-time sheet ~3s after the programs section comes into view (never again after subscribing; 60 days after "Not now"); bands before the closing section on About, Approach, Results, Community Dialogues, Conferences; a "Get Arena Notes" button/row in program closing blocks; desktop footer field; phone footer row. Not on Contact, Enroll, Pay, Schools, or Partnerships bodies.
- Copy: "Programs we're opening, talks we're giving, and what we're learning about kids and AI." No cadence promise. Role is required: "I'm a…" Parent / Student / Educator / Other.
- Testing: `?nl=now` opens the sheet; `?nl=reset` clears the remembered "Not now" / subscribed state.

## Elegance pass: audience and winter pages (2026-10-16)
Applies to Teachers (`/programs/teacher-training`), Technology staff (`/schools/technology`), School leaders (`/schools`), and the winter program page (`/events/isb-winter-2027`), EN and CN. Founder direction: elegance and simplicity over critic scores; short pages; depth in tabs, carousels, and expandables; a small picture behind each point.
- **Files:** `css/elegance.css` (all `.el-*` layout and `.elg-*` pictures) and `/elegance.js` (tabs and carousel arrows). Pages carry `<body class="el">` and drop `zl-page`, so the nav sits dark-on-light over a light hero.
- **No dot grid.** Heroes are flat header paper (`#F3E9DD`) with a hairline; no `.hero-bg` riso field and no `hero-inv`.
- **Hero:** eyebrow chip, Newsreader 500 h1 with one italic `--ink-2` phrase, lede, one primary pill plus a text link; the right column is an "at a glance" list (label/value rows on hairlines, navy top rule). Phones center the hero.
- **Section head:** two columns, eyebrow plus Newsreader 300 h2 on the left, one short line on the right.
- **Depth on demand:** tabs (`.el-tabs`, 2px `--ink-2` underline on the active tab), a vertical tab list with a picture panel (Technology), a scroll-snap card carousel with arrow buttons (Teachers tools; swipe on phones with an 84% peek), and hairline `<details>` FAQs.
- **Pictures (`.elg-*`):** small HTML/CSS mockups in navy line on ivory (`#FFFDF9` windows, `#FCF3ED` panes, 1px `rgba(11,26,74,.14)` hairlines). Decorative, so `aria-hidden`. No icons, no stock art.
- **Closing band:** navy, cream h2 with `#A9BEEA` italic, cream pill; the one-pager form sits on a flat cream card.
- **Winter banner on phones:** the program name scrolls sideways as a ticker; the Register pill stays fixed (`promo.css`).


## Pro system (2026-10-16, founder: "more professional/legit for schools"): supersedes the cream palette above
Where this section conflicts with earlier sections (paper colors, eyebrow chips, pill buttons, dot grids, the seal watermark, riso markers), this section wins. Decks and talks are out of scope and keep their own look.
- **Grounds:** page white `#FFFFFF`; bands and heroes cool off-white `#F5F7FA`; sunk wells `#EEF1F6`; hairlines `#E2E6EE` (stronger `#CDD3DF`). Navy `#0B1A4A` stays the ink and the one dark band per page. Colors were moved in the source files by `tools/pro_recolor.py` (idempotent).
- **Type:** one scale with `clamp()`: h1 `clamp(34px, 1.1rem + 2.1vw, 52px)`, h2 `clamp(26px, .95rem + 1.25vw, 36px)`, both Newsreader 500; body Geist. h1 max 20ch. One italic accent at most; no halftone markers.
- **Labels, not chips:** eyebrows are 12px Geist 600 caps in `--ink-2` (light blue on navy), no fill, no dot.
- **Components:** 8px buttons, 10–12px cards, hairline borders, no shadows on cards; "at a glance" facts sit in a bordered panel.
- **Heroes:** light, copy left, a real photo plus the facts panel right, both aligned to the top (fixes the 1024–1280 Technology hero).
- **Photos:** one slot component `.pro-photo` (3:2, 12px radius, hairline). Real photos only; missing ones are dashed placeholders with `TODO-PHOTO:` comments. Inventory: `PHOTO-SLOTS.md`.
- **Logos:** tools taught (only those the page lists) and team affiliations (only those on About), grayscale, optical heights. Inventory and sources: `LOGOS.md`.
- **Motion:** the existing `.reveal` system, softened to a 12px rise over 600ms ease-out with the 80ms stagger in motion.js; tab panels crossfade in 450ms; everything is static under `prefers-reduced-motion`.
- **Files and order:** `css/pro.css` is linked last on every site page by `tools/pro_markup.py`, which also stamps stylesheet versions. Run after edits: `python3 tools/pro_recolor.py && python3 tools/phone_markup.py && python3 tools/newsletter_markup.py && python3 tools/pro_markup.py`.
- **Canvas:** Arena School pro system, https://claude.ai/artifact/6YmQtcXvpoLUVLybmrzTfq (system sheet plus home, technology, teachers, leaders, winter, and a program page at 1280 and 390).

- **Photo-led program heroes (2026-10-16; the photo band is superseded by the cine4 hero below):** every program page hero (programs/*, schools, schools/technology, events/*, mentorship, zero-to-launch) ends in one large real-photo band, `.pro-hero-media` with `.pro-photo.is-wide` (2:1, 3:2 on phones, `--focus` sets the focal point). People first; mockups and logo strips are secondary, lower on the page. Missing photos are dashed `is-todo` blocks with `TODO-PHOTO:` comments. No stock photos anywhere on the site. Inventory: `PHOTO-SLOTS.md`.
- **Site hero: cine4 (approved 2026-10-16, FINAL-BRIEF):** every site page (not decks/, talks/, `card/*`, or the payment page) opens on a full-bleed real photo crossfade (1 to 4 photos, 7s each, slow zoom) under a navy gradient, a faint light particle field (riso-particles.js on black paper with light ink, screen-blended at 38%, calm zone around the copy), the ivory crest (72 to 104px, 88% opacity) above the eyebrow, and white type; the photo caption sits above the shade and crossfades with its photo. Headline size per page via `--cine-h1` (clamp). Facts panels: a white card (audience pages) or a dark glass row (program pages, desktop; phones keep the phone layer's white rows). The nav stays solid white; `zl-page` is gone from these pages. Files: `tools/hero_markup.py` (markup and per-page photos; rerun after hero edits), `cine.js`, `css/cine.css`. Reduced motion: one still photo, no zoom, still dots. The earlier ?hero previews (A/B/C, cine1 to cine5) and `css/hero-bg.css` are removed. Photos: `PHOTO-PICKS.md`; slots and fallbacks: `PHOTO-SLOTS.md`.
- **Hero crops and motion (2026-10-16, CROP-BRIEF):** each hero photo has face boxes and crop settings in `tools/hero_markup.py` (read off a 5% grid of the photo). Desktop (over 900px): a slow Ken Burns zoom about the main face (homepage 6%, subpages about half), with the copy kept to the left ~42% so faces stay clear of text, panels, and the shade. Phones and tablets: the photo sits in a band under the nav (copy below it) and pans right to left with a slow zoom, 14s per photo, crossfading over 1.6s (subpages pan about half as far); separate pan stops for 761 to 900px. The Hong Kong hands-on still has faces across the whole frame, so on desktop it swaps for another photo in the same slot. Reduced motion: one still frame with the faces centered. Transform-only animation with will-change. The homepage's rotating word (students, families, educators, schools) sits in a fixed-width slot (the widest word) and fades out before the next fades in, so two words never overlap and nothing reflows.
