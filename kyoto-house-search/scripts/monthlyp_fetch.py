#!/usr/bin/env python3
"""monthly-p.com (月極駐車場どっとこむ): tiled bbox search via /area/ajaxSearch (<=100 results per box), then verify detail URLs."""
import json, os, time, math, urllib.parse, requests, collections
from geo import dist_km, CENTER
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
s = requests.Session()
s.headers.update({"User-Agent": UA, "X-Requested-With": "XMLHttpRequest", "Referer": "https://www.monthly-p.com/zone_map/" + urllib.parse.quote("京都府京都市下京区") + "/"})
LAT0, LON0 = CENTER; DLAT = 5.5 / 111.0; DLON = 5.5 / (111.0 * math.cos(math.radians(LAT0)))
BASE = {"prefecture": "京都府", "address": "京都市下京区", "zoom": "14", "condition[min_price]": "", "condition[max_price]": "", "condition[floor]": "指定なし",
        "condition[is_no_fees_campaign]": "0", "condition[is_no_key_money]": "0", "condition[is_no_deposit]": "0", "condition[can_short_use]": "0", "condition[is_ok_speed_contract]": "0"}
lots = {}; nreq = 0; log = []
def query(b, page):
    global nreq
    d = dict(BASE); d.update({"location[lat]": f"{(b[0]+b[1])/2:.6f}", "location[lng]": f"{(b[2]+b[3])/2:.6f}", "page_num": str(page),
                             "bounds[startLat]": f"{b[0]:.6f}", "bounds[endLat]": f"{b[1]:.6f}", "bounds[startLng]": f"{b[2]:.6f}", "bounds[endLng]": f"{b[3]:.6f}"})
    for attempt in range(3):
        try:
            r = s.post("https://www.monthly-p.com/area/ajaxSearch", data=d, timeout=60); nreq += 1
            time.sleep(1.1)
            if r.status_code == 200:
                j = r.json()
                if j.get("is_success"): return j["result"]["parking_data"]
        except Exception as e:
            print("err", e, flush=True)
        time.sleep(4)
    return None
def cell_outside(b):
    clat = min(max(LAT0, b[0]), b[1]); clon = min(max(LON0, b[2]), b[3])
    return dist_km(clat, clon) > 5.6
def harvest(b, depth=0):
    if cell_outside(b): return
    pd = query(b, 1)
    if pd is None: print("FAIL cell", b, flush=True); return
    total = int(pd["total_count"] or 0); items = pd["list"]
    if total > 100 and depth < 6:
        mlat = (b[0]+b[1])/2; mlon = (b[2]+b[3])/2
        for sb in ((b[0], mlat, b[2], mlon), (mlat, b[1], b[2], mlon), (b[0], mlat, mlon, b[3]), (mlat, b[1], mlon, b[3])):
            harvest(sb, depth+1)
        return
    for it in items: lots.setdefault(it["id"], it)
    for p in range(2, math.ceil(min(total, 100) / 25) + 1):
        pd2 = query(b, p)
        if pd2: 
            for it in pd2["list"]: lots.setdefault(it["id"], it)
    log.append((b, total, len(items)))
    print(f"cell depth={depth} total={total} lots_so_far={len(lots)} req={nreq}", flush=True)
n = 3
for i in range(n):
    for j in range(n):
        b = (LAT0 - DLAT + 2*DLAT*i/n, LAT0 - DLAT + 2*DLAT*(i+1)/n, LON0 - DLON + 2*DLON*j/n, LON0 - DLON + 2*DLON*(j+1)/n)
        harvest(b)
allr = list(lots.values())
for it in allr:
    try: it["distance_km"] = dist_km(float(it["lat"]), float(it["lng"]))
    except Exception: it["distance_km"] = None
json.dump(allr, open("out/monthlyp_list.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
cand = [it for it in allr if it["distance_km"] is not None and it["distance_km"] <= 5.5]
print("DISTINCT", len(allr), "CANDIDATES", len(cand), "car:", sum(it.get("is_parking_type_car") == "1" for it in cand), flush=True)
print(collections.Counter(it.get("parking_available_kind_label") for it in cand), flush=True)
STATUS = "out/monthlyp_detail_status.json"
status = json.load(open(STATUS)) if os.path.exists(STATUS) else {}
s.headers.pop("X-Requested-With", None)
os.makedirs("out/raw/parking/monthlyp_detail", exist_ok=True)
for i, it in enumerate(cand, 1):
    u = "https://www.monthly-p.com" + it["detail_link"]
    if status.get(u) == 200: continue
    code = None
    for attempt in range(2):
        try:
            r = s.get(u, timeout=60, stream=True); code = r.status_code
            if code == 200 and i <= 3:
                open(f"out/raw/parking/monthlyp_detail/{it['parking_num']}.html", "w", encoding="utf-8").write(r.text)
            r.close()
            if code < 500: break
        except requests.RequestException as e:
            code = f"ERR {type(e).__name__}"
        time.sleep(3)
    status[u] = code
    if i % 20 == 0: json.dump(status, open(STATUS, "w"), indent=0); print(f"verify {i}/{len(cand)} last={code}", flush=True)
    time.sleep(1.1)
json.dump(status, open(STATUS, "w"), indent=0)
print("VERIFY DONE", collections.Counter(map(str, status.values())), flush=True)
