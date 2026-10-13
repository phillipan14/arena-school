"""Build /events/* pages from the Community Dialogues template (same head assets, nav, footer)."""
import re, sys, os, html
ROOT = sys.argv[1]
E = lambda s: html.escape(s, quote=True)

PAGES = {
 'isb-parent-coffee': {
  'en': dict(title='ISB PTA Parent Coffee: Which Skills Will Matter?',
    desc='A morning conversation with ISB parents on October 14, 2026: what AI is changing about work, and why agency, taste, and craft matter. With Jing Jing Yang and Phillip An.',
    eyebrow='ISB PTA Parent Coffee',
    h1='Our Kids’ Jobs Don’t Exist Yet. So Which Skills Will Matter?',
    lede='A morning conversation with ISB parents. Jing Jing Yang (ISB Class of 2019) and Phillip An, co-founders of Arena School, share what they’ve seen, and why agency, taste, and craft matter in the age of AI.',
    facts=[('When','Wednesday, October 14'),('Time','8:30–10:00 am'),('Where','ISB Commons, International School of Beijing'),('For','ISB parents, hosted by the ISB PTA')],
    cta=[('Slides and resources','/talk',True),('Our approach','/approach',False)],
    sec_k='The conversation', sec_h='The questions we’ll answer',
    rows=[('What does “AI native” work look like in law, medicine, and finance?','How work in these fields is changing, from our team’s own experience.'),
          ('What do employers actually look for now?','What hiring teams value when AI can do the first draft.'),
          ('What can students build today?','Real projects ISB students made with AI.'),
          ('Which skills compound, and how do we grow them without adding another class?','Habits families can build at home, alongside school.')],
    end_k='After the talk', end_h='Slides and resources', end_p='The slides, PDFs, and case studies from the talk are on one page.',
    end_cta=('Open the talk resources','/talk'), end_more=('Bring a parent dialogue to your school','/programs/community-dialogues')),
  'cn': dict(title='ISB PTA 家长咖啡会：哪些能力最重要？',
    desc='2026年10月14日，面向 ISB 家长的晨间交流：AI正在如何改变工作，以及为什么主动性、审美与匠心最重要。主讲：羊筱涵、安广宁。',
    eyebrow='ISB PTA 家长咖啡会',
    h1='孩子们未来的工作还不存在，那么，哪些能力最重要？',
    lede='面向 ISB 家长的晨间交流。Arena School 联合创始人羊筱涵（ISB 2019届）与安广宁，分享亲身所见：在AI时代，真正重要的是主动性、审美与匠心。',
    facts=[('日期','10月14日（周三）'),('时间','上午8:30–10:00'),('地点','ISB Commons，北京顺义国际学校'),('对象','ISB 家长，由 ISB PTA 主办')],
    cta=[('讲座资料','/talk',True),('教学理念','/approach-cn',False)],
    sec_k='交流内容', sec_h='我们将回答的问题',
    rows=[('“AI原生”的工作，在法律、医学、金融领域是什么样子？','结合团队自身经历，看这些领域的工作正在如何变化。'),
          ('如今的雇主，真正看重的是什么？','当AI能完成初稿，招聘团队看重的又是什么。'),
          ('学生现在能做出什么？','ISB 学生借助AI做出的真实项目。'),
          ('哪些能力会持续增值？如何不多加一门课就能培养？','家庭可以在课外养成的习惯。')],
    end_k='讲座之后', end_h='幻灯片与资料', end_p='讲座的幻灯片、PDF 和案例，都在同一个页面。',
    end_cta=('查看讲座资料','/talk'), end_more=('把家长交流会带进贵校','/programs/community-dialogues-cn')),
 },
 'acamis-tech-2026': {
  'en': dict(title='ACAMIS Technology Conference 2026 Workshop: From Lab to Classroom',
    desc='A 60-minute hands-on workshop at the 2026 ACAMIS Technology Conference, Keystone Academy, Beijing: running an AI student program inside a school, with a live website build.',
    eyebrow='ACAMIS Technology Conference 2026',
    h1='From Lab to Classroom: Running an AI Student Program Inside a School',
    lede='A 60-minute hands-on workshop for teachers and tech coaches, built on a case study from the International School of Beijing.',
    facts=[('When','Sunday, October 18'),('Time','11:20 am–12:20 pm (per the agenda)'),('Where','Keystone Academy, Beijing'),('For','Teachers and tech coaches')],
    cta=[('Conference details','https://www.acamis.org/technology-conference-2026',True),('See the ISB case','/results',False)],
    sec_k='How the hour runs', sec_h='A case, the reasons it worked, and a live build',
    rows=[('The case: what students built in five days','Over five days, ISB students built working websites and apps with AI and presented them to judges from Harvard, Stanford, Y Combinator, and AI labs.'),
          ('Why it worked','The program starts from lasting skills like creativity and judgment, with AI strengthening the learning instead of replacing it.'),
          ('Build a website, live, with the room','We start from a pre-built site and add the sections and features you call out, so you see what it takes to turn ideas into a working website.'),
          ('Take it back to your school','You leave with a planning checklist and a guide to accessing AI tools on school networks.')],
    end_k='After the conference', end_h='Bring this to your school', end_p='We run hands-on AI training for teachers and help schools plan student programs like the ISB case.',
    end_cta=('AI for Educators','/programs/teacher-training'), end_more=('Talk with our team','/contact?program=conferences')),
  'cn': dict(title='ACAMIS 2026 技术大会工作坊：从实验室到课堂',
    desc='2026 ACAMIS 技术大会（北京鼎石学校）上的60分钟动手工作坊：如何在学校里开展AI学生项目，并现场搭建网站。',
    eyebrow='ACAMIS 2026 技术大会',
    h1='从实验室到课堂：如何在学校里开展AI学生项目',
    lede='一场60分钟的动手工作坊，面向教师与教育技术教练，以北京顺义国际学校（ISB）的项目为案例。',
    facts=[('日期','10月18日（周日）'),('时间','上午11:20–12:20（以大会日程为准）'),('地点','北京鼎石学校'),('对象','教师与教育技术教练')],
    cta=[('大会详情','https://www.acamis.org/technology-conference-2026',True),('查看 ISB 案例','/results-cn',False)],
    sec_k='一小时的安排', sec_h='一个案例，它为什么有效，以及现场搭建',
    rows=[('案例：学生五天做出了什么','五天里，ISB 学生借助AI做出了可用的网站和应用，并向来自哈佛、斯坦福、Y Combinator 与AI实验室的评委展示。'),
          ('为什么有效','项目从创造力、判断力等长期能力出发，让AI强化学习，而不是取代学习。'),
          ('现场和大家一起搭建网站','我们从一个预先搭好的网站出发，现场加入大家提出的板块和功能，让您亲眼看到，把想法变成可用的网站需要什么。'),
          ('带回您的学校','您将带走一份规划清单，以及在校园网络中使用AI工具的指南。')],
    end_k='大会之后', end_h='把这场工作坊带进贵校', end_p='我们为教师提供动手的AI培训，也帮助学校规划类似 ISB 案例的学生项目。',
    end_cta=('教育者AI培训','/programs/teacher-training-cn'), end_more=('联系我们的团队','/contact-cn?program=conferences')),
 },
}
SPEAKERS = {
 'en': [('Jing Jing Yang','Co-founder, Arena School. At ISB from elementary school through graduation (Class of 2019); Brown and Tsinghua; Kimi (Moonshot AI).','/about#jing-jing-yang'),
        ('Phillip An','Co-founder, Arena School. Forbes 30 Under 30 and a YC-backed founder; McKinsey and Goldman Sachs; Caltech, Harvard, and Tsinghua.','/about#phillip-an')],
 'cn': [('羊筱涵','Arena School 联合创始人。小学至高中毕业就读 ISB（2019届）；毕业于布朗、清华；曾任职于 Kimi（月之暗面）。','/about-cn#jing-jing-yang'),
        ('安广宁','Arena School 联合创始人。福布斯 30U30，YC 投资的连续创业者；曾任职于麦肯锡、高盛；毕业于加州理工、哈佛、清华。','/about-cn#phillip-an')],
}

def main_html(d, lang):
    zh = lang == 'cn'
    ext = lambda u: u.startswith('http')
    btn = lambda t,u,p: '<a href="%s" class="btn %s"%s>%s%s</a>' % (E(u), 'btn-primary' if p else 'btn-ghost', ' target="_blank" rel="noopener"' if ext(u) else '', E(t), ' <span class="arr">→</span>' if p else '')
    facts = ''.join('<li><b>%s</b><span>%s</span></li>' % (E(k), E(v)) for k,v in d['facts'])
    rows = ''.join('<li><h3>%s</h3><p>%s</p></li>' % (E(a), E(b)) for a,b in d['rows'])
    spk = ''.join('<li><h3><a class="ev-spk" href="%s">%s</a></h3><p>%s</p></li>' % (E(u), E(n), E(b)) for n,b,u in SPEAKERS[lang])
    return f'''<main id="top" class="pc pc-event">
<section class="hero hero-pad-md hero-inv pc-hero" data-screen-label="Hero">
  <div class="hero-bg" data-riso-field="static" aria-hidden="true"></div>
  <div class="container">
    <div class="hero-copy hero-copy-wide">
      <div class="hero-eyebrow-row reveal"><span class="eyebrow">{E(d['eyebrow'])}</span></div>
      <h1 class="display reveal cs-h1">{E(d['h1'])}</h1>
      <p class="lede reveal lede-56">{E(d['lede'])}</p>
      <ul class="pc-facts reveal" aria-label="{'概要' if zh else 'At a glance'}">{facts}</ul>
      <div class="pc-cta reveal">{''.join(btn(t,u,p) for t,u,p in d['cta'])}</div>
    </div>
  </div>
</section>
<section class="zl-section pc-sec pc-why" data-screen-label="Session">
  <div class="container pc-why-grid">
    <div class="sec-head reveal"><span class="eyebrow">{E(d['sec_k'])}</span><h2 class="h2 h2-md">{E(d['sec_h'])}</h2></div>
    <div class="reveal"><ul class="pc-why-list">{rows}</ul></div>
  </div>
</section>
<section class="zl-section section-alt pc-sec" data-screen-label="Speakers">
  <div class="container pc-why-grid">
    <div class="sec-head reveal"><span class="eyebrow">{'主讲' if zh else 'Speakers'}</span><h2 class="h2 h2-md">{'Arena School 两位联合创始人' if zh else 'The co-founders of Arena School'}</h2></div>
    <div class="reveal"><ul class="pc-why-list ev-speakers">{spk}</ul></div>
  </div>
</section>
<section class="zl-section pc-sec ev-end" data-screen-label="After">
  <div class="container">
    <div class="sec-head reveal"><span class="eyebrow">{E(d['end_k'])}</span><h2 class="h2 h2-md">{E(d['end_h'])}</h2><p class="pc-intro">{E(d['end_p'])}</p></div>
    <div class="pc-cta reveal ev-end-cta">{btn(d['end_cta'][0], d['end_cta'][1], True)}<a class="tlink" href="{E(d['end_more'][1])}">{E(d['end_more'][0])} →</a></div>
  </div>
</section>
</main>'''

for slug, langs in PAGES.items():
    for lang, d in langs.items():
        zh = lang == 'cn'
        tpl = open(os.path.join(ROOT, 'programs', 'community-dialogues%s.html' % ('-cn' if zh else ''))).read()
        # strip markup our scripts add; they re-add it
        tpl = re.sub(r'\n?<link rel="stylesheet" href="/(phone|newsletter)\.css[^"]*" data-(phone|nl)>', '', tpl)
        tpl = re.sub(r'\n?<script src="/newsletter\.js[^"]*" defer data-nl></script>', '', tpl)
        tpl = re.sub(r'\n?<!-- phone:start -->.*?<!-- phone:end -->', '', tpl, flags=re.S)
        path = '/events/%s%s' % (slug, '-cn' if zh else '')
        other = '/events/%s%s' % (slug, '' if zh else '-cn')
        t = tpl
        t = re.sub(r'<title>.*?</title>', '<title>%s · Arena School</title>' % E(d['title']), t, count=1)
        t = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+E(d['desc'])+m.group(2), t, count=1)
        t = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1)+E(d['desc'])+m.group(2), t, count=1)
        t = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1)+E(d['title'])+' · Arena School'+m.group(2), t, count=1)
        t = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1)+'https://arenaschool.org'+path+m.group(2), t, count=1)
        t = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1)+'https://arenaschool.org'+path+m.group(2), t, count=1)
        # language switch points at the twin page
        t = re.sub(r'(<div class="lang-switch".*?</div>)', lambda m: m.group(1).replace('/programs/community-dialogues-cn', other if not zh else path).replace('/programs/community-dialogues"', (path if not zh else other)+'"'), t, count=1, flags=re.S)
        # no nav item is "current" on an event page
        t = t.replace(' aria-current="page"', '').replace('nav-dd is-current', 'nav-dd')
        t = t.replace('</head>', '<style>@media (min-width:761px){.pc-event .pc-facts{grid-template-columns:repeat(4,minmax(0,1fr)) !important}.pc-event .pc-facts li span,.pc-event .pc-facts li b{white-space:normal !important}}</style>\n</head>', 1)
        i, j = t.find('<main'), t.find('</main>') + len('</main>')
        t = t[:i] + main_html(d, lang) + t[j:]
        os.makedirs(os.path.join(ROOT, 'events'), exist_ok=True)
        open(os.path.join(ROOT, path.lstrip('/') + '.html'), 'w').write(t)
        print('wrote', path)
