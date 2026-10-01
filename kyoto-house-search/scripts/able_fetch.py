import re,time,os,requests,warnings
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
s=requests.Session(); s.headers["User-Agent"]=UA
wards=["26106","26104","26107","26108","26102","26111","26105","26101","26109"]
q="cf=0&ct=0&m=5&m=6&m=7&m=8&m=9&m=A&m=B&sf=45&st=0&h=7&b=1&b=2&b=3&n=B"
log=open("out/raw/able/fetch.log","a")
for w in wards:
    page=1
    while True:
        url=f"https://www.able.co.jp/kyoto/area/{w}/list/?{q}&p={page}" if page>1 else f"https://www.able.co.jp/kyoto/area/{w}/list/?{q}"
        r=s.get(url,timeout=40)
        if r.status_code>=500:
            time.sleep(2); r=s.get(url,timeout=40)
        fn=f"out/raw/able/list_{w}_p{page}.html"
        open(fn,"w",encoding="utf-8").write(r.text)
        soup=BeautifulSoup(r.text,"lxml")
        n=len(soup.select("section.m-list_cassette"))
        # total count
        tot=None
        for el in soup.find_all(string=re.compile(r"該当.*?件|件中|全\s*\d+\s*件")):
            tot=el.strip()[:60]; break
        log.write(f"{url} {r.status_code} cassettes={n} tot={tot}\n"); log.flush()
        # next page?
        nxt=soup.find("a",href=re.compile(rf"/kyoto/area/{w}/list/\?.*p={page+1}(&|$)"))
        time.sleep(1.2)
        if not nxt or n==0 or page>=10: break
        page+=1
log.write("DONE\n"); log.close()
