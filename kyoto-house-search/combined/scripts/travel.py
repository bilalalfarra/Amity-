#!/usr/bin/env python3
"""Travel times from a home to the places that matter, via OSRM table service
(FOSSGIS routing.openstreetmap.de, bike + car profiles). One request per profile per home, cached."""
import json, os, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "out", "travelcache.json")
UA = "amity-house-search/1.0 (personal flat search)"

WORK = ("work", "الشغل 京都技術科学センター", 35.023968, 135.773178)
BIKE_DEST = [WORK,
             ("friend", "UR 松ノ木町 (رفيقك)", 34.975815, 135.764618),
             ("jr", "محطة JR 京都", 34.987183, 135.758743),
             ("doshisha_imadegawa", "دوشيشا 今出川", 35.029343, 135.760376)]
CAR_DEST = [("ramp_kamogawanishi", "鴨川西出入口", 34.972893, 135.763168),
            ("ramp_kamogawahigashi", "鴨川東出入口", 34.974926, 135.767303),
            ("ramp_kamitoba", "上鳥羽出入口", 34.965160, 135.755417),
            ("doshisha_kyotanabe", "دوشيشا 京田辺", 34.801334, 135.770508)]
RAMPS = {"ramp_kamogawanishi", "ramp_kamogawahigashi", "ramp_kamitoba"}


def _load():
    try:
        return json.load(open(CACHE, encoding="utf-8"))
    except Exception:
        return {}


_cache = _load()


def _table(profile, lat, lon, dests):
    coords = ";".join([f"{lon},{lat}"] + [f"{d[3]},{d[2]}" for d in dests])
    url = f"https://routing.openstreetmap.de/routed-{profile}/table/v1/driving/{coords}?sources=0&annotations=duration,distance"
    for attempt in range(3):
        try:
            time.sleep(1.0)
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40) as r:
                d = json.loads(r.read().decode("utf-8"))
            if d.get("code") == "Ok":
                return d["durations"][0][1:], d["distances"][0][1:]
        except Exception:
            time.sleep(3 * (attempt + 1))
    return None, None


def travel(lat, lon):
    """-> dict key -> {"min": int, "km": float}; plus 'ramp' = nearest ramp entry with its name."""
    if lat is None or lon is None:
        return {}
    key = f"{lat:.5f},{lon:.5f}"
    if key in _cache:
        return _cache[key]
    res = {}
    for profile, dests in (("bike", BIKE_DEST), ("car", CAR_DEST)):
        dur, dist = _table(profile, lat, lon, dests)
        if dur is None:
            continue
        for d, t, m in zip(dests, dur, dist):
            if t is not None:
                res[d[0]] = {"min": round(t / 60), "km": round(m / 1000, 1), "label": d[1]}
    ramps = [dict(v, key=k) for k, v in res.items() if k in RAMPS]
    if ramps:
        res["ramp"] = min(ramps, key=lambda v: v["min"])
    _cache[key] = res
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(_cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
    return res


if __name__ == "__main__":
    import sys
    print(json.dumps(travel(float(sys.argv[1]), float(sys.argv[2])), ensure_ascii=False, indent=1))
