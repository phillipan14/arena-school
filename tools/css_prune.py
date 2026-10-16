"""Remove dead CSS selectors for classes that no longer exist in any page or script (MIGRATION-BRIEF).

  python3 tools/css_prune.py --classes gm-lane,gm-bar file.css page.html ...   (add --check to only report)

A selector is dead when it names one of the given classes. Dead selectors are dropped from each rule's selector
list; a rule with none left is removed; an @media block left empty is removed. Works on .css files and on the
<style> blocks inside .html files. Before pruning, confirm the classes are gone from every page and script.
"""
import re
import sys


def dead_sel(sel, pat):
    """A selector is dead only when a dead class sits outside parentheses: there it must match for the selector
    to match. Inside :not(), :is(), :where(), or :has() it may be optional or negated, so the selector stays."""
    for m in pat.finditer(sel):
        if sel[:m.start()].count('(') == sel[:m.start()].count(')'):
            return True
    return False


def prune_css(css, dead):
    pat = re.compile(r'(?<![\w-])\.(%s)(?![\w-])' % '|'.join(re.escape(c) for c in dead))
    out, i, n, removed = [], 0, len(css), 0
    while i < n:
        j = css.find('{', i)
        if j == -1:
            out.append(css[i:]); break
        head = css[i:j]
        # comments and whitespace before the selector stay as they are
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == '{': depth += 1
            elif css[k] == '}': depth -= 1
            k += 1
        body = css[j + 1:k - 1]
        lead = re.match(r'(?s)^(\s*(?:/\*.*?\*/\s*)*)', head).group(1)
        sel = head[len(lead):]
        if sel.strip().startswith('@'):
            inner, r = prune_css(body, dead)
            removed += r
            if inner.strip():
                out.append(lead + sel + '{' + inner + '}')
            else:
                out.append(lead.rstrip(' ') if lead.strip() else lead)
        else:
            parts = [p for p in re.split(r',(?![^()]*\))', sel)]
            keep = [p for p in parts if not dead_sel(p, pat)]
            removed += len(parts) - len(keep)
            if keep:
                out.append(lead + ','.join(keep) + '{' + body + '}')
            else:
                out.append(lead.rstrip(' ') if lead.strip() else '')
        i = k
    return ''.join(out), removed


def prune_file(path, dead, check):
    s = open(path, encoding='utf-8').read()
    total = 0
    if path.endswith('.html'):
        def fix(m):
            nonlocal total
            css, r = prune_css(m.group(2), dead)
            total += r
            return m.group(1) + css + m.group(3)
        t = re.sub(r'(?s)(<style[^>]*>)(.*?)(</style>)', fix, s)
    else:
        t, total = prune_css(s, dead)
    t = re.sub(r'\n{3,}', '\n\n', t)
    if t != s and not check:
        open(path, 'w', encoding='utf-8').write(t)
    return total


if __name__ == '__main__':
    args = sys.argv[1:]
    check = '--check' in args
    dead = args[args.index('--classes') + 1].split(',')
    files = [a for a in args if a not in ('--check', '--classes') and a != args[args.index('--classes') + 1]]
    for f in files:
        print('%-28s %3d selectors %s' % (f, prune_file(f, dead, check), 'would be removed' if check else 'removed'))
