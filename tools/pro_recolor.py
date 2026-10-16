"""Pro pass (2026-10-16): move the site off cream/beige onto white and cool off-white.
Rewrites colors in the shared stylesheets, the phone partials, and inline styles of site pages
(never decks/, talks/, review/, or promo.css, which the decks share). Idempotent: cool colors are left alone.
    python3 tools/pro_recolor.py          # rewrite
    python3 tools/pro_recolor.py --check  # report what would change
Then run: python3 tools/phone_build.py (or phone_markup.py) so phone.css picks up the partials."""
import glob, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = '--check' in sys.argv

# Brand tokens: explicit targets (paper -> white, bands -> cool off-white, rules -> cool hairline,
# cream text on navy -> near-white, sand accent on navy -> light blue).
EXPLICIT = {
    'EFE3D4': 'FFFFFF',  # --bg-paper (page)
    'FCF3ED': 'FFFFFF',  # --paper-hi (cards, text on navy)
    'FBF6EF': 'FFFFFF',  # homepage card surface
    'FFFDF9': 'FFFFFF', 'FFF9F4': 'FFFFFF', 'FDF6F1': 'FFFFFF', 'FFF6F1': 'FFFFFF', 'FFF4EE': 'FFFFFF',
    'F3E9DD': 'F5F7FA',  # header paper
    'E6D4C1': 'F5F7FA',  # --bg-paper-soft (alt band)
    'F6ECE1': 'F5F7FA', 'F6EDE2': 'F5F7FA', 'F3EEE7': 'F5F7FA',
    'D4C0AA': 'E2E6EE',  # --border-paper
    'F7F1E7': 'FFFFFF', 'F6F0E5': 'F4F6FA', 'F4ECE0': 'E6E9F0', 'F4ECE1': 'E6E9F0',  # cream text on navy
    'E9C9A0': 'A9BEEA',  # sand italic on navy
    'EBCDA4': 'E2E6EE',
}
EXPLICIT_RGB = {
    (252, 243, 237): (255, 255, 255), (239, 227, 212): (255, 255, 255), (246, 240, 229): (244, 246, 250),
    (244, 236, 224): (230, 233, 240), (242, 236, 226): (240, 243, 247), (212, 192, 170): (226, 230, 238),
}


def cool(r, g, b):
    """Map a light, low-chroma warm neutral to a cool neutral of similar lightness; else None."""
    chroma = max(r, g, b) - min(r, g, b)
    y = 0.299 * r + 0.587 * g + 0.114 * b
    if y < 175 or chroma > 48 or r - b < 6:
        return None
    if y >= 246: return (255, 255, 255)
    if y >= 238: return (245, 247, 250)
    if y >= 228: return (238, 241, 246)
    if y >= 215: return (226, 230, 238)
    if y >= 195: return (205, 211, 223)
    v = int(round(y))
    return (max(0, v - 6), max(0, v - 2), min(255, v + 6))


def hex_sub(m):
    h = m.group(1).upper()
    if h in EXPLICIT:
        return '#' + EXPLICIT[h]
    t = cool(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return '#%02X%02X%02X' % t if t else m.group(0)


def rgb_sub(m):
    fn, r, g, b = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
    t = EXPLICIT_RGB.get((r, g, b)) or cool(r, g, b)
    if not t:
        return m.group(0)
    return '%s(%d, %d, %d' % (fn, *t)


def recolor(s):
    s = re.sub(r'#([0-9a-fA-F]{6})\b', hex_sub, s)
    s = re.sub(r'(rgba?)\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', rgb_sub, s)
    return s


def targets():
    css = ['styles.css', 'riso-theme.css', 'mobile.css', 'newsletter.css'] + sorted(glob.glob('css/*.css')) + sorted(glob.glob('phone/*.css'))
    html = [f for f in subprocess.run(['git', 'ls-files', '*.html'], cwd=ROOT, capture_output=True, text=True).stdout.split()
            if not re.match(r'(decks|talks|review)/', f)]
    return css + html


if __name__ == '__main__':
    os.chdir(ROOT)
    changed = 0
    for f in targets():
        s = open(f, encoding='utf-8').read()
        n = recolor(s)
        if n != s:
            changed += 1
            if not CHECK:
                open(f, 'w', encoding='utf-8').write(n)
    print(('Would change' if CHECK else 'Changed'), changed, 'files')
