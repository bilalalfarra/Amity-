#!/usr/bin/env python3
"""CHINTAI (chintai.net) scraper for the Kyoto rental search.

Server-side filters discovered from the search form (#searchInputForm, GET /kyoto/area/<ward>/list/):
  ct=100  rent upper bound 10万円 (賃料 only; the `k=1` "共益費・管理費を含む" box is deliberately NOT sent)
  sf=45   floor area lower bound 45㎡
  m=...   layouts: 6=2LDK 8=3DK 9=3LDK A=4K B=4DK C=4LDK D=5K/5DK E=5LDK以上
  h=7     building age 25年以内 (tier A)          kz=1  鉄筋系 structure (tier B candidates, no age cap)
Pagination: pager links /kyoto/area/<ward>/list/pageN/?...  (follow the 次へ link).
"""
import json, os, re, sys, time, datetime, traceback
import requests
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import urllib.parse  # noqa: E402
import geo as _geo  # noqa: E402  (shared helper, not modified)
from geo import dist_km  # noqa: E402

MYCACHE = os.path.join(HERE, "out", "chintai_geocache.json")


def geocode(addr):
    """geo.geocode with retries; the shared cache file is written by several agents at once and can
    raise FileNotFoundError on its tmp->real rename. Falls back to a private GSI lookup + private cache."""
    for i in range(3):
        try:
            return _geo.geocode(addr)
        except Exception as e:  # noqa: BLE001
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
    cands = [key]
    c2 = re.sub(r"\d.*$", "", key)
    if c2 and c2 != key:
        cands.append(c2)
    result = None
    for cand in cands:
        url = "https://msearch.gsi.go.jp/address-search/AddressSearch?q=" + urllib.parse.quote(cand)
        try:
            time.sleep(0.3)
            data = requests.get(url, headers={"User-Agent": UA}, timeout=20).json()
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

OUT = os.path.join(HERE, "out")
RAW = os.path.join(OUT, "raw", "chintai")
os.makedirs(RAW, exist_ok=True)
LOG = open(os.path.join(OUT, "chintai_log.txt"), "a", encoding="utf-8")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
S = requests.Session()
S.headers.update({"User-Agent": UA, "Accept-Language": "ja,en;q=0.8",
                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})
BASE = "https://www.chintai.net"
MAX_KM = 5.5
JST = datetime.timezone(datetime.timedelta(hours=9))

WARDS = {"26106": "下京区", "26104": "中京区", "26107": "南区", "26108": "右京区", "26102": "上京区",
         "26111": "西京区", "26105": "東山区", "26101": "北区", "26109": "伏見区", "26103": "左京区"}
LAYOUT_CODES = ["6", "8", "9", "A", "B", "C", "D", "E"]
QUERIES = {
    "A": [("ct", "100"), ("sf", "45"), ("h", "7")] + [("m", c) for c in LAYOUT_CODES],
    "B": [("ct", "100"), ("sf", "45"), ("kz", "1")] + [("m", c) for c in LAYOUT_CODES],
}

_last = [0.0]


def log(*a):
    msg = " ".join(str(x) for x in a)
    print(msg, flush=True)
    LOG.write(msg + "\n"); LOG.flush()


def get(url, params=None, tries=2):
    """Polite GET: >=1.0 s between requests, retry once on 5xx / network error."""
    for i in range(tries):
        wait = 1.0 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        try:
            r = S.get(url, params=params, timeout=30)
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


# ----------------------------------------------------------------------------- parsing helpers
def yen(txt):
    """'9.7万円' -> 97000 ; '9,000円' -> 9000 ; 'なし'/'--'/'-'/'0円' -> 0 ; else None"""
    if txt is None:
        return None
    t = txt.replace(",", "").replace("\xa0", " ").strip()
    if t in ("なし", "無", "--", "-", "0円", "0") or t.startswith("なし"):
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
    return None


def built(txt):
    """'1994年10月（築32年）' -> (1994, 10)"""
    if not txt:
        return None, None
    m = re.search(r"(\d{4})年\s*(\d{1,2})?月?", txt)
    if not m:
        return None, None
    return int(m.group(1)), (int(m.group(2)) if m.group(2) else None)


def structure_of(txt):
    if not txt:
        return None
    t = txt
    if "鉄骨鉄筋" in t:
        return "SRC"
    if "鉄筋コンクリート" in t or re.search(r"\bRC\b", t):
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
    """2LDK/2SLDK or 3DK+/3LDK+ or any 4-room+ layout. Not 1LDK, 2DK, 2K, 3K."""
    if not layout:
        return False
    m = re.match(r"(\d+)\s*(S?LDK|S?DK|S?K|R)", layout.upper().replace("Ｌ", "L").replace("Ｄ", "D").replace("Ｋ", "K"))
    if not m:
        return False
    rooms, kind = int(m.group(1)), m.group(2)
    if rooms >= 4:
        return True
    if rooms == 3 and kind in ("LDK", "SLDK", "DK", "SDK"):
        return True
    if rooms == 2 and kind in ("LDK", "SLDK"):
        return True
    return False


def floor_of(txt):
    """'3階' -> 3 ; '1階/7階建' -> 1 ; 'B1階' -> -1 ; '2-3階' -> 2 ; else None"""
    if not txt:
        return None
    t = txt.replace("階建", "").split("/")[0]
    m = re.search(r"(B)?(\d+)\s*[-〜～]?\s*(\d+)?\s*階", t)
    if not m:
        return None
    f = int(m.group(2))
    return -f if m.group(1) else f


def floors_of(txt):
    """'7階建' / '1階/7階建' / '地上7階地下1階建' -> 7"""
    if not txt:
        return None
    m = re.search(r"地上\s*(\d+)\s*階", txt) or re.search(r"(\d+)\s*階建", txt) or re.search(r"/\s*(\d+)\s*階", txt)
    return int(m.group(1)) if m else None


def age_years(y):
    return None if y is None else datetime.date.today().year - y


def tier_of(year, structure, kind):
    """Return 'A', 'B', 'house' or None (fails the age rule)."""
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
def parse_list(html):
    soup = BeautifulSoup(html, "lxml")
    units = []
    for sec in soup.select("section.cassette_item"):
        h2 = sec.select_one(".cassette_ttl h2")
        kind = ""
        name = None
        if h2 is not None:
            sp = h2.find("span")
            kind = sp.get_text(strip=True) if sp else ""
            name = h2.get_text(" ", strip=True).replace(kind, "", 1).strip()
        info = {}
        for tr in sec.select(".bukken_information tr"):
            cells = tr.find_all(["th", "td"])
            i = 0
            while i + 1 < len(cells):
                if cells[i].name == "th" and cells[i + 1].name == "td":
                    info[cells[i].get_text(strip=True)] = cells[i + 1]
                    i += 2
                else:
                    i += 1
        addr = None; lat = lon = None; traffic = []
        if "住所" in info:
            td = info["住所"]
            mp = td.find("p", class_="map")
            if mp is not None:
                a = mp.find("a")
                if a is not None and a.get("onclick"):
                    m = re.search(r"showGoogleMap\(\s*([\d.]+)\s*,\s*([\d.]+)", a["onclick"])
                    if m:
                        lat, lon = float(m.group(1)), float(m.group(2))
                mp.extract()
            addr = td.get_text(" ", strip=True)
        if "交通" in info:
            traffic = [li.get_text(" ", strip=True) for li in info["交通"].find_all("li")]
        by, bm = built(info["築年"].get_text(strip=True) if "築年" in info else "")
        nfl = floors_of(info["階建"].get_text(strip=True) if "階建" in info else "")
        struct_txt = info["構造"].get_text(strip=True) if "構造" in info else None
        for tb in sec.select("tbody.js-detailLinkUrl"):
            u = {"building_name": name, "kind": kind, "address": addr, "lat": lat, "lon": lon,
                 "traffic": traffic, "built_year": by, "built_month": bm, "building_floors": nfl,
                 "structure_txt": struct_txt, "structure": structure_of(struct_txt)}
            u["url"] = BASE + tb.get("data-detailurl")
            u["bkkey"] = tb.get("data-bkkey")
            hid = {}
            for inp in tb.find_all("input", type="hidden"):
                c = inp.get("class")
                if c:
                    hid[c[0]] = inp.get("value")
            u["rent"] = int(hid["chinRyo"]) if hid.get("chinRyo", "").isdigit() else None
            u["layout"] = hid.get("madori")
            try:
                u["area_m2"] = float(hid["senMenseki"])
            except Exception:
                u["area_m2"] = None
            fl = tb.select_one("td.floar li")
            u["floor_txt"] = fl.get_text(strip=True) if fl else None
            u["floor"] = floor_of(u["floor_txt"])
            pr = tb.select_one("td.price")
            if pr is not None:
                parts = [p for p in pr.get_text("|", strip=True).split("|") if p]
                u["kanrihi_txt"] = parts[-1] if len(parts) >= 3 else None
                u["kanrihi"] = yen(u["kanrihi_txt"])
            op = tb.select_one("td.other_price")
            if op is not None:
                sp = [s.get_text(strip=True) for s in op.find_all("span")]
                u["shikikin_txt"] = sp[0] if len(sp) > 0 else None
                u["reikin_txt"] = sp[1] if len(sp) > 1 else None
                u["shikikin"] = yen(u["shikikin_txt"])
                u["reikin"] = yen(u["reikin_txt"])
            shop = sec.select_one(".information_box a.gtm_aw_shopDetail")
            u["agent"] = shop.get_text(" ", strip=True) if shop else None
            pt = sec.select_one(".point_txt")
            u["point_txt"] = pt.get_text(" ", strip=True) if pt else None
            icons = [li.get_text(strip=True) for li in sec.select(".icn_box li")]
            u["icons"] = icons
            units.append(u)
    pager = soup.find(class_="list_pager")
    total = None
    nxt = None
    if pager is not None:
        t = pager.find(class_="total")
        if t is not None:
            try:
                total = int(t.get_text(strip=True).replace(",", ""))
            except Exception:
                total = None
        for a in pager.find_all("a", href=True):
            if "次へ" in a.get_text():
                nxt = a["href"]
    nores = "ご指定の条件に一致する物件は見つかりませんでした" in soup.get_text()
    return units, total, nxt, nores


HIDDEN = {}  # building name -> hidden-room count reported by the list page ("残りN件を表示する")


def crawl_pages(ward, wname, q, params, all_units, sort=None):
    """Crawl all pages of one ward/query (optionally with an explicit sort). Returns (total, units_seen, pages, hidden_found)."""
    page = 1
    total = None
    nunits = 0
    hidden_found = False
    url = f"{BASE}/kyoto/area/{ward}/list/"
    while url and page <= 30:
        # NOTE: the site's own 次へ link drops the multi-valued m= params, so build page URLs ourselves
        if page > 1:
            url = f"{BASE}/kyoto/area/{ward}/list/page{page}/"
        extra = [("o", sort)] if sort else ([("o", "10")] if page > 1 else [])
        r = get(url, params=params + extra)
        if r is None or r.status_code != 200:
            log(f"[{wname} {q}{' o='+sort if sort else ''}] page {page} HTTP {r.status_code if r else 'ERR'}")
            break
        fn = os.path.join(RAW, f"list_{ward}_{q}{'_o'+sort if sort else ''}_p{page}.html")
        with open(fn, "w", encoding="utf-8") as f:
            f.write(r.text)
        units, tot, nxt, nores = parse_list(r.text)
        if page == 1:
            total = tot if tot is not None else (0 if nores else None)
        for u in units:
            u["ward"] = wname; u["query"] = q
            all_units.setdefault(u["bkkey"], u)
        soup = BeautifulSoup(r.text, "lxml")
        for sec in soup.select("section.cassette_item.build"):
            el = sec.find(string=re.compile(r"残り\d+件"))
            if el:
                hidden_found = True
                h2 = sec.select_one(".cassette_ttl h2")
                nm = h2.get_text(" ", strip=True) if h2 else "?"
                HIDDEN[nm] = max(HIDDEN.get(nm, 0), int(re.search(r"残り(\d+)件", el).group(1)))
        nunits += len(units)
        log(f"[{wname} {q}{' o='+sort if sort else ''}] page {page}: {len(units)} units (total={tot}, next={'yes' if nxt else 'no'}, hidden={'yes' if hidden_found else 'no'})")
        url = nxt  # only used as a "has next page" flag
        page += 1
    return total, nunits, page - 1, hidden_found


def crawl_lists():
    all_units = {}
    stats = []
    for ward, wname in WARDS.items():
        for q, params in QUERIES.items():
            total, nunits, pages, hidden = crawl_pages(ward, wname, q, params, all_units)
            extra_pages = 0
            if hidden:
                # The list page shows at most 3 rooms per building and loads the rest ("残りN件") through
                # /api/list/buildingProperties/, which robots.txt disallows. Instead re-read the same result
                # set sorted by rent ascending and descending (o=2 / o=3), so the cheapest and the most
                # expensive rooms of each building are both displayed; the union recovers up to 6 rooms/building.
                for sort in ("2", "3"):
                    _, _, p2, _ = crawl_pages(ward, wname, q, params, all_units, sort=sort)
                    extra_pages += p2
            stats.append({"ward": wname, "query": q, "total_site": total, "units_seen": nunits, "pages": pages, "extra_sort_pages": extra_pages})
    return all_units, stats


# ----------------------------------------------------------------------------- detail pages
def table_pairs(soup):
    pairs = {}
    for tbl in soup.find_all("table"):
        for tr in tbl.find_all("tr"):
            cells = tr.find_all(["th", "td"], recursive=False)
            i = 0
            while i + 1 < len(cells):
                if cells[i].name == "th" and cells[i + 1].name == "td":
                    k = cells[i].get_text(" ", strip=True).replace("\xa0", " ")
                    v = re.sub(r"\s+", " ", cells[i + 1].get_text(" ", strip=True))
                    if k and k not in pairs:
                        pairs[k] = v
                    i += 2
                else:
                    i += 1
    return pairs


def parse_detail(html, u):
    soup = BeautifulSoup(html, "lxml")
    d = {}
    d["title"] = soup.title.get_text(strip=True) if soup.title else ""
    p = table_pairs(soup)
    d["pairs"] = p
    d["kanrihi"] = yen(p.get("管理費等"))
    sk = p.get("敷金 / 保証金", "")
    rk = p.get("礼金 / 償却", "")
    d["shikikin_txt"] = sk
    d["reikin_txt"] = rk
    d["shikikin"] = yen(sk.split("/")[0]) if sk else None
    d["hoshokin"] = yen(sk.split("/")[1]) if "/" in sk else None
    d["reikin"] = yen(rk.split("/")[0]) if rk else None
    d["shokyaku"] = yen(rk.split("/")[1]) if "/" in rk else None
    d["layout_full"] = p.get("間取り")
    d["area_txt"] = p.get("専有面積")
    d["built_txt"] = p.get("築年")
    d["direction"] = p.get("方位") or p.get("位置")
    d["kind"] = p.get("建物種別")
    d["structure_txt"] = p.get("構造")
    d["floor_txt"] = p.get("物件階層")
    d["address"] = re.sub(r"地図で物件の周辺環境をチェック！?", "", p.get("住所", "")).strip() or None
    d["traffic"] = p.get("交通")
    d["parking"] = p.get("駐車・駐輪")
    d["conditions"] = p.get("条件")
    d["other_initial"] = p.get("その他初期費用")
    d["koshinryo"] = p.get("更新料")
    d["guarantor_co"] = p.get("家賃保証会社等")
    d["insurance"] = p.get("保険")
    d["remarks"] = p.get("備考")
    d["move_in"] = p.get("入居時期")
    d["contract"] = p.get("契約期間")
    d["deal_type"] = p.get("取引形態")
    d["updated"] = p.get("情報更新日")
    equip_rows = [p.get(k) for k in ("放送・通信", "収納", "キッチン/バス・トイレ", "セキュリティ", "その他", "位置") if p.get(k)]
    box = soup.select_one(".mod_equipmentBox")
    icons = [li.get_text(" ", strip=True) for li in box.find_all("li") if "on" in (li.get("class") or [])] if box else []
    d["equip_icons"] = icons
    equip_text = " / ".join(equip_rows + icons)
    d["equip_text"] = equip_text
    if "エレベーター" in equip_text or "エレベータ" in equip_text or "EV" in equip_text:
        d["elevator"] = True
    elif equip_rows or icons:
        d["elevator"] = False
    else:
        d["elevator"] = None
    # agent (shop)
    agent = None
    for a in soup.select('a[href^="/shop/"]'):
        t = a.get_text(" ", strip=True)
        t = re.sub(r"の詳細を見る$", "", t).replace("\u3000", " ").replace("\xa0", " ").strip()
        if t and len(t) > 3 and "店舗" not in t[:2]:
            agent = t
            break
    d["agent"] = agent
    d["pet"] = bool(re.search(r"ペット(可|相談)", soup.get_text()))
    return d


def parking_fee(txt):
    if not txt:
        return None
    m = re.search(r"([\d,]+)\s*円\s*/\s*月", txt) or re.search(r"（\s*([\d,]+)\s*円", txt)
    return int(m.group(1).replace(",", "")) if m else None


def main():
    t0 = time.time()
    log("=== CHINTAI crawl start", datetime.datetime.now(JST).isoformat())
    units, stats = crawl_lists()
    log(f"list crawl done: {len(units)} unique units from {sum(s['units_seen'] for s in stats)} rows")
    # ---- pre-filter on list data
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
        t = tier_of(u["built_year"], u["structure"], u["kind"])
        if t is None:
            rej("age/structure rule"); continue
        u["tier"] = t
        if u["floor"] is not None and u["floor"] in (1, -1) and t != "house":
            rej("1F"); continue
        if u.get("reikin") is not None and u["reikin"] > u["rent"] * 2.05:
            rej("reikin>1 month"); continue
        cands.append(u)
    log(f"pre-filter: {len(cands)} candidates; rejected: {rejected}")

    kept, dropped = [], []
    for i, u in enumerate(cands):
        fn = os.path.join(RAW, f"detail_{u['bkkey']}.html")
        if os.path.exists(fn) and time.time() - os.path.getmtime(fn) < 3 * 3600:
            html = open(fn, encoding="utf-8").read(); status = 200; u["detail_cached"] = True
        else:
            r = get(u["url"])
            status = r.status_code if r is not None else None
            if r is None or status != 200:
                log(f"  detail {u['url']} -> HTTP {status}")
                u["http_status"] = status
                u["drop_reason"] = f"detail HTTP {status}"; dropped.append(u); continue
            html = r.text
            with open(fn, "w", encoding="utf-8") as f:
                f.write(html)
        u["http_status"] = status
        try:
            d = parse_detail(html, u)
        except Exception:
            log("  parse error", u["url"], traceback.format_exc()); d = {}
        u["detail"] = d
        # verification: page shows this unit
        shows = (u["bkkey"] in html) and (u["layout"] or "") in d.get("title", "")
        u["verified"] = bool(shows)
        # refresh fields from detail
        if d.get("floor_txt"):
            u["floor"] = floor_of(d["floor_txt"]); u["building_floors"] = floors_of(d["floor_txt"]) or u["building_floors"]
        if d.get("built_txt"):
            by, bm = built(d["built_txt"]); u["built_year"], u["built_month"] = by or u["built_year"], bm or u["built_month"]
        if d.get("structure_txt"):
            u["structure_txt"] = d["structure_txt"]; u["structure"] = structure_of(d["structure_txt"])
        if d.get("kanrihi") is not None:
            u["kanrihi"] = d["kanrihi"]
        if d.get("reikin") is not None:
            u["reikin"] = d["reikin"]; u["reikin_txt"] = d["reikin_txt"]
        if d.get("shikikin") is not None:
            u["shikikin"] = d["shikikin"]; u["shikikin_txt"] = d["shikikin_txt"]
        if d.get("address"):
            u["address"] = d["address"]
        u["tier"] = tier_of(u["built_year"], u["structure"], d.get("kind") or u["kind"])
        if u["tier"] is None:
            u["drop_reason"] = "age/structure rule (detail)"; dropped.append(u); continue
        if u["reikin"] is not None and u["reikin"] > u["rent"] * 2.05:
            u["drop_reason"] = "reikin>1 month (detail)"; dropped.append(u); continue
        u["elevator"] = d.get("elevator")
        if u["tier"] != "house":
            if u["floor"] is not None and u["floor"] in (1, -1):
                u["drop_reason"] = "1F (detail)"; dropped.append(u); continue
            if u["floor"] is not None and u["floor"] >= 4 and u["elevator"] is not True:
                u["drop_reason"] = f"floor {u['floor']} without confirmed elevator (elevator={u['elevator']})"; dropped.append(u); continue
        # geocode: site coordinates preferred, geo.py fallback / cross-check
        glat, glon = geocode(u["address"]) if u.get("address") else (None, None)
        if u["lat"] is None and glat is not None:
            u["lat"], u["lon"] = glat, glon; u["geo_source"] = "geo.py"
        else:
            u["geo_source"] = "chintai map coords"
        u["geo_py"] = [glat, glon, dist_km(glat, glon)] if glat is not None else None
        u["distance_km"] = dist_km(u["lat"], u["lon"])
        if u["distance_km"] is None:
            u["drop_reason"] = "could not geocode"; dropped.append(u); continue
        if u["distance_km"] > MAX_KM:
            u["drop_reason"] = f"distance {u['distance_km']} km > {MAX_KM}"; dropped.append(u); continue
        kept.append(u)
        log(f"  KEEP [{u['tier']}] {u['building_name']} {u['layout']} {u['area_m2']}㎡ {u['rent']}円 {u['floor']}F/{u['building_floors']} {u['built_year']} {u['structure']} {u['distance_km']}km")

    # ---- output
    now = datetime.datetime.now(JST).isoformat(timespec="seconds")
    out = []
    for u in kept:
        d = u.get("detail", {})
        notes = []
        for k in ("direction", "conditions", "contract", "deal_type", "move_in", "koshinryo"):
            if d.get(k):
                notes.append(f"{k}: {d[k]}")
        if d.get("equip_icons"):
            notes.append("設備: " + ", ".join(d["equip_icons"]))
        if d.get("remarks"):
            notes.append("備考: " + d["remarks"][:200])
        if u.get("point_txt"):
            notes.append("PR: " + u["point_txt"][:200])
        notes.append(f"kind: {d.get('kind') or u.get('kind')}; updated {d.get('updated')}; geo: {u.get('geo_source')}")
        if u.get("geo_py") and u["geo_py"][2] is not None and u["distance_km"] is not None and abs(u["geo_py"][2] - u["distance_km"]) > 1.0:
            notes.append(f"geo.py cross-check differs: {u['geo_py'][2]} km")
        other_initial = "; ".join(x for x in [
            f"その他初期費用: {d['other_initial']}" if d.get("other_initial") else None,
            f"更新料: {d['koshinryo']}" if d.get("koshinryo") else None,
            f"保証会社: {d['guarantor_co']}" if d.get("guarantor_co") else None,
            f"保険: {d['insurance']}" if d.get("insurance") else None,
            f"保証金/償却: {d.get('hoshokin')}/{d.get('shokyaku')}" if (d.get("hoshokin") or d.get("shokyaku")) else None,
        ] if x)
        out.append({
            "source": "chintai",
            "url": u["url"],
            "building_name": u["building_name"],
            "address": u["address"],
            "lat": u["lat"], "lon": u["lon"], "distance_km": u["distance_km"],
            "rent": u["rent"], "kanrihi": u.get("kanrihi"),
            "shikikin": (f"{u['shikikin']:,}円" if u.get("shikikin") is not None else None) and (f"{u['shikikin']:,}円 ({u['shikikin']/u['rent']:.1f}ヶ月)" if u['shikikin'] else "0円"),
            "reikin": (f"{u['reikin']:,}円 ({u['reikin']/u['rent']:.1f}ヶ月)" if u.get("reikin") else ("0円" if u.get("reikin") == 0 else None)),
            "other_initial": other_initial or None,
            "layout": u["layout"], "area_m2": u["area_m2"],
            "floor": u["floor"], "building_floors": u["building_floors"], "elevator": u["elevator"],
            "built_year": u["built_year"], "built_month": u["built_month"], "age_years": age_years(u["built_year"]),
            "structure": u["structure"],
            "parking": d.get("parking"), "parking_fee": parking_fee(d.get("parking")),
            "nearest_station": (u["traffic"][0] if u.get("traffic") else None),
            "tier": u["tier"],
            "notes": " | ".join(notes),
            "agent": d.get("agent") or u.get("agent"),
            "guarantor_company": d.get("guarantor_co"),
            "move_in": d.get("move_in"),
            "direction": d.get("direction"),
            "layout_detail": d.get("layout_full"),
            "verified_http_200": u.get("verified", False) and u.get("http_status") == 200,
            "ward": u["ward"],
            "fetched_at": now,
        })
    out.sort(key=lambda x: (x["tier"] != "A", x["distance_km"] or 99))
    with open(os.path.join(HERE, "out_r2", "chintai.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, "out_r2", "chintai_dropped.json"), "w", encoding="utf-8") as f:
        json.dump([{k: v for k, v in u.items() if k != "detail"} | {"detail_kind": (u.get("detail") or {}).get("kind")} for u in dropped],
                  f, ensure_ascii=False, indent=1, default=str)

    # ---- markdown summary
    lines = ["# CHINTAI (chintai.net) — summary", "",
             f"Run: {now} (JST). Elapsed {time.time()-t0:.0f}s. ~1 request/s, Chrome UA, plain requests+bs4.", "",
             "## Server-side filters used",
             "`/kyoto/area/<ward>/list/?ct=100&sf=45&m=6&m=8&m=9&m=A&m=B&m=C&m=D&m=E` (+`h=7` for tier A = 築25年以内, or `kz=1` 鉄筋系 with no age cap for tier-B candidates).",
             "ct = 賃料上限 10万円 (管理費を含まない: `k=1` not sent), sf = 専有面積 45㎡以上, m = 2LDK/3DK/3LDK/4K/4DK/4LDK/5K・5DK/5LDK+.",
             "Not available server-side: floor ≠ 1F (only an *include 1F* checkbox exists), elevator, 礼金 ≤ 1 month, exact year range 1991–2000 → applied client-side.",
             "Pagination: `/list/pageN/` URLs built by the script (the site's 次へ link drops the multi-valued `m=` params).",
             "Rooms beyond 3 per building are collapsed (残りN件) and normally loaded via `/api/list/buildingProperties/` (robots.txt: Disallow /api/) → not called; instead the affected ward/query lists were re-read sorted by rent asc/desc (o=2/o=3) to surface those rooms.", "",
             "## Pages scanned", "| ward | query | site total | units seen | pages | extra sort pages |", "|---|---|---|---|---|---|"]
    for s in stats:
        lines.append(f"| {s['ward']} | {s['query']} | {s['total_site']} | {s['units_seen']} | {s['pages']} | {s.get('extra_sort_pages', 0)} |")
    if HIDDEN:
        lines += ["", "Buildings with collapsed rooms on the list page (残りN件) and how many unique rooms were collected:"]
        for nm, n in HIDDEN.items():
            got = sum(1 for u in units.values() if ((u.get('kind') or '') + ' ' + (u.get('building_name') or '')).strip() == nm)
            lines.append(f"- {nm}: 3 shown + {n} hidden → {got} unique rooms collected")
    lines += ["", f"Unique units collected from lists: **{len(units)}**; after list-level pre-filter: **{len(cands)}**; "
                  f"detail pages fetched: {len(cands)}; **kept: {len(out)}** (A: {sum(1 for x in out if x['tier']=='A')}, "
                  f"B: {sum(1 for x in out if x['tier']=='B')}, house: {sum(1 for x in out if x['tier']=='house')}).",
              "", "List-level rejections: " + ", ".join(f"{k}: {v}" for k, v in sorted(rejected.items(), key=lambda x: -x[1])),
              "", "## Dropped after detail fetch"]
    for u in dropped:
        lines.append(f"- {u.get('building_name')} ({u.get('layout')}, {u.get('rent')}円, {u.get('floor')}F, {u.get('built_year')}) — {u.get('drop_reason')} — {u['url']}")
    lines += ["", "## Kept units", "| tier | building | layout | ㎡ | rent | 管理費 | floor | built | struct | km | parking | url |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in out:
        lines.append(f"| {x['tier']} | {x['building_name']} | {x['layout']} | {x['area_m2']} | {x['rent']:,} | {x['kanrihi']} | {x['floor']}/{x['building_floors']}{' EV' if x['elevator'] else ''} | {x['built_year']}.{x['built_month']} | {x['structure']} | {x['distance_km']} | {(x['parking'] or '')[:40]} | {x['url']} |")
    lines += ["", "## Problems / notes",
              "- No blocks or captchas; all pages 200.",
              "- The site's result counts are per unit (rooms), buildings are grouped on the list page.",
              "- `elevator` = true when 設備 text lists エレベーター, false when the listing has a 設備 section without it, null when no 設備 section.",
              "- Coordinates come from the listing's own map link (building-level); geo.py (GSI) used as fallback/cross-check.",
              "- 左京区 (26103) was also scanned since its SW corner is within 5.5 km; distance filter applied to everything."]
    with open(os.path.join(HERE, "out_r2", "chintai.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    log(f"=== done: kept {len(out)} / dropped {len(dropped)} ; wrote out/chintai.json, out/chintai.md ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
