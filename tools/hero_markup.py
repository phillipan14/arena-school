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
P = {
    'duo': ('/photos/isb-2026/pitch-duo-800.webp', '/photos/isb-2026/pitch-duo-1600.webp', '62% 38%', '100% 30%',
            'Presenting at demo day, Beijing 2026', '路演日展示，北京，2026年'),
    'gesture': ('/photos/isb-hq/isb-pitch-gesture-800.webp', '/photos/isb-hq/isb-pitch-gesture-1400.webp', '60% 26%', '66% 22%',
                'Pitching to the panel, Beijing 2026', '向评委路演，北京，2026年'),
    'mentors': ('/photos/isb-2026/mentor-feedback-800.webp', '/photos/isb-2026/mentor-feedback-1600.webp', '50% 32%', '66% 30%',
                'Mentors react to a student demo, Beijing 2026', '导师为学生展示叫好，北京，2026年'),
    'hands': ('/photos/steps/collab-stage-poster.webp', None, '55% 40%', '60% 40%',
              'Building together, Hong Kong 2025', '一起动手做，香港，2025年'),
}

H1 = 'clamp(36px, 1.2rem + 2.8vw, 60px)'
H1_HOME = 'clamp(36px, 1.2rem + 3vw, 62px)'
H1_LONG = 'clamp(30px, 1rem + 2.2vw, 46px)'

# page stem: (photo keys, headline size, fallback TODO subject or None)
PAGES = {
    'index': (['duo', 'gesture', 'mentors', 'hands'], H1_HOME, None),
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


def slide(key, i, zh):
    small, large, focus, focus_m, cap_en, cap_cn = P[key]
    srcset = '%s 800w, %s 1600w' % (small, large) if large else ''
    attrs = ('src="%s"%s fetchpriority="high" loading="eager"' % (small, ' srcset="%s" sizes="100vw"' % srcset if srcset else '')) if i == 0 else \
            ('data-src="%s"%s loading="lazy"' % (small, ' data-srcset="%s" sizes="100vw"' % srcset if srcset else ''))
    return '<div class="cine-slide"><img %s alt="" decoding="async" style="--focus:%s;--focus-m:%s" /></div>' % (attrs, focus, focus_m)


def cap(key, zh):
    return '<span>%s</span>' % html.escape(P[key][5] if zh else P[key][4])


def block(keys, zh, todo):
    slides = ''.join(slide(k, i, zh) for i, k in enumerate(keys))
    note = '\n<!-- TODO-PHOTO: %s (fallback photos until then) -->' % todo if todo else ''
    caps = ''.join(cap(k, zh) for k in keys)
    return ('<!-- cine:start -->%s\n<div class="cine-media" aria-hidden="true">%s</div>'
            '<div class="cine-shade" aria-hidden="true"></div><div class="cine-field-light" aria-hidden="true"></div>'
            '<div class="cine-caps" aria-hidden="true">%s</div>\n<!-- cine:end -->' % (note, slides, caps))


CREST = ('<!-- cine:crest --><div class="cine-crest" aria-hidden="true"><img src="/logos/arena/seal-ivory-512.png" alt="" width="108" height="108" decoding="async" /></div>')


def convert(s, keys, h1, todo, zh):
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
    body = '\n' + block(keys, zh, todo) + body
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
            n = assets(convert(s, keys, h1, todo, zh))
            if n != s:
                changed += 1
                if not CHECK:
                    open(page, 'w', encoding='utf-8').write(n)
    print(('Would change' if CHECK else 'Changed'), changed, 'pages')
