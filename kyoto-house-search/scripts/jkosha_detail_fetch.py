import re,time,requests,warnings,json
warnings.filterwarnings("ignore")
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
s=requests.Session(); s.headers["User-Agent"]=UA
ids={"bc_100529117996":"クレードル桂川301","bc_100511981251":"サンハイム井上301","bc_100512168413":"サンハイム井上501","bc_100503844152":"コープ・ミール花園402","bc_100382620853":"リジョイス桂205","bc_100509823581":"セントラルヴィレッジ302","bc_100178203769":"イースタン平野路304","bc_100506095531":"ソフィスタ洛北203"}
log=open("out/raw/jkosha/detail_fetch.log","a")
for i,nm in ids.items():
    url=f"https://suumo.jp/chintai/{i}/"
    r=s.get(url,timeout=40)
    if r.status_code>=500:
        time.sleep(2); r=s.get(url,timeout=40)
    open(f"out/raw/jkosha/suumo_{i}.html","w",encoding="utf-8").write(r.text)
    log.write(f"{url} {r.status_code} {len(r.text)} {nm}\n"); log.flush()
    time.sleep(1.3)
log.write("DONE\n"); log.close()
