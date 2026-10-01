import re,json,os,time,datetime,collections,glob,sys
sys.path.insert(0,".")
from eheya_detail_parse import parse
for _ in range(75):
    if "DONE" in open("out/raw/eheya/stage.log",encoding="utf-8").read(): break
    time.sleep(1)
cands=json.load(open("out/raw/eheya/candidates.json",encoding="utf-8"))
stats=json.loads(open("out/raw/eheya/stage.log",encoding="utf-8").readline())
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec="seconds")
LAY_OK=re.compile(r"^(2LDK|2SLDK|3K|3DK|3SDK|3LDK|3SLDK|4K|4DK|4LDK|4SLDK|5\w+|6\w+)$")
out=[];missing=0;dropped=collections.Counter()
for c in cands:
    pid=re.search(r"/detail/(\d+)/",c["url"]).group(1); fn=f"out/raw/eheya/detail/{pid}.html"
    if not os.path.exists(fn) or os.path.getsize(fn)<20000: missing+=1; continue
    d=parse(fn)
    if not d.get("ok"): dropped["gone/unparsable"]+=1; continue
    layout=(d["layout"] or c["layout"] or "").replace("＋S","S")
    if not LAY_OK.match(layout): dropped["layout"]+=1; continue
    area=d["area_m2"] or c["area"]
    if area is None or area<45: dropped["area"]+=1; continue
    rent=d["rent"] or c["rent"]
    if rent is None or rent>100000: dropped["rent"]+=1; continue
    by=d["built_year"]; st=d["structure"]
    house=(d["kind"] in ("HOUSE","DETACHED_HOUSE","TERRACE_HOUSE")) or ("戸建" in (c.get("btype") or "")) or ("テラス" in (c.get("btype") or ""))
    if by is None: dropped["age"]+=1; continue
    if by>=2001: tier="house" if house else "A"
    elif by>=1991 and st in ("RC","SRC"): tier="B"
    else: dropped["age/structure"]+=1; continue
    floor=d["floor"] if d["floor"] is not None else c["floor"]
    if not house:
        if floor==1: dropped["floor1"]+=1; continue
        if floor is not None and floor>=4 and not d["elevator"]: dropped["4F_no_elevator"]+=1; continue
    rm=d.get("reikin_months")
    if rm is not None and rm>1.0: dropped["reikin"]+=1; continue
    sn=(d.get("special_notes") or "").replace("\n"," / ")
    o={"source":"eheya","url":c["url"],"building_name":d["building_name"] or c["bname"],"address":d["address"] or c["addr"],"lat":c["lat"],"lon":c["lon"],"distance_km":c["distance_km"],
       "rent":rent,"kanrihi":d["kanrihi"] if d["kanrihi"] is not None else c["kanrihi"],"shikikin":d["shikikin"],"reikin":d["reikin"],
       "other_initial":"; ".join(x for x in [f"更新料 {d['renewal_fee']}" if d.get('renewal_fee') else None, f"更新事務手数料 {d['renewal_charge']}" if d.get('renewal_charge') else None, f"特記: {sn[:300]}" if sn else None, "仲介手数料 要 (いい部屋ネット/大東建託リーシング)"] if x),
       "layout":layout,"area_m2":area,"floor":floor,"building_floors":d["building_floors"] or c["bfloors"],"elevator":d["elevator"],
       "built_year":by,"built_month":d["built_month"],"age_years":2026-by,"structure":st,"structure_raw":d["structure_code"],
       "parking":d["parking_text"],"parking_fee":(lambda m:int(m.group(1).replace(",","")) if m else None)(re.search(r"([\d,]+)円",d["parking_text"] or "")),
       "nearest_station":d["stations"] or c["station"],"tier":tier,"btype":d["kind"],"agency":d["shop"],"agency_tel":d["shop_tel"],"available":d["available"],"move_in_status":d["move_in_status"],
       "notes":("; ".join(d["features"])[:500]+(" | PR: "+(d["sales_point"] or "")[:150])),"fetched_at":now}
    out.append(o)
out.sort(key=lambda x:x["distance_km"])
json.dump(out,open("out/eheya.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("kept",len(out),"missing",missing,"dropped",dict(dropped))
tiers=collections.Counter(o["tier"] for o in out); ev=collections.Counter(o["elevator"] for o in out)
pages=len(glob.glob("out/raw/eheya/list_*_p*.html"))
md=["# eheya — いい部屋ネット (eheya.net, 大東建託), fetched 2026-10-01\n","## Method",
 "- The site is a Next.js app; its filter panel builds the result client-side (no URL query parameters are exposed, and headless Chromium gets a CloudFront 403), so the SSR ward pages https://www.eheya.net/kyoto/area/<city>/search/?page=N were crawled **unfiltered** with curl (plain requests-lib sessions got 403 on ?page≥2; curl with a Chrome UA worked).",
 f"- Wards: 下京 291, 中京 218, 南 642, 右京 495, 上京 325, 西京 320, 東山 27, 北 178, 伏見 526 listings (site counts) → {pages} list pages, {stats['total']} unique room cards parsed (building, 築年, 階建, address, floor, rent, 管理費, 敷/礼, layout, area).",
 f"- Client-side funnel: layout not 2LDK+ {stats['layout']}, area<45 {stats['area']}, rent>100,000 {stats['rent']}, 築36+ {stats['age']}, 1F {stats['floor1']}, >5.5 km {stats['far']} → {stats['keep']} candidates → detail pages fetched (HTTP 200; fields read from the page's __NEXT_DATA__ JSON: constructionDate, buildingStructure, story, propertyFeatures incl. LIFT, parkingText, keyMoney, renewal fees, specialNotes) → dropped: {dict(dropped)} → **{len(out)} kept**.",
 f"- Kept by tier: {dict(tiers)}; elevator yes/no: {dict(ev)}. Geocoding by town-level address (block numbers not shown) → ±300 m.",
 "- Caveats: most いい部屋ネット stock is 大東建託 light-steel/wood apartments (軽量鉄骨/木造) — these pass only if built 2001+ (tier A). 礼金 is often quoted in yen (e.g. 130,000円 on a 99,000 rent = 1.31 months → dropped). 保証会社 fees and 'ruumサポート費用' etc. are in `other_initial`.\n",
 "## Kept units (closest first)","| km | building | layout | m² | rent | 管理費 | 敷/礼 | floor | EV | built | struct | parking | tier | url |","|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for o in out:
    md.append(f"| {o['distance_km']} | {o['building_name'][:22]} | {o['layout']} | {o['area_m2']} | {o['rent']:,} | {o['kanrihi']} | {o['shikikin']}/{o['reikin']} | {o['floor']}/{o['building_floors']} | {'Y' if o['elevator'] else 'n'} | {o['built_year']}/{o['built_month']} | {o['structure']} | {(o['parking'] or '')[:24]} | {o['tier']} | {o['url']} |")
open("out/eheya.md","w",encoding="utf-8").write("\n".join(md))
for o in out: print(o["distance_km"],o["building_name"],o["layout"],o["area_m2"],o["rent"],o["kanrihi"],o["shikikin"],o["reikin"],o["floor"],"/",o["building_floors"],"EV" if o["elevator"] else "-",o["built_year"],o["structure"],o["parking"],o["tier"])
