import re,time,os,json,sys
import requests
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
ids=sorted(set(re.findall(r"80_\d{4}",open("out/raw/ur/list_index.html",encoding="utf-8",errors="ignore").read())))
os.makedirs("out/raw/ur",exist_ok=True)
s=requests.Session(); s.headers["User-Agent"]=UA
log=open("out/raw/ur/fetch.log","a")
for i in ids:
    for suffix in ["",'_report']:
        fn=f"out/raw/ur/{i}{suffix}.html"
        if os.path.exists(fn) and os.path.getsize(fn)>1000: continue
        url=f"https://www.ur-net.go.jp/chintai/kansai/kyoto/{i}{suffix}.html"
        try:
            r=s.get(url,timeout=30)
            code=r.status_code
            if code>=500:
                time.sleep(2); r=s.get(url,timeout=30); code=r.status_code
            if code==200:
                open(fn,"w",encoding="utf-8").write(r.text)
            log.write(f"{url} {code} {len(r.text)}\n"); log.flush()
        except Exception as e:
            log.write(f"{url} ERR {e}\n"); log.flush()
        time.sleep(1.1)
log.write("DONE\n"); log.close()
