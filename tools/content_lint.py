"""Enforce CONTENT-RULES.md: word and section budgets, block limits, banned phrases,
em dashes, and sentences duplicated across pages. Run from the site root:
    python3 tools/content_lint.py            # all pages
    python3 tools/content_lint.py about zero-to-launch
Exit code 1 if any page fails."""
import glob, re, sys, collections
from html.parser import HTMLParser

BUDGET = {  # page -> (max words, max sections)
    'index': (450, 7), 'mentorship': (700, 7), 'zero-to-launch': (700, 7),
    'case-studies/student-programs': (550, 6), 'case-studies/skill-workshops': (550, 6),
    'case-studies/parent-talks': (550, 6), 'case-studies/teacher-training': (550, 6),
    'programs/website-portfolio-workshop': (550, 6), 'programs/product-intensive': (550, 6),
    'programs/community-dialogues': (550, 6), 'programs/teacher-training': (550, 6),
    'schools': (500, 6), 'curriculum': (650, 5), 'approach': (650, 5), 'about': (650, 5),
    'results': (750, 6), 'partnerships': (450, 5), 'contact': (100, 2),
}
BLOCK = {'lede': 30, 'card': 25, 'detail': 30, 'faq': 45}
BANNED = [r'instead of writ', r'you (just )?review', r'type less', r'does (it|the work) for you', r'replace (you|teachers|your)', r'in minutes, not', r'never (mark|grade|write) again', r'\bweekend of marking', r'AI (builds|writes|grades|marks) (it|the|your)', r'替您完成', r'不再负责写', r'取代(老师|您|教师)', r'\bunlike school', r'school never', r'career teacher', r'\bNot [A-Z][^.]{0,40}\. Not ', r'waiting room', r'eulogy',
          r'creativity, taste', r'\bcourage\b.*\bjudgment\b', r'学校从不']
SKIP_TAGS = {'script', 'style', 'svg', 'nav', 'footer', 'head', 'noscript'}

class Page(HTMLParser):
    def __init__(s):
        super().__init__(); s.skip = 0; s.sections = 0; s.text = []; s.blocks = []; s.cur = None; s.details = []
    def handle_starttag(s, t, a):
        a = dict(a); cls = a.get('class') or ''
        if t in SKIP_TAGS: s.skip += 1
        if s.skip: return
        if t == 'section': s.sections += 1
        if a.get('data-detail'): s.details.append(a['data-detail'])
        kind = ('lede' if re.search(r'\b(lede|sub|thesis)\b', cls) else 'card' if re.search(r'\b(card-p|gc-sub|tile-body|hc-tex|fp-trip-card)\b', cls)
                else 'faq' if 'faq-a' in cls else None)
        if kind and t in ('p', 'div'): s.cur = [kind, t, []]; s.blocks.append(s.cur)
        s.text.append(' ')
    def handle_endtag(s, t):
        if t in SKIP_TAGS and s.skip: s.skip -= 1
        if s.cur and t == s.cur[1]: s.cur = None
    def handle_data(s, d):
        if s.skip: return
        s.text.append(d)
        if s.cur: s.cur[2].append(d)

def words(t): return re.findall(r"[A-Za-z0-9’']+", t)

def lint(names):
    fails = 0; sentences = collections.defaultdict(set)
    for name in names:
        f = name + '.html'
        try: src = open(f, encoding='utf-8').read()
        except FileNotFoundError: continue
        p = Page(); p.feed(src); text = ' '.join(''.join(p.text).split())
        n = len(words(text)); mw, ms = BUDGET.get(name, (700, 7)); probs = []
        if n > mw: probs.append(f'{n} words > {mw}')
        if p.sections > ms: probs.append(f'{p.sections} sections > {ms}')
        for kind, _, parts in p.blocks:
            w = len(words(''.join(parts)))
            if w > BLOCK[kind]: probs.append(f'{kind} block {w} words > {BLOCK[kind]}: "{" ".join("".join(parts).split())[:60]}…"')
        for d in p.details:
            if len(words(d)) > BLOCK['detail']: probs.append(f'hover detail {len(words(d))} words > {BLOCK["detail"]}')
        if '—' in text: probs.append('em dash in visible text')
        for b in BANNED:
            if re.search(b, text, re.I): probs.append(f'banned phrase /{b}/')
        for s in re.split(r'(?<=[.!?])\s+', text):
            if len(words(s)) >= 9: sentences[s.strip().lower()].add(name)
        status = 'FAIL' if probs else 'ok  '
        print(f'{status} {name:34s} {n:5d} words  {p.sections} sections')
        for pr in probs[:12]: print('       - ' + pr)
        fails += bool(probs)
    dup = {s: pg for s, pg in sentences.items() if len(pg) > 1}
    if dup:
        print(f'\nSentences repeated across pages ({len(dup)}), keep one canonical home:')
        for s, pg in list(dup.items())[:25]: print(f'  [{", ".join(sorted(pg))}] {s[:90]}')
    return fails

if __name__ == '__main__':
    names = sys.argv[1:] or sorted(f[:-5] for f in glob.glob('*.html') + glob.glob('case-studies/*.html')
                                   if '-cn' not in f and not f.startswith(('pay-', 'enroll')))
    sys.exit(1 if lint(names) else 0)
