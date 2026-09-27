from net import get,image
from PIL import Image

W,H=1200,840
COMMONS="https://commons.wikimedia.org/wiki/Special:Redirect/file/Keijo%20map%201937.gif"

def render():
    im=image(get(COMMONS,timeout=90).content)
    im.thumbnail((W,H),Image.Resampling.LANCZOS)
    canvas=Image.new("RGB",(W,H),"#eee9dc")
    x=(W-im.width)//2; y=(H-im.height)//2
    canvas.paste(im,(x,y))
    return canvas,(x+int(im.width*0.52),y+int(im.height*0.69))
