#!/usr/bin/env python3
"""Fetch every distinct at-parking.jp detail page for candidates (<=5.5 km); save raw HTML + status codes."""
import json, os, time, requests
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
cand = json.load(open("out/atparking_candidates.json", encoding="utf-8"))
urls = sorted({r["url"] for r in cand})
RAW = "out/raw/parking/atp_detail"; os.makedirs(RAW, exist_ok=True)
STATUS = "out/atp_detail_status.json"
status = json.load(open(STATUS)) if os.path.exists(STATUS) else {}
s = requests.Session(); s.headers["User-Agent"] = UA
for i, u in enumerate(urls, 1):
    pno = u.rsplit("/", 1)[-1].replace(".html", "")
    fn = f"{RAW}/{pno}.html"
    if status.get(u) == 200 and os.path.exists(fn):
        continue
    code = None
    for attempt in range(2):
        try:
            r = s.get(u, timeout=30); code = r.status_code
            if code < 500:
                break
        except requests.RequestException as e:
            code = f"ERR {type(e).__name__}"
        time.sleep(3)
    if code == 200:
        r.encoding = "utf-8"
        open(fn, "w", encoding="utf-8").write(r.text)
    status[u] = code
    if i % 10 == 0 or i == len(urls):
        json.dump(status, open(STATUS, "w"), indent=0)
        print(f"{i}/{len(urls)} last={code}", flush=True)
    time.sleep(1.1)
json.dump(status, open(STATUS, "w"), indent=0)
from collections import Counter
print("DONE", Counter(map(str, status.values())))
