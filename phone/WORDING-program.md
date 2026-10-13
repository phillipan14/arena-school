# Phone wording: program template + shared components (30-program.*)

Phone-only text built by `phone/30-program.js`. Desktop copy is unchanged. Everything else on phones reuses the page's own words.

| Where | Desktop (source) | Phone (EN) | Phone (CN) | Why |
|---|---|---|---|---|
| Proof row, judges | "Demo-day judges: founders and operators from these institutions and AI labs" + Harvard/Stanford/YC logos | Demo-day judges from Harvard, Stanford, Y Combinator, and AI labs | 路演评委来自哈佛、斯坦福、Y Combinator及AI实验室 | Logos are dropped from the row (no logos on a surface), so "these institutions" needs the names. Built from the logos' alt text. |
| Proof row, NPS | "9.5/10" + "NPS from 20 students" (two lines) | **9.5/10** NPS from 20 students | **9.5/10** 20名学生评出的净推荐值 | Same words, joined into one row. |
| Proof row, teacher training | "We have led hands-on work… Tsinghua University. See results →" | Row: the sentence. Row: See results › | Same, CN source | The link becomes its own row. |
| Proof rows, conferences | Event title + "Upcoming · March 17–20, 2027 · Bangkok" + description | Title, then the date line. Description dropped | Same | Short rows. The full description stays on desktop. |
| Closing row, one-pager | "Get the Arena one-pager" (form card) | Get the Arena one-pager / Every program on one page | 获取项目简介 / 所有项目一页看完 | Second line is new. The full description shows in the sheet. |
| Closing row, parent | "A parent? Tell us your school and we will reach out →" | A parent? Tell us your school | 您是家长？告诉我们孩子的学校 | Fits on one row line. |
| Closing row, partners (schools) | "Run an education company? See partnerships →" | Run an education company? See partnerships | 经营教育机构？了解机构合作 | Arrow removed (the row has a chevron). |
| Closing rows, other | "See all Arena programs →", ghost buttons ("Ask a question first", "How we work with schools", …) | Same text, no arrow | Same | Become rows with chevrons. |
| Closing pill | "Contact us →" | Contact us | 联系我们 | Arrow hidden. A pill never shows an arrow. |
| Team rows | Founder cards: name, role, credential line, expand + | Name / Co-founder › (to /about#jing-jing-yang, /about#phillip-an) | 姓名 / 联合创始人 › (to /about-cn#jing-jing-yang, /about-cn#phillip-an) | Per user: no credential text, no expanding panel on phones. |
| Team logos label (screen readers) | (none) | Where our team studied and worked | 团队曾就读和任职的机构 | aria-label on the logo scroll strip (lists every logo). |
| Sheet close | (none) | Close | 关闭 | aria-label on the sheet's × button. |
