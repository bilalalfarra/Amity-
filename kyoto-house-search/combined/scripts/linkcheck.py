import json, re, subprocess, sys
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
bad=[];n=0
for p in sys.argv[1:]:
    for x in json.load(open(p,encoding='utf-8')):
        for s in x['sources']:
            u=s['url']
            if 'homes.co.jp' in u: continue
            n+=1
            r=subprocess.run(["curl","-sS","-L","--max-time","25","-A",UA,"-w","\n%{http_code}",u],capture_output=True,text=True)
            body,code=r.stdout.rsplit("\n",1) if "\n" in r.stdout else ("",r.stdout)
            title=(re.search(r"<title>([^<]*)",body) or [None,""])[1]
            ids=re.findall(r"\d{9,}",u)
            ok = code=="200" and (not ids or ids[-1] in body) and not re.search(r"(見つかりません|エラー|Not Found|掲載終了しました)",title)
            if not ok: bad.append((p.split('/')[0],x['rank'],(x['building_name'] or '')[:12],code,title[:40],u))
print('checked',n,'bad',len(bad)); [print(b) for b in bad]
