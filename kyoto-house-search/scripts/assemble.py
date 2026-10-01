#!/usr/bin/env python3
"""Assemble all parking sources into out/parking.json + out/parking.md"""
import json, re, os, statistics, collections, datetime
from geo import dist_km
def load(fn, default=None):
    try: return json.load(open(fn, encoding="utf-8"))
    except Exception: return default if default is not None else []
def ward_of(addr, fallback=None):
    m = re.search(r"京都[府市](?:京都市)?(北|上京|左京|中京|東山|下京|南|右京|伏見|山科|西京)区", addr or "")
    if m: return m.group(1) + "区"
    m2 = re.search(r"(向日市|長岡京市|大山崎町|久御山町|宇治市)", addr or "")
    return m2.group(1) if m2 else fallback
def yen(t):
    m = re.search(r"(\d[\d,]*)\s*円", t or "")
    return int(m.group(1).replace(",", "")) if m else None
recs = []; dropped = collections.Counter(); unverified = collections.Counter()
# --- at-parking
for r in load("out/atparking_lots.json"):
    if r["http_status"] != 200: unverified["at-parking"] += 1; continue
    if r["distance_km"] is None or r["distance_km"] > 5.5: dropped["at-parking:dist"] += 1; continue
    ft = r["fee_text"]
    if ft and r.get("fee_max") and r["fee_max"] != r["monthly_fee"]: ft = f"{r['monthly_fee']:,}～{r['fee_max']:,}円（税込）"
    recs.append({"source": "at-parking", "url": r["url"], "name": r["name"], "address": r["address"], "lat": r["lat"], "lon": r["lon"], "distance_km": r["distance_km"],
                 "ward": ward_of(r["address"], r["ward"]), "monthly_fee": r["monthly_fee"], "fee_text": ft, "availability": r["availability"] or "不明（一覧に満空表示なし）", "notes": r["notes"]})
# --- times
for r in load("out/times_lots.json"):
    if r["http_status"] != 200: unverified["times"] += 1; continue
    recs.append({"source": "times", "url": r["url"], "name": r["name"], "address": r["address"], "lat": r["lat"], "lon": r["lon"], "distance_km": r["distance_km"],
                 "ward": ward_of(r["address"], r["ward"]), "monthly_fee": r["monthly_fee"], "fee_text": r["fee_text"], "availability": r["availability"], "notes": r["notes"]})
# --- park direct
pst = load("out/parkdirect_detail_status.json", {})
for x in load("out/parkdirect_list.json"):
    if x["distance_km"] is None or x["distance_km"] > 5.5: continue
    u = "https://www.park-direct.jp" + x["detailUrl"]
    if pst.get(u) != 200: unverified["park-direct"] += 1; continue
    groups = x["partitionGroups"]
    car = [g for g in groups if g.get("carKind") != "バイク"]
    if groups and not car: dropped["park-direct:bike"] += 1; continue
    fees = [g["monthlyFee"] for g in car if g.get("monthlyFee") and g.get("isPublishThePrice", True) and (g.get("rentWithTax") or 0) >= 1000]
    x["parkingFullAddress"] = re.sub(r"^(京都府京都市\S+?区)(京都府京都市\S+?区)", r"\2", x["parkingFullAddress"] or "")
    rents = [g["rentWithTax"] for g in car if g.get("rentWithTax")]
    fee = min(fees) if fees else None
    ft = None
    if fees:
        ft = (f"月額使用料 {min(fees):,}円" + (f"～{max(fees):,}円" if max(fees) != min(fees) else "") + "（税込・保証/管理料込）")
        if rents: ft += f"／うち賃料 {min(rents):,}円" + (f"～{max(rents):,}円" if max(rents) != min(rents) else "")
    av = collections.Counter(g.get("available") for g in car)
    avail = "契約可（空きあり）" if av.get("契約可") else ("空き待ち可（現在満車）" if av.get("空き待ち可") else "/".join(k for k in av if k))
    notes = []
    kinds = sorted({g.get("parkingType") for g in car if g.get("parkingType")}); cars = sorted({g.get("carKind") for g in car if g.get("carKind")})
    if kinds: notes.append("/".join(kinds))
    if any(g.get("roof") for g in car): notes.append("屋根あり")
    if cars: notes.append("対応: " + "/".join(cars))
    if any(g.get("hasFreeRent") for g in car): notes.append("フリーレントあり")
    notes.append(f"{len(car)}区画グループ; オンライン契約（Park Direct）")
    recs.append({"source": "park-direct", "url": u, "name": x["parkingName"], "address": x["parkingFullAddress"], "lat": x["latitude"], "lon": x["longitude"], "distance_km": x["distance_km"],
                 "ward": ward_of(x["parkingFullAddress"], x.get("ward")), "monthly_fee": fee, "fee_text": ft, "availability": avail, "notes": "; ".join(notes)})
# --- athome
ast = load("out/athome_detail_status.json", {})
for r in load("out/athome_list.json"):
    if r["distance_km"] is None or r["distance_km"] > 5.5: continue
    if ast.get(r["url"]) != 200: unverified["athome"] += 1; continue
    title = r["title"] or ""
    if "バイク" in title or "自転車" in title or "原付" in title: dropped["athome:bike"] += 1; continue
    if re.search(r"用地|土地|店舗|倉庫|資材置", title): dropped["athome:land/other"] += 1; continue
    c = r.get("contract") or {}
    pm = re.search(r"([\d.]+)万円", c.get("price") or "")
    fee = int(round(float(pm.group(1)) * 10000)) if pm else None
    notes = []
    for k, lab in (("managementFee", "管理費"), ("deposit", "敷金"), ("keyMoney", "礼金"), ("guaranteeDeposit", "保証金")):
        v = c.get(k)
        if v and v not in ("－", "-"): notes.append(f"{lab} {v}")
    acc = [re.sub(r"<BR\s*/?>", " ", a.get("name", "")).strip() for a in (r.get("bukkenAccess") or []) if a.get("name") and a.get("name") != "無"]
    if acc: notes.append("交通: " + " / ".join(acc[:2]))
    if r.get("kaiin"): notes.append("取扱: " + r["kaiin"])
    if r.get("comment"): notes.append(re.sub(r"\s+", " ", r["comment"])[:80])
    recs.append({"source": "athome", "url": r["url"], "name": title, "address": "京都府" + r["location"] if not r["location"].startswith("京都府") else r["location"], "lat": r["lat"], "lon": r["lon"], "distance_km": r["distance_km"],
                 "ward": ward_of(r["location"], r.get("ward")), "monthly_fee": fee, "fee_text": (c.get("price") if pm else None), "availability": "掲載中（空き状況は要問合せ）", "notes": "; ".join(notes)})
# --- monthly-p
mst = load("out/monthlyp_detail_status.json", {})
for x in load("out/monthlyp_list.json"):
    if x.get("distance_km") is None or x["distance_km"] > 5.5: continue
    u = "https://www.monthly-p.com" + x["detail_link"]
    if mst.get(u) != 200: unverified["monthly-p"] += 1; continue
    if x.get("is_parking_type_car") != "1" and x.get("is_parking_type_minicar") != "1": dropped["monthly-p:not-car"] += 1; continue
    fee = yen(x.get("display_price"))
    notes = []
    if x.get("parking_form_label"): notes.append(x["parking_form_label"])
    if x.get("parking_attribute_type_label"): notes.append(x["parking_attribute_type_label"])
    for k, lab in (("deposit", "敷金"), ("key_money", "礼金"), ("fee", "手数料"), ("renewal_fee", "更新料")):
        if x.get(k): notes.append(f"{lab} {x[k]}")
    if x.get("size_limit"): notes.append("制限 " + x["size_limit"][:60])
    if x.get("display_use_time"): notes.append(x["display_use_time"])
    if x.get("update_datetime"): notes.append("更新 " + x["update_datetime"][:10])
    nm = x.get("name") or ""
    if x.get("parking_space_type"): nm += f"（{x['parking_space_type']}）"
    recs.append({"source": "monthly-p", "url": u, "name": nm, "address": x.get("display_address"), "lat": float(x["lat"]), "lon": float(x["lng"]), "distance_km": x["distance_km"],
                 "ward": ward_of(x.get("display_address")), "monthly_fee": fee, "fee_text": x.get("display_price") or None, "availability": x.get("parking_available_kind_label"), "notes": "; ".join(notes)})
# --- p-king
kst = load("out/pking_detail_status.json", {})
VAC = {1: "空き有り", 2: "空き待ち予約可能", 3: "空き状況はお問合せ"}
pk = load("out/pking_list.json", {"lots": []}); pk_unverified = []
for x in pk.get("lots", []):
    if x.get("distance_km") is None or x["distance_km"] > 5.5: continue
    u = f"https://p-king.jp/detail/{x['propertyPublicId']}"
    if kst.get(u) != 200:
        unverified["p-king"] += 1
        pk_unverified.append({"source": "p-king", "url": u, "name": x["name"], "address": x["address"], "lat": x["lat"], "lon": x["lon"], "distance_km": round(x["distance_km"], 2),
                              "monthly_fee": yen(x.get("min_price") or ""), "fee_text": x.get("min_price") or None, "availability": VAC.get(x.get("vacancyStatus")), "url_verified": False})
        continue
    mp = x.get("min_price") or ""
    fee = yen(mp); ft = mp if fee else (mp or None)
    cb = x.get("canbin1") or []
    notes = []
    if len(cb) >= 10: notes.append(f"{cb[7]}/{cb[6]}; 全高{cb[1]} 全幅{cb[2]} 全長{cb[3]} 重量{cb[4]}" + ("; 大型可" if cb[8] == "可" else "") + ("; ハイルーフ可" if cb[9] == "可" else ""))
    if x.get("cabinCount"): notes.append(f"{x['cabinCount']}区画タイプ")
    notes.append("ID " + str(x["propertyPublicId"]))
    recs.append({"source": "p-king", "url": u, "name": x["name"], "address": x["address"], "lat": x["lat"], "lon": x["lon"], "distance_km": x["distance_km"],
                 "ward": ward_of(x["address"]), "monthly_fee": fee, "fee_text": ft, "availability": VAC.get(x.get("vacancyStatus"), str(x.get("vacancyStatus"))), "notes": "; ".join(notes)})
# ---- finalize
def oversize(r):
    txt = (r.get("name") or "") + " " + (r.get("notes") or "")
    if re.search(r"バス|トラック|大型重量|大型車専用|マイクロ", txt): return True
    m = re.search(r"全長[：:]?\s*[～~]?\s*(\d[\d,]*)\s*mm", txt)
    if m and int(m.group(1).replace(",", "")) >= 8000: return True
    return False
TODAY = datetime.date.today().isoformat()
_before = len(recs)
recs = [r for r in recs if not re.search(r"バイク|二輪|原付|自転車", r.get("name") or "")]
dropped["all:bike-by-name"] += _before - len(recs)
for r in recs:
    if r["monthly_fee"] is not None and r["monthly_fee"] < 2000:
        r["notes"] = (r["notes"] + "; " if r["notes"] else "") + f"表示価格 {r['monthly_fee']}円 は仮表示とみなし monthly_fee を null に"
        r["monthly_fee"] = None
for r in recs:
    r["distance_km"] = round(r["distance_km"], 2)
    r["oversize_vehicle"] = oversize(r)
    r["fetched_at"] = TODAY
    for k in ("lat", "lon"):
        if r[k] is not None: r[k] = round(float(r[k]), 6)
recs.sort(key=lambda r: (r["distance_km"], r["source"]))
# cross-source duplicate hint: same ~50 m cell and same fee
cell = collections.defaultdict(list)
for i, r in enumerate(recs):
    if r["lat"] is not None: cell[(round(r["lat"], 3), round(r["lon"], 3), r["monthly_fee"])].append(i)
dups = 0
for k, idx in cell.items():
    if len(idx) > 1 and len({recs[i]["source"] for i in idx}) > 1:
        for i in idx:
            recs[i]["notes"] = (recs[i]["notes"] + "; " if recs[i]["notes"] else "") + "※他サイトにも同一と思われる掲載あり"
        dups += len(idx) - 1
os.makedirs("out", exist_ok=True)
json.dump(recs, open("out/parking.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
pk_unverified.sort(key=lambda r: r["distance_km"])
json.dump(pk_unverified, open("out/parking_pking_unverified.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ---- summary
def fees(rs):
    return [r["monthly_fee"] for r in rs if r["monthly_fee"] and not r["oversize_vehicle"] and r["monthly_fee"] <= 150000]
def stats(vals):
    vals = [v for v in vals if v]
    if not vals: return "–"
    return f"中央値 {int(statistics.median(vals)):,}円 ／ {min(vals):,}–{max(vals):,}円 (n={len(vals)})"
by_ward = collections.defaultdict(list)
for r in recs: by_ward[r["ward"] or "不明"].append(r)
by_src = collections.Counter(r["source"] for r in recs)
lines = []
lines.append(f"# 月極駐車場データベース（KRP 半径5.5 km）\n\n生成: {datetime.datetime.now().astimezone().isoformat(timespec='minutes')}  基準点: 京都技術科学センター（下京区中堂寺南町134, 34.9951/135.7405）\n")
lines.append(f"**収録 {len(recs)} 件**（全URL HTTP 200 確認済、5.5 km以内、バイク専用は除外）。ファイル: `out/parking.json`\n")
lines.append("## ソース別件数\n\n| source | 件数 | 月額判明 | 備考 |\n|---|---|---|---|")
SRC_NOTE = {"at-parking": "アットパーキング。賃料は税込、幅がある場合は最安区画。満空は一覧ページ表示を転記（空き状況お問合せ／現在満車 空き待ち受付中／空きあり）",
            "times": "タイムズ月極（times-info.net）。募集中のみ掲載。使用料税込、契約手数料・保証金各1ヶ月、礼金0",
            "park-direct": "Park Direct（三井のリパーク月極も同システム）。monthly_fee は月額使用料（賃料＋保証/管理料、税込）。'契約可'=即契約可、'空き待ち可'=満車で空き待ち予約",
            "athome": "アットホーム賃貸駐車場。賃料のみ（万円表記を換算）。空き状況は掲載＝募集中だが詳細は要問合せ",
            "monthly-p": "月極駐車場どっとこむ（日本パーキングマーケット等）。要確認が大半。賃料のみ",
            "p-king": "日本駐車場検索。駅周辺検索（半径約1.4 km）を複数駅で集約。賃料は最安区画、約25%は要問合せ。住所は町名まで"}
for s_, n in by_src.most_common():
    lines.append(f"| {s_} | {n} | {sum(1 for r in recs if r['source']==s_ and r['monthly_fee'])} | {SRC_NOTE.get(s_,'')} |")
lines.append(f"\n（統計はバス・トラック等の大型専用 {sum(1 for r in recs if r['oversize_vehicle'])} 件と15万円超を除外。収録データには含む）")
lines.append("\n## 区別 件数と月額相場（monthly_fee が判明している物件、普通車）\n\n| 区 | 件数 | 月額（中央値／最小–最大） | 空きあり/契約可 | 満車・空き待ち | 要問合せ・要確認 |\n|---|---|---|---|---|---|")
ORDER = ["下京区", "中京区", "南区", "右京区", "上京区", "西京区", "東山区", "北区", "伏見区", "左京区", "山科区", "不明"]
def avail_class(a):
    a = a or ""
    if re.search(r"空きあり|契約可|空き有り|募集中|^空き$|空き予定", a) and "待ち" not in a: return "open"
    if re.search(r"満車|空き待ち", a): return "full"
    return "ask"
for w in ORDER:
    rs = by_ward.get(w)
    if not rs: continue
    ac = collections.Counter(avail_class(r["availability"]) for r in rs)
    lines.append(f"| {w} | {len(rs)} | {stats(fees(rs))} | {ac['open']} | {ac['full']} | {ac['ask']} |")
lines.append("\n### 区別・ソース別の月額中央値（参考）\n\n| 区 | " + " | ".join(by_src) + " |\n|---|" + "---|" * len(by_src))
for w in ORDER:
    rs = by_ward.get(w)
    if not rs: continue
    cells = []
    for s_ in by_src:
        v = fees([r for r in rs if r["source"] == s_])
        cells.append(f"{int(statistics.median(v)):,} (n={len(v)})" if v else "–")
    lines.append(f"| {w} | " + " | ".join(cells) + " |")
# distance bands
lines.append("\n## 基準点からの距離帯別\n\n| 距離 | 件数 | 月額中央値 |\n|---|---|---|")
for lo, hi in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5.5)):
    rs = [r for r in recs if lo <= r["distance_km"] < hi]
    lines.append(f"| {lo}–{hi} km | {len(rs)} | {stats(fees(rs)).split(' ／')[0] if rs else '–'} |")
lines.append("\n## 空き状況の内訳\n")
for k, v in collections.Counter(r["availability"] for r in recs).most_common(20):
    lines.append(f"- {k}: {v}")
lines.append("\n## 収集方法・検証\n")
lines.append("- アットパーキング: 区別の地図検索ページ（/searchp/）に全物件が座標付きで埋め込まれているため区ごとに取得→各物件詳細ページを取得（332/334が200、2件404は除外）。満空は区別テキスト検索結果＋詳細ページの周辺物件一覧から転記。")
lines.append("- タイムズ: 区別一覧（C101…C111）を取得、住所をGSIジオコーダで町名レベル測位、詳細URLを全件200確認。")
lines.append("- Park Direct: Next.js の __NEXT_DATA__ から区別・ページ別に取得（京都市873件→5.5 km内597件）。詳細URLはCloudFrontが生成中に202を返すため再試行して200確認。")
lines.append("- アットホーム: SSR状態(serverApp-state)から取得。2ページ目以降でボット認証ページが出るため Playwright(Chromium) で取得・検証。")
lines.append("- 月極駐車場どっとこむ: /area/ajaxSearch を矩形範囲（100件上限、超過時は4分割）で巡回。詳細URLを200確認。")
lines.append("- 日本駐車場検索(p-king): 区ページに載る駅（基準点から5 km以内）ごとに周辺検索（約1.4 km半径、hidden input jsonProperties）を全ページ取得し propertyPublicId で重複排除。詳細URLを距離順に200確認（未確認分は除外）。")
lines.append(f"\n## 除外・未検証\n\n- 距離>5.5 km／バイク専用／非自動車: {dict(dropped)}\n- URL未検証または非200で除外: {dict(unverified)}（p-king の未検証分 {len(pk_unverified)} 件は `out/parking_pking_unverified.json` に座標・賃料付きで保存。URL形式は同一なので後日検証可）\n- 他サイトとの重複と思われる掲載（同一50 m・同額）: 約{dups}件（notesに注記、両方とも収録）")
lines.append("\n## 問題点・注意\n")
lines.append("- 到達不可（プロキシでブロック 502）: pmc-tsukigime.jp, tsukigime-parking.com, parking-mkt, nihon-parking, mitsui-repark.jp(repark.jp 本体は到達可で Park Direct へ転送), e-parking, navipark, anabuki-parking。chumap.jp（駐マップ）はメンテナンス中(503)。carparking.jp は403のため未使用。")
lines.append("- アットホームの 伏見区 5ページ目（3件）は認証ページのため未取得（5.5 km外が大半）。")
lines.append("- 月額の意味がソースで異なる: Park Direct は保証/管理料込みの総額、他は賃料（税込）。契約時費用（敷金・礼金・手数料）は notes 参照。")
lines.append("- 住所が町名までのソース（タイムズ・アットホーム・p-king）は座標が町の代表点（p-king は物件座標あり）。距離は±300 m程度の誤差あり。")
open("out/parking.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("RECORDS", len(recs), dict(by_src)); print("dropped", dict(dropped)); print("unverified", dict(unverified)); print("dups", dups)
for w in ORDER:
    if by_ward.get(w): print(w, len(by_ward[w]), stats([r["monthly_fee"] for r in by_ward[w]]))
