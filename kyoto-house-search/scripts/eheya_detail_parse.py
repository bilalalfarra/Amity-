import re,json,warnings
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
STRUCT={"RC":"RC","REINFORCED_CONCRETE":"RC","SRC":"SRC","STEEL_REINFORCED_CONCRETE":"SRC","GAUGE_STEEL":"軽量鉄骨","LIGHT_GAUGE_STEEL":"軽量鉄骨","HEAVY_STEEL":"重量鉄骨","STEEL":"鉄骨","WOOD":"木造","WOODEN":"木造","PC":"RC","ALC":"その他","OTHER":"その他","BLOCK":"その他"}
def money(m):
    if not m: return None
    n=m.get("number"); u=m.get("unit")
    if n is None: return None
    return f"{n}ヶ月" if u=="MONTH" else f"{int(n):,}円"
def parse(fn):
    html=open(fn,encoding="utf-8",errors="ignore").read()
    soup=BeautifulSoup(html,"lxml")
    nd=soup.find("script",id="__NEXT_DATA__")
    r={"ok":False}
    if not nd or not nd.string: return r
    p=json.loads(nd.string).get("props",{}).get("pageProps",{}).get("property")
    if not p: return r
    r["ok"]=True
    r["building_name"]=p.get("buildingName"); r["address"]=p.get("address"); r["kind"]=p.get("buildingKind")
    m=re.search(r"(\d+)",p.get("floor") or ""); r["floor"]=int(m.group(1)) if m else None
    r["layout"]=p.get("housePlan"); r["area_m2"]=p.get("roomArea")
    r["rent"]=(p.get("price") or {}).get("number"); r["kanrihi"]=(p.get("manageCost") or {}).get("number")
    r["building_floors"]=p.get("story"); r["under_story"]=p.get("underStory")
    r["shikikin"]=money(p.get("securityDeposit")); r["reikin"]=money(p.get("keyMoney"))
    km=p.get("keyMoney") or {}; r["reikin_months"]=(km.get("number") if km.get("unit")=="MONTH" else (round(km["number"]/r["rent"],2) if km.get("number") is not None and r["rent"] else None))
    r["renewal_fee"]=money(p.get("renewalFee")); r["renewal_charge"]=money(p.get("renewalCharge")); r["repair_cost"]=money(p.get("repairCost"))
    r["structure_code"]=p.get("buildingStructure"); r["structure"]=STRUCT.get(p.get("buildingStructure") or "","その他")
    m=re.match(r"(\d{4})年(\d{1,2})月",p.get("constructionDate") or ""); r["built_year"]=int(m.group(1)) if m else None; r["built_month"]=int(m.group(2)) if m else None
    r["age_text"]=p.get("age"); r["direction"]=p.get("windowDirection")
    feats=p.get("propertyFeatures") or []
    r["features"]=[f.get("label") for f in feats if f.get("label")]
    r["elevator"]=any(f.get("kind")=="LIFT" or f.get("label")=="エレベーター" for f in feats)
    r["parking_text"]=p.get("parkingText"); r["is_parking"]=p.get("isParking")
    r["available"]=p.get("availableDate"); r["move_in_status"]=p.get("moveInStatus")
    r["transaction"]=p.get("transactionStyle"); r["insurance"]=p.get("insuranceType")
    r["special_notes"]=p.get("specialNotes"); r["remarks"]=p.get("remarks"); r["sales_point"]=p.get("salesPoint")
    r["total_units"]=p.get("totalUnitNum")
    ms=p.get("mainShop") or {}; r["shop"]=f"{ms.get('companyName','')} {ms.get('name','')}".strip(); r["shop_tel"]=ms.get("tel")
    st=[]
    for t in p.get("transportations") or []:
        ls=t.get("lineStation") or {}
        ln=(ls.get("line") or {}).get("name") or ""; stn=(ls.get("station") or {}).get("name") or ""
        if t.get("walkingMinutesFromStation") is not None:
            st.append(f"{ln} {stn}駅 徒歩{t['walkingMinutesFromStation']}分")
        elif t.get("busMinutesFromStation") is not None:
            st.append(f"{ln} {stn}駅 バス{t['busMinutesFromStation']}分 {t.get('busStopName','')} 徒歩{t.get('walkingMinutesFromBusStop')}分")
        else:
            st.append(f"{ln} {stn}駅".strip())
    if not st:
        for s in p.get("nearestStations") or []: st.append(s.get("name"))
    r["stations"]=" / ".join(x for x in st if x)
    r["is_pet"]=p.get("isPet"); r["free_internet"]=p.get("isFreeInternet"); r["autolock"]=p.get("isAutolock")
    r["renew_date"]=p.get("renewDate")
    return r
if __name__=="__main__":
    import glob
    for f in sorted(glob.glob("out/raw/eheya/detail/*.html"))[:2]:
        print(f); print(json.dumps(parse(f),ensure_ascii=False)[:1800])
    # show transportation raw structure
    soup=BeautifulSoup(open(f,encoding="utf-8").read(),"lxml")
    p=json.loads(soup.find("script",id="__NEXT_DATA__").string)["props"]["pageProps"]["property"]
    print(json.dumps(p.get("transportations"),ensure_ascii=False)[:600])
    print(json.dumps(p.get("propertyFeatures"),ensure_ascii=False)[:300])
