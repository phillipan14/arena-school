"""Arena School one-pagers, v3 (ONEPAGER2-BRIEF and UPDATES 1 to 4, Oct 17, 2026): general, teacher, parent; EN + CN.

Outputs (A4, exactly one page each; the general one keeps its old paths so onepager.js and every link keep working):
  onepager/arena-school-one-pager-{en,cn}.pdf          general
  onepager/arena-school-teacher-one-pager-{en,cn}.pdf  teachers and school leaders
  onepager/arena-school-parent-one-pager-{en,cn}.pdf   families
  + a 520px .jpg thumbnail next to each PDF; HTML sources in tools/one-pager/
The build fails unless each PDF is one page, nothing is taller than the page, every grid item's left and right edges sit
on the 12-column grid, cards in a row have equal heights, and no text is under 7pt (checked in the browser).

Layout: one 12-column grid (10mm side margins, 4mm gutters) on every row; thirds, halves and quarters only; numbered
section headers in one position. Offer and proof are one section (UPDATES 3 and 4): abstracted audience tiles (icon,
short label, one line, formats in a few words; no grades, dates or program names) with a proof line of real partner
logos from the repo and a 3 to 5 word caption (a plain text label where no logo file exists; never a recreated logo).
Diagrams: the learning wheel, the fluency staircase, the mentorship ladder, a personal vs school account pair.
Copy: the site's own sources (tools/approach_page.py, tools/fluency_section.py, tools/data_section.py, the program pages,
PAST-TALKS-SOURCES.md). No stats, no ISB numbers, no em dashes. CN marked for JJ review. Changes: ONEPAGER-CHANGES.md.
  python3 tools/one-pager/build.py [general|teacher|parent ...] [--dir A|B|C] [--png DIR]   (B is the chosen direction)   (needs the local server on 127.0.0.1:8931)
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import approach_page as A  # noqa: E402
import approach_wheel as W  # noqa: E402
import data_section as DS  # noqa: E402
import fluency_section as FL  # noqa: E402

ICONS = json.load(open(os.path.join(ROOT, 'tools', 'lucide_icons.json')))['icons']


def ic(name, cls='ic'):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true">%s</svg>' % (cls, ICONS[name]))


# real partner marks in the repo (logo file) or a text label where none exists
LOGO = {'isb': ('/logos/cred/isb.png', 6.4), 'tsinghua': ('/logos/cred/tsinghua-lockup.png', 6.4), 'pta': ('/decks/img/conversation/pta-logo.png', 6.2),
        'lux': ('/logos/lux/lux-navy-horizontal.png', 6.6), 'bodley': (None, 'Bodley Academy'), 'acamis': (None, 'ACAMIS')}

L = {
 'en': dict(
   member='A member of', anth='Startup Program', oai='Partner Network', studied='Our team studied at', worked='Our team worked at',
   web='arenaschool.org', mail='phillip@arenaschool.org', proof='Run with',
   # audience tiles: key -> (icon, label, one line, formats, [proof marks], proof caption)
   T={'students': ('graduation-cap', 'Students', 'Build and launch real products with AI.', 'Workshops · mentorship', ['isb', 'bodley'], 'Five-day student programs'),
      'schools': ('school', 'Educators', 'Make the tools classes need, inside school rules.', 'Sessions · workshops', ['tsinghua'], 'Staff training, Schwarzman College'),
      'families': ('heart-handshake', 'Families', 'One project with a mentor, and parent talks.', '1:1 mentorship · parent talks', ['pta'], 'Parent talk, ISB PTA'),
      'career': ('briefcase', 'Career', 'Launch a live AI product, ready for work.', 'Bootcamp', ['lux'], 'Jointly hosted with Lux Scholar'),
      # teacher variant
      'teachers': ('wrench', 'Teachers', 'Make the tool your class is missing.', 'Session · workshop · school-wide', ['tsinghua'], 'Staff training, Schwarzman College'),
      'tech': ('monitor-cog', 'Tech teams', 'Training on your approved systems.', 'Planning · sessions', [], ''),
      'leaders': ('building-2', 'School leaders', 'Programs for the whole school community.', 'Planned with your team', ['isb'], 'Student program on campus'),
      'conf': ('mic', 'Conferences', 'Talks and hands-on workshops.', 'Keynote · workshop · panel', ['acamis'], 'Next: ACAMIS workshop'),
      # parent variant
      'workshops': ('smartphone', 'Workshops', 'Rebuild an app, or build a portfolio site.', 'At your child’s school', [], ''),
      'intensive': ('rocket', 'Intensives', 'Teams launch a real product and pitch it.', 'With mentors in the room', ['isb', 'bodley'], 'Five-day student programs'),
      'mentor': ('route', 'Mentorship', 'One project, 1:1, at their own pace.', 'Weekly check-ins, hybrid', ['isb'], 'ISB alumni continue here'),
      'talks': ('messages-square', 'Parent talks', 'How AI is changing work and college.', 'At your child’s school', ['pta'], 'Parent talk, ISB PTA')},
   formats_k='Formats',
   skills=[('compass', 'Agency', 'Choose what is worth doing.'), ('search-check', 'Taste', 'Judge whether it is actually good.'), ('badge-check', 'Craft', 'Finish it so people can trust it.')],
   loop='Learners decide. AI builds. Real people judge.', strands_k='Four strands, assessed on every project',
   dk='Whose account is it?', personal='Personal account', school='School-approved platform',
   prow=['Consumer terms', 'No data agreement', 'Not for student data'], srow=['Enterprise agreement', 'Agreed by the school', 'Approved for student data'],
   cta='Bring Arena to your school.', ctap='Planned with your team, run on your campus. Your teachers keep the materials.',
   hub='Arena School',
 ),
 'cn': dict(
   member='成员计划', anth='初创企业计划', oai='合作伙伴网络', studied='团队就读于', worked='团队曾任职于',
   web='arenaschool.org', mail='phillip@arenaschool.org', proof='合作',
   T={'students': ('graduation-cap', '学生', '借助AI做出并上线真实的产品。', '工作坊 · 集训营 · 导师计划', ['isb', 'bodley'], '五天学生项目'),
      'schools': ('school', '教师与学校', '在学校规则之内，做出课堂需要的工具。', '分享 · 工作坊 · 全校培训', ['tsinghua'], '苏世民书院教职员工培训'),
      'families': ('heart-handshake', '家庭', '与导师一起完成一个项目，以及家长讲座。', '一对一导师 · 家长讲座', ['pta'], 'ISB PTA 家长讲座'),
      'career': ('briefcase', '大学与职场', '做出上线的AI产品，为工作做好准备。', '训练营', ['lux'], '与千麓学者联合举办'),
      'teachers': ('wrench', '教师', '为课堂做一个正缺的小工具。', '现场分享 · 工作坊 · 全校培训', ['tsinghua'], '苏世民书院教职员工培训'),
      'tech': ('monitor-cog', '技术团队', '在学校认可的系统上开展培训。', '规划 · 培训', [], ''),
      'leaders': ('building-2', '校长与管理层', '服务整个学校社群的项目。', '与贵校团队共同规划', ['isb'], '在校园内开展的学生项目'),
      'conf': ('mic', '会议与活动', '主题演讲与动手工作坊。', '演讲 · 工作坊 · 圆桌', ['acamis'], '即将举行：ACAMIS 工作坊'),
      'workshops': ('smartphone', '动手工作坊', '重做一款应用，或做一个作品集网站。', '在孩子的学校', [], ''),
      'intensive': ('rocket', '集训营', '团队做出真实的产品并路演。', '导师全程在场', ['isb', 'bodley'], '五天学生项目'),
      'mentor': ('route', '学年导师计划', '一个项目，一对一，按自己的节奏。', '每周例会，线上线下结合', ['isb'], 'ISB 营员在此继续'),
      'talks': ('messages-square', '家长讲座', 'AI如何改变工作与升学。', '在孩子的学校', ['pta'], 'ISB PTA 家长讲座')},
   formats_k='形式',
   skills=[('compass', '主动性', '选出值得做的事。'), ('search-check', '审美', '判断它是否真的好。'), ('badge-check', '匠心', '把它做好做完，让人信得过。')],
   loop='学习者做决定，AI动手做，真实的人来评判。', strands_k='四条学习主线，每个项目都评估',
   dk='这是谁的账号？', personal='个人账号', school='学校认可的平台',
   prow=['面向消费者的条款', '与学校没有数据协议', '不可用于学生数据'], srow=['企业协议', '由学校签订', '获准用于学生数据'],
   cta='把 Arena 带进贵校。', ctap='与贵校团队共同规划，在贵校校园开展。老师们保留全部材料。',
   hub='Arena School',
 ),
}
LOGO_CN = {'bodley': 'Bodley Academy', 'acamis': 'ACAMIS'}

DOCS = {
 'general': dict(file='arena-school-one-pager', tiles=['students', 'schools', 'families', 'career'],
   en=dict(eyebrow='What is Arena School', h1='Hands-on programs that help students, families, educators, and schools <em>thrive in the age of AI.</em>'),
   cn=dict(eyebrow='认识 Arena School', h1='动手实践的项目，陪伴学生、家庭、教育者与学校，<em>从容走进AI时代。</em>')),
 'teacher': dict(file='arena-school-teacher-one-pager', tiles=['teachers', 'tech', 'leaders', 'conf'],
   en=dict(eyebrow='For teachers and school leaders', h1='AI fluency for the whole staff, <em>inside your school’s rules.</em>'),
   cn=dict(eyebrow='面向教师与学校管理层', h1='全体教职员工的AI素养，<em>始终在学校的规则之内。</em>')),
 'parent': dict(file='arena-school-parent-one-pager', tiles=['workshops', 'intensive', 'mentor', 'talks'],
   en=dict(eyebrow='For families', h1='What your child makes, learns, and keeps <em>at Arena School.</em>'),
   cn=dict(eyebrow='写给家长', h1='孩子在 Arena School <em>做什么、学什么、带走什么。</em>')),
}
STUDIED = [('caltech', 3.2), ('harvard', 4.4), ('brown', 5.2), ('tsinghua-lockup', 4.6), ('isb', 4.6)]
WORKED = [('mckinsey', 2.6), ('goldman', 4.0), ('yc', 3.8), ('apple', 4.0), ('microsoft-ai', 3.2), ('deloitte', 2.7), ('kimi-wordmark', 2.8)]

S = {
 'en': dict(who='Who we serve, and where we’ve run it', who_t='Who we work with, and where we’ve run it', who_p='What your child can do, and where we’ve run it',
            teach='How we teach', learn='How your child learns', fluency='Staff AI fluency', fluency_s='Five levels; every teacher moves up one a term',
            data='Student data first', guard='Student data guardrails', safe='Safety and student data',
            move='How a teacher moves up one level', outcomes='Learning outcomes', tools='Tools teachers made', tools_by='Made by Ben, an English teacher at Shanghai American School (SAS)',
            ladder='Year-long mentorship: the milestone ladder'),
 'cn': dict(who='我们服务谁，在哪里开展过', who_t='我们与谁合作，在哪里开展过', who_p='孩子可以做什么，我们在哪里开展过',
            teach='我们如何教', learn='孩子如何学习', fluency='教职员工AI素养', fluency_s='五个层级，每位老师每学期提升一级',
            data='学生数据放在第一位', guard='学生数据保护规则', safe='安全与学生数据',
            move='老师如何提升一级', outcomes='学习成果', tools='老师们做的工具', tools_by='由上海美国学校（SAS）英文老师 Ben 制作',
            ladder='学年项目导师计划：里程碑'),
}
X = {
 'en': dict(
   move=[('book-open', 'Before', 'Each teacher brings one task from a class they teach now.'), ('presentation', 'Show', 'We make one tool live from a plain-language description.'),
         ('hammer', 'Make', 'Each teacher makes theirs on your approved tools and checks every result.'), ('check', 'Keep', 'Teachers keep the tool and the prompt, to reuse and share.')],
   tools=[('file-text', 'Poem annotator', 'Literary devices marked in a poem’s margin.'), ('list-checks', 'Who is missing what', 'Which students are missing which piece of knowledge.'),
          ('pen-line', 'Feedback helper', 'Comment ideas against your own rubric; you edit each one.')],
   model=[('list-checks', 'Baseline', 'A short self-assessment places every teacher.'), ('users', 'One level up', 'Each group trains up one level.'),
          ('search-check', 'Each term', 'Re-measure, so leaders see the curve shift.'), ('user-check', 'Coaches', 'Level 5 teachers coach colleagues.')],
   ladder=['Launch', 'Traction', 'Revenue', 'Impact', 'Recognition'], ladder_d=['A working product at a public link', 'Users from outside their circle', 'First income from paying users', 'Many users, press, or a final', 'A national win, or a company'],
   ladder_l='Each student sets a target with their mentor, then moves up at their own pace, judged on the work.',
   mfacts=[('calendar', 'Weekly', '25-minute check-ins, hybrid'), ('users', 'Solo or a team', 'Up to four students'), ('flag', 'Start', 'Rolling'), ('repeat', 'Length', 'Six months to a year')]),
 'cn': dict(
   move=[('book-open', '培训前', '每位老师带来自己正在教的一门课里的一项任务。'), ('presentation', '演示', '我们现场演示，从一段文字描述做出一个工具。'),
         ('hammer', '动手', '每位老师用学校认可的工具做出自己的版本，并检查每个结果。'), ('check', '带走', '老师留下工具和背后的提示词，可反复使用和分享。')],
   tools=[('file-text', '诗歌批注', '在诗歌旁边标出修辞手法。'), ('list-checks', '谁还没掌握哪个知识点', '一眼看出哪些学生还没掌握哪个知识点。'),
          ('pen-line', '评语助手', '按您的评分标准给出评语建议，每条都由您修改。')],
   model=[('list-checks', '基线', '简短的自我评估确定每位老师的层级。'), ('users', '各升一级', '每组老师提升一级。'),
          ('search-check', '每学期', '重新评估，让管理层看到曲线移动。'), ('user-check', '教练', '第五层级的老师带动同事。')],
   ladder=['上线', '用户增长', '收入', '影响力', '认可'], ladder_d=['可用的产品，发布在公开网址', '来自自己圈子以外的用户', '第一笔付费收入', '大量用户、媒体报道或进入决赛', '全国性比赛获奖，或注册公司'],
   ladder_l='每名学生和导师定好目标，按自己的节奏一级级往上走，看的是做出来的成果。',
   mfacts=[('calendar', '每周', '25分钟例会，线上线下结合'), ('users', '单人或团队', '4人以内'), ('flag', '开始', '滚动入学'), ('repeat', '周期', '六个月到一年')]),
}


# ---------------------------------------------------------------- v4 (ONEPAGER3-BRIEF): three strong sections per variant
INTRO = {
 'general': {'en': 'When AI can make almost anything, learners need to know what is worth making, whether it is good, and how to finish it.',
             'cn': '当AI几乎什么都能做出来，学习者需要知道什么值得做、做得好不好，以及怎样把它做完。'},
 'teacher': {'en': 'A few early adopters are already there. We bring the rest of your staff up, one level at a time, safely.',
             'cn': '少数老师已经走在前面。我们帮助其余教职员工一级一级、安全地跟上。'},
 'parent': {'en': 'Hands-on programs where your child builds something real with AI, with mentors beside them.',
            'cn': '动手实践的项目：孩子在导师陪伴下，借助AI做出真实的作品。'},
}
H1 = {'general': DOCS['general'],
      'teacher': {'en': dict(eyebrow='For teachers and school leaders', h1='AI fluency for the whole staff, <em>inside your school’s rules.</em>'),
                  'cn': dict(eyebrow='面向教师与学校管理层', h1='全体教职员工的AI素养，<em>始终在学校的规则之内。</em>')},
      'parent': {'en': dict(eyebrow='For families', h1='What your child <em>makes, learns and keeps.</em>'),
                 'cn': dict(eyebrow='写给家长', h1='孩子在这里<em>做什么、学什么、带走什么。</em>')}}
CAP = {'en': 'Demo day, Beijing, 2026', 'cn': '路演日，北京，2026年'}
# section titles: (title, one-line dek)
SEC = {
 'en': dict(who=('Who we serve', 'And where we have run it.'), teach=('How we teach', 'One framework in every program.'),
            data=('Student data comes first', 'Before which tool, ask whose account it is.'),
            fl=('Five levels of AI fluency', 'Every teacher moves up one level a term.'), move=('Moving up a level', 'One session, one task from a real class.'),
            kids=('What your child does', 'And where we have run it.'), ladder=('The milestone ladder', 'Year-long mentorship, judged on the work.'),
            safe=('Safety and student data', 'Student data stays in accounts the school approves.')),
 'cn': dict(who=('我们服务谁', '以及我们在哪里开展过。'), teach=('我们如何教', '一套框架贯穿每个项目。'),
            data=('学生数据放在第一位', '先别问用哪个工具，先问是谁的账号。'),
            fl=('AI素养的五个层级', '每位老师每学期提升一级。'), move=('如何提升一级', '一次培训，一项真实课堂里的任务。'),
            kids=('孩子可以做什么', '以及我们在哪里开展过。'), ladder=('里程碑', '学年项目导师计划，看做出来的成果。'),
            safe=('安全与学生数据', '学生数据只放在学校认可的账号里。')),
}
# proof marks normalized to one optical height (mm) inside a 7mm slot; text labels in the same serif, no box
PROOF_H = {'isb': 5.0, 'tsinghua': 5.0, 'pta': 4.8, 'lux': 5.2}


def header(lang, d):
    t = H1[d][lang]
    return ('<header class="top"><div class="g12 topgrid"><div class="c1-7 top-copy">'
            '<img class="wm" src="/logos/arena/wordmark-ivory-1600.png" alt="Arena School" />'
            '<span class="eyebrow">%s</span><h1>%s</h1><p class="lede">%s</p></div></div>'
            '<figure class="photo"><img src="/photos/isb-2026/pitch-duo-1600.webp" alt="" /><figcaption>%s</figcaption></figure></header>'
            % (t['eyebrow'], t['h1'], INTRO[d][lang], CAP[lang]))


def strip(lang):
    """Bottom credentials: three rows, each on one line, labels in columns 1 to 3."""
    c = L[lang]
    lg = lambda items: ''.join('<img src="/logos/cred/%s.png" alt="" style="height:%smm" />' % (k, h) for k, h in items)
    return ('<section class="strip">'
            '<div class="g12 row"><span class="c1-3 lab">%s</span><div class="c4-12 logos member">'
            '<span class="m"><img src="/logos/partners/anthropic.svg" alt="Anthropic" style="height:2.6mm" /><em>%s</em></span>'
            '<span class="m"><img src="/logos/partners/openai.svg" alt="OpenAI" style="height:4.8mm" /><em>%s</em></span></div></div>'
            '<div class="g12 row"><span class="c1-3 lab">%s</span><div class="c4-12 logos">%s</div></div>'
            '<div class="g12 row"><span class="c1-3 lab">%s</span><div class="c4-12 logos">%s</div></div></section>'
            % (c['member'], c['anth'], c['oai'], c['studied'], lg(STUDIED), c['worked'], lg(WORKED)))


def shead(n, key, lang, span='c1-12'):
    t, d = SEC[lang][key]
    return ('<div class="sh %s"><span class="num">%02d</span><div class="sht"><h2>%s</h2><p>%s</p></div></div>' % (span, n, t, d))


def sec(n, key, lang, inner, cls=''):
    return '<section class="sec %s"><div class="g12">%s</div>%s</section>' % (cls, shead(n, key, lang), inner)


def mark(k):
    f, v = LOGO[k]
    return ('<img src="%s" alt="" style="height:%smm" />' % (f, PROOF_H[k])) if f else '<span class="wordmark">%s</span>' % v


FACT = {'workshops': {'en': ('2 days', 'At your school, no coding needed'), 'cn': ('两天', '在贵校进行，无需编程基础')},
        'tech': {'en': ('Your systems', 'Locked down is fine'), 'cn': ('贵校的系统', '严格管控的环境也可以')}}


def tiles(lang, keys):
    c = L[lang]
    spans = ['c1-3', 'c4-6', 'c7-9', 'c10-12']
    out = []
    for s, k in zip(spans, keys):
        icon, label, line, fm, marks, cap = c['T'][k]
        if marks:
            pr = '<div class="proof"><div class="marks">%s</div><span class="cap">%s</span></div>' % (''.join(mark(m) for m in marks), cap)
        elif k in FACT:   # no verified past run with a logo: a site fact in the same slot (never an invented proof)
            pr = '<div class="proof"><div class="marks"><span class="fact">%s</span></div><span class="cap">%s</span></div>' % FACT[k][lang]
        else:
            pr = '<div class="proof empty"><div class="marks"></div><span class="cap">&nbsp;</span></div>'
        out.append('<div class="%s card tile"><div class="th">%s<b class="nm">%s</b></div><span class="out">%s</span><span class="fm">%s</span>%s</div>' % (s, ic(icon, 'ic big'), label, line, fm, pr))
    return '<div class="g12 rrow">%s</div>' % ''.join(out)


def teach(lang, wide=True):
    c, t = L[lang], A.T['cn' if lang == 'cn' else 'en']
    dom = ['target', 'search-check', 'hammer', 'messages-square']
    skills = ''.join('<div class="%s sk"><div class="skh">%s<b>%s</b></div><span>%s</span></div>' % (sp, ic(i), a, b)
                     for sp, (i, a, b) in zip(['c4-6', 'c7-9', 'c10-12'], c['skills']))
    strands = ''.join('<div class="%s st">%s<span>%s</span></div>' % (sp, ic(dom[k]), d)
                      for k, (sp, d) in enumerate(zip(['c1-3', 'c4-6', 'c7-9', 'c10-12'], t['domains'])))
    return ('<div class="g12 teach"><div class="c1-3 wheel">%s</div><div class="c4-12 loopc"><p class="loop">%s</p></div>%s</div>'
            '<div class="g12 strandk"><span class="c1-12 k">%s</span></div><div class="g12 strow">%s</div>'
            % (W.svg('cn' if lang == 'cn' else 'en'), c['loop'], skills, c['strands_k'], strands))


def stairs(items, descs=True):
    steps = ''.join('<li style="--s:%d"><i>%d</i><b>%s</b></li>' % (i, i + 1, n) for i, (n, _) in enumerate(items))
    below = ''.join('<span>%s</span>' % d for _, d in items) if descs else ''
    return '<div class="stairs-wrap"><ol class="stairs">%s</ol><div class="stairs-d">%s</div></div>' % (steps, below)


def row4(items, cls='row4'):
    spans = ['c1-3', 'c4-6', 'c7-9', 'c10-12']
    return '<div class="g12 %s">%s</div>' % (cls, ''.join('<div class="%s it">%s<div><b>%s</b><span>%s</span></div></div>' % (s, ic(i), a, b) for s, (i, a, b) in zip(spans, items)))


def account(lang):
    c = L[lang]
    col = lambda title, rs, ok: ('<div class="acc %s"><div class="acch">%s<b>%s</b></div><ul>%s</ul></div>'
                                 % ('ok' if ok else 'no', ic('school' if ok else 'user-round', 'ic big'), title, ''.join('<li>%s%s</li>' % (ic('check' if ok else 'x', 'mk'), r) for r in rs)))
    return '<div class="pair">%s<span class="vs">vs</span>%s</div>' % (col(c['personal'], c['prow'], False), col(c['school'], c['srow'], True))


def commits(lang, pick):
    d = DS.C['cn' if lang == 'cn' else 'en']
    return '<ul class="commit">%s</ul>' % ''.join('<li>%s<b>%s</b></li>' % (ic(d['commit'][k][0]), d['commit'][k][1]) for k in pick)


def data(lang, pick=(0, 1, 2, 4)):
    """Account cards on columns 1-3 and 4-6 (vs badge centred in the gutter), commitments on 7-12, tops and bottoms aligned."""
    c = L[lang]
    col = lambda span, title, rs, ok: ('<div class="%s acc %s"><div class="acch">%s<b>%s</b></div><ul>%s</ul>%s</div>'
                                       % (span, 'ok' if ok else 'no', ic('school' if ok else 'user-round', 'ic big'), title,
                                          ''.join('<li>%s%s</li>' % (ic('check' if ok else 'x', 'mk'), r) for r in rs), '' if ok else '<span class="vs">vs</span>'))
    return ('<div class="g12 data">%s%s<div class="c7-12">%s</div></div>'
            % (col('c1-3', c['personal'], c['prow'], False), col('c4-6', c['school'], c['srow'], True), commits(lang, pick)))


PCTA = {'en': ('Two ways to start.', 'Ask your child’s school to bring Arena, or enroll in the Year-Long Project Mentorship directly.'),
        'cn': ('两种开始方式。', '请孩子的学校邀请 Arena，或直接报名学年项目导师计划。')}


def footer(lang, doc='general'):
    c = L[lang]
    h, p = PCTA[lang] if doc == 'parent' else (c['cta'], c['ctap'])
    return ('<footer class="cta g12"><div class="c1-8"><h2>%s</h2><p>%s</p></div><div class="c9-12 contact"><b>%s</b><span>%s</span></div></footer>'
            % (h, p, c['mail'], c['web']))


def general(lang, d):
    if d == 'C':   # magazine: section 1 full width, 2 and 3 side by side
        return (sec(1, 'who', lang, tiles(lang, DOCS['general']['tiles'])) +
                '<section class="sec"><div class="g12 halves"><div class="c1-6">%s%s</div><div class="c7-12">%s%s%s</div></div></section>'
                % ('<div class="g6h">%s</div>' % shead(2, 'teach', lang, ''), teach(lang, False), '<div class="g6h">%s</div>' % shead(3, 'data', lang, ''), account(lang), commits(lang, (0, 1))))
    return (sec(1, 'who', lang, tiles(lang, DOCS['general']['tiles'])) + sec(2, 'teach', lang, teach(lang)) + sec(3, 'data', lang, data(lang, (0, 1, 2))))


def teacher(lang, d):
    f = FL.C['cn' if lang == 'cn' else 'en']
    x = X[lang]
    move = '<div class="g12 rrow">%s</div>' % ''.join('<div class="c%d-%d card step"><div class="sthead"><i>%d</i>%s</div><b class="nm">%s</b><span class="out">%s</span></div>'
                                                       % (1 + 3 * k, 3 + 3 * k, k + 1, ic(i, 'ic big'), a, b) for k, (i, a, b) in enumerate(x['move']))
    return (sec(1, 'fl', lang, '<div class="g12"><div class="c1-12">%s</div></div>' % stairs(f['levels']) + row4(x['model'])) +
            sec(2, 'move', lang, move) + sec(3, 'data', lang, data(lang)))


def parent(lang, d):
    x = X[lang]
    return (sec(1, 'kids', lang, tiles(lang, DOCS['parent']['tiles'])) +
            sec(2, 'ladder', lang, '<div class="g12"><div class="c1-12">%s</div></div>' % stairs(list(zip(x['ladder'], x['ladder_d']))) + row4(x['mfacts'])) +
            sec(3, 'safe', lang, data(lang, (1, 3, 0, 5))))


BODY = {'general': general, 'teacher': teacher, 'parent': parent}
SPANS = '\n'.join('.c%d-%d { grid-column: %d / %d; }' % (a, b, a, b + 1) for a in range(1, 13) for b in range(a, 13))


def page(doc, lang, d):
    cn = lang == 'cn'
    jj = '<!-- JJ review: %s one-pager CN copy (ONEPAGER3-BRIEF, Oct 17, 2026) -->\n' % doc if cn else ''
    fonts = '<link rel="stylesheet" href="/fonts/gf.css" />' + ('<link rel="stylesheet" href="/fonts/zh/zh.css?v=2" />' if cn else '')
    serif = "'Newsreader', 'Arena Serif SC', 'Songti SC', 'Noto Serif SC', Georgia, serif" if cn else "'Newsreader', Georgia, serif"
    root = re.search(r'(?s):root\s*\{.*?\n\}', open(os.path.join(ROOT, 'css', 'pro.css'), encoding='utf-8').read()).group(0)
    wcss = '\n'.join(l for l in open(os.path.join(ROOT, 'css', 'approach.css'), encoding='utf-8').read().splitlines() if l.startswith('.apw'))
    return ('<!doctype html>\n<html lang="%s">\n<head>\n<meta charset="utf-8" />\n<title>Arena School one-pager</title>\n%s%s\n<style>\n%s\n%s\n%s\n</style>\n</head>\n<body>\n'
            '<main class="op %s dir-%s">\n%s\n<div class="body">%s</div>\n%s\n%s\n</main>\n</body>\n</html>\n'
            % ('zh-CN' if cn else 'en', jj, fonts, root, wcss, CSS.replace('SERIF', serif), doc, d, header(lang, doc), BODY[doc](lang, d), strip(lang), footer(lang, doc)))


CSS = r"""
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Geist', 'PingFang SC', system-ui, sans-serif; color: #1E2740; font-size: 8.2pt; line-height: 1.4; }
.op { width: 210mm; height: 297mm; overflow: hidden; display: flex; flex-direction: column; }
.op > * { flex-shrink: 0; }
.g12 { display: grid; column-gap: 4mm; grid-template-columns: repeat(12, minmax(0, 1fr)); padding: 0 10mm; }
SPANS
h1, h2, .nm, .loop { font-family: SERIF; font-weight: 500; color: var(--pro-ink); margin: 0; }
em { font-style: italic; }
.ic { width: 4.4mm; height: 4.4mm; color: var(--pro-action); flex: none; } .ic.big { width: 6.2mm; height: 6.2mm; }
.k, .lab, .eyebrow { font: 600 7.2pt/1.2 'Geist', system-ui, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #4A5578; }
:lang(zh) .k, :lang(zh) .lab, :lang(zh) .eyebrow { letter-spacing: .04em; font-size: 7.6pt; }
/* header: the v2 band (navy, wordmark, large headline with italic accent, intro, demo-day photo right) */
.top { position: relative; background: #0B1A4A; color: #fff; height: 52mm; overflow: hidden; }
.topgrid { position: relative; z-index: 2; height: 100%; align-items: center; }
.top-copy { padding: 0; }
.wm { height: 5mm; width: auto; display: block; margin-bottom: 3.4mm; }
.top .eyebrow { color: #C9D6F2; }
.top h1 { color: #fff; font-size: 19pt; line-height: 1.1; margin: 1.6mm 0 2.6mm; letter-spacing: -.006em; }
:lang(zh) .top h1 { font-size: 18.5pt; line-height: 1.26; }
.general:lang(en) .top h1, .general .top h1:lang(en) { font-size: 17.5pt; }
.top h1 em { color: #C9D6F2; white-space: nowrap; }
.lede { margin: 0; font-size: 8.6pt; line-height: 1.5; color: rgba(255,255,255,.86); max-width: 112mm; }
.photo { position: absolute; top: 0; right: 0; bottom: 0; width: 48%; margin: 0; }
.photo img { width: 100%; height: 100%; object-fit: cover; object-position: 60% 30%; display: block;
  -webkit-mask-image: linear-gradient(90deg, transparent 0, rgba(0,0,0,.6) 22%, #000 46%); mask-image: linear-gradient(90deg, transparent 0, rgba(0,0,0,.6) 22%, #000 46%); }
.photo::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 14mm; background: linear-gradient(180deg, rgba(11,26,74,0), rgba(11,26,74,.78)); }
.photo figcaption { position: absolute; z-index: 2; right: 10mm; bottom: 3.4mm; font-size: 7pt; color: #fff; text-shadow: 0 1px 4px rgba(8,15,38,.7); }
/* body: three sections, equal gaps */
.body { flex: 1; display: flex; flex-direction: column; justify-content: space-evenly; padding: 2mm 0; }
/* section header: a navy number block, a serif title, a one-line dek */
.sh { display: flex; align-items: center; gap: 3.4mm; margin-bottom: 3mm; }
.num { flex: none; width: 9mm; height: 9mm; display: grid; place-items: center; background: #0B1A4A; color: #fff; font: 400 12pt/1 SERIF; border-radius: 1.2mm; }
.sht h2 { font-size: 14.5pt; line-height: 1.1; }
.sht p { margin: .8mm 0 0; font-size: 8.4pt; color: #4A5578; }
/* cards */
.card { border: 1px solid var(--pro-line); border-radius: 2mm; padding: 3mm 3.2mm; background: #fff; display: flex; flex-direction: column; gap: 1.6mm; min-width: 0; }
.nm { display: block; font-size: 11.5pt; line-height: 1.2; margin-top: 1mm; }
.out { display: block; font-size: 8.4pt; line-height: 1.4; color: #3A4466; }
.fm { display: block; font: 600 7.6pt/1.3 'Geist', system-ui, sans-serif; color: var(--pro-action); }
.rrow { align-items: stretch; }
.tile .proof { margin-top: auto; padding-top: 2.4mm; border-top: 1px solid var(--pro-line); display: grid; gap: 1.4mm; }
.tile .proof.empty { border-top-color: transparent; }
.marks { height: 6mm; display: flex; align-items: center; gap: 2.6mm; overflow: visible; }
.marks img { width: auto; display: block; filter: grayscale(1) contrast(1.1); opacity: .85; }
.wordmark { font: 600 7.6pt/1.05 SERIF; color: #3A4466; white-space: normal; max-width: 15mm; }
.cap { font-size: 7.4pt; color: #4A5578; }
.fact { font: 500 12pt/1 SERIF; color: var(--pro-ink); }
/* tile and skill heads: icon inline with the name */
.th { display: flex; align-items: center; gap: 2.2mm; } .th .nm { margin: 0; }
.skh { display: flex; align-items: center; gap: 1.6mm; }
/* wheel at print size: ring labels would be under 7pt, so only the core text shows (strands are listed beside) */
.wheel .apw-out-t, .wheel .apw-mid-t { display: none; }
/* how we teach */
.teach { grid-template-rows: 1fr 1fr; row-gap: 3.4mm; } .teach .wheel { grid-row: 1 / span 2; align-self: center; } .loopc { align-self: end; } .teach .sk { align-self: start; }
.strandk { margin-top: 2.4mm; } .strandk .k { display: block; margin-bottom: 1.2mm; }
:lang(zh) .wheel .apw { max-width: 44.5mm; }
.strow .st { display: flex; align-items: center; gap: 2mm; padding-top: 1.8mm; border-top: 1px solid var(--pro-line); font-size: 8.6pt; font-weight: 500; color: var(--pro-ink); }
.wheel .apw { width: 100%; max-width: 42mm; height: auto; display: block; }
.loop { font-size: 14pt; line-height: 1.22; margin: 0; }
.skills { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4mm; margin-bottom: 3.4mm; }
.sk { display: grid; gap: 1mm; padding-top: 2.4mm; border-top: 2px solid var(--pro-action); }
.sk b { font: 600 10pt/1.2 'Geist', system-ui, sans-serif; color: var(--pro-ink); } .sk span { font-size: 8.4pt; color: #3A4466; }
.strands { list-style: none; margin: 1.6mm 0 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 1.6mm 4mm; }
.strands li { display: flex; align-items: center; gap: 2mm; font-size: 8.6pt; font-weight: 500; color: var(--pro-ink); }
/* staircase: steps carry the number and name; descriptions sit below, one column each */
.stairs { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(5, 1fr); gap: 2.4mm; align-items: end; }
.stairs li { height: calc(15mm + var(--s) * 3mm); border-top: 2.4px solid var(--pro-action); background: color-mix(in srgb, var(--pro-action) calc(7% + var(--s) * 5%), #fff);
  padding: 2.4mm 2.6mm; display: flex; flex-direction: column; justify-content: flex-start; border-radius: 0 0 1.2mm 1.2mm; }
.stairs li > * { flex: none; }
.stairs i { font: 400 13pt/1 SERIF; color: var(--pro-action); font-style: normal; }
.stairs b { font: 600 9pt/1.2 'Geist', system-ui, sans-serif; color: var(--pro-ink); margin-top: 1mm; }
.stairs-d { display: grid; grid-template-columns: repeat(5, 1fr); gap: 2.4mm; margin-top: 2.4mm; }
.stairs-d span { font-size: 8pt; line-height: 1.38; color: #3A4466; padding: 0 2.6mm; }
.row4 { margin-top: 3.4mm; }
.row4 .it { display: flex; gap: 2.4mm; align-items: flex-start; padding-top: 2.6mm; border-top: 1px solid var(--pro-line); }
.row4 b { display: block; font: 600 8.8pt/1.25 'Geist', system-ui, sans-serif; color: var(--pro-ink); } .row4 span { font-size: 8pt; color: #3A4466; }
.step .sthead { display: flex; align-items: center; justify-content: space-between; } .step i { font: 400 15pt/1 SERIF; color: var(--pro-action); font-style: normal; }
/* data: account pair + commitments */
.data { align-items: stretch; } .data .acc { position: relative; } .data .vs { position: absolute; right: -2mm; top: 50%; transform: translate(50%, -50%); z-index: 2; background: #fff; border: 1px solid var(--pro-line-2); border-radius: 50%; width: 7mm; height: 7mm; display: grid; place-items: center; font-size: 7pt; }
.data .c7-12 { display: flex; } .data .commit { flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
.pair { display: grid; grid-template-columns: 1fr auto 1fr; gap: 2.4mm; align-items: stretch; }
.vs { align-self: center; font: 600 7.4pt/1 'Geist', system-ui, sans-serif; letter-spacing: .1em; text-transform: uppercase; color: #4A5578; }
.acc { border: 1px solid var(--pro-line); border-radius: 2mm; padding: 3mm; } .acc.ok { border-color: #0B1A4A; box-shadow: inset 0 3px 0 var(--pro-action); }
.acch { display: flex; align-items: center; gap: 2mm; margin-bottom: 2mm; } .acch b { font: 600 9.4pt/1.2 'Geist', system-ui, sans-serif; color: var(--pro-ink); }
.acc.no .acch .ic { color: #4A5578; }
.acc ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 1.2mm; } .acc li { display: flex; gap: 1.6mm; align-items: center; font-size: 8.4pt; color: #3A4466; }
.mk { width: 3.6mm; height: 3.6mm; flex: none; } .acc.no .mk { color: #9A3B2E; } .acc.ok .mk { color: var(--pro-action); }
.commit { list-style: none; margin: 0; padding: 0; display: grid; gap: 0; }
.commit li { display: flex; align-items: center; gap: 2.6mm; padding: 2mm 0; border-top: 1px solid var(--pro-line); }
.commit li:last-child { border-bottom: 1px solid var(--pro-line); }
:lang(zh) .commit li { padding: 1.7mm 0; }
.commit b { font: 600 9pt/1.3 'Geist', system-ui, sans-serif; color: var(--pro-ink); }
/* bottom credentials strip */
.strip { padding: 3mm 0; border-top: 1px solid var(--pro-line); display: grid; gap: 2.2mm; background: #F6F7FA; }
.strip .row { align-items: center; }
.strip .lab { white-space: nowrap; }
.logos { display: flex; align-items: center; justify-content: space-between; flex-wrap: nowrap; min-width: 0; }
.logos img { width: auto; display: block; filter: grayscale(1) contrast(1.15); opacity: .8; }
.logos img[src*='/brown.'], .logos img[src*='/harvard.'] { filter: grayscale(1) contrast(1.6) brightness(.72); opacity: 1; }
.member { justify-content: flex-start; gap: 12mm; } .member img { filter: none; opacity: 1; }
.m { display: inline-flex; align-items: center; gap: 2mm; white-space: nowrap; } .m em { font-style: normal; font-size: 7.6pt; color: #4A5578; }
/* closing band */
.cta { background: #0B1A4A; color: #fff; padding-top: 4.4mm; padding-bottom: 4.4mm; align-items: center; }
.cta h2 { color: #fff; font-size: 13pt; } .cta p { margin: 1mm 0 0; font-size: 8.2pt; color: rgba(255,255,255,.84); }
.cta .contact { text-align: right; display: grid; gap: .8mm; font-size: 9pt; } .cta .contact span { color: #C9D6F2; }
/* direction B: alternating full-bleed bands, header without the block */
.dir-B .body { padding: 0; justify-content: stretch; }
.dir-B .sec { flex: 1 1 auto; display: flex; flex-direction: column; justify-content: center; padding: 3mm 0; }
.dir-B .sec:nth-child(2) { background: #F3F5FA; }
.dir-B .num { background: none; color: var(--pro-action); width: auto; height: auto; font-size: 22pt; border-right: 1px solid var(--pro-line-2); padding-right: 3.4mm; border-radius: 0; }
/* direction C: magazine halves */
.halves { align-items: start; } .g6h .sh { margin-bottom: 3mm; }
.teach.narrow .wheel .apw { max-width: 34mm; } .teach.narrow { display: grid; grid-template-columns: 34mm 1fr; column-gap: 4mm; align-items: center; }
.teach.narrow .skills { grid-column: 1 / -1; margin-top: 3mm; } .teach.narrow .loop { font-size: 12pt; margin: 0; }
.halves .pair { margin-bottom: 3mm; }
""".replace('SPANS', SPANS)


RENDER_JS = r"""
const { chromium } = require('playwright');
(async () => {
  const [src, pdf] = process.argv.slice(1);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.emulateMedia({ media: 'print' });
  await p.goto(src, { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const r = await p.evaluate(() => {
    const m = document.querySelector('.op'), H = m.getBoundingClientRect().height;
    const over = Math.round([...m.children].reduce((a, k) => a + k.getBoundingClientRect().height, 0) - H);
    const bd = document.querySelector('.body'); const inner = Math.round([...bd.children].reduce((a, k) => a + k.scrollHeight, 0) + parseFloat(getComputedStyle(bd).paddingTop) + parseFloat(getComputedStyle(bd).paddingBottom) - bd.clientHeight);
    const secOver = [...document.querySelectorAll('.sec')].map(x => x.scrollHeight - x.clientHeight).filter(v => v > 1);
    const g = document.querySelector('.g12'), gr = g.getBoundingClientRect(), cs = getComputedStyle(g);
    const cols = cs.gridTemplateColumns.split(' ').map(parseFloat), gap = parseFloat(cs.columnGap), pl = parseFloat(cs.paddingLeft);
    const starts = [], ends = []; let x = gr.left + pl; cols.forEach(w => { starts.push(x); ends.push(x + w); x += w + gap; });
    const bad = [];
    document.querySelectorAll('.g12 > *').forEach(c => { const r = c.getBoundingClientRect(); if (!r.width) return;
      if (!starts.some(s => Math.abs(s - r.left) < .6) || !ends.some(e => Math.abs(e - r.right) < .6)) bad.push((c.className || c.tagName) + ' ' + r.left.toFixed(1) + '-' + r.right.toFixed(1)); });
    const uneven = [];
    document.querySelectorAll('.rrow').forEach(row => { const hs = [...row.children].map(c => Math.round(c.getBoundingClientRect().height)); if (Math.max(...hs) - Math.min(...hs) > 1) uneven.push(hs.join('/')); });
    document.querySelectorAll('.rrow').forEach(row => { const th = [...row.querySelectorAll('.th')].map(t => Math.round(t.getBoundingClientRect().height)); if (th.length && Math.max(...th) - Math.min(...th) > 1) uneven.push('titles ' + th.join('/')); });
    const stepBad = []; document.querySelectorAll('.stairs li').forEach(li => { const r = li.getBoundingClientRect(), pad = parseFloat(getComputedStyle(li).paddingBottom); [...li.children].forEach(c => { if (c.getBoundingClientRect().bottom > r.bottom - pad + .5) stepBad.push(c.textContent); }); });
    const stepTops = [...new Set([...document.querySelectorAll('.stairs li i')].map(i => Math.round((i.getBoundingClientRect().top - i.parentElement.getBoundingClientRect().top) * 10) / 10))];
    let svgMin = 99; document.querySelectorAll('svg.apw text').forEach(t => { if (getComputedStyle(t).display === 'none') return; const sv = t.ownerSVGElement; const k = sv.getBoundingClientRect().width / sv.viewBox.baseVal.width; svgMin = Math.min(svgMin, parseFloat(t.getAttribute('font-size') || getComputedStyle(t).fontSize) * k); });
    const hb = document.querySelector('.top').getBoundingClientRect(), hc = document.querySelector('.top-copy').getBoundingClientRect();
    if (hc.top < hb.top + 8 || hc.bottom > hb.bottom - 8) stepBad.push('header copy outside band');
    const tops = []; document.querySelectorAll('.sh').forEach(d => tops.push(Math.round(d.getBoundingClientRect().left)));
    let min = 99; document.querySelectorAll('.op *').forEach(e => { if ([...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && !e.closest('svg')) min = Math.min(min, parseFloat(getComputedStyle(e).fontSize)); });
    const clipped = []; document.querySelectorAll('.marks, .logos').forEach(l => { const p = l.closest('.card, .row'); const pr = p.getBoundingClientRect(); [...l.children].forEach(c => { const r = c.getBoundingClientRect(); if (r.right > pr.right - 1 || r.left < pr.left) clipped.push(c.textContent || c.getAttribute('src')); }); });
    const wrapped = []; document.querySelectorAll('.logos, .marks').forEach(l => { const ys = [...l.children].map(c => Math.round(c.getBoundingClientRect().top + c.getBoundingClientRect().height / 2)); if (Math.max(...ys) - Math.min(...ys) > 4) wrapped.push(l.className); });
    return { over: Math.max(over, inner), stepBad, stepTops, svgPt: +(svgMin * .75).toFixed(2), secOver, clipped, nbad: bad.length, bad: bad.slice(0, 4), uneven, shLeft: [...new Set(tops)], minPt: +(min * .75).toFixed(2), wrapped,
             cols: starts.map((s, i) => [Math.round(s), Math.round(ends[i])]) };
  });
  await p.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  console.log(JSON.stringify(r)); await b.close();
})();
"""


def overlay(png, out):
    """The 12-column grid (10mm margins, 4mm gutters) drawn over a 150dpi render; blue lines mark the thirds."""
    from PIL import Image, ImageDraw
    im = Image.open(png).convert('RGB')
    d = ImageDraw.Draw(im, 'RGBA')
    px = im.size[0] / 210.0
    col = (210 - 20 - 11 * 4) / 12.0
    for i in range(12):
        x0 = (10 + i * (col + 4)) * px
        x1 = x0 + col * px
        d.rectangle([x0, 0, x1, im.size[1]], fill=(255, 0, 80, 20))
        d.line([x0, 0, x0, im.size[1]], fill=(255, 0, 80, 140))
        d.line([x1, 0, x1, im.size[1]], fill=(255, 0, 80, 140))
    for k in (4, 8):
        x = (10 + k * (col + 4) - 2) * px
        d.line([x, 0, x, im.size[1]], fill=(0, 110, 255, 220), width=2)
    im.save(out)


def build(doc, lang, opt, pngdir=None):
    name = '%s-%s' % (DOCS[doc]['file'], lang)
    open(os.path.join(HERE, name + '.html'), 'w', encoding='utf-8').write(page(doc, lang, opt))
    pdf = os.path.join(ROOT, 'onepager', name + '.pdf')
    out = subprocess.run(['node', '-e', RENDER_JS, 'http://127.0.0.1:8931/tools/one-pager/%s.html' % name, pdf],
                         capture_output=True, text=True, cwd=os.path.join(ROOT, '.ds-sync'))
    if out.returncode:
        sys.exit(out.stderr)
    r = json.loads(out.stdout.strip().splitlines()[-1])
    pages = re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1)
    subprocess.run(['pdftoppm', '-jpeg', '-jpegopt', 'quality=86', '-singlefile', '-scale-to-x', '520', '-scale-to-y', '-1', pdf, pdf[:-4]], check=True)
    if pngdir:
        base = os.path.join(pngdir, name)
        subprocess.run(['pdftoppm', '-png', '-r', '150', '-singlefile', pdf, base], check=True)
        overlay(base + '.png', base + '-grid.png')
    ok = not r['stepBad'] and len(r['stepTops']) <= 1 and r['svgPt'] >= 6.95 and not r['secOver'] and not r['clipped'] and pages == '1' and r['over'] <= 1 and r['nbad'] == 0 and not r['uneven'] and r['minPt'] >= 6.95 and not r['wrapped'] and len(r['shLeft']) <= 1
    print('%-40s steps %s tops %s | svg %spt | clipped %s | pages %s | overflow %spx | off-grid %d %s | uneven %s | header lefts %s | logo rows wrapped %s | min %spt | %s'
          % (name, r['stepBad'], r['stepTops'], r['svgPt'], r['clipped'], pages, r['over'], r['nbad'], r['bad'][:2], r['uneven'], r['shLeft'], r['wrapped'], r['minPt'], 'OK' if ok else 'FAIL'))
    return ok


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opt = sys.argv[sys.argv.index('--dir') + 1] if '--dir' in sys.argv else 'B'
    args = [a for a in args if a != opt]
    pngdir = sys.argv[sys.argv.index('--png') + 1] if '--png' in sys.argv else None
    if pngdir:
        args = [a for a in args if a != pngdir]
    docs = args or list(DOCS)
    fails = [d + '-' + l for d in docs for l in ('en', 'cn') if not build(d, l, opt, pngdir)]
    if fails:
        sys.exit('FAILED: ' + ', '.join(fails))
