"""AI fluency for the whole staff (FLUENCY-BRIEF, Oct 17, 2026), EN + CN, on Teachers and Schools.

Written between <!-- fluency:start --> and <!-- fluency:end --> right after the student data section
(tools/data_section.py). Positioning: a few early adopters are already there; we bring everyone else up, safely,
inside the school's rules. No percentages: the chart is an illustrative shape (labeled as such), not data.
  - the five-level teacher fluency scale, as a staircase
  - the model: baseline self-assessment, train each group up one level, re-measure each term (a distribution shift),
    level 5 teachers become in-house coaches, all inside the student-data guardrails (#student-data)
  - a self-assessment: pick the statement that fits (native radio buttons, keyboard accessible); the result shows
    in place; nothing is sent or stored (fluency.js, client-side only)
CN copy is marked for JJ review.
  python3 tools/fluency_section.py           write
  python3 tools/fluency_section.py --check   report pages that would change
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = json.load(open(os.path.join(ROOT, 'tools', 'lucide_icons.json')))['icons']
PAGES = ['programs/teacher-training', 'schools']


def ic(name, cls='ds-ic'):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>' % (cls, ICONS[name]))


C = dict(
  en=dict(
    k='AI fluency for the whole staff', h='A few early adopters are there. <em>We bring everyone else up.</em>',
    l='Most schools have a few teachers already building with AI. We bring the rest of the staff up to par, safely, inside your school’s rules.',
    sk='Five levels of teacher fluency',
    levels=[('Unaware', 'Hasn’t used AI, or avoids it.'), ('Curious', 'Tries chat tools now and then.'),
            ('Practitioner', 'Uses approved tools weekly for planning, feedback, and admin.'),
            ('Designer', 'Builds AI into lessons, and teaches students to use it responsibly.'),
            ('Builder', 'Creates tools for colleagues, and leads others.')],
    lvl='Level',
    mk='How we move the whole staff',
    model=[('list-checks', 'Baseline', 'A short self-assessment places every teacher on the scale.'),
           ('users', 'One level up', 'We train each group up one level, starting where they are.'),
           ('search-check', 'Each term', 'We re-measure each term, so leadership sees the whole curve shift.'),
           ('user-check', 'In-house coaches', 'Level 5 teachers become coaches for their colleagues.')],
    guard=('#student-data', 'All of it inside your student-data guardrails'),
    chart_cap='Illustrative shape, not data: the staff curve before, and after a term of training.',
    before='Before', after='After a term',
    qk='Where are you now?', qh='Pick the statement that fits you best.',
    q=['I haven’t used AI yet, or I avoid it.', 'I try chat tools now and then.',
       'I use approved AI tools every week for planning, feedback, or admin.',
       'I build AI into my lessons and teach students to use it responsibly.',
       'I make tools for colleagues and help others get started.'],
    res='You’re at level {n}: {name}.', nxt='Next: level {n}, {name}. {desc}', top='This is the level that coaches colleagues.',
    priv='Nothing you pick here is sent or stored. It stays in your browser.',
  ),
  cn=dict(
    k='全体教职员工的AI素养', h='少数老师已经走在前面，<em>我们带上其他所有人。</em>',
    l='大多数学校都有几位老师已经在用AI做东西。我们帮助其余教职员工安全地跟上，而且始终在学校的规则之内。',
    sk='教师AI素养的五个层级',
    levels=[('未接触', '还没用过AI，或刻意回避。'), ('好奇', '偶尔试用聊天类工具。'),
            ('实践者', '每周用学校认可的工具备课、写反馈和处理行政事务。'),
            ('设计者', '把AI融入课程，并教学生负责任地使用。'),
            ('构建者', '为同事制作工具，并带动他人。')],
    lvl='层级',
    mk='如何带动全体教职员工',
    model=[('list-checks', '基线', '通过简短的自我评估，确定每位老师所在的层级。'),
           ('users', '各升一级', '从每组老师当前的层级出发，帮助他们提升一级。'),
           ('search-check', '每学期', '每学期重新评估，让学校管理层看到整体曲线的移动。'),
           ('user-check', '校内教练', '第五层级的老师成为同事的教练。')],
    guard=('#student-data', '全部在学生数据保护的规则之内'),
    chart_cap='示意图形，并非数据：培训前与一个学期后的教职员工分布。',
    before='培训前', after='一个学期后',
    qk='您现在在哪一级？', qh='选择最符合您的一项。',
    q=['我还没用过AI，或者在回避它。', '我偶尔试用聊天类工具。', '我每周用学校认可的AI工具备课、写反馈或处理行政事务。',
       '我把AI融入课程，并教学生负责任地使用。', '我为同事制作工具，并帮助别人起步。'],
    res='您在第{n}层级：{name}。', nxt='下一步：第{n}层级“{name}”。{desc}', top='这是可以带动同事的层级。',
    priv='您在这里的选择不会被发送或保存，只留在您的浏览器中。',
  ),
)


def curve(cx, w=640, h=150, base=128, amp=104, sd=78):
    # an illustrative bell shape centered at cx (smooth path from sampled points); not data
    import math
    pts = [(x, base - amp * math.exp(-((x - cx) ** 2) / (2 * sd * sd))) for x in range(0, w + 1, 16)]
    return 'M' + ' L'.join('%d %.1f' % p for p in pts)


def chart(c):
    xs = [64, 192, 320, 448, 576]
    ticks = ''.join('<text x="%d" y="148" text-anchor="middle">%d</text>' % (x, i + 1) for i, x in enumerate(xs))
    return ('<figure class="fl-chart"><svg viewBox="0 0 640 156" role="img" aria-label="%s">'
            '<line x1="16" y1="128" x2="624" y2="128" class="fl-axis" />'
            '<path d="%s L640 128 L0 128 Z" class="fl-area-a" /><path d="%s" class="fl-line-a" />'
            '<path d="%s L640 128 L0 128 Z" class="fl-area-b" /><path d="%s" class="fl-line-b" />'
            '<g class="fl-ticks">%s</g></svg>'
            '<figcaption><span class="fl-key"><i class="a"></i>%s</span><span class="fl-key"><i class="b"></i>%s</span><span class="fl-cap">%s</span></figcaption></figure>'
            % (c['chart_cap'], curve(170), curve(170), curve(390), curve(390), ticks, c['before'], c['after'], c['chart_cap']))


def section(lang):
    c = C[lang]
    jj = '<!-- JJ review: AI fluency section CN copy (FLUENCY-BRIEF, Oct 17, 2026) -->\n' if lang == 'cn' else ''
    steps = ''.join('<li style="--s:%d"><span class="fl-n">%s %d</span><b>%s</b><span>%s</span></li>' % (i, c['lvl'], i + 1, n, d)
                    for i, (n, d) in enumerate(c['levels']))
    model = ''.join('<li>%s<div><b>%s</b><span>%s</span></div></li>' % (ic(i), a, b) for i, a, b in c['model'])
    opts = ''.join('<label class="fl-opt"><input type="radio" name="fl-level" value="%d" /><span class="fl-opt-n">%d</span><span>%s</span></label>'
                   % (i + 1, i + 1, q) for i, q in enumerate(c['q']))
    data = json.dumps(dict(levels=[dict(name=n, desc=d) for n, d in c['levels']], res=c['res'], nxt=c['nxt'], top=c['top']), ensure_ascii=False)
    quiz = ('<form class="fl-quiz" data-fluency onsubmit="return false"><fieldset><legend><span class="ds-eyebrow">%s</span><b>%s</b></legend>%s</fieldset>'
            '<p class="fl-result" aria-live="polite"></p><p class="fl-priv">%s</p>'
            '<script type="application/json" class="fl-data">%s</script></form>' % (c['qk'], c['qh'], opts, c['priv'], data))
    return ('<!-- fluency:start -->\n%s<section class="ds-section fl-sec" id="ai-fluency" data-screen-label="AI fluency"><div class="container">'
            '<header class="ds-head reveal"><span class="ds-eyebrow">%s</span><h2 class="ds-h2">%s</h2><p class="ds-lede">%s</p></header>'
            '<div class="fl-scale reveal"><span class="ds-eyebrow">%s</span><ol class="fl-stairs">%s</ol></div>'
            '<div class="fl-grid reveal"><div><span class="ds-eyebrow">%s</span><ol class="fl-model">%s</ol><p class="fl-guard"><a class="tlink" href="%s">%s →</a></p></div><div>%s</div></div>'
            '%s</div></section>\n<script src="/fluency.js" defer></script>\n<!-- fluency:end -->'
            % (jj, c['k'], c['h'], c['l'], c['sk'], steps, c['mk'], model, c['guard'][0], c['guard'][1], chart(c), quiz))


def apply(s, lang):
    sec = section(lang)
    if '<!-- fluency:start -->' in s:
        return re.sub(r'(?s)<!-- fluency:start -->.*?<!-- fluency:end -->', lambda m: sec, s)
    j = s.index('<!-- data:end -->') + len('<!-- data:end -->')
    return s[:j] + '\n' + sec + s[j:]


if __name__ == '__main__':
    check = '--check' in sys.argv
    n = 0
    for stem in PAGES:
        for lang, f in (('en', stem + '.html'), ('cn', stem + '-cn.html')):
            p = os.path.join(ROOT, f)
            s = open(p, encoding='utf-8').read()
            t = apply(s, lang)
            if t != s:
                n += 1
                if not check:
                    open(p, 'w', encoding='utf-8').write(t)
    print(('Would change' if check else 'Changed') + ' %d pages' % n)
