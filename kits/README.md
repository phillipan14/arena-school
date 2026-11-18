# Arena School design systems and output kits

Every Arena School design system and output kit, so any PDF or image can be regenerated with one command.
**This folder is in a public repo and is excluded from the website deploy (`.vercelignore`).** Private material
(pricing, contact details, QR codes, client proposals, and finished posters) is kept out; see "Private assets" below.

Requirements: Python 3.11+, `pip install playwright pillow numpy pypdf`, `playwright install chromium`.
Fonts, logos, and photos are bundled, so nothing needs the internet except the ISB winter poster's fallback to
arenaschool.org for any missing site asset.

## Which system for what

| Need | System | Style | Where |
|---|---|---|---|
| A proposal for a school or partner | **Proposal design system** | Current (pro) | `kits/print/proposal/` |
| Any other multi-page PDF (brief, report, plan) | **Print kit** | Current (pro) | `kits/print/` |
| General one-pagers (general, teacher, parent; EN and CN) | One-pager v3 | Current (pro) | This repo, root (see Links) |
| The website itself | Website design system | Current (pro) | This repo, root (see Links) |
| Talk and workshop decks | Deck sources | Current | Website repo `decks/` (see Links) |
| Event posters (vertical, WeChat and Xiaohongshu) | Poster kits | Riso, one per event | `kits/riso/web/_kit/…` + `kits/posters/` |
| Wordmark + web address lockups (image posters only) | Lockup builder | Brand | `kits/brand/wordmark-url/` |
| Business cards, contact share card, LinkedIn banner | Card kits | Riso | `kits/riso/web/_kit/` |
| Xiaohongshu carousels (3:4) | XHS kit | Riso covers | `kits/xhs/` |

"Current (pro)" = the arenaschool.org style since Oct 16, 2026: white pages, Geist body, Newsreader headings, navy
`#0B1A4A`. New documents use it. The riso kits are kept so past posters and cards can be reissued or adapted.

## Build commands

### Proposals and print documents (`kits/print/`)
```bash
cd print
python3 new_proposal.py <slug> "<Client full name>" "<Client short name>" [client-logo.png]   # creates docs/<slug>/
cd docs/<slug> && python3 build.py      # fill every yellow [Write: ...] first; the build refuses otherwise
```
- Spec: `print/proposal/DESIGN-SYSTEM.md` (readers, page structure, components, copy rules, fee rules, checks).
- Shared recipe: `print/README.md`. Checks: `print/orphans.py`, `print/measure_centering.py`.
- The day rate and finished client proposals are in the private Drive Proposals folder. `print/docs/` is git-ignored so
  client proposals (which contain fees) never get committed.

### Riso kits: posters, cards, lockup page (`riso/`)
All of them load `/fonts`, `/logos`, `/art`, `/card`, and `/_kit` from `riso/web`. Start the server on the port the
render script expects, then run the script from its folder:
```bash
python3 kits/riso/serve.py 8780     # or 8781; leave it running in another terminal
```

| Output | Server | Render |
|---|---|---|
| ISB parent coffee poster, EN and CN, Oct 14, 2026 (PNG, JPG, PDF for Canva) | `riso/serve.py 8781` | `cd kits/riso/web/_kit/isb-coffee && python3 render.py en cn && python3 pdf.py` → finals in `posters/isb-parent-coffee-2026-10-14/` |
| Lux Scholar talk poster, Oct 14, 2026 (CN) | `riso/serve.py 8780` | `cd kits/posters/lux-talk-2026-10-14 && python3 render.py final.png` |
| Lux Scholar talk poster, Nov 15, 2026 (CN) | `riso/serve.py 8781` | `cd kits/posters/lux-talk-2026-11-15 && python3 render-v2.py final-v2.png` |
| Business card (per person, EN and CN sides) | `riso/serve.py 8780` | Open `http://127.0.0.1:8780/_kit/business-card.html?who=jingjing` (or `phillip`) and print to PDF |
| Contact share card, LinkedIn banner | `riso/serve.py 8780` | Open `/_kit/share-card.html` or `/_kit/linkedin-banner.html` and screenshot the card |
| Wordmark + URL lockup page | `riso/serve.py 8780` | Open `/_kit/wordmark-url/` |

To make a new poster: copy the closest `riso/web/_kit/<poster>/` folder and its `posters/<event>/` render script,
change the copy and assets, and render. Posters use the web-address lockup (`brand/wordmark-url`) only when the image
will be shared without clickable links.

### AI Fundamentals @ ISB poster, Jan 5–8, 2027 (`posters/isb-ai-fundamentals-2027-01/`)
```bash
cd kits/posters/isb-ai-fundamentals-2027-01 && python3 serve.py 8795     # leave running
cd v3 && python3 build.py && python3 render3.py en cn                 # → out-en.png, out-cn.png (2160x3840)
```

### Wordmark + URL lockups (`kits/brand/wordmark-url/`)
```bash
python3 kits/riso/serve.py 8780                         # leave running (the builder renders /_kit/wordmark-url/)
cd kits/brand/wordmark-url && python3 make_all.py      # 8 colorways × 2 sizes + REVIEW-all-colorways.png
```

### Xiaohongshu carousels (`kits/xhs/`)
```bash
cd kits/xhs && python3 render.py [post numbers]      # → out/post-NN/slide-NN.png (1080x1440); no server needed
python3 build_preview.py                        # preview page (needs node)
```

## Final exports and private assets

Finished files are not in the repo. They are in Google Drive:
- **Posters:** Arena AI › 04 Marketing, Brand & Media › Design systems › Posters.
- **Private (pricing, contacts, QR codes):** Arena AI › 02 Curriculum & Programs › Meeting kit (private) ›
  Proposals (private: pricing) and Kit private assets.

Before rendering anything that prints contact details or QR codes, copy the real files from "Kit private assets":
- QR images: every `qr*.png` / `qr*.jpg` in the kits is a gray placeholder of the right size; drop the real one in
  under the same name (don't commit it).
- `riso/web/_kit/business-card.html` and `share-card.html`: replace `[WeChat]`, `[WeChat ID]`, and `[phone]`.
- Proposals: replace the yellow day-rate placeholder with the rate from the Proposals folder.

## Links: systems elsewhere in this repo

- Website design system: `DESIGN.md`, `DESIGN-SYSTEM.md`, `DESIGN-MIGRATION.md`, `LOGOS.md`, `CONTENT-RULES.md`;
  tokens in `css/pro.css`, components in `css/ds.css`.
- One-pager v3 (general, teacher, parent; EN and CN): `tools/one-pager/build.py`; outputs in `onepager/`.
  Rationale: `ONEPAGER-RETHINK.md`, `ONEPAGER-POSITIONING.md`, `ONEPAGER-CHANGES.md`.
- Decks: `decks/<deck>/src` (`build.py`, `export.py`); exported slides and reader pages in `talks/`.
- Format audit checklist: `.claude/skills/format-audit`.
- Logo library (canonical): Google Drive › Arena AI › 04 Marketing, Brand & Media › Logos.

Note: `DESIGN.md` §10.3 still describes the retired riso one-pager recipe. The replacement text
is in `kits/print/DESIGN-10.3-replacement.md`.

## Retired

- `kits/riso/web/_kit/onepager*.html`, `kits/riso/retired-onepagers/`: the riso one-pagers, superseded by one-pager v3.
  Kept for reference only.
