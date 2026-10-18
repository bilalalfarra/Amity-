# flat — フラットエージェンシー (flat-a.co.jp → flat.chintai-kyoto.jp), WALK3 survey (≤3.0 km, rent ≤ 14万, 2LDK+, ≥45 m²), fetched 2026-10-18

## Method (walk3/flat_walk.py, copy of walk/flat_walk.py)
- The site's own search API `GET /wp-json/wp/v2/get_search_result` (same parameters as its search page) per ward 北/上京/左京/中京/東山/下京 with
  `house_plan_summary_code[]=203,301,302,303,401,402,403,599&occupied_area_from=45.0&price_to=140000` (2LDK+, ≥45 m², 賃料 ≤ 14万).
- Addresses carry block numbers → GSI geocode (通り名 stripped) with a 3.2 km margin; unit pages `/rent/<kokoku id>/` fetched (HTTP 200); final distance from the page's map coordinates; 駐車場 cell copied verbatim.
- Rooms hidden behind 「残りN件を表示」 are not expanded (the site's hit count is per room, a few more than the links shown).

## Result
- **Kept 11 units** (after merging 0 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via the same building name in another listing with a full address, 0 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 2; rent range kept: 82000–140000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'old': 3, 'house': 3, 'B': 3, 'A': 2}; 礼金 ≤1ヶ月 7, >1ヶ月 4, unknown 0 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'site': 11} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 4/0/7; by ward: {'上京区': 3, '左京区': 5, '北区': 1, '東山区': 1, '中京区': 1}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/flat/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.62 | ベルメゾン鴨川 206 | 2LDK | 48.6 | 95,000 | 7000 | 1ヶ月 / 100,000円 | 1.05 | 2/3 | ? | 1988/9 | RC | 状況：空無 価格：22,000円 〜 特徴：駐輪 | old | https://flat.chintai-kyoto.jp/rent/902000000001827866/ |
| 0.99 | 京都グランドハイツ 411 | 2LDK | 64.5 | 140,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 4/7 | Y | 1971/6 | RC | 状況：空無 特徴：駐輪場有り、バイク置き場有り | old | https://flat.chintai-kyoto.jp/rent/1130674537890000387276/ |
| 1.56 | 出雲路俵町貸家 ｶｼﾔ | 4DK | 66.21 | 93,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | ? | 1979/1 | 木造 | 状況：有（敷地内） 価格：駐車場無料 特徴：自走 | house | https://flat.chintai-kyoto.jp/rent/1130674537890000399506/ |
| 1.94 | マナーハウス A-106 | 2LDK | 62.31 | 115,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/4 | Y | 1996/1 | RC | 状況：近隣駐車場 距離：10m 価格：23,00 | B | https://flat.chintai-kyoto.jp/rent/1130674537890000320504/ |
| 2.02 | 北白川西伊織町貸家(平屋) ｶｼﾔ | 5K | 82.64 | 82,000 | 0 | 1ヶ月 / 120,000円 | 1.46 | 1/1 | ? | 1933/1 | 木造 | 状況：無 特徴：駐輪場有り、バイク置き場有り | house | https://flat.chintai-kyoto.jp/rent/902000000001835132/ |
| 2.15 | 北白川上終町貸家 ｶｼﾔ | 5DK | 99.68 | 100,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | ? | 1973/9 | 軽量鉄骨 | 状況：無 | house | https://flat.chintai-kyoto.jp/rent/1130674537890000324615/ |
| 2.57 | ハイツ白川 317 | 3LDK | 70.69 | 90,000 | 10000 | 0円 / 0円 | 0.0 | 3/9 | Y | 1976/2 | RC | 状況：要問合せ 価格：12,400円 〜 20, | old | https://flat.chintai-kyoto.jp/rent/1130674537890000353036/ |
| 2.73 | ペレニアルフラックス 201 | 2LDK | 75.5 | 120,000 | 6000 | 1ヶ月 / 1ヶ月 | 1.0 | 2/3 | ? | 1992/8 | RC | 状況：有（敷地内） 価格：15,400円 〜 特 | B | https://flat.chintai-kyoto.jp/rent/902000000001827907/ |
| 2.83 | Weaving House Ⅱ 303 | 2LDK | 56.2 | 125,000 | 6000 | 1ヶ月 / 1.5ヶ月 | 1.5 | 3/3 | ? | 2027/2 | 木造 | 状況：有（敷地内） 1台空きあり 価格：16,5 | A | https://flat.chintai-kyoto.jp/rent/1130674537890000405497/ |
| 2.83 | Weaving House Ⅱ 203 | 2LDK | 56.2 | 125,000 | 6000 | 1ヶ月 / 1.5ヶ月 | 1.5 | 2/3 | ? | 2027/2 | 木造 | 状況：有（敷地内） 2台空きあり 価格：16,5 | A | https://flat.chintai-kyoto.jp/rent/1130674537890000405498/ |
| 2.85 | 嶋津マンション 403 | 3LDK | 60.0 | 125,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 4/7 | Y | 1991/7 | RC | 状況：空無 価格：23,000円 〜 特徴：駐輪 | B | https://flat.chintai-kyoto.jp/rent/1130674537890000352535/ |
