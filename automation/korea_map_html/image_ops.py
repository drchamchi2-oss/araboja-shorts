import os
from PIL import ImageDraw,ImageFont

def font(size=20):
    paths=["/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
           "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for p in paths:
        if os.path.exists(p):
            try:return ImageFont.truetype(p,size)
            except Exception:pass
    return ImageFont.load_default()

def marker(im,x=None,y=None,label="동일 비교 기준점"):
    x=im.width//2 if x is None else x
    y=im.height//2 if y is None else y
    d=ImageDraw.Draw(im)
    for r,w,c in [(25,8,"white"),(25,4,"#e5302b")]:
        d.ellipse((x-r,y-r,x+r,y+r),outline=c,width=w)
    for a,b in [((x-48,y),(x-30,y)),((x+30,y),(x+48,y)),((x,y-48),(x,y-30)),((x,y+30),(x,y+48))]:
        d.line((a,b),fill="white",width=6); d.line((a,b),fill="#e5302b",width=3)
    f=font(18)
    d.rounded_rectangle((10,10,500,50),radius=8,fill="white",outline="#e5302b",width=2)
    d.text((20,17),label,font=f,fill="#111")

def footer(im,text):
    d=ImageDraw.Draw(im); f=font(16); h=38
    d.rectangle((0,im.height-h,im.width,im.height),fill="#142d36")
    d.text((12,im.height-h+9),text[:125],font=f,fill="white")
