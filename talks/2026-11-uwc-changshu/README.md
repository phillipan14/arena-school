# UWC Changshu · November 2026 presentation

## One canonical presentation

- **Share this deck:** https://arenaschool.org/talks/2026-11-uwc-changshu/deck
- Resources: https://arenaschool.org/talks/2026-11-uwc-changshu
- **Edit `deck.html` in this directory.** This is the authoritative HTML presentation, including its CSS, slide markup, and navigation JavaScript. There is no separate PowerPoint/PPTX source.
- `slides.pdf`, `slides/*.png`, and `read.html` are generated views of the same presentation, not alternative drafts. Do not edit those files independently.
- `student-guide.html` is the editable companion guide; `student-guide.pdf` is its export.
- `index.html` is the resource landing page. Keep its links pointing at the canonical files.
- `assets/` holds the video, QR code, and source brand/example images. Some images and fonts are embedded in the deck for portability.

Old `?revision=...` links point to this same deck, not older versions. The deck removes the obsolete cache-refresh parameters when opened. `#12`, for example, simply opens slide 12. Keep previous states in Git history rather than adding `v2`, `final`, or duplicate deck files.

## Handoff for Phillip’s agent

1. Pull the latest `main` from `phillipan14/arena-school`, then create a working branch. Read this file first.
2. Edit `talks/2026-11-uwc-changshu/deck.html`. Use targeted edits: the file includes long embedded image/font data. The late CSS rules contain the final style overrides.
3. Maintain the approved title, Jing Jing as presenter, five sections, clickable contents, and resource QR. The deck currently has 24 slides. If reordering, update contents destinations, `part-*` IDs, section labels and displayed footer numbers.
4. Preserve Arena’s Newsreader/Geist typography, dotted backgrounds, navy chapter slides, official crest watermarks, and animated beige highlights. Cards and table cells are centered horizontally and vertically. Highlights must remain fully visible in PDF and reduced-motion mode.
5. Install export dependencies once, then regenerate the derived files:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install playwright beautifulsoup4
   python -m playwright install chromium
   python talks/2026-11-uwc-changshu/render.py
   ```

6. Review the deck in a browser and the exported slides. Check contents links, slide numbering, table/card alignment, highlights, video, QR destination and PDF pagination. Use `python3 -m http.server 8000` at the repository root for local browsing.
7. Commit the edited HTML and regenerated PDF/reader/images together. Open a PR and merge using the normal review workflow. The existing Vercel deployment publishes merged `main` at the same URLs.

`render.py` uses only files in this repository. It needs no files from Jing Jing’s laptop, private Drive, or the earlier local Python revision scripts. Those local drafts are not the source for future work. Do not overwrite this deck with a stale local export.
