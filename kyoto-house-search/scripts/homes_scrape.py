#!/usr/bin/env python3
"""LIFULL HOME'S (homes.co.jp) scraper for the Kyoto rental search.

Tier A : built 2001+ (server filter 築25年以内), any structure.
Tier B : wider age search restricted to 鉄筋系 (RC/SRC), keep only built 1991-2000.
Writes out/homes.json + out/homes.md, raw HTML under out/raw/homes/.
"""
import json, os, re, sys, time, datetime, traceback, subprocess
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from geo import geocode, dist_km  # noqa: E402

OUT = os.path.join(HERE, "out")
RAW = os.path.join(OUT, "raw", "homes")
os.makedirs(RAW, exist_ok=True)
LOG = open(os.path.join(HERE, "homes_scrape.log"), "a", encoding="utf-8")

JST = datetime.timezone(datetime.timedelta(hours=9))
NOW = datetime.datetime.now(JST)
MAX_KM = 5.5
RENT_MAX = 100000
AREA_MIN = 45.0

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
}
PACE = 2.0           # seconds between requests (1 req/s with persisted cookies triggered the AWS WAF challenge)
WAF_COOKIES = {}     # aws-waf-token etc. obtained by homes_waf.js when a 202 challenge appears
GSTAT = {"waf_challenges": 0, "waf_solved": 0, "cache_hits": 0, "requests": 0}
_last = [0.0]


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.write(s + "\n"); LOG.flush()


def solve_waf(url, html_out=None):
    """Run headless Chromium on the challenged URL. Harvests the aws-waf-token cookie for reuse (if the browser
    was challenged) and returns the browser-rendered HTML of the page (or None)."""
    out = os.path.join(RAW, "waf_cookies.json")
    html_out = html_out or os.path.join(RAW, "waf_page.html")
    try:
        env = dict(os.environ, PLAYWRIGHT_BROWSERS_PATH="/opt/pw-browsers")
        r = subprocess.run(["node", os.path.join(HERE, "homes_waf.js"), url, out, html_out], capture_output=True,
                           text=True, timeout=180, env=env)
        info = json.loads(r.stdout.strip().splitlines()[-1]) if r.stdout.strip() else {}
        log("  WAF solver:", r.stdout.strip()[:200], "|", r.stderr.strip()[-200:])
        for c in json.load(open(out, encoding="utf-8")):
            if "homes.co.jp" in (c.get("domain") or "") and c["name"] == "aws-waf-token":
                WAF_COOKIES[c["name"]] = c["value"]   # only the WAF token; session cookies are what got challenged
                GSTAT["waf_solved"] += 1
        if info.get("ok"):
            t = open(html_out, encoding="utf-8").read()
            if "challenge-container" not in t and len(t) > 20000:
                GSTAT["browser_pages"] = GSTAT.get("browser_pages", 0) + 1
                return t
        return None
    except Exception as e:
        log("  WAF solver failed:", e)
        return None


def _cached(path):
    try:
        if os.path.exists(path) and os.path.getsize(path) > 20000:
            t = open(path, encoding="utf-8").read()
            if "challenge-container" not in t and ("totalNum" in t or "該当物件は0件" in t or "築年月" in t):
                return t
    except Exception:
        pass
    return None


def get(url, params=None, save_as=None):
    """Polite GET (PACE seconds apart, no persisted cookies), reuse of saved raw pages, one retry on 5xx /
    network error, AWS-WAF 202 challenge -> solve with headless Chromium and retry. Returns (status, text)."""
    if save_as:
        t = _cached(os.path.join(RAW, save_as))
        if t is not None:
            GSTAT["cache_hits"] += 1
            return 200, t
    for attempt in range(4):
        wait = PACE - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        GSTAT["requests"] += 1
        try:
            r = requests.get(url, params=params, headers=HEADERS, cookies=WAF_COOKIES or None, timeout=40)
        except Exception as e:  # network
            log("  ! network error", url, e)
            if attempt < 3:
                time.sleep(5); continue
            return None, ""
        if r.status_code == 202 and "challenge" in r.text:
            GSTAT["waf_challenges"] += 1
            log("  ! AWS WAF challenge (202) on", r.url[:120], "-> fetching via headless Chromium")
            html = solve_waf(r.url, os.path.join(RAW, save_as) if save_as else None)
            if html is not None:
                return 200, html          # browser-rendered page (already saved to save_as)
            time.sleep(45)
            continue
        if r.status_code >= 500 and attempt < 3:
            log("  ! HTTP", r.status_code, "retrying", r.url)
            time.sleep(5); continue
        if save_as:
            with open(os.path.join(RAW, save_as), "w", encoding="utf-8") as f:
                f.write(r.text)
        return r.status_code, r.text
    return 202, ""


# ---------------------------------------------------------------- search conditions
WARDS = ["kyoto_shimogyo-city", "kyoto_nakagyo-city", "kyoto_minami-city", "kyoto_ukyo-city",
         "kyoto_kamigyo-city", "kyoto_nishikyo-city", "kyoto_higashiyama-city", "kyoto_kita-city",
         "kyoto_fushimi-city"]
LIST_URL = "https://www.homes.co.jp/chintai/kyoto/{ward}/list/"

BASE = {
    "cond[monthmoneyroomh]": "10",     # 賃料上限 10万円 (管理費を含まない; cond[kanrihi]=1 would include it)
    "cond[housearea]": "45",           # 専有面積下限 45m²
    "cond[madori][25]": "25",          # 2LDK
    "cond[madori][33]": "33",          # 3DK
    "cond[madori][35]": "35",          # 3LDK
    "cond[madori][43]": "43",          # 4DK
    "cond[madori][45-]": "45-",        # 4LDK以上
    "cond[sortby]": "period",          # 築年数が新しい順
}
COND_A = dict(BASE, **{"cond[houseageh]": "25"})                           # 築25年以内
COND_B = dict(BASE, **{"cond[houseageh]": "0", "cond[housekouzougroup][rebar]": "rebar"})  # 指定なし + 鉄筋系

ALLOWED_LAYOUT = re.compile(r"^(2S?LDK|[3-9]S?(DK|LDK)|\d{2,}S?(DK|LDK))")


# ---------------------------------------------------------------- helpers
def yen(s):
    """'11.5万円' -> 115000, '5,000円' -> 5000, '-'/'無' -> 0, else None."""
    if s is None:
        return None
    s = s.strip()
    if s in ("-", "無", "なし", "0円", ""):
        return 0
    m = re.search(r"([\d.,]+)\s*万円", s)
    if m:
        return int(round(float(m.group(1).replace(",", "")) * 10000))
    m = re.search(r"([\d,]+)\s*円", s)
    if m:
        return int(m.group(1).replace(",", ""))
    return None


def months_or_yen(s, rent):
    """Return amount in yen for '2ヶ月' / '1.5ヶ月' / '32.6万円' / '無' / '-'; None if unparsable."""
    if s is None:
        return None
    s = s.strip()
    if s in ("-", "無", "なし", ""):
        return 0
    m = re.search(r"([\d.]+)\s*[ヶカか]月", s)
    if m and rent:
        return int(round(float(m.group(1)) * rent))
    return yen(s)


def parse_age(s):
    """'24年 / 2階建' -> (24, 2); '新築 / 5階建' -> (0, 5)."""
    age = floors = None
    if s:
        if "新築" in s:
            age = 0
        m = re.search(r"(\d+)年", s)
        if m:
            age = int(m.group(1))
        m = re.search(r"(\d+)階建", s)
        if m:
            floors = int(m.group(1))
    return age, floors


def norm_structure(s):
    if not s:
        return None
    t = s.replace(" ", "")
    if "SRC" in t or "鉄骨鉄筋" in t:
        return "SRC"
    if t.startswith("RC") or "鉄筋コンクリート" in t or "ＲＣ" in t:
        return "RC"
    if "軽量鉄骨" in t:
        return "軽量鉄骨"
    if "重量鉄骨" in t:
        return "重量鉄骨"
    if "鉄骨" in t:
        return "鉄骨"
    if "木造" in t:
        return "木造"
    return "その他"


def geocode_kyoto(addr):
    """geo.py first; fallback: ward + last 町名 (Kyoto 通り名 addresses confuse the GSI geocoder)."""
    addr = re.sub(r"\s*地図を見る.*$", "", addr or "").strip()
    if not addr:
        return None, None, None
    lat, lon = geocode(addr)
    note = None
    if lat is None:
        m = re.match(r"^(京都府京都市[^\s区]+区)(.*)$", addr)
        if m:
            ward, rest = m.group(1), m.group(2)
            parts = [p for p in re.split(r"上る|下る|上ル|下ル|東入ル|西入ル|東入|西入|通り?|丁目|\d+", rest) if p]
            town = parts[-1] if parts else ""
            town = re.sub(r"[^぀-ヿ一-鿿々ヶ]", "", town)
            if town and town != rest:
                lat, lon = geocode(ward + town)
                if lat is not None:
                    note = "geocoded by 町名 fallback (%s%s)" % (ward, town)
    return lat, lon, note


# ---------------------------------------------------------------- list parsing
def parse_list(html, ward, tier):
    soup = BeautifulSoup(html, "lxml")
    units = []
    # regular merged-building blocks
    for blk in soup.select('div[class*="mod-mergeBuilding"]'):
        cls = " ".join(blk.get("class") or [])
        btype_el = blk.find(class_="bukkenType")
        btype = btype_el.get_text(strip=True) if btype_el else ""
        if not btype:
            for k, v in (("rMansion", "賃貸マンション"), ("rApart", "賃貸アパート"), ("rKodate", "賃貸一戸建て"),
                         ("rTerrace", "賃貸テラスハウス")):
                if k in cls.split():
                    btype = v
            if not btype:
                hd = blk.find(class_="heading")
                btype = (hd.get_text(" ", strip=True).split(" ")[0] if hd else "")
        name_el = blk.find(class_="bukkenName")
        name = name_el.get_text(" ", strip=True) if name_el else None
        spec = {}
        bs = blk.find(class_="bukkenSpec")
        if bs:
            for tr in bs.find_all("tr"):
                th, td = tr.find("th"), tr.find("td")
                if th and td:
                    spec[th.get_text(strip=True)] = td.get_text(" ", strip=True)
        traffic = spec.get("交通", "")
        if name and traffic and name in traffic:
            name = None  # nameless building: HOME'S repeats the station text as heading
        age, floors = parse_age(spec.get("築年数/階数"))
        is_house = ("rKodate" in cls) or ("一戸建" in btype) or ("テラス" in btype) or ("rTerrace" in cls)
        for tr in blk.select("tr.prg-roomInfo"):
            fl_el = tr.find(class_="roomKaisuu")
            fl_txt = fl_el.get_text(strip=True) if fl_el else "-"
            rn_el = tr.find(class_="roomNumber")
            price_td = tr.find("td", class_="price")
            price_txt = price_td.get_text(" ", strip=True) if price_td else ""
            lay_td = tr.find("td", class_="layout")
            lay_txt = lay_td.get_text(" ", strip=True) if lay_td else ""
            a = tr.find("a", class_="prg-detailAnchor")
            href = (a.get("href") if a else None) or tr.get("data-href")
            bid = a.get("data-bid") if a else None
            # price: "9.5 万円 /- 無/無/-/-"  -> rent / kanrihi ; shikikin/reikin/hosho/shikibiki
            m = re.match(r"\s*([\d.]+)\s*万円\s*/\s*([^\s]+)\s*(.*)$", price_txt)
            rent = kanrihi_txt = rest = None
            if m:
                rent = int(round(float(m.group(1)) * 10000))
                kanrihi_txt, rest = m.group(2), m.group(3)
            parts = (rest or "").split("/")
            lm = re.match(r"\s*(\S+?)\s+([\d.]+)\s*m", lay_txt)
            layout = lm.group(1) if lm else (lay_txt.split()[0] if lay_txt else None)
            area = float(lm.group(2)) if lm else None
            # features + agency rows follow this row
            feats, agency = [], None
            nxt = tr.find_next_sibling("tr")
            while nxt is not None and "prg-roomInfo" not in (nxt.get("class") or []):
                if "prg-relatedKeywordsRow" in (nxt.get("class") or []):
                    feats = [li.get_text(strip=True) for li in nxt.find_all("li")]
                if "prg-memberDataRow" in (nxt.get("class") or []):
                    agency = nxt.get_text(" ", strip=True)
                nxt = nxt.find_next_sibling("tr")
            units.append(dict(
                ward=ward, tier_search=tier, building_name=name, building_type=btype, is_house=is_house,
                address=spec.get("所在地"), traffic=traffic, list_age=age, list_floors=floors,
                floor_txt=fl_txt, room_no=rn_el.get_text(strip=True) if rn_el else None,
                rent=rent, kanrihi_txt=kanrihi_txt,
                shikikin_txt=parts[0].strip() if len(parts) > 0 else None,
                reikin_txt=parts[1].strip() if len(parts) > 1 else None,
                layout=layout, area=area, url=href, bid=bid, features=feats, agency=agency, pr=False,
            ))
    # PR (ad) blocks: same conditions, b-URL, less detail
    for blk in soup.select("div.prg-kksBukken"):
        a = blk.find("a", class_="prg-detailLink")
        if not a:
            continue
        name_el = blk.find(class_="bukkenName")
        room_el = blk.find(class_="bukkenRoom")
        btype_el = blk.find(class_="bukkenType")
        btype = btype_el.get_text(strip=True) if btype_el else ""
        spec = {}
        for tr in blk.select(".bukkenSpec tr"):
            th, td = tr.find("th"), tr.find("td")
            if th and td:
                spec[th.get_text(strip=True)] = td.get_text(" ", strip=True)
        pm = re.match(r"\s*([\d.]+)\s*万円\s*/\s*(\S+)", spec.get("賃料/管理費等", ""))
        sm = re.match(r"\s*([\d.]+)\s*m²?\s*/\s*(\S+)", spec.get("専有面積/間取り", ""))
        units.append(dict(
            ward=ward, tier_search=tier, building_name=name_el.get_text(" ", strip=True) if name_el else None,
            building_type=btype, is_house=("一戸建" in btype or "テラス" in btype),
            address=spec.get("所在地"), traffic=spec.get("交通", ""), list_age=None, list_floors=None,
            floor_txt=room_el.get_text(strip=True) if room_el else "-", room_no=None,
            rent=int(round(float(pm.group(1)) * 10000)) if pm else None, kanrihi_txt=pm.group(2) if pm else None,
            shikikin_txt=None, reikin_txt=None,
            layout=sm.group(2) if sm else None, area=float(sm.group(1)) if sm else None,
            url=a.get("href"), bid=a.get("adllid"), features=[], agency=None, pr=True,
        ))
    last = soup.select_one("li.lastPage span, li.lastPage a")
    last_page = int(re.sub(r"\D", "", last.get_text())) if last and re.search(r"\d", last.get_text()) else None
    if last_page is None:
        pages = [int(x.get("data-page")) for x in soup.select(".mod-listPaging a[data-page]")]
        last_page = max(pages) if pages else 1
    tn = soup.find(class_="totalNum")
    total = int(re.sub(r"\D", "", tn.get_text())) if tn and re.search(r"\d", tn.get_text()) else None
    return units, last_page, total


# ---------------------------------------------------------------- detail parsing
def parse_detail(html):
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    d = {}
    for dt in soup.find_all("dt"):
        k = dt.get_text(" ", strip=True)
        dd = dt.find_next_sibling("dd")
        if not dd:
            continue
        v = re.sub(r"\s+", " ", dd.get_text(" ", strip=True))
        d.setdefault(k, []).append(v)

    def first(k):
        return d.get(k, [None])[0]

    title = soup.title.get_text(strip=True) if soup.title else ""
    h1 = [h.get_text(" ", strip=True) for h in soup.find_all("h1") if h.get_text(strip=True)]
    h1 = h1[0] if h1 else ""
    equip = {}
    equip_text = ""
    h2 = [h for h in soup.find_all("h2") if "設備・条件" in h.get_text()]
    if h2:
        sec = h2[0].parent
        equip_text = re.sub(r"\s+", " ", sec.get_text(" ", strip=True))
        for li in sec.find_all("li"):
            p = li.find("p")
            div = li.find("div")
            if p and div and li.find("ul") is None:
                equip[p.get_text(strip=True)] = [s.get_text(strip=True).rstrip("、") for s in div.find_all("span")] or \
                    [re.sub(r"\s+", " ", div.get_text(" ", strip=True))]
        # icon grid: 該当 / 非該当
        icons = {}
        for sp in sec.select("span.sr-only"):
            lab = sp.find_previous_sibling("span")
            if lab:
                icons[lab.get_text(strip=True)] = ("非該当" not in sp.get_text())
        equip["_icons"] = icons
    return dict(d=d, first=first, title=title, h1=h1, equip=equip, equip_text=equip_text)


def build_record(u, det, url, status):
    first = det["first"]
    rent = yen(first("賃料")) if first("賃料") else u["rent"]
    kanrihi = yen(first("管理費等")) if first("管理費等") is not None else yen(u.get("kanrihi_txt"))
    sr = first("敷金/礼金") or ""
    sparts = [p.strip() for p in sr.split("/")]
    shikikin_txt = sparts[0] if sparts else None
    reikin_txt = sparts[1] if len(sparts) > 1 else None
    reikin_yen = months_or_yen(reikin_txt, rent)
    shikikin_yen = months_or_yen(shikikin_txt, rent)
    hosho = first("保証金/敷引・償却金")
    madori = first("間取り") or ""
    layout = madori.split(" ")[0].split("(")[0].strip() if madori else u["layout"]
    area = None
    m = re.search(r"([\d.]+)\s*(?:㎡|m²|m2)", first("専有面積") or "")
    if m:
        area = float(m.group(1))
    floor = bfloors = None
    fl = first("所在階/階数") or ""
    m = re.match(r"\s*(B?\d+)階", fl)
    if m:
        floor = -int(m.group(1)[1:]) if m.group(1).startswith("B") else int(m.group(1))
    m = re.search(r"(\d+)階建", fl)
    if m:
        bfloors = int(m.group(1))
    by = bm = age = None
    m = re.match(r"\s*(\d{4})年(?:(\d{1,2})月)?", first("築年月") or "")
    if m:
        by = int(m.group(1)); bm = int(m.group(2)) if m.group(2) else None
        age = ((NOW.year * 12 + NOW.month) - (by * 12 + (bm or 1))) // 12
    structure_raw = first("建物構造")
    structure = norm_structure(structure_raw)
    equip = det["equip"]
    services = equip.get("設備・サービス") or []
    # structured equipment lists only (位置/入居条件/キッチン/設備・サービス/その他) — the 備考 free text is excluded
    all_equip_items = [x for k, v in equip.items() if k not in ("_icons", "備考") for x in v]
    if any("エレベーター" in x and "なし" not in x and "無" not in x for x in all_equip_items):
        elevator = True
    elif services:
        elevator = False
    else:
        elevator = None
    parking_txt = first("駐車場")
    parking_fee = None
    if parking_txt and not re.fullmatch(r"\s*(無|-|なし)\s*", parking_txt):
        parking_fee = yen(parking_txt) if re.search(r"\d", parking_txt) else None
        if parking_fee == 0:
            parking_fee = None
        if "無料" in parking_txt and parking_fee is None:
            parking_fee = 0
    traffic = first("交通") or u.get("traffic") or ""
    st = re.split(r"\s+(?=\S+\s+\S+駅\s+徒歩)", traffic)
    nearest = None
    m = re.search(r"(\S+)\s+(\S+?駅)\s+(徒歩\d+分|バス[^\s]*)", traffic)
    if m:
        nearest = " ".join(m.groups())
    elif traffic:
        nearest = traffic[:60]
    addr = re.sub(r"\s*地図を見る.*$", "", first("所在地") or u.get("address") or "").strip()
    name = re.sub(r"[（(].*$", "", det["h1"]).strip() or u.get("building_name")
    if name and re.search(r"駅\s*(徒歩|バス)|バス\d+分|下車", name):
        name = None   # nameless building: HOME'S shows the access text as the heading
    icons = equip.get("_icons", {})
    notes = []
    if first("主要採光面"):
        notes.append("向き:" + first("主要採光面"))
    for key in ("オートロック", "追焚機能", "ペット相談", "南向き", "駐車場"):
        if key in icons:
            notes.append(("" if icons[key] else "非") + key)
    hi = [x for x in all_equip_items if any(k in x for k in (
        "宅配ボックス", "床暖房", "浴室乾燥", "インターネット", "都市ガス", "プロパン", "オール電化", "追焚",
        "ペット", "システムキッチン", "カウンターキッチン", "温水洗浄", "TVモニタ", "防犯カメラ", "ウォークイン",
        "駐輪場", "バイク置き場", "二人入居", "楽器", "事務所", "ルームシェア", "敷地内ごみ", "ゴミ出し", "即入居", "分譲"))]
    notes.extend(sorted(set(hi)))
    if first("入居可能時期"):
        notes.append("入居可能:" + first("入居可能時期"))
    if first("現況"):
        notes.append("現況:" + first("現況"))
    if first("総戸数") and first("総戸数") != "-":
        notes.append("総戸数:" + first("総戸数"))
    if structure_raw:
        notes.append("構造:" + structure_raw)
    if first("会社名"):
        notes.append("不動産会社:" + first("会社名"))
    if u.get("building_type"):
        notes.append("種別:" + u["building_type"])
    if madori and "(" in madori:
        notes.append("間取り詳細:" + re.sub(r"\s+", " ", madori)[:120])
    other = []
    if hosho and hosho.replace("-", "").replace("/", "").strip():
        other.append("保証金/敷引・償却:" + hosho)
    for k in ("保証会社", "住宅保険", "更新料", "その他費用", "取引態様", "契約期間", "契約形態"):
        vals = [v for v in det["d"].get(k, []) if v and v != "-"]
        if vals:
            v = max(vals, key=len) if k == "保証会社" else vals[0]
            other.append("%s:%s" % (k, v[:160]))
    if reikin_yen is not None and reikin_txt and "月" not in reikin_txt and reikin_yen:
        pass
    rec = {
        "source": "homes",
        "url": url,
        "building_name": name,
        "address": addr,
        "lat": None, "lon": None, "distance_km": None,
        "rent": rent, "kanrihi": kanrihi,
        "shikikin": shikikin_txt, "reikin": reikin_txt,
        "other_initial": ", ".join(other) if other else None,
        "layout": layout, "area_m2": area,
        "floor": floor, "building_floors": bfloors, "elevator": elevator,
        "built_year": by, "built_month": bm, "age_years": age,
        "structure": structure,
        "parking": parking_txt, "parking_fee": parking_fee,
        "nearest_station": nearest,
        "tier": None,
        "notes": ", ".join(notes),
        "fetched_at": NOW.isoformat(timespec="seconds"),
        "_reikin_yen": reikin_yen, "_shikikin_yen": shikikin_yen, "_http": status, "_title": det["title"],
        "_homes_id": first("LIFULL HOME'S 物件番号"),
    }
    return rec


# ---------------------------------------------------------------- main
def main():
    stats = {"pages": {}, "list_units": 0, "list_units_A": 0, "list_units_B": 0, "pr_units": 0,
             "drop_1F_list": 0, "drop_layout_list": 0, "drop_area_list": 0, "drop_rent_list": 0,
             "drop_age_list_B": 0, "drop_reikin_list": 0, "dup_same_unit": 0, "drop_far_list": 0, "geocode_fail_list": 0,
             "detail_fetched": 0, "detail_http_fail": 0, "drop_1F": 0, "drop_4F_no_elev": 0, "drop_reikin": 0,
             "drop_age": 0, "drop_structure_B": 0, "drop_far": 0, "drop_rent": 0, "drop_area": 0, "drop_layout": 0,
             "kept": 0, "kept_A": 0, "kept_B": 0, "kept_house": 0, "totals": {}}
    all_units = []
    for tier, cond in (("A", COND_A), ("B", COND_B)):
        for ward in WARDS:
            page = 1
            while True:
                params = dict(cond)
                if page > 1:
                    params["page"] = str(page)
                fn = "list%s_%s_p%d.html" % (tier, ward.replace("kyoto_", "").replace("-city", ""), page)
                st, html = get(LIST_URL.format(ward=ward), params=params, save_as=fn)
                stats["pages"][fn] = st
                if st != 200 or not html:
                    log("LIST", tier, ward, "page", page, "HTTP", st); break
                units, last_page, total = parse_list(html, ward, tier)
                if page == 1:
                    stats["totals"]["%s_%s" % (tier, ward)] = total
                ages = [u["list_age"] for u in units if u["list_age"] is not None]
                log("LIST", tier, ward, "page %d/%s" % (page, last_page), "total", total, "units", len(units),
                    "ages", (min(ages), max(ages)) if ages else None,
                    "challenge?" , ("captcha" in html.lower() or "access denied" in html.lower()))
                all_units.extend(units)
                if tier == "B" and ages and min(ages) > 36:
                    break
                if last_page is None or page >= last_page or page >= 40:
                    break
                page += 1
    stats["list_units"] = len(all_units)
    stats["list_units_A"] = sum(1 for u in all_units if u["tier_search"] == "A")
    stats["list_units_B"] = sum(1 for u in all_units if u["tier_search"] == "B")
    stats["pr_units"] = sum(1 for u in all_units if u["pr"])

    # ---- list-level pre-filter + dedupe
    cands = {}
    for u in all_units:
        if u["tier_search"] == "B" and u["list_age"] is not None and (u["list_age"] < 24 or u["list_age"] > 36):
            stats["drop_age_list_B"] += 1; continue
        if re.fullmatch(r"1階", u["floor_txt"] or ""):
            stats["drop_1F_list"] += 1; continue
        if u["layout"] and not ALLOWED_LAYOUT.match(u["layout"]):
            stats["drop_layout_list"] += 1; continue
        if u["area"] is not None and u["area"] < AREA_MIN:
            stats["drop_area_list"] += 1; continue
        if u["rent"] is not None and u["rent"] > RENT_MAX:
            stats["drop_rent_list"] += 1; continue
        ry = months_or_yen(u.get("reikin_txt"), u["rent"])
        if ry is not None and u["rent"] and ry > u["rent"] + 1:
            stats["drop_reikin_list"] += 1; continue
        key = (u["address"], u["floor_txt"], u["layout"], round(u["area"] or 0))
        if key in cands:
            stats["dup_same_unit"] += 1
            c = cands[key]
            if u["rent"] is not None and (c["rent"] is None or u["rent"] < c["rent"]):
                # cheaper listing of the same unit becomes the representative
                u["alt_urls"] = c["alt_urls"] + ["%s (賃料%s円)" % (c["url"], c["rent"])]
                if not u["building_name"] and c["building_name"]:
                    u["building_name"] = c["building_name"]
                cands[key] = u
            else:
                c["alt_urls"].append("%s (賃料%s円)" % (u["url"], u["rent"]) if u["rent"] != c["rent"] else u["url"])
                if not c["building_name"] and u["building_name"]:
                    c["building_name"] = u["building_name"]
            continue
        u["alt_urls"] = []
        cands[key] = u
    log("CANDIDATES after list filter:", len(cands))

    # ---- geocode from list address, skip far ones before fetching detail
    todo = []
    for u in cands.values():
        lat, lon, gnote = geocode_kyoto(u["address"])
        u["lat"], u["lon"], u["gnote"] = lat, lon, gnote
        u["distance_km"] = dist_km(lat, lon) if lat is not None else None
        if u["distance_km"] is None:
            stats["geocode_fail_list"] += 1
        elif u["distance_km"] > MAX_KM:
            stats["drop_far_list"] += 1; continue
        todo.append(u)
    todo.sort(key=lambda u: (0 if u["tier_search"] == "A" else 1, u["distance_km"] if u["distance_km"] is not None else 9, u["rent"] or 0))
    log("to fetch detail:", len(todo))
    if "--plan" in sys.argv:
        # hand the detail-page list to homes_fetch.js (headless Chromium), which saves HTML into the cache paths
        plan = []
        for u in todo:
            if not u["url"]:
                continue
            key = re.sub(r"\W", "", u["url"].rsplit("/chintai/", 1)[-1])[:60]
            plan.append({"url": u["url"], "path": os.path.join(RAW, "detail_%s.html" % key)})
        with open(os.path.join(HERE, "fetch_plan.json"), "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=0)
        log("PLAN written:", len(plan), "detail pages ->", os.path.join(HERE, "fetch_plan.json"))
        return

    results = []
    unverified = []
    seen_urls = set()
    for i, u in enumerate(todo, 1):
        url = u["url"]
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        key = re.sub(r"\W", "", url.rsplit("/chintai/", 1)[-1])[:60]
        if "--cache-only" in sys.argv and _cached(os.path.join(RAW, "detail_%s.html" % key)) is None:
            stats["pending_not_cached"] = stats.get("pending_not_cached", 0) + 1
            unverified.append({
                "source": "homes", "url": url, "verified": False, "tier_search": u["tier_search"],
                "building_name": u["building_name"], "building_type": u["building_type"], "address": u["address"],
                "lat": u["lat"], "lon": u["lon"], "distance_km": u["distance_km"], "rent": u["rent"],
                "kanrihi_text": u["kanrihi_txt"], "shikikin": u["shikikin_txt"], "reikin": u["reikin_txt"],
                "layout": u["layout"], "area_m2": u["area"], "floor_text": u["floor_txt"],
                "building_floors": u["list_floors"], "list_age_years": u["list_age"],
                "built_year_approx": (NOW.year - u["list_age"]) if u["list_age"] is not None else None,
                "traffic": u["traffic"], "list_features": u["features"], "agency": u["agency"],
                "alt_urls": u["alt_urls"], "note": "list-page data only; unit page not fetched (AWS WAF CAPTCHA budget)"})
            continue
        st, html = get(url, save_as="detail_%s.html" % key)
        stats["detail_fetched"] += 1
        if st != 200 or not html:
            stats["detail_http_fail"] += 1
            log("DETAIL", i, "HTTP", st, url); continue
        try:
            det = parse_detail(html)
            rec = build_record(u, det, url, st)
        except Exception:
            log("DETAIL parse error", url); log(traceback.format_exc()); continue
        rec["_ward"] = u["ward"]; rec["_search_tier"] = u["tier_search"]
        rec["_alt_urls"] = u["alt_urls"]
        # verify page still shows the unit
        shows = (rec["layout"] or "") in det["title"] or (rec["building_name"] or "@@") in det["title"]
        if not shows or "物件が見つかりません" in det["title"] or "掲載終了" in html[:200000]:
            log("DETAIL", i, "does not show unit?", url, det["title"][:80])
        # ---- hard filters on detail data
        why = None
        if rec["rent"] is None or rec["rent"] > RENT_MAX:
            why = "drop_rent"
        elif rec["area_m2"] is not None and rec["area_m2"] < AREA_MIN:
            why = "drop_area"
        elif rec["layout"] and not ALLOWED_LAYOUT.match(rec["layout"]):
            why = "drop_layout"
        elif rec["floor"] == 1:
            why = "drop_1F"
        elif rec["floor"] is not None and rec["floor"] >= 4 and rec["elevator"] is not True:
            why = "drop_4F_no_elev"
        elif rec["_reikin_yen"] is not None and rec["rent"] and rec["_reikin_yen"] > rec["rent"] * 1.0 + 1:
            why = "drop_reikin"
        else:
            by = rec["built_year"]
            if by is None:
                why = "drop_age"
            elif by >= 2001:
                rec["tier"] = "house" if u["is_house"] else "A"
            elif 1991 <= by <= 2000:
                if rec["structure"] in ("RC", "SRC"):
                    rec["tier"] = "house" if u["is_house"] else "B"
                else:
                    why = "drop_structure_B"
            else:
                why = "drop_age"
        if why is None:
            # distance: prefer detail address
            lat, lon, gnote = geocode_kyoto(rec["address"])
            if lat is None:
                lat, lon, gnote = u["lat"], u["lon"], u["gnote"]
            rec["lat"], rec["lon"] = lat, lon
            rec["distance_km"] = dist_km(lat, lon) if lat is not None else None
            if gnote:
                rec["notes"] += ", " + gnote
            if rec["distance_km"] is not None and rec["distance_km"] > MAX_KM:
                why = "drop_far"
            elif rec["distance_km"] is None:
                rec["notes"] += ", 距離不明(geocode失敗)"
        if why:
            stats[why] += 1
            log("DETAIL", i, "DROP", why, rec["building_name"], rec["floor"], rec["layout"], rec["area_m2"], rec["built_year"], rec["structure"], rec["distance_km"], url)
            continue
        alts = [a for a in dict.fromkeys(rec["_alt_urls"]) if a and a != url]
        if alts:
            rec["notes"] += ", 同一住戸の他掲載: " + " ".join(alts[:4])
        if u.get("bid"):
            rec["notes"] += ", b-URL: https://www.homes.co.jp/chintai/b-%s/" % u["bid"]
        stats["kept"] += 1
        stats["kept_" + rec["tier"]] += 1
        log("DETAIL", i, "KEEP", rec["tier"], rec["building_name"], rec["rent"], rec["layout"], rec["area_m2"], rec["floor"], "/", rec["building_floors"], "elev", rec["elevator"], rec["built_year"], rec["structure"], rec["distance_km"], "km", url)
        results.append(rec)

    # result-stage dedupe: same physical unit reached via differently written addresses / building names
    merged = {}
    for r in results:
        k2 = (r["floor"], r["layout"], r["area_m2"], r["rent"], r["built_year"], r["built_month"], r["building_floors"],
              round(r["lat"] or 0, 3), round(r["lon"] or 0, 3))
        if k2 in merged:
            m = merged[k2]
            stats["dup_same_unit_detail"] = stats.get("dup_same_unit_detail", 0) + 1
            if not m["building_name"] and r["building_name"]:
                m["building_name"] = r["building_name"]
            m["notes"] += ", 同一住戸の他掲載: " + r["url"]
            if r["parking"] and not m["parking"]:
                m["parking"], m["parking_fee"] = r["parking"], r["parking_fee"]
            continue
        merged[k2] = r
    results = list(merged.values())
    stats["kept"] = len(results)
    for t in ("A", "B", "house"):
        stats["kept_" + t] = sum(1 for r in results if r["tier"] == t)
    results.sort(key=lambda r: ({"A": 0, "B": 1, "house": 2}[r["tier"]], r["distance_km"] if r["distance_km"] is not None else 99, r["rent"] or 0))
    clean = []
    for r in results:
        clean.append({k: v for k, v in r.items() if not k.startswith("_")})
    with open(os.path.join(OUT, "homes.json"), "w", encoding="utf-8") as f:
        json.dump(clean, f, ensure_ascii=False, indent=1)
    if unverified:
        with open(os.path.join(OUT, "homes_unverified.json"), "w", encoding="utf-8") as f:
            json.dump(unverified, f, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "homes_debug.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    stats.update(GSTAT)
    with open(os.path.join(OUT, "homes_stats.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)
    log("DONE kept", stats["kept"], json.dumps({k: v for k, v in stats.items() if k not in ("pages", "totals")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
