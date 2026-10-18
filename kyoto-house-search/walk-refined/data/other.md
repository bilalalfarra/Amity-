# other — small agencies' own sites, WALK3 survey (≤3.0 km of 左京区吉田河原町14, rent ≤ 14万, 2LDK+, ≥45 m²), fetched 2026-10-18

## Sources used (script: walk3/other_walk.py; every kept URL fetched in this run, HTTP 200)
- **八清 (hachise.jp)** — 京町家 / 戸建 specialist. Rental list `https://www.hachise.jp/rent/list/index.html` (one page; `li.property` items carry `filter-use-live` and `filter-area-<ward>` classes). Residential items in 北/上京/左京/中京/東山/下京 with 居住用賃料 ≤ 14万, 2LDK+ (町家 layouts like 3DK＋お庭 / 5K count) and ≥ 45 m², ≤ 3.25 km by town geocode → unit pages. Most 八清 houses are > 14万 or 1–2DK (see out/raw/other/dropped.json). 築年 is often 「築不詳」 → built_year null (record in notes).
- **三井のリハウス (rehouse.co.jp/rent)** — 分譲賃貸. Ward lists `/rent/area/prefecture/26/city/<code>/` (北区 0, 上京区 3, 左京区 4, 中京区 21, 東山区 1, 下京区 17 listings); almost all are > 14万; the ≤ 14万 2LDK+ ones were opened (lat/lon from the page).

## Not used
- エリッツ, 長栄, 京都R不動産: blocked in the first run (proxy 502 / HTTP 403) — skipped as instructed. at home skipped (CAPTCHA last time). ハウスメイト: no stock in the area in the first run.

## Result
- **Kept 4 units** (after merging 0 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via the same building name in another listing with a full address, 0 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 1; rent range kept: 130000–138000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'house': 2, 'B': 2}; 礼金 ≤1ヶ月 2, >1ヶ月 2, unknown 0 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'town': 1, 'site': 2, 'address (GSI)': 1} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 2/0/2; by ward: {'左京区': 1, '中京区': 2, '上京区': 1}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/other/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.7 | 吉田近衛町の京町家（京都市左京区吉田近衛町） | 5K | 102.3 | 130,000 | None | 130,000円 / 130,000円 | 1.0 | None/2 | ? | None/None | 木造 | 駐輪スペース／駐車スペース: 無／無 | house | https://www.hachise.jp/rent/71507/index.html |
| 2.24 | ライオンズマンション二条城東 | 3SDK | 61.07 | 138,000 | 0 | 13.8万円 / 13.8万円 | 1.0 | 10/11 | Y | 1991/2 | SRC | - | B | https://www.rehouse.co.jp/rent/bkdetail/4YL26067/ |
| 2.8 | 藤和シティホームズ三条堀川 | 2LDK | 58.72 | 135,000 | 10000 | 1ヶ月 / 2ヶ月 | 2.0 | 6/11 | Y | 1997/3 | RC | 無 | B | https://www.rehouse.co.jp/rent/bkdetail/4YL26147/ |
| 2.93 | 北野の改装済京町家（京都市上京区若松町） | 3DK | 58.06 | 130,000 | None | 居住用 130,000円 / 居住兼事務 / 居住用 143,000円 / 居住兼事務 | 1.1 | None/2 | ? | None/None | 木造 | 駐輪・駐車: 無 | house | https://www.hachise.jp/rent/70568/index.html |
