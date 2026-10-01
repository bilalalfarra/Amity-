import re,glob,json,warnings
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
rooms={}
for f in sorted(glob.glob("out/raw/eheya/list_*_p*.html")):
    soup=BeautifulSoup(open(f,encoding="utf-8",errors="ignore").read(),"lxml")
    for cas in soup.select("div[class^=styles_cassette__]"):
        h2=cas.find("h2")
        if not h2: continue
        kind=h2.find("span"); kind_t=kind.get_text(strip=True) if kind else ""
        name=h2.get_text(" ",strip=True).replace(kind_t,"").strip()
        lib=cas.find("a",href=re.compile(r"/library/detail/"))
        ag=cas.select_one('[data-testid="InfoContent_ageAndStory"]'); ag=ag.get_text(" ",strip=True) if ag else ""
        m=re.search(r"築(\d+)年",ag); age=int(m.group(1)) if m else (0 if "新築" in ag else None)
        m=re.search(r"(\d+)階建",ag); bfl=int(m.group(1)) if m else None
        tr=cas.select_one('[data-testid="InfoContent_transportation"]'); tr=tr.get_text(" ",strip=True) if tr else None
        ad=cas.select_one('[data-testid="InfoContent_address"]'); ad=ad.get_text(" ",strip=True) if ad else None
        for pc in cas.select('[data-testid="BuildingCassette_propertyCassette"]'):
            a=pc.find("a",href=re.compile(r"/detail/\d+/"))
            if not a: continue
            url="https://www.eheya.net"+a["href"]
            fl=pc.select_one('[data-testid="BuildingPropertyCassette_floorRoomPicto"]'); fl=fl.get_text(" ",strip=True) if fl else ""
            m=re.search(r"(\d+)階",fl); floor=int(m.group(1)) if m else None
            rp=pc.select_one(".styles_rentPrice__JuPfB") or pc.select_one('[class*=rentPrice]')
            rent=int(round(float(rp.get_text(strip=True))*10000)) if rp else None
            mf=pc.select_one('[data-testid="BuildingPropertyCassette_managementFee"]'); mf=mf.get_text(" ",strip=True) if mf else ""
            m=re.search(r"([\d,]+)円",mf); kanrihi=int(m.group(1).replace(",","")) if m else (0 if "なし" in mf or "-" in mf else None)
            money=[x.get_text(strip=True) for x in pc.select('[class*=moneyText]')]
            shiki=money[0] if len(money)>0 else None; rei=money[1] if len(money)>1 else None
            rd=pc.select_one('[data-testid="BuildingPropertyCassette_roomDetail"]'); rd=rd.get_text(" ",strip=True) if rd else ""
            m=re.match(r"\s*(\S+?)\s*/\s*([\d.]+)",rd); layout=m.group(1) if m else None; area=float(m.group(2)) if m else None
            rooms[url]={"url":url,"bname":name,"btype":kind_t,"age":age,"bfloors":bfl,"station":tr,"addr":ad,"floor":floor,"rent":rent,"kanrihi":kanrihi,"shiki":shiki,"rei":rei,"layout":layout,"area":area,"file":f}
json.dump(list(rooms.values()),open("out/raw/eheya/rooms_raw.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("rooms",len(rooms))
import collections
print(collections.Counter(r["layout"] for r in rooms.values()).most_common(20))
for r in list(rooms.values())[:3]: print(r)
