import re,time,os,requests,warnings,json
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
s=requests.Session(); s.headers["User-Agent"]=UA
wards={"26106":"shimogyo","26104":"nakagyo","26107":"minami","26108":"ukyo","26102":"kamigyo","26111":"nishikyo","26105":"higashiyama","26101":"kita","26109":"fushimi"}
base="https://sumaity.com/chintai/area_list/list.php?search_type=a&pref_id=26&page_count=30&price_high=100000&foot_print_low=45&madori%5B%5D=2_50&madori%5B%5D=3_30&madori%5B%5D=3_50&madori%5B%5D=4_30&madori%5B%5D=4_50_ge"
log=open("out/raw/sumaity/fetch.log","a")
for w,nm in wards.items():
    page=1
    while True:
        url=f"{base}&acity_id%5B%5D={w}000000"+(f"&page={page}" if page>1 else "")
        r=s.get(url,timeout=40)
        if r.status_code>=500:
            time.sleep(2); r=s.get(url,timeout=40)
        fn=f"out/raw/sumaity/list_{nm}_p{page}.html"
        open(fn,"w",encoding="utf-8").write(r.text)
        soup=BeautifulSoup(r.text,"lxml")
        n=len(soup.select("div.building"))
        ac=soup.find("input",attrs={"name":"all_count"})
        tot=ac.get("value") if ac else None
        log.write(f"{url} {r.status_code} buildings={n} all_count={tot}\n"); log.flush()
        time.sleep(1.2)
        nxt=soup.find("a",href=re.compile(rf"page={page+1}(&|$)"))
        if not nxt or n==0 or page>=15: break
        page+=1
log.write("DONE\n"); log.close()
