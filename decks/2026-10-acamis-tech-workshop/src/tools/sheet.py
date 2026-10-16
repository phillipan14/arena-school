"""Contact sheet of screenshots from shots.py, two per row.
Usage: python3 tools/sheet.py SHOTDIR 6,7,8 OUT.png [width_per_slide=960]"""
import sys
from PIL import Image, ImageDraw
d=sys.argv[1]; nums=[int(x) for x in sys.argv[2].split(',')]; out=sys.argv[3]; W=int(sys.argv[4]) if len(sys.argv)>4 else 960
H=W*9//16; cols=2; rows=(len(nums)+cols-1)//cols; S=Image.new('RGB',(W*cols,H*rows),'white')
for k,n in enumerate(nums):
    im=Image.open(f'{d}/{n:02d}.png').convert('RGB').resize((W,H)); dr=ImageDraw.Draw(im); dr.rectangle([0,0,46,30],fill='red'); dr.text((6,6),str(n),fill='white')
    S.paste(im,((k%cols)*W,(k//cols)*H))
S.save(out); print(out)
