# Poster v3 audit (round 1, superseded by round 2 at the bottom): AI Fundamentals for Students @ International School of Beijing (EN + CN)

Measured with `audit3.py` (DOM + rendered pixels at 2x), `leftedge.py` (ink left edges of each headline line), and OpenCV QR decoding at full size and at iPhone width. WeChat shows the 1080px poster about 390pt wide (x0.36).

## 1. Visibility on iPhone in WeChat: 8.5 / 10
Standards: body text >= 10pt on screen, labels >= 9pt, headings >= 14pt, every text WCAG AA (4.5:1) or better, QR decodable at phone size.
- Smallest text anywhere: 9.0pt (caps labels, bold, blue). Body: 10.4pt (29px). Hero lede: 11.9pt. Headings: 14.4pt (card titles) to 30pt (title).
- 0 text runs under 9pt, 0 under 4.5:1 contrast (EN and CN).
- QR decodes at full size and at iPhone size (EN to /events/isb-winter-2027, CN to /events/isb-winter-2027-cn); the "Press and hold to scan" / 长按识别二维码 line matches the WeChat gesture.
- Deduction: the smallest founder wordmarks (McKinsey, Microsoft AI) render about 7pt tall in a chat, kept at the founder-approved size; tool icons are grayscale like the site, so a few light icons (Ideogram, Midjourney) read faintly.

## 2. Centeredness: 9.0 / 10
Standards: every pill, card, and row within 2px of vertical center (ink, cap-to-baseline for type); every text block's left ink edge on the 54px margin (or the card's 30px inset); QR column centered in the navy band and aligned to the text column.
- Pills: 1.0 to 2.0px (EN), 1.0 to 2.0px (CN).
- Open-to-all card 0.0 / -1.0px; founders card 1.0 / 1.5px; navy band 0.5 / 1.5px; text column vs QR column 0.6 / -0.9px; facts rows within 1.5px.
- Headline lines: left ink edge 54.0px on all three lines in EN (italic overhang corrected) and 54.0 to 54.5px in CN (glyph side bearing corrected).
- Deduction: CN pills and CN founders card sit at the 1.5 to 2px edge of the tolerance.

## 3. Cohesiveness and flow: 8.5 / 10
Standards: one story top to bottom (what it is > who it's for > what they do > who teaches > logistics > next step); name, wording, and tools identical to the live page; no repeated sentences; nothing that contradicts the site.
- Order: title and lede > "Open to every student" > What students do (Learn / Choose / Finish, the live page's three points and wording) > Taught by the founders themselves > When / Where / Language > Scan to register interest.
- Name exactly per CONTENT-RULES §9 (school spelled out, no "ISB" in the name); "20+" dropped like the site; the 15 tool icons are exactly the 15 on the live page.
- Non-ISB students: "All schools welcome" pill + "You don't need to attend ISB, code, or love STEM." The "Who: ISB students" fact row was removed so nothing says ISB-only.
- Deduction: the date appears twice (eyebrow and facts) and the location three times (title, facts, and implicitly the pill); acceptable for a poster but not perfectly lean.

## 4. Communication and call to action: 9.0 / 10
Standards: one unmistakable action, said in words and shown by the QR; the reader knows what happens after scanning; nothing competes with it.
- Navy closing band, the only dark block on the poster: "Next step" > "Scan to register interest." > what's on the page (four-day plan, FAQs, short sign-up form) > "not a commitment; fees and details will follow" > QR with "Press and hold to scan".
- The QR lands on the program page, whose register-interest form is still at the bottom (see note); the band says "the page has ... a short sign-up form" so the promise stays true either way.
- Deduction: the form is not the first thing a scanner sees on the live page.

## Iterations
Round 1: labels 8.3pt and fact labels 7.9pt (fail) > raised to 9pt; open card 3px and navy band 12px off center > fixed; one short last line in card 02 > shortened.
Round 2-4: facts rows 10px off (EN) > fixed; Who row removed (ISB-only wording); italic headline line overhung the margin by 7px > corrected to 0; CN headline 4px right of margin > corrected; WeChat press-and-hold line added; tool icons darkened for contrast; QR enlarged with a quiet zone.


# Round 2 (JJ feedback, 2026-10-20)
Changes: one-line bold headline "AI Fundamentals for Students" / 学生AI基础营 (EN 74px Newsreader 600, fits 963 of 972px); location moved into the lede ("Located at the International School of Beijing." / 地点在北京顺义国际学校。); STEM card label removed, headline "You don't need to be a STEM student." / 不是理科生，也完全可以。; navy divider moved above the founders card (facts keep hairlines only); tool icons blend into the page (no gray tiles); poster 160px shorter (EN 2645px).

1. iPhone visibility: 8.5. Min 9.0pt, body 10.4pt, lede 11.9pt, headline 26.7pt; 0 runs under 9pt or under 4.5:1. QR decodes at phone size. Same deduction: smallest founder wordmarks about 7pt tall.
2. Centeredness: 9.0. Pills 1.0 to 2.0px; STEM card 0.0/0.0; founders 1.0/0.5; navy band 0.5/1.5; text vs QR column 0.1px; facts rows within 1.5px; headline left ink edge 54.0px in both languages.
3. Cohesiveness and flow: 8.5. Hero now says what, where, and who in three lines; divider splits "what students do" from "who teaches + logistics". Deduction: location appears in the lede and the facts, date in the eyebrow and the facts.
4. Call to action: 9.0. Unchanged navy band; deduction remains that the live page's form sits at the bottom.


# Round 3 (JJ feedback, 2026-10-20)
Changes: lede one line ("Students learn AI tools and use them to build a real product." / 学生学会使用AI工具，把一个想法做成真正能用的产品。), location now only in the Where row; card 03 one line ("A working version anyone can test, presented on day four." / 做出人人都能试用的版本，并在第四天上台展示。); founders-to-facts gap 40 > 22px; CTA: "Next step" label removed, headline one line, QR 300 > 236px. Height: EN 2645 > 2454px (-7%), CN 2658 > 2506px.

1. iPhone visibility: 8.5. Min 9.0pt, body 10.4pt, CTA headline 18.8pt; 0 runs under 9pt or under 4.5:1; QR decodes at phone size after shrinking. Deduction unchanged (smallest founder wordmarks).
2. Centeredness: 9.0. Pills 1.0 to 2.0px; STEM card 0.0/0.0; founders 1.0/0.0; navy band within 1.5px; text vs QR column within 0.5px; headline left ink 54.0px both languages.
3. Cohesiveness and flow: 8.5. Repetition is down (location once, in the facts). Deduction: the date still appears in the eyebrow and the facts; the lede is now generic ("build a real product") and no longer says where.
4. Call to action: 9.0. "Scan to register interest." is the first and largest line of the band, unlabeled; deduction unchanged (form at the bottom of the live page).


# Round 4 (JJ feedback, 2026-10-20)
Changes: STEM card and the 01-03 list replaced by one emphasized card, "Four days, step by step" / 四天安排: a vertical timeline (numbered nodes on a rail, Day 4 node filled navy) with Day 1 Learn (20+ professional tools for research, design, code, and video), Day 2 Choose and iterate (talk to real users, collect feedback, improve each version), Day 3 Prepare (polish, shape the pitch), Day 4 Present (live at its own link, on stage). Tool logos removed. STEM line moved into the lede as its own line. Height: EN 2454 > 2330px, CN 2506 > 2388px.

1. iPhone visibility: 8.5. Min 9.0pt (day labels raised from 8.3pt), body 10.4pt; 0 runs under 9pt or under 4.5:1; QR decodes at phone size. Deduction unchanged (smallest founder wordmarks).
2. Centeredness: 9.0. Timeline card 0.0 / 1.0px; each node's center on its day label's center (-0.4 / -0.1px); rail runs node to node; founders, navy band, facts, and pills all within 2px; text vs QR column 0.0px; headline left ink 54.0px.
3. Cohesiveness and flow: 8.5. The timeline now carries the whole story in order (learn > choose and iterate > prepare > present) and replaces two blocks. Deduction: date in the eyebrow and the facts; "20+" returns (Phillip removed it from the site as unconfirmed).
4. Call to action: 9.0. Unchanged; deduction remains the form's position on the live page.


# Round 5 (JJ feedback, 2026-10-20)
JJ caught that round 4's audit missed the numbers inside the timeline circles (not centered). Lesson: the audit now measures every repeated element individually (each numeral's ink against its title), not just the container.
Changes: timeline rebuilt in the site's own visual language (the research-stats and matrix blocks on arenaschool.org: navy top rule, hairline column and row dividers, big Newsreader numerals, no circles or dots); heading "Over four days, students will:" / 这四天里，学生会： set as a 58px serif h2; 2x2 grid instead of four stacked rows; "Day 1 · Learn" labels removed; per-digit side-bearing correction so each numeral's left ink sits on its title's left edge; Chinese breaks controlled (no split 设计, no orphan 改进/展示); grid bottom hairline dropped so only the navy divider separates the steps from the founders. Height: EN 2330 > 2189px, CN 2388 > 2198px.

1. iPhone visibility: 8.5. Min 9.0pt, body 10.4pt, section heading 21pt, numerals 27pt; 0 runs under 9pt or under 4.5:1; QR decodes at phone size. Deduction unchanged: smallest founder wordmarks about 7pt.
2. Centeredness: 9.0. Numerals vs titles 1.0 to 1.8px; titles and bodies share one left edge per column (54.5 / 571.5px); grid row ink gaps equalized (top 23 = bottom 23); founders, navy band, facts, pills within 2px; text vs QR 0.0 to 0.5px; headline left ink 54.0px.
3. Cohesiveness and flow: 8.5. One story: what it is > over four days students will 1-4 > who teaches > when/where > scan. Deduction: date in the eyebrow and facts; "20+" (unconfirmed per Phillip).
4. Call to action: 9.0. Unchanged; deduction remains the form's position on the live page.


# Round 6 (JJ feedback, 2026-10-20): 9:16
Format: exactly 1080x1920 CSS px (2160x3840 export), 9:16 vertical; the poster has a fixed height and any slack goes above the CTA (currently 30px, the minimum).
Changes: numerals now hang on the title line (60px serif numeral, baseline-aligned with the 38px title; description runs full width under both); spacing tightened throughout (hero 44/38, rule 24/28, grid 18, navy 24-26, facts 14, CTA 30); CTA copy shortened to one line each ("See the four-day plan, FAQs, and sign-up form." / "Not a commitment. Fees and details will follow."). No type was shrunk.

1. iPhone visibility: 8.5. Min 9.0pt, body 10.4pt, numerals 21.7pt, section heading 21pt; 0 runs under 9pt or under 4.5:1; QR decodes at phone size. 9:16 fills a phone screen exactly when opened. Deduction unchanged: smallest founder wordmarks about 7pt.
2. Centeredness: 9.0. Numeral left ink vs description left ink 0 to 1.0px (per-digit bearings corrected); numeral baseline vs title baseline 0 to 0.5px EN, CN corrected for CJK glyph bottoms; grid rows within 1px top vs bottom; outer margins equal (44px top and bottom, 54px sides); cards, facts, pills within 2px; headline left ink 54.0px.
3. Cohesiveness and flow: 8.5. Unchanged story; CTA copy now leaner. Deduction: date twice; "20+" unconfirmed.
4. Call to action: 9.0. Deduction unchanged (form position on the live page).


# Round 7 (JJ feedback, 2026-10-20)
Changes: title "AI Fundamentals: Winter Session" / 学生AI基础营·寒假班 (not "Course": CONTENT-RULES §9 bans "AI course/camp"); date moved top right as two right-aligned lines spanning the lockup's ink height (Winter break / Jan 5–8, 2027; CN 寒假 / date); section heading back to the caps label style; numerals removed, titles read "Day 1: Learn the AI tools" with "Day 1:" in --ink-2; founders label "Instructors from" / 授课老师来自; Day 4 "Present the final product to industry leaders." / 向业界人士展示最终作品。 (new claim, to confirm); "Not a commitment" line removed; QR 236 > 200px. Freed space spent on readability: lede 33 > 34px, day titles 38 > 39px, day text 29 > 29.5px (EN; CN 28 > 30), facts 33 > 36px, pills 25 > 27px, founder logos zoom 1.07 > 1.17, CTA headline 52 > 56px.

1. iPhone visibility: 9.0. Min 9.4pt (EN) / 9.8pt (CN) excluding the deliberately quiet contact line (8pt); body 10.7pt; facts 13pt; founder logos about 8pt tall now (were 7pt); QR decodes at phone size.
2. Centeredness: 9.0. Day titles and their text share one left edge (0.0 to 1.0px); top-right date ink spans the lockup's ink top to bottom within 0.6px and ends on the right margin; outer margins 45 top / 44 bottom; cards, facts, CTA within 1.5px; pills within 2px.
3. Cohesiveness and flow: 8.5. Deductions: "Winter Session" in the title and "Winter break" top right say the same thing; the date appears top right and in the When row; "industry leaders" and "20+" need confirming.
4. Call to action: 9.0. Unchanged structure; one supporting line instead of two.


# CN readability (JJ feedback, 2026-10-26), CN only, no content changes
Changes: serif kept only for the headline (学生AI基础营·寒假班) and the QR heading (扫码登记意向); day titles (600 36px) and facts values (500 33px) now PingFang; all Latin digits in CN use PingFang's own figures (fixes the bold Geist digits in 1月5日至8日); section labels 这四天里，学生会： / 授课老师来自 / 时间 地点 语言 27 > 31px. EN poster byte-identical.
Audit (audit3.py cn): min 9.8pt, body 10.5pt, 0 runs under 9pt or 4.5:1; facts rows 0.0 / 0.0 / -1.0px (时间 row nudged 1px); grid titles vs bodies within 1px; CTA text vs QR -0.2px; fixed 9:16 height holds (29px above the CTA, 44px bottom margin).


# Full-day note (JJ, 2026-10-26), EN + CN
Added under When / 时间: "Full days, about 9 a.m. to 5 p.m." / 全天，约上午9点至下午5点 (27px muted sans). Space recovered inside the fixed 9:16 frame with equal trims, no type shrunk: day cells -6px top and bottom, founders margin EN 50 > 38 / CN 38 > 30, facts margin -4px, CN facts rows -2px each. Result: EN 30px above CTA, CN 33px, 44px bottom margin both. Audit: facts rows EN 0.0 / 1.5 / 1.5, CN 0.5 / 0.0 / -1.0; min 9.4pt EN / 9.8pt CN; 0 under 9pt or 4.5:1. Pre-change snapshot: _snap-2026-10-26/.

# Full-day note, revised (JJ, 2026-10-26)
Reverted the separate line, the hours, and the spacing trims (restored _snap-2026-10-26). Now inline: "Tuesday to Friday, Jan 5–8, 2027; full days" / 1月5日至8日（周二至周五，全天）. One line each (EN 655 / CN 526 of 752px). Facts rows EN 1.5 / 1.5 / 1.5, CN 0.0 / 0.0 / -1.0; layout otherwise identical to the pre-change version.
