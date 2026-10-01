import re,glob,json,warnings,datetime,sys
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
def parse(fn):
    soup=BeautifulSoup(open(fn,encoding="utf-8").read(),"lxml")
    d={}
    for tr in soup.find_all("tr"):
        cells=tr.find_all(["th","td"])
        for j in range(len(cells)-1):
            if cells[j].name=="th" and cells[j+1].name=="td":
                k=cells[j].get_text(" ",strip=True); v=cells[j+1].get_text(" ",strip=True)
                if k and k not in d: d[k]=v
    title=soup.title.string if soup.title else ""
    txt=soup.get_text(" ",strip=True)
    r={}
    r["title"]=title.strip()
    m=re.search(r"([\d.]+)\s*万円",d.get("家賃","")); r["rent"]=int(round(float(m.group(1))*10000)) if m else None
    m=re.search(r"([\d,]+)円",d.get("管理費","")); r["kanrihi"]=int(m.group(1).replace(",","")) if m else (0 if d.get("管理費","").startswith(("-","なし","0")) else None)
    r["shikikin"]=d.get("敷金(保証金)") or d.get("敷金"); r["reikin"]=(d.get("礼金/償却･敷引") or d.get("礼金") or "").split("/")[0].strip() or None
    m=re.match(r"(\S+?)\s*/\s*([\d.]+)",d.get("間取り/面積","")); r["layout"]=m.group(1) if m else None; r["area_m2"]=float(m.group(2)) if m else None
    m=re.match(r"(\d+)階/(\d+)階建",d.get("所在階/階数","")); r["floor"]=int(m.group(1)) if m else None; r["building_floors"]=int(m.group(2)) if m else None
    m=re.match(r"(\d{4})年(\d{2})月",d.get("築年月","")); r["built_year"]=int(m.group(1)) if m else None; r["built_month"]=int(m.group(2)) if m else None
    sk=d.get("種別/構造",""); r["btype"]=sk.split("/")[0]; sraw=sk.split("/")[-1]
    r["structure_raw"]=sraw
    if "SRC" in sraw or "鉄骨鉄筋" in sraw: st="SRC"
    elif "RC" in sraw or "鉄筋" in sraw: st="RC"
    elif "軽量鉄骨" in sraw: st="軽量鉄骨"
    elif "重量鉄骨" in sraw: st="重量鉄骨"
    elif "鉄骨" in sraw: st="鉄骨"
    elif "木造" in sraw: st="木造"
    else: st="その他"
    r["structure"]=st
    r["address"]=re.sub(r"\s*地図.*$","",d.get("住所","")).strip()
    r["nearest_station"]=d.get("交通") or d.get("交通機関")
    setsubi=" / ".join(f"{k}: {d[k]}" for k in ["キッチン","バス・トイレ","冷暖房","収納","インターネット・TV","室内設備","共用部","セキュリティ","駐車場・駐輪場","その他"] if k in d)
    r["setsubi"]=setsubi
    r["elevator"]=True if "エレベーター" in setsubi or "エレベータ" in setsubi else False
    pk=d.get("駐車場"); r["parking"]=pk
    m=re.search(r"([\d,]+)円",pk or ""); r["parking_fee"]=int(m.group(1).replace(",","")) if m else None
    r["agency"]=d.get("不動産会社"); r["units"]=d.get("総戸数"); r["updated"]=d.get("情報登録日"); r["contract"]=d.get("契約期間")
    r["hoken"]=d.get("住宅保険"); r["other_cost"]=d.get("その他費用"); r["chukai"]=d.get("仲介手数料"); r["hosho"]=d.get("保証会社")
    r["conditions"]=d.get("入居条件")
    r["comment"]=(d.get("その他") or "")[:200]
    r["still_listed"]=("募集終了" not in txt) and ("掲載を終了" not in txt) and r["rent"] is not None
    return r
if __name__=="__main__":
    fs=sorted(glob.glob("out/raw/sumaity/detail/prop_*.html"))[:3]
    for f in fs:
        print(f); print(json.dumps(parse(f),ensure_ascii=False)[:1500]); print()
