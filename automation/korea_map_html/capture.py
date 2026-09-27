from __future__ import annotations
import json,sys
from datetime import datetime,timezone
from pathlib import Path
from PIL import Image
import hgis,modern,special
from image_ops import marker,footer

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output"; RAW=OUT/"raw"
OUT.mkdir(parents=True,exist_ok=True); RAW.mkdir(parents=True,exist_ok=True)
cases=json.loads((ROOT/"cases.json").read_text(encoding="utf-8"))
overrides={"A06":"서울 한양도성 유적전시관","A07":"서울 저자도","A10":"서울 봉은사역"}
key=hgis.public_key()
records=[]; failures=[]
for c in cases:
    try:
        q=overrides.get(c["id"],c["query"])
        lon,lat,address,score=modern.geocode(q)
        box=hgis.extent(lon,lat,float(c["width"]))
        if c["id"]=="A06":
            old,pos=special.render()
            marker(old,pos[0],pos[1],"1937 지도상 신궁 부근 · 대략 위치")
            old_title="Heibonsha 1937 경성도 · 신궁 존속기"
            old_source="https://commons.wikimedia.org/wiki/File:Keijo_map_1937.gif"
        else:
            old,z,res=hgis.render(key,box,float(c["width"]))
            marker(old,label="동일 좌표 기준점")
            old_title=f"국사편찬위원회 HGIS 1919년도 배경지도 · level {z}"
            old_source="https://hgis.history.go.kr/api/intro.do"
        now=modern.render(box)
        marker(now,label="동일 좌표 기준점")
        footer(old,f'{c["id"]} | {lat:.6f} N, {lon:.6f} E | {old_title}')
        footer(now,f'{c["id"]} | {lat:.6f} N, {lon:.6f} E | Esri World Imagery')
        op=RAW/f'{c["id"]}_old.jpg'; np=RAW/f'{c["id"]}_now.jpg'
        old.save(op,"JPEG",quality=87,optimize=True)
        now.save(np,"JPEG",quality=87,optimize=True)
        records.append({"id":c["id"],"group":c["group"],"name":c["name"],"query":q,
          "width":c["width"],"lon":lon,"lat":lat,"address":address,"score":score,
          "old_file":op.name,"now_file":np.name,"old_title":old_title,"old_source":old_source,
          "now_title":"Esri World Imagery","now_source":"https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer",
          "retrieved":datetime.now(timezone.utc).isoformat()})
        print("OK",c["id"],address,score,flush=True)
    except Exception as e:
        failures.append({"id":c["id"],"name":c["name"],"error":repr(e)})
        print("FAIL",c["id"],repr(e),flush=True)
meta={"records":records,"failures":failures}
(OUT/"capture.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"captured {len(records)}/20 pairs",flush=True)
sys.exit(0 if len(records)==20 else 2)
