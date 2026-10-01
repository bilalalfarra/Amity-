#!/usr/bin/env python3
"""Apply the user's final rules to sakyo/out/merged.json:
 - real bicycle route time to the office ≤ 20 min (OSRM bike profile)
 - rent + 管理費 + parking ≤ ¥100,000 (parking = on-site fee, listed nearby fee, or cheapest
   verified monthly lot within 600 m)
 - split into 礼金 ≤ 1 month and 1–2 months
Writes out/final.json (kept) and out/final_dropped.json (with reasons)."""
import json, os
from geo import dist_km
from route import bike_route

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
MAX_MIN = 20
BUDGET = 100_000
LOT_RADIUS_KM = 0.6

units = json.load(open(os.path.join(OUT, "merged.json"), encoding="utf-8"))
lots = [l for l in json.load(open(os.path.join(OUT, "parking.json"), encoding="utf-8"))
        if l.get("lat") is not None and not l.get("oversize_vehicle") and (l.get("monthly_fee") or 0) <= 60000
        and "要確認" not in str(l.get("notes") or "")]


def lots_near(u):
    res = []
    for l in lots:
        d = dist_km(u["lat"], u["lon"], center=(l["lat"], l["lon"]))
        if d is not None and d <= LOT_RADIUS_KM:
            res.append((d, l))
    res.sort(key=lambda x: x[0])
    return res


kept, dropped = [], []
for u in units:
    mins, km = bike_route(u.get("lat"), u.get("lon"))
    u["bike_min"], u["route_km"] = mins, km
    u["straight_km"] = u.get("distance_km")
    u["distance_km"] = km
    why = []
    if mins is None:
        why.append("no route")
    elif mins > MAX_MIN:
        why.append(f"bike {mins} min")

    # parking cost
    st, fee = u.get("parking_status"), u.get("parking_fee")
    near = lots_near(u) if u.get("lat") is not None else []
    priced = sorted([(l["monthly_fee"], d, l) for d, l in near if l.get("monthly_fee")], key=lambda x: (x[0], x[1]))
    u["nearby_parking"] = [{"name": l.get("name"), "url": l.get("url"), "monthly_fee": l.get("monthly_fee"),
                            "fee_text": l.get("fee_text"), "address": l.get("address"), "distance_km": round(d, 2),
                            "walk_min": max(1, round(d * 1000 / 80)), "availability": l.get("availability")}
                           for f, d, l in priced[:3]]
    if st == "onsite" and fee is not None:
        pk, pk_src = fee, "onsite"
    elif st == "nearby" and fee:
        pk, pk_src = fee, "listing_nearby"
    elif priced:
        pk, pk_src = priced[0][0], "lot"
    else:
        pk, pk_src = None, None
    if pk_src != "onsite":
        u["parking_status"] = st if st != "onsite" else "onsite_nofee"
    u["parking_cost"], u["parking_cost_src"] = pk, pk_src
    total = u["rent"] + (u.get("kanrihi") or 0)
    u["monthly_total"] = total
    u["monthly_total_with_parking"] = total + pk if pk is not None else None
    if pk is None:
        why.append("parking cost unknown")
    elif total + pk > BUDGET:
        why.append(f"total {total + pk:,} > 100k")

    r = u.get("reikin_months")
    u["reikin_group"] = "le1" if (r is None or r <= 1.0) else "le2"

    s = 0.0
    s += max(0, 30 - (mins or 30))
    s += max(0, (BUDGET - (u["monthly_total_with_parking"] or BUDGET)) / 1500)
    s += min(15, max(0, ((u["area_m2"] or 45) - 45) * 0.75))
    s += {"A": 20, "B+": 16, "B": 12, "B-": 8, "C": 4}.get(u.get("insulation_grade"), 0)
    s += 6 if pk_src == "onsite" else 0
    s += 4 if u.get("elevator") is True else 0
    s += 4 if (r or 0) == 0 else 0
    s += 3 if u.get("structure") in ("RC", "SRC") else 0
    u["score"] = round(s, 1)
    u["near"] = False
    if why == [f"bike {mins} min"] and mins is not None and mins <= 25:
        u["near"] = True                      # only fails the 20-min rule, by ≤ 5 min
        kept.append(u)
    elif why:
        u["dropped_because"] = why
        dropped.append(u)
    else:
        kept.append(u)

kept.sort(key=lambda u: -u["score"])
i = 0
for u in kept:
    if u["near"]:
        i += 1
        u["rank"] = f"N{i}"
for grp in ("le1", "le2"):
    i = 0
    for u in kept:
        if u["reikin_group"] == grp and not u["is_house"] and not u["near"]:
            i += 1
            u["rank"] = f"{'' if grp == 'le1' else 'K'}{i}"
i = 0
for u in kept:
    if u["is_house"] and not u["near"]:
        i += 1
        u["rank"] = f"H{i}"

json.dump(kept, open(os.path.join(OUT, "final.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(dropped, open(os.path.join(OUT, "final_dropped.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(f"kept {len(kept)} / dropped {len(dropped)}")
print("kept groups:", Counter((u['reikin_group'], 'house' if u['is_house'] else u['tier']) for u in kept))
print("drop reasons:", Counter(w.split(' ')[0] + ' ' + w.split(' ')[1] for d in dropped for w in d['dropped_because']).most_common(8))
