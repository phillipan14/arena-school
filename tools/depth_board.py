"""Claude Design board for a page's depth sections (DEPTH-BRIEF): writes <PageName>Depth.dc.html and its canvas entry
into a local copy of the design project, ready to publish with the Artifact tool.
  python3 tools/depth_board.py PAGE ROOT_OF_PROJECT_COPY X Y
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import depth as D  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@300..700&amp;family=Newsreader:ital,opsz,wght@0,6..72,300..600;'
         '1,6..72,300..500&amp;display=swap">')


def main(page, R, x, y):
    rd = lambda p: open(os.path.join(ROOT, p), encoding='utf-8').read()
    root = re.search(r'(?s):root\s*\{.*?\n\}', rd('css/pro.css')).group(0)
    c = D.PAGES[page]['en']
    (a, r), b = D.block_a(c, 'en'), D.block_b(c)
    body = (a + r + b).replace(' reveal', '')
    body = re.sub(r'<!--.*?-->', '', body)
    body = re.sub(r'href="/[^"#]*"', 'href="#"', body).replace('src="/logos', 'src="https://arenaschool.org/logos')
    css = ("body{margin:0}\n.ab{font-family:'Geist',system-ui,sans-serif;color:#111827;background:#FFFFFF}\n"
           ".ab .container{max-width:1124px;margin:0 auto;padding:0 32px}\n.ab .tlink{color:#22458A;font-weight:500;text-decoration:none}\n" + root + rd('css/ds.css'))
    name = ''.join(w.capitalize() for w in re.split(r'[-_]', page)) + 'Depth.dc.html'
    doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Arena %s depth</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n%s\n<style>\n%s\n</style>\n</helmet>\n'
           '<div class="ab" style="width: 100%%; max-width: 1440px; margin: 0 auto">\n%s\n</div>\n</x-dc>\n'
           '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":1440,"height":3000}}\'>\nclass Component extends DCLogic {\n  renderVals() {\n    return {};\n  }\n}\n</script>\n</body>\n</html>\n'
           % (page, FONTS, css, body))
    open(os.path.join(R, 'project', name), 'w', encoding='utf-8').write(doc)
    p = os.path.join(R, 'project', 'canvas.json')
    d = json.load(open(p))
    d['boards'][name] = {"x": int(x), "y": int(y), "w": 1440, "h": 3000, "title": "%s depth · pressures, research, cases (DEPTH-BRIEF)" % page, "expand": "fill"}
    if name not in d['order']:
        d['order'].append(name)
    json.dump(d, open(p, 'w'), indent=2, ensure_ascii=False)
    print('project/' + name)


if __name__ == '__main__':
    main(*sys.argv[1:5])
