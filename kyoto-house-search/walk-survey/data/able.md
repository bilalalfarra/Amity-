# able — エイブル (able.co.jp), WALK survey (≤1.3 km of 京都技術科学センター, 左京区吉田河原町14), fetched 2026-10-18

## Method
- List URL: https://www.able.co.jp/kyoto/area/<ward>/list/?cf=0&ct=0&m=5&m=6&m=7&m=8&m=9&m=A&m=B&sf=45&st=0&h=99&b=1&b=2&b=3&n=B (2LDK+ layouts, ≥45 m², no age limit, アパート/マンション/戸建, incl. 定期借家), pagination `&i=N`. No rent cap (the server ignores `ct=` anyway); no 礼金 / age / floor / elevator rules.
- Wards 左京(26103), 上京(26102), 中京(26104) (site room counts {'左京区': 115, '上京区': 82, '中京区': 115}): 11 list pages, 312 unique room listings (raw: out/raw/able/list_<ward>_p<N>.html).
- List-stage funnel: total 312, > 1.3 km 277, candidates 34, layout 1 → all 34 unit pages fetched (Detail.do?bk=…; raw: out/raw/able/detail/; HTTP cached) → detail-stage drops: none.
- Distances use the exact lat/lon embedded in each list card (showGoogleMap) → block-level accurate.
- `parking` is quoted verbatim from the unit page (駐車場). エイブル usually lists 仲介手数料 0.55ヶ月; 諸費用 (鍵交換, 清掃, サポート費) are in `other_initial`.
- Station plausibility check (geofix.py; Kyoto town names repeat, GSI returns one): {'checked': 1, 'no_station': 0, 'inconsistent_moved': 0, 'dropped_lower_bound': 1}; dropped (cannot be ≤1.3 km given the listed 駅徒歩): 1 → out/able_geodropped.json.

## Result
- **Kept 33 units** (after merging 0 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via the same building name in another listing with a full address, 0 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 22; rent range kept: 100000–402000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'old': 8, 'A': 22, 'house': 2, 'B': 1}; 礼金 ≤1ヶ月 18, >1ヶ月 15, unknown 0 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'site': 33} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 24/9/0; by ward: {'左京区': 16, '上京区': 12, '中京区': 5}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/able/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.28 | 上阿達谷口マンション | 3DK | 46.12 | 110,000 | 6000 | 11万/-- / 11万/-- | 1.0 | 1/4 | n | 1989/4 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710064314018&prefkey=kyoto |
| 0.45 | THE　Residence　御車道 | 2LDK | 59.7 | 192,000 | 10000 | 19.2万/-- / 20万/-- | 1.04 | 2/4 | Y | 2026/8 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000707753663005&prefkey=kyoto |
| 0.45 | GrandEterna京大正門前 | 2LDK | 64.9 | 163,000 | 9000 | なし/-- / 32.6万/-- | 2.0 | 4/5 | Y | 2008/9 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000710154252005&prefkey=kyoto |
| 0.45 | GrandEterna京大正門前 | 2LDK | 64.2 | 163,500 | 9000 | なし/-- / 32.7万/-- | 2.0 | 3/5 | Y | 2008/9 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000710154252026&prefkey=kyoto |
| 0.45 | GrandEterna京大正門前 | 3LDK | 71.07 | 168,500 | 11000 | なし/-- / 33.7万/-- | 2.0 | 2/5 | Y | 2008/9 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000710154252024&prefkey=kyoto |
| 0.45 | GrandEterna京大正門前 | 2LDK | 64.2 | 160,500 | 9000 | なし/-- / 32.1万/-- | 2.0 | 2/5 | Y | 2008/9 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000710154252016&prefkey=kyoto |
| 0.5 | ノーベルテラス稔 | 2LDK | 57.76 | 220,000 | 8000 | 22万/-- / 44万/-- | 2.0 | 4/5 | Y | 2003/3 | 鉄骨 | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000710640427003&prefkey=kyoto |
| 0.61 | ベリエ茶五 | 2LDK | 54.72 | 150,000 | 15000 | なし/-- / 30万/-- | 2.0 | 3/6 | Y | 2008/3 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000707146989013&prefkey=kyoto |
| 0.62 | エスタプレイス | 2LDK | 73.03 | 216,000 | 7500 | なし/-- / 21.6万/-- | 1.0 | 4/6 | Y | 2027/4 | RC | 有料駐車場1台(22,000円/月) ※駐車場の | A | https://www.able.co.jp/detail/Detail.do?bk=000000710755736010&prefkey=kyoto |
| 0.62 | エスタプレイス | 2LDK | 73.03 | 216,000 | 7500 | なし/-- / 21.6万/-- | 1.0 | 3/6 | Y | 2027/4 | RC | 有料駐車場1台(22,000円/月) ※駐車場の | A | https://www.able.co.jp/detail/Detail.do?bk=000000710755736008&prefkey=kyoto |
| 0.62 | エスタプレイス | 2LDK | 73.03 | 215,000 | 7500 | なし/-- / 21.5万/-- | 1.0 | 2/6 | Y | 2027/4 | RC | 有料駐車場1台(22,000円/月) ※駐車場の | A | https://www.able.co.jp/detail/Detail.do?bk=000000710755736004&prefkey=kyoto |
| 0.62 | エスタプレイス | 2LDK | 68.55 | 206,000 | 7500 | なし/-- / 20.6万/-- | 1.0 | 2/6 | Y | 2027/4 | RC | 有料駐車場1台(22,000円/月) ※駐車場の | A | https://www.able.co.jp/detail/Detail.do?bk=000000710755736001&prefkey=kyoto |
| 0.62 | エスタプレイス | 2LDK | 68.55 | 207,000 | 7500 | なし/-- / 20.7万/-- | 1.0 | 3/6 | Y | 2027/4 | RC | 有料駐車場1台(22,000円/月) ※駐車場の | A | https://www.able.co.jp/detail/Detail.do?bk=000000710755736005&prefkey=kyoto |
| 0.65 | レジディア御所東 | 3LDK | 113.88 | 402,000 | 18000 | 40.2万/-- / なし/-- | 0.0 | 9/10 | Y | 2007/9 | RC | 有料駐車場1台(25,300円/月)/バイク置場 | A | https://www.able.co.jp/detail/Detail.do?bk=000000710137648002&prefkey=kyoto |
| 0.65 | イーグルコート聖護院(605) | 3LDK | 78.04 | 215,000 | 10000 | 21.5万/-- / 21.5万/-- | 1.0 | 6/7 | Y | 2003/3 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000710747149001&prefkey=kyoto |
| 0.68 | グランレブリー御所東Ⅱ | 2LDK | 53.94 | 138,000 | 10000 | なし/-- / 13.8万/-- | 1.0 | 2/3 | n | 1987/3 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710536804003&prefkey=kyoto |
| 0.68 | グランレブリー御所東Ⅱ | 2LDK | 53.94 | 136,000 | 10000 | なし/-- / 13.6万/-- | 1.0 | 1/3 | n | 1987/3 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710536804002&prefkey=kyoto |
| 0.75 | サンアートビル | 3DK | 59.14 | 130,000 | 8000 | なし/-- / なし/-- | 0.0 | 6/6 | Y | 1981/12 | 鉄骨 | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710755283001&prefkey=kyoto |
| 0.76 | 聖護院アパルトメント | 2LDK | 94.4 | 190,000 | 4000 | なし/-- / なし/-- | 0.0 | 4/4 | n | 1977/1 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710029443013&prefkey=kyoto |
| 0.79 | BRIGH　STONE　御所北 | 2LDK | 52.01 | 174,000 | 10000 | 17.4万/-- / 34.8万/-- | 2.0 | 1/3 | Y | 2024/9 | 鉄骨 | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000707712630010&prefkey=kyoto |
| 0.87 | 吉田上大路町19番地1貸家 | 3LDK+S | 94.92 | 230,000 | 0 | 23万/-- / 46万/-- | 2.0 | 1/2 | n | 2016/1 | 木造 | 無料駐車場1台 ※駐車場の金額表示は1台分の表示 | house | https://www.able.co.jp/detail/Detail.do?bk=000000710754085001&prefkey=kyoto |
| 0.98 | ベレヴュー聖護院（６０１） | 3LDK | 65.28 | 150,000 | 0 | 15万/-- / 15万/-- | 1.0 | 6/7 | Y | 1994/12 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000710751818001&prefkey=kyoto |
| 1.04 | 京都グランドハイツ(411) | 2LDK | 64.5 | 140,000 | 10000 | 14万/-- / 14万/-- | 1.0 | 4/7 | Y | 1971/6 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710728798001&prefkey=kyoto |
| 1.06 | サンシティ御所南 | 3LDK | 89.44 | 260,000 | 10000 | 26万/-- / 52万/-- | 2.0 | 3/3 | Y | 2006/3 | RC | 有料駐車場1台(30,000円/月)/バイク置場 | A | https://www.able.co.jp/detail/Detail.do?bk=000000714116385008&prefkey=kyoto |
| 1.11 | 岡崎東福ノ川町貸家 | 3LDK+S | 107.96 | 135,000 | 0 | なし/-- / なし/-- | 0.0 | 3/3 | n | 1995/4 | 木造 | 無料駐車場1台 ※駐車場の金額表示は1台分の表示 | house | https://www.able.co.jp/detail/Detail.do?bk=000000704763079001&prefkey=kyoto |
| 1.14 | ＫＢ．メゾンロ－タス | 2LDK | 51.17 | 121,000 | 4600 | なし/-- / 12.1万/-- | 1.0 | 1/3 | n | 2011/3 | 鉄骨 | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000710182240002&prefkey=kyoto |
| 1.17 | メゾンフジ | 3LDK | 80.0 | 135,000 | 5000 | なし/-- / なし/-- | 0.0 | 2/5 | n | 1985/10 | 鉄骨 | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000704612009005&prefkey=kyoto |
| 1.19 | フォルム聖護院別邸(303) | 3LDK | 72.57 | 168,000 | 12000 | なし/-- / 20万/-- | 1.19 | 3/5 | Y | 2001/6 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000710759054001&prefkey=kyoto |
| 1.22 | ジオ御所南河原町二条(501) | 2LDK | 66.49 | 230,000 | 17950 | 23万/-- / 24.795万/-- | 1.08 | 5/7 | Y | 2013/9 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000714756786001&prefkey=kyoto |
| 1.27 | 仮)ROUAGE御所南 | 2LDK | 76.29 | 270,000 | 20000 | なし/-- / 54万/-- | 2.0 | 4/5 | Y | 2026/4 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000714745843006&prefkey=kyoto |
| 1.27 | 仮)ROUAGE御所南 | 2LDK | 76.29 | 265,000 | 20000 | なし/-- / 53万/-- | 2.0 | 3/5 | Y | 2026/4 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000714745843004&prefkey=kyoto |
| 1.27 | 仮)ROUAGE御所南 | 2LDK | 76.29 | 260,000 | 20000 | なし/-- / 52万/-- | 2.0 | 2/5 | Y | 2026/4 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000714745843002&prefkey=kyoto |
| 1.3 | 北白川コーポラス | 3DK | 66.0 | 100,000 | 8000 | 10万/-- / 10万/-- | 1.0 | 3/4 | n | 1970/10 | RC | 有料駐車場1台(8,000円/月) ※駐車場の金 | old | https://www.able.co.jp/detail/Detail.do?bk=000000710038383006&prefkey=kyoto |
