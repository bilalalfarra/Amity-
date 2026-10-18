# athome — at home (athome.co.jp), WALK survey (≤1.3 km of 左京区吉田河原町14), fetched 2026-10-18

## Method (deliberately minimal: the site showed an Imperva puzzle CAPTCHA after ~4 pages on 2026-10-01)
- Plain requests, Chrome UA, **25 s between requests**, hard budget of 8 requests, stop at the first non-200 / CAPTCHA page (no retries, no workarounds).
- List = station search (format `/chintai/kyoto/<station>-st/list/`, found in the site's route code) for the two stations next to the office, page 1 only:
  `?basic=kc001,kc138,ke005,kn001,kt007,ki002,kj001,km010,km014,km015,km018,km019,km021&q=1&sort=33&limit=30`
  (賃料 下限/上限なし, 駅徒歩15分以内, 築年数指定なし, 45㎡以上, 定期借家含む, 2LDK/3DK/3LDK/4K/4DK/4LDK以上).
  出町柳: 736 rooms / 125 buildings on the site (52 rooms on page 1); 神宮丸太町: 534 rooms / 124 buildings (59 on page 1). Raw: out/raw/athome/list_*.html.gz.
- The 100 rooms seen: 99 within ~1.6 km by town geocode; 83 of them match a unit already in walk/out (same area + rent from SUUMO/CHINTAI/スマイティ/エイブル/eheya/Yahoo/京都ライフ…), 16 listings (≈6 physical units, all 1.3–1.55 km by town centroid) were new → their unit pages were fetched one per physical unit, nearest first, until the budget or a block.
- Coverage is therefore only the first page of each station list (~8 % of the station results); the rest of at home was not crawled on purpose.
- **Block hit, run stopped**: requests 1–7 (2 list pages + 5 unit pages, 25 s apart) were normal; request 8 (unit page https://www.athome.co.jp/chintai/1105074624/, 出雲路俵町貸家) returned the 8 KB Imperva interstitial 「【アットホーム】認証中」 (raw: out/raw/athome/detail_1105074624.html.gz). Stopped immediately — no retry, no CAPTCHA solving, no workaround. Unit pages not fetched: 出雲路俵町貸家 4DK 66.21 m² 9.3万 (北区, ~1.5 km by town).
- Of the 5 unit pages read, only 京都市中京区 堺町通竹屋町下る絹屋町 5F 3LDK (1.29 km by at home's map pin) is ≤ 1.3 km; ジオエント御所北寺町通 (1.45), 北小路室町 3LDK (1.47), コスモ下鴨リバーステージ / 高野清水町 3LDK (1.42–1.43) are farther.
- `parking` = the 費用 table's 駐車場 cell (e.g. 「有 33,000円/月」); the feature tag (駐車・駐輪) is kept in notes.

## Result
- **Kept 1 units** (after merging 0 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via the same building name in another listing with a full address, 0 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 0; rent range kept: 225000–225000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'old': 1}; 礼金 ≤1ヶ月 0, >1ヶ月 1, unknown 0 (no 礼金 limit in this survey).
- Elevator yes/no/unknown: 1/0/0; by ward: {'中京区': 1}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/athome/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.29 | 京都市中京区 堺町通竹屋町下る絹屋町（丸太町 | 3LDK | 86.14 | 225,000 | 20000 | なし / 30万円 | 1.33 | 5/6 | Y | 1989/9 | RC | 有 33,000円/月 | old | https://www.athome.co.jp/chintai/1181434319/ |
