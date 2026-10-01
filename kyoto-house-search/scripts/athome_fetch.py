#!/usr/bin/env python3
"""athome rent_parking: fetch ward list pages (SSR Angular state), geocode, filter <=5.5 km, verify detail URLs."""
import warnings; warnings.filterwarnings("ignore")
import re, json, os, time, math, requests
from bs4 import BeautifulSoup
from geo import geocode, dist_km
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
WARDS = {"kyoto_shimogyo-city":"下京区","kyoto_nakagyo-city":"中京区","kyoto_minami-city":"南区","kyoto_ukyo-city":"右京区",
         "kyoto_kamigyo-city":"上京区","kyoto_nishikyo-city":"西京区","kyoto_higashiyama-city":"東山区","kyoto_kita-city":"北区","kyoto_fushimi-city":"伏見区"}
s = requests.Session(); s.headers["User-Agent"] = UA
def state(html):
    sc = BeautifulSoup(html, "lxml").find("script", id="serverApp-state")
    raw = sc.string.replace("&q;", '"').replace("&a;", "&").replace("&l;", "<").replace("&g;", ">").replace("&s;", "'")
    return json.loads(raw)
def get(url, fn):
    if os.path.exists(fn) and os.path.getsize(fn) > 5000 and "serverApp-state" in open(fn, encoding="utf-8").read():
        return open(fn, encoding="utf-8").read()
    for attempt in range(4):
        r = s.get(url, timeout=40)
        if r.status_code == 200 and "serverApp-state" in r.text:
            break
        print("retry", attempt, r.status_code, len(r.text), url, flush=True)
        time.sleep(8 + 8 * attempt)
    time.sleep(1.5)
    if r.status_code != 200 or "serverApp-state" not in r.text:
        print("HTTP", r.status_code, "no-state", url, flush=True); return None
    open(fn, "w", encoding="utf-8").write(r.text); return r.text
rows = {}
for slug, ward in WARDS.items():
    base = f"https://www.athome.co.jp/rent_parking/kyoto/{slug}/list/"
    html = get(base, f"out/raw/parking/athome_{slug}_p1.html")
    if not html: continue
    st = state(html); bd = st["first-view-ITEMS"]["bukkenData"]
    total = bd.get("bukkenCount"); items = list(bd.get("bukkenList", []))
    pages = math.ceil((total or 0) / 30)
    for p in range(2, pages + 1):
        h = get(f"{base}page{p}/", f"out/raw/parking/athome_{slug}_p{p}.html")
        if h: items += state(h)["first-view-ITEMS"]["bukkenData"].get("bukkenList", [])
    n_in = 0
    for b in items:
        loc = b.get("location") or ""
        lat, lon = geocode(loc)
        d = dist_km(lat, lon)
        rec = {"ward": ward, "id": b.get("id"), "title": b.get("title"), "tatemonoNm": b.get("tatemonoNm"), "location": loc,
               "lat": lat, "lon": lon, "distance_km": d, "contract": b.get("contract"), "type": b.get("type"),
               "traffic": [(t.get("lineName"), t.get("stationName"), t.get("tohoJikan")) for t in (b.get("traffic") or [])][:2],
               "kaiin": (b.get("kaiin") or {}).get("syogo"), "bukkenAccess": b.get("bukkenAccess"), "bukkenInfo": b.get("bukkenInfo"),
               "comment": ((b.get("recommendComment") or {}).get("comment")),
               "url": f"https://www.athome.co.jp/rent_parking/{b.get('id')}/"}
        if d is not None and d <= 5.5: n_in += 1
        rows.setdefault(rec["id"], rec)
    print(f"{ward}: bukkenCount={total} pages={pages} fetched={len(items)} within5.5={n_in}", flush=True)
allr = list(rows.values())
json.dump(allr, open("out/athome_list.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("sample contract:", json.dumps(allr[0]["contract"], ensure_ascii=False)[:600], flush=True)
print("sample type:", json.dumps(allr[0]["type"], ensure_ascii=False)[:300], flush=True)
cand = [r for r in allr if r["distance_km"] is not None and r["distance_km"] <= 5.5]
print("DISTINCT", len(allr), "CANDIDATES", len(cand), flush=True)
if os.environ.get("NO_VERIFY"): raise SystemExit(0)
STATUS = "out/athome_detail_status.json"
status = json.load(open(STATUS)) if os.path.exists(STATUS) else {}
os.makedirs("out/raw/parking/athome_detail", exist_ok=True)
for i, r in enumerate(cand, 1):
    u = r["url"]
    if status.get(u) == 200: continue
    code = None
    for attempt in range(2):
        try:
            resp = s.get(u, timeout=40); code = resp.status_code
            if code == 200 and "認証中" in resp.text[:3000]:
                code = "challenge"; time.sleep(10); continue
            if code < 500: break
        except requests.RequestException as e:
            code = f"ERR {type(e).__name__}"
        time.sleep(3)
    if code == 200 and i <= 3:
        open(f"out/raw/parking/athome_detail/{r['id']}.html", "w", encoding="utf-8").write(resp.text)
    status[u] = code
    if i % 20 == 0: json.dump(status, open(STATUS, "w"), indent=0); print(f"verify {i}/{len(cand)} last={code}", flush=True)
    time.sleep(1.2)
json.dump(status, open(STATUS, "w"), indent=0)
from collections import Counter
print("VERIFY DONE", Counter(map(str, status.values())), flush=True)
