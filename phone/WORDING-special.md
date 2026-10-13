# Phone-only wording: special pages (40-special.js)

All swaps run only at 760px and below. Desktop copy is unchanged.

| Where | Desktop text | Phone EN | Phone CN | Why |
|---|---|---|---|---|
| /zero-to-launch #week, day labels | Day 01 … Day 07 | Day 1 … Day 7 | 第1天 … 第7天 | Plain label; the CN pages showed English "DAY 01" |
| /programs/conferences, track control (new) | Classroom practice / Teaching and assessment / Leadership and parents (h3s; CN 课堂实践 / 教学与评估 / 学校管理者与家长) | Classroom / Assessment / Leadership | 课堂实践 / 教学评估 / 管理者与家长 | Three segments must fit on one line at 360px. The full track names stay as each button's aria-label. |
| /programs/website-portfolio-workshop, swipe hint | Hover to scroll each site | Swipe to see more sites → | 左右滑动查看更多网站 → | The text was already set this way through a font-size:0 ::after trick. It is now real text (screen readers read the right thing). |
| /programs/website-portfolio-workshop, extra sample cards | (address shown in the mini browser bar) | jordanlee.site, sampatel.site, avakim.site shown as each card's title | same | The mini browser bar is hidden on phones, so the address moves into the card |

Nothing else is reworded. Text hidden on phones is listed in the builder report.
