#!/usr/bin/env python3
"""Geocode a Japanese address with the GSI (国土地理院) address search API and
return the distance to the workplace reference point (KRP / 京都技術科学センター).

Usage:  python3 geo.py "京都府京都市南区西九条池ノ内町"
Prints: <lat> <lon> <distance_km>   (or "null null null" if not found)
"""
import json, math, os, re, sys, time, urllib.parse, urllib.request

CENTER = (34.9951, 135.7405)  # 京都技術科学センター (KRP東地区, 下京区中堂寺南町134)
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(HERE, "out", "geocache.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"


def _load():
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save(c):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    tmp = CACHE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False)
    os.replace(tmp, CACHE_FILE)


def normalize(addr: str) -> str:
    a = addr.strip()
    a = re.sub(r"\s+", "", a)
    a = a.replace("－", "-").replace("ー", "-") if re.search(r"\d", a) else a
    # strip building names / room numbers after the block number
    a = re.sub(r"(\d+(?:-\d+){0,2}(?:番地?|号)?).*$", r"\1", a) if re.search(r"\d", a) else a
    if not a.startswith("京都府"):
        a = "京都府" + a if a.startswith("京都市") else a
    return a


def geocode(addr: str, _tries=(0, 1, 2)):
    """Return (lat, lon) or (None, None). Falls back to progressively shorter addresses."""
    cache = _load()
    key = normalize(addr)
    if key in cache:
        v = cache[key]
        return (v[0], v[1]) if v else (None, None)
    candidates = [key]
    # fallbacks: drop block numbers, then last token
    c2 = re.sub(r"\d.*$", "", key)
    if c2 and c2 != key:
        candidates.append(c2)
    for cand in candidates:
        url = "https://msearch.gsi.go.jp/address-search/AddressSearch?q=" + urllib.parse.quote(cand)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            time.sleep(0.3)
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.loads(r.read().decode("utf-8"))
        except Exception:
            data = []
        if data:
            lon, lat = data[0]["geometry"]["coordinates"]
            cache[key] = [lat, lon]
            _save(cache)
            return lat, lon
    cache[key] = None
    _save(cache)
    return None, None


def dist_km(lat, lon, center=CENTER):
    if lat is None or lon is None:
        return None
    R = 6371.0
    p1, p2 = math.radians(lat), math.radians(center[0])
    dphi = math.radians(center[0] - lat)
    dl = math.radians(center[1] - lon)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * R * math.asin(math.sqrt(a)), 2)


def bike_minutes(d_km):
    """Rough door-to-door estimate: road distance ≈ 1.25 × straight line, 13 km/h incl. signals."""
    if d_km is None:
        return None
    return round(d_km * 1.25 / 13 * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    lat, lon = geocode(" ".join(sys.argv[1:]))
    d = dist_km(lat, lon)
    print(lat if lat is not None else "null", lon if lon is not None else "null", d if d is not None else "null")
