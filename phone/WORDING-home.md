# Homepage phone wording changes (20-home.css / 20-home.js)

Phone only (≤760px). Desktop text is unchanged. No HTML file was edited.

| Where | Desktop | Phone | Why |
|---|---|---|---|
| Grade map axis, last column (EN) | "After high school" (stage) over "College" (tick) | "College" only, used as the stage label | "After high school" wrapped to 3 lines in a 55px column. The column's existing "College" tick moves up into the stage row. "After high school" stays in the DOM, pushed out of view with text-indent. |
| Grade map axis, last column (CN) | 毕业后 over 大学 | 大学 only | Same structure as EN |
| Program links, grade-map lanes, events, "See how we partner", "Read our approach", email/LinkedIn | trailing "→" | trailing iOS chevron | The arrow text is kept but hidden (.ph-arr) |
| Upcoming events | "Program details →" / "Conferences & events →" inline link in each description | not shown; the whole row is the link | It repeated the row's destination. The link stays in the DOM, set to font-size 0, and its ::after covers the whole row. |
| Pillars I/II/III | buttons that expand an inline panel | rows that link to /approach#agency, #taste, #craft (CN: /approach-cn#…) | User: no big expansions on phones. The panel is display:none on phones, and /approach has the full text. |

The hero eyebrow is not handled here. The lead owns the hero and removes that chip on phones.
