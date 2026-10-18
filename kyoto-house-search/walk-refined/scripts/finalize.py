#!/usr/bin/env python3
"""Refined survey: apartments within ~3 km by bike, detached houses within 15 min walk (built 1980+),
rent ≤ 140k; key money > 2 months or > 250k goes to a separate list. -> out/final.json, out/final_dropped.json"""
import json, os, re, statistics, time, urllib.request
from geo import CENTER, dist_km

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
MAX_RENT = 140_000
HOUSE_MAX_WALK = 15
APT_MAX_BIKE_KM = 3.3          # "about 3 km"
HOUSE_MIN_YEAR = 1980
REIKIN_MAX_MONTHS, REIKIN_MAX_YEN = 2.0, 250_000
LOT_RADIUS_KM = 0.5
BANDS = [(0, 100_000, "≤ 100 ألف"), (100_001, 130_000, "100–130 ألف"), (130_001, 160_000, "130–160 ألف"),
         (160_001, 10**9, "فوق 160 ألف")]
# Locations corrected by hand after checking the listing (geocoder put them in the wrong town)
LOCATION_FIX = {"大北小路東町": (35.032967, 135.751099)}
UA = "amity-house-search/1.0 (personal flat search)"
CACHE = os.path.join(OUT, "routecache.json")
try:
    _cache = json.load(open(CACHE, encoding="utf-8"))
except Exception:
    _cache = {}


def route(profile, lat, lon):
    key = f"{profile}:{lat:.5f},{lon:.5f}"
    if key not in _cache:
        url = (f"https://routing.openstreetmap.de/routed-{profile}/route/v1/driving/"
               f"{lon},{lat};{CENTER[1]},{CENTER[0]}?overview=false")
        v = None
        for attempt in range(3):
            try:
                time.sleep(1.0)
                d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30).read())
                if d.get("code") == "Ok":
                    r = d["routes"][0]
                    v = [round(r["duration"] / 60), round(r["distance"] / 1000, 2)]
                break
            except Exception:
                time.sleep(3 * (attempt + 1))
        _cache[key] = v
        json.dump(_cache, open(CACHE, "w", encoding="utf-8"))
    return _cache[key] or [None, None]


units = json.load(open(os.path.join(OUT, "merged.json"), encoding="utf-8"))
_exp = set(json.load(open(os.path.join(OUT, "expired.json")))) if os.path.exists(os.path.join(OUT, "expired.json")) else set()
for _u in units:
    _u["sources"] = [s for s in _u["sources"] if s["url"] not in _exp]
units = [_u for _u in units if _u["sources"]]
lots = [l for l in json.load(open(os.path.join(OUT, "parking.json"), encoding="utf-8"))
        if l.get("lat") is not None and not l.get("oversize_vehicle") and (l.get("monthly_fee") or 0) <= 60000
        and "要確認" not in str(l.get("notes") or "")]

kept, dropped = [], []
for u in units:
    for k, (la, lo) in LOCATION_FIX.items():
        if k in str(u.get("address") or ""):
            u["lat"], u["lon"], u["geo_rank"], u["location_fixed"] = la, lo, 2, True
    why = []
    blob = f'{u.get("building_name") or ""} {u.get("notes") or ""}'
    if re.search(r"(貸家|一戸建|戸建|テラスハウス|タウンハウス|平屋|町家|長屋)", blob):
        u["is_house"] = True
    if u.get("coarse_address") or u.get("lat") is None:
        why.append("location unknown")
        dropped.append(dict(u, dropped_because=why)); continue
    u["walk_min"], u["walk_km"] = route("foot", u["lat"], u["lon"])
    u["bike_min"], u["bike_km"] = route("bike", u["lat"], u["lon"])
    u["distance_km"] = u["bike_km"]
    if u["rent"] > MAX_RENT:
        why.append(f"rent {u['rent']}")
    if u["is_house"]:
        if u.get("built_year") is None or u["built_year"] < HOUSE_MIN_YEAR:
            why.append(f"house built {u.get('built_year')}")
        if u["walk_min"] is None or u["walk_min"] > HOUSE_MAX_WALK:
            why.append(f"house walk {u['walk_min']} min")
    else:
        if u["bike_km"] is None or u["bike_km"] > APT_MAX_BIKE_KM:
            why.append(f"bike {u['bike_km']} km")
    rm = u.get("reikin_months") or 0
    ryen = round(rm * u["rent"]) if rm else 0
    u["reikin_yen"] = ryen
    u["reikin_over"] = rm > REIKIN_MAX_MONTHS + 0.05 or ryen > REIKIN_MAX_YEN
    u["has_reikin"] = rm > 0

    near = []
    for l in lots:
        d = dist_km(u["lat"], u["lon"], center=(l["lat"], l["lon"]))
        if d <= LOT_RADIUS_KM and l.get("monthly_fee"):
            near.append((d, l))
    near.sort(key=lambda x: x[0])
    u["nearby_parking"] = [{"name": l.get("name"), "url": l.get("url"), "monthly_fee": l["monthly_fee"], "distance_km": round(d, 2),
                            "walk_min": max(1, round(d * 1000 / 75)), "availability": l.get("availability"), "source": l.get("source")}
                           for d, l in near[:12]]
    cheapest = min(near, key=lambda x: (x[1]["monthly_fee"], x[0])) if near else None
    st, fee = u.get("parking_status"), u.get("parking_fee")
    if st == "onsite" and fee is not None:
        pk, src = fee, "onsite"
    elif st == "nearby" and fee:
        pk, src = fee, "listing_nearby"
    elif cheapest:
        pk, src = cheapest[1]["monthly_fee"], "lot"
    else:
        pk, src = None, None
    if pk is None:
        why.append("no parking price within 500 m")
    u["parking_cost"], u["parking_cost_src"] = pk, src
    u["monthly_total"] = u["rent"] + (u.get("kanrihi") or 0)
    u["monthly_total_with_parking"] = u["monthly_total"] + (pk or 0)
    u["yen_per_m2"] = round(u["rent"] / u["area_m2"]) if u.get("area_m2") else None
    u["band"] = next(i for i, (lo, hi, _) in enumerate(BANDS) if lo <= u["monthly_total_with_parking"] <= hi)
    u["dist_label"] = (f"{u['walk_min']} د مشي" if (u["walk_min"] or 99) <= 15 else f"{u['bike_min']} د مسكليت")
    (dropped if why else kept).append(dict(u, dropped_because=why) if why else u)

kept.sort(key=lambda u: (u["reikin_over"], u["band"], u["monthly_total_with_parking"]))
i = j = 0
for u in kept:
    if u["reikin_over"]:
        j += 1; u["rank"] = f"R{j}"
    else:
        i += 1; u["rank"] = str(i)
json.dump(kept, open(os.path.join(OUT, "final.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(dropped, open(os.path.join(OUT, "final_dropped.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(f"kept {len(kept)} (main {i}, reikin-over {j}) / dropped {len(dropped)}")
print("bands main:", Counter(BANDS[u['band']][2] for u in kept if not u['reikin_over']))
print("drop reasons:", Counter(re.sub(r'[\d.,]+', 'N', w) for d in dropped for w in d['dropped_because']).most_common(8))
