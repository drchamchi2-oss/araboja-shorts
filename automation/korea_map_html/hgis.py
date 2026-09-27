import math,re
from PIL import Image
from pyproj import Transformer
from net import get,image

W,H=1200,840
DOC="https://hgis.history.go.kr/api/intro.do"
ENDPOINT="https://hgis.history.go.kr/openapi/get.do"
ORIGIN=(-200000.0,4000000.0)
RES=[15636.779110998164,7818.389555499082,3909.194777749541,1954.5973888747706,977.2986944373853,488.64934721869264,244.32467360934632,122.16233680467316,61.08116840233658,30.54058420116829,15.270292100584145,7.6351460502920725,3.8175730251460362]
TO5179=Transformer.from_crs(4326,5179,always_xy=True)

def public_key():
    text=get(DOC).text
    m=re.search(r"apiKey=([0-9a-fA-F-]{36})",text)
    if not m:
        raise RuntimeError("HGIS public example key not found")
    return m.group(1)

def extent(lon,lat,width):
    x,y=TO5179.transform(lon,lat)
    half_h=width*(H/W)/2
    return [x-width/2,y-half_h,x+width/2,y+half_h]

def level(width):
    target=width/W
    return min(range(len(RES)),key=lambda i:abs(math.log(RES[i]/target)))

def tile(key,z,row,col):
    p={"Service":"WMTS","Request":"GetTile","Version":"1.0.0",
       "Layer":"history:map1919","Style":"normal",
       "TileMatrixSet":"EPSG:5179","TileMatrix":f"EPSG:5179:{z}",
       "TileRow":row,"TileCol":col,"Format":"image/png","apiKey":key}
    return image(get(ENDPOINT,p,45).content)

def render(key,box,width):
    z=level(width); res=RES[z]; size=256
    xmin,ymin,xmax,ymax=box; ox,oy=ORIGIN
    c0=math.floor((xmin-ox)/(res*size)); c1=math.floor((xmax-ox)/(res*size))
    r0=math.floor((oy-ymax)/(res*size)); r1=math.floor((oy-ymin)/(res*size))
    count=(c1-c0+1)*(r1-r0+1)
    if count>64:
        raise RuntimeError(f"too many historic tiles: {count}")
    canvas=Image.new("RGB",((c1-c0+1)*size,(r1-r0+1)*size),"white")
    for r in range(r0,r1+1):
        for c in range(c0,c1+1):
            canvas.paste(tile(key,z,r,c),((c-c0)*size,(r-r0)*size))
    mx=ox+c0*size*res
    my=oy-r0*size*res
    crop=canvas.crop(((xmin-mx)/res,(my-ymax)/res,(xmax-mx)/res,(my-ymin)/res))
    return crop.resize((W,H),Image.Resampling.LANCZOS),z,res
