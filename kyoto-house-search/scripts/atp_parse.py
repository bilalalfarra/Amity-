#!/usr/bin/env python3
"""Parse saved at-parking detail pages + status sources into out/atparking_lots.json"""
import warnings; warnings.filterwarnings("ignore")
import re, glob, json, os, collections, time, requests
from bs4 import BeautifulSoup
from geo import dist_km, geocode
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
WARD = {"shimogyo":"下京区","nakagyo":"中京区","minami":"南区","ukyo":"右京区","kamigyo":"上京区","nishikyo":"西京区","higashiyama":"東山区","kita":"北区","fushimi":"伏見区","sakyo":"左京区","yamashina":"山科区"}
# 1) statuses: ward result pages (retry 右京区 with shorter query) + vicinity harvest
if os.path.getsize("out/raw/parking/atparking_result_右京区.html") < 30000:
    r = requests.get("https://www.at-parking.jp/result/index.php", params={"action":"input","text_input":"右京区"}, headers={"User-Agent":UA}, timeout=30)
    open("out/raw/parking/atparking_result_右京区.html","w",encoding="utf-8").write(r.text); print("右京区 retry", r.status_code, len(r.text))
status = {}
for fn in glob.glob("out/raw/parking/atparking_result_*.html"):
    s = BeautifulSoup(open(fn, encoding="utf-8").read(), "lxml")
    for li in s.select("li.dtlList"):
        a = li.find("a", href=re.compile(r"/(\d+)\.html")); img = li.find("img", src=re.compile(r"icon_status"))
        if a and img: status[re.search(r"/(\d+)\.html", a["href"]).group(1)] = img.get("alt")
print("result-page statuses:", len(status))
vic = json.load(open("out/atparking_vicinity_status.json"))
for k, v in vic.items(): status.setdefault(k, v)
print("merged statuses:", len(status))
# 2) detail pages
cand = {r["pno"]: r for r in json.load(open("out/atparking_candidates.json"))}
dstat = json.load(open("out/atp_detail_status.json"))
def yen(t):
    m = re.search(r"(\d[\d,]*)\s*円", t or "")
    return int(m.group(1).replace(",", "")) if m else None
rows = []; bikes = 0
for fn in sorted(glob.glob("out/raw/parking/atp_detail/*.html")):
    pno = os.path.basename(fn)[:-5]
    s = BeautifulSoup(open(fn, encoding="utf-8").read(), "lxml")
    nb = s.find(id="neighborhood")
    lat = lon = None; open_fee = None
    if nb:
        oi = nb.select_one("div.openInfo p.adress")
        if oi:
            mm = re.search(r"賃料[：:]\s*(.+)$", oi.get_text(" ", strip=True))
            if mm: open_fee = mm.group(1).strip()
        li, lg = nb.find("input", class_="lat"), nb.find("input", class_="lng")
        try: lat, lon = float(li["value"]), float(lg["value"])
        except Exception: pass
        nb.decompose()
    c = cand.get(pno, {})
    kv = {}
    for tr in s.select("table.graph tr"):
        tds = tr.find_all("td")
        if len(tds) >= 2:
            kv[tds[-2].get_text(" ", strip=True)] = tds[-1].get_text(" ", strip=True)
    name = kv.get("駐車場名称"); addr = kv.get("駐車場所在地", "")
    addr_clean = re.sub(r"^〒\d{3}-\d{4}\s*", "", addr)
    fee_text = kv.get("賃料") or open_fee or c.get("price_display")
    if fee_text in ("-", "", None): fee_text = None
    nums = [int(x.replace(",", "")) for x in re.findall(r"(\d[\d,]*)\s*(?=～|円)", fee_text or "")]
    fee_min = min(nums) if nums else None; fee_max = max(nums) if nums else None
    if lat is None: lat, lon = c.get("lat"), c.get("lon")
    d = dist_km(lat, lon)
    url = c.get("url") or f"https://www.at-parking.jp/search/kyoto/x/x/{pno}.html"
    m = re.search(r"kyoto-shi_(\w+)-ku", url); ward = WARD.get(m.group(1)) if m else None
    cars = kv.get("対応車種", "")
    is_bike = ("バイク" in (name or "")) or (cars and set(re.split(r"[、,/／ ]+", cars)) <= {"バイク", "原付", ""})
    if is_bike: bikes += 1; continue
    notes = []
    for k in ("敷金","礼金","更新料","仲介手数料"):
        v = kv.get(k)
        if v: notes.append(f"{k} {v.split('※')[0].strip()}")
    for k in ("対応車種","屋内外","利用可能時間","駐車場スペック"):
        v = kv.get(k)
        if v and v != "-":
            vv = re.sub(r"\s+", " ", v)[:80]
            notes.append(f"{k}: {vv}")
    ic = c.get("icons", {})
    feats = [n for k, n in (("24h","24時間"),("bigcar","大型車可"),("highroof","ハイルーフ可"),("m","機械式"),("s","自走式"),("indoor","屋内"),("outdoor","屋外")) if ic.get(k) == "1"]
    if feats: notes.append("特徴: " + "/".join(feats))
    if c.get("updated"): notes.append("更新 " + c["updated"][:10])
    rows.append({"source":"at-parking","url":url,"name":name or c.get("name"),"address":addr_clean or c.get("address"),"postal":(re.match(r"〒(\d{3}-\d{4})",addr) or [None,None])[1],
                 "lat":lat,"lon":lon,"distance_km":d,"ward":ward,"monthly_fee":fee_min,"fee_max":fee_max,
                 "fee_text":(fee_text or c.get("price_display") or None),"availability":status.get(pno),"notes":"; ".join(notes),
                 "http_status":dstat.get(url)})
print("parsed", len(rows), "| bike-only skipped", bikes, "| with fee", sum(r["monthly_fee"] is not None for r in rows), "| with status", sum(bool(r["availability"]) for r in rows), "| within5.5", sum((r["distance_km"] or 99) <= 5.5 for r in rows))
print(collections.Counter(r["ward"] for r in rows))
print(collections.Counter(r["availability"] for r in rows))
json.dump(rows, open("out/atparking_lots.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(rows[0], ensure_ascii=False)[:900])
