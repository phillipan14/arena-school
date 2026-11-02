#!/usr/bin/env python3
"""AI Fundamentals for Students @ International School of Beijing: parent-group poster v3 (EN + CN).
Aligned with Phillip's Oct 16 "pro system" (DESIGN.md): white page, cool #F5F7FA hero band, navy ink,
Newsreader headings + Geist body, caps labels in --ink-2 (no chips), hairline cards, grayscale logos,
one navy closing band. Name per CONTENT-RULES §9. Render: python3 ../render.py (see render3.py)."""
TOOLS = ['openai', 'claude', 'deepseek', 'perplexity', 'cursor', 'kimi', 'github', 'vercel',
         'figma', 'canva', 'ideogram', 'midjourney', 'capcut', 'suno', 'elevenlabs']
SCHOOLS = [('caltech', 'Caltech', 30), ('harvard', 'Harvard University', 38), ('brown', 'Brown University', 38),
           ('tsinghua-lockup', 'Tsinghua University', 42), ('isb', 'International School of Beijing', 44)]
COS = [('mckinsey', 'McKinsey & Company', 19), ('goldman', 'Goldman Sachs', 31), ('apple', 'Apple', 33),
       ('microsoft-ai', 'Microsoft AI', 26), ('deloitte', 'Deloitte', 19), ('kimi-wordmark', 'Kimi (Moonshot AI)', 20)]

C = {
 'en': dict(lang='en', title='AI Fundamentals for Students @ International School of Beijing',
  eyebrow='Winter break<br>Jan 5–8, 2027',
  h1='AI Fundamentals: <em>Winter Course</em>', h1b='',
  lede='Four days to build AI fluency and future-proof skills:<br>master the newest AI tools and launch an AI-native product.',
  days_k='Over four days, students will:',
  days=[('<span class="dl">Day 1:</span> Learn the AI tools', '20+ professional tools for research, design, code, and video.'),
        ('<span class="dl">Day 2:</span> Build and test', 'Pick a project, talk to real users, and improve each version.'),
        ('<span class="dl">Day 3:</span> Prepare the pitch', 'Polish the product and shape the story behind it.'),
        ('<span class="dl">Day 4:</span> Launch and present', 'Present the final product to industry leaders.')],
  tags=['Four days', 'Grades 6–12', 'All schools welcome', 'No coding needed'],
  open_k='',
  open_b='You don’t need to be a STEM student.',
  open_p='Students who love art, music, writing, sports, or business are just as welcome. Every interest has something to make with AI.',
  do_k='What students do',
  do=[('01 · Learn', 'AI tools, on their own project', 'Professional tools for research, design, code, and video.', True),
      ('02 · Choose', 'A project worth making', 'A sport, a cause, a hobby, or a subject they love.', False),
      ('03 · Finish', 'Something real', 'A working version anyone can test, presented on day four.', False)],
  f_k='Instructors from',
  facts=[('When', 'Tuesday to Friday, Jan 5–8, 2027; full days'), ('Where', 'International School of Beijing'),
         ('Language', 'English, with Chinese support')],
  cta_k='Next step', cta_h='Scan to <em>register interest.</em>',
  cta_p='See the four-day plan and sign-up form.',
  cta_n='Not a commitment. Fees and details will follow.', qr='qr-en.png', hold='Press and hold to scan'),
 'cn': dict(lang='zh-CN', title='学生AI基础营 · 北京顺义国际学校',
  eyebrow='寒假<br><span class="lat">2027</span>年<span class="lat">1</span>月<span class="lat">5</span>日至<span class="lat">8</span>日',
  h1='学生<em>AI基础营</em><span class="mid">·</span>寒假班', h1b='',
  lede='<span class="nw">四天培养AI素养和面向未来的能力：</span><br><span class="nw">掌握最新的AI工具，做出自己的AI原生产品。</span>',
  days_k='这四天里，学生会：',
  days=[('<span class="dl">第一天：</span>学会AI工具', '<span class="nw">20多款专业AI工具，</span><br><span class="nw">覆盖调研、设计、编程和视频。</span>'),
        ('<span class="dl">第二天：</span>动手做，找人试', '<span class="nw">选定项目，访谈真实用户，</span><br><span class="nw">一版一版改进。</span>'),
        ('<span class="dl">第三天：</span>准备路演', '完善产品，理清背后的故事。'),
        ('<span class="dl">第四天：</span>上线与展示', '向业界人士展示最终作品。')],
  tags=['四天', '初高中学生', '不限学校', '无需编程基础'],
  open_k='',
  open_b='不是理科生，也完全可以。',
  open_p='喜欢艺术、音乐、写作、体育或商业的学生，同样欢迎。无论什么兴趣，都能用AI做出东西。',
  do_k='学生会做什么',
  do=[('01 · 学', '在自己的项目上学AI工具', '调研、设计、编程和视频，都用专业人士在用的工具。', True),
      ('02 · 选', '选一个值得做的项目', '一项运动、一个公益议题、一个爱好，或一门喜欢的学科。', False),
      ('03 · 做', '真正做出来', '做出人人都能试用的版本，并在第四天上台展示。', False)],
  f_k='授课老师来自',
  facts=[('时间', '<span class="lat">1</span>月<span class="lat">5</span>日至<span class="lat">8</span>日（周二至周五，全天）'), ('地点', '北京顺义国际学校'),
         ('语言', '英文授课，提供中文支持')],
  cta_k='下一步', cta_h='扫码<em>登记意向</em>',
  cta_p='查看四天安排、常见问题和报名表。',
  cta_n='登记意向不代表报名，费用等详情另行发送。', qr='qr-cn.png', hold='长按识别二维码'),
}


def logos(row, lang):
    if lang == 'cn':
        row = [('goldman-cn', 'Goldman Sachs 高盛', 27) if f == 'goldman' else (f, a, h) for f, a, h in row]
    return '<div class="lg">' + ''.join(f'<img src="cred/{f}.png" alt="{a}" style="height:{h}px">' for f, a, h in row) + '</div>'


for L, c in C.items():
    tags = ''.join(f'<span class="tag">{t}</span>' for t in c['tags'])
    tools = '<div class="tools">' + ''.join(f'<img src="tools/{t}.png" alt="">' for t in TOOLS) + '</div>'
    days = ''.join(f'<li><b>{b}</b><p>{p}</p></li>' for i, (b, p) in enumerate(c['days']))
    do = ''.join(f'<div class="do"><span class="k">{k}</span><b>{b}</b><p>{p}</p>{tools if t else ""}</div>' for k, b, p, t in c['do'])
    facts = ''.join(f'<div class="fr"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in c['facts'])
    html = f'''<!doctype html>
<html lang="{c['lang']}"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<title>{c['title']}</title>
<link rel="stylesheet" href="/fonts/fonts.css"><link rel="stylesheet" href="v3.css"></head>
<body class="{L}"><div class="poster" id="poster">
  <header class="hero">
    <div class="top"><img class="lockup" src="lockup.png" alt="Arena School, www.arenaschool.org"><span class="k when">{c['eyebrow']}</span></div>
    <hr class="rule">
    <h1>{c['h1']}</h1>
    <p class="lede">{c['lede']}</p>
    <div class="tags">{tags}</div>
  </header>
  <main class="body">
    <section class="week"><span class="k wh">{c['days_k']}</span><ol class="grid4">{days}</ol></section>
    <hr class="navy">
    <section class="card founders"><span class="k">{c['f_k']}</span><div class="lwall">{logos(SCHOOLS, L)}{logos(COS, L)}</div></section>
    <section class="facts">{facts}</section>
    <section class="cta">
      <div class="ct"><h2>{c['cta_h']}</h2><p>{c['cta_p']}</p><p class="ct-links"><span>arenaschool.org</span><i aria-hidden="true">·</i><span>contact@arenaschool.org</span></p></div>
      <div class="qw"><div class="qr"><img src="{c['qr']}" alt="QR code to the program page"></div><span class="hold">{c['hold']}</span></div>
    </section>
  </main>
</div></body></html>'''
    open(f'{L}.html', 'w').write(html)
print('built en.html cn.html')
