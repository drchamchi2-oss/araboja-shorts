from net import get,image

W,H=1200,840
GEOCODER="https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates"
IMAGERY="https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export"

def geocode(query):
    p={"SingleLine":query,"sourceCountry":"KOR","outSR":"4326","maxLocations":5,"f":"json"}
    data=get(GEOCODER,p).json()
    candidates=data.get("candidates") or []
    if not candidates:
        raise RuntimeError("geocoder returned no candidates")
    best=max(candidates,key=lambda x:float(x.get("score",0)))
    loc=best["location"]
    return float(loc["x"]),float(loc["y"]),best.get("address",""),float(best.get("score",0))

def render(box):
    p={"bbox":",".join(f"{v:.3f}" for v in box),
       "bboxSR":"5179","imageSR":"5179","size":f"{W},{H}",
       "format":"jpg","transparent":"false","dpi":96,"f":"image"}
    return image(get(IMAGERY,p,90).content).resize((W,H))
