#!/usr/bin/env python3
"""Merge the per-site JSON files written by the search agents into one ranked list.

- normalises fields, re-geocodes anything missing lat/lon
- dedupes the same unit found on several sites (keeps every source URL)
- re-applies the hard filters from spec.md (defensive; agents may differ)
- computes bike time, an insulation grade, nearest monthly parking lots, and a rank score
- writes out/merged.json and out/merged_dropped.json
"""
import glob, json, os, re, sys
from geo import geocode, dist_km, bike_minutes

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT_DIR") or os.path.join(HERE, "out")
SKIP_FILES = {"parking.json", "geocache.json", "merged.json", "merged_dropped.json", "ur.json"}  # ur.json is rendered separately (vacancy unverifiable)

MAX_RENT = 100_000
MIN_AREA = 45.0
MAX_DIST = 5.5           # straight-line km; ~20–25 min by bicycle
OK_LAYOUT = re.compile(r"^(2S?LDK|[3-9]S?[LD]?DK|[3-9]S?LDK|[3-9]S?K|[3-9]DK|[5-9]K)")  # 2LDK+, 3DK+, excludes 1LDK/2DK/2K


def to_int(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v).replace(",", "").replace("円", "").replace("¥", "")
    m = re.search(r"(\d+(?:\.\d+)?)\s*万", s)
    if m:
        return int(float(m.group(1)) * 10000)
    m = re.search(r"\d+", s)
    return int(m.group(0)) if m else None


def to_float(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    m = re.search(r"\d+(?:\.\d+)?", str(v))
    return float(m.group(0)) if m else None


def norm_layout(s):
    if not s:
        return None
    s = str(s).upper().replace("Ｌ", "L").replace("Ｄ", "D").replace("Ｋ", "K").replace("Ｓ", "S")
    s = re.sub(r"[^0-9A-Z+]", "", s)
    return s or None


def norm_structure(s):
    if not s:
        return None
    t = str(s)
    if "鉄骨鉄筋" in t or "SRC" in t.upper():
        return "SRC"
    if "鉄筋" in t or t.upper().startswith("RC"):
        return "RC"
    if "軽量" in t:
        return "軽量鉄骨"
    if "重量" in t:
        return "重量鉄骨"
    if "鉄骨" in t or t.upper() in ("S", "S造"):
        return "鉄骨"
    if "木" in t:
        return "木造"
    if t in ("RC", "SRC", "重量鉄骨", "軽量鉄骨", "鉄骨", "木造"):
        return t
    return "その他"


def months_of_rent(text, rent):
    """Return key money / deposit as months of rent (float) or None."""
    if text is None:
        return None
    if isinstance(text, (int, float)):
        return round(float(text) / rent, 2) if rent else None
    s = str(text)
    if re.search(r"(なし|無|0円|^0$|-|－|ー)", s) and not re.search(r"[1-9]", s):
        return 0.0
    m = re.search(r"(\d+(?:\.\d+)?)\s*(ヶ月|か月|カ月|ヵ月|ケ月)", s)
    if m:
        return float(m.group(1))
    yen = to_int(s)
    if yen is not None and rent:
        return round(yen / rent, 2)
    return None


def zen2han(s):
    """Full-width digits/letters/spaces -> half-width; unify small ke/ga variants."""
    s = str(s).translate(str.maketrans("０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ　",
                                      "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "))
    return s.replace("ヶ", "ケ").replace("ヵ", "カ").replace("が", "ケ").replace("之", "ノ").replace("の", "ノ")


def norm_address(a):
    if not a:
        return ""
    a = re.sub(r"\s+", "", zen2han(a))
    a = a.replace("京都府", "").replace("京都市", "")
    a = re.sub(r"(丁目|番地|番|号)", "-", a)
    a = re.sub(r"[－ー−]", "-", a)
    a = a.rstrip("-")
    return a


def insulation_grade(built_year, structure):
    """Rough thermal-comfort grade from era + structure (Japan energy standards: 1980 / 1992 / 1999 / 2013)."""
    if not built_year:
        return ("?", "سنة البناء غير معروفة — اسأل الوكيل")
    s = structure or ""
    if built_year >= 2015:
        return ("A", "بناء حديث (معيار الطاقة 2013)؛ عزل جيد عادةً")
    if built_year >= 2001:
        if s == "軽量鉄骨":
            return ("B-", "ما بعد معيار 1999 لكن هيكل فولاذي خفيف؛ اسأل عن العزل والضجيج")
        if s == "木造":
            return ("B", "خشبي ما بعد معيار 1999؛ العزل حسب الشركة المنفّذة")
        return ("B+", "ما بعد معيار 1999 (次世代省エネ基準)؛ RC/SRC كتلة حرارية جيدة")
    if built_year >= 1991 and s in ("RC", "SRC"):
        return ("C", "معيار 1992؛ RC يحفظ الحرارة لكن النوافذ غالباً زجاج مفرد — تحقق من ساشي/زجاج مزدوج")
    return ("D", "قديم — لا يُنصح به من ناحية العزل")


def load_parking():
    p = os.path.join(OUT, "parking.json")
    if not os.path.exists(p):
        return []
    try:
        lots = json.load(open(p, encoding="utf-8"))
    except Exception:
        return []
    good = []
    for l in lots:
        if l.get("lat") is None or l.get("lon") is None:
            continue
        if l.get("oversize_vehicle"):          # bus / truck bays
            continue
        if l.get("monthly_fee") and l["monthly_fee"] > 60000:   # not a normal passenger-car space
            continue
        good.append(l)
    return good


def nearest_lots(lat, lon, lots, k=3, max_km=0.8):
    if lat is None or lon is None:
        return []
    res = []
    for l in lots:
        d = dist_km(lat, lon, center=(l["lat"], l["lon"]))
        if d is not None and d <= max_km:
            res.append((d, l))
    res.sort(key=lambda x: (x[0], x[1].get("monthly_fee") or 10**9))
    return [{"name": l.get("name"), "url": l.get("url"), "monthly_fee": l.get("monthly_fee"),
             "fee_text": l.get("fee_text"), "address": l.get("address"), "distance_km": round(d, 2),
             "walk_min": max(1, round(d * 1000 / 80))} for d, l in res[:k]]


def parking_status(text):
    """-> ('onsite'|'onsite_full'|'nearby'|'none'|'unknown', fee_int_or_None)"""
    if text is None:
        return ("unknown", None)
    s = str(text)
    fee = None
    m = re.search(r"(\d[\d,]*)\s*円", s)
    if m:
        fee = int(m.group(1).replace(",", ""))
    else:
        m = re.search(r"(\d+(?:\.\d+)?)\s*万", s)
        if m:
            fee = int(float(m.group(1)) * 10000)
    if "無料" in s:
        return ("onsite", 0)
    if re.search(r"(近隣|周辺|付近)", s):
        return ("nearby", fee)
    if re.search(r"(空無|空き無|空きなし|満車|空車なし)", s):
        return ("onsite_full", fee)
    if re.search(r"(無|なし|ナシ|不可)", s) and not re.search(r"有", s):
        return ("none", None)
    if re.search(r"(敷地内|空有|空き有|有|あり)", s) or fee:
        return ("onsite", fee)
    return ("unknown", fee)


def main():
    SOURCE_FILES = ["suumo", "homes", "athome", "chintai", "jkosha", "juko", "sumaity", "eheya", "able", "yahoo", "other"]
    files = [os.path.join(OUT, n + ".json") for n in SOURCE_FILES if os.path.exists(os.path.join(OUT, n + ".json"))]
    rows = []
    for f in files:
        try:
            data = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            print(f"!! cannot read {f}: {e}", file=sys.stderr)
            continue
        if isinstance(data, dict):
            data = data.get("listings") or data.get("items") or []
        for r in data:
            r = dict(r)
            r.setdefault("source", os.path.basename(f).replace(".json", ""))
            rows.append(r)
    print(f"loaded {len(rows)} raw rows from {len(files)} files")

    lots = load_parking()
    print(f"parking lots available for matching: {len(lots)}")

    kept, dropped = [], []
    for r in rows:
        why = []
        rent = to_int(r.get("rent"))
        area = to_float(r.get("area_m2"))
        layout = norm_layout(r.get("layout"))
        floor = to_int(r.get("floor"))
        bfl = to_int(r.get("building_floors"))
        elev = r.get("elevator")
        built = to_int(r.get("built_year"))
        struct = norm_structure(r.get("structure"))
        reikin_m = months_of_rent(r.get("reikin"), rent)
        shikikin_m = months_of_rent(r.get("shikikin"), rent)
        lat, lon = r.get("lat"), r.get("lon")
        if (lat is None or lon is None) and r.get("address"):
            lat, lon = geocode(r["address"])
        d = dist_km(lat, lon) if lat is not None else to_float(r.get("distance_km"))

        is_ur = r.get("source") == "ur"
        is_house = (r.get("tier") == "house") or bool(re.search(r"(一戸建|戸建|テラス|タウンハウス)", str(r.get("building_type", "")) + str(r.get("notes", ""))))

        if rent is None or rent > MAX_RENT:
            why.append(f"rent {rent}")
        if area is None or area < MIN_AREA:
            why.append(f"area {area}")
        if layout is None or not OK_LAYOUT.match(layout):
            why.append(f"layout {layout}")
        if reikin_m is not None and reikin_m > float(os.environ.get("REIKIN_MAX", "1.0")):
            why.append(f"reikin {reikin_m} months")
        if not is_house and not is_ur:
            if floor is None:
                why.append("floor unknown")
            elif floor <= 1:
                why.append("1F")
            elif floor >= 4 and elev is not True:
                why.append(f"{floor}F without confirmed elevator")
        if built is None:
            why.append("built year unknown")
        elif built < 1991:
            why.append(f"built {built} (<1991)")
        elif built < 2001 and struct not in ("RC", "SRC"):
            why.append(f"built {built} but structure {struct}")
        if d is None:
            why.append("no distance")
        elif d > MAX_DIST:
            why.append(f"distance {d} km")
        name_blob = f'{r.get("building_name") or ""} {r.get("notes") or ""}'
        if re.search(r"(市営住宅|府営住宅|公営住宅|県営住宅|特定優良賃貸|特優賃)", name_blob):
            why.append("public housing (income-restricted / lottery)")
        coarse = bool(re.search(r"区$", norm_address(r.get("address") or "")))   # nothing after the ward name

        tier = "house" if is_house else ("A" if (built or 0) >= 2001 else "B")
        pstat, pfee = parking_status(r.get("parking"))
        if pfee is None and r.get("parking_fee") is not None:
            pfee = to_int(r.get("parking_fee"))
        grade, grade_note = insulation_grade(built, struct)
        rec = {
            "sources": [{"source": r.get("source"), "url": r.get("url")}],
            "building_name": r.get("building_name"),
            "address": r.get("address"),
            "lat": lat, "lon": lon,
            "distance_km": round(d, 2) if d is not None else None,
            "bike_min": bike_minutes(d),
            "rent": rent, "kanrihi": to_int(r.get("kanrihi")) or 0,
            "shikikin": r.get("shikikin"), "shikikin_months": shikikin_m,
            "reikin": r.get("reikin"), "reikin_months": reikin_m,
            "other_initial": r.get("other_initial"),
            "layout": layout, "area_m2": area,
            "floor": floor, "building_floors": bfl, "elevator": elev,
            "built_year": built, "built_month": to_int(r.get("built_month")),
            "age_years": (2026 - built) if built else None,
            "structure": struct,
            "parking": r.get("parking"), "parking_status": pstat, "parking_fee": pfee,
            "nearest_station": r.get("nearest_station"),
            "tier": tier, "is_ur": is_ur, "is_house": is_house,
            "insulation_grade": grade, "insulation_note": grade_note,
            "notes": r.get("notes"),
            "coarse_address": coarse,
            "fetched_at": r.get("fetched_at"),
        }
        if why:
            rec["dropped_because"] = why
            dropped.append(rec)
        else:
            kept.append(rec)

    # ---- dedupe: same address + area + floor (+ layout) across sites
    merged = {}
    name_index = {}

    def town(a):
        return re.sub(r"\d.*$", "", norm_address(a))

    def nname(n):
        n = zen2han(n or "")
        n = re.sub(r"[（(].*?[）)]", "", n)                 # (旧○○) etc.
        n = re.sub(r"\s*\d{2,4}\s*号室?$", "", n)          # trailing room number
        n = re.sub(r"[\s・･\-－ー]", "", n)
        if re.search(r"(駅|徒歩|階建|築\d)", n):              # generic auto-generated names
            return ""
        return n if len(n) >= 3 else ""

    for rec in kept:
        key = (town(rec["address"]), round(rec["area_m2"] or 0, 0), rec["floor"], rec["layout"], rec["rent"])
        nkey = (nname(rec["building_name"]), round(rec["area_m2"] or 0, 0), rec["floor"], rec["rent"]) if nname(rec["building_name"]) else None
        if key not in merged and nkey and nkey in name_index:
            key = name_index[nkey]
        if key in merged:
            m = merged[key]
            m["sources"].extend(s for s in rec["sources"] if s["url"] not in {x["url"] for x in m["sources"]})
            # prefer the more precise address (and its coordinates) when one source only gives the ward
            if len(norm_address(rec["address"])) > len(norm_address(m["address"])):
                for k in ("address", "lat", "lon", "distance_km", "bike_min", "coarse_address"):
                    m[k] = rec[k]
            # fill real gaps from the other source (None/"" only — never overwrite 0 or False)
            for k, v in rec.items():
                if k in ("sources", "address", "lat", "lon", "distance_km", "bike_min", "coarse_address"):
                    continue
                if (m.get(k) is None or m.get(k) == "") and v not in (None, ""):
                    m[k] = v
            if rec["rent"] and m["rent"] and rec["rent"] < m["rent"]:
                m["rent"] = rec["rent"]
            if rec.get("elevator") is True:
                m["elevator"] = True
            # a generic auto-generated name loses to a real one
            if re.search(r"(駅|徒歩|階建|築\d)", str(m.get("building_name") or "")) and rec.get("building_name") and not re.search(r"(駅|徒歩|階建|築\d)", rec["building_name"]):
                m["building_name"] = rec["building_name"]
            m["building_name"] = re.sub(r"^\[あと\d+日\]", "", str(m.get("building_name") or "")).strip() or m.get("building_name")
        else:
            rec["building_name"] = re.sub(r"^\[あと\d+日\]", "", str(rec.get("building_name") or "")).strip() or rec.get("building_name")
            merged[key] = rec
            if nkey:
                name_index[nkey] = key
    units = list(merged.values())

    # ---- second pass: near-duplicates (same building, same floor/layout/rent/year, area within 1 m²,
    #      or generic auto-named rows that match a named row on ward+area+rent+year+layout)
    def ward(a):
        m = re.search(r"(北|上京|左京|中京|東山|下京|南|右京|伏見|山科|西京)区", a or "")
        return m.group(0) if m else ""

    def absorb(m, rec):
        m["sources"].extend(s for s in rec["sources"] if s["url"] not in {x["url"] for x in m["sources"]})
        if len(norm_address(rec["address"])) > len(norm_address(m["address"])):
            for k in ("address", "lat", "lon", "distance_km", "bike_min", "coarse_address"):
                m[k] = rec[k]
        for k, v in rec.items():
            if k in ("sources", "address", "lat", "lon", "distance_km", "bike_min", "coarse_address"):
                continue
            if (m.get(k) is None or m.get(k) == "") and v not in (None, ""):
                m[k] = v
        if rec.get("elevator") is True:
            m["elevator"] = True
        if re.search(r"(駅|徒歩|階建|築\d)", str(m.get("building_name") or "")) and rec.get("building_name") and not re.search(r"(駅|徒歩|階建|築\d)", rec["building_name"]):
            m["building_name"] = rec["building_name"]

    changed = True
    while changed:
        changed = False
        out = []
        for rec in units:
            hit = None
            for m in out:
                same_core = (m["floor"] == rec["floor"] and m["layout"] == rec["layout"] and m["rent"] == rec["rent"]
                             and m["built_year"] == rec["built_year"] and ward(m["address"]) == ward(rec["address"]))
                if not same_core:
                    continue
                n1, n2 = nname(m["building_name"]), nname(rec["building_name"])
                close_area = abs((m["area_m2"] or 0) - (rec["area_m2"] or 0)) <= 1.0
                if (n1 and n1 == n2 and close_area) or ((not n1 or not n2) and (m["area_m2"] == rec["area_m2"])):
                    hit = m
                    break
            if hit:
                absorb(hit, rec)
                changed = True
            else:
                out.append(rec)
        units = out

    # ---- optional: keep only units that are NOT already in another merged file (e.g. the main report)
    excl = os.environ.get("EXCLUDE_MERGED")
    if excl and os.path.exists(excl):
        seen = {s["url"] for x in json.load(open(excl, encoding="utf-8")) for s in x["sources"]}
        before = len(units)
        units = [u for u in units if not any(s["url"] in seen for s in u["sources"]) and (u["reikin_months"] or 0) > 1.0]
        print(f"excluded {before - len(units)} units already in {excl} (or 礼金 ≤ 1 month)")

    # ---- parking match + score
    for u in units:
        u["nearby_parking"] = [] if u["parking_status"] == "onsite" else nearest_lots(u["lat"], u["lon"], lots)
        total = u["rent"] + (u["kanrihi"] or 0)
        pk = u["parking_fee"] if u["parking_status"] == "onsite" and u["parking_fee"] else (
            u["nearby_parking"][0]["monthly_fee"] if u["nearby_parking"] and u["nearby_parking"][0].get("monthly_fee") else None)
        u["monthly_total"] = total
        u["monthly_total_with_parking"] = total + pk if pk else None
        s = 0.0
        s += max(0, 25 - (u["distance_km"] or 5.5) * 5)           # 0–25: distance
        s += max(0, (100_000 - total) / 2000)                     # 0–~15: cheaper total
        s += min(15, max(0, ((u["area_m2"] or 45) - 45) * 0.75))  # 0–15: bigger
        s += {"A": 20, "B+": 16, "B": 12, "B-": 8, "C": 4}.get(u["insulation_grade"], 0)
        s += 10 if u["parking_status"] == "onsite" else (5 if u["nearby_parking"] else 0)
        s += 5 if u["elevator"] is True else 0
        s += 5 if (u["reikin_months"] or 0) == 0 else 0
        s += 3 if u["structure"] in ("RC", "SRC") else 0
        s -= 8 if u.get("coarse_address") else 0                   # distance only known to ward level
        u["score"] = round(s, 1)
    units.sort(key=lambda u: (-u["score"], u["distance_km"] or 99))
    apts = [u for u in units if not u["is_house"]]
    houses = [u for u in units if u["is_house"]]
    for i, u in enumerate(apts, 1):
        u["rank"] = i
    for i, u in enumerate(houses, 1):
        u["rank"] = f"H{i}"
    units = apts + houses

    json.dump(units, open(os.path.join(OUT, "merged.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(dropped, open(os.path.join(OUT, "merged_dropped.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"kept {len(kept)} rows -> {len(units)} unique units; dropped {len(dropped)}")
    from collections import Counter
    print("by tier:", Counter(u["tier"] for u in units))
    print("by source:", Counter(s["source"] for u in units for s in u["sources"]))
    print("drop reasons:", Counter(w.split(" ")[0] for d in dropped for w in d["dropped_because"]).most_common(12))


if __name__ == "__main__":
    main()
