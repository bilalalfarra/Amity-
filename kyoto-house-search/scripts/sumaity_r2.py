import re,glob,json,os,datetime,sys
sys.path.insert(0,".")
from sumaity_detail_parse import parse
cands=json.load(open("out/raw/sumaity/candidates.json",encoding="utf-8"))
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec="seconds")
out=[];missing=0;dropped={"gone":0,"floor_rule":0,"reikin":0,"layout":0,"area":0,"rent":0,"age":0}
LAY_OK=re.compile(r"^(2LDK|2SLDK|2LDK\+S|3K|3DK|3SDK|3LDK|3SLDK|3LDK\+S|4K|4DK|4LDK|4SLDK|5\w+|6\w+)$")
for c in cands:
    pid=re.search(r"prop_(\d+)",c["url"]).group(1); fn=f"out/raw/sumaity/detail/prop_{pid}.html"
    if not os.path.exists(fn): missing+=1; continue
    d=parse(fn)
    if not d["still_listed"]: dropped["gone"]+=1; continue
    layout=d["layout"] or c.get("layout")
    if not layout or not LAY_OK.match(layout.replace("＋","+")): dropped["layout"]+=1; continue
    area=d["area_m2"] or c.get("area")
    if area is None or area<45: dropped["area"]+=1; continue
    rent=d["rent"] or c.get("rent")
    if rent is None or rent>100000: dropped["rent"]+=1; continue
    by=d["built_year"]; st=d["structure"]
    house=("一戸建" in (d["btype"] or "")) or ("一戸建" in (c.get("btype") or ""))
    if by is None: dropped["age"]+=1; continue
    if by>=2001: tier="house" if house else "A"
    elif by>=1991 and st in ("RC","SRC"): tier="B"
    else: dropped["age"]+=1; continue
    floor=d["floor"] if d["floor"] is not None else c.get("floor")
    if not house:
        if floor==1: dropped["floor_rule"]+=1; continue
        if floor is not None and floor>=4 and not d["elevator"]: dropped["floor_rule"]+=1; continue
    # reikin ≤ 1 month
    rk=d["reikin"] or ""
    m=re.search(r"([\d.]+)\s*万円",rk); rk_yen=int(round(float(m.group(1))*10000)) if m else None
    m2=re.search(r"([\d.]+)\s*ヶ月",rk)
    if m2 and float(m2.group(1))>2.0: dropped["reikin"]+=1; continue
    if rk_yen is not None and rk_yen>rent*2.0+1: dropped["reikin"]+=1; continue
    addr=d["address"] if d["address"] and len(d["address"])>len("京都府京都市中京区") else (c.get("addr") or d["address"])
    o={"source":"sumaity","url":c["url"],"building_name":c.get("bname") or d["title"].split(" ")[0],"address":addr,"lat":c["lat"],"lon":c["lon"],"distance_km":c["distance_km"],
       "rent":rent,"kanrihi":d["kanrihi"] if d["kanrihi"] is not None else c.get("kanrihi"),
       "shikikin":(d["shikikin"] or c.get("shiki") or "").replace(" 初期費用を聞いてみる","").strip() or None,"reikin":rk or c.get("rei"),
       "other_initial":"; ".join(x for x in [f"仲介手数料: {d['chukai']}" if d['chukai'] else None, f"保証会社: {d['hosho']}" if d['hosho'] else None, f"住宅保険: {d['hoken']}" if d['hoken'] and d['hoken']!='-/-年' else None, f"契約期間: {d['contract']}" if d['contract'] and d['contract']!='-' else None] if x) or None,
       "layout":layout,"area_m2":area,"floor":floor,"building_floors":d["building_floors"] or c.get("bfloors"),"elevator":d["elevator"],
       "built_year":by,"built_month":d["built_month"],"age_years":2026-by,"structure":st,"structure_raw":d["structure_raw"],
       "parking":d["parking"],"parking_fee":d["parking_fee"],"nearest_station":d["nearest_station"],"tier":tier,"btype":d["btype"],
       "agency":d["agency"],"units":d["units"],"conditions":(d["conditions"] or "").replace(" 入居条件について質問する","").replace(" 飼育可能なペットの数や種類を確認する","").strip() or None,
       "notes":re.sub(r"(資料や写真を送ってもらう|設備について質問する|インターネット環境について聞く|駐車可能な車種や台数を確認する)","",d["setsubi"])[:600],
       "fetched_at":now}
    out.append(o)
out.sort(key=lambda x:x["distance_km"])
json.dump(out,open("out_r2/sumaity.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("kept",len(out),"missing",missing,"dropped",dropped)
import collections
print(collections.Counter(o["tier"] for o in out), collections.Counter(o["elevator"] for o in out))
for o in out[:12]: print(o["distance_km"],o["building_name"],o["layout"],o["area_m2"],o["rent"],o["kanrihi"],o["reikin"],o["floor"],"/",o["building_floors"],"EV" if o["elevator"] else "-",o["built_year"],o["structure"],o["parking"],o["tier"])
