#!/usr/bin/env python3
"""Fetch at-parking.jp map pages per ward and parse the embedded latlngList into candidates (<= 5.5 km)."""
import re, json, time, os, sys, requests
from geo import dist_km, CENTER
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
WARDS = {"kyoto-shi_shimogyo-ku":"下京区","kyoto-shi_nakagyo-ku":"中京区","kyoto-shi_minami-ku":"南区",
         "kyoto-shi_ukyo-ku":"右京区","kyoto-shi_kamigyo-ku":"上京区","kyoto-shi_nishikyo-ku":"西京区",
         "kyoto-shi_higashiyama-ku":"東山区","kyoto-shi_kita-ku":"北区","kyoto-shi_fushimi-ku":"伏見区"}
RAW = "out/raw/parking"; os.makedirs(RAW, exist_ok=True)
s = requests.Session(); s.headers["User-Agent"] = UA
allrows = []
for slug, ward in WARDS.items():
    fn = f"{RAW}/atparking_map_{slug}.html"
    if os.path.exists(fn) and os.path.getsize(fn) > 10000:
        html = open(fn, encoding="utf-8").read()
    else:
        for attempt in range(2):
            r = s.get(f"https://www.at-parking.jp/searchp/kyoto/{slug}/", timeout=30)
            if r.status_code < 500: break
            time.sleep(3)
        r.encoding = "utf-8"
        html = r.text
        open(fn, "w", encoding="utf-8").write(html)
        time.sleep(1.1)
    ents = re.findall(r"latlngList\[\d+\]\s*=\s*\{(.*?)\};", html, re.S)
    n_in = 0
    for e in ents:
        d = dict(re.findall(r"(\w+):\s*'((?:[^'\\]|\\.)*)'", e))
        try:
            lat, lon = float(d.get("lat") or "nan"), float(d.get("lng") or "nan")
        except ValueError:
            lat = lon = None
        dk = dist_km(lat, lon) if lat == lat and lon == lon else None
        row = {"ward": ward, "pno": d.get("no"), "lat": lat, "lon": lon, "distance_km": dk,
               "url": "https://www.at-parking.jp" + d.get("url", ""), "name": d.get("name"),
               "price_display": d.get("list_price_display"), "address": d.get("address"),
               "icons": {k.replace("icon_", "").replace("_display", ""): v for k, v in d.items() if k.startswith("icon_")},
               "rec_flg": d.get("rec_flg"), "updated": d.get("daysago")}
        allrows.append(row)
        if dk is not None and dk <= 5.5: n_in += 1
    print(f"{ward}: {len(ents)} lots on map page, {n_in} within 5.5 km", flush=True)
json.dump(allrows, open("out/atparking_map_all.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
cand = [r for r in allrows if r["distance_km"] is not None and r["distance_km"] <= 5.5]
json.dump(cand, open("out/atparking_candidates.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("TOTAL", len(allrows), "CANDIDATES", len(cand), "distinct urls", len({r['url'] for r in cand}))
