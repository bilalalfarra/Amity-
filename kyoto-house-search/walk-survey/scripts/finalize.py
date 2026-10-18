#!/usr/bin/env python3
"""Walking-distance price survey: keep homes ≤ MAX_WALK min on foot from the office, attach parking cost,
compute the all-in monthly total and the price band. -> out/final.json, out/final_dropped.json"""
import json, os, statistics, time, urllib.request
from geo import CENTER, dist_km

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
MAX_WALK = int(os.environ.get("MAX_WALK", "10"))
NEAR_WALK = int(os.environ.get("NEAR_WALK", "15"))
LOT_RADIUS_KM = 0.5
BANDS = [(0, 100_000, "≤ 100 ألف"), (100_001, 130_000, "100–130 ألف"), (130_001, 160_000, "130–160 ألف"),
         (160_001, 200_000, "160–200 ألف"), (200_001, 10**9, "فوق 200 ألف")]
CACHE = os.path.join(OUT, "walkcache.json")
UA = "amity-house-search/1.0 (personal flat search)"
try:
    _cache = json.load(open(CACHE, encoding="utf-8"))
except Exception:
    _cache = {}


def walk(lat, lon):
    key = f"{lat:.5f},{lon:.5f}"
    if key not in _cache:
        url = (f"https://routing.openstreetmap.de/routed-foot/route/v1/driving/"
               f"{lon},{lat};{CENTER[1]},{CENTER[0]}?overview=false")
        v = None
        for attempt in range(3):
            try:
                time.sleep(1.0)
                d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read())
                if d.get("code") == "Ok":
                    r = d["routes"][0]
                    v = [round(r["duration"] / 60), int(r["distance"])]
                break
            except Exception:
                time.sleep(3 * (attempt + 1))
        _cache[key] = v
        json.dump(_cache, open(CACHE, "w", encoding="utf-8"))
    return _cache[key]


units = json.load(open(os.path.join(OUT, "merged.json"), encoding="utf-8"))
lots = [l for l in json.load(open(os.path.join(OUT, "parking.json"), encoding="utf-8"))
        if l.get("lat") is not None and not l.get("oversize_vehicle") and (l.get("monthly_fee") or 0) <= 60000
        and "要確認" not in str(l.get("notes") or "")]
area_fees = [l["monthly_fee"] for l in lots if l.get("monthly_fee") and dist_km(l["lat"], l["lon"]) <= 1.0]
AREA_MEDIAN = int(statistics.median(area_fees)) if area_fees else 15000

kept, dropped = [], []
for u in units:
    w = walk(u["lat"], u["lon"]) if u.get("lat") is not None else None
    u["walk_min"], u["walk_m"] = (w or [None, None])
    why = []
    if u.get("coarse_address"):
        why.append("address only gives the ward")
    if u["walk_min"] is None:
        why.append("no walking route")
    elif u["walk_min"] > NEAR_WALK:
        why.append(f"walk {u['walk_min']} min")
    u["near"] = u["walk_min"] is not None and u["walk_min"] > MAX_WALK

    near = []
    for l in lots:
        d = dist_km(u["lat"], u["lon"], center=(l["lat"], l["lon"])) if u.get("lat") is not None else None
        if d is not None and d <= LOT_RADIUS_KM and l.get("monthly_fee"):
            near.append((l["monthly_fee"], d, l))
    near.sort(key=lambda x: (x[0], x[1]))
    u["nearby_parking"] = [{"name": l.get("name"), "url": l.get("url"), "monthly_fee": f, "distance_km": round(d, 2),
                            "walk_min": max(1, round(d * 1000 / 75)), "availability": l.get("availability")}
                           for f, d, l in near[:3]]
    st, fee = u.get("parking_status"), u.get("parking_fee")
    if st == "onsite" and fee is not None:
        pk, src = fee, "onsite"
    elif st == "nearby" and fee:
        pk, src = fee, "listing_nearby"
    elif near:
        pk, src = near[0][0], "lot"
    else:
        pk, src = AREA_MEDIAN, "estimate"
    u["parking_cost"], u["parking_cost_src"] = pk, src
    u["monthly_total"] = u["rent"] + (u.get("kanrihi") or 0)
    u["monthly_total_with_parking"] = u["monthly_total"] + pk
    u["yen_per_m2"] = round(u["rent"] / u["area_m2"]) if u.get("area_m2") else None
    u["has_reikin"] = (u.get("reikin_months") or 0) > 0
    u["band"] = next(i for i, (lo, hi, _) in enumerate(BANDS) if lo <= u["monthly_total_with_parking"] <= hi)
    (dropped if why else kept).append(dict(u, dropped_because=why) if why else u)

kept.sort(key=lambda u: (u["near"], u["band"], u["has_reikin"], u["monthly_total_with_parking"]))
i = j = 0
for u in kept:
    if u["near"]:
        j += 1; u["rank"] = f"N{j}"
    else:
        i += 1; u["rank"] = str(i)
json.dump(kept, open(os.path.join(OUT, "final.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(dropped, open(os.path.join(OUT, "final_dropped.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(f"kept {len(kept)} / dropped {len(dropped)}; parking median within 1 km = {AREA_MEDIAN}")
print("bands:", Counter((BANDS[u['band']][2], 'reikin' if u['has_reikin'] else 'no-reikin') for u in kept))
print("parking source:", Counter(u["parking_cost_src"] for u in kept))
