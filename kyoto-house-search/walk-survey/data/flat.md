# flat — フラットエージェンシー (flat-a.co.jp → rental search flat.chintai-kyoto.jp), WALK survey (≤1.3 km of 左京区吉田河原町14), fetched 2026-10-18

## Method
- The site's own search page loads its results from `GET /wp-json/wp/v2/get_search_result` with the page's `localize.searchParams`; called the same way per ward:
  `rent_or_sale=rent&area_or_line=area&pref=26&city[]=<103|102|104>&address[]=京都府京都市<ward>&house_plan_summary_code[]=203,301,302,303,401,402,403,599&occupied_area_from=45.0` (2LDK, 3K/3DK/3LDK, 4K/4DK/4LDK, 5K以上; ≥45 m²).
- Site hit counts (rooms): 左京区 23, 上京区 6, 中京区 8 → 4 result pages (raw: out/raw/flat/list/), 34 unit links. Addresses include block numbers → geocoded (通り名 stripped) with a 1.5 km margin → 4 candidates.
- Unit pages `/rent/<kokoku id>/` all HTTP 200 (raw: out/raw/flat/detail/); final distance from the map coordinates in the page. 駐車場 cell copied verbatim; elevator from the エレベーター cell / 設備 text.
- 2 中京区 rooms hidden behind 「残りN件を表示」 were not expanded (their buildings are at 四条烏丸 / 新町三条, > 2 km).

## Result
- **Kept 4 units** (after merging 0 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via nearest station (noted in `notes`), 0 of them dropped as >1.3 km.
- Within 1.0 km: 3; rent range kept: 95000–250000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'house': 2, 'old': 2}; 礼金 ≤1ヶ月 2, >1ヶ月 2, unknown 0 (no 礼金 limit in this survey).
- Elevator yes/no/unknown: 1/0/3; by ward: {'左京区': 3, '上京区': 1}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/flat/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.34 | 吉田上阿達町貸家(7-19) 7-19 | 3LDK | 101.65 | 250,000 | 0 | 1ヶ月 / 1.5ヶ月 | 1.5 | 1/2 | ? | 2019/2 | 木造 | 状況：有（敷地内） 1台空きあり 価格：駐車場無 | house | https://flat.chintai-kyoto.jp/rent/1130674537890000400667/ |
| 0.62 | ベルメゾン鴨川 206 | 2LDK | 48.6 | 95,000 | 7000 | 1ヶ月 / 100,000円 | 1.05 | 2/3 | ? | 1988/9 | RC | 状況：空無 価格：22,000円 〜 特徴：駐輪 | old | https://flat.chintai-kyoto.jp/rent/902000000001827866/ |
| 0.99 | 京都グランドハイツ 411 | 2LDK | 64.5 | 140,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 4/7 | Y | 1971/6 | RC | 状況：空無 特徴：駐輪場有り、バイク置き場有り | old | https://flat.chintai-kyoto.jp/rent/1130674537890000387276/ |
| 1.23 | 王様田中野神町貸家 ｶｼﾔ | 6DK | 145.36 | 150,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/4 | ? | 1976/8 | 鉄骨 | 状況：無 | house | https://flat.chintai-kyoto.jp/rent/1130674537890000388871/ |
