#!/usr/bin/env python3
"""Post-processing for out/suumo.json (run after suumo_scrape.py):
  1. re-geocode records whose GSI lookup failed, using a Kyoto 通り名-aware fallback
     (ward + 町名 / 丁目, then nearest-station approximation); drop > 5.5 km
  2. flag probable agency duplicates (same address, area, floor, layout, built year) in notes
  3. tidy house records (全フロア wording instead of メゾネット)
  4. rewrite out/suumo.json and refresh the 'Kept listings' table + add a post-processing section in out/suumo.md
"""
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from geo import geocode, dist_km  # noqa: E402

OUT = os.path.join(HERE, "out")
MAX_DIST_KM = 5.5

STATION_HINT = {}  # filled from nearest_station text when needed


def simplify(addr):
    """Kyoto 通り名 address -> [ward+町名 candidates]."""
    a = re.sub(r"\s+", "", addr or "")
    m = re.match(r"(京都府)?京都市(\S+?区)(.*)$", a)
    if not m:
        return []
    ward, rest = m.group(2), m.group(3)
    rest = re.sub(r"[\d０-９][\d０-９\-－番地号]*$", "", rest)
    cands = []
    parts = re.split(r"(?:上ル|下ル|上る|下る|東入ル|西入ル|東入る|西入る|東入|西入|上がる|下がる|上ガル|下ガル|東イル|西イル)", rest)
    tail = parts[-1] if parts else ""
    tail = re.sub(r"^(?:通り?|ル|る)", "", tail)
    if tail and tail != rest and len(tail) >= 2:
        cands.append(f"京都府京都市{ward}{tail}")
    m2 = re.search(r"([^\d通]{1,8}町)$", rest)
    if m2 and f"京都府京都市{ward}{m2.group(1)}" not in cands:
        cands.append(f"京都府京都市{ward}{m2.group(1)}")
    return cands


def station_fallback(nearest):
    """'ＪＲ山陰本線/丹波口駅 歩7分' -> geocode '京都府京都市 丹波口駅'."""
    if not nearest:
        return None, None, None
    m = re.search(r"/(\S+?)駅", nearest)
    if not m:
        return None, None, None
    name = m.group(1).translate(str.maketrans("ＪＲ", "JR"))
    for q in (f"京都府京都市{name}駅", f"{name}駅"):
        lat, lon = geocode(q)
        if lat is not None:
            return lat, lon, name + "駅"
    return None, None, None


def main():
    path = os.path.join(OUT, "suumo.json")
    recs = json.load(open(path, encoding="utf-8"))
    n0 = len(recs)
    regeo, dropped_dist, approx = 0, 0, 0
    kept = []
    for r in recs:
        if r.get("lat") is None:
            got = False
            for c in simplify(r["address"]):
                lat, lon = geocode(c)
                if lat is not None:
                    r["lat"], r["lon"] = lat, lon
                    r["distance_km"] = dist_km(lat, lon)
                    r["notes"] = r["notes"].replace("GEOCODE FAILED – distance unknown", f"geocoded at 町名 level via '{c}'")
                    got = True
                    regeo += 1
                    break
            if not got:
                lat, lon, st = station_fallback(r.get("nearest_station"))
                if lat is not None:
                    r["lat"], r["lon"] = lat, lon
                    r["distance_km"] = dist_km(lat, lon)
                    r["notes"] = r["notes"].replace("GEOCODE FAILED – distance unknown",
                                                    f"APPROX location = nearest station {st} ({r.get('nearest_station')}); address not geocodable")
                    approx += 1
            if r.get("distance_km") is not None and r["distance_km"] > MAX_DIST_KM:
                dropped_dist += 1
                continue
        if r.get("tier") == "house":
            r["notes"] = re.sub(r"^メゾネット (\d+-\d+階); ", r"一戸建て 全フロア \1; ", r["notes"])
        kept.append(r)

    # duplicate flagging (conservative: flag, never drop)
    groups = defaultdict(list)
    for r in kept:
        key = (r["address"], r["area_m2"], r["floor"], r["layout"], r["built_year"])
        groups[key].append(r)
    dup_groups = 0
    for key, rs in groups.items():
        if len(rs) < 2:
            continue
        dup_groups += 1
        for r in rs:
            others = [o["url"] for o in rs if o is not r]
            r["notes"] += "; POSSIBLE DUPLICATE (same address/area/floor/layout/year — may be the same unit listed by another agency, or an identical neighbouring unit) of " + ", ".join(others)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(kept, f, ensure_ascii=False, indent=1)

    # refresh md
    mdp = os.path.join(OUT, "suumo.md")
    md = open(mdp, encoding="utf-8").read()
    head = md.split("\n## Kept listings")[0]
    lines = [head.rstrip("\n"), ""]
    lines.append("## Post-processing (suumo_post.py)")
    lines.append(f"- records after scrape+verification: {n0}; after post-processing: {len(kept)}")
    lines.append(f"- geocode fallback for Kyoto 通り名 addresses (ward+町名): {regeo} re-geocoded; station-based approximation: {approx}; dropped >5.5 km after re-geocoding: {dropped_dist}")
    still = sum(1 for r in kept if r.get("lat") is None)
    lines.append(f"- records still without coordinates (distance_km null): {still}")
    lines.append(f"- probable agency duplicates flagged in `notes` (not dropped): {dup_groups} groups covering {sum(len(v) for v in groups.values() if len(v) > 1)} records")
    from collections import Counter
    def ward(r):
        m = re.search(r"京都市(\S+?区)", r["address"])
        return m.group(1) if m else "?"
    lines.append(f"- final by tier: {dict(Counter(r['tier'] for r in kept))}; by ward: {dict(Counter(ward(r) for r in kept).most_common())}")
    lines.append(f"- final by parking: 敷地内/付 = {sum(1 for r in kept if r.get('parking') and re.search(r'敷地内|付', r['parking']))}, "
                 f"近隣 = {sum(1 for r in kept if r.get('parking') and '近隣' in r['parking'])}, "
                 f"無/空無/none = {sum(1 for r in kept if not r.get('parking') or re.search(r'^無|^なし|空無|^-$', r['parking']))}")
    lines.append("")
    lines.append("## Kept listings")
    lines.append("| tier | ward | building | layout | ㎡ | rent | 管理費 | 礼金 | floor | elev | built | struct | km | parking | url |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(kept, key=lambda x: (x["tier"], x["distance_km"] if x["distance_km"] is not None else 99)):
        lines.append(f"| {r['tier']} | {ward(r)} | {r['building_name']} | {r['layout']} | {r['area_m2']} | {r['rent']:,} | {r['kanrihi']} | {r['reikin']} | "
                     f"{r['floor']}/{r['building_floors']} | {r['elevator']} | {r['built_year']} | {r['structure']} | {r['distance_km']} | {r['parking']} | {r['url']} |")
    open(mdp, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"post: {n0} -> {len(kept)}; regeo={regeo} approx={approx} dropped_dist={dropped_dist} dup_groups={dup_groups} still_null={still}")


if __name__ == "__main__":
    main()
