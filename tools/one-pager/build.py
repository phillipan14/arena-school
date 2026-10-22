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
        'lux': ('/logos/lux/lux-navy-horizontal.png', 6.6), 'schwarzman': ('/logos/cred/schwarzman.png', 4.6), 'bodley': (None, 'Bodley Academy'), 'acamis': (None, 'ACAMIS')}

L = {
 'en': dict(
   member='A member of', anth='Startup Program', oai='Partner Network', studied='Coached by a team from', worked='',
   web='arenaschool.org', mail='phillip@arenaschool.org', proof='Run with',
   # audience tiles: key -> (icon, label, one line, formats, [proof marks], proof caption)
   T={'students': ('graduation-cap', 'Students', 'Want real AI skills and work to show. They launch a product.', 'Workshops · mentorship', ['isb', 'bodley'], 'Five-day student programs'),
      'schools': ('school', 'Educators', 'Want confident staff and safe use. Each makes a classroom tool.', 'Sessions · workshops', ['tsinghua', 'schwarzman'], 'Staff training, Schwarzman College'),
      'families': ('heart-handshake', 'Families', 'Want their child ready for AI-era work. 1:1 mentors help.', '1:1 mentorship · parent talks', ['pta'], 'Parent talk, ISB PTA'),
      'career': ('briefcase', 'Career', 'Want an edge for internships and jobs. They ship a live product.', 'Bootcamp', ['lux'], 'Jointly hosted with Lux Scholar'),
      # teacher variant
      'teachers': ('wrench', 'Teachers &amp; tech teams', 'Make the tool your class is missing, on your approved systems.', 'Session · workshop · school-wide', ['tsinghua', 'schwarzman'], 'Staff training, Schwarzman College'),
      'tech': ('monitor-cog', 'Tech teams', 'Training on your approved systems.', 'Planning · sessions', [], ''),
      'leaders': ('building-2', 'School leaders', 'Programs for the whole school community.', 'Planned with your team', ['isb'], 'Student program on campus'),
      'conf': ('mic', 'Conferences', 'Talks and hands-on workshops.', 'Keynote · workshop · panel', ['acamis'], 'Next: ACAMIS workshop'),
      # parent variant
      'workshops': ('smartphone', 'Workshops', 'Rebuild an app, or build a portfolio site.', 'At your child’s school', [], ''),
      'intensive': ('rocket', 'Workshops &amp; intensives', 'Two to five days: launch a real product, then pitch it.', 'At your child’s school', ['isb', 'bodley'], 'Five-day student programs'),
      'mentor': ('route', 'Year-long mentorship', 'One project, 1:1, at their own pace.', 'Weekly check-ins, hybrid', ['isb'], 'ISB alumni continue here'),
      'talks': ('messages-square', 'Parent talks', 'How AI is changing work and college.', 'At your child’s school', ['pta'], 'Parent talk, ISB PTA')},
   formats_k='Formats',
   skills=[('compass', 'Choose a real problem', 'And pitch it in three minutes. (Agency)'), ('search-check', 'Test with real users', 'And judge which version works. (Taste)'), ('badge-check', 'Launch and explain it', 'At a live link, every decision defended. (Craft)')],
   loop='Learners decide. AI builds. Real people judge.', strands_k='Four strands, assessed on every project',
   dk='Whose account is it?', personal='Personal account', school='School-approved platform',
   prow=['Consumer terms', 'No data agreement', 'Not for student data'], srow=['Enterprise agreement', 'Agreed by the school', 'Cleared for student data'],
   cta='Bring Arena to your school.', ctap='Planned with your team, run on your campus. Your teachers keep the materials.',
   hub='Arena School',
 ),
 'cn': dict(
   member='成员计划', anth='初创企业计划', oai='合作伙伴网络', studied='<!-- JJ review: 导师团队来自 (PARENT2-BRIEF) -->导师团队来自', worked='',
   web='arenaschool.org', mail='phillip@arenaschool.org', proof='合作',
   T={'students': ('graduation-cap', '学生', '想学真本事、有作品可展示：做出并上线产品。', '工作坊 · 集训营 · 导师计划', ['isb', 'bodley'], '五天学生项目'),
      'schools': ('school', '教师与学校', '想让老师有信心、用得安全：每人做一个课堂工具。', '分享 · 工作坊 · 全校培训', ['tsinghua', 'schwarzman'], '苏世民书院教职员工培训'),
      'families': ('heart-handshake', '家庭', '希望孩子为AI时代的工作做好准备：一对一导师陪伴。', '一对一导师 · 家长讲座', ['pta'], 'ISB PTA 家长讲座'),
      'career': ('briefcase', '大学与职场', '想在实习和求职中脱颖而出：上线一个真实产品。', '训练营', ['lux'], '与千麓学者联合举办'),
      'teachers': ('wrench', '教师与技术团队', '在学校认可的系统上，为课堂做一个正缺的小工具。', '现场分享 · 工作坊 · 全校培训', ['tsinghua', 'schwarzman'], '苏世民书院教职员工培训'),
      'tech': ('monitor-cog', '技术团队', '在学校认可的系统上开展培训。', '规划 · 培训', [], ''),
      'leaders': ('building-2', '校长与管理层', '服务整个学校社群的项目。', '与贵校团队共同规划', ['isb'], '在校园内开展的学生项目'),
      'conf': ('mic', '会议与活动', '主题演讲与动手工作坊。', '演讲 · 工作坊 · 圆桌', ['acamis'], '即将举行：ACAMIS 工作坊'),
      'workshops': ('smartphone', '动手工作坊', '重做一款应用，或做一个作品集网站。', '在孩子的学校', [], ''),
      'intensive': ('rocket', '工作坊与集训营', '两到五天：做出真实的产品，再路演。', '在孩子的学校', ['isb', 'bodley'], '五天学生项目'),
      'mentor': ('route', '学年导师计划', '一个项目，一对一，按自己的节奏。', '每周例会，线上线下结合', ['isb'], 'ISB 营员在此继续'),
      'talks': ('messages-square', '家长讲座', 'AI如何改变工作与升学。', '在孩子的学校', ['pta'], 'ISB PTA 家长讲座')},
   formats_k='形式',
   skills=[('compass', '选一个真实的问题', '三分钟讲清楚。（主动性）'), ('search-check', '拿给真实用户测试', '判断哪个版本真正好用。（审美）'), ('badge-check', '上线并讲清楚', '发布在公开网址，每个决定都讲得出理由。（匠心）')],
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
 'teacher': dict(file='arena-school-teacher-one-pager', tiles=['teachers', 'leaders', 'conf'],
   en=dict(eyebrow='For teachers and school leaders', h1='AI fluency for the whole staff, <em>inside your school’s rules.</em>'),
   cn=dict(eyebrow='面向教师与学校管理层', h1='全体教职员工的AI素养，<em>始终在学校的规则之内。</em>')),
 'parent': dict(file='arena-school-parent-one-pager', tiles=['intensive', 'mentor', 'talks'],
   en=dict(eyebrow='For families', h1='What your child makes, learns, and keeps <em>at Arena School.</em>'),
   cn=dict(eyebrow='写给家长', h1='孩子在 Arena School <em>做什么、学什么、带走什么。</em>')),
}
STUDIED = [('caltech', 2.65), ('harvard', 5.0), ('brown', 5.6), ('tsinghua-lockup', 4.8), ('isb', 4.6)]   # equal ink area per mark (EDGES-BRIEF), from each file's ink; crest + small-caps marks raised to a legible minimum
WORKED = [('mckinsey', 2.8), ('goldman', 4.07), ('yc', 3.84), ('apple', 4.8), ('microsoft-ai', 3.93), ('deloitte', 2.4), ('kimi-wordmark', 2.95)]

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
 'general': {'en': 'Workshops, intensives, year-long mentorship, and staff training, by a team from Harvard, Caltech, Tsinghua, and Y Combinator.',
             'cn': '工作坊、集训营、学年导师计划和教职员工培训；团队来自哈佛、加州理工、清华和 Y Combinator。'},
 'teacher': {'en': 'Staff training, a student bootcamp, and parent talks.',
             'cn': '<!-- JJ review: 导语 (TEACHER-V10, Oct 20) -->教职员工培训、学生训练营、家长讲座。'},
 'parent': {'en': 'With mentors from Harvard, Caltech, Tsinghua, McKinsey, Goldman Sachs, and Y Combinator.',
            'cn': '导师来自哈佛、加州理工、清华、麦肯锡、高盛和 Y Combinator。'},
}
H1 = {'general': {'en': dict(eyebrow='What is Arena School', h1='Hands-on AI programs for students, teachers, <em>and families.</em>'),
                  'cn': dict(eyebrow='认识 Arena School', h1='面向学生、老师和家庭的<em>动手实践AI项目。</em>')},
      'teacher': {'en': dict(eyebrow='For teachers and school leaders', h1='AI programs built to complement <em>your school’s curriculum.</em>'),
                  'cn': dict(eyebrow='面向教师与学校管理层', h1='<!-- JJ review: 标题 (TEACHER-V10) -->与贵校课程互为补充的<em>AI项目。</em>')},
      'parent': {'en': dict(eyebrow='For families', h1='Hands-on AI programs where students build <em>and launch a real product.</em>'),
                 'cn': dict(eyebrow='写给家长', h1='动手实践的AI项目，学生亲手做出<em>并上线真实的产品。</em>')}}
CAP = {'en': 'Demo day at the International School of Beijing, 2026', 'cn': '<!-- JJ review: 照片说明 (CAPTION-BRIEF) -->北京顺义国际学校路演日'}
# section titles: (title, one-line dek)
SEC = {
 'en': dict(who=('Who we serve', 'Each audience and what they come for.'), teach=('What learners actually do', 'The same three moves in every program.'),
            data=('Student data comes first', 'Before which tool, ask whose account it is.'),
            fl=('Five levels of AI fluency', 'A baseline, then every teacher moves up one level a term.'), move=('One session, one working tool', 'Then every teacher moves up one level a term.'), run_k='How a session runs',
            whyt=('Why now', ''), whyp=('Why it matters now', ''), whyg=('Why now', ''),
            kids=('How they get there', 'Five days, from a problem to demo day.'), lead=('What your child walks away with', 'For college, summer program, scholarship, and internship applications.')),
 'cn': dict(who=('我们服务谁', '每类对象，以及他们为什么来。'), teach=('学习者实际做什么', '每个项目都是同样的三个动作。'),
            data=('学生数据放在第一位', '先别问用哪个工具，先问是谁的账号。'),
            fl=('AI素养的五个层级', '先做基线评估，每位老师每学期提升一级。'), move=('一次培训，一个能用的工具', '之后每位老师每学期提升一级。'), run_k='一次培训怎么进行',
            whyt=('为什么是现在', ''), whyp=('为什么是现在', ''), whyg=('为什么是现在', ''),
            kids=('怎样做到', '五天，从选题到路演日。'), lead=('孩子带走什么', '可用于大学、暑期项目、奖学金和实习申请。')),
}
# proof marks normalized to one optical height (mm) inside a 7mm slot; text labels in the same serif, no box
PROOF_H = {'isb': 5.0, 'tsinghua': 4.6, 'pta': 4.8, 'lux': 5.2, 'schwarzman': 4.2}


def header(lang, d):
    t = H1[d][lang]
    return ('<header class="top"><div class="g12 topgrid"><div class="c1-7 top-copy">'
            '<div class="brandrow"><img class="wm" src="/logos/arena/wordmark-ivory-1600.png" alt="Arena School" /><span class="bsep"></span>'
            '<span class="bmem"><span class="blab">%s</span><img src="/logos/partners/anthropic.svg" alt="Anthropic Startup Program" style="height:2.2mm" />'
            '<img src="/logos/partners/openai.svg" alt="OpenAI Partner Network" style="height:4mm" /></span></div>'
            '<span class="eyebrow">%s</span><h1>%s</h1><p class="lede">%s</p>%s</div></div>'
            '<figure class="photo"><img src="/photos/isb-2026/pitch-duo-1600.webp" alt="" /><figcaption>%s</figcaption></figure></header>'
            % (L[lang]['member'], t['eyebrow'], t['h1'], INTRO[d][lang], hstat(lang) if (d == 'parent' and PDIR == 'A') else '', CAP[lang]))


PDIR = os.environ.get('PDIR', 'B')   # parent layout direction (PARENT3-BRIEF): A stat in header, B stat beside outcomes, C stat as intro


def hstat(lang):
    import depth as D
    st = D.STATS['rand-students']
    return '<div class="hstat"><b>%s</b><span>%s</span></div>' % (st['n'], st['cn' if lang == 'cn' else 'en'])


def strip(lang):
    """Bottom credentials: "A member of" on one line; "Team from" with twelve marks on two balanced lines of six equal cells."""
    c = L[lang]
    order = ['caltech', 'harvard', 'brown', 'tsinghua-lockup', 'isb', 'apple', 'mckinsey', 'goldman', 'yc', 'microsoft-ai', 'deloitte', 'kimi-wordmark']
    h = dict(STUDIED + WORKED)
    marks = [(k, h[k]) for k in order]
    cell = lambda k, h: '<span class="lc%s"><img src="/logos/cred/%s.png" alt="" style="height:%smm" /></span>' % (' w2' if k == 'mckinsey' else '', k, h)
    return ('<section class="strip">'
            '<div class="g12 row trow"><span class="c1-3 lab tlabel">%s</span><div class="c4-12 team cols-%d">%s</div></div></section>'
            % (c['studied'], TEAMCOLS, ''.join(cell(k, h) for k, h in marks)))


TEAMCOLS = int(os.environ.get('TEAMCOLS', '6'))   # 6 (2 rows) or 4 (3 rows): the logo grid's column count


def memtop(lang):
    """Slim "A member of" strip under the photo header, as on the homepage: a small centred label and two marks."""
    c = L[lang]
    return ('<section class="memtop g12"><span class="c1-3 lab">%s</span><div class="c4-12 mt">'
            '<span class="m"><img src="/logos/partners/anthropic.svg" alt="Anthropic" style="height:2.6mm" /><em>%s</em></span>'
            '<span class="m"><img src="/logos/partners/openai.svg" alt="OpenAI" style="height:4.8mm" /><em>%s</em></span></div></section>'
            % (c['member'], c['anth'], c['oai']))


def shead(n, key, lang, span='c1-12'):
    t, d = SEC[lang][key]
    return ('<div class="sh %s"><span class="num">%02d</span><div class="sht"><h2>%s</h2>%s</div></div>' % (span, n, t, '<p>%s</p>' % d if d else ''))


def sec(n, key, lang, inner, cls=''):
    cls = cls or ('hs' if key.startswith('why') else '')
    return '<section class="sec %s"><div class="g12">%s</div>%s</section>' % (cls, shead(n, key, lang), inner)


def mark(k):
    f, v = LOGO[k]
    return ('<img src="%s" alt="" style="height:%smm" />' % (f, PROOF_H[k])) if f else '<span class="wordmark">%s</span>' % v


FACT = {'workshops': {'en': ('2 days', 'At your school, no coding needed'), 'cn': ('两天', '在贵校进行，无需编程基础')},
        'tech': {'en': ('Your systems', 'Locked down is fine'), 'cn': ('贵校的系统', '严格管控的环境也可以')}}


def tiles(lang, keys):
    c = L[lang]
    spans = ['c1-4', 'c5-8', 'c9-12'] if len(keys) == 3 else ['c1-3', 'c4-6', 'c7-9', 'c10-12']
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
                      for k, (sp, d) in enumerate(zip(['c4-6', 'c7-9', 'c10-12', 'c4-6'], t['domains'])))
    core = '由学习者<br><em>做决定</em>' if lang == 'cn' else 'The<br>learner<br><em>decides</em>'
    sep = '、' if lang == 'cn' else ' · '
    line = '<p class="c4-12 strline"><b>%s</b>%s</p>' % (c['strands_k'] + ('：' if lang == 'cn' else ': '), sep.join(t['domains']))
    return ('<div class="g12 teach"><div class="c1-3 wheel">%s<span class="core">%s</span></div><div class="c4-12 loopc"><p class="loop">%s</p></div>%s%s</div>'
            % (W.svg('cn' if lang == 'cn' else 'en'), core, c['loop'], skills, line))


def hero(lang, k):
    """One big stat, no citation line (its source is recorded in STATS-SOURCES.md)."""
    import depth as D
    cn = lang == 'cn'
    st = D.STATS[k]
    unit = (' ' + st['unit']['cn' if cn else 'en']) if st['unit'] else ''
    n = '一半' if cn and st['n'] == '1 in 2' else st['n']
    return '<div class="g12 hero"><b class="c1-4 hn">%s%s</b><p class="c5-12 ht">%s</p></div>' % (n, unit, st['cn' if cn else 'en'])


PROG = {
 'en': dict(k='The five-day Entrepreneurship &amp; AI Intensive, at your child’s school', days=[('Day 1', 'Choose a problem', 'Pitch it in three minutes. Teams form.'), ('Day 2', 'Talk to users', 'Interview the people they want to help.'),
            ('Day 3', 'Live at a link', 'A working version anyone can open.'), ('Day 4', 'Brand and price', 'Name it, price it, stop at a fixed hour.'), ('Day 5', 'Demo day', 'Pitch to a panel. Families invited.')],
            mile={2: 'Launch', 4: 'Pitch'}, stretch='Stretch goals in year-long mentorship', stretch_items=['Traction', 'Revenue', 'Impact', 'Recognition'],
            tools_k='AI tools they use', run='Programs run at'),
 'cn': dict(k='五天的创业与AI集训营，在孩子的学校', days=[('第1天', '选定问题', '三分钟讲清楚，再组队。'), ('第2天', '访谈用户', '访谈想帮助的人。'),
            ('第3天', '发布上线', '做出人人都能打开的版本。'), ('第4天', '品牌与定价', '命名、定价，准时封版。'), ('第5天', '路演日', '向评审团路演，家长到场。')],
            mile={2: '上线', 4: '路演'}, stretch='学年导师计划中的进阶目标', stretch_items=['用户增长', '收入', '影响力', '认可'],
            tools_k='孩子用的AI工具', run='项目开展于'),
}
TOOLS = ['openai', 'claude', 'deepseek', 'kimi', 'figma', 'canva']


def timeline(lang):
    g = PROG[lang]
    days = ''.join('<div class="c%d dy%s%s"><span class="dn">%s%s</span><b>%s</b><span class="dd">%s</span></div>'
                   % (k + 1, ' is-m' if k in g['mile'] else '', ' is-top' if k == len(g['days']) - 1 else '', dn, '<span class="ms">%s</span>' % g['mile'][k] if k in g['mile'] else '', t, d)
                   for k, (dn, t, d) in enumerate(g['days']))
    tools = ''.join('<img src="/logos/tools/sm/%s.webp" alt="" />' % t for t in TOOLS)
    stretch = ''.join('<span>%s</span>' % x for x in g['stretch_items'])
    return ('<div class="g12"><div class="c1-12 frame"><span class="k fk">%s</span><div class="days">%s</div>'
            '<div class="frow"><span class="k">%s</span><span class="tl">%s</span><span class="k st">%s</span><span class="sti">%s</span></div></div></div>'
            % (g['k'], days, g['tools_k'], tools, g['stretch'], stretch))


RUN_H = {'isb': 4.6, 'tsinghua': 4.6, 'schwarzman': 4.2, 'pta': 4.6, 'lux': 4.8}


def runat(lang, marks):
    cells = ''.join('<span class="lc">%s</span>' % (('<img src="%s" alt="" style="height:%smm" />' % (LOGO[m][0], RUN_H[m])) if LOGO[m][0] else '<span class="wordmark">%s</span>' % LOGO[m][1]) for m in marks)
    return '<div class="g12 runat trow"><span class="c1-3 lab tlabel">%s</span><div class="c4-12 team rteam cols-6">%s</div></div>' % (PROG[lang]['run'], cells)


def statband(lang, ids):
    import depth as D
    cn = lang == 'cn'
    cells = []
    for sp, k in zip(['c1-4', 'c5-8', 'c9-12'], ids):
        st = D.STATS[k]
        unit = (' ' + st['unit']['cn' if cn else 'en']) if st['unit'] else ''
        n = '一半' if cn and st['n'] == '1 in 2' else st['n']
        cells.append('<div class="%s stat"><b>%s%s</b><span>%s</span><small>%s</small></div>' % (sp, n, unit, st['cn' if cn else 'en'], st['src']['cn' if cn else 'en']))
    return '<div class="g12 rrow stats">%s</div>' % ''.join(cells)


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
                                          ''.join('<li>%s%s</li>' % (ic('check' if ok else 'x', 'mk'), r) for r in rs), ''))
    return ('<div class="g12 data">%s%s<div class="c7-12">%s</div></div>'
            % (col('c1-3', c['personal'], c['prow'], False), col('c4-6', c['school'], c['srow'], True), commits(lang, pick)))


PCTA = {'en': ('Two ways to start.', 'Ask your child’s school to bring Arena, or enroll in the Year-Long Project Mentorship directly.'),
        'cn': ('两种开始方式。', '请孩子的学校邀请 Arena，或直接报名学年项目导师计划。')}


def footer(lang, doc='general'):
    c = L[lang]
    h, p = PCTA[lang] if doc == 'parent' else (c['cta'], c['ctap'])
    nt = '<small class="ctanote">%s</small>' % PX[lang]['note'] if doc == 'parent' else ''
    return ('<footer class="cta g12"><div class="c1-8"><h2>%s</h2><p>%s</p>%s</div><div class="c9-12 contact"><b>%s</b><span>%s</span></div></footer>'
            % (h, p, nt, c['mail'], c['web']))


GEN = {
 'en': dict(cols=['Who', 'Why they come', 'Format', 'What they make'],
            rows=[('Real AI skills, and work to show', 'A launched product'), ('Confident staff, safe use', 'A tool for their class'),
                  ('A child ready for AI-era work', 'A year-long project'), ('An edge for internships and jobs', 'A live AI product')]),
 'cn': dict(cols=['对象', '为什么来', '形式', '做出什么'],
            rows=[('学真本事，有作品可展示', '一个上线的产品'), ('老师有信心，用得安全', '一个课堂工具'),
                  ('孩子为AI时代的工作做好准备', '一个学年项目'), ('在实习和求职中脱颖而出', '一个上线的AI产品')]),
}


def general(lang, d):
    c = L[lang]
    spans = ['c1-3', 'c4-6', 'c7-9', 'c10-12']
    aud = ''.join('<div class="%s card tile"><div class="th">%s<b class="nm">%s</b></div><span class="out">%s</span><span class="fm">%s</span></div>' % (sp, ic(t[0], 'ic big'), t[1], t[2], t[3])
                  for sp, t in zip(spans, [c['T'][k] for k in DOCS['general']['tiles']]))
    g = GEN[lang]
    head = '<div class="ar ah"><span>%s</span><span>%s</span><span>%s</span><span>%s</span></div>' % tuple(g['cols'])
    rows = ''.join('<div class="ar">%s<b class="nm">%s</b></span><span class="aw">%s</span><span class="af">%s</span><span class="am">%s%s</span></div>'
                   % ('<span class="awho">' + ic(t[0], 'ic big'), t[1], why, t[3], ic('check', 'mk'), make)
                   for t, (why, make) in zip([c['T'][k] for k in DOCS['general']['tiles']], g['rows']))
    diagram = '<div class="g12"><div class="c1-12 frame aud">%s%s</div></div>' % (head, rows)
    return (sec(1, 'whyg', lang, hero(lang, 'rand-students-use')) +
            sec(2, 'who', lang, diagram + runat(lang, ['isb', 'bodley', 'tsinghua', 'schwarzman'])) +
            sec(3, 'teach', lang, teach(lang)))


def teacher(lang, d):
    f = FL.C['cn' if lang == 'cn' else 'en']
    x = X[lang]
    flow = ''.join('<div class="fl-step"><span class="fn">%d</span>%s<b>%s</b><span class="dd">%s</span></div>' % (k + 1, ic(i, 'ic big'), a, b) for k, (i, a, b) in enumerate(x['move']))
    return (sec(1, 'whyt', lang, hero(lang, 'rand-use')) +
            sec(2, 'move', lang, '<div class="g12"><div class="c1-12 frame tfr"><span class="k fk">%s</span><div class="flow4">%s</div><span class="k fk fk2">%s</span>%s</div></div>'
                % (SEC[lang]['run_k'], flow, SEC[lang]['fl'][0], stairs(f['levels'], False)) + runat(lang, ['tsinghua', 'schwarzman', 'isb'])) +
            sec(3, 'data', lang, data(lang, (0, 1, 2))))


PX = {
 'en': dict(practical=[('hammer', 'Building with AI', 'Directing AI coding tools, then testing the results.'), ('users', 'Talking to users', 'Interviewing the people they want to help.'),
                       ('mic', 'Pitching', 'Presenting to a panel, and answering questions.'), ('search-check', 'Research and judgment', 'Checking sources, including AI output.')],
            keep=[('rocket', 'A live product', 'At its own link, with their name.'), ('file-text', 'A documented record', 'To describe in an application.'),
                  ('users', 'People who know their work', 'Mentors and reviewers.'), ('mic', 'Experience presenting it', 'To people who ask hard questions.')],
            proof=[(mark('isb'), 'Students built working apps with AI and presented them to judges from Harvard, Stanford, Y Combinator, and AI labs.'), ('<span class="wordmark">Bodley Academy</span>', 'A student launched a sign-language-to-speech app in five days.')],
            prac_k='Practical skills', keep_k='What they keep, for college, summer, and internship applications', note='Admissions decisions rest with each university; we do not promise an outcome.'),
 'cn': dict(practical=[('hammer', '用AI做产品', '指挥AI编程工具，再亲自测试结果。'), ('users', '访谈用户', '访谈自己想帮助的人。'),
                       ('mic', '路演', '向评审团展示，并回答提问。'), ('search-check', '研究与判断', '核查资料来源，包括AI的输出。')],
            keep=[('rocket', '一个上线的产品', '在自己的网址上，署着自己的名字。'), ('file-text', '有据可查的成果记录', '可以写进申请材料。'),
                  ('users', '了解他作品的人', '导师和评审。'), ('mic', '公开展示的经验', '面对尖锐的提问。')],
            proof=[(mark('isb'), '学生借助AI做出可用的应用，并向来自哈佛、斯坦福、Y Combinator 和AI实验室的评委展示。'), ('<span class="wordmark">Bodley Academy</span>', '一名学生在五天里上线了一款手语转语音的应用。')],
            prac_k='实用技能', keep_k='带走什么：可用于大学、暑期项目和实习申请', note='录取的决定权在每所大学自己手里，我们不对结果作任何承诺。'),
}


def outcomes(lang, spans):
    px = PX[lang]
    return ''.join('<div class="%s oc2"><div class="otop"><span class="onum">%02d</span>%s</div><div class="oh"><b>%s</b></div><span class="od">%s</span></div>'
                   % (sp, k + 1, ic(i, 'ic big'), a, b) for k, (sp, (i, a, b)) in enumerate(zip(spans, px['keep'])))


def runrow(lang, marks):
    cells = ''.join('<span class="lc">%s</span>' % (('<img src="%s" alt="" style="height:%smm" />' % (LOGO[m][0], RUN_H2[m])) if LOGO[m][0] else '<span class="wordmark big">%s</span>' % LOGO[m][1]) for m in marks)
    return '<div class="g12 runrow"><span class="c1-3 lab">%s</span><div class="c4-12 rcells cols6" style="grid-template-columns:repeat(%d,minmax(0,1fr))">%s</div></div>' % (PROG[lang]['run'], max(3, len(marks)), cells)


RUN_H2 = {'isb': 7.4}


def timeline2(lang):
    g = PROG[lang]
    days = ''.join('<div class="dy%s%s"><span class="dn">%s%s</span><b>%s</b><span class="dd">%s</span></div>'
                   % (' is-m' if k in g['mile'] else '', ' is-top' if k == len(g['days']) - 1 else '', dn, '<span class="ms">%s</span>' % g['mile'][k] if k in g['mile'] else '', t, d)
                   for k, (dn, t, d) in enumerate(g['days']))
    tools = ''.join('<span class="tc"><img src="/logos/tools/sm/%s.webp" alt="" /><em>%s</em></span>' % (t, TOOLN[t]) for t in TOOLS)
    stretch = ''.join('<span class="sg">%s%s</span>' % (ic('trending-up', 'mk'), x) for x in g['stretch_items'])
    return ('<div class="g12"><div class="c1-12 frame tl2"><span class="k fk">%s</span><div class="days">%s</div></div></div>'
            '<div class="g12 trow2"><span class="c1-3 lab">%s</span><div class="c4-12 tools2">%s</div></div>'
            '<div class="g12 trow2"><span class="c1-3 lab">%s</span><div class="c4-12 stretch2">%s</div></div>'
            % (g['k'], days, g['tools_k'], tools, g['stretch'], stretch))


TOOLN = {'openai': 'ChatGPT', 'claude': 'Claude', 'deepseek': 'DeepSeek', 'kimi': 'Kimi', 'figma': 'Figma', 'canva': 'Canva'}


def parent(lang, d):
    px = PX[lang]
    note = '<div class="g12"><p class="c1-12 note">%s</p></div>' % px['note']
    if PDIR == 'A':
        s1 = sec(1, 'lead', lang, '<div class="g12 rrow">%s</div>' % outcomes(lang, ['c1-3', 'c4-6', 'c7-9', 'c10-12']) + runrow(lang, ['isb', 'bodley']) + note)
    elif PDIR == 'B':
        import depth as D
        st = D.STATS['rand-students']
        statc = '<div class="c1-4 sidestat"><b>%s</b><span>%s</span></div>' % (st['n'], st['cn' if lang == 'cn' else 'en'])
        s1 = sec(1, 'lead', lang, '<div class="g12 rrow">%s<div class="c5-12 ocg">%s</div></div>' % (statc, outcomes(lang, ['', '', '', ''])) + runrow(lang, ['isb', 'bodley']) + note)
    else:
        import depth as D
        st = D.STATS['rand-students']
        intro = '<div class="g12 sint"><p class="c1-12"><b>%s</b> %s</p></div>' % (st['n'], st['cn' if lang == 'cn' else 'en'])
        s1 = sec(1, 'lead', lang, intro + '<div class="g12 rrow">%s</div>' % outcomes(lang, ['c1-6', 'c7-12', 'c1-6', 'c7-12']) + runrow(lang, ['isb', 'bodley']) + note)
    return s1 + sec(2, 'kids', lang, timeline2(lang), 'tlsec')


# ---------------------------------------------------------------- v9 (BUILD-A-BRIEF, Oct 18, 2026): concept A's poster header on every page,
# icon-led structure diagrams, a skills/tools grid, logo rows. Tool lists come only from the site (sources in ONEPAGER-CHANGES.md).
EXTRA_ICONS = {   # two Lucide icons missing from tools/lucide_icons.json (same stroke style)
 'link': '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
 'tag': '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>',
}
ICONS.update(EXTRA_ICONS)

PHOTO9 = {
 'parent': ('/photos/isb-2026/pitch-duo-1600.webp', '60% 32%', CAP),
 'teacher': ('/photos/isb-2026/mentor-feedback-1600.webp', '50% 30%',
             {'en': 'Mentors respond to a student’s work, Beijing 2026', 'cn': '<!-- JJ review: 照片说明 (BUILD-A-BRIEF) -->导师对学生的作品给出反馈，北京，2026年'}),
 'general': ('/photos/hero/gesture-1600.jpg', '50% 34%',
             {'en': 'Demo day at the International School of Beijing, 2026', 'cn': '<!-- JJ review: 照片说明 (BUILD-A-BRIEF) -->北京顺义国际学校路演日'}),
}
EYEBROW9 = {'parent': {'en': 'For families · Five days to demo day', 'cn': '<!-- JJ review: 眉题 (BUILD-A-BRIEF) -->写给家长 · 五天，直到路演日'}}


def poster(lang, d):
    """Concept A's poster: full-bleed real photo, navy fade, wordmark with the memberships right beside it, literal headline."""
    t = H1[d][lang]
    src, pos, cap = PHOTO9[d]
    eb = EYEBROW9.get(d, {}).get(lang, t['eyebrow'])
    return ('<header class="top poster"><figure class="photo"><img src="%s" alt="" style="object-position:%s" /><figcaption>%s</figcaption></figure>'
            '<div class="g12 pgrid"><div class="c1-12 top-copy">'
            '<div class="brandrow"><img class="wm" src="/logos/arena/wordmark-ivory-1600.png" alt="Arena School" /><span class="bsep"></span>'
            '<span class="bmem"><span class="blab">%s</span><span class="bm"><img src="/logos/partners/anthropic.svg" alt="Anthropic" style="height:2.3mm" /><em>%s</em></span>'
            '<span class="bm"><img src="/logos/partners/openai.svg" alt="OpenAI" style="height:4.2mm" /><em>%s</em></span></span></div>'
            '<div class="pcopy"><span class="eyebrow">%s</span><h1>%s</h1><p class="lede">%s</p></div></div></div></header>'
            % (src, pos, cap[lang], L[lang]['member'], L[lang]['anth'], L[lang]['oai'], eb, t['h1'], INTRO[d][lang]))


def itl(nodes, cls=''):
    """Icon-led timeline: one outlined circle per step, joined by an arrowed line; the last step is filled navy.
    nodes: (icon, label, tag or '', title, line)."""
    out = []
    for k, (i, lab, tag, t, dd) in enumerate(nodes):
        last = k == len(nodes) - 1
        out.append('<div class="node%s"><div class="ndrow"><span class="nd">%s</span>%s</div><span class="dn">%s%s</span><b>%s</b><span class="dd">%s</span></div>'
                   % (' is-top' if last else '', ic(i, 'ic'), '' if last else '<span class="ln"></span>', lab,
                      '<span class="ms">%s</span>' % tag if tag else '', t, dd))
    return '<div class="itl %s" style="--n:%d">%s</div>' % (cls, len(nodes), ''.join(out))


DAYICON = ['target', 'messages-square', 'link', 'tag', 'mic']

# tools students use in the five-day intensive: each is listed on programs/product-intensive.html (the intensive's own page)
# Claude Code and Cursor: confirmed by Phillip An, Oct 18, 2026 (STATS-SOURCES.md), now on the intensive page too
PTOOLS = [('openai', 'ChatGPT', 'Research a problem', '调研一个问题'), ('deepseek', 'DeepSeek', 'Research and reason', '调研与推理'),
          ('perplexity', 'Perplexity', 'Check sources', '核查来源'), ('claude', 'Claude Code', 'Build apps', '做应用'),
          ('cursor', 'Cursor', 'Write and fix code', '写代码、改代码'), ('github', 'GitHub', 'Save and share code', '保存和分享代码'),
          ('vercel', 'Vercel', 'Launch at a live link', '上线到公开网址'), ('figma', 'Figma', 'Design the screens', '设计界面'),
          ('canva', 'Canva', 'Make the brand', '做品牌视觉')]
MORE = {'en': '+30 more tools', 'cn': '<!-- JJ review: 工具数量 (TOOLS-BRIEF) -->另有 30 多种工具'}   # Phillip An, Oct 18, 2026
# tools teachers use: listed on programs/teacher-training.html ("Tools we often work with")
TTOOLS = [('openai', 'ChatGPT', 'Plan lessons', '备课'), ('claude', 'Claude', 'Build a class tool', '做课堂工具'),
          ('deepseek', 'DeepSeek', 'Draft materials', '准备材料'), ('kimi', 'Kimi', 'Read long documents', '阅读长文档'),
          ('perplexity', 'Perplexity', 'Check sources', '核查来源'), ('canva', 'Canva', 'Make class visuals', '做课堂视觉')]
# tools students and staff have learned: listed on schools.html
GTOOLS = ['openai', 'claude', 'deepseek', 'kimi', 'figma', 'canva']
SEC9 = {
 'en': dict(lead=('What your child walks away with', 'For college, summer program, scholarship, and internship applications.'),
            kids=('How they get there', 'The five-day Entrepreneurship &amp; AI Intensive, at your child’s school.'),
            learn=('The AI tools they learn', 'Real tools, used hands-on, on a project of their own.'),
            move=('One session, one working tool', 'Each teacher brings one task from a class they teach now.'),
            ttools=('Tools we work with', ''),
            who=('Who we serve', 'Each audience, why they come, and what they make.'),
            fl='Five levels of AI fluency: every teacher moves up one level a term', step='Step', makes='Makes', tools_k='AI tools'),
 'cn': dict(lead=('孩子带走什么', '可用于大学、暑期项目、奖学金和实习申请。'),
            kids=('怎样做到', '五天的创业与AI集训营，在孩子的学校。'),
            learn=('孩子学会的AI工具', '真实的工具，亲手用在自己的项目上。'),
            move=('一次培训，一个能用的工具', '每位老师带来自己正在教的一门课里的一项任务。'),
            ttools=('我们常用的工具', ''),
            who=('我们服务谁', '每类对象，为什么来，做出什么。'),
            fl='AI素养的五个层级：每位老师每学期提升一级', step='第%d步', makes='做出', tools_k='学会的工具'),
}


def sec9(n, key, lang, inner, cls=''):
    t, dk = SEC9[lang][key]
    return ('<section class="sec %s"><div class="g12"><div class="sh c1-12"><span class="num">%02d</span><div class="sht"><h2>%s</h2><p>%s</p></div></div></div>%s</section>'
            % (cls, n, t, dk, inner))


def toolgrid(lang, tools, per):
    span = 12 // per
    cells = ''.join('<div class="c%d-%d tool"><img src="/logos/tools/sm/%s.webp" alt="" /><div class="tx"><b>%s</b><span>%s</span></div></div>'
                    % (1 + (k % per) * span, (k % per + 1) * span, f, n, cn if lang == 'cn' else en) for k, (f, n, en, cn) in enumerate(tools))
    return '<div class="g12 rrow tgrid">%s</div>' % cells


def toolgrid5(lang, tools):
    cells = ''.join('<div class="tool"><img src="/logos/tools/sm/%s.webp" alt="" /><div class="tx"><b>%s</b><span>%s</span></div></div>'
                    % (f, n, cn if lang == 'cn' else en) for f, n, en, cn in tools)
    return '<div class="g12"><div class="c1-12 tg5">%s<div class="tool more"><b>%s</b></div></div></div>' % (cells, MORE[lang])


def keep4(lang):
    spans = ['c1-3', 'c4-6', 'c7-9', 'c10-12']
    return '<div class="g12 rrow keep4">%s</div>' % ''.join(
        '<div class="%s kc"><div class="kh"><span class="ki">%s</span><b>%s</b></div><span>%s</span></div>' % (sp, ic(i), a, b) for sp, (i, a, b) in zip(spans, PX[lang]['keep']))


RUN_H2.update({'isb': 6.6, 'tsinghua': 6.4, 'schwarzman': 5.6})


def parent9(lang, d):
    g, px = PROG[lang], PX[lang]
    days = itl([(DAYICON[k], dn, g['mile'].get(k, ''), t, dd) for k, (dn, t, dd) in enumerate(g['days'])], 'days5')
    note = ''
    return (sec9(1, 'lead', lang, keep4(lang)) +
            sec9(2, 'kids', lang, '<div class="g12"><div class="c1-12">%s</div></div>' % days) +
            sec9(3, 'learn', lang, toolgrid5(lang, PTOOLS) + runrow(lang, ['isb', 'bodley']) + note))


def teacher9(lang, d):
    f, x, s9 = FL.C['cn' if lang == 'cn' else 'en'], X[lang], SEC9[lang]
    lab = lambda k: (s9['step'] % (k + 1)) if lang == 'cn' else '%s %d' % (s9['step'], k + 1)
    flow = itl([(i, lab(k), '', a, b) for k, (i, a, b) in enumerate(x['move'])], 'flow')
    tools = ''.join('<span class="tc"><img src="/logos/tools/sm/%s.webp" alt="" /><em>%s</em></span>' % (t[0], t[1]) for t in TTOOLS)
    trow = '<div class="g12 trow2"><span class="c1-3 lab">%s</span><div class="c4-12 tools2">%s</div></div>' % (s9['ttools'][0], tools)
    return (sec9(1, 'move', lang, '<div class="g12"><div class="c1-12">%s</div></div>' % flow +
                 '<div class="g12 flk"><span class="c1-12 k">%s</span></div><div class="g12"><div class="c1-12">%s</div></div>' % (s9['fl'], stairs(f['levels'], False)) +
                 runrow(lang, ['tsinghua', 'schwarzman', 'isb'])) +
            sec(2, 'data', lang, data(lang, (0, 1, 2)) + trow))


def general9(lang, d):
    c, g, s9 = L[lang], GEN[lang], SEC9[lang]
    spans = ['c1-3', 'c4-6', 'c7-9', 'c10-12']
    aud = ''.join('<div class="%s ac"><span class="nd">%s</span><b class="nm">%s</b><span class="out">%s</span><span class="fm">%s</span><span class="mkl">%s<em>%s</em></span></div>'
                  % (sp, ic(t[0]), t[1], why, t[3], ic('check', 'mk'), make)
                  for sp, t, (why, make) in zip(spans, [c['T'][k] for k in DOCS['general']['tiles']], g['rows']))
    tools = ''.join('<span class="tc"><img src="/logos/tools/sm/%s.webp" alt="" /><em>%s</em></span>' % (t, TOOLN[t]) for t in GTOOLS)
    tools += '<span class="tc tmore">%s</span>' % MORE[lang]
    trow = '<div class="g12 trow2"><span class="c1-2 lab">%s</span><div class="c3-12 tools2">%s</div></div>' % (s9['tools_k'], tools)
    return (sec9(1, 'who', lang, '<div class="g12 rrow aud4">%s</div>' % aud + runrow(lang, ['isb', 'bodley', 'tsinghua', 'schwarzman'])) +
            sec(2, 'teach', lang, teach(lang) + trow))


# ---------------------------------------------------------------- v11 teacher (TEACHER-V11, Oct 20, 2026; JJ's review of v10): no photo (no students'
# faces on print), one component per section (label, serif title, one or two lines, in columns), hairlines between sections, the Arena
# wordmark and the teacher page link in the footer. Every fact is from the live site: programs/teacher-training, schools,
# events/isb-winter-2027, zero-to-launch, programs/community-dialogues, learning-approach ("ISB AI Founders Program"), results.
# Ben/SAS stays off this page (internal only, Oct 15 call notes).
T11 = {
 'en': dict(
   member='A member of', anth='Startup Program', oai='Partner Network',
   s=[('Staff training on their own work', '',
       [('Live session', 'A staff meeting', 'One live session at a meeting you already hold.'),
        ('Hands-on workshop', 'A department', 'Each teacher leaves with a tool for their class.'),
        ('School-wide', 'The whole faculty', 'Each department gets its own session, then a follow-up.')]),
      ('A week-long intensive for your students', '',
       [('ISB · Summer 2026', 'ISB AI Founders Program', 'Grades 7 to 12 pitched to judges from Harvard and Y Combinator.'),
        ('ISB · Jan 5 to 8, 2027', 'AI Fundamentals', 'Grades 6 to 12 build an AI project over winter break.'),
        ('Guangzhou · Dec 27 to Jan 2', 'AI Advantage Bootcamp', 'College and early-career learners launch an AI product.')]),
      ('Talks for your parents', '',
       [('ISB PTA · Oct 14, 2026', 'Parent coffee', 'How AI is changing jobs and college admissions.'),
        ('Evening', 'Parent talk', 'Practical advice for families of grades 6 to 12.'),
        ('Leadership', 'Staff briefing', 'Prepares leaders and counselors for parents’ top AI questions.')]),
      ('How we plan it with you', '',
       [('Step 1', 'Scope', 'Plan a call to determine your school’s goals and work around your schedule.'),
        ('Step 2', 'Adapt', 'We adapt the program to your students’ ages, language, and timetable.'),
        ('Step 3', 'Run', 'We lead every session, and one of your teachers co-runs it with us.'),
        ('Step 4', 'Hand off', 'Your team keeps the curriculum, rubrics, and demo-day format to reuse.')])],
   fl='Five levels of AI fluency, re-measured each term',
   team='Coached by a team from', foot='Planned with your team, run on your campus.',
   link='arenaschool.org', mail='contact@arenaschool.org'),
 'cn': dict(
   member='', anth='<!-- JJ review: 成员说法 (TEACHER-V11) -->初创企业计划成员', oai='合作伙伴网络成员',
   s=[('<!-- JJ review: 全部中文文案 (TEACHER-V11) -->教职员工培训：从老师手头的工作出发', '',
       [('现场分享', '教职工例会', '在已有的教职工例会上，做一场现场分享。'),
        ('动手工作坊', '教研组', '每位老师带走一个能在课堂上用的小工具。'),
        ('全校培训', '全体教师', '每个教研组各安排一场培训，之后再跟进。')]),
      ('为学生开设的一周集训营', '',
       [('ISB · 2026年夏', 'ISB AI Founders Program', '初高中学生做出应用，向哈佛和 Y Combinator 的评委路演。'),
        ('ISB · 2027年1月5日至8日', '学生AI基础营', '初高中学生在寒假最后四天，用AI做出一个项目。'),
        ('广州 · 12月27日至1月2日', 'AI职场先发营', '大学生与职场新人七天上线一款真实的AI产品。')]),
      ('面向家长的讲座', '',
       [('ISB PTA · 2026年10月14日', '家长咖啡会', '上午的小范围交流：AI如何改变就业和大学录取。'),
        ('晚间', '主题分享', '为初高中学生的家庭提供具体建议。'),
        ('管理层', '教职工简报', '帮助校长、校董会和升学顾问回答家长最常问的AI问题。')]),
      ('我们如何与贵校一起规划', '',
       [('第1步', '明确目标', '安排一次通话，明确贵校的目标，并配合贵校的时间安排。'),
        ('第2步', '调整方案', '按学生的年龄、语言和校历，调整整个项目方案。'),
        ('第3步', '共同开展', '每一场课程都由我们带领，贵校老师全程参与。'),
        ('第4步', '交接留存', '课程、评分标准和路演日流程都留给贵校团队。')])],
   fl='AI素养五个层级，每学期重新评估',
   team='团队成员来自', foot='与贵校团队共同规划，在贵校校园开展。',
   link='arenaschool.org', mail='contact@arenaschool.org'),
}
TEAM11 = [('harvard', 5.6), ('caltech', 3.1), ('tsinghua-lockup', 5.2), ('goldman', 4.8), ('mckinsey', 2.5), ('microsoft-ai', 4.4), ('kimi-wordmark', 3.2)]   # seven marks, one row; McKinsey at 2.5mm fits its cell
NW_CN = ['斯坦福', '哈佛', '大学录取', '大学生', '职场新人', '千麓学者', '初高中学生', 'Y Combinator', 'AI工具', 'AI产品', '小工具', '项目', '路演日', '评委',
         '学习', '校历', '老师', '跟进', '分享', '规则', '升学顾问', '教职工', '提问', '推销', '评分标准', '参与', '贵校团队', '学生', '形式', '调整', '目标', '就业', '现场分享', '真实', '建议', '统一', '贵校', '带领', 'AI原生工作', '具体建议', '负责任地', '课堂小工具', '项目制学习', '手机应用', '一手观察', '招聘方式', '时间安排', '项目方案', '贵校老师', '路演日流程', '升学顾问', 'AI问题']
NW_EN = ['Y Combinator', 'Lux Scholar', 'grades 6 to 12', 'grades 7 to 12', 'Grades 6 to 12', 'Grades 7 to 12', '8 to 12 weeks', 'early-career', 'a follow-up', 'Hong Kong']


def nw(text, lang):
    """Wrap names, number ranges, and (CN) words in no-break spans so a line never splits inside them; longest match wins."""
    words = sorted(NW_CN if lang == 'cn' else NW_EN, key=len, reverse=True)
    return re.sub('|'.join(re.escape(w) for w in words), lambda m: '<span class="nw">%s</span>' % m.group(0), text)


def header11(lang):
    """Type-only navy band: wordmark and memberships on one line, then eyebrow, headline, and lede."""
    t, h = T11[lang], H1['teacher'][lang]
    lab = '<span class="blab">%s</span>' % t['member'] if t['member'] else ''
    return ('<header class="top hd11"><img class="crest11" src="/logos/arena/seal-ivory-1024.png" alt="" /><div class="g12"><div class="c1-12 top-copy">'
            '<div class="brand11"><img class="wm" src="/logos/arena/wordmark-ivory-1600.png" alt="Arena School" /><span class="bsep"></span>%s'
            '<span class="bm"><img class="lg-anth" src="/logos/partners/anthropic.svg" alt="Anthropic" /><em>%s</em></span>'
            '<span class="bm"><img class="lg-oai" src="/logos/partners/openai.svg" alt="OpenAI" /><em>%s</em></span></div>'
            '<span class="eyebrow">%s</span><h1>%s</h1><p class="lede">%s</p></div></div></header>'
            % (lab, t['anth'], t['oai'], h['eyebrow'], h['h1'], INTRO['teacher'][lang]))


def strip11(lang):
    cells = ''.join('<span class="lc"><img src="/logos/cred/%s.png" alt="" style="height:%smm" /></span>' % (k, h) for k, h in TEAM11)
    return ('<section class="strip"><div class="g12 row trow"><span class="c1-3 lab tlabel">%s</span><div class="c4-12 team cols-6">%s</div></div></section>'
            % (T11[lang]['team'], cells))


def footer11(lang):
    c, t = L[lang], T11[lang]
    return ('<footer class="cta g12 ft11"><span class="c1-6 fwm"><img class="wm" src="/logos/arena/wordmark-ivory-1600.png" alt="Arena School" /></span>'
            '<div class="c7-12 ct11"><b class="lk">%s</b><span class="em">%s</span></div></footer>' % (t['link'], t['mail']))


# ---------------------------------------------------------------- v13 teacher (TEACHER-V13, Oct 20, 2026; JJ): three offerings with clear hierarchy.
# Level 1 headline; level 2 the rail (number + category); level 3 the offering (name, a key-facts line, what happens);
# level 4 detail (fluency levels, the five days, the talk's topics); level 5 proof ("Run at"). "How we work" is a quieter band.
# Facts: JJ (PD 2-3 hours; AI Fundamentals 5-day product-building bootcamp, 20+ newest AI tools, ethical and responsible use,
# project-based; one parent coffee on the future of work and education); the site (teacher-training, product-intensive
# day plan, community-dialogues topics, schools steps, results).
T13 = {
 'en': dict(
   staff=('Staff training', [
       ('PD session · 2 to 3 hours', 'A live session for all staff', 'A live demo, then each teacher tries the task on their own material.'),
       ('Hands-on workshop', 'Department or whole faculty', 'Each teacher leaves with a working tool for their class, plus a follow-up.')],
       'Five levels of AI fluency, reassessable each term', 'Most recently at Schwarzman College, Tsinghua University.'),
   stu=('Student program', '5 days · Grades 6 to 12 · On your campus', 'AI Fundamentals: a product-building bootcamp',
        'Project-based: students learn 20+ of the newest AI tools, use AI ethically and responsibly, and leave with a working web or mobile app.',
        [('Day 1', 'Pick a problem'), ('Day 2', 'Talk to users'), ('Day 3', 'Launch it'), ('Day 4', 'Name and price'), ('Day 5', 'Demo day')],
        'Most recently at ISB, with judges from Harvard, Stanford, and Y Combinator;<br>upcoming sessions in Hong Kong and Guangzhou.'),
   par=('Parent talk', 'Morning · Small group · English or Chinese', 'Parent coffee: the future of work and education',
        'Firsthand, from people who do the hiring themselves.',
        ['AI-native work and<br>how hiring has changed', 'Which skills will<br>matter as jobs change', 'Practical advice for<br>families of grades 6 to 12'],
        'Most recently at the ISB PTA Parent Coffee.'),
   how=('How we work', [('Scope', 'Plan a call to determine your school’s goals and work around your schedule.'),
                        ('Adapt', 'We adapt the program to your students’ ages, language, and timetable.'),
                        ('Run', 'We lead every session, and one of your teachers co-runs it with us.'),
                        ('Hand off', 'Your team keeps the curriculum, rubrics, and demo-day format to reuse.')],
        'Only school-approved tools; data rules agreed with your tech team.')),
 'cn': dict(
   staff=('<!-- JJ review: 全部中文文案 (TEACHER-V13) -->教职员工培训', [
       ('教师发展培训 · 2到3小时', '全体教职员工现场分享', '我们在屏幕上现场演示一项任务，随后每位老师用自己的材料上手尝试。'),
       ('动手工作坊', '按教研组或全校开展', '每位老师都带走一个课堂小工具，之后再跟进。')],
       'AI素养五个层级，每学期可重新评估', '最近一次：清华大学苏世民书院。'),
   stu=('学生项目', '5天 · 初高中学生 · 在贵校校园', 'AI基础营：动手做产品的训练营',
        '项目制学习：学生学会20多种最新的AI工具，合乎伦理、负责任地使用AI，最后做出一个能用的网页或手机应用。',
        [('第1天', '选定问题'), ('第2天', '访谈用户'), ('第3天', '发布上线'), ('第4天', '品牌与定价'), ('第5天', '路演日')],
        '最近一次：ISB，评委来自哈佛、斯坦福和 Y Combinator；<br>即将在香港和广州开展。'),
   par=('家长讲座', '上午 · 小范围 · 中文或英文', '家长咖啡会：工作与教育的未来',
        '来自亲自做招聘的人的一手观察。',
        ['AI原生工作，<br>以及招聘方式的变化', '工作在变，<br>哪些能力最重要', '为初高中各年龄段家庭<br>给出具体建议'],
        '最近一场：ISB PTA 家长咖啡会。'),
   how=('合作方式', [('明确目标', '安排一次通话，明确贵校的目标，并配合贵校的时间安排。'),
                     ('调整方案', '按学生的年龄、语言和校历，调整整个项目方案。'),
                     ('共同开展', '每一场课程都由我们带领，贵校老师全程参与。'),
                     ('交接留存', '课程、评分标准和路演日流程都留给贵校团队。')],
        '只用贵校认可的工具，数据规则事先与技术团队商定。')),
}


def teacher13(lang, d):
    t, f = T13[lang], FL.C['cn' if lang == 'cn' else 'en']
    rail = lambda n, cat: '<div class="c1-3 rail">%s<b class="cat">%s</b></div>' % ('<span class="num">%02d</span>' % n if n else '', cat)   # no number: not an offering
    sec = lambda n, cat, main, cls='': ('<section class="sec s13 %s"><div class="g12">%s<div class="c4-12 main13">%s</div></div></section>'
                                        % (cls, rail(n, cat), main))
    proof = lambda x: '<p class="proof13">%s</p>' % nw(x, lang)
    # 01 staff training: two offerings, then the fluency levels
    cat, offers, fl, pr = t['staff']
    cards = ''.join('<div class="card11 off13"><span class="cl">%s</span><b class="ot">%s</b><span class="cd">%s</span></div>' % (a, b, nw(c, lang)) for a, b, c in offers)
    levels = ''.join('<span class="lv"><span class="lvi"><i>%d</i>%s</span></span>' % (j + 1, name) for j, (name, _) in enumerate(f['levels']))
    s1 = sec(1, cat, '<div class="cols cols-2">%s</div><span class="cl flk13">%s</span><div class="lvs">%s</div>%s' % (cards, fl, levels, proof(pr)))
    # 02 the student program: one offering, its five days
    cat, meta, name, desc, days, pr = t['stu']
    dayrow = ''.join('<div class="dy13"><span class="cl">%s</span><b>%s</b></div>' % (a, b) for a, b in days)
    s2 = sec(2, cat, '<div class="card11 off13 wide dayc"><span class="cl">%s</span><b class="ot">%s</b><span class="cd">%s</span><div class="days13">%s</div></div>%s'
             % (meta, name, nw(desc, lang), dayrow, proof(pr)))
    # 03 the parent coffee: one talk, its three topics
    cat, meta, name, first, topics, pr = t['par']
    tops = ''.join('<div class="tp13"><span class="cd">%s</span></div>' % nw(x, lang) for x in topics)
    s3 = sec(3, cat, '<div class="card11 off13 wide topc"><span class="cl">%s</span><b class="ot">%s</b><span class="cd">%s</span><div class="tops13">%s</div></div>%s'
             % (meta, name, nw(first, lang), tops, proof(pr)))
    # how we work: how we partner, not an offering, so it is unnumbered; a quieter band, no cards
    cat, steps, note = t['how']
    st = ''.join('<div class="st13"><b>%s</b><span>%s</span></div>' % (a, nw(b, lang)) for a, b in steps)
    s4 = sec(None, cat, '<div class="steps13">%s</div>' % st, 'how13')
    return s1 + s2 + s3 + s4


BODY9 = {'general': general9, 'teacher': teacher13, 'parent': parent9}


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
            '<main class="op %s dir-%s v9%s">\n%s\n<div class="body">%s</div>\n%s\n%s\n</main>\n</body>\n</html>\n'
            % ('zh-CN' if cn else 'en', jj, fonts, root, wcss, CSS.replace('SERIF', serif), doc, d, ' v11' if doc == 'teacher' else '', header11(lang) if doc == 'teacher' else poster(lang, doc), BODY9[doc](lang, d),
               strip11(lang) if doc == 'teacher' else strip(lang), footer11(lang) if doc == 'teacher' else footer(lang, doc)))


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
.top-copy { padding: 0 4mm 0 0; }
.wm { height: 5mm; width: auto; display: block; margin-bottom: 3.4mm; }
.top .eyebrow { color: #C9D6F2; }
.top h1 { color: #fff; font-size: 19pt; line-height: 1.1; margin: 1.6mm 0 2.6mm; letter-spacing: -.006em; }
:lang(zh) .top h1 { font-size: 18.5pt; line-height: 1.26; }
.general:lang(en) .top h1, .general .top h1:lang(en) { font-size: 17.5pt; }
.top h1 em { color: #C9D6F2; white-space: nowrap; }
.lede { margin: 0; font-size: 8.6pt; line-height: 1.5; color: rgba(255,255,255,.86); max-width: 112mm; }
.photo { position: absolute; top: 0; right: 0; bottom: 0; left: 92mm; margin: 0; }
/* a soft left-to-right fade from the navy into the photo (as on the site's hero); the headline area stays solid navy */
.photo::before { content: ''; position: absolute; top: 0; bottom: 0; right: 0; left: -1mm; z-index: 1; background: linear-gradient(90deg, #0B1A4A 0, #0B1A4A 18%, rgba(11,26,74,.6) 30%, rgba(11,26,74,0) 44%); }
.photo img { width: 100%; height: 100%; object-fit: cover; object-position: 68% 30%; display: block;
  }
.photo::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 14mm; background: linear-gradient(180deg, rgba(11,26,74,0), rgba(11,26,74,.78)); }
.photo figcaption { position: absolute; z-index: 2; right: 10mm; bottom: 3.4mm; font-size: 7pt; color: #fff; white-space: nowrap; text-shadow: 0 1px 4px rgba(8,15,38,.85); }
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
.tile .proof { margin-top: auto; height: 17mm; align-content: start; padding-top: 2.4mm; border-top: 1px solid var(--pro-line); display: grid; gap: 1.4mm; }
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
.teach { row-gap: 3mm; align-items: start; } .teach .wheel { grid-row: 1 / span 3; position: relative; align-self: center; }
.strline { margin: 0; font-size: 7.6pt; color: #3A4466; padding-top: 2mm; border-top: 1px solid var(--pro-line); } .strline b { font-weight: 600; color: var(--pro-ink); } .teach .sk { align-self: start; }
.wheel .apw-core-t { display: none; }
.wheel .core { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); text-align: center; font: 500 7pt/1.12 SERIF; color: #fff; width: 38%; }
.wheel .core em { color: #C9D6F2; }
.strow { margin-top: 3mm; row-gap: 1.4mm; align-items: center; } .strow .k { grid-row: 1 / span 2; align-self: center; }
:lang(zh) .wheel .apw { max-width: 38mm; }
.strow .st { display: flex; align-items: center; gap: 2mm; padding-top: 1.8mm; border-top: 1px solid var(--pro-line); font-size: 8.6pt; font-weight: 500; color: var(--pro-ink); }
.wheel .apw { width: 100%; max-width: 38mm; height: auto; display: block; margin: 0 auto; }
.loop { font-size: 13pt; line-height: 1.22; margin: 0; }
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
.data .c7-12 { display: flex; } .data .commit { flex: 1; display: grid; grid-auto-rows: 1fr; } .data .commit li { padding: 0; }
.pair { display: grid; grid-template-columns: 1fr auto 1fr; gap: 2.4mm; align-items: stretch; }
.vs { align-self: center; font: 600 7.4pt/1 'Geist', system-ui, sans-serif; letter-spacing: .1em; text-transform: uppercase; color: #4A5578; }
.acc { border: 1px solid var(--pro-line); border-radius: 2mm; padding: 3mm; } .acc.ok { border-color: #0B1A4A; box-shadow: inset 0 3px 0 var(--pro-action); }
.acch { display: flex; align-items: center; gap: 2mm; margin-bottom: 2mm; } .acch b { font: 600 9.4pt/1.2 'Geist', system-ui, sans-serif; color: var(--pro-ink); }
.acc.no .acch .ic { color: #4A5578; }
.acc ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 1.2mm; } .acc li { display: flex; gap: 1.4mm; align-items: center; font-size: 8pt; color: #3A4466; white-space: nowrap; }
.mk { width: 3.6mm; height: 3.6mm; flex: none; } .acc.no .mk { color: #9A3B2E; } .acc.ok .mk { color: var(--pro-action); }
.commit { list-style: none; margin: 0; padding: 0; display: grid; gap: 0; }
.commit li { display: flex; align-items: center; gap: 2.6mm; padding: 2mm 0; border-top: 1px solid var(--pro-line); }
.commit li:last-child { border-bottom: 1px solid var(--pro-line); }
:lang(zh) .commit li { padding: 1.7mm 0; }
.commit b { font: 600 9pt/1.3 'Geist', system-ui, sans-serif; color: var(--pro-ink); }
/* "A member of" under the header: centred label, two marks with captions */
.memtop { align-items: center; padding-top: 2.6mm; padding-bottom: 2.6mm; border-bottom: 1px solid var(--pro-line); }
.memtop .mt { display: flex; align-items: center; justify-content: flex-end; gap: 9mm; }
.memtop .m { display: inline-flex; align-items: center; gap: 2mm; white-space: nowrap; } .memtop .m em { font-style: normal; font-size: 7.4pt; color: #4A5578; }
/* bottom credentials strip */
.strip { padding: 2.4mm 0; border-top: 1px solid var(--pro-line); display: grid; gap: 2.2mm; background: #F6F7FA; }
.strip .row { align-items: center; }
.strip .lab { white-space: nowrap; }
.logos { display: flex; align-items: center; justify-content: space-between; flex-wrap: nowrap; min-width: 0; }
/* one 6-column grid for both credential rows: every logo centred in its column */
.six { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); row-gap: 1.4mm; align-items: center; }
.six .lc { display: flex; align-items: center; justify-content: center; height: 6.2mm; min-width: 0; }
/* columns stay aligned row to row; the outer columns sit on the content edges */
.six.member { gap: 0; column-gap: 0; justify-content: stretch; }
.six .m { flex-direction: column; height: auto; gap: .8mm; } .six .m em { font-style: normal; font-size: 7pt; color: #4A5578; white-space: nowrap; }
.team img { width: auto; display: block; filter: grayscale(1) contrast(1.15); opacity: .8; }
/* one greyscale darkness for every mark */
.team img, .team img[src*='/brown.'], .team img[src*='/harvard.'] { filter: grayscale(1) brightness(0); opacity: .72; }
.trow { align-items: center; } .tlabel { align-self: center; }
/* the logo block: equal cells, every mark centred in its cell, the block ends on the right content edge */
.team { display: grid; row-gap: 1.8mm; column-gap: 0; align-items: center; }
.team.cols-6 { grid-template-columns: repeat(6, minmax(0, 1fr)); } .team.cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
.team .lc { display: flex; align-items: center; justify-content: center; height: 6.2mm; min-width: 0; }
.team.cols-6 .lc:nth-child(6n+1) { justify-content: flex-start; } .team.cols-6 .lc:nth-child(6n) { justify-content: flex-end; }
.logos img { width: auto; display: block; filter: grayscale(1) contrast(1.15); opacity: .8; }
.logos img[src*='/brown.'], .logos img[src*='/harvard.'] { filter: grayscale(1) contrast(1.6) brightness(.72); opacity: 1; }
.member { justify-content: flex-start; gap: 12mm; } .member img { filter: none; opacity: 1; }
.m { display: inline-flex; align-items: center; gap: 2mm; white-space: nowrap; } .m em { font-style: normal; font-size: 7.6pt; color: #4A5578; }
.sk3 { display: flex; flex-direction: column; gap: 1.2mm; padding-top: 2.4mm; border-top: 2px solid var(--pro-action); }
.pk { margin-top: 3.4mm; } .pk .k { display: block; margin-bottom: 1.4mm; }
.prac .pi { display: flex; align-items: center; gap: 2mm; padding: 2mm 0; border-top: 1px solid var(--pro-line); border-bottom: 1px solid var(--pro-line); } .prac b { font: 600 8.2pt/1.2 'Geist', system-ui, sans-serif; color: var(--pro-ink); white-space: nowrap; }
.parent .stairs li { height: calc(15mm + var(--s) * 2mm); }
.dir-B.parent .sec { padding: 2.3mm 0; }
.keepk { margin-top: 3.4mm; }
.pf { display: flex; align-items: center; gap: 3mm; margin-top: 2.4mm; padding: 2mm 2.4mm; background: #F3F5FA; border-radius: 1.6mm; } .pf .marks { flex: none; height: 6mm; } .pf span { font-size: 7.8pt; line-height: 1.35; color: #3A4466; } .keepk .k { margin-bottom: 1.6mm; } .keepk .k { display: block; } .keep { margin-top: 1.4mm; } .note { margin: 2.4mm 0 0; padding: 0; font-size: 7.2pt; color: #4A5578; }
/* why-now stats: big figure, one line, source in small type */
.stats .stat { display: flex; flex-direction: column; gap: 1mm; padding-top: 2.2mm; border-top: 2px solid var(--pro-action); }
.stats .stat b { font: 400 18pt/1 SERIF; color: var(--pro-ink); }
.stats .stat span { font-size: 7.8pt; line-height: 1.35; color: #3A4466; }
.stats .stat small { margin-top: auto; font-size: 7pt; line-height: 1.3; color: #4A5578; }
/* header brand row: wordmark, a hairline, and the two memberships in white */
.brandrow { display: flex; align-items: center; gap: 3.4mm; margin-bottom: 4mm; } .brandrow .wm { margin: 0; }
.bsep { width: 1px; height: 5mm; background: rgba(255,255,255,.3); }
.bmem { display: flex; align-items: center; gap: 3mm; } .bmem img { filter: brightness(0) invert(1); opacity: .92; }
.blab { font: 600 7pt/1 'Geist', system-ui, sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #C9D6F2; }
:lang(zh) .blab { letter-spacing: .04em; font-size: 7.2pt; }
/* hero stat */
.hero { align-items: center; } .hn { font: 400 44pt/1 SERIF; color: var(--pro-action); letter-spacing: -.01em; }
.ht { margin: 0; font: 400 14pt/1.35 SERIF; color: var(--pro-ink); }
/* framed program timeline */
.frame { border: 1px solid var(--pro-ink); border-radius: 2mm; padding: 4mm 4.4mm 3.6mm; background: #fff; }
.frame + * {}
.fk { display: block; margin-bottom: 2.6mm; }
.days { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0; position: relative; }
.dy { position: relative; padding: 3.4mm 3mm 3.4mm; border-top: 3px solid var(--pro-line-2); }
.dy + .dy { border-left: 1px solid var(--pro-line); }
.dy.is-m { border-top-color: var(--pro-action); background: color-mix(in srgb, var(--pro-action) 6%, #fff); }
.dy .dn { display: block; font: 600 7pt/1 'Geist', system-ui, sans-serif; letter-spacing: .1em; text-transform: uppercase; color: var(--pro-action); }
.dy b { display: block; margin: 2mm 0 1.2mm; font: 500 12pt/1.2 SERIF; color: var(--pro-ink); }
.dy .dd { display: block; font-size: 8.4pt; line-height: 1.35; color: #3A4466; }
.dy .dn { display: flex; align-items: center; justify-content: space-between; } .dy .ms { font: 600 7pt/1 'Geist', system-ui, sans-serif; letter-spacing: 0; text-transform: none; color: #fff; background: var(--pro-action); padding: .8mm 1.6mm; border-radius: 1mm; }
.frow { display: flex; align-items: center; gap: 3mm; margin-top: 4mm; padding-top: 2.6mm; border-top: 1px solid var(--pro-line); flex-wrap: nowrap; }
.frow .tl { display: flex; align-items: center; gap: 2.8mm; } .frow .tl img { height: 5.6mm; width: auto; border-radius: 1mm; }
.frow .st { margin-left: auto; } .sti { display: flex; gap: 1.4mm; } .sti span { font-size: 8pt; color: var(--pro-ink); border: 1px dashed var(--pro-line-2); border-radius: 1mm; padding: .6mm 1.6mm; }
/* programs run at: logos only */
.runat { align-items: center; margin-top: 3.6mm; } .runat .wordmark { font-size: 9pt; white-space: nowrap; max-width: none; color: #3A4466; }
.rteam img { filter: grayscale(1) brightness(0); opacity: .72; }
.kp { flex-direction: column; gap: 1mm; } .kp .out { margin: 0; }
.parent .top h1:lang(en) { font-size: 17.5pt; } .rmarks { display: flex; align-items: center; gap: 8mm; } .runat .k { align-self: center; }
.rmarks img { width: auto; filter: grayscale(1) contrast(1.1); opacity: .85; } .rmarks .wordmark { font-size: 9pt; max-width: none; white-space: nowrap; }
/* teacher session flow */
.flow { align-items: stretch; } .fl-step { position: relative; display: flex; flex-direction: column; gap: 1mm; padding: 3mm; border: 1px solid var(--pro-line); border-radius: 2mm; }
.fl-step:not(:last-child)::after { content: '→'; position: absolute; right: -3.4mm; top: 50%; transform: translateY(-50%); color: var(--pro-action); font-size: 9pt; z-index: 2; }
.fl-step .fn { font: 400 12pt/1 SERIF; color: var(--pro-action); } .fl-step b { font: 500 10pt/1.2 SERIF; color: var(--pro-ink); } .fl-step .dd { font-size: 7.6pt; line-height: 1.35; color: #3A4466; }
/* day 5: the climax, navy */
.dy.is-top { background: #0B1A4A; border-top-color: #0B1A4A; } .dy.is-top .dn { color: #C9D6F2; } .dy.is-top b, .dy.is-top .dd { color: #fff; }
.dy.is-top .ms { background: #fff; color: #0B1A4A; }
/* general: framed audience diagram, who -> why -> format -> what they make */
.aud { padding: 1.6mm 4.4mm 2mm; } .ar { display: grid; grid-template-columns: 1.1fr 1.45fr 1.15fr 1.5fr; gap: 4mm; align-items: center; padding: 2.6mm 0; border-top: 1px solid var(--pro-line); }
.ar.ah { border-top: 0; padding: 1.4mm 0; font: 600 7pt/1.2 'Geist', system-ui, sans-serif; letter-spacing: .1em; text-transform: uppercase; color: #4A5578; }
.awho { display: flex; align-items: center; gap: 2.4mm; } .awho .nm { margin: 0; font-size: 11pt; }
.aw { font-size: 8.6pt; color: #3A4466; } .af { font: 600 8pt/1.3 'Geist', system-ui, sans-serif; color: var(--pro-action); }
.am { display: flex; align-items: center; gap: 1.6mm; font: 500 10pt/1.2 SERIF; color: var(--pro-ink); }
/* fill the reclaimed space with bigger diagrams, not padding */
.general .ar { padding: 3.6mm 0; } .general .awho .nm { font-size: 12pt; } .general .am { font-size: 11pt; } .general .aw { font-size: 9pt; }
.general .wheel .apw { max-width: 44mm; } .general .loop { font-size: 14pt; }
.parent .kp { padding: 3.6mm 3.6mm; } .parent .kp .nm { font-size: 12pt; } .parent .kp .out { font-size: 8.6pt; }
.parent .dy { padding-top: 4mm; padding-bottom: 4mm; }
/* teacher: one frame for the session flow and the fluency levels */
.flow4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; } .fk2 { margin-top: 3.6mm; }
/* ===== parent v8 (PARENT3-BRIEF) ===== */
.hstat { display: flex; align-items: baseline; gap: 3mm; margin-top: 3.4mm; padding-top: 2.6mm; border-top: 1px solid rgba(255,255,255,.25); max-width: 112mm; }
.hstat b { font: 400 22pt/1 SERIF; color: #C9D6F2; } .hstat span { font-size: 8.4pt; line-height: 1.35; color: rgba(255,255,255,.88); }
.oc2 { position: relative; display: flex; flex-direction: column; gap: 1.6mm; padding: 4mm 4mm 4.2mm; background: #fff; border: 1px solid var(--pro-line); border-top: 3px solid #0B1A4A; border-radius: 0 0 2mm 2mm; min-width: 0; }
.onum { font: 400 22pt/1 SERIF; color: var(--pro-action); }
.oh { display: flex; align-items: center; gap: 2.2mm; } .oh b { font: 500 12pt/1.2 SERIF; color: var(--pro-ink); white-space: nowrap; }
.otop { display: flex; align-items: center; justify-content: space-between; }
.ocg .oc2 { padding: 3.6mm 3.4mm 3.8mm; }
.od { font-size: 8.6pt; line-height: 1.4; color: #3A4466; }
.ocg { display: grid; grid-template-columns: 1fr 1fr; gap: 4mm; }
.sidestat { display: flex; flex-direction: column; justify-content: center; gap: 3mm; padding: 5mm; background: #0B1A4A; border-radius: 2mm; color: #fff; }
.sidestat b { font: 400 46pt/1 SERIF; color: #C9D6F2; } .sidestat span { font: 400 11pt/1.4 SERIF; color: #fff; }
.sint p { margin: 0 0 3.4mm; font: 400 12pt/1.4 SERIF; color: var(--pro-ink); } .sint b { font: 400 20pt/1 SERIF; color: var(--pro-action); margin-right: 1.4mm; }
.runrow { align-items: center; margin-top: 4mm; padding-top: 3.4mm; border-top: 1px solid var(--pro-line); }
.rcells { display: flex; align-items: center; gap: 12mm; } .rcells img { width: auto; filter: grayscale(1) brightness(0); opacity: .72; }
.wordmark.big { font: 600 12pt/1 SERIF; color: #3A4466; border: 0; padding: 0; max-width: none; white-space: nowrap; }
.tl2 .days { grid-template-columns: repeat(5, 1fr); }
.trow2 { align-items: center; margin-top: 3.6mm; } .trow2 + .trow2 { margin-top: 2.8mm; }
.tools2 { display: grid; grid-template-columns: repeat(6, 1fr); } .tc { display: flex; align-items: center; gap: 1.8mm; }
.tc img { height: 6mm; width: auto; border-radius: 1.2mm; } .tc em { font-style: normal; font-size: 8.4pt; font-weight: 500; color: var(--pro-ink); }
.stretch2 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; }
.sg { display: flex; align-items: center; gap: 2mm; padding: 2mm 2.4mm; border: 1px dashed var(--pro-line-2); border-radius: 1.4mm; font: 500 9pt/1.2 SERIF; color: var(--pro-ink); }
.sg .mk { color: var(--pro-action); width: 3.6mm; height: 3.6mm; }
.sg i { font-style: normal; font: 600 7pt/1 'Geist', system-ui, sans-serif; color: #fff; background: var(--pro-action); border-radius: 50%; width: 4.2mm; height: 4.2mm; display: grid; place-items: center; flex: none; }
/* ===== v9 (BUILD-A-BRIEF): poster header, icon-led timelines, tool grid ===== */
.poster { height: 86mm; } .teacher .poster { height: 80mm; } .general .poster { height: 90mm; }
.poster .photo { left: 0; }
.poster .photo::before { left: 0; background: linear-gradient(180deg, rgba(11,26,74,.82) 0, rgba(11,26,74,.2) 20%, rgba(11,26,74,.08) 38%, rgba(11,26,74,.72) 62%, #0B1A4A 92%); }
.poster .photo::after { display: none; }
.poster .photo figcaption { top: 9.4mm; bottom: auto; }
.poster .pgrid { position: relative; z-index: 2; height: 100%; padding-top: 8mm; padding-bottom: 7mm; align-items: stretch; }
.poster .top-copy { display: flex; flex-direction: column; justify-content: space-between; padding: 0; }
.poster .brandrow { margin: 0; }
.poster h1 { font-size: 26pt; line-height: 1.08; margin: 2mm 0 2.6mm; max-width: 175mm; }
:lang(zh) .poster h1 { font-size: 22pt; line-height: 1.28; }
.poster .lede { font-size: 9.2pt; max-width: 150mm; }
.v9 .sht h2 { font-size: 14pt; }
/* icon-led timeline */
.itl { display: grid; grid-template-columns: repeat(var(--n), minmax(0, 1fr)); column-gap: 4mm; }
.node { display: flex; flex-direction: column; min-width: 0; }
.ndrow { display: flex; align-items: center; margin-bottom: 2.6mm; }
.nd { flex: none; width: 11mm; height: 11mm; border-radius: 50%; display: grid; place-items: center; border: 1.4px solid var(--pro-action); background: #fff; }
.nd .ic { width: 5.2mm; height: 5.2mm; }
.ln { flex: 1; position: relative; height: 1.4px; background: var(--pro-line-2); margin: 0 -2.4mm 0 2.4mm; }
.ln::after { content: ''; position: absolute; right: -.4mm; top: 50%; transform: translateY(-50%); border: 1.3mm solid transparent; border-left: 2mm solid var(--pro-action); border-right: 0; }
.node .dn { height: 4mm; display: flex; align-items: center; gap: 2mm; font: 600 7pt/1 'Geist', system-ui, sans-serif; letter-spacing: .1em; text-transform: uppercase; color: var(--pro-action); }
:lang(zh) .node .dn { letter-spacing: .04em; font-size: 7.4pt; }
.node .ms { font: 600 7pt/1 'Geist', system-ui, sans-serif; letter-spacing: 0; text-transform: none; color: #fff; background: var(--pro-action); padding: .8mm 1.6mm; border-radius: 1mm; }
.node b { text-wrap: balance; display: block; margin: 1.8mm 0 1mm; font: 500 12pt/1.2 SERIF; color: var(--pro-ink); }
.node .dd { font-size: 8.4pt; line-height: 1.38; color: #3A4466; }
.node.is-top .nd { background: #0B1A4A; border-color: #0B1A4A; box-shadow: 0 0 0 1.4mm color-mix(in srgb, var(--pro-action) 16%, #fff); }
.node.is-top .nd .ic { color: #fff; }
.node.is-top .ms { background: #0B1A4A; }
.node.is-top b { font-weight: 600; }
/* outcomes strip */
.keep4 .kc { display: flex; flex-direction: column; gap: 2mm; align-items: flex-start; padding: 3mm 3.2mm 3.2mm; border: 1px solid var(--pro-line); border-top: 3px solid #0B1A4A; border-radius: 0 0 1.6mm 1.6mm; background: #fff; }
.ki { flex: none; width: 8.6mm; height: 8.6mm; border-radius: 50%; display: grid; place-items: center; background: color-mix(in srgb, var(--pro-action) 10%, #fff); }
.ki .ic { width: 4.6mm; height: 4.6mm; }
.keep4 .kc { position: relative; padding-right: 3.2mm; } .kh { display: block; padding-right: 9mm; } .kh .ki { position: absolute; top: 2.6mm; right: 2.6mm; width: 7.4mm; height: 7.4mm; } .kh .ki .ic { width: 4mm; height: 4mm; }
.kc b { display: block; text-wrap: balance; font: 500 11pt/1.2 SERIF; color: var(--pro-ink); } .kc > span { display: block; font-size: 8.2pt; line-height: 1.35; color: #3A4466; }
/* tool grid: logo, name, the skill */
.tgrid + .tgrid { margin-top: 3mm; }
.tool { display: flex; align-items: center; gap: 2.6mm; padding: 2.6mm 2.8mm; border: 1px solid var(--pro-line); border-radius: 1.6mm; background: #fff; min-width: 0; }
.tool img { flex: none; width: 8.4mm; height: 8.4mm; border-radius: 1.8mm; object-fit: contain; }
.tool .tx { min-width: 0; } .tool b { display: block; font: 600 9pt/1.2 'Geist', system-ui, sans-serif; color: var(--pro-ink); white-space: nowrap; }
.tool span { display: block; margin-top: .6mm; font-size: 8pt; line-height: 1.3; color: #3A4466; white-space: nowrap; }
.teacher .tool { padding: 2.2mm 2.2mm; gap: 2mm; } .teacher .tool img { width: 7mm; height: 7mm; } .teacher .tool span { white-space: normal; }
.v9 .runrow { margin-top: 3.6mm; }
.v9 .note { margin-top: 2.2mm; }
/* teacher */
.flk { margin-top: 4.4mm; margin-bottom: 2.4mm; }
.teacher .stairs li { height: calc(9mm + var(--s) * 2mm); padding: 1.6mm 2.4mm; flex-direction: row; align-items: baseline; gap: 1.8mm; } .teacher .stairs b { margin: 0; }
.teacher .stairs i { font-size: 11pt; }
/* general: audience cards with an icon node */
.aud4 .ac { display: flex; flex-direction: column; gap: 1.4mm; padding: 3.4mm 3.2mm; border: 1px solid var(--pro-line); border-radius: 2mm; background: #fff; }
.ac .out, .ac .fm { text-wrap: pretty; } .ac .nd { margin-bottom: 1mm; } .ac .nm { margin: 0; font-size: 12pt; } .ac .out { font-size: 8.4pt; }
.ac .mkl { margin-top: auto; padding-top: 2mm; border-top: 1px solid var(--pro-line); display: flex; align-items: center; gap: 1.6mm; }
.ac .mkl em { font: 500 9.6pt/1.2 SERIF; font-style: normal; color: var(--pro-ink); }
.teacher .trow2 { margin-top: 3.6mm; }
.general .trow2 { margin-top: 4mm; padding-top: 3mm; border-top: 1px solid var(--pro-line); }
.rcells.cols6 { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 0; }
.rcells.cols6 .lc { display: flex; align-items: center; justify-content: center; height: 7mm; } .rcells.cols6 .lc:first-child { justify-content: flex-start; }
.rcells .wordmark.big { font-size: 11pt; }
.ctanote { display: block; margin-top: 1.2mm; font-size: 7pt; color: #C9D6F2; }
:lang(zh) .poster h1 em { font-style: normal; }
.parent .poster .photo::before { background: linear-gradient(180deg, rgba(11,26,74,.8) 0, rgba(11,26,74,.1) 18%, rgba(11,26,74,0) 46%, rgba(11,26,74,.7) 68%, #0B1A4A 94%); }
.parent .poster .photo img { filter: contrast(1.08) saturate(1.05); }
.teacher .stairs { align-items: stretch; } .teacher .stairs li { height: 10mm; }
/* TOOLS-BRIEF: memberships with their qualifying words; parent 2 x 5 tool grid; the +30 tile */
.poster .bmem { gap: 3.4mm; } .bm { display: inline-flex; align-items: center; gap: 1.6mm; white-space: nowrap; }
.bm img { filter: brightness(0) invert(1); opacity: .92; } .bm em { font-style: normal; font-size: 7.4pt; color: #DCE4F7; }
.poster .photo figcaption { top: auto; bottom: 7.4mm; }
.poster .lede { max-width: 122mm; text-wrap: balance; }
.tg5 { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 3mm 3mm; }
.tg5 .tool { padding: 2.4mm 2.2mm; gap: 2mm; } .tg5 .tool img { width: 7mm; height: 7mm; border-radius: 1.6mm; }
.tg5 .tool b { font-size: 8.8pt; } .tg5 .tool span { white-space: normal; font-size: 7.8pt; }
.tool.more { justify-content: center; background: #0B1A4A; border-color: #0B1A4A; }
.tool.more b { font: 500 11pt/1.2 SERIF; color: #fff; white-space: normal; text-align: center; }
.general .tools2 { grid-template-columns: repeat(7, minmax(0, 1fr)); } .general .tc img { height: 5.4mm; } .general .tc em { font-size: 8pt; }
.tc.tmore { justify-content: center; font: 500 8.4pt/1.15 SERIF; color: #fff; background: #0B1A4A; border-radius: 1.2mm; padding: 1.4mm 1.6mm; text-align: center; }
/* closing band */
.cta { background: #0B1A4A; color: #fff; padding-top: 4.4mm; padding-bottom: 4.4mm; align-items: center; }
.cta h2 { color: #fff; font-size: 13pt; } .cta p { margin: 1mm 0 0; font-size: 8.2pt; color: rgba(255,255,255,.84); }
.cta .contact { text-align: right; display: grid; gap: .8mm; font-size: 9pt; } .cta .contact span { color: #C9D6F2; }
/* direction B: alternating full-bleed bands, header without the block */
.dir-B .body { padding: 0; justify-content: stretch; }
.dir-B .sec { flex: 1 1 auto; display: flex; flex-direction: column; justify-content: center; padding: 3mm 0; }
.dir-B .sec.hs { flex: 0 0 auto; padding: 4mm 0; } .sec.hs .sh { margin-bottom: 1.6mm; }
.dir-B .sec:nth-child(2) { background: #F3F5FA; }
.dir-B .num { background: none; color: var(--pro-action); width: auto; height: auto; font-size: 22pt; border-right: 1px solid var(--pro-line-2); padding-right: 3.4mm; border-radius: 0; }
/* direction C: magazine halves */
.halves { align-items: start; } .g6h .sh { margin-bottom: 3mm; }
.teach.narrow .wheel .apw { max-width: 34mm; } .teach.narrow { display: grid; grid-template-columns: 34mm 1fr; column-gap: 4mm; align-items: center; }
.teach.narrow .skills { grid-column: 1 / -1; margin-top: 3mm; } .teach.narrow .loop { font-size: 12pt; margin: 0; }
.halves .pair { margin-bottom: 3mm; }
/* ===== v11 teacher (TEACHER-V11): one spacing system. Side margin 15mm; header and footer bands pad 9mm; sections share the
   leftover height equally and are split by hairlines; every section uses one component (label, serif title, one or two lines). ===== */
.v11 .g12 { padding: 0 15mm; column-gap: 5mm; }
.v11 .hd11 { height: auto; padding: 7mm 0 6.1mm; background: #0B1A4A; }
.crest11 { position: absolute; z-index: 0; width: 58mm; height: 58mm; right: -12mm; top: 50%; transform: translateY(-50%); opacity: .07; pointer-events: none; }
.hd11 > .g12 { position: relative; z-index: 1; } :lang(zh) .v11 .hd11 { padding-bottom: 6.1mm; }
.brand11 { display: flex; align-items: center; gap: 3.4mm; height: 6mm; margin-bottom: 5.6mm; }
.brand11 .wm { height: 5mm; width: auto; margin: 0; display: block; }
.brand11 .bm { display: inline-flex; align-items: center; gap: 1.8mm; white-space: nowrap; }
.brand11 .bm img { display: block; width: auto; filter: brightness(0) invert(1); opacity: .92; }
.brand11 .lg-anth { height: 2.3mm; } .brand11 .lg-oai { height: 4.2mm; }
.brand11 .bm em { font-style: normal; font-size: 7.6pt; line-height: 1; color: #DCE4F7; }
.brand11 .blab { line-height: 1; transform: translateY(.26mm); }
.v11 .hd11 .eyebrow { display: block; color: #C9D6F2; }
.v11 .hd11 h1 { color: #fff; font-size: 22pt; line-height: 1.1; margin: 1.6mm 0 2.2mm; letter-spacing: -.006em; }
:lang(zh) .v11 .hd11 h1 { font-size: 22pt; line-height: 1.25; }
.v11 .hd11 h1 em { color: #C9D6F2; white-space: nowrap; }
:lang(zh) .v11 .hd11 h1 em { font-style: normal; }
.v11 .hd11 .lede { margin: 0; max-width: none; font-size: 9.6pt; line-height: 1.45; color: rgba(255,255,255,.88); }
.v11 .body { padding: 0; justify-content: flex-start; }
.v11 .s11, .v11.dir-B .s11:nth-child(2) { flex: 1 1 auto; display: flex; flex-direction: column; justify-content: center; padding: 3.28mm 0 3.12mm; background: #fff; }
:lang(zh) .v11 .s11, :lang(zh) .v11.dir-B .s11:nth-child(2) { padding: 3.25mm 0 3.15mm; }
.v11 .s11 + .s11 { box-shadow: inset 0 1px 0 #E2E6EE; }
.v11 .s11 .sh { display: flex; align-items: center; gap: 4mm; margin: 0 0 2.8mm; }
.v11 .s11 .num { flex: none; width: auto; height: auto; padding: 0 4mm 0 0; border-right: 1px solid var(--pro-line-2); border-radius: 0; background: none;
  font: 400 21pt/1 SERIF; color: var(--pro-action); }
.v11 .s11 .sht h2 { font-size: 14.5pt; line-height: 1.15; }
.v11 .s11 .sht p { margin: 1mm 0 0; font-size: 8.8pt; line-height: 1.35; color: #4A5578; }
.cols { display: grid; column-gap: 5mm; } .cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); } .cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); column-gap: 4mm; }
.cols-4 .card11 { padding-left: 3.8mm; padding-right: 3.6mm; }
.col { display: flex; flex-direction: column; min-width: 0; }
.card11 { padding: 4.1mm 4.4mm 3.5mm; border: 1px solid #DCE1EA; border-radius: 2mm; background: #fff; }
:lang(zh) .card11 { padding-top: 4.15mm; padding-bottom: 3.55mm; }   /* CJK lines carry more slack below the ink */
.cl { display: block; font: 600 7.2pt/1.2 'Geist', system-ui, sans-serif; letter-spacing: .1em; text-transform: uppercase; color: var(--pro-action); }
:lang(zh) .cl { letter-spacing: .04em; font-size: 7.6pt; }
.ct { display: block; margin: 1.2mm 0 .9mm; font: 500 11.5pt/1.2 SERIF; color: var(--pro-ink); }
.cd { display: block; font-size: 8.8pt; line-height: 1.42; color: #3A4466; }
.nw { white-space: nowrap; }
.flk11 { margin-top: 3.2mm; margin-bottom: 1.8mm; }
.lvs { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 2mm; }
.lv { display: flex; align-items: center; justify-content: center; height: 7.6mm; border-radius: 1.2mm; background: color-mix(in srgb, var(--pro-action) 8%, #fff); }
.lv:nth-child(2) { background: color-mix(in srgb, var(--pro-action) 12%, #fff); } .lv:nth-child(3) { background: color-mix(in srgb, var(--pro-action) 16%, #fff); }
.lv:nth-child(4) { background: color-mix(in srgb, var(--pro-action) 20%, #fff); } .lv:nth-child(5) { background: color-mix(in srgb, var(--pro-action) 24%, #fff); }
.lvi { display: inline-flex; align-items: baseline; gap: 1.6mm; font: 600 9pt/1 'Geist', system-ui, sans-serif; color: var(--pro-ink); }
.lvi i { font: inherit; font-style: normal; color: var(--pro-action); }
.lvi { transform: translateY(.12mm); } :lang(zh) .lvi { transform: translateY(.16mm); }
.v11 .strip { padding: 5.13mm 0; background: #fff; border-top: 1px solid #E2E6EE; } :lang(zh) .v11 .strip { padding: 6.15mm 0; }
.v11 .strip .tlabel { transform: translateY(.22mm); } :lang(zh) .v11 .strip .tlabel { transform: translateY(.27mm); }   /* CJK label sat 1.25px above the logos' center line */
.v11 .strip .team { grid-template-columns: repeat(7, auto); justify-content: space-between; }   /* equal gaps between marks of different widths */
.v11 .strip .team .lc { justify-content: center; }
.v11 .cta { padding-top: 4.8mm; padding-bottom: 4.6mm; align-items: center; }
.ft11 { align-items: center; }
.ft11 .fwm { display: flex; align-items: center; } .ft11 .wm { height: 8.4mm; width: auto; display: block; margin: 0; }
.ft11 .ct11 { display: grid; gap: 1.6mm; justify-items: end; }
.ft11 .lk { text-align: right; font-size: 9pt; color: #fff; white-space: nowrap; }
.ft11 .em { text-align: right; font-size: 8.6pt; line-height: 1.3; color: #C9D6F2; }
/* ===== v13 teacher (TEACHER-V13): a left rail (number + category) and one offering block per section ===== */
.v11 .s13, .v11.dir-B .s13:nth-child(2) { flex: 1 1 auto; display: flex; flex-direction: column; justify-content: center; padding: 4.33mm 0 3.67mm; background: #fff; }
:lang(zh) .v11 .s13, :lang(zh) .v11.dir-B .s13:nth-child(2) { padding: 4.42mm 0 3.58mm; }
.v11 .s13 + .s13 { box-shadow: inset 0 1px 0 #E2E6EE; }
.rail { display: flex; flex-direction: column; gap: 1.6mm; align-self: start; transform: translateY(-.36mm); }
:lang(zh) .how13 .rail { transform: translateY(-.03mm); }   /* the CN label sat 1.25px above the step titles */
.rail .num { display: block; width: auto; height: auto; padding: 0; border: 0; border-radius: 0; background: none; text-align: left; font: 400 21pt/1 SERIF; color: var(--pro-action); }
.rail .cat { font: 500 14pt/1.15 SERIF; color: var(--pro-ink); }
.main13 { display: flex; flex-direction: column; min-width: 0; }
.cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.off13 { display: flex; flex-direction: column; }
.off13 .ot { display: block; margin: 1.2mm 0 1mm; font: 500 12.5pt/1.2 SERIF; color: var(--pro-ink); }
.off13.wide .ot { font-size: 14pt; }
.dy13, .tp13 { flex: none; } .tp13 .cd { white-space: nowrap; }
:lang(en) .dayc { padding-bottom: 3.87mm; } :lang(en) .topc { padding-bottom: 3.75mm; }
.flk13 { display: block; margin: 3.4mm 0 1.6mm; }
.proof13 { margin: 2.4mm 0 0; font-size: 7.8pt; line-height: 1.35; color: #4A5578; }
.days13 { display: flex; justify-content: space-between; margin-top: 3mm; padding-top: 2.6mm; border-top: 1px solid #E2E6EE; }
.dy13 b { display: block; margin-top: .8mm; font: 600 8.6pt/1.25 'Geist', system-ui, sans-serif; color: var(--pro-ink); white-space: nowrap; }
.tops13 { display: flex; justify-content: space-between; margin-top: 2.2mm; padding-top: 2.4mm; border-top: 1px solid #E2E6EE; }
.how13 .steps13 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 4mm; }
.st13 > b { display: block; font: 500 10.5pt/1.2 SERIF; color: var(--pro-ink); } .st13 > span { display: block; margin-top: .8mm; font-size: 8pt; line-height: 1.38; color: #3A4466; }
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
    document.querySelectorAll('.rrow').forEach(row => { const pt = [...row.querySelectorAll('.tile .proof')].map(t => Math.round(t.getBoundingClientRect().top)); if (pt.length && Math.max(...pt) - Math.min(...pt) > 1) uneven.push('proof ' + pt.join('/')); });
    const cents = sel => [...document.querySelectorAll(sel)].map(e => { const r = e.getBoundingClientRect(); return Math.round(r.left + r.width / 2); });
    const tc = cents('.strip .team .lc'), mc = cents('.member .lc');
    const nc = getComputedStyle(document.querySelector('.strip .team')).gridTemplateColumns.split(' ').length;
    for (let i = nc; i < tc.length; i++) if (Math.abs(tc[i] - tc[i - nc]) > 1) uneven.push('team col ' + i);
    document.querySelectorAll('.acc li').forEach(li => { if (li.getBoundingClientRect().height > 16) uneven.push('acc wrap: ' + li.textContent); });
    const fc = document.querySelector('.photo figcaption'); if (fc && fc.getBoundingClientRect().height > 14) stepBad.push('caption wraps');
    const g0 = document.querySelector('.body .g12'), g0r = g0.getBoundingClientRect(), gcs = getComputedStyle(g0);
    const L0 = g0r.left + parseFloat(gcs.paddingLeft), R0 = g0r.right - parseFloat(gcs.paddingRight);
    const edges = [];
    const lefts = ['.top-copy', '.memtop .lab', '.sh', '.rrow > :first-child', '.data > :first-child', '.tlabel', '.cta > :first-child'];
    const rights = ['.memtop .mt > :last-child', '.rrow > :last-child', '.data > :last-child', '.team', '.cta .contact', '.stairs-wrap', '.row4 > :last-child'];
    lefts.forEach(sel => document.querySelectorAll(sel).forEach(e => { const x = e.getBoundingClientRect().left; if (Math.abs(x - L0) > 1) edges.push('L ' + sel + ' ' + Math.round(x - L0)); }));
    rights.forEach(sel => document.querySelectorAll(sel).forEach(e => { if (e.closest('.frame')) return; const x = e.getBoundingClientRect().right; if (Math.abs(x - R0) > 1) edges.push('R ' + sel + ' ' + Math.round(x - R0)); }));
    const tops = []; document.querySelectorAll('.sh').forEach(d => tops.push(Math.round(d.getBoundingClientRect().left)));
    let min = 99; document.querySelectorAll('.op *').forEach(e => { if ([...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && !e.closest('svg')) min = Math.min(min, parseFloat(getComputedStyle(e).fontSize)); });
    const clipped = []; document.querySelectorAll('.marks, .logos, .team .tl, .prac .pi, .memtop .mt, .oc2 .oh, .tool .tx, .poster .brandrow, .poster .bmem, .tools2').forEach(l => { const p = l.closest('.card, .row, .prac, .memtop, .pf, .oc2, .tool, .top-copy, .trow2'); const pr = p.getBoundingClientRect(); [...l.children].forEach(c => { const r = c.getBoundingClientRect(); if (r.right > pr.right - 1 || r.left < pr.left) clipped.push(c.textContent || c.getAttribute('src')); }); });
    const wrapped = []; document.querySelectorAll('.logos, .marks').forEach(l => { const ys = [...l.children].map(c => Math.round(c.getBoundingClientRect().top + c.getBoundingClientRect().height / 2)); if (Math.max(...ys) - Math.min(...ys) > 4) wrapped.push(l.className); });
    return { over: Math.max(over, inner), edges, stepBad, stepTops, svgPt: +(svgMin * .75).toFixed(2), secOver, clipped, nbad: bad.length, bad: bad.slice(0, 4), uneven, shLeft: [...new Set(tops)], minPt: +(min * .75).toFixed(2), wrapped,
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
    ok = not r['edges'] and not r['stepBad'] and len(r['stepTops']) <= 1 and r['svgPt'] >= 6.95 and not r['secOver'] and not r['clipped'] and pages == '1' and r['over'] <= 1 and r['nbad'] == 0 and not r['uneven'] and r['minPt'] >= 6.95 and not r['wrapped'] and len(r['shLeft']) <= 1
    print('%-40s edges %s | steps %s tops %s | svg %spt | clipped %s | pages %s | overflow %spx | off-grid %d %s | uneven %s | header lefts %s | logo rows wrapped %s | min %spt | %s'
          % (name, r['edges'], r['stepBad'], r['stepTops'], r['svgPt'], r['clipped'], pages, r['over'], r['nbad'], r['bad'][:2], r['uneven'], r['shLeft'], r['wrapped'], r['minPt'], 'OK' if ok else 'FAIL'))
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
