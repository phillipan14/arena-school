# Arena School design system (Oct 16, 2026)

Tokens live on `:root` in `css/pro.css`; components in `css/ds.css` (linked on every page by `tools/pro_markup.py`,
right after `pro.css`). Recorded in the Claude Design project "Arena School pro system":
https://claude.ai/artifact/6YmQtcXvpoLUVLybmrzTfq (boards: tokens and components, Motion and UX, Spacing and
components, Editorial matrix, Learning approach). Migration status: `DESIGN-MIGRATION.md`.

## Spacing, measure and type (EDITORIAL-BRIEF)
| Token | Value | Use |
|---|---|---|
| `--space-1` … `--space-10` | 4, 8, 12, 16, 24, 32, 48, 64, 96, 128px | every gap, padding and margin in ds components |
| `--section-y` | clamp(64px, 8vw, 128px) | vertical rhythm between sections (64px on phones) |
| `--measure` / `--measure-narrow` | 68ch / 60ch | body line length; ledes use the narrow measure |
| `--radius-ctl` / `--radius-card` | 8px / 12px | controls / cards |
| `--hairline` | 1px solid `--pro-line` | rules between rows, card borders |
| `--text-xs` … `--text-lg` | 12, 14, 16, 17, 19px | small caps labels to large body |
| `--pro-h1` / `--pro-h2` / `--pro-h3` | clamp scales | display, section and card headings (Newsreader) |
| `--lh-tight` / `--lh-body` | 1.15 / 1.6 | headings / body |
| `--pro-ink`, `--pro-ink-2`, `--pro-soft`, `--pro-line`, `--pro-alt`, `--pro-tint` | navy, action blue, body grey, hairline, band, light accent on navy | colour |

## Components (`css/ds.css`)
- **ds-section** (`.is-alt` for the band colour): `--section-y` top and bottom; a hairline between two white sections.
- **ds-head**: eyebrow across the top, the heading left (max 24ch), the lede right on the narrow measure; `.is-center` for a single column.
- **ds-eyebrow** (small caps label, `.is-muted`), **ds-h2**, **ds-lede**.
- **ds-grid** (`-3`, `-4`; collapses at 1100 / 900 / 760px) and **ds-card** (hairline, 12px radius, `--space-6` padding; `.is-media` puts a photo on top).
- **ds-doors**: a ruled row of audience links ("Who are you?").
- **ds-list** / **ds-list-row**: dated rows (date column, body, arrow) on hairlines.
- **ds-logos**: logo rows with a label column.
- **ds-mx** (editorial matrix) with **ds-band** (BAND-BRIEF): hairline grid, small caps heads, faint column guides; one flat tinted band per row (`--pro-ink-tint` 14% of the action blue, 5px radius, 30px), label inside; worked-example days as blocks, practiced in `--pro-ink-tint-2`. Hover/focus: the band turns solid navy, other rows dim. Phones: name, grades, a thin track with the band; day chips in the same tints. Used by the Learning approach week and the homepage "Where each program fits" (`.ds-gmx`, `tools/grade_matrix.py`).
- **ds-ic**: Lucide line icons, 1.6 stroke, `currentColor` (`tools/lucide_icons.json`, ISC).
Migrated pages keep their legacy classes where scripts rely on them; above 760px the ds rules win. At 760px and below
the phone layer (`phone.css`, built from `phone/*.css`) keeps its own layout until each page group is migrated.

# Motion and UX (MOTION2-BRIEF)

Recorded in the Claude Design project "Arena School pro system", artboard **Motion and UX · tokens, rules,
timeline**: https://claude.ai/artifact/6YmQtcXvpoLUVLybmrzTfq (private until shared from its Share menu).
The code reads the same values as CSS custom properties on `:root` in `css/pro.css`.

## Why
macOS/iOS/Windows **Reduce Motion** made every photo on the site still: all motion was gated behind
`prefers-reduced-motion: no-preference`, and `cine.js` skipped the crossfade under `reduce`. The system now says:
photos always move; Reduce Motion gets a gentler version, never none.

## Tokens (`css/pro.css`)
| Token | Full motion | Reduce Motion | Used by |
|---|---|---|---|
| `--ease` | cubic-bezier(.22, .61, .36, 1) | same | UI: hovers, reveals, menus |
| `--ease-io` | cubic-bezier(.45, 0, .25, 1) | same | photo zoom and drift |
| `--dur-fast` / `--dur-ui` / `--dur-reveal` | 180ms / 280ms / 600ms | same (reveals show content, no slide) | UI |
| `--xf-hold` | 6s | 7s | hero crossfade, time each photo holds |
| `--xf-fade` | 1.4s | 2.2s | hero crossfade length |
| `--kb-dur` | 20s, alternate | 30s | hero Ken Burns |
| `--kb-scale` / `--kb-tx` / `--kb-ty` | 1.07 / −3% / −1.5% | 1.03 / −1% / −0.5% | hero Ken Burns |
| `--drift-dur` | 22s, alternate | 30s | framed photos |
| `--drift-scale` / `--drift-tx` / `--drift-ty` | 1.07 / −2.5% / −1.5% | 1.03 / −1% / −0.5% | framed photos |

## Texture: the deck dot grid (DOTS-BRIEF, Oct 16)
Copied exactly from the ACAMIS deck's photo divider slides: selector `.p6-dots` in
`~/arena-school/decks/2026-10-acamis-tech-workshop/src/css/s99zzzzzzzzzzzzzzzzzzzzzzzzzzzzz-p6.css` (working copy).
| Token | Desktop | Phones and tablets (≤900px) |
|---|---|---|
| `--tex-dots-c` | rgba(201, 214, 242, .9) | same |
| `--tex-dots-s` (grid) | 22px (dot 1px, soft edge to 1.6px) | 26px |
| `--tex-dots-o` | .22, `mix-blend-mode: screen` | .14 |
Mask: `linear-gradient(100deg, #000 0%, rgba(0,0,0,.55) 45%, transparent 80%)`, so the grid fades toward the photo's
bright side. On the site it is `.cine-dots` (css/cine.css): static (the deck drifts it; the site does not), above the
photo and navy shade, below captions and text, `pointer-events: none`. It replaces the old JS particle field
(riso-particles.js no longer loads on hero pages).

## Rules
- **Hero:** 3 photos. Crossfade cycle = 3 × hold (18s; 21s under Reduce Motion); slot *i* starts at *i* × hold − fade,
  so photo 1 is fully in at load. Ken Burns runs continuously on the `img` (ease-in-out, back and forth), independent
  of the crossfade; the slide wrapper only fades. Desktop scales from the left edge, so the right overhang always
  covers the drift; phones pan right to left (Reduce Motion: a short pan around the faces-centered frame).
- **Framed photos** (closing CTA, results cases, contact, school photo rows): `pro-drift` at every width.
- **Dropped under Reduce Motion:** big zoom/pan, parallax, scroll-linked effects. **Kept:** gentle zoom, crossfades.
- Transform and opacity only; max zoom 1.07 for the 1600px sources; every animated photo sits in a clipping frame.
- **Reveals** are gated on `html.js` (content never hidden without JavaScript); none inside the hero.
- **Header:** plain CSS `position: sticky; top: 0`, solid ground, hairline bottom; no hide-on-scroll, no transform.
  The banner scrolls away above it; its space is reserved from first paint.
- **Focus:** one ring, `outline: 2px solid #2F55A8; outline-offset: 3px` plus a white halo (white ring on navy bands).
- **Touch:** targets at least 44px; small links grow by padding. Anchors use `scroll-margin-top` 92px (68px phones).
- **Forms:** focus, `:user-invalid`, busy and success states.
- **Timeline component** ("Where each program fits"): 44px rows on a `#F5F7FA` track, bars in the navy family
  (`--pro-ink-2` to `--pro-ink`), every label inside its bar (short bars stack name over grades), a wider College column.
  Phones: name, grades as text, then an 8px track with the program's segment.

## Where it lives in code
`css/pro.css` (tokens, Reduce Motion token swap, `pro-drift`), `css/cine.css` (crossfade and Ken Burns keyframes),
`cine.js` (loads photos 2 and 3 after the first and starts the cycle in both modes), `tools/hero_markup.py`
(slot index `--i` only; no timing in markup), `css/grades.css` (timeline).
