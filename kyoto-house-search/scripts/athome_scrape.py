#!/usr/bin/env python3
"""at home (athome.co.jp) scraper for the Kyoto rental search.

The site is an Angular app, but every list / detail page is server-side rendered and embeds the
backend-for-frontend responses in <script id="serverApp-state"> (Angular TransferState), so plain
requests + JSON is enough (no API calls of our own; we only read the pages a browser would load).

List URL (per ward):  /chintai/kyoto/<ward>-city/list/[pageN/]?basic=<codes>&q=1&sort=33&limit=30
  basic codes (from the site's own condition dictionary):
    kc001 賃料下限なし, kc115 賃料上限10万円, kt007 専有面積45㎡以上, ki002 定期借家含む, ke001 駅徒歩指定なし,
    kj001 情報公開日指定なし, km010 2LDK, km014 3DK, km015 3LDK, km018 4K, km019 4DK, km021 4LDK以上,
    kn021 築25年以内 (tier A) / kn023 築35年以内 + kh001 鉄筋系 (tier-B candidates)
Detail URL: /chintai/<bukkenNo>/   (SSR state key ".../property-detail/first-view?...bukkenNo=...")
"""
import json, os, re, sys, time, datetime, traceback, html as H
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import geo as _geo  # noqa: E402  (shared helper, not modified)
from geo import dist_km  # noqa: E402
import urllib.parse  # noqa: E402

OUT = os.path.join(HERE, "out")
RAW = os.path.join(OUT, "raw", "athome")
os.makedirs(RAW, exist_ok=True)
LOG = open(os.path.join(OUT, "athome_log.txt"), "a", encoding="utf-8")
MYCACHE = os.path.join(OUT, "athome_geocache.json")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept-Language": "ja,en;q=0.8",
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})
BASE = "https://www.athome.co.jp"
MAX_KM = 5.5
JST = datetime.timezone(datetime.timedelta(hours=9))

WARDS = {"kyoto_shimogyo": "下京区", "kyoto_nakagyo": "中京区", "kyoto_minami": "南区", "kyoto_ukyo": "右京区",
         "kyoto_kamigyo": "上京区", "kyoto_nishikyo": "西京区", "kyoto_higashiyama": "東山区", "kyoto_kita": "北区",
         "kyoto_fushimi": "伏見区", "kyoto_sakyo": "左京区"}
COMMON = "kc001,kc115,ke001,kt007,ki002,kj001,km010,km014,km015,km018,km019,km021"
QUERIES = {"A": COMMON + ",kn021", "B": COMMON + ",kn023,kh001"}

_last = [0.0]


def log(*a):
    msg = " ".join(str(x) for x in a)
    print(msg, flush=True)
    LOG.write(msg + "\n"); LOG.flush()


def get(url, params=None, tries=2):
    for i in range(tries):
        wait = 1.0 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        try:
            r = S.get(url, params=params, timeout=60)
            _last[0] = time.time()
            if r.status_code >= 500 and i + 1 < tries:
                log("  5xx", r.status_code, url, "retrying"); time.sleep(3); continue
            return r
        except requests.RequestException as e:
            _last[0] = time.time()
            log("  request error", repr(e), url)
            if i + 1 < tries:
                time.sleep(3)
    return None


def state_of(html):
    m = re.search(r'<script id="serverApp-state" type="application/json">(.*?)</script>', html, re.S)
    if not m:
        return None
    return json.loads(H.unescape(m.group(1)))


def bff(state, needle):
    for k, v in state.items():
        if k.startswith("G.text") and needle in k:
            return k, json.loads(v["body"]) if isinstance(v.get("body"), str) else v.get("body")
    return None, None


# ----------------------------------------------------------------------------- geocoding (guarded)
def geocode(addr):
    for i in range(3):
        try:
            return _geo.geocode(addr)
        except Exception as e:  # noqa: BLE001  shared cache file race between agents
            log("  geo.py failed:", repr(e), "- retry", i + 1)
            time.sleep(0.7 + i)
    try:
        cache = json.load(open(MYCACHE, encoding="utf-8"))
    except Exception:
        cache = {}
    key = _geo.normalize(addr)
    if key in cache:
        v = cache[key]
        return (v[0], v[1]) if v else (None, None)
    result = None
    for cand in [key] + ([re.sub(r"\d.*$", "", key)] if re.search(r"\d", key) else []):
        try:
            time.sleep(0.3)
            data = requests.get("https://msearch.gsi.go.jp/address-search/AddressSearch?q=" + urllib.parse.quote(cand),
                                headers={"User-Agent": UA}, timeout=20).json()
        except Exception:
            data = []
        if data:
            lon, lat = data[0]["geometry"]["coordinates"]
            result = [lat, lon]
            break
    cache[key] = result
    try:
        json.dump(cache, open(MYCACHE, "w", encoding="utf-8"), ensure_ascii=False)
    except Exception:
        pass
    return (result[0], result[1]) if result else (None, None)


# ----------------------------------------------------------------------------- parsing helpers
def z2h(t):
    return t.translate(str.maketrans("０１２３４５６７８９．ＬＤＫＳＲ", "0123456789.LDKSR")) if t else t


def yen(txt):
    """'7.5' / '7.5万円' -> 75000 ; '8,000円' -> 8000 ; 'なし'/'-'/'－' -> 0 ; else None"""
    if txt is None:
        return None
    t = z2h(str(txt)).replace(",", "").replace("\xa0", " ").strip()
    if t in ("なし", "無", "-", "－", "--", "0円", "0") or t.startswith("なし"):
        return 0
    m = re.search(r"(\d+(?:\.\d+)?)\s*万", t)
    if m:
        v = float(m.group(1)) * 10000
        m2 = re.search(r"万\s*(\d+)\s*円?", t)
        if m2:
            v += int(m2.group(1))
        return int(round(v))
    m = re.search(r"(\d+)\s*円", t)
    if m:
        return int(m.group(1))
    if re.fullmatch(r"\d+(?:\.\d+)?", t):  # list page: chinryo "7.5" means 万円
        return int(round(float(t) * 10000))
    return None


def built(txt):
    if not txt:
        return None, None
    m = re.search(r"(\d{4})年\s*(\d{1,2})?月?", z2h(txt))
    return (int(m.group(1)), int(m.group(2)) if m.group(2) else None) if m else (None, None)


def structure_of(txt):
    if not txt:
        return None
    t = txt
    if "鉄骨鉄筋" in t or "SRC" in t:
        return "SRC"
    if "鉄筋" in t or "RC" in t:
        return "RC"
    if "重量鉄骨" in t:
        return "重量鉄骨"
    if "軽量鉄骨" in t:
        return "軽量鉄骨"
    if "鉄骨" in t:
        return "鉄骨"
    if "木造" in t:
        return "木造"
    return "その他"


def layout_ok(layout):
    if not layout:
        return False
    m = re.match(r"(\d+)\s*(S?LDK|S?DK|S?K|R)", z2h(layout).upper())
    if not m:
        return False
    rooms, kind = int(m.group(1)), m.group(2)
    return rooms >= 4 or (rooms == 3 and kind in ("LDK", "SLDK", "DK", "SDK")) or (rooms == 2 and kind in ("LDK", "SLDK"))


def floor_of(txt):
    """'2階' / '3階建 / 1階' -> unit floor ; 'B1階' -> -1"""
    if not txt:
        return None
    t = z2h(txt)
    if "/" in t:
        t = t.split("/")[-1]
    m = re.search(r"(B|地下)?(\d+)\s*[-〜～]?\s*(\d+)?\s*階", t)
    if not m:
        return None
    f = int(m.group(2))
    return -f if m.group(1) else f


def floors_of(txt):
    if not txt:
        return None
    t = z2h(txt)
    m = re.search(r"地上\s*(\d+)\s*階", t) or re.search(r"(\d+)\s*階建", t)
    return int(m.group(1)) if m else None


def area_of(txt):
    if not txt:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", z2h(txt).replace(",", ""))
    return float(m.group(1)) if m else None


def age_years(y):
    return None if y is None else datetime.date.today().year - y


def tier_of(year, structure, kind):
    if year is None:
        return None
    if year >= 2001:
        t = "A"
    elif 1991 <= year <= 2000 and structure in ("RC", "SRC"):
        t = "B"
    else:
        return None
    if kind and re.search(r"一戸建|テラスハウス|戸建", kind):
        return "house"
    return t


# ----------------------------------------------------------------------------- list pages
def parse_list(state):
    key, body = bff(state, "property-list/first-view")
    if body is None:
        return None, [], None
    d = body.get("data") or {}
    pl = d.get("propertyListData") or {}
    cfg = d.get("config") or {}
    units = []
    for b in pl.get("propertyList") or []:
        by, bm = built(b.get("chikunengetsu"))
        traffic = [a.get("name") for a in (b.get("access") or []) if a.get("name")]
        for rm in b.get("roomList") or []:
            u = {"bukkenNo": rm.get("bukkenNo"), "building_name_list": b.get("bukkenNm"), "room_name": rm.get("bukkenNm"),
                 "address": b.get("address"), "kind": b.get("syumokuNm"), "built_year": by, "built_month": bm,
                 "building_floors": floors_of(b.get("kaidate")), "traffic": traffic, "room_number": rm.get("roomNumber"),
                 "floor_txt": rm.get("kai"), "floor": floor_of(rm.get("kai")), "rent": yen(rm.get("chinryo")),
                 "kanrihi": yen(rm.get("managementFee")), "shikikin_txt": rm.get("deposit"), "shikikin": yen(rm.get("deposit")),
                 "reikin_txt": rm.get("keyMoney"), "reikin": yen(rm.get("keyMoney")), "layout": z2h(rm.get("madori")),
                 "area_m2": area_of(rm.get("area")), "agent": (rm.get("kaiin") or {}).get("syogo"),
                 "nayose": rm.get("heyaNayoseBukkenNoList") or []}
            u["url"] = f"{BASE}/chintai/{u['bukkenNo']}/"
            units.append(u)
    return {"total": pl.get("totalBukkenCount"), "buildings": pl.get("tatemonoCount"), "pageNo": cfg.get("pageNo"),
            "key": re.sub(r"frontUa=[^&]*", "frontUa=..", key)}, units, d


def crawl_lists():
    all_units = {}
    stats = []
    for ward, wname in WARDS.items():
        for q, basic in QUERIES.items():
            params = [("basic", basic), ("q", "1"), ("sort", "33"), ("limit", "30")]
            page, total, seen = 1, None, 0
            while page <= 40:
                url = f"{BASE}/chintai/kyoto/{ward}-city/list/" + (f"page{page}/" if page > 1 else "")
                r = get(url, params=params)
                if r is None or r.status_code != 200:
                    log(f"[{wname} {q}] page {page} HTTP {r.status_code if r else 'ERR'} {url}")
                    break
                with open(os.path.join(RAW, f"list_{ward}_{q}_p{page}.html"), "w", encoding="utf-8") as f:
                    f.write(r.text)
                st = state_of(r.text)
                if st is None:
                    log(f"[{wname} {q}] page {page}: no SSR state (blocked?) len={len(r.text)}")
                    break
                meta, units, d = parse_list(st)
                if meta is None:
                    log(f"[{wname} {q}] page {page}: no first-view data"); break
                if page == 1:
                    total = meta["total"]
                    # sanity: the SSR echo must show our conditions were applied
                    sel = []
                    for g in ((d.get("conditions") or {}).get("basicConditions") or {}).get("group", []):
                        for c in g["conditions"]:
                            sel += [x["value"] for x in c["condition"] if x.get("selected")]
                    if "kc115" not in sel:
                        log(f"[{wname} {q}] WARNING: filters not echoed: {sel}")
                if meta["pageNo"] not in (page, str(page)):
                    log(f"[{wname} {q}] page {page}: server pageNo={meta['pageNo']} -> stopping")
                    break
                for u in units:
                    u["ward"] = wname; u["query"] = q
                    all_units.setdefault(u["bukkenNo"], u)
                seen += len(units)
                log(f"[{wname} {q}] page {page}: {len(units)} rooms / {len(d.get('propertyListData', {}).get('propertyList') or [])} buildings (total rooms={total}, buildings={meta['buildings']})")
                if not units or (meta["buildings"] and page * 30 >= int(meta["buildings"])):
                    break
                page += 1
            stats.append({"ward": wname, "query": q, "total_rooms": total, "rooms_seen": seen, "pages": page})
    return all_units, stats


# ----------------------------------------------------------------------------- detail pages
def parse_detail(state):
    key, body = bff(state, "property-detail/first-view")
    if body is None:
        return None
    pd = (body.get("data") or {}).get("propertyData") or {}
    ri = pd.get("rentInfo") or {}
    bi = ri.get("buildingInfo") or {}
    oi = ri.get("otherPropertyInfo") or {}
    feats = {f.get("title"): f.get("text") for f in (pd.get("facilityFeatureList") or []) if f.get("title")}
    costs = {}
    for row in (pd.get("costInfo") or {}).get("costList") or []:
        for c in row:
            if c.get("title"):
                costs[c["title"]] = c.get("text")
    dim = pd.get("dimension") or {}
    mp = ((pd.get("surroundingInfo") or {}).get("mapData") or {})
    d = {"title": ri.get("buildingNm"), "kind": ri.get("syumokuNm"), "address": ri.get("address"),
         "price": ri.get("price"), "deposit": ri.get("deposit"), "keyMoney": ri.get("keyMoney"), "hoshokin": ri.get("hoshokin"),
         "managementFee": ri.get("managementFee"), "madori": ri.get("madori"), "madori_detail": bi.get("madori"),
         "area": ri.get("area"), "chikunengetsu": ri.get("chikunengetsu") or bi.get("chikunengetsu"),
         "kaidateKai": ri.get("kaidateKai"), "direction": ri.get("lightSurface"), "access": [a.get("name") for a in ri.get("access") or []],
         "move_in": ri.get("hikiwatashi"), "genkyo": ri.get("genkyo"), "structure_txt": bi.get("tatemonoKozo"),
         "biko": bi.get("biko"), "contract": oi.get("contract"), "koshinryo": oi.get("koshinryo"), "jokento": oi.get("jokento"),
         "torihiki": oi.get("torihikiTaiyo"), "kokai": oi.get("kokaiDate"), "next_update": oi.get("jikaiKousinData"),
         "features": feats, "costs": costs, "setsubi": dim.get("setsubi"), "tokki": dim.get("tokki"),
         "hosho": ((pd.get("costInfo") or {}).get("initialCostSimulation") or {}).get("chintaiHosho"),
         "agent": (pd.get("kaiinInfo") or {}).get("syogo"), "lat": mp.get("ido"), "lon": mp.get("keido"),
         "sokosu": bi.get("sokosu"), "appeal": ri.get("appealPoint"), "pickup": ri.get("pickup") or {}}
    eq = " / ".join(x for x in [d["setsubi"], d["tokki"], feats.get("設備"), feats.get("共用施設"), feats.get("その他")] if x)
    d["equip_text"] = eq
    if re.search(r"エレベータ|EV", eq):
        d["elevator"] = True
    elif eq:
        d["elevator"] = False
    else:
        d["elevator"] = None
    d["parking"] = feats.get("駐車・駐輪") or feats.get("駐車場")
    return d


def parking_fee(txt):
    if not txt:
        return None
    t = z2h(txt).replace(",", "")
    m = re.search(r"(\d+)\s*円\s*/?\s*月?", t)
    return int(m.group(1)) if m and ("駐車" in txt or "円" in txt) else None


def main():
    t0 = time.time()
    log("=== at home crawl start", datetime.datetime.now(JST).isoformat())
    units, stats = crawl_lists()
    log(f"list crawl done: {len(units)} unique rooms")
    # 名寄せ: the same room offered by several agents appears several times; keep one, remember the others
    seen_rooms = {}
    dups = 0
    for u in list(units.values()):
        sig = (u["address"], u["building_name_list"], u["floor_txt"], u["layout"], u["area_m2"], u["rent"])
        if sig in seen_rooms:
            seen_rooms[sig]["dup_urls"] = seen_rooms[sig].get("dup_urls", []) + [u["url"]]
            del units[u["bukkenNo"]]; dups += 1
        else:
            seen_rooms[sig] = u
    log(f"after 名寄せ dedupe: {len(units)} rooms ({dups} duplicates folded)")

    cands, rejected = [], {}

    def rej(reason):
        rejected[reason] = rejected.get(reason, 0) + 1

    for u in units.values():
        if u["rent"] is None or u["rent"] > 100000:
            rej("rent>10万 or unknown"); continue
        if u["area_m2"] is None or u["area_m2"] < 45:
            rej("area<45"); continue
        if not layout_ok(u["layout"]):
            rej(f"layout {u['layout']}"); continue
        if u["built_year"] is None or u["built_year"] < 1991:
            rej("built<1991 or unknown"); continue
        is_house = bool(re.search(r"一戸建|テラスハウス|戸建", u.get("kind") or ""))
        if not is_house and u["floor"] is not None and u["floor"] in (1, -1):
            rej("1F"); continue
        if u.get("reikin") is not None and u["reikin"] > u["rent"] * 1.05:
            rej("reikin>1 month"); continue
        cands.append(u)
    log(f"pre-filter: {len(cands)} candidates; rejected: {rejected}")

    kept, dropped = [], []
    for u in cands:
        fn = os.path.join(RAW, f"detail_{u['bukkenNo']}.json")
        d = None
        if os.path.exists(fn) and time.time() - os.path.getmtime(fn) < 3 * 3600:
            d = json.load(open(fn, encoding="utf-8")); u["http_status"] = 200; u["detail_cached"] = True
        else:
            r = get(u["url"])
            u["http_status"] = r.status_code if r is not None else None
            if r is None or r.status_code != 200:
                log(f"  detail {u['url']} -> HTTP {u['http_status']}")
                u["drop_reason"] = f"detail HTTP {u['http_status']}"; dropped.append(u); continue
            st = state_of(r.text)
            try:
                d = parse_detail(st) if st else None
            except Exception:
                log("  parse error", u["url"], traceback.format_exc()); d = None
            if d is None:
                u["drop_reason"] = "detail page without property data"; dropped.append(u); continue
            d["_html_len"] = len(r.text)
            json.dump(d, open(fn, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        u["detail"] = d
        u["verified"] = bool(d.get("title"))
        # refresh from detail
        if d.get("kaidateKai"):
            u["floor"] = floor_of(d["kaidateKai"]); u["building_floors"] = floors_of(d["kaidateKai"]) or u["building_floors"]
        by, bm = built(d.get("chikunengetsu"))
        if by:
            u["built_year"], u["built_month"] = by, bm
        u["structure_txt"] = d.get("structure_txt"); u["structure"] = structure_of(d.get("structure_txt"))
        if yen(d.get("price")) is not None:
            u["rent"] = yen(d.get("price"))
        if yen(d.get("managementFee")) is not None:
            u["kanrihi"] = yen(d.get("managementFee"))
        if d.get("keyMoney") is not None:
            u["reikin"], u["reikin_txt"] = yen(d["keyMoney"]), d["keyMoney"]
        if d.get("deposit") is not None:
            u["shikikin"], u["shikikin_txt"] = yen(d["deposit"]), d["deposit"]
        if d.get("address"):
            u["address"] = d["address"]
        if d.get("madori"):
            u["layout"] = z2h(d["madori"])
        if area_of(d.get("area")):
            u["area_m2"] = area_of(d.get("area"))
        u["tier"] = tier_of(u["built_year"], u["structure"], d.get("kind") or u.get("kind"))
        if u["tier"] is None:
            u["drop_reason"] = f"age/structure rule (built {u['built_year']}, {u['structure']})"; dropped.append(u); continue
        if u["rent"] > 100000:
            u["drop_reason"] = "rent>10万 (detail)"; dropped.append(u); continue
        if u["area_m2"] is None or u["area_m2"] < 45 or not layout_ok(u["layout"]):
            u["drop_reason"] = "area/layout (detail)"; dropped.append(u); continue
        if u["reikin"] is not None and u["reikin"] > u["rent"] * 1.05:
            u["drop_reason"] = "reikin>1 month (detail)"; dropped.append(u); continue
        u["elevator"] = d.get("elevator")
        if u["tier"] != "house":
            if u["floor"] is not None and u["floor"] in (1, -1):
                u["drop_reason"] = "1F (detail)"; dropped.append(u); continue
            if u["floor"] is not None and u["floor"] >= 4 and u["elevator"] is not True:
                u["drop_reason"] = f"floor {u['floor']} without confirmed elevator (elevator={u['elevator']})"; dropped.append(u); continue
        # coordinates: site map coords first, geo.py fallback + cross-check
        try:
            u["lat"], u["lon"] = float(d["lat"]), float(d["lon"]); u["geo_source"] = "athome map coords"
        except Exception:
            u["lat"] = u["lon"] = None
        glat, glon = geocode(u["address"]) if u.get("address") else (None, None)
        if u["lat"] is None and glat is not None:
            u["lat"], u["lon"] = glat, glon; u["geo_source"] = "geo.py"
        u["geo_py"] = [glat, glon, dist_km(glat, glon)] if glat is not None else None
        u["distance_km"] = dist_km(u["lat"], u["lon"])
        if u["distance_km"] is None:
            u["drop_reason"] = "could not geocode"; dropped.append(u); continue
        if u["distance_km"] > MAX_KM:
            u["drop_reason"] = f"distance {u['distance_km']} km > {MAX_KM}"; dropped.append(u); continue
        kept.append(u)
        log(f"  KEEP [{u['tier']}] {d.get('title')} {u['layout']} {u['area_m2']}㎡ {u['rent']}円 {u['floor']}F/{u['building_floors']} {u['built_year']} {u['structure']} {u['distance_km']}km")

    now = datetime.datetime.now(JST).isoformat(timespec="seconds")
    out = []
    for u in kept:
        d = u["detail"]
        f = d.get("features") or {}
        notes = []
        if d.get("direction"):
            notes.append(f"向き: {d['direction']}")
        for k in ("条件", "設備", "共用施設", "セキュリティ", "バス・トイレ", "キッチン", "収納", "冷暖房", "テレビ・通信", "特徴", "その他"):
            if f.get(k):
                notes.append(f"{k}: {f[k][:160]}")
        if d.get("tokki"):
            notes.append("特記: " + d["tokki"][:120])
        for k, lab in (("contract", "契約期間"), ("koshinryo", "更新料"), ("torihiki", "取引態様"), ("move_in", "引渡"), ("genkyo", "現況"), ("sokosu", "総戸数"), ("kokai", "公開日")):
            if d.get(k):
                notes.append(f"{lab}: {d[k]}")
        if d.get("biko"):
            notes.append("備考: " + re.sub(r"<br\s*/?>", " ", d["biko"])[:200])
        if u.get("dup_urls"):
            notes.append("同一住戸の他掲載: " + ", ".join(u["dup_urls"]))
        notes.append(f"kind: {d.get('kind')}; geo: {u.get('geo_source')}")
        if u.get("geo_py") and u["geo_py"][2] is not None and abs(u["geo_py"][2] - u["distance_km"]) > 1.0:
            notes.append(f"geo.py cross-check differs: {u['geo_py'][2]} km")
        other_initial = "; ".join(x for x in [
            f"保証金: {d['hoshokin']}" if d.get("hoshokin") and d["hoshokin"] not in ("なし", "-", "－") else None,
            f"保証会社: {d['hosho']}" if d.get("hosho") else None,
            f"更新料: {d['koshinryo']}" if d.get("koshinryo") else None,
            f"仲介手数料: {(d.get('costs') or {}).get('仲介手数料')}" if (d.get("costs") or {}).get("仲介手数料") else None,
            f"その他: {(d.get('costs') or {}).get('その他')}" if (d.get("costs") or {}).get("その他") else None,
        ] if x)
        out.append({
            "source": "athome", "url": u["url"],
            "building_name": d.get("title") or u.get("building_name_list"),
            "address": u["address"], "lat": u["lat"], "lon": u["lon"], "distance_km": u["distance_km"],
            "rent": u["rent"], "kanrihi": u.get("kanrihi"),
            "shikikin": (f"{u['shikikin']:,}円 ({u['shikikin']/u['rent']:.1f}ヶ月)" if u.get("shikikin") else ("0円" if u.get("shikikin") == 0 else u.get("shikikin_txt"))),
            "reikin": (f"{u['reikin']:,}円 ({u['reikin']/u['rent']:.1f}ヶ月)" if u.get("reikin") else ("0円" if u.get("reikin") == 0 else u.get("reikin_txt"))),
            "other_initial": other_initial or None,
            "layout": u["layout"], "area_m2": u["area_m2"],
            "floor": u["floor"], "building_floors": u["building_floors"], "elevator": u["elevator"],
            "built_year": u["built_year"], "built_month": u["built_month"], "age_years": age_years(u["built_year"]),
            "structure": u["structure"],
            "parking": d.get("parking"), "parking_fee": parking_fee(d.get("parking")),
            "nearest_station": (d.get("access") or u.get("traffic") or [None])[0],
            "tier": u["tier"], "notes": " | ".join(notes),
            "agent": d.get("agent") or u.get("agent"), "guarantor_company": d.get("hosho"), "move_in": d.get("move_in"),
            "direction": d.get("direction"), "layout_detail": d.get("madori_detail"), "room_number": u.get("room_number"),
            "verified_http_200": u.get("http_status") == 200 and bool(d.get("title")),
            "ward": u["ward"], "fetched_at": now,
        })
    out.sort(key=lambda x: (x["tier"] != "A", x["distance_km"] or 99))
    json.dump(out, open(os.path.join(OUT, "athome.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump([{k: v for k, v in u.items() if k != "detail"} for u in dropped], open(os.path.join(OUT, "athome_dropped.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=str)

    lines = ["# at home (athome.co.jp) — summary", "",
             f"Run: {now} (JST). Elapsed {time.time()-t0:.0f}s. ~1 request/s, Chrome UA.",
             "Method: the Angular list/detail pages are server-side rendered with the BFF JSON embedded in `<script id=\"serverApp-state\">`, "
             "so plain requests + JSON parsing was enough (Playwright was used only to discover the filter/URL format; no private API calls). No captcha / Imperva / geo block was hit.", "",
             "## Server-side filters used",
             "`/chintai/kyoto/<ward>-city/list/[pageN/]?basic=" + COMMON + ",kn021&q=1&sort=33&limit=30` (tier A: 築25年以内) and `...,kn023,kh001` (tier-B candidates: 築35年以内 + 鉄筋系).",
             "kc115 = 賃料上限10万円 (賃料のみ; 管理費含むオプション kc201 not used), kt007 = 専有面積45㎡以上, km010/014/015/018/019/021 = 2LDK/3DK/3LDK/4K/4DK/4LDK以上, ki002 = 定期借家含む.",
             "Applied client-side: floor ≠ 1F (the site has a 2階以上 insistence code P02, deliberately not used so that houses stay visible), elevator rule for ≥4F, 礼金 ≤ 1 month, exact 1991–2000 range + RC/SRC for tier B, distance ≤ 5.5 km.",
             "Pagination: `/list/pageN/` with the same query string (30 buildings per page, several rooms per building).", "",
             "## Pages scanned", "| ward | query | site total rooms | rooms seen | pages |", "|---|---|---|---|---|"]
    for s in stats:
        lines.append(f"| {s['ward']} | {s['query']} | {s['total_rooms']} | {s['rooms_seen']} | {s['pages']} |")
    lines += ["", f"Unique rooms from lists: **{len(units) + dups}** ({dups} 名寄せ duplicates folded → {len(units)}); after list-level pre-filter: **{len(cands)}**; "
                  f"detail pages fetched: {len(cands)}; **kept: {len(out)}** (A: {sum(1 for x in out if x['tier']=='A')}, B: {sum(1 for x in out if x['tier']=='B')}, house: {sum(1 for x in out if x['tier']=='house')}).",
              "", "List-level rejections: " + ", ".join(f"{k}: {v}" for k, v in sorted(rejected.items(), key=lambda x: -x[1])),
              "", "## Dropped after detail fetch"]
    for u in dropped:
        lines.append(f"- {(u.get('detail') or {}).get('title') or u.get('building_name_list')} ({u.get('layout')}, {u.get('rent')}円, {u.get('floor')}F, {u.get('built_year')}) — {u.get('drop_reason')} — {u['url']}")
    lines += ["", "## Kept units", "| tier | building | layout | ㎡ | rent | 管理費 | floor | built | struct | km | parking | url |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in out:
        lines.append(f"| {x['tier']} | {x['building_name']} | {x['layout']} | {x['area_m2']} | {x['rent']:,} | {x['kanrihi']} | {x['floor']}/{x['building_floors']}{' EV' if x['elevator'] else ''} | {x['built_year']}.{x['built_month']} | {x['structure']} | {x['distance_km']} | {(x['parking'] or '')[:40]} | {x['url']} |")
    lines += ["", "## Problems / notes",
              "- `/chintai/kyoto/kyoto-city/list/` (the URL given in the brief) always returns 0件 — the real 京都市 pages are `kyoto-locate` (whole city) and `kyoto_<ward>-city` (per ward).",
              "- `basic=` conditions in the URL are only honoured together with `q=1` (found in the app's route chunk).",
              "- `elevator` = true when the listing's 設備/共用施設 text mentions エレベーター, false when it has equipment text without it, null when no equipment text at all.",
              "- Coordinates come from the detail page's own map data (building-level); geo.py (GSI) is used as fallback/cross-check.",
              "- Rooms listed by several agents (名寄せ) are folded into one record; the other URLs are kept in notes."]
    open(os.path.join(OUT, "athome.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    log(f"=== done: kept {len(out)} / dropped {len(dropped)} ; wrote out/athome.json, out/athome.md ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
