# Arena riso design system

Every style rule below applies to **every page**. The code lives in `riso-theme.css`, which loads after `styles.css` on all 33 pages, and in `riso-field.js`. To change the look, change these two files, then run the visibility audit (see the last section).

## Inks and paper
| Token | Value | Use |
|---|---|---|
| `--ink` | `#0B1A4A` | Navy ink: titles, dots, eyebrow chips |
| `--ink-2` | `#2F55A8` | Bright blue ink, the second drum: keywords, title italics, misregistration shadow |
| `--paper-hi` | `#FCF3ED` | Clean paper: the homepage hero and the seal disc |
| `--bg-paper` | `#EFE3D4` | Light beige surfaces. These carry the riso tint. |
| `--bg-paper-soft` | `#E6D4C1` | Darker beige surfaces (for example, founding team). These stay clean, with no tint. |

## Print texture
- **Screen:** one halftone screen throughout. The angle is 18.4° and the pitch is about 2.5 CSS px. Each dot is printed in either navy or blue, about 45% blue.
- **Homepage hero:** a `data-riso-field` canvas that reacts to the cursor.
  - A soft ombré follows the cursor and fades out.
  - When the page is idle, a slow drift keeps it moving.
  - The ink clears behind the text and the nav.
  - The bottom 22% fades into `--bg-paper`.
- **Inner-page heroes:** a `data-riso-field="static"` canvas, drawn once.
  - No cursor effect and no motion.
  - The resting ombré is mirrored so the ink sits on the right, away from the left-aligned text.
- **Light beige paper:** `art/riso-tint.png`, sparse tiny dots on the same screen, about 0.9% coverage. It's the same texture the hero fades into.
- **Never** use random splatter or grain: every dot sits on the halftone screen.

## Inner-page heroes: social-kit header (chosen Sept 28)
- **Look:** ivory paper `--paper-hi` with a 24px dot grid, and the navy seal as a watermark at 8.5% opacity, sitting 130px below the top on the right and turning once every 4 minutes. It's built by hero-options.js (option A) on every page whose hero section has `hero-inv`.
- **Headline:** navy, with italic key words in `--ink-2` that get the riso marker, which prints in on load.
- **Nav:** stays navy. ?hero=B|C|D|navy previews the rejected alternatives; header-demo.html compares them.

## (Previous) inverted print
- **Which pages:** every inner page (not the homepage) opens with an inverted riso print: navy paper `--ink`, beige `#EFE3D4` and brown `#B8895C` dots (about 42% brown), and light type.
- **Motion:** each dot bounces gently around its home spot, at about 14% of the dot spacing and about 30fps. Nothing morphs, and there's no cursor effect. With reduced motion, it's static.
- **Markup:** `<section class="hero hero-inv">` plus `<div class="hero-bg" data-riso-field="static">`. The page's `<body>` gets `zl-page`, so the nav is light while it's over the navy and switches to navy once scrolled.
- **Chips and buttons invert:** paper chips and buttons, with brown offset shadows.

## Type
- **Hero titles on every page** (`.hero-riso-h1`, `.hero h1`, `.curr-hero h1`): Newsreader at weight 500, in `--ink`. Italic words inside them use `--ink-2`.
- **Eyebrow labels** (`.eyebrow`): a solid navy chip with paper-colored mono text and a 2px blue offset shadow, which imitates riso misregistration. On dark bands the chip inverts.
- **Keywords** (`<em class="rh">word</em>`): blue italic with a halftone marker band.
  - The band prints in from left to right, staggered word by word, when its block reveals.
  - Hovering over the word reprints the band.
  - With reduced motion, the band is simply shown.
  - Use it only for short keywords, with one `.rh` per word. Don't use it for whole phrases.

## Graphics and interaction
- **Plain paper behind graphics:** any section containing a timeline, steps, milestones, stats, cards or a form uses plain `--bg-paper`, with no tint. The texture is decoration, and it never sits behind something the reader has to parse.
- **Cards:** on hover a card lifts 6px and gets a navy border plus a 5px blue offset shadow, the same misregistration language as the eyebrows.
- **Sequences:** `riso-interact.js` turns every timeline (`.tl-row`), numbered step (`.structure-row`), daily cascade (`.cascade-row`), milestone (`.fp-rung`) and rhythm node (`.fp-rhythm-node`) into an explorable graphic.
  - Hover, focus or tap an item to spotlight it; the other items dim.
  - It reveals the item's `data-detail`, a "what this means for you" line.
  - Vertical lists expand in place, and the timeline spine fills with ink down to the active day.
  - Horizontal tracks show a shared detail panel under the track.
  - A pulsing hint sits above each sequence.
  - The arrow keys and Escape work.
- **New sequence items** must carry a `data-detail` in both EN and CN (drafts are in `DETAIL-COPY.md`).
- **Contact promises** (`.partners-trust`): three ink-bordered pills with check marks.
- **Eyebrows:** always `inline-flex`, so the dot can never overlap the text.

## Icons
- **Style:** curriculum icons are literal line drawings, one metaphor per idea. They're drawn inline so they can animate, in navy with the key part in blue, on a paper disc with the same offset shadow as the chips.
- **Motion:** each icon draws itself in when it first appears, then acts out its idea once (for example, the lever tilts or the dot hops up the steps). Hovering its card or row replays that motion. With reduced motion, it's static.
- **Source:** the drawings live in `tools/icons.py`, which generates them. Add new icons there so the style stays consistent.

## Logos and photos
- **Logos:** only the transparent wordmarks in `logos/cred/`, in navy #1B2540. The old square "orgs" chips are retired. `microsoft-ai.png` was recreated in the same navy; replace it with an official file if Microsoft provides one.
- **Photos:** only as content (galleries, portraits), never as section backgrounds. Former photo heroes are static riso heroes, and former photo bands are pull-quotes on paper.

## Visibility audit
Run `python3 audit.py` with the preview server on port 8780. For every page, it measures how much ink sits behind each title, lede and eyebrow. It flags any block with more than 10% ink behind it, and writes `audit/sheet.png` so you can review every page by eye.

## Logo rule (founder direction, Sept 28)
Always use the **official lockup PNG** (seal plus wordmark as one image): `logos/arena/wordmark-navy-1600.png` on light backgrounds, `wordmark-ivory-1600.png` on dark ones. The source files are `arena-wordmark-*-transparent*.png` in the brand kit. **Never** place the seal next to typed-out "ARENA SCHOOL" text. That applies to the website, decks, social posts and every other asset.

## Formal tone (founder direction, Sept 28)
The site speaks to parents, heads of school, and educators, so it must read as official and trustworthy.
- **No solid offset shadows** (the old blue/coral "misregistration" blocks behind cards, buttons, eyebrows, and pins). Cards lift with a soft shadow: `0 18px 40px -22px rgba(11,26,74,.38)`. Small elements get no shadow.
- No handwriting fonts, sticky-note walls, emoji, chat bubbles, spinning seals, or floating stat chips.
- Prefer real program photos and official institution lockups over illustrations.
