"""Session QR codes: navy (#0B1A4A) on transparent, 840x840, error correction M.
Writes /decks/img/acamis/qr-acamis-download-{clear,tight}.png for QR_URL (site_paths.py).
clear = one-module quiet margin (cover), tight = no margin (close slide, white tile supplies it).
Usage: python3 tools/qr.py     Needs: pip install qrcode pillow"""
import os, sys
import qrcode
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from site_paths import ROOT, QR_URL

NAVY = (11, 26, 74, 255)
SIZE = 840
IMG = os.path.join(ROOT, 'decks', 'img', 'acamis')

def render(matrix, margin):
    n = len(matrix) + 2 * margin
    im = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    edge = lambda k: round(k * SIZE / n)  # exact module edges, no gaps or overlaps
    for r, row in enumerate(matrix):
        for c, dark in enumerate(row):
            if dark:
                dr.rectangle([edge(c + margin), edge(r + margin), edge(c + margin + 1) - 1, edge(r + margin + 1) - 1], fill=NAVY)
    return im

q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
q.add_data(QR_URL); q.make(fit=True)
m = q.get_matrix()
for name, margin in (('clear', 1), ('tight', 0)):
    out = os.path.join(IMG, f'qr-acamis-download-{name}.png')
    render(m, margin).save(out, optimize=True)
    print(out, f'{len(m)} modules', QR_URL)
