"""Past talks page, EN + CN (HERO2-BRIEF D, Oct 17, 2026): every past talk, workshop and speaking engagement in the
repo, as session cards, newest first, with an audience filter. Real events only; each one's source is listed in
PAST-TALKS-SOURCES.md, and a field that is not known is left out. Slides are linked, never copied: talks/ and
decks/ are not modified (the card images are 800px exports of each deck's cover slide, in photos/talks/).

The page is built from the Results page's shell on its first run; after that only the parts between the markers
change. The hero photos come from tools/hero_markup.py, the header and footer from tools/site_nav.py.
  python3 tools/past_talks.py           write past-talks.html and past-talks-cn.html
  python3 tools/past_talks.py --check   report pages that would change
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (audience key, date shown, card data per language). Newest first; month-only dates after exact dates of the
# same month (the day is not recorded), undated last.
TALKS = [
    ('parents', dict(
        en=dict(date='Oct 14, 2026', where='ISB PTA Parent Coffee · International School of Beijing', city='Beijing',
                title='Our Kids’ Jobs Don’t Exist Yet. So Which Skills Will Matter?',
                dl=[('For', 'ISB parents, hosted by the ISB PTA'), ('Speakers', 'Jing Jing Yang and Phillip An'), ('Language', 'English and Chinese slides')],
                img=('/photos/talks/isb-parent-coffee-cover-800.webp', 'Cover slide of the talk'),
                links=[('/talks/2026-10-isb-parent-coffee', 'Slides and resources'), ('/talks/2026-10-isb-parent-coffee/slides-en.pdf', 'PDF'), ('/events/isb-parent-coffee', 'About the session')]),
        cn=dict(date='2026年10月14日', where='ISB PTA 家长咖啡会 · 北京顺义国际学校', city='北京',
                title='孩子们未来的工作还不存在，那么，哪些能力最重要？',
                dl=[('对象', 'ISB 家长，由 ISB PTA 主办'), ('主讲', '羊筱涵、安广宁'), ('语言', '中英文幻灯片')],
                img=('/photos/talks/isb-parent-coffee-cover-cn-800.webp', '讲座封面幻灯片'),
                links=[('/talks/2026-10-isb-parent-coffee', '幻灯片与资料'), ('/talks/2026-10-isb-parent-coffee/slides-cn.pdf', 'PDF'), ('/events/isb-parent-coffee-cn', '活动介绍')]))),
    ('students', dict(
        en=dict(date='October 2026', where='Info session with Lux Scholar', city=None,
                title='AI Advantage Bootcamp: the info session',
                dl=[('For', 'College students and early-career professionals'), ('Language', 'Chinese')],
                img=('/photos/talks/lux-bootcamp-info-cover-800.webp', 'Cover slide of the info session (in Chinese)'),
                links=[('/talks/2026-10-lux-bootcamp-info/deck', 'Slides'), ('/talks/2026-10-lux-bootcamp-info/slides-cn.pdf', 'PDF'), ('/zero-to-launch', 'The bootcamp')]),
        cn=dict(date='2026年10月', where='与千麓学者合办的说明会', city=None,
                title='AI职场先发营：项目说明会',
                dl=[('对象', '大学生与职场新人'), ('语言', '中文')],
                img=('/photos/talks/lux-bootcamp-info-cover-800.webp', '说明会封面幻灯片'),
                links=[('/talks/2026-10-lux-bootcamp-info/deck', '幻灯片'), ('/talks/2026-10-lux-bootcamp-info/slides-cn.pdf', 'PDF'), ('/zero-to-launch-cn', '训练营介绍')]))),
    ('educators', dict(
        en=dict(date=None, where='Schwarzman College, Tsinghua University', city='Beijing',
                title='Staff training at Schwarzman College',
                dl=[('For', 'Staff, Schwarzman College'), ('Format', 'Hands-on workshop'), ('Taught by', 'Phillip An')],
                img=None, links=[('/results#tsinghua', 'See results')]),
        cn=dict(date=None, where='清华大学苏世民书院', city='北京',
                title='苏世民书院教职员工培训',
                dl=[('对象', '苏世民书院教职员工'), ('形式', '动手工作坊'), ('主讲', '安广宁')],
                img=None, links=[('/results-cn#tsinghua', '查看成果')]))),
]
NEXT = dict(
    en=dict(k='Up next', date='Oct 18, 2026', where='ACAMIS Technology Conference · Keystone Academy, Beijing',
            title='From Lab to Classroom: Running an AI Student Program Inside a School', link=('/events/acamis-tech-2026', 'Session details')),
    cn=dict(k='下一场', date='2026年10月18日', where='ACAMIS 2026 技术大会 · 北京鼎石学校',
            title='从实验室到课堂：如何在学校里开展AI学生项目', link=('/events/acamis-tech-2026-cn', '活动详情')))
T = dict(
    en=dict(title='Past talks · Arena School', desc='Talks and workshops the Arena School team has led for parents, students, and school staff, newest first, with slides where we have them.',
            eyebrow='Past talks', h1='Talks and <em>workshops.</em>',
            lede='Sessions the Arena School team has led for parents, students, and school staff, newest first, with the slides where we have them.',
            k='Past talks', h='Where we have <em>spoken.</em>', filt='Show talks for', all='All',
            aud={'parents': 'Parents', 'students': 'Students', 'educators': 'Educators and staff'}, cta=('/programs/conferences', 'Invite us to speak')),
    cn=dict(title='往期讲座 · Arena School', desc='Arena School 团队为家长、学生和学校教职员工做过的讲座与工作坊，按时间倒序，附有幻灯片。',
            eyebrow='往期讲座', h1='讲座与<em>工作坊。</em>',
            lede='Arena School 团队为家长、学生和学校教职员工做过的分享，按时间倒序排列，有幻灯片的都附上了。',
            k='往期讲座', h='我们讲过的<em>内容。</em>', filt='按对象筛选', all='全部',
            aud={'parents': '家长', 'students': '学生', 'educators': '教育者与教职员工'}, cta=('/programs/conferences-cn', '邀请我们分享')))


def card(aud, c, t):
    meta = ' · '.join(x for x in (c['date'], c['city']) if x)
    fig = ('<figure class="pt-fig"><img src="%s" alt="%s" width="800" height="450" loading="lazy" decoding="async" /></figure>' % c['img']) if c['img'] else ''
    dl = ''.join('<dt>%s</dt><dd>%s</dd>' % kv for kv in c['dl'])
    links = ''.join('<a class="tlink" href="%s"><span class="tl">%s</span> <span class="arr">→</span></a>' % l for l in c['links'])
    return ('<li class="ds-case pt-card reveal" data-aud="%s">%s<div class="pt-body"><span class="ds-eyebrow is-muted">%s</span>%s<h3>%s</h3>'
            '<p class="pt-where">%s</p><dl>%s</dl><p class="pt-links">%s</p></div></li>'
            % (aud, fig, t['aud'][aud], '<span class="pt-date">%s</span>' % meta if meta else '', c['title'], c['where'], dl, links))


def body(lang):
    t = T[lang]
    jj = '<!-- JJ review: Past talks page CN copy (HERO2-BRIEF D, Oct 17, 2026) -->\n' if lang == 'cn' else ''
    chips = ''.join('<button type="button" class="pt-chip" aria-pressed="%s" data-f="%s">%s</button>' % ('true' if k == 'all' else 'false', k, v)
                    for k, v in [('all', t['all'])] + list(t['aud'].items()))
    cards = ''.join(card(aud, d[lang], t) for aud, d in TALKS)
    n = NEXT[lang]
    nxt = ('<aside class="pt-next reveal"><span class="ds-eyebrow">%s</span><p><b>%s</b> · %s</p><h3>%s</h3><a class="tlink" href="%s"><span class="tl">%s</span> <span class="arr">→</span></a></aside>'
           % (n['k'], n['date'], n['where'], n['title'], n['link'][0], n['link'][1]))
    return ('<!-- pt:start -->\n%s<section class="ds-section" id="talks" data-screen-label="Past talks"><div class="container">'
            '<header class="ds-head reveal"><span class="ds-eyebrow">%s</span><h2 class="ds-h2">%s</h2></header>'
            '<div class="pt-chips reveal" role="group" aria-label="%s">%s</div>'
            '<ul class="pt-list">%s</ul>%s<p class="pt-cta reveal"><a class="btn btn-ghost" href="%s">%s <span class="arr">→</span></a></p>'
            '</div></section>\n<script src="/past-talks.js" defer></script>\n<!-- pt:end -->'
            % (jj, t['k'], t['h'], t['filt'], chips, cards, nxt, t['cta'][0], t['cta'][1]))


def build(lang, s):
    t = T[lang]
    sfx = '-cn' if lang == 'cn' else ''
    if '<!-- pt:start -->' not in s:   # first build from the Results shell: keep the hero, replace the rest of <main>
        i = s.index('</section>', s.index('cine-hero')) + len('</section>')
        s = s[:i] + '\n\n' + body(lang) + '\n\n' + s[s.index('</main>'):]
        s = s.replace('pg-results', 'pg-results pg-talks', 1)
    s = re.sub(r'(?s)<!-- pt:start -->.*?<!-- pt:end -->', lambda m: body(lang), s)
    s = re.sub(r'(?s)\s*<ul class="pp-glance reveal".*?</ul>', '', s, count=1)
    s = re.sub(r'(<div class="hero-eyebrow-row reveal"><span class="eyebrow">)[^<]*(</span>)', lambda m: m.group(1) + t['eyebrow'] + m.group(2), s, count=1)
    s = re.sub(r'(?s)(<h1 class="display reveal cs-h1">).*?(</h1>)', lambda m: m.group(1) + t['h1'] + m.group(2), s, count=1)
    s = re.sub(r'(?s)(<p class="lede sub reveal lede-56">).*?(</p>)', lambda m: m.group(1) + t['lede'] + m.group(2), s, count=1)
    s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % t['title'], s, count=1)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(attr), lambda m: m.group(1) + t['desc'] + m.group(2), s, count=1)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(attr), lambda m: m.group(1) + t['title'] + m.group(2), s, count=1)
    url = 'https://arenaschool.org/past-talks' + sfx
    s = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), s, count=1)
    s = re.sub(r'(<link rel="alternate" hreflang="en" href=")[^"]*(")', lambda m: m.group(1) + 'https://arenaschool.org/past-talks' + m.group(2), s)
    s = re.sub(r'(<link rel="alternate" hreflang="zh[^"]*" href=")[^"]*(")', lambda m: m.group(1) + 'https://arenaschool.org/past-talks-cn' + m.group(2), s)
    return s


if __name__ == '__main__':
    check = '--check' in sys.argv
    n = 0
    for lang, f, src in (('en', 'past-talks.html', 'results.html'), ('cn', 'past-talks-cn.html', 'results-cn.html')):
        p = os.path.join(ROOT, f)
        s = open(p if os.path.exists(p) else os.path.join(ROOT, src), encoding='utf-8').read()
        t = build(lang, s)
        if not os.path.exists(p) or t != open(p, encoding='utf-8').read():
            n += 1
            if not check:
                open(p, 'w', encoding='utf-8').write(t)
    print(('Would change' if check else 'Changed') + ' %d pages' % n)
