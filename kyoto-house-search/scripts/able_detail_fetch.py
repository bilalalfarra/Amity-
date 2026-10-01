import re,time,os,json,requests,warnings
warnings.filterwarnings("ignore")
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
s=requests.Session(); s.headers["User-Agent"]=UA
cands=json.load(open("out/raw/able/candidates.json",encoding="utf-8"))
os.makedirs("out/raw/able/detail",exist_ok=True)
log=open("out/raw/able/detail_fetch.log","a")
for c in cands:
    fn=f"out/raw/able/detail/{c['bk']}.html"
    if os.path.exists(fn) and os.path.getsize(fn)>5000: continue
    try:
        r=s.get(c["url"],timeout=40)
        if r.status_code>=500: time.sleep(2); r=s.get(c["url"],timeout=40)
        open(fn,"w",encoding="utf-8").write(r.text)
        log.write(f"{c['url']} {r.status_code} {len(r.text)}\n"); log.flush()
    except Exception as e:
        log.write(f"{c['url']} ERR {e}\n"); log.flush()
    time.sleep(1.2)
log.write("DONE\n"); log.close()
