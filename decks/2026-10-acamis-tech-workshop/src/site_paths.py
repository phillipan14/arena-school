"""Where this talk lives. Everything is derived from the folder name, so a new talk is:
copy decks/<old-slug>/ to decks/<new-slug>/, edit the slides, run build.py and export.py.

  decks/<slug>/src/        source (this folder; not deployed, see .vercelignore)
  talks/<slug>/            published: index.html (landing page), deck.html, deck-cn.html,
                           read/en.html, read/cn.html, slides-en.pdf, slides-cn.pdf, slides/{en,cn}/NN.jpg
  https://arenaschool.org/talks/<slug>   the public address (Vercel cleanUrls drop .html)
"""
import os
SRC = os.path.dirname(os.path.abspath(__file__))
SLUG = os.path.basename(os.path.dirname(SRC))
ROOT = os.path.abspath(os.path.join(SRC, '..', '..', '..'))
OUT = os.path.join(ROOT, 'talks', SLUG)          # published files
BASE = '/talks/' + SLUG                           # public path
URL = 'https://arenaschool.org' + BASE            # what the QR codes encode
DISPLAY = 'arenaschool.org' + BASE                # printed under the QR codes
# printed form with one deliberate break point after "talks/" and none inside the slug
DISPLAY_HTML = '<span class="nw">arenaschool.org/talks/</span><wbr><span class="nw">' + SLUG + '</span>'
# the slide QR codes open the download page (name, institution, email, then the files); see tools/qr.py
QR_URL = URL + '/download'
QR_DISPLAY = DISPLAY + '/download'
QR_DISPLAY_HTML = DISPLAY_HTML[:-len('</span>')] + '/download</span>'
