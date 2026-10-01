#!/usr/bin/env python3
"""Real bicycle route time from a home to the office, via the OSRM bike profile
hosted by FOSSGIS (routing.openstreetmap.de). Cached; ~1 request/second."""
import json, os, time, urllib.request

from geo import CENTER

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "out", "routecache.json")
URL = "https://routing.openstreetmap.de/routed-bike/route/v1/driving/{lon},{lat};{clon},{clat}?overview=false"
UA = "amity-house-search/1.0 (personal flat search)"


def _load():
    try:
        return json.load(open(CACHE, encoding="utf-8"))
    except Exception:
        return {}


_cache = _load()


def bike_route(lat, lon):
    """-> (minutes, km) or (None, None). Minutes = OSRM bike duration (≈15 km/h on flat roads)."""
    if lat is None or lon is None:
        return None, None
    key = f"{lat:.5f},{lon:.5f}"
    if key in _cache:
        v = _cache[key]
        return (v[0], v[1]) if v else (None, None)
    url = URL.format(lat=lat, lon=lon, clat=CENTER[0], clon=CENTER[1])
    data = None
    for attempt in range(3):
        try:
            time.sleep(1.0)
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except Exception:
            time.sleep(3 * (attempt + 1))
    if not data or data.get("code") != "Ok" or not data.get("routes"):
        _cache[key] = None
    else:
        rt = data["routes"][0]
        _cache[key] = [round(rt["duration"] / 60), round(rt["distance"] / 1000, 2)]
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(_cache, open(CACHE, "w", encoding="utf-8"))
    v = _cache[key]
    return (v[0], v[1]) if v else (None, None)


if __name__ == "__main__":
    import sys
    print(bike_route(float(sys.argv[1]), float(sys.argv[2])))
