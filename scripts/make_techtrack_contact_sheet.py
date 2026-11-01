#!/usr/bin/env python3
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import io,cairosvg
ROOT=Path(__file__).resolve().parents[1]
TW,TH=460,300
res=Image.new('RGB',(TW*4,TH*7),'#E9EEF0');d=ImageDraw.Draw(res)
for row,(brand,comp) in enumerate([(b,c) for b in ['techtrack','techtrack-kids'] for c in ['mark','stacked','horizontal','wordmark']]):
  if row>=7:break
  p=ROOT/'brands'/brand
  for col,bg in enumerate(['white','black','lemon','transparent']):
    sv=p/'vector'/comp/f'{brand}-{comp}-master.svg' if bg=='transparent' else p/'logos'/'svg'/f'{brand}-{comp}-{bg}-v1.svg'
    raw=cairosvg.svg2png(url=str(sv),output_width=395)
    im=Image.open(io.BytesIO(raw)).convert('RGBA'); im.thumbnail((TW-35,TH-55))
    x=col*TW+(TW-im.width)//2;y=row*TH+40+(TH-55-im.height)//2
    d.rectangle((col*TW+7,row*TH+7,(col+1)*TW-7,(row+1)*TH-7),fill={'white':'#FFFFFF','black':'#000000','lemon':'#FFC93D','transparent':'#D4D9DC'}[bg])
    res.paste(im,(x,y),im)
    fg='#FFFFFF' if bg=='black' else '#121A2E'
    d.text((col*TW+15,row*TH+15),f'{brand} {comp} / {bg}',fill=fg)
# Create sheet for 8 rows
allc=[(b,c) for b in ['techtrack','techtrack-kids'] for c in ['mark','stacked','horizontal','wordmark']]
res=Image.new('RGB',(TW*4,TH*8),'#E9EEF0');d=ImageDraw.Draw(res)
for row,(brand,comp) in enumerate(allc):
 p=ROOT/'brands'/brand
 for col,bg in enumerate(['white','black','lemon','transparent']):
  sv=p/'vector'/comp/f'{brand}-{comp}-master.svg' if bg=='transparent' else p/'logos'/'svg'/f'{brand}-{comp}-{bg}-v1.svg'
  im=Image.open(io.BytesIO(cairosvg.svg2png(url=str(sv),output_width=395))).convert('RGBA');im.thumbnail((TW-35,TH-55))
  d.rectangle((col*TW+7,row*TH+7,(col+1)*TW-7,(row+1)*TH-7),fill={'white':'#FFFFFF','black':'#000000','lemon':'#FFC93D','transparent':'#E2E6E9'}[bg])
  res.paste(im,(col*TW+(TW-im.width)//2,row*TH+40+(TH-55-im.height)//2),im)
  d.text((col*TW+15,row*TH+15),f'{brand} {comp} / {bg}',fill='#FFFFFF' if bg=='black' else '#0B2135')
res.save(ROOT/'TechTrack_Visual_Contact_Sheet.png',optimize=True)
print(ROOT/'TechTrack_Visual_Contact_Sheet.png')
