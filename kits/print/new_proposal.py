"""Start a new Arena School proposal from the proposal design system.

Usage:
  python3 new_proposal.py <folder-slug> "<Client full name>" "<Client short name>" [client-logo.png]
Example:
  python3 new_proposal.py isb-spring "International School of Beijing" "ISB" ~/Downloads/isb-logo.png

Creates print/docs/<folder-slug>/ with proposal.html (template with names, date, and logo filled in) and build.py.
Then replace every yellow [Write: ...] placeholder and run `python3 build.py` in that folder.
"""
import sys, pathlib, shutil, datetime, html
KIT = pathlib.Path(__file__).parent
if len(sys.argv) < 4:
    sys.exit(__doc__)
slug, full, short = sys.argv[1], sys.argv[2], sys.argv[3]
logo = pathlib.Path(sys.argv[4]).expanduser() if len(sys.argv) > 4 else None
dest = KIT / 'docs' / slug
if (dest / 'proposal.html').exists():
    sys.exit(f'{dest}/proposal.html already exists; not overwriting.')
dest.mkdir(parents=True, exist_ok=True)
today = datetime.date.today()
year = today.year if today.month >= 7 else today.year - 1
if logo:
    if not logo.exists(): sys.exit(f'logo not found: {logo}')
    target = KIT / 'site' / 'logos' / 'clients' / f'{slug}{logo.suffix.lower()}'
    target.parent.mkdir(parents=True, exist_ok=True); shutil.copy(logo, target)
    logo_html = f'<img src="/logos/clients/{target.name}" alt="{html.escape(full)}" style="height:6.4mm" />'
else:
    logo_html = f'<span class="ph">[Add {html.escape(full)} logo: rerun with a logo file, or put it in print-kit/site/logos/clients/]</span>'
fill = {
    '{{CLIENT_FULL}}': html.escape(full), '{{CLIENT_SHORT}}': html.escape(short),
    '{{DATE}}': today.strftime('%B %-d, %Y'), '{{MONTH_YEAR}}': today.strftime('%B %Y'),
    '{{SCHOOL_YEAR}}': f'{year}–{str(year + 1)[-2:]}', '{{CLIENT_LOGO_HTML}}': logo_html,
}
t = (KIT / 'proposal' / 'template.html').read_text()
for k, v in fill.items(): t = t.replace(k, v)
(dest / 'proposal.html').write_text(t)
(dest / 'build.py').write_text(f'''"""Build this proposal with the Arena print kit (../../print-kit)."""
import subprocess, sys, pathlib
HERE = pathlib.Path(__file__).parent
KIT = HERE.parent.parent
out = HERE / 'Arena-School-Proposal-{slug}.pdf'
rc = subprocess.call([sys.executable, str(KIT / 'build.py'), str(HERE / 'proposal.html'), str(out)] + sys.argv[1:])
subprocess.call([sys.executable, str(KIT / 'orphans.py'), str(HERE / 'proposal.html')])
sys.exit(rc)
''')
print(f'Created {dest}/proposal.html and build.py.\nNext: fill every yellow [Write: ...] placeholder, then run: cd {dest} && python3 build.py')
