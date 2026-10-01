#!/usr/bin/env python3
"""Parse saved Times (times-info.net) monthly list pages, geocode, filter <=5.5 km, then fetch detail pages for 200 verification."""
import warnings; warnings.filterwarnings("ignore")
import re, json, os, time, requests
from bs4 import BeautifulSoup
from geo import geocode, dist_km
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
WARD = {"C101":"北区","C102":"上京区","C104":"中京区","C105":"東山区","C106":"下京区","C107":"南区","C108":"右京区","C109":"伏見区","C111":"西京区"}
rows = []
for code, ward in WARD.items():
    html = open(f"out/raw/parking/times_{code}.html", encoding="utf-8").read()
    s = BeautifulSoup(html, "lxml")
    for a in s.select("a.searchResult-parkingList_card_item[href*='park-detail-']"):
        name = a.select_one(".searchResult-parkingList_card_ttl").get_text(strip=True)
        addr = a.select_one(".searchResult-parkingList_card_address").get_text(strip=True)
        st = a.select_one(".searchResult-parkingList_card_status")
        status = " ".join(x.get_text(strip=True) for x in st.select("span")) if st else None
        price_el = a.select_one(".searchResult-parkingList_card_price")
        fee_text = price_el.get_text(" ", strip=True).replace("使用料:", "").strip() if price_el else None
        cat = a.select_one(".searchResult-parkingList_card_category")
        fac = [x.get_text(strip=True) for x in a.select(".searchResult-parkingList_card_facilities_item")]
        m = re.search(r"(\d[\d,]*)円", fee_text or "")
        fee = int(m.group(1).replace(",", "")) if m else None
        lat, lon = geocode(addr)
        d = dist_km(lat, lon)
        rows.append({"source": "times", "url": "https://times-info.net" + a["href"], "name": name, "address": addr,
                     "lat": lat, "lon": lon, "distance_km": d, "monthly_fee": fee, "fee_text": fee_text,
                     "availability": status, "ward": ward, "category": cat.get_text(strip=True) if cat else None,
                     "facilities": fac})
print("parsed", len(rows), "| geocoded", sum(r["lat"] is not None for r in rows), "| within 5.5km", sum((r["distance_km"] or 99) <= 5.5 for r in rows))
json.dump(rows, open("out/times_list.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# fetch detail pages for those within range
keep = [r for r in rows if r["distance_km"] is not None and r["distance_km"] <= 5.5]
os.makedirs("out/raw/parking/times_detail", exist_ok=True)
STATUS = "out/times_detail_status.json"
status = json.load(open(STATUS)) if os.path.exists(STATUS) else {}
s = requests.Session(); s.headers["User-Agent"] = UA
for i, r in enumerate(keep, 1):
    u = r["url"]
    if status.get(u) == 200: continue
    bid = re.search(r"park-detail-(BUK\d+)", u).group(1)
    code = None
    for attempt in range(2):
        try:
            resp = s.get(u, timeout=30); code = resp.status_code
            if code < 500: break
        except requests.RequestException as e:
            code = f"ERR {type(e).__name__}"
        time.sleep(3)
    if code == 200:
        resp.encoding = resp.apparent_encoding or "utf-8"
        open(f"out/raw/parking/times_detail/{bid}.html", "w", encoding="utf-8").write(resp.text)
    status[u] = code
    if i % 10 == 0: json.dump(status, open(STATUS, "w"), indent=0); print(f"{i}/{len(keep)} last={code}", flush=True)
    time.sleep(1.1)
json.dump(status, open(STATUS, "w"), indent=0)
from collections import Counter
print("DETAIL DONE", Counter(map(str, status.values())))
