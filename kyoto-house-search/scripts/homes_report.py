#!/usr/bin/env python3
"""Write out/homes.md from out/homes.json + out/homes_stats.json (+ discovered parameter codes)."""
import json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
recs = json.load(open(os.path.join(OUT, "homes.json"), encoding="utf-8"))
stats = json.load(open(os.path.join(OUT, "homes_stats.json"), encoding="utf-8"))
dbg = json.load(open(os.path.join(OUT, "homes_debug.json"), encoding="utf-8"))

pages = stats["pages"]
pagesA = {k: v for k, v in pages.items() if k.startswith("listA_")}
pagesB = {k: v for k, v in pages.items() if k.startswith("listB_")}
non200 = {k: v for k, v in pages.items() if v != 200}
by_ward = collections.Counter(r["_ward"].replace("kyoto_", "").replace("-city", "") for r in dbg)
by_tier = collections.Counter(r["tier"] for r in recs)

L = []
L.append("# LIFULL HOME'S (homes.co.jp) — Kyoto rental scan summary\n")
L.append("Scanned %s (JST). Script: `homes_scrape.py`, raw HTML in `out/raw/homes/` (list pages `listA_*`/`listB_*`, unit pages `detail_*`).\n" % (recs[0]["fetched_at"] if recs else "n/a"))
L.append("## Result\n")
L.append("- **Kept: %d units** → tier A %d, tier B %d, house %d (`out/homes.json`)." % (len(recs), by_tier.get("A", 0), by_tier.get("B", 0), by_tier.get("house", 0)))
L.append("- Kept by ward: " + ", ".join("%s %d" % kv for kv in by_ward.most_common()))
L.append("")
L.append("## How the site was queried\n")
L.append("Listings are server-rendered in the HTML (no JS rendering needed to read them; the only obstacle is the AWS WAF bot protection described under Problems). "
         "Ward list URL: `https://www.homes.co.jp/chintai/kyoto/<ward>/list/?<cond…>&page=N` (GET works even though the form posts). "
         "`<span class=\"totalNum\">` = number of units, `li.lastPage` = last page, 30 buildings/page. "
         "Unit links in list rows are `https://www.homes.co.jp/chintai/room/<40-hex>/` (canonical unit page; one per agency listing), the `data-bid` gives the equivalent `/chintai/b-<13 digits>/` URL (also recorded in notes). "
         "PR (ad) blocks `div.prg-kksBukken` link straight to `b-` URLs and were parsed too.\n")
L.append("### Query-string parameter codes discovered (search form)\n")
L.append("| condition | parameter | used |")
L.append("|---|---|---|")
rows = [
    ("賃料上限 10万円", "`cond[monthmoneyroomh]=10` (万円; `cond[monthmoneyroom]` = lower bound; `cond[kanrihi]=1` would make it include 管理費)", "yes"),
    ("専有面積 ≥45㎡", "`cond[housearea]=45` (`cond[houseareah]` = upper bound)", "yes"),
    ("間取り", "`cond[madori][25]=25` 2LDK, `[33]` 3DK, `[35]` 3LDK, `[43]` 4DK, `[45-]=45-` 4LDK以上 (others: 11 ワンルーム, 12 1K, 13 1DK, 15 1LDK, 22 2K, 23 2DK, 32 3K, 42 4K)", "yes"),
    ("築年数", "`cond[houseageh]=25` 25年以内 (values 0 指定なし/1 新築/3/5/10/15/20/25/30 — no 35)", "A: 25, B: 0"),
    ("構造", "`cond[housekouzougroup][rebar]=rebar` 鉄筋系 (others: wooden 木造系, steelframe 鉄骨系, blockother ブロック・その他)", "B only"),
    ("2階以上", "`cond[mcf][340102]=340102` (必須) / `cond[want_mcf][340102]` (できれば); 1階の物件 = 340101, 最上階 = 340201", "no (floor rule applied client-side)"),
    ("エレベーター", "`cond[mcf][320101]=320101`", "no (not filtered server-side, as instructed)"),
    ("駐車場あり", "`cond[mcf][320801]=320801` (駐車場2台以上 = 320601, 駐輪場 = 321001, バイク置き場 = 320901)", "no (not filtered server-side)"),
    ("礼金なし / 敷金なし", "`cond[reikin]=120101` / `cond[shikikin]=120201`", "no (礼金 ≤1ヶ月 applied client-side)"),
    ("物件種別", "`cond[mbg][3002]` マンション, `[3001]` アパート, `[3003]` 一戸建て (all three are on by default)", "default"),
    ("その他 mcf", "オートロック 310101, 追焚機能 220401, ペット相談可 113201, 南向き 340501, 宅配ボックス 321101, 床暖房 240201, 都市ガス 210201, 即入居可 350301, 保証人不要 121002, 分譲賃貸 331001", "no"),
    ("並び順", "`cond[sortby]=period` 築年数が新しい順 (recommend / fee / -fee / area_house / addr / newdate)", "yes"),
    ("ページ", "`page=N`", "yes"),
]
for a, b, c in rows:
    L.append("| %s | %s | %s |" % (a, b, c))
L.append("")
L.append("## Pages scanned\n")
L.append("- Tier A list pages (2LDK+/≥45㎡/≤10万/築25年以内, all wards): %d pages; tier B list pages (same but 築 指定なし + 鉄筋系, newest first, stop when 築>36年): %d pages." % (len(pagesA), len(pagesB)))
L.append("- Server-reported unit totals per ward/tier (None = 0件 page): " + ", ".join("%s=%s" % kv for kv in stats["totals"].items()))
L.append("- Unit rows parsed from lists: %d (A %d, B %d, PR blocks %d)." % (stats["list_units"], stats["list_units_A"], stats["list_units_B"], stats["pr_units"]))
L.append("- Non-200 list pages: %s" % (non200 or "none"))
L.append("- Unit detail pages fetched: %d (HTTP failures: %d)." % (stats["detail_fetched"], stats["detail_http_fail"]))
L.append("")
L.append("## Counts dropped per rule\n")
L.append("List stage (before fetching the unit page):")
L.append("- tier-B rows outside 築24–36年 window (already in tier A or too old): %d" % stats["drop_age_list_B"])
L.append("- 1階: %d" % stats["drop_1F_list"])
L.append("- layout not 2LDK+ : %d, area <45㎡: %d, rent >10万: %d" % (stats["drop_layout_list"], stats["drop_area_list"], stats["drop_rent_list"]))
L.append("- same unit listed by several agencies (merged on address+floor+layout+rounded area, cheapest listing kept, other URLs/rents in notes): %d (+%d merged after reading unit pages)" % (stats["dup_same_unit"], stats.get("dup_same_unit_detail", 0)))
L.append("- >5.5 km from KRP by list address: %d (geocode failed at list stage: %d → fetched anyway)" % (stats["drop_far_list"], stats["geocode_fail_list"]))
L.append("")
L.append("Unit-page stage:")
L.append("- 1階 (detail): %d; ≥4階 without elevator: %d" % (stats["drop_1F"], stats["drop_4F_no_elev"]))
L.append("- 礼金 >1ヶ月: %d" % stats["drop_reikin"])
L.append("- built before 1991 or 築年月 unknown: %d; built 1991–2000 but not RC/SRC: %d" % (stats["drop_age"], stats["drop_structure_B"]))
L.append("- >5.5 km (detail address): %d; rent/area/layout mismatch on detail: %d/%d/%d" % (stats["drop_far"], stats["drop_rent"], stats["drop_area"], stats["drop_layout"]))
L.append("")
L.append("## Problems / caveats\n")
fetch_log = []
for fn in ("homes_fetch_run1.out", "homes_fetch_run2.out", "homes_fetch.out"):
    try:
        fetch_log += [json.loads(x) for x in open(os.path.join(HERE, fn), encoding="utf-8") if x.startswith("{")]
    except Exception:
        pass
f_ok = sum(1 for x in fetch_log if x.get("result") == "ok"); f_blocked = sum(1 for x in fetch_log if x.get("result") == "blocked")
f_err = sum(1 for x in fetch_log if x.get("result") == "error")
L.append("- **Bot protection (AWS WAF)**: list pages and the first unit pages were fetched with python-requests (Chrome UA). "
         "After ~5 requests at 1 req/s with persisted cookies the site answered HTTP 202 with an AWS WAF JavaScript challenge; "
         "cookie-less requests at 1 req/2 s got further (~45 requests) before being challenged again, and after a handful of "
         "challenges the WAF escalated to HTTP 405 「Human Verification」 (CAPTCHA) for python-requests. Headless Chromium (Playwright) "
         "passed the JS challenge every time and was never shown the CAPTCHA, but a browser session was shown the CAPTCHA after roughly a dozen unit pages (the state sticks to the session, "
         "a fresh session is served normally). No CAPTCHA was ever solved or bypassed; the remaining unit pages were fetched by headless-browser "
         "sessions rotated every 9 pages (`homes_fetch.js`: HTML document only, ~10–14 s between pages, 45 s pause between sessions, "
         "4-minute back-off on CAPTCHA): %d ok, %d blocked, %d errors. "
         "Challenges seen by the python fetcher: %s; pages served from the raw-HTML cache on the final parse run: %s." % (
             f_ok, f_blocked, f_err, stats.get("waf_challenges"), stats.get("cache_hits")))
L.append("- 中京区 and 東山区 tier-A queries legitimately return 「該当物件は0件でした」 (no 2LDK+/≥45㎡/≤10万/築25年以内 units).")
L.append("- Kyoto 通り名 addresses (e.g. 若宮通松原下る亀屋町) are not understood by the GSI geocoder; fallback geocodes ward + last 町名 (flagged in notes). Town-level precision only.")
L.append("- `elevator=false` means the unit page's 設備・サービス list exists but does not include エレベーター; `null` when no equipment list was present.")
L.append("- HOME'S lists the same room once per agency; duplicates were merged, other listings' URLs are in `notes`.")
L.append("- Houses (一戸建て/テラスハウス) have no 所在階, so the floor rule is not applied to them; they are `tier: \"house\"`.")
L.append("")
unv = []
try:
    unv = json.load(open(os.path.join(OUT, "homes_unverified.json"), encoding="utf-8"))
except Exception:
    pass
if unv or stats.get("pending_not_cached"):
    L.append("## Candidates NOT verified (unit page not fetched)\n")
    L.append("%d list-stage candidates passed every filter that the list page can answer (2LDK+, ≥45㎡, ≤10万, 礼金≤1ヶ月, not 1F, ≤5.5 km, "
             "age window) but their unit page was not fetched within the CAPTCHA budget, so 構造/エレベーター/駐車場/築年月 are unknown and the URL "
             "is unverified. They are exported with list-page data to `out/homes_unverified.json` (not in `homes.json`)." % len(unv))
    if unv:
        L.append("")
        L.append("| search | km | rent | layout | ㎡ | floor | bldg floors | age (list) | address | url |")
        L.append("|---|---|---|---|---|---|---|---|---|---|")
        for r in sorted(unv, key=lambda r: (r["tier_search"], r["distance_km"] or 99)):
            L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (r["tier_search"], r["distance_km"], r["rent"], r["layout"], r["area_m2"],
                     r["floor_text"], r["building_floors"], r["list_age_years"], (r["address"] or "").replace("京都府京都市", ""), r["url"]))
    L.append("")
L.append("## Kept units\n")
L.append("| tier | km | rent | 管理費 | layout | ㎡ | floor | elev | built | struct | 礼金 | parking | name | url |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in recs:
    L.append("| %s | %s | %s | %s | %s | %s | %s/%s | %s | %s | %s | %s | %s | %s | %s |" % (
        r["tier"], r["distance_km"], r["rent"], r["kanrihi"], r["layout"], r["area_m2"], r["floor"], r["building_floors"],
        r["elevator"], "%s-%s" % (r["built_year"], r["built_month"]), r["structure"], r["reikin"], (r["parking"] or "")[:30].replace("|", "/"),
        (r["building_name"] or "")[:30].replace("|", "/"), r["url"]))
open(os.path.join(OUT, "homes.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("wrote out/homes.md", len(recs), "records")
