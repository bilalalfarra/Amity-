#!/usr/bin/env python3
"""Park Direct: fetch all ward list pages (Next.js __NEXT_DATA__), compute distance, then verify detail URLs (<=5.5 km)."""
import warnings; warnings.filterwarnings("ignore")
import re, json, os, time, math, requests
from bs4 import BeautifulSoup
from geo import dist_km
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
WARDS = {"kyoutoshishimogyouku":"下京区","kyoutoshinakagyouku":"中京区","kyoutoshiminamiku":"南区","kyoutoshiukyouku":"右京区",
         "kyoutoshikamigyouku":"上京区","kyoutoshinishikyouku":"西京区","kyoutoshihigashiyamaku":"東山区","kyoutoshikitaku":"北区","kyoutoshifushimiku":"伏見区"}
s = requests.Session(); s.headers["User-Agent"] = UA
def get(url, fn):
    if os.path.exists(fn) and os.path.getsize(fn) > 5000:
        return open(fn, encoding="utf-8").read()
    for attempt in range(2):
        r = s.get(url, timeout=30)
        if r.status_code < 500: break
        time.sleep(3)
    time.sleep(1.1)
    if r.status_code != 200:
        print("HTTP", r.status_code, url, flush=True); return None
    open(fn, "w", encoding="utf-8").write(r.text)
    return r.text
def props(html):
    sp = BeautifulSoup(html, "lxml")
    return json.loads(sp.find("script", id="__NEXT_DATA__").string)["props"]["pageProps"]
lots = {}
for slug, ward in WARDS.items():
    html = get(f"https://www.park-direct.jp/area/kyoto/{slug}", f"out/raw/parking/parkdirect_{slug}_p1.html")
    pp = props(html); total = pp["totalParkingListCount"]; pages = math.ceil(total / 20)
    items = list(pp["parkingList"])
    for p in range(2, pages + 1):
        h = get(f"https://www.park-direct.jp/area/kyoto/{slug}?page={p}", f"out/raw/parking/parkdirect_{slug}_p{p}.html")
        if h: items += props(h)["parkingList"]
    n_in = 0
    for it in items:
        d = dist_km(it.get("latitude"), it.get("longitude"))
        it["ward"] = ward; it["distance_km"] = d
        if d is not None and d <= 5.5: n_in += 1
        lots.setdefault(it["id"], it)
    print(f"{ward}: total={total} pages={pages} fetched={len(items)} within5.5={n_in}", flush=True)
allr = list(lots.values())
json.dump(allr, open("out/parkdirect_list.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
cand = [it for it in allr if it["distance_km"] is not None and it["distance_km"] <= 5.5]
print("DISTINCT", len(allr), "CANDIDATES", len(cand), flush=True)
# verify detail urls
STATUS = "out/parkdirect_detail_status.json"
status = json.load(open(STATUS)) if os.path.exists(STATUS) else {}
os.makedirs("out/raw/parking/parkdirect_detail", exist_ok=True)
for i, it in enumerate(sorted(cand, key=lambda x: x["id"]), 1):
    u = "https://www.park-direct.jp" + it["detailUrl"]
    if status.get(u) == 200: continue
    code = None
    for attempt in range(3):
        try:
            r = s.get(u, timeout=30); code = r.status_code
            if code == 202:
                time.sleep(4); continue
            if code < 500: break
        except requests.RequestException as e:
            code = f"ERR {type(e).__name__}"
        time.sleep(3)
    if code == 200 and i <= 5:
        open(f"out/raw/parking/parkdirect_detail/{it['id']}.html", "w", encoding="utf-8").write(r.text)
    status[u] = code
    if i % 20 == 0: json.dump(status, open(STATUS, "w"), indent=0); print(f"verify {i}/{len(cand)} last={code}", flush=True)
    time.sleep(1.1)
json.dump(status, open(STATUS, "w"), indent=0)
from collections import Counter
print("VERIFY DONE", Counter(map(str, status.values())), flush=True)
