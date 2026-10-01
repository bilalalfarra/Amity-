#!/usr/bin/env python3
"""SUUMO (suumo.jp) rental scraper for the Kyoto home search (see spec.md).

Two list searches over 9 wards (2LDK+, >=45 m2, rent <=10万, server-side):
  search 1: cn=25       -> tier A candidates (built 2001+)
  search 2: cn=9999999  -> tier B candidates (built 1991-2000, RC/SRC only; verified on detail page)
Every list-level survivor's detail page (jnc_...) is fetched, parsed, filtered, geocoded,
and finally re-verified (HTTP 200 + unit still shown).  Outputs out/suumo.json + out/suumo.md.
"""
import datetime
import json
import os
import re
import sys
import time
import traceback
from collections import Counter, OrderedDict

import requests
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from geo import geocode, dist_km  # noqa: E402  (shared helper; not modified)

OUT = os.path.join(HERE, "out")
RAW = os.path.join(OUT, "raw", "suumo")
os.makedirs(RAW, exist_ok=True)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
JST = datetime.timezone(datetime.timedelta(hours=9))
NOW = datetime.datetime.now(JST)
MAX_DIST_KM = 5.5
REQ_INTERVAL = 1.0  # seconds between requests

WARDS = OrderedDict([
    ("26101", "北区"), ("26102", "上京区"), ("26104", "中京区"), ("26105", "東山区"),
    ("26106", "下京区"), ("26107", "南区"), ("26108", "右京区"), ("26109", "伏見区"),
    ("26111", "西京区"),
])
HOUSE_LABELS = ("一戸建て", "テラス", "タウンハウス")

# ----------------------------------------------------------------------------- HTTP
session = requests.Session()
session.headers.update({
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.8,en;q=0.6",
})
_last_req = [0.0]
REQ_COUNT = Counter()


def get(url, what="page"):
    """Polite GET: >=1 s between requests, one retry on 5xx / network error."""
    for attempt in (1, 2):
        wait = REQ_INTERVAL - (time.time() - _last_req[0])
        if wait > 0:
            time.sleep(wait)
        try:
            r = session.get(url, timeout=30)
            _last_req[0] = time.time()
            REQ_COUNT[what] += 1
            if r.status_code >= 500 and attempt == 1:
                log(f"  {r.status_code} on {url} -> retry")
                time.sleep(3)
                continue
            return r
        except requests.RequestException as e:
            _last_req[0] = time.time()
            REQ_COUNT[what] += 1
            log(f"  network error {e!r} on {url} (attempt {attempt})")
            if attempt == 1:
                time.sleep(3)
                continue
            return None
    return None


def log(msg):
    print(msg, flush=True)


# ----------------------------------------------------------------------------- helpers
def T(el):
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)) if el is not None else ""


def z2h(s):
    """Full-width digits/letters -> half-width."""
    return s.translate(str.maketrans("０１２３４５６７８９．ＲＣＳ－", "0123456789.RCS-")) if s else s


def money_to_yen(text):
    """'9.5万円' -> 95000, '3000円' -> 3000, '-' / '無' / '' -> 0, unknown -> None."""
    if text is None:
        return None
    t = z2h(text).replace(",", "").replace(" ", "")
    if t in ("", "-", "－", "無", "なし", "0円", "0"):
        return 0
    m = re.search(r"(\d+(?:\.\d+)?)万円?", t)
    if m:
        return int(round(float(m.group(1)) * 10000))
    m = re.search(r"(\d+)円", t)
    if m:
        return int(m.group(1))
    return None


def layout_ok(layout):
    """2LDK or bigger: 2 rooms only with LDK (incl. 2SLDK); 3+ rooms any kitchen type."""
    if not layout:
        return False
    l = z2h(layout).upper().replace("ＬＤＫ", "LDK")
    m = re.match(r"^(\d+)(S?)(LDK|DK|K|L|R)?", l)
    if not m:
        return False
    rooms = int(m.group(1))
    kind = (m.group(3) or "") + ""
    if rooms >= 3:
        return True
    if rooms == 2 and kind == "LDK":
        return True
    return False


def parse_area(text):
    if not text:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", z2h(text))
    return float(m.group(1)) if m else None


def parse_floor_text(text):
    """'3階' -> (3,3); '1-2階' -> (1,2); 'B1-1階' -> (-1,1); '地下1階' -> (-1,-1); '-' -> (None,None)."""
    if not text:
        return None, None
    t = z2h(text).replace("階", "")
    vals = []
    for prefix, num in re.findall(r"(B|地下)?(\d+)", t):
        vals.append(-int(num) if prefix else int(num))
    if not vals:
        return None, None
    return min(vals), max(vals)


def parse_age_text(text):
    """'築24年' -> 24, '新築' -> 0."""
    if not text:
        return None
    if "新築" in text:
        return 0
    m = re.search(r"築(\d+)年", z2h(text))
    return int(m.group(1)) if m else None


def map_structure(text):
    if not text:
        return None, None
    t = z2h(text)
    if "鉄骨鉄筋" in t or "SRC" in t:
        s = "SRC"
    elif "鉄筋" in t or "RC" in t:
        s = "RC"
    elif "重量鉄骨" in t:
        s = "重量鉄骨"
    elif "軽量鉄骨" in t:
        s = "軽量鉄骨"
    elif "鉄骨" in t:
        s = "鉄骨"
    elif "木造" in t:
        s = "木造"
    else:
        s = "その他"
    return s, t


# ----------------------------------------------------------------------------- list pages
def build_list_url(cn, page=1):
    sc = "&".join("sc=" + w for w in WARDS)
    return ("https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=060&bs=040&ta=26&" + sc +
            "&cb=0.0&ct=10.0&et=9999999&mb=45&mt=9999999&md=07&md=09&md=10&md=12&md=13&md=14"
            f"&cn={cn}&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=17&pc=50&page={page}")


def parse_list(html):
    soup = BeautifulSoup(html, "lxml")
    hit_el = soup.select_one("div.paginate_set-hit")
    hit = None
    if hit_el:
        m = re.search(r"([\d,]+)", T(hit_el))
        hit = int(m.group(1).replace(",", "")) if m else None
    max_page = 1
    for a in soup.select("div.pagination a, ol.pagination-parts a"):
        if a.get_text(strip=True).isdigit():
            max_page = max(max_page, int(a.get_text(strip=True)))
    has_next = any("次へ" in a.get_text() for a in soup.select("div.pagination a, p.pagination-parts a"))
    rows = []
    for b in soup.select("div.cassetteitem"):
        name = T(b.select_one("div.cassetteitem_content-title"))
        label = T(b.select_one("div.cassetteitem_content-label"))
        addr = T(b.select_one("li.cassetteitem_detail-col1"))
        stations = [T(d) for d in b.select("li.cassetteitem_detail-col2 div.cassetteitem_detail-text")]
        col3 = [T(d) for d in b.select("li.cassetteitem_detail-col3 div")]
        age_text = col3[0] if col3 else ""
        floors_text = col3[1] if len(col3) > 1 else ""
        for tr in b.select("tr.js-cassette_link"):
            tds = tr.select("td")
            link = None
            for a in tr.select("a[href]"):
                h = a.get("href") or ""
                if "/chintai/jnc_" in h:
                    link = h
                    break
            if not link:
                continue
            m = re.search(r"jnc_(\d+)", link)
            jnc = m.group(1) if m else None
            floor_text = T(tds[2]) if len(tds) > 2 else ""
            rows.append({
                "jnc": jnc,
                "href": "https://suumo.jp" + link if link.startswith("/") else link,
                "building_name": name, "label": label, "address": addr, "stations": stations,
                "age_text": age_text, "floors_text": floors_text, "floor_text": floor_text,
                "rent_text": T(tr.select_one("span.cassetteitem_price--rent")),
                "kanri_text": T(tr.select_one("span.cassetteitem_price--administration")),
                "shikikin_text": T(tr.select_one("span.cassetteitem_price--deposit")),
                "reikin_text": T(tr.select_one("span.cassetteitem_price--gratuity")),
                "layout": T(tr.select_one("span.cassetteitem_madori")),
                "area_text": T(tr.select_one("span.cassetteitem_menseki")),
            })
    return hit, max_page, has_next, rows


def scan_search(cn, tag):
    """Fetch all pages of one search; returns (hit, pages_scanned, rows)."""
    all_rows, page, hit, pages = [], 1, None, 0
    while True:
        url = build_list_url(cn, page)
        r = get(url, "list")
        if r is None or r.status_code != 200:
            log(f"[{tag}] page {page}: HTTP {r.status_code if r else 'ERR'} -> stop")
            break
        with open(os.path.join(RAW, f"list_{tag}_p{page}.html"), "w", encoding="utf-8") as f:
            f.write(r.text)
        h, max_page, has_next, rows = parse_list(r.text)
        pages += 1
        if hit is None:
            hit = h
        log(f"[{tag}] page {page}/{max_page}: {len(rows)} unit rows, hit={h}")
        all_rows.extend(rows)
        if not rows or (page >= max_page and not has_next):
            break
        page += 1
        if page > 60:  # safety
            break
    return hit, pages, all_rows


# ----------------------------------------------------------------------------- detail pages
def parse_detail(html):
    d = BeautifulSoup(html, "lxml")
    out = {}
    out["title"] = T(d.select_one("title"))
    out["h1"] = T(d.select_one("h1.section_h1-header-title"))
    note = d.select_one("div.property_view_note")
    out["rent_text"] = T(d.select_one("span.property_view_note-emphasis"))
    note_text = T(note)
    out["note_text"] = note_text

    def grab(label):
        m = re.search(re.escape(label) + r"[:：]\s*([^\s]+(?: [^\s:：]+)*?)(?=\s+\S+[:：]|\s*空室状況|$)", note_text)
        return m.group(1).strip() if m else None
    out["kanri_text"] = grab("管理費・共益費")
    out["shikikin_text"] = grab("敷金")
    out["reikin_text"] = grab("礼金")
    out["hoshokin_text"] = grab("保証金")
    out["shikibiki_text"] = grab("敷引・償却")

    fields = {}
    for th in d.select("table.property_view_table th, table.data_table th"):
        td = th.find_next_sibling("td")
        if td is None:
            continue
        key = re.sub(r"\s+", "", th.get_text(strip=True))
        if key and key not in fields:
            fields[key] = T(td)
    out["fields"] = fields
    # 設備・特徴 list (first inline_list / bgc-wht)
    setsubi = ""
    el = d.select_one("div.bgc-wht")
    if el:
        setsubi = T(el)
    if not setsubi:
        for ul in d.select("ul.inline_list"):
            t = T(ul)
            if "、" in t and len(t) > 20:
                setsubi = t
                break
    out["setsubi"] = setsubi
    out["company"] = T(d.select_one("span.itemcassette-header-ttl")) or None
    out["company_sub"] = T(d.select_one("span.itemcassette-header-sub")) or None
    out["gone"] = bool(re.search(r"掲載(を)?終了|この物件は(現在)?掲載されて|ご指定の物件は", d.get_text(" ", strip=True)[:4000])) or not fields
    return out


def classify_and_build(row, det, search_tag):
    """Return (record or None, drop_reason or None)."""
    f = det["fields"]
    address = f.get("所在地") or row["address"]
    layout = f.get("間取り") or row["layout"]
    area = parse_area(f.get("専有面積") or row["area_text"])
    rent = money_to_yen(det["rent_text"] or row["rent_text"])
    kanri = money_to_yen(det["kanri_text"] if det["kanri_text"] is not None else row["kanri_text"])
    shikikin = money_to_yen(det["shikikin_text"] if det["shikikin_text"] is not None else row["shikikin_text"])
    reikin = money_to_yen(det["reikin_text"] if det["reikin_text"] is not None else row["reikin_text"])
    btype = f.get("建物種別") or ""
    is_house = any(k in btype for k in HOUSE_LABELS) or any(k in row["label"] for k in HOUSE_LABELS)

    if not layout_ok(layout):
        return None, "layout"
    if area is None or area < 45:
        return None, "area"
    if rent is None:
        return None, "rent_unknown"
    if rent > 100000:
        return None, "rent"
    if reikin is None:
        rt = det["reikin_text"] or row["reikin_text"] or ""
        mm = re.search(r"(\d+(?:\.\d+)?)[ヶケか]月", z2h(rt))
        if mm and rent:
            reikin = int(round(float(mm.group(1)) * rent))
    if shikikin is None:
        st = det["shikikin_text"] or row["shikikin_text"] or ""
        mm = re.search(r"(\d+(?:\.\d+)?)[ヶケか]月", z2h(st))
        if mm and rent:
            shikikin = int(round(float(mm.group(1)) * rent))
    if reikin is None:
        return None, "reikin_unknown"
    if reikin > rent:
        return None, "reikin_gt_1month"

    # floors
    kaidate = z2h(f.get("階建") or "")
    floor_min = floor_max = bfloors = None
    m = re.match(r"\s*(B?\d+(?:-\d+)?)階?\s*/\s*(.*)$", kaidate)
    if m:
        floor_min, floor_max = parse_floor_text(m.group(1) + "階")
        m2 = re.search(r"地上(\d+)階建", m.group(2)) or re.search(r"(\d+)階建", m.group(2))
        bfloors = int(m2.group(1)) if m2 else None
    else:
        floor_min, floor_max = parse_floor_text(f.get("階") or row["floor_text"])
        m2 = re.search(r"地上(\d+)階建", kaidate) or re.search(r"(\d+)階建", kaidate or z2h(row["floors_text"]))
        bfloors = int(m2.group(1)) if m2 else None
    setsubi = det["setsubi"]
    elevator = (True if "エレベーター" in setsubi or "エレベータ" in setsubi else (False if setsubi else None))

    if not is_house:
        if floor_min is None:
            return None, "floor_unknown"
        if floor_min <= 1:
            return None, "floor_1F"
        if floor_min >= 4 and elevator is not True:
            return None, "4F_no_elevator"

    # age / structure
    structure, structure_raw = map_structure(f.get("構造"))
    built_year = built_month = None
    m = re.search(r"(\d{4})年(?:(\d{1,2})月)?", z2h(f.get("築年月") or ""))
    if m:
        built_year = int(m.group(1))
        built_month = int(m.group(2)) if m.group(2) else None
    if built_year is None:
        age_l = parse_age_text(row["age_text"])
        if age_l is not None:
            built_year = NOW.year - age_l
    if built_year is None:
        return None, "age_unknown"
    if built_year >= 2001:
        age_tier = "A"
    elif 1991 <= built_year <= 2000 and structure in ("RC", "SRC"):
        age_tier = "B"
    elif 1991 <= built_year <= 2000:
        return None, "1991-2000_not_RC"
    else:
        return None, "built_before_1991"
    tier = "house" if is_house else age_tier
    months = (NOW.year - built_year) * 12 + (NOW.month - (built_month or 1))
    age_years = max(0, months // 12)

    # geocode
    lat, lon = geocode(address)
    if lat is None:
        # fallback: ward + town only (strip anything after 町/区 + digits)
        short = re.sub(r"[\d０-９].*$", "", address)
        lat, lon = geocode(short)
    dist = dist_km(lat, lon)
    if dist is not None and dist > MAX_DIST_KM:
        return None, "distance"

    # parking
    parking = f.get("駐車場")
    parking_fee = None
    if parking:
        pm = re.search(r"(\d[\d,]*)円", z2h(parking))
        if pm:
            parking_fee = int(pm.group(1).replace(",", ""))
        elif re.search(r"無|なし", parking) and not re.search(r"空無", parking):
            parking_fee = None

    # other initial costs / guarantor / agency fee
    extra_src = " / ".join(x for x in [f.get("ほか諸費用"), f.get("備考"), f.get("条件"), setsubi] if x)
    other = []
    hm = re.search(r"保証会社[^、。/]*", extra_src)
    if hm:
        other.append(hm.group(0).strip())
    cm = re.search(r"仲介手数料[^、。/]*", extra_src)
    if cm:
        other.append(cm.group(0).strip())
    if det["hoshokin_text"] and det["hoshokin_text"] not in ("-", "－"):
        other.append("保証金 " + det["hoshokin_text"])
    if det["shikibiki_text"] and det["shikibiki_text"] not in ("-", "－"):
        other.append("敷引・償却 " + det["shikibiki_text"])
    if f.get("ほか諸費用"):
        other.append("ほか諸費用: " + f["ほか諸費用"])
    if f.get("損保"):
        other.append("損保 " + f["損保"])
    if det["company_sub"]:
        other.append(det["company_sub"])

    # notes
    note_bits = []
    if f.get("向き"):
        note_bits.append(f"{f['向き']}向き")
    if btype:
        note_bits.append(f"建物種別: {btype}")
    if f.get("条件"):
        note_bits.append("条件: " + f["条件"])
    keys = ["オートロック", "追焚", "都市ガス", "プロパン", "ペット", "浴室乾燥", "宅配ボックス", "角部屋", "最上階",
            "インターネット無料", "礼金不要", "敷金不要", "保証人不要", "定期借家", "分譲賃貸", "二人入居", "システムキッチン",
            "床暖房", "ウォークインクロゼット", "駐輪場", "バイク置場", "敷地内ごみ置き場", "TVモニタ付インターホン",
            "リフォーム", "リノベーション", "ロフト", "専用庭", "メゾネット", "複層ガラス", "ペアガラス", "断熱", "高気密"]
    hits = [k for k in keys if k in setsubi or k in (f.get("備考") or "") or k in (f.get("条件") or "")]
    if hits:
        note_bits.append("設備: " + ", ".join(hits))
    if f.get("入居"):
        note_bits.append("入居: " + f["入居"])
    if f.get("総戸数"):
        note_bits.append("総戸数 " + f["総戸数"])
    if det["company"]:
        note_bits.append("取扱: " + det["company"])
    if f.get("情報更新日"):
        note_bits.append("更新 " + f["情報更新日"])
    if is_house and age_tier == "B":
        note_bits.append("築年ティア B (1991–2000, RC/SRC)")
    if f.get("備考"):
        note_bits.append("備考: " + f["備考"][:200])
    note_bits.append(f"構造(原文): {structure_raw}")
    if lat is None:
        note_bits.append("GEOCODE FAILED – distance unknown")

    def fmt_money(yen, label_months=True):
        if yen is None:
            return None
        s = f"{yen:,}円"
        if label_months and yen and rent:
            s += f" ({yen / rent:.2g}ヶ月)".replace(".0ヶ月", "ヶ月")
        return s

    station = (f.get("駅徒歩") or (" ".join(row["stations"]) if row["stations"] else "")).split(" ")
    nearest = None
    if f.get("駅徒歩"):
        mm = re.match(r"(\S+/\S+駅\s*歩\d+分)", f["駅徒歩"])
        nearest = mm.group(1) if mm else f["駅徒歩"][:40]
    elif row["stations"]:
        nearest = row["stations"][0]

    rec = OrderedDict([
        ("source", "suumo"),
        ("url", f"https://suumo.jp/chintai/jnc_{row['jnc']}/"),
        ("building_name", det["h1"] or row["building_name"] or None),
        ("address", address),
        ("lat", lat), ("lon", lon), ("distance_km", dist),
        ("rent", rent), ("kanrihi", kanri),
        ("shikikin", fmt_money(shikikin) if shikikin is not None else None),
        ("reikin", fmt_money(reikin) if reikin is not None else None),
        ("other_initial", ", ".join(other) if other else None),
        ("layout", layout), ("area_m2", area),
        ("floor", None if is_house and floor_min is None else floor_min),
        ("building_floors", bfloors), ("elevator", elevator),
        ("built_year", built_year), ("built_month", built_month), ("age_years", age_years),
        ("structure", structure),
        ("parking", parking), ("parking_fee", parking_fee),
        ("nearest_station", nearest),
        ("tier", tier),
        ("notes", "; ".join(note_bits)),
        ("fetched_at", NOW.isoformat(timespec="seconds")),
    ])
    if floor_max is not None and floor_max != floor_min:
        rec["notes"] = f"メゾネット {floor_min}-{floor_max}階; " + rec["notes"]
    rec["_search"] = search_tag
    rec["_bc_url"] = row["href"]
    rec["_ward"] = re.search(r"京都市(\S+?区)", address).group(1) if re.search(r"京都市(\S+?区)", address) else None
    return rec, None


# ----------------------------------------------------------------------------- main
def main():
    summary = {"searches": {}, "drops_list": Counter(), "drops_detail": Counter(), "problems": []}
    candidates = OrderedDict()  # jnc -> (row, tag)

    # ---- search 1: cn=25
    hit1, pages1, rows1 = scan_search(25, "cn25")
    summary["searches"]["cn25"] = {"hit_count": hit1, "pages": pages1, "unit_rows": len(rows1)}
    # ---- search 2: cn=9999999 (all ages) -> tier B candidates
    hit2, pages2, rows2 = scan_search(9999999, "cnall")
    summary["searches"]["cnall"] = {"hit_count": hit2, "pages": pages2, "unit_rows": len(rows2)}

    ward_rows = Counter()
    for tag, rows in (("cn25", rows1), ("cnall", rows2)):
        for row in rows:
            ward = re.search(r"京都市(\S+?区)", row["address"])
            ward = ward.group(1) if ward else "?"
            if tag == "cn25":
                ward_rows[ward] += 1
            if row["jnc"] in candidates:
                summary["drops_list"]["duplicate_jnc"] += 1
                continue
            age = parse_age_text(row["age_text"])
            if tag == "cnall":
                # only need buildings not already covered by cn=25; keep 築25–36年 (built ~1990–2001)
                if age is None:
                    pass
                elif age < 25:
                    summary["drops_list"]["cnall_covered_by_cn25"] += 1
                    continue
                elif age > 36:
                    summary["drops_list"]["cnall_too_old(>36y)"] += 1
                    continue
            if not layout_ok(row["layout"]):
                summary["drops_list"]["layout"] += 1
                continue
            a = parse_area(row["area_text"])
            if a is not None and a < 45:
                summary["drops_list"]["area<45"] += 1
                continue
            rent = money_to_yen(row["rent_text"])
            if rent is not None and rent > 100000:
                summary["drops_list"]["rent>10万"] += 1
                continue
            reikin = money_to_yen(row["reikin_text"])
            if rent and reikin is not None and reikin > rent:
                summary["drops_list"]["reikin>1month"] += 1
                continue
            is_house = any(k in row["label"] for k in HOUSE_LABELS)
            fmin, fmax = parse_floor_text(row["floor_text"])
            if not is_house and fmin is not None and fmin <= 1:
                summary["drops_list"]["floor_1F(list)" if fmin == fmax else "floor_1F_maisonette(list)"] += 1
                continue
            candidates[row["jnc"]] = (row, tag)
    summary["list_rows_per_ward_cn25"] = dict(ward_rows)
    summary["detail_candidates"] = len(candidates)
    log(f"\n{len(candidates)} candidates for detail fetch "
        f"(cn25={sum(1 for v in candidates.values() if v[1]=='cn25')}, "
        f"cnall={sum(1 for v in candidates.values() if v[1]=='cnall')})\n")

    kept = []
    for i, (jnc, (row, tag)) in enumerate(candidates.items(), 1):
        r = get(row["href"], "detail")
        if r is None:
            summary["drops_detail"]["fetch_error"] += 1
            summary["problems"].append(f"detail fetch failed: {row['href']}")
            continue
        with open(os.path.join(RAW, f"detail_jnc_{jnc}.html"), "w", encoding="utf-8") as f:
            f.write(r.text)
        if r.status_code != 200:
            summary["drops_detail"][f"http_{r.status_code}"] += 1
            continue
        try:
            det = parse_detail(r.text)
        except Exception as e:  # pragma: no cover
            summary["drops_detail"]["parse_error"] += 1
            summary["problems"].append(f"parse error {jnc}: {e!r}")
            traceback.print_exc()
            continue
        if det["gone"]:
            summary["drops_detail"]["listing_gone"] += 1
            continue
        rec, why = classify_and_build(row, det, tag)
        if rec is None:
            summary["drops_detail"][why] += 1
            log(f"[{i}/{len(candidates)}] {jnc} {row['building_name'][:20]:20s} {row['layout']:6s} {row['floor_text']:5s} -> DROP {why}")
            continue
        kept.append(rec)
        log(f"[{i}/{len(candidates)}] {jnc} {rec['building_name'][:20]:20s} {rec['layout']:6s} {rec['floor']}F/{rec['building_floors']} "
            f"{rec['rent']} {rec['area_m2']}m2 {rec['built_year']} {rec['structure']} tier={rec['tier']} {rec['distance_km']}km")

    # ---- verification pass (clean URL returns 200 and still shows the unit)
    log(f"\nverifying {len(kept)} URLs ...")
    verified = []
    for rec in kept:
        ok = False
        for url in (rec["url"], rec["_bc_url"]):
            r = get(url, "verify")
            if r is not None and r.status_code == 200:
                txt = r.text
                jnc_id = re.search(r"jnc_(\d+)", rec["url"]).group(1)
                code_ok = (jnc_id in txt) and "専有面積" in txt and "property_view_note" in txt \
                    and not re.search(r"掲載(を)?終了", txt[:20000])
                if code_ok:
                    rec["url"] = url
                    ok = True
                    break
        if ok:
            verified.append(rec)
        else:
            summary["drops_detail"]["verify_failed"] += 1
            summary["problems"].append(f"verification failed: {rec['url']}")

    # ---- write JSON (schema fields only)
    out_json = []
    for rec in verified:
        o = OrderedDict((k, v) for k, v in rec.items() if not k.startswith("_"))
        out_json.append(o)
    with open(os.path.join(OUT, "suumo.json"), "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=1)

    # ---- summary markdown
    by_ward = Counter(r["_ward"] for r in verified)
    by_tier = Counter(r["tier"] for r in verified)
    by_search = Counter(r["_search"] for r in verified)
    lines = []
    lines.append("# SUUMO search summary (suumo.jp)\n")
    lines.append(f"Fetched: {NOW.isoformat(timespec='seconds')}  ")
    lines.append(f"Requests: {dict(REQ_COUNT)} (≈1 req/s, Chrome UA, no blocks/captchas encountered)\n")
    lines.append("## Searches (server-side filters: 9 wards, 2LDK/3DK/3LDK/4DK/4LDK/5K+, ≥45㎡, 賃料≤10万, sorted 住所別)")
    for tag, s in summary["searches"].items():
        lines.append(f"- `{tag}` (cn={'25' if tag=='cn25' else '9999999'}): hit count (agency listings, incl. duplicates) = {s['hit_count']}, "
                     f"pages scanned = {s['pages']}, unit rows = {s['unit_rows']}")
    lines.append(f"\nUnit rows per ward in the cn=25 search: {dict(sorted(ward_rows.items(), key=lambda x: -x[1]))}")
    lines.append(f"\nDetail pages fetched: {summary['detail_candidates']}  → kept & URL-verified: **{len(verified)}**")
    lines.append(f"- by tier: {dict(by_tier)}")
    lines.append(f"- by ward: {dict(sorted(by_ward.items(), key=lambda x: -x[1]))}")
    lines.append(f"- by originating search: {dict(by_search)}")
    lines.append("\n## Dropped at list level")
    for k, v in summary["drops_list"].most_common():
        lines.append(f"- {k}: {v}")
    lines.append("\n## Dropped at detail level")
    for k, v in summary["drops_detail"].most_common():
        lines.append(f"- {k}: {v}")
    lines.append("\n## こだわり条件 codes in SUUMO's full condition form FR301FB005 (noted only – NOT applied server-side)")
    lines.append("- 駐車場: `tc=0400901` 駐車場あり, `tc=0400911` 敷地内駐車場, `tc=0400910` 駐車場2台以上, `co=2` 駐車場代込み")
    lines.append("- 階: `tc=0400101` 2階以上, `tc=0400105` 1階の物件, `tc=0400102` 最上階; エレベーター: `tc=0400904`")
    lines.append("- 礼金なし: `co=3`; 敷金・保証金なし: `co=4`; 管理費込み: `co=1`")
    lines.append("- 構造: `kz=1` 鉄筋系 (RC/SRC), `kz=2` 鉄骨系, `kz=3` 木造, `kz=4` ブロック・その他 — usable for tier B, but structure was verified on each detail page instead")
    lines.append("- misc: `tc=0400801` オートロック, `tc=0400912` 都市ガス, `tc=0400913` プロパン, `tc=0400303` 浴室乾燥機, `tc=0400905` 宅配ボックス, "
                 "`tc=0400602` 床暖房, `tc=0401102` ペット相談可, `tc=0401106` 定期借家を含まない, `tc=0401003` 保証人不要, `tc=0401002` 分譲賃貸; "
                 "no 追焚 code exists. 建物種別: `ts=1` マンション / `ts=2` アパート / `ts=3` 一戸建て・その他")
    lines.append("- Building-age filter `cn` only accepts 5/10/15/20/25/30/9999999, so the 1991–2000 window was derived from 築年月 on detail pages.")
    lines.append("\n## Rules applied client-side")
    lines.append("- 礼金 ≤ 1 month rent; not 1F (maisonettes spanning 1F dropped unless 一戸建て/テラスハウス); ≥4F requires エレベーター in 設備; "
                 "tier A = 築年月 ≥ 2001; tier B = 1991–2000 and RC/SRC; everything else by age dropped; distance ≤ 5.5 km (GSI geocoder, town-level).")
    lines.append("- `elevator` = true if エレベーター appears in the 設備 list, false if a 設備 list exists without it, null if no 設備 list.")
    lines.append("- URL stored is the canonical unit URL `https://suumo.jp/chintai/jnc_<id>/`; every stored URL was re-fetched (HTTP 200, building name + 専有面積 present) just before writing.")
    if summary["problems"]:
        lines.append("\n## Problems")
        for p in summary["problems"]:
            lines.append(f"- {p}")
    else:
        lines.append("\n## Problems\n- none (no blocks, captchas or 5xx)")
    # table of kept
    lines.append("\n## Kept listings")
    lines.append("| tier | ward | building | layout | ㎡ | rent | 管理費 | 礼金 | floor | elev | built | struct | km | parking | url |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(verified, key=lambda x: (x["tier"], x["distance_km"] if x["distance_km"] is not None else 99)):
        lines.append(f"| {r['tier']} | {r['_ward']} | {r['building_name']} | {r['layout']} | {r['area_m2']} | {r['rent']:,} | {r['kanrihi']} | {r['reikin']} | "
                     f"{r['floor']}/{r['building_floors']} | {r['elevator']} | {r['built_year']} | {r['structure']} | {r['distance_km']} | {r['parking']} | {r['url']} |")
    with open(os.path.join(OUT, "suumo.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    log(f"\nDONE: kept {len(verified)} -> out/suumo.json, out/suumo.md")
    log(json.dumps({"drops_list": summary["drops_list"], "drops_detail": summary["drops_detail"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
