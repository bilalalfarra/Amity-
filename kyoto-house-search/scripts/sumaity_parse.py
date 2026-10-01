import re,glob,json,sys,warnings
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
sys.path.insert(0,".")
from geo import geocode,dist_km
def num(s):
    s=s.replace(",","")
    m=re.search(r"[\d.]+",s); return float(m.group()) if m else None
rooms=[]
for f in sorted(glob.glob("out/raw/sumaity/list_*_p*.html")):
    soup=BeautifulSoup(open(f,encoding="utf-8").read(),"lxml")
    for b in soup.select("div.building"):
        t=b.get_text(" | ",strip=True)
        bl=b.find("a",href=re.compile(r"/chintai/kyoto_bldg/bldg_\d+/"))
        name=bl.get_text(strip=True) if bl else None
        # address: text containing 京都府京都市
        m=re.search(r"京都府京都市\S+?(?= \| )",t)
        addr=m.group(0) if m else None
        age=re.search(r"築年数 \| (築\d+年|新築)",t); age=age.group(1) if age else None
        st=re.search(r"構造 \| ([^|]+?) \|",t); st=st.group(1).strip() if st else None
        fl=re.search(r"総階数 \| (\d+)階建",t); fl=int(fl.group(1)) if fl else None
        btype=t.split(" | ")[0]
        for a in b.find_all("a",href=re.compile(r"/chintai/kyoto_prop/prop_\d+/")):
            # room row container
            tr=a.find_parent("tr") or a.find_parent("li") or a.find_parent("div")
            rt=tr.get_text(" | ",strip=True) if tr else ""
            rooms.append({"file":f,"bname":name,"btype":btype,"addr":addr,"age":age,"structure":st,"bfloors":fl,"url":a["href"],"row":rt[:300]})
# dedupe by url
seen=set(); uniq=[]
for r in rooms:
    if r["url"] in seen: continue
    seen.add(r["url"]); uniq.append(r)
print("rooms",len(rooms),"unique",len(uniq))
json.dump(uniq,open("out/raw/sumaity/rooms_raw.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for r in uniq[:5]: print(r)
