"""Enforce the photo rules (standing content rules; DEPTH-BRIEF photo pass): never the cohort group photo
(isb-cohort, isb-2026/cohort), never prize cheques (pilot-check, isb-winners). Each figure that used one gets an
approved real photo, with alt text and caption that say what the new photo shows (EN and CN). Idempotent.
  python3 tools/photo_rules.py           write
  python3 tools/photo_rules.py --check   report files that would change, and any banned photo left anywhere
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANNED = re.compile(r'/photos/(?:isb-hq/isb-cohort|isb-2026/cohort|isb-cohort|mix/pilot-check|pilot-check|isb-hq/isb-winners|isb-winners|mix/pilot-classroom-800|pilot-classroom\.jpg)[-."]')
# straight swaps: a cleaned copy of the same photo (pilot-classroom: the room screen showed another organization's
# name; the copy blurs only the screen)
SWAP = {'/photos/mix/pilot-classroom-800.webp': '/photos/mix/pilot-classroom-noscreen-800.webp'}

# replacement photos: key -> (src 800, src large or None, EN alt/caption, CN alt/caption)
PH = {
    'parents': ('/photos/isb-2026/parents-audience-800.webp', '/photos/isb-2026/parents-audience-1600.webp',
                'Families at a student demo day, Beijing 2026', '家长在学生路演日现场，北京，2026年'),
    'pitchteam': ('/photos/isb-2026/pitch-team-800.webp', '/photos/isb-2026/pitch-team-1600.webp',
                  'Presenting to the panel, Beijing 2026', '向评委展示，北京，2026年'),
    'demolaptop': ('/photos/isb-2026/demo-laptop-800.webp', '/photos/isb-2026/demo-laptop-1600.webp',
                   'Students present a finished product, Beijing 2026', '学生展示做完的产品，北京，2026年'),
    'mentors': ('/photos/isb-2026/mentor-feedback-800.webp', '/photos/isb-2026/mentor-feedback-1600.webp',
                'Mentors respond to a student’s work, Beijing 2026', '导师对学生的作品给出反馈，北京，2026年'),
    'collab': ('/photos/steps/collab-stage-poster.webp', None,
               'Building together, Hong Kong 2025', '一起动手做，香港，2025年'),
}
# (file stem, banned src fragment) -> replacement key; the CN twin uses the same key
RULES = [
    ('programs/community-dialogues', 'isb-2026/cohort-800', 'parents'),
    ('programs/product-intensive', 'isb-2026/cohort-800', 'pitchteam'),
    ('programs/remake-your-favorite-app', 'isb-2026/cohort-800', 'demolaptop'),
    ('programs/website-portfolio-workshop', 'isb-2026/cohort-800', 'mentors'),
    ('contact', 'isb-hq/isb-cohort-800', 'mentors'),
    ('results', 'mix/pilot-check-800', 'collab'),
    ('results', 'isb-hq/isb-winners-800', 'pitchteam'),
    ('results', 'isb-hq/isb-cohort-800', 'mentors'),   # the strip already has the families photo
    ('index', 'isb-hq/isb-cohort-800', 'demolaptop'),
    ('index', 'mix/pilot-check-800', 'collab'),
    ('index', 'isb-hq/isb-winners-800', 'pitchteam'),
]


def swap_figure(fig, key, cn):
    src, big, en, zh = PH[key]
    text = zh if cn else en
    fig = re.sub(r'<img src="/photos/[^"]+"', '<img src="%s"' % src, fig, count=1)
    if big:
        fig = re.sub(r' srcset="[^"]*"', ' srcset="%s 800w, %s 1600w"' % (src, big), fig, count=1)
    else:
        fig = re.sub(r' srcset="[^"]*"', '', fig, count=1)
    fig = re.sub(r'(<img src="[^"]+"[^>]*?) alt="[^"]*"', lambda m: m.group(1) + ' alt="%s"' % text, fig, count=1)
    fig = re.sub(r' style="object-position:[^"]*"', '', fig, count=1)
    # caption: keep any leading seal image or place span; replace the trailing caption words
    def cap(m):
        inner = m.group(1)
        lead = ''.join(re.findall(r'<img[^>]*>|<span>[^<]*</span>', inner))
        if '<span>' in lead:   # homepage gallery: <span>place · year</span>title
            place = 'Hong Kong · 2025' if key == 'collab' else 'Beijing · 2026'
            if cn:
                place = '香港 · 2025' if key == 'collab' else '北京 · 2026'
            title = text.split(',')[0].split('，')[0]
            return '<figcaption><span>%s</span>%s</figcaption>' % (place, title)
        if re.fullmatch(r'\s*(Beijing, 2026|北京，2026年|2026年，北京)\s*', re.sub(r'<[^>]+>', '', inner)):
            return m.group(0)   # contact keeps its short place line
        return '<figcaption>%s%s</figcaption>' % (lead, text)
    fig = re.sub(r'(?s)<figcaption>(.*?)</figcaption>', cap, fig, count=1)
    return fig


def apply(s, frag, key, cn):
    out, pos = [], 0
    for m in re.finditer(r'(?s)<figure\b[^>]*>(?:(?!</figure>).)*?/photos/%s(?:(?!</figure>).)*?</figure>' % re.escape(frag[:-4] if frag.endswith('-800') else frag), s):
        if frag not in m.group(0):
            continue
        out.append(s[pos:m.start()])
        out.append(swap_figure(m.group(0), key, cn))
        pos = m.end()
    out.append(s[pos:])
    return ''.join(out)


if __name__ == '__main__':
    check = '--check' in sys.argv
    n = 0
    for stem, frag, key in RULES:
        for f, cn in ((stem + '.html', False), (stem + '-cn.html', True)):
            p = os.path.join(ROOT, f)
            s = open(p, encoding='utf-8').read()
            t = apply(s, frag, key, cn)
            if t != s:
                n += 1
                if not check:
                    open(p, 'w', encoding='utf-8').write(t)
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in ('decks', 'talks', '.git', 'node_modules') and not x.startswith('.')]
        for f in files:
            if f.endswith('.html'):
                p = os.path.join(d, f)
                s = open(p, encoding='utf-8').read()
                t = s
                for a, b in SWAP.items():
                    t = t.replace(a, b)
                if t != s:
                    n += 1
                    if not check:
                        open(p, 'w', encoding='utf-8').write(t)
    left = []
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in ('decks', 'talks', '.git', 'node_modules') and not x.startswith('.')]
        for f in files:
            if f.endswith('.html'):
                p = os.path.join(d, f)
                for m in BANNED.finditer(re.sub(r'(?s)<!--.*?-->', '', open(p, encoding='utf-8').read())):
                    left.append(os.path.relpath(p, ROOT))
    print(('Would change' if check else 'Changed') + ' %d file edits; banned photos left: %d %s' % (n, len(left), sorted(set(left))))
