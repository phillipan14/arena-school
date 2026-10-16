"""cine4 hero on every site page (EN + CN), approved Oct 16, 2026 (FINAL-BRIEF.md).

Rewrites each page's hero section in place, idempotently:
  - the section keeps its classes (minus hero-inv, so hero-options.js leaves it alone) and gains
    `cine-hero` plus a per-page headline size (--cine-h1);
  - the old hero furniture inside it is removed: the riso field and scrim, the notebook background,
    the homepage side photo stays in the markup but is hidden by css/cine.css, and the photo band
    (.pro-hero-media) that the photo-led pass added;
  - a <!-- cine:start --> ... <!-- cine:end --> block goes in first: the photo slides (the first
    one eager with fetchpriority=high, the rest data-src for cine.js), the navy shade, and the
    empty layer cine.js fills with the light particle field;
  - the crest goes in as the first child of the hero copy (<!-- cine:crest -->);
  - /css/cine.css and /cine.js are linked once, and `zl-page` leaves the body (the nav stays solid white).
Photos follow PHOTO-PICKS.md (no cohort shot, no prize cheques, no other organizations' names).
Pages without a fitting photo use a bright general one, marked as a fallback here and in
PHOTO-SLOTS.md with a TODO-PHOTO comment in the page.

    python3 tools/hero_markup.py          # rewrite
    python3 tools/hero_markup.py --check  # report"""
import hashlib, html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = '--check' in sys.argv

# key: (small src, large src or None, desktop focus, phone focus, EN caption, CN caption)
# key: (small src, large src or None, natural aspect w/h, EN caption, CN caption,
#       faces as [x0, y0, x1, y1] fractions of the photo (e=1: already cut by the photo edge, so it must be cropped out),
#       desktop crop: z (base zoom), ox/oy (zoom origin), py (object-position y),
#       narrow pan: pa (start, 1 = right edge), pb (end), ps (still frame for reduced motion), pym (object-position y))
# Face boxes and crops were read off a 5% grid of each photo (CROP-BRIEF, Oct 16) and are verified by the crop check.
P = {
    'duo': ('/photos/isb-2026/pitch-duo-800.webp', '/photos/isb-2026/pitch-duo-1600.webp', 1.5,
            'Presenting at demo day, Beijing 2026', '路演日展示，北京，2026年',
            [[.49, .23, .63, .50, 0], [.80, .20, .93, .45, 0], [0, .20, .07, .42, 1]],
            dict(z=1.11, ox=.72, oy=.6, py=.25, kz=1.06, pa=1, pb=.2, pbs=.9, ps=.95, pat=1, pbt=.8, pst=.8, pym=.2)),
    'gesture': ('/photos/isb-hq/isb-pitch-gesture-800.webp', '/photos/isb-hq/isb-pitch-gesture-1400.webp', 4 / 3,
                'Pitching to the panel, Beijing 2026', '向评委路演，北京，2026年',
                [[.64, .11, .78, .40, 0], [.05, .11, .18, .31, 0]],
                dict(z=1.22, ox=1.0, oy=.2, py=.20, kz=1.06, pa=1, pb=.6, pbs=.8, ps=.85, pat=1, pbt=.97, pst=.15, pym=.2)),
    'mentors': ('/photos/isb-2026/mentor-feedback-800.webp', '/photos/isb-2026/mentor-feedback-1600.webp', 1.5,
                'Mentors react to a student demo, Beijing 2026', '导师为学生展示叫好，北京，2026年',
                [[.54, .13, .72, .42, 0], [0, .05, .17, .38, 1]],
                dict(z=1.27, ox=.8, oy=.3, py=.20, kz=1.06, pa=1, pb=.45, pbs=.75, ps=.75, pat=1, pbt=.95, pst=.97, pym=.2)),
    'hands': ('/photos/steps/collab-stage-poster.webp', None, 4 / 3,
              'Building together, Hong Kong 2025', '一起动手做，香港，2025年',
              [[.09, .35, .21, .50, 0], [.48, .31, .58, .47, 0], [.65, .09, .77, .27, 0]],
              dict(z=1, ox=.5, oy=.4, py=.3, kz=1.04, pa=1, pb=.72, pbs=.85, ps=.85, pat=.4, pbt=.1, pst=.3, pym=.2)),
}
# The Hong Kong still has faces spread across the frame, so on desktop (where the copy sits on the left)
# it is swapped for another photo in the same slot; it stays in the phone and tablet rotation.
WIDE_SUB = {'hands': ['duo', 'gesture', 'mentors']}

H1 = 'clamp(36px, 1.2rem + 2.8vw, 60px)'
H1_HOME = 'clamp(36px, 1.2rem + 3vw, 62px)'
H1_LONG = 'clamp(30px, 1rem + 2.2vw, 46px)'

# page stem: (photo keys, headline size, fallback TODO subject or None)
PAGES = {
    'index': (['duo', 'gesture', 'mentors'], H1_HOME, None),
    'programs/teacher-training': (['hands', 'mentors'], H1, 'Teachers at a hands-on Arena session, making a tool on their own laptops'),
    'schools/technology': (['hands', 'mentors'], H1, 'Tech coaches and IT staff at an Arena session, working on the school’s approved tools'),
    'schools': (['duo', 'gesture', 'mentors'], H1, None),
    'events/isb-winter-2027': (['duo', 'gesture', 'hands'], 'clamp(34px, 1.1rem + 2.6vw, 56px)', None),
    'events/acamis-tech-2026': (['gesture', 'duo'], H1_LONG, None),
    'events/isb-parent-coffee': (['mentors', 'duo'], H1_LONG, 'ISB PTA parent coffee on Oct 14, 2026: Jing Jing Yang and Phillip An with parents'),
    'programs/product-intensive': (['gesture', 'duo', 'hands'], H1, None),
    'programs/remake-your-favorite-app': (['hands', 'duo'], H1, None),
    'programs/website-portfolio-workshop': (['duo', 'hands'], H1, None),
    'programs/community-dialogues': (['mentors', 'duo'], H1, 'A Community Dialogues parent talk: families in conversation with the Arena team'),
    'programs/conferences': (['gesture', 'mentors'], H1, 'The Arena team leading a hands-on conference workshop for teachers'),
    'mentorship': (['mentors', 'gesture'], H1, None),
    'enroll': (['mentors', 'duo'], H1, None),
    'zero-to-launch': (['hands', 'gesture'], H1, 'College students and early-career professionals building with AI (first AI Advantage Bootcamp cohort)'),
    'about': (['mentors', 'hands'], H1, None),
    'approach': (['hands', 'gesture'], H1, None),
    'results': (['duo', 'gesture', 'hands'], H1, None),
    'partnerships': (['hands', 'duo'], H1, None),
    'contact': (['mentors', 'duo'], H1, 'The Arena team, smiling, ready to talk (a team photo)'),
}


def ver(path):
    return hashlib.sha1(open(os.path.join(ROOT, path), 'rb').read()).hexdigest()[:8]


def delay(i, n):
    """Animation delay for slot i of n: each photo owns a 14s window that starts with a 1.6s fade-in; at load
    the first photo is already 1.6s in (fully visible) and every other photo is mid-gap (invisible)."""
    return -round((1.6 - 14 * i) % (14 * n), 2) if n > 1 else 0


def srcset(key):
    small, large = P[key][0], P[key][1]
    return '%s 800w, %s 1600w' % (small, large) if large else '%s 1024w' % small


def wide_list(keys):
    """Desktop photos per slot: the Hong Kong still swaps for a photo the page does not already use."""
    out = []
    for k in keys:
        if k in WIDE_SUB:
            k = next(c for c in WIDE_SUB[k] if c not in keys and c not in out)
        out.append(k)
    return out


def slide(i, n, nk, wk, home):
    """One slot: a <picture> with the desktop photo (wk) as a source and the phone/tablet photo (nk) as the img."""
    w, m = P[wk][6], P[nk][6]
    kz = w['kz'] if home else round(1 + (w['kz'] - 1) / 2, 3)          # subpages: half the zoom
    pb = m['pb'] if home else m['pbs']                                   # subpages: a shorter pan
    style = ('--d:%ss;--z:%s;--kz:%s;--ox:%s%%;--oy:%s%%;--py:%s%%;--pa-m:%s;--pb-m:%s;--ps-m:%s;--pa-t:%s;--pb-t:%s;--ps-t:%s;--pym:%s%%'
             % (delay(i, n), w['z'], kz, round(w['ox'] * 100, 1), round(w['oy'] * 100, 1), round(w['py'] * 100, 1),
                m['pa'], pb, m['ps'], m['pat'], m['pbt'], m['pst'], round(m['pym'] * 100, 1)))
    faces = 'data-wide="%s" data-narrow="%s"' % (html.escape(repr([wk, P[wk][2], P[wk][5]]).replace("'", '"')),
                                                  html.escape(repr([nk, P[nk][2], P[nk][5]]).replace("'", '"')))
    if i == 0:
        src = '<source media="(min-width: 901px)" srcset="%s" sizes="100vw" />' % srcset(wk)
        img = '<img src="%s" srcset="%s" sizes="100vw" fetchpriority="high" loading="eager"' % (P[nk][0], srcset(nk))
    else:
        src = '<source media="(min-width: 901px)" data-srcset="%s" sizes="100vw" />' % srcset(wk)
        img = '<img data-src="%s" data-srcset="%s" sizes="100vw" loading="lazy"' % (P[nk][0], srcset(nk))
    return '<div class="cine-slide" style="%s"><picture>%s%s alt="" decoding="async" %s /></picture></div>' % (style, src, img, faces)


def cap(nk, wk, i, n, zh):
    c = 5 if zh else 4
    d = delay(i, n)
    if nk == wk:
        return '<span style="--d:%ss">%s</span>' % (d, html.escape(P[nk][c - 1]))
    return ('<span style="--d:%ss"><i class="is-w">%s</i><i class="is-n">%s</i></span>'
            % (d, html.escape(P[wk][c - 1]), html.escape(P[nk][c - 1])))


def block(keys, zh, todo, home):
    n = len(keys)
    wkeys = wide_list(keys)
    slides = ''.join(slide(i, n, nk, wk, home) for i, (nk, wk) in enumerate(zip(keys, wkeys)))
    caps = ''.join(cap(nk, wk, i, n, zh) for i, (nk, wk) in enumerate(zip(keys, wkeys)))
    note = '\n<!-- TODO-PHOTO: %s (fallback photos until then) -->' % todo if todo else ''
    return ('<!-- cine:start -->%s\n<div class="cine-media n-%d%s" aria-hidden="true">%s</div>'
            '<div class="cine-shade" aria-hidden="true"></div><div class="cine-field-light" aria-hidden="true"></div>'
            '<div class="cine-caps n-%d" aria-hidden="true">%s</div>\n<!-- cine:end -->' % (note, n, ' is-home' if home else '', slides, n, caps))


CREST = ('<!-- cine:crest --><div class="cine-crest" aria-hidden="true"><img src="/logos/arena/seal-ivory-512.png" alt="" width="108" height="108" decoding="async" /></div>')


def convert(s, keys, h1, todo, zh, home=False):
    s = re.sub(r'\n?<!-- cine:start -->.*?<!-- cine:end -->', '', s, flags=re.S)
    s = s.replace(CREST, '')
    m = re.search(r'<section class="((?:hero|hero-riso)\b[^"]*)"([^>]*)>', s)
    a = m.start(); b = s.index('</section>', a)
    hero = s[a:b]
    classes = [c for c in m.group(1).split() if c not in ('hero-inv', 'cine-hero')] + ['cine-hero']
    rest = re.sub(r'\s*style="--cine-h1:[^"]*"', '', m.group(2))
    open_tag = '<section class="%s"%s style="--cine-h1:%s">' % (' '.join(classes), rest, h1)
    body = hero[m.end() - a:]
    body = re.sub(r'\s*<div class="hero-bg"[^>]*></div>', '', body)
    body = re.sub(r'\s*<div class="hero-scrim"[^>]*></div>', '', body)
    body = re.sub(r'\s*<div class="pro-hero-bg"[^>]*>.*?</div></div>', '', body, flags=re.S)
    body = re.sub(r'\s*(?:<!-- TODO-PHOTO:[^>]*-->\s*)?<div class="(?:container|el-wrap) pro-hero-media">.*?</div>\n?(?=\s*$)', '', body, flags=re.S)
    body = '\n' + block(keys, zh, todo, home) + body
    copy = re.search(r'<div class="(?:hero-riso-copy|hero-copy[^"]*)">|<div class="el-wrap el-hero-grid[^"]*">\s*<div>', body)
    body = body[:copy.end()] + CREST + body[copy.end():]
    s = s[:a] + open_tag + body + s[b:]
    # the nav is solid white over these heroes; zl-page would restyle it for a dark, see-through header
    return re.sub(r'(<body class="[^"]*?)\s*\bzl-page\b', r'\1', s, count=1)


def assets(s):
    s = re.sub(r'<link rel="stylesheet" href="/css/(?:cine|hero-bg)\.css[^"]*" />\n', '', s)
    s = re.sub(r'<script src="/cine\.js[^"]*" defer></script>\n', '', s)
    s = s.replace('<link rel="stylesheet" href="/css/pro.css', '<link rel="stylesheet" href="/css/cine.css?v=%s" />\n<link rel="stylesheet" href="/css/pro.css' % ver('css/cine.css'), 1)
    tag = '<script src="/cine.js?v=%s" defer></script>\n' % ver('cine.js')
    i = s.find('<script src="/riso-field.js')
    if i != -1:
        j = s.index('\n', i) + 1; s = s[:j] + tag + s[j:]
    else:
        s = s.replace('<script src="/promo.js', tag + '<script src="/promo.js', 1)
    return s


if __name__ == '__main__':
    os.chdir(ROOT)
    changed = 0
    for stem, (keys, h1, todo) in PAGES.items():
        for page, zh in ((stem + '.html', False), (stem + '-cn.html', True)):
            if not os.path.exists(page):
                continue
            s = open(page, encoding='utf-8').read()
            n = assets(convert(s, keys, h1, todo, zh, stem == 'index'))
            if n != s:
                changed += 1
                if not CHECK:
                    open(page, 'w', encoding='utf-8').write(n)
    print(('Would change' if CHECK else 'Changed'), changed, 'pages')
