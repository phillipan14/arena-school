"""Student data section (DATA-BRIEF, Oct 17, 2026), EN + CN, on Teachers, Technology, Schools, and Partnerships.

One copy deck, written between <!-- data:start --> and <!-- data:end --> right after each page's pressures section:
  - "Whose account is it?": a two-column diagram, a personal account vs a school-approved platform
  - How we handle it: our commitments (not certifications; Arena claims no compliance certification)
  - FULL pages (Technology, Schools) also carry the law behind it (PIPL, GDPR, PDPA; quotes verified in
    LEGAL-SOURCES.md; general information, not legal advice) and the checklist to use before adopting any AI tool
    (numbered, printable). Teachers and Partnerships link to it.
Commitments: approved platforms only, data rules agreed first, and teachers' own materials instead of student records
were already on the site (Technology, Teachers, Schools). New, stated at Phillip's request (Oct 17): no student
personal data in personal or consumer accounts; anonymized or sample data for practice; every teacher session covers
whose account a tool runs in and what its data agreement says; we follow the school's data-protection lead.
CN copy is marked for JJ review. Icons: Lucide (ISC), tools/lucide_icons.json.
  python3 tools/data_section.py           write
  python3 tools/data_section.py --check   report pages that would change
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = json.load(open(os.path.join(ROOT, 'tools', 'lucide_icons.json')))['icons']
PAGES = [('programs/teacher-training', False), ('schools/technology', True), ('schools', True), ('partnerships', False)]


def ic(name, cls='ds-ic'):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>' % (cls, ICONS[name]))


C = dict(
  en=dict(
    k='Student data comes first', h='Before which tool, ask: <em>whose account is it?</em>',
    l='Our first job is safeguarding students. The same AI tool can be safe or unsafe for student data, depending on the account it runs in.',
    rows=['Terms', 'Data agreement', 'Safeguards set by', 'Student data'],
    left=('A personal account', 'Signed up by one person', ['Consumer terms, accepted by one user', 'None with the school', 'The provider', 'Not approved for student data']),
    right=('A school-approved platform', 'Set up and managed by the school', ['An enterprise agreement with the school', 'Yes, agreed by the school', 'The school', 'Approved, under the school’s policy']),
    hk='How we handle it',
    commit=[('building-2', 'Inside your approved platforms', 'We work only in the accounts and tools your school approves, and agree the data rules with your team before any session.'),
            ('lock', 'No student data in personal accounts', 'Student names, work, and records never go into a personal or consumer account.'),
            ('file-text', 'Sample data for practice', 'Teacher sessions use teachers’ own materials or anonymized sample data, not student records.'),
            ('eye', 'AI use disclosed', 'Learners say which steps they handed to AI, and how they used it.'),
            ('search-check', 'Teachers learn to check the terms', 'Every teacher session covers whose account a tool runs in and what its data agreement says.'),
            ('shield-check', 'Your data-protection lead decides', 'We follow your data-protection officer and policy, and adjust when they do.')],
    lk='The law behind it',
    laws=[('China', 'Personal Information Protection Law (PIPL), in force since Nov 1, 2021',
           'Personal information of children under 14 is sensitive personal information (Art. 28). Processing it needs the consent of a parent or guardian, and dedicated processing rules (Art. 31).',
           'https://www.cac.gov.cn/2021-08/20/c_1631050028355286.htm', 'Official text (Chinese)'),
          ('European Union', 'General Data Protection Regulation (GDPR)',
           'Depending on its location and families, a school may also fall under the GDPR. For online services offered directly to a child, consent below 16 must come from a parent; member states may set 13 to 16 (Art. 8).',
           'https://eur-lex.europa.eu/eli/reg/2016/679/oj', 'Official text (EUR-Lex)'),
          ('Thailand', 'Personal Data Protection Act B.E. 2562 (2019)',
           'The data controller is whoever has the power to decide how personal data is collected, used, or disclosed (Section 6). For student data, that is the school.',
           'https://www.pdpc.or.th/', 'Personal Data Protection Committee')],
    note='General information, not legal advice. Your school’s data-protection lead decides what applies.',
    ck='Before adopting any AI tool', ch='Eight questions to ask first.', cp='Print the checklist',
    checks=[('user-round', 'Whose account is it?', 'A personal account, or one the school approves and manages?'),
            ('file-text', 'Is there a data agreement with the school?', 'Signed by the school, not accepted by one user.'),
            ('map-pin', 'Where is data stored and processed?', 'And does that fit the laws your school follows?'),
            ('users', 'Will minors use it?', 'If so, is parental consent in place where the law requires it?'),
            ('trash-2', 'How long is data kept?', 'Can the school delete it, and how?'),
            ('brain', 'Does the provider train on what users type or upload?', 'Can that be switched off for the school?'),
            ('settings', 'What can school administrators control?', 'Accounts, sharing, and activity logs.'),
            ('megaphone', 'How will families be told?', 'Which tools are used, and for what.')],
    more=('/schools/technology#student-data', 'The full checklist and the law behind it'),
  ),
  cn=dict(
    k='学生数据放在第一位', h='先别问用哪个工具，<em>先问是谁的账号。</em>',
    l='我们的首要职责是保护学生。同一个AI工具，对学生数据是否安全，取决于它运行在谁的账号里。',
    rows=['条款', '数据协议', '保护措施由谁设定', '学生数据'],
    left=('个人账号', '由个人自行注册', ['面向消费者的条款，由个人接受', '与学校之间没有', '服务提供方', '未获准使用学生数据']),
    right=('学校认可的平台', '由学校开通和管理', ['与学校签订的企业协议', '有，由学校签订', '学校', '获准使用，遵循学校的政策']),
    hk='我们的做法',
    commit=[('building-2', '只在学校认可的平台里', '我们只使用学校认可的账号和工具，并在任何课程开始前与贵校团队商定数据规则。'),
            ('lock', '学生数据不进个人账号', '学生的姓名、作品和记录，绝不进入个人或面向消费者的账号。'),
            ('file-text', '练习用示例数据', '教师培训使用老师自己的材料或匿名的示例数据，不使用学生记录。'),
            ('eye', '如实说明AI的使用', '学习者说明哪些步骤交给了AI，以及如何使用。'),
            ('search-check', '老师学会查看条款', '每一次教师培训都会讲到工具运行在谁的账号里，以及它的数据协议怎么写。'),
            ('shield-check', '由贵校的数据保护负责人决定', '我们遵循贵校的数据保护负责人和政策，并随之调整。')],
    lk='相关法律',
    laws=[('中国', '《中华人民共和国个人信息保护法》，2021年11月1日起施行',
           '不满十四周岁未成年人的个人信息属于敏感个人信息（第二十八条）。处理这类信息，应当取得父母或其他监护人的同意，并制定专门的个人信息处理规则（第三十一条）。',
           'https://www.cac.gov.cn/2021-08/20/c_1631050028355286.htm', '官方文本'),
          ('欧盟', '《通用数据保护条例》（GDPR）',
           '视学校所在地和学生家庭情况，学校也可能适用GDPR。对于直接面向儿童的在线服务，16岁以下儿童须由家长同意；成员国可将年龄定在13至16岁之间（第8条）。',
           'https://eur-lex.europa.eu/eli/reg/2016/679/oj', '官方文本（EUR-Lex）'),
          ('泰国', '《个人数据保护法》（PDPA，佛历2562年，即2019年）',
           '数据控制者是有权决定如何收集、使用或披露个人数据的一方（第6条）。就学生数据而言，就是学校。',
           'https://www.pdpc.or.th/', '泰国个人数据保护委员会')],
    note='以上为一般性信息，不构成法律意见。具体适用哪些规定，由贵校的数据保护负责人判断。',
    ck='引入任何AI工具之前', ch='先问这八个问题。', cp='打印这份清单',
    checks=[('user-round', '这是谁的账号？', '个人账号，还是由学校认可并管理的账号？'),
            ('file-text', '有没有与学校签订的数据协议？', '由学校签订，而不是由某个用户点击接受。'),
            ('map-pin', '数据存储和处理在哪里？', '是否符合贵校所遵循的法律？'),
            ('users', '会有未成年人使用吗？', '如有，在法律要求的情况下是否已取得家长同意？'),
            ('trash-2', '数据保存多久？', '学校能否删除，如何删除？'),
            ('brain', '服务提供方会用用户输入或上传的内容训练模型吗？', '能否为学校关闭这一功能？'),
            ('settings', '学校管理员能管控哪些内容？', '账号、共享和使用记录。'),
            ('megaphone', '如何告知家长？', '用了哪些工具，用来做什么。')],
    more=('/schools/technology-cn#student-data', '完整清单与相关法律'),
  ),
)


def section(lang, full):
    c = C[lang]
    jj = '<!-- JJ review: student data section CN copy (DATA-BRIEF, Oct 17, 2026) -->\n' if lang == 'cn' else ''

    def col(side, icon, cls):
        t, sub, vals = c[side]
        rows = ''.join('<div class="dt-row"><dt>%s</dt><dd>%s%s</dd></div>' % (r, ic('x' if side == 'left' else 'check', 'ds-ic dt-mk'), v)
                       for r, v in zip(c['rows'], vals))
        return ('<div class="dt-col %s">%s<h3>%s</h3><p class="dt-sub">%s</p><dl>%s</dl></div>' % (cls, ic(icon, 'ds-ic lg'), t, sub, rows))
    diagram = ('<div class="dt-pair reveal" role="group" aria-label="%s">%s<span class="dt-vs" aria-hidden="true">%s</span>%s</div>'
               % (re.sub(r'<[^>]+>', '', c['h']), col('left', 'user-round', 'is-personal'), 'vs' if lang == 'en' else '对比', col('right', 'school', 'is-school')))
    commits = ''.join('<li>%s<div><h3>%s</h3><p>%s</p></div></li>' % (ic(i), a, b) for i, a, b in c['commit'])
    out = [diagram, '<div class="dt-block reveal"><span class="ds-eyebrow">%s</span><ul class="dt-commit">%s</ul></div>' % (c['hk'], commits)]
    if full:
        laws = ''.join('<li class="ds-card"><span class="ds-eyebrow is-muted">%s</span><h3>%s</h3><p>%s</p><a class="tlink" href="%s" rel="noopener">%s →</a></li>'
                       % l for l in c['laws'])
        out.append('<div class="dt-block reveal"><span class="ds-eyebrow">%s</span><ul class="ds-grid ds-grid-3 dt-laws">%s</ul><p class="dt-note">%s</p></div>'
                   % (c['lk'], laws, c['note']))
        checks = ''.join('<li><div><b>%s</b><span>%s</span></div></li>' % (a, b) for i, a, b in c['checks'])   # numbers only (r2: number + icon was busy)
        out.append('<div class="dt-check reveal" id="data-checklist"><div class="dt-check-head"><div><span class="ds-eyebrow">%s</span><h3>%s</h3></div>'
                   '<button type="button" class="btn btn-ghost dt-print" data-print-checklist>%s%s</button></div><ol>%s</ol></div>'
                   % (c['ck'], c['ch'], ic('printer'), c['cp'], checks))
    else:
        out.append('<p class="dt-more reveal"><a class="tlink" href="%s">%s →</a></p>' % c['more'])
    return ('<!-- data:start -->\n%s<section class="ds-section is-alt dt-sec" id="student-data" data-screen-label="Student data"><div class="container">'
            '<header class="ds-head reveal"><span class="ds-eyebrow">%s</span><h2 class="ds-h2">%s</h2><p class="ds-lede">%s</p></header>%s</div></section>\n'
            '%s<!-- data:end -->' % (jj, c['k'], c['h'], c['l'], ''.join(out), '<script src="/data-print.js" defer></script>\n' if full else ''))


def apply(s, lang, full):
    sec = section(lang, full)
    if '<!-- data:start -->' in s:
        return re.sub(r'(?s)<!-- data:start -->.*?<!-- data:end -->', lambda m: sec, s)
    i = s.index('id="pressures"')
    j = s.index('</section>', i) + len('</section>')
    j = s.index('<!-- /depth:a -->', j) + len('<!-- /depth:a -->') if s.find('<!-- /depth:a -->', j) != -1 and s.find('<!-- /depth:a -->', j) < s.find('<section', j) else j
    return s[:j] + '\n' + sec + s[j:]


if __name__ == '__main__':
    check = '--check' in sys.argv
    n = 0
    for stem, full in PAGES:
        for lang, f in (('en', stem + '.html'), ('cn', stem + '-cn.html')):
            p = os.path.join(ROOT, f)
            s = open(p, encoding='utf-8').read()
            t = apply(s, lang, full)
            if t != s:
                n += 1
                if not check:
                    open(p, 'w', encoding='utf-8').write(t)
    print(('Would change' if check else 'Changed') + ' %d pages' % n)
