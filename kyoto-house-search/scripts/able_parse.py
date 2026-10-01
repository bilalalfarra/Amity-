import re,glob,json,warnings,sys,time,os
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
sys.path.insert(0,".")
from geo import geocode,dist_km
rooms={}
for f in sorted(glob.glob("out/raw/able/list*_p*.html")):
    sweep="B" if "/listB_" in f else "A"
    soup=BeautifulSoup(open(f,encoding="utf-8").read(),"lxml")
    for sec in soup.select("section.m-list_cassette"):
        h2=sec.select_one(".list_ttl h2"); 
        if not h2: continue
        kind=h2.select_one("li"); kind_t=kind.get_text(strip=True) if kind else ""
        a=h2.find("a",href=True); name=a.get_text(strip=True) if a else h2.get_text(strip=True)
        bk=a.get("data-bkkey") if a else None
        info={}
        for tr in sec.select("table.l-table tr"):
            cells=tr.find_all(["th","td"])
            for j in range(len(cells)-1):
                if cells[j].name=="th" and cells[j+1].name=="td":
                    k=cells[j].get_text(" ",strip=True); v=cells[j+1].get_text(" ",strip=True)
                    if k and k not in info: info[k]=v
        addr=re.sub(r"周辺地図.*$","",info.get("住所","")).strip()
        m=re.search(r"showGoogleMap\(([\d.]+),\s*([\d.]+)",str(sec)); glat=float(m.group(1)) if m else None; glon=float(m.group(2)) if m else None
        m=re.match(r"(\d{4})年(\d{1,2})月",info.get("築年","")); by=int(m.group(1)) if m else None; bm=int(m.group(2)) if m else None
        m=re.search(r"(\d+)階建",info.get("階建","")); bfl=int(m.group(1)) if m else None
        sraw=info.get("構造","")
        for tr in sec.select("table tr.detail-inner"):
            fl=tr.select_one("td.floar"); fl=fl.get_text(" ",strip=True) if fl else ""
            m=re.search(r"(\d+)階",fl); floor=int(m.group(1)) if m else None
            prices=tr.select("td.price")
            rent=None;kanrihi=None;shiki=None;rei=None
            if len(prices)>=1:
                pt=prices[0].get_text(" ",strip=True)
                m=re.search(r"([\d.]+)\s*万円",pt); rent=int(round(float(m.group(1))*10000)) if m else None
                m=re.search(r"万円\s*([\d,]+)円",pt); kanrihi=int(m.group(1).replace(",","")) if m else (0 if re.search(r"万円\s*(--|なし|-)",pt) else None)
            if len(prices)>=2:
                parts=[x.strip() for x in prices[1].get_text("|",strip=True).split("|") if x.strip()]
                shiki=parts[0] if len(parts)>0 else None; rei=parts[1] if len(parts)>1 else None
            lay=tr.select_one("td.layout"); lt=lay.get_text("|",strip=True) if lay else ""
            m=re.match(r"([^|]+)\|([\d.]+)",lt); layout=m.group(1).strip() if m else None; area=float(m.group(2)) if m else None
            link=tr.select_one("a.js-detailLink"); rbk=link.get("data-bkkey") if link else bk
            if not rbk: continue
            url=f"https://www.able.co.jp/detail/Detail.do?bk={rbk}&prefkey=kyoto"
            cm=sec.select_one(".pr-comment"); cm=cm.get_text(" ",strip=True) if cm else ""
            shop=sec.select_one("#shopName"); shop=shop.get_text(strip=True) if shop else None
            tags=[li.get_text(strip=True) for li in sec.select(".bukken-tag li")]
            rooms[rbk]={"url":url,"bk":rbk,"bname":name,"btype":kind_t,"addr":addr,"glat":glat,"glon":glon,"built_year":by,"built_month":bm,"bfloors":bfl,"structure_raw":sraw,
                        "station":info.get("交通"),"floor":floor,"rent":rent,"kanrihi":kanrihi,"shiki":shiki,"rei":rei,"layout":layout,"area":area,"comment":cm[:200],"shop":shop,"tags":tags,"sweep":sweep,"file":f}
print("rooms",len(rooms))
def struct(s):
    if "鉄骨鉄筋" in s: return "SRC"
    if "鉄筋" in s: return "RC"
    if "軽量鉄骨" in s: return "軽量鉄骨"
    if "重量鉄骨" in s: return "重量鉄骨"
    if "鉄骨" in s: return "鉄骨"
    if "木造" in s: return "木造"
    return "その他"
stats={"total":len(rooms),"age":0,"rent":0,"floor1":0,"far":0,"nogeo":0,"keep":0}
cands=[]
for r in rooms.values():
    st=struct(r["structure_raw"]); r["structure"]=st
    by=r["built_year"]
    house=("戸建" in r["btype"] or "テラス" in r["btype"] or "貸家" in r["btype"])
    if by is None: stats["age"]+=1; continue
    if by>=2001: tier="house" if house else "A"
    elif by>=1991 and st in ("RC","SRC"): tier="B"
    else: stats["age"]+=1; continue
    if r["rent"] is None or r["rent"]>100000: stats["rent"]+=1; continue
    if r["floor"]==1 and tier!="house": stats["floor1"]+=1; continue
    if r["glat"] and r["glon"]: lat,lon=r["glat"],r["glon"]
    else: lat,lon=geocode(r["addr"])
    dk=dist_km(lat,lon)
    if dk is None: stats["nogeo"]+=1; continue
    if dk>5.5: stats["far"]+=1; continue
    r["tier"]=tier; r["lat"]=lat; r["lon"]=lon; r["distance_km"]=dk
    cands.append(r); stats["keep"]+=1
print(stats)
json.dump(cands,open("out/raw/able/candidates.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for c in sorted(cands,key=lambda x:x["distance_km"])[:8]: print(c["distance_km"],c["bname"],c["layout"],c["area"],c["rent"],c["built_year"],c["structure"],c["floor"],"/",c["bfloors"],c["tier"])
