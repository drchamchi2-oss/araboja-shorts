import io,time,requests
from PIL import Image,ImageStat

S=requests.Session()
S.headers.update({"User-Agent":"KoreaHistoricalMapComparison/2.0"})

def get(url,params=None,timeout=60):
    last=None
    for n in range(4):
        try:
            r=S.get(url,params=params,timeout=timeout,allow_redirects=True)
            r.raise_for_status()
            return r
        except Exception as e:
            last=e
            time.sleep(2+n*2)
    raise RuntimeError(f"GET failed: {url}: {last}")

def image(blob):
    im=Image.open(io.BytesIO(blob)).convert("RGB")
    im.load()
    if im.width<128 or im.height<128:
        raise ValueError("image too small")
    if max(ImageStat.Stat(im.resize((64,64))).stddev)<3:
        raise ValueError("image nearly blank")
    return im
