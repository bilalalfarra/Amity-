import re,time,os,requests,math
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
s=requests.Session(); s.headers.update({"User-Agent":UA,"Accept-Language":"ja,en;q=0.8"})
counts={"26106":291,"26104":218,"26107":642,"26108":495,"26102":325,"26111":320,"26105":27,"26101":178,"26109":526}
log=open("out/raw/eheya/fetch.log","a")
for w,cnt in counts.items():
    maxp=math.ceil(cnt/50)+1
    for p in range(1,maxp+1):
        fn=f"out/raw/eheya/list_{w}_p{p}.html"
        url=f"https://www.eheya.net/kyoto/area/{w}/search/"+(f"?page={p}" if p>1 else "")
        if os.path.exists(fn) and os.path.getsize(fn)>20000: continue
        try:
            r=s.get(url,timeout=40)
            if r.status_code>=500: time.sleep(3); r=s.get(url,timeout=40)
            n=len(set(re.findall(r'/detail/(\d+)/',r.text)))
            open(fn,"w",encoding="utf-8").write(r.text)
            log.write(f"{url} {r.status_code} details={n}\n"); log.flush()
            if r.status_code!=200 or n==0: break
        except Exception as e:
            log.write(f"{url} ERR {e}\n"); log.flush()
        time.sleep(1.2)
log.write("DONE\n"); log.close()
