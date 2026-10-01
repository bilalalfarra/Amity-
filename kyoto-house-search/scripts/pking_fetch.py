#!/usr/bin/env python3
"""p-king.jp (日本駐車場検索): station-centred searches (~1.4 km radius each) covering the 5.5 km circle; hidden jsonProperties; verify detail URLs."""
import re, json, os, time, html as H, collections, requests
from geo import dist_km
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
s = requests.Session(); s.headers["User-Agent"] = UA
RAW = "out/raw/parking"; os.makedirs(f"{RAW}/pking", exist_ok=True)
def get(url, fn):
    if fn and os.path.exists(fn) and os.path.getsize(fn) > 3000: return open(fn, encoding="utf-8").read()
    for attempt in range(3):
        try:
            r = s.get(url, timeout=40); time.sleep(1.1)
            if r.status_code == 200:
                if fn: open(fn, "w", encoding="utf-8").write(r.text)
                return r.text
            if r.status_code == 404: return None
        except requests.RequestException as e:
            print("err", e, flush=True)
        time.sleep(4)
    return None
def props(h):
    m = re.search(r'<input id="jsonProperties" type="hidden" value="([^"]*)"', h)
    if not m: return []
    v = H.unescape(m.group(1))
    try: return json.loads(v)
    except Exception: return json.loads(re.sub(r",\s*([\]}])", r"\1", v))
WARDS = ["kyoto-shimogyo_city","kyoto-nakagyo_city","kyoto-minami_city","kyoto-ukyo_city","kyoto-kamigyo_city","kyoto-nishikyo_city","kyoto-higashiyama_city","kyoto-kita_city","kyoto-fushimi_city"]
stations = {}
for w in WARDS:
    h = get(f"https://p-king.jp/search/kyoto_pre/{w}", f"{RAW}/pking/ward_{w}.html")
    if not h: print("ward page missing", w, flush=True); continue
    for href, name in re.findall(r'href="(/search_station/kyoto_pre/\d+/\d+)"[^>]*>\s*([^<]{1,20}?)\s*<', h):
        stations.setdefault(href, name)
print("stations found:", len(stations), flush=True)
byname = {}
for href, name in stations.items(): byname.setdefault(name, href)
print("distinct station names:", len(byname), flush=True)
lots = {}; used = []
for name, href in byname.items():
    code = href.rsplit("/", 1)[-1]
    h = get("https://p-king.jp" + href, f"{RAW}/pking/station_{code}_p1.html")
    if not h: continue
    la = re.search(r"coordinateInfLat\s*=\s*([\d.]+)", h); lo = re.search(r"coordinateInfLng\s*=\s*([\d.]+)", h); pc = re.search(r"pageCount\s*=\s*(\d+)", h)
    if not (la and lo): continue
    sd = dist_km(float(la.group(1)), float(lo.group(1))); total = int(pc.group(1)) if pc else 0
    if sd > 5.0 or total == 0:
        print(f"skip {name} ({code}) dist={sd} total={total}", flush=True); continue
    items = props(h); seen = {x["propertyPublicId"] for x in items}
    p = 2
    while len(seen) < total and p <= 30:
        h2 = get(f"https://p-king.jp{href}?page={p}", f"{RAW}/pking/station_{code}_p{p}.html")
        if not h2: break
        new = [x for x in props(h2) if x["propertyPublicId"] not in seen]
        if not new: break
        items += new; seen |= {x["propertyPublicId"] for x in new}; p += 1
    for x in items: lots.setdefault(x["propertyPublicId"], x)
    used.append((name, code, sd, total, len(items)))
    print(f"{name} ({code}) dist={sd} total={total} got={len(items)} pages={p-1} cum={len(lots)}", flush=True)
allr = list(lots.values())
for x in allr:
    try:
        la, lo = map(float, x["lat_lan"].split(",")); x["lat"], x["lon"] = la, lo; x["distance_km"] = dist_km(la, lo)
    except Exception: x["lat"] = x["lon"] = x["distance_km"] = None
json.dump({"stations": used, "lots": allr}, open("out/pking_list.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
cand = [x for x in allr if x["distance_km"] is not None and x["distance_km"] <= 5.5]
print("DISTINCT", len(allr), "CANDIDATES", len(cand), collections.Counter(x["vacancyStatus"] for x in cand), flush=True)
STATUS = "out/pking_detail_status.json"
status = json.load(open(STATUS)) if os.path.exists(STATUS) else {}
os.makedirs(f"{RAW}/pking_detail", exist_ok=True)
for i, x in enumerate(sorted(cand, key=lambda x: x["distance_km"]), 1):
    u = f"https://p-king.jp/detail/{x['propertyPublicId']}"
    if status.get(u) == 200: continue
    code = None
    for attempt in range(2):
        try:
            r = s.get(u, timeout=40); code = r.status_code
            if code == 200 and i <= 3: open(f"{RAW}/pking_detail/{x['propertyPublicId']}.html", "w", encoding="utf-8").write(r.text)
            if code < 500: break
        except requests.RequestException as e:
            code = f"ERR {type(e).__name__}"
        time.sleep(3)
    status[u] = code
    if i % 25 == 0: json.dump(status, open(STATUS, "w"), indent=0); print(f"verify {i}/{len(cand)} last={code}", flush=True)
    time.sleep(1.1)
json.dump(status, open(STATUS, "w"), indent=0)
print("VERIFY DONE", collections.Counter(map(str, status.values())), flush=True)
