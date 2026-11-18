<!-- Drop-in replacement for §10.3 of DESIGN.md in phillipan14/arena-school (the current text still prescribes the
retired riso recipe). Not pushed: waiting for JJ's go-ahead. -->

### 10.3 One-pagers, proposals, and other PDFs [Print]
- **Style:** the pro style of the site (Oct 16, 2026). The riso recipe (beige paper, dot grid, seal watermark,
  serif only) is retired for new documents.
- **Sources:** one-pagers in `tools/one-pager/` (built by `tools/one-pager/build.py`); proposals and other
  multi-page PDFs from the print kit (`arena-print.css`, kept with the working files outside the repo).
- **Export:** Playwright `pdf(format='A4', print_background=True, margin=0)`. One-pagers must be exactly one page;
  multi-page documents must clear the running footer on every page.
- **Recipe:**
  1. **Ground:** white, `--pro-alt` for tinted cards; no texture.
  2. **Type:** Geist body and labels; Newsreader 500 for headings and numbers; one italic accent per headline.
  3. **Header:** navy band, real program photo fading in from the left, ivory wordmark, "A member of" with the
     Anthropic Startup Program and OpenAI Partner Network marks.
  4. **Sections:** navy number block, serif title, one-line dek.
  5. **Blocks:** hairline cards (2mm radius), hairline tables, logo rows in one greyscale darkness.
  6. **Footer:** navy contact band with named people and arenaschool.org addresses.
  7. **Checks:** no em dashes, Oxford commas, honest photo captions, no dead space, no orphaned words.
