import re,glob,json,os,datetime,warnings,collections
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
cands=json.load(open("out/raw/able/candidates.json",encoding="utf-8"))
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec="seconds")
def parse(fn):
    soup=BeautifulSoup(open(fn,encoding="utf-8").read(),"lxml")
    d={}
    for tr in soup.find_all("tr"):
        cells=tr.find_all(["th","td"])
        for j in range(len(cells)-1):
            if cells[j].name=="th" and cells[j+1].name=="td":
                k=cells[j].get_text(" ",strip=True); v=cells[j+1].get_text(" ",strip=True)
                if k and k not in d: d[k]=v
    txt=soup.get_text(" ",strip=True)
    r={"title":(soup.title.string or "").strip() if soup.title else ""}
    m=re.search(r"([\d.]+)\s*万円\s*([\d,]+)円",d.get("家賃 管理費","")); 
    if m: r["rent"]=int(round(float(m.group(1))*10000)); r["kanrihi"]=int(m.group(2).replace(",",""))
    else:
        m=re.search(r"([\d.]+)\s*万円",d.get("家賃 管理費","")); r["rent"]=int(round(float(m.group(1))*10000)) if m else None; r["kanrihi"]=0 if re.search(r"万円\s*(--|なし|-)",d.get("家賃 管理費","")) else None
    r["shikikin"]=d.get("敷金/保証金"); r["reikin"]=d.get("礼金/償却")
    r["layout"]=(d.get("間取り") or "").split("(")[0].strip() or None
    m=re.search(r"([\d.]+)㎡",d.get("広さ","")); r["area_m2"]=float(m.group(1)) if m else None
    m=re.match(r"(\d+)階/(\d+)階建",d.get("階/階建","").replace(" ","")); r["floor"]=int(m.group(1)) if m else None; r["building_floors"]=int(m.group(2)) if m else None
    m=re.search(r"(\d{4})年(\d{1,2})月",d.get("築年/築年月","")); r["built_year"]=int(m.group(1)) if m else None; r["built_month"]=int(m.group(2)) if m else None
    bs=d.get("建物種別/構造",""); r["btype"]=bs.split("/")[0]; sraw=bs.split("/")[-1]; r["structure_raw"]=sraw
    if "鉄骨鉄筋" in sraw: st="SRC"
    elif "鉄筋" in sraw: st="RC"
    elif "軽量鉄骨" in sraw: st="軽量鉄骨"
    elif "重量鉄骨" in sraw: st="重量鉄骨"
    elif "鉄骨" in sraw: st="鉄骨"
    elif "木造" in sraw: st="木造"
    else: st="その他"
    r["structure"]=st
    r["address"]=re.sub(r"\s+","",d.get("住所",""))
    r["nearest_station"]=d.get("交通")
    set_keys=["キッチン/バス・トイレ","お部屋の設備サービス","セキュリティ","共有スペースの特徴・設備","建物の特徴・設備","その他"]
    setsubi=" / ".join(f"{k}: {d[k]}" for k in set_keys if k in d)
    r["setsubi"]=setsubi; r["elevator"]=("エレベーター" in setsubi) or ("エレベータ" in setsubi)
    r["parking"]=d.get("駐車場"); m=re.search(r"([\d,]+)円",r["parking"] or ""); r["parking_fee"]=int(m.group(1).replace(",","")) if m else None
    r["hosho"]=d.get("家賃保証会社等"); r["conditions"]=d.get("入居条件"); r["remarks"]=d.get("備考"); r["contract"]=d.get("契約"); r["shohiyo"]=d.get("諸費用"); r["hoken"]=d.get("保険"); r["movein"]=d.get("入居時期"); r["updated"]=d.get("登録日/掲載有効期限")
    r["still_listed"]=("募集を終了" not in txt and "掲載終了" not in txt and r["rent"] is not None)
    return r
out=[];missing=0;dropped=collections.Counter()
LAY_OK=re.compile(r"^(2LDK|2SLDK|2LDK\+S|3K|3DK|3SDK|3LDK|3SLDK|3LDK\+S|4K|4DK|4LDK|4SLDK|5\w+|6\w+)$")
for c in cands:
    fn=f"out/raw/able/detail/{c['bk']}.html"
    if not os.path.exists(fn): missing+=1; continue
    d=parse(fn)
    if not d["still_listed"]: dropped["gone"]+=1; continue
    layout=(d["layout"] or c["layout"] or "").replace("(+S)","").replace("＋S","+S")
    if not LAY_OK.match(layout): dropped["layout"]+=1; continue
    area=d["area_m2"] or c["area"]
    if area is None or area<45: dropped["area"]+=1; continue
    rent=d["rent"] or c["rent"]
    if rent is None or rent>100000: dropped["rent"]+=1; continue
    by=d["built_year"] or c["built_year"]; st=d["structure"] if d["structure_raw"] else c["structure"]
    house=("戸建" in (d["btype"] or "")) or ("貸家" in (c["btype"] or "")) or ("戸建" in (c["btype"] or ""))
    if by is None: dropped["age"]+=1; continue
    if by>=2001: tier="house" if house else "A"
    elif by>=1991 and st in ("RC","SRC"): tier="B"
    else: dropped["age"]+=1; continue
    floor=d["floor"] if d["floor"] is not None else c["floor"]
    if not house:
        if floor==1: dropped["floor1"]+=1; continue
        if floor is not None and floor>=4 and not d["elevator"]: dropped["4F_no_elevator"]+=1; continue
    rk=d["reikin"] or ""
    m=re.search(r"([\d.]+)万",rk.split("/")[0]); rk_yen=int(round(float(m.group(1))*10000)) if m else (0 if rk.startswith(("--","なし","-")) else None)
    if rk_yen is not None and rk_yen>rent+1: dropped["reikin"]+=1; continue
    o={"source":"able","url":c["url"],"building_name":c["bname"],"address":d["address"] or c["addr"],"lat":c["lat"],"lon":c["lon"],"distance_km":c["distance_km"],
       "rent":rent,"kanrihi":d["kanrihi"] if d["kanrihi"] is not None else c["kanrihi"],"shikikin":d["shikikin"] or c["shiki"],"reikin":rk or c["rei"],
       "other_initial":"; ".join(x for x in [f"仲介手数料: {c.get('tags') and next((t for t in c['tags'] if 'ヶ月' in t or '無料' in t),None)}" if c.get('tags') and any(('ヶ月' in t or '無料' in t) for t in c['tags']) else None, f"保証会社: {d['hosho']}" if d['hosho'] else None, f"諸費用: {d['shohiyo']}" if d['shohiyo'] else None, f"保険: {d['hoken']}" if d['hoken'] else None, f"契約: {d['contract']}" if d['contract'] else None] if x) or None,
       "layout":layout,"area_m2":area,"floor":floor,"building_floors":d["building_floors"] or c["bfloors"],"elevator":d["elevator"],
       "built_year":by,"built_month":d["built_month"] or c["built_month"],"age_years":2026-by,"structure":st,"structure_raw":d["structure_raw"] or c["structure_raw"],
       "parking":d["parking"],"parking_fee":d["parking_fee"],"nearest_station":d["nearest_station"] or c["station"],"tier":tier,"btype":d["btype"] or c["btype"],
       "agency":c["shop"],"movein":d["movein"],"conditions":d["conditions"],"remarks":d["remarks"],
       "notes":(d["setsubi"][:500]+(" | PR: "+c["comment"][:150] if c.get("comment") else "")),"fetched_at":now}
    out.append(o)
out.sort(key=lambda x:x["distance_km"])
json.dump(out,open("out/able.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("kept",len(out),"missing",missing,"dropped",dict(dropped))
print(collections.Counter(o["tier"] for o in out),collections.Counter(o["elevator"] for o in out))
for o in out[:12]: print(o["distance_km"],o["building_name"],o["layout"],o["area_m2"],o["rent"],o["kanrihi"],o["shikikin"],o["reikin"],o["floor"],"/",o["building_floors"],"EV" if o["elevator"] else "-",o["built_year"],o["structure"],o["parking"],o["tier"])
