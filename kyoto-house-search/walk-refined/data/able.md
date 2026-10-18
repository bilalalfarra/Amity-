# able — エイブル (able.co.jp), WALK3 survey (≤3.0 km of 京都技術科学センター, 左京区吉田河原町14; rent ≤140,000), fetched 2026-10-18

## Method
- List URL: https://www.able.co.jp/kyoto/area/<ward>/list/?cf=0&ct=0&m=5&m=6&m=7&m=8&m=9&m=A&m=B&sf=45&st=0&h=99&b=1&b=2&b=3&n=B (2LDK+ layouts, ≥45 m², no age limit, アパート/マンション/戸建, incl. 定期借家), pagination `&i=N`. Rent ≤140,000 applied client-side (the server ignores `ct=`); no 礼金 / age / floor / elevator rules.
- Wards 北(26101), 上京(26102), 左京(26103), 中京(26104), 東山(26105), 下京(26106) (site room counts {'北区': 47, '上京区': 82, '左京区': 115, '中京区': 116, '東山区': 6, '下京区': 90}): 17 list pages, 456 unique room listings (raw: out/raw/able/list_<ward>_p<N>.html).
- List-stage funnel: total 456, > 3.0 km 116, rent>140,000 277, candidates 62, layout 1 → all 62 unit pages fetched (Detail.do?bk=…; raw: out/raw/able/detail/; HTTP {200: 52}) → detail-stage drops: none.
- Distances use the exact lat/lon embedded in each list card (showGoogleMap) → block-level accurate.
- `parking` is quoted verbatim from the unit page (駐車場). エイブル usually lists 仲介手数料 0.55ヶ月; 諸費用 (鍵交換, 清掃, サポート費) are in `other_initial`.
- Station plausibility check (geofix.py; Kyoto town names repeat, GSI returns one): {'checked': 1, 'no_station': 0, 'inconsistent_moved': 0, 'dropped_lower_bound': 0}; dropped (cannot be ≤3.0 km given the listed 駅徒歩): 0 → out/able_geodropped.json.

## Result
- **Kept 61 units** (after merging 1 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via the same building name in another listing with a full address, 0 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 4; rent range kept: 68000–140000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'old': 31, 'house': 4, 'A': 12, 'B': 14}; 礼金 ≤1ヶ月 49, >1ヶ月 12, unknown 0 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'site': 60, 'address (GSI)': 1} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 34/27/0; by ward: {'左京区': 24, '上京区': 28, '中京区': 8, '北区': 1}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/able/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.28 | 上阿達谷口マンション | 3DK | 46.12 | 110,000 | 6000 | 11万/-- / 11万/-- | 1.0 | 1/4 | n | 1989/4 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710064314018&prefkey=kyoto |
| 0.68 | グランレブリー御所東Ⅱ | 2LDK | 53.94 | 138,000 | 10000 | なし/-- / 13.8万/-- | 1.0 | 2/3 | n | 1987/3 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710536804003&prefkey=kyoto |
| 0.68 | グランレブリー御所東Ⅱ | 2LDK | 53.94 | 136,000 | 10000 | なし/-- / 13.6万/-- | 1.0 | 1/3 | n | 1987/3 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710536804002&prefkey=kyoto |
| 0.75 | サンアートビル | 3DK | 59.14 | 130,000 | 8000 | なし/-- / なし/-- | 0.0 | 6/6 | Y | 1981/12 | 鉄骨 | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710755283001&prefkey=kyoto |
| 1.04 | 京都グランドハイツ(411) | 2LDK | 64.5 | 140,000 | 10000 | 14万/-- / 14万/-- | 1.0 | 4/7 | Y | 1971/6 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710728798001&prefkey=kyoto |
| 1.11 | 岡崎東福ノ川町貸家 | 3LDK+S | 107.96 | 135,000 | 0 | なし/-- / なし/-- | 0.0 | 3/3 | n | 1995/4 | 木造 | 無料駐車場1台 ※駐車場の金額表示は1台分の表示 | house | https://www.able.co.jp/detail/Detail.do?bk=000000704763079001&prefkey=kyoto |
| 1.14 | ＫＢ．メゾンロ－タス | 2LDK | 51.17 | 121,000 | 4600 | なし/-- / 12.1万/-- | 1.0 | 1/3 | n | 2011/3 | 鉄骨 | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000710182240002&prefkey=kyoto |
| 1.17 | メゾンフジ | 3LDK | 80.0 | 135,000 | 5000 | なし/-- / なし/-- | 0.0 | 2/5 | n | 1985/10 | 鉄骨 | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000704612009005&prefkey=kyoto |
| 1.3 | 北白川コーポラス | 3DK | 66.0 | 100,000 | 8000 | 10万/-- / 10万/-- | 1.0 | 3/4 | n | 1970/10 | RC | 有料駐車場1台(8,000円/月) ※駐車場の金 | old | https://www.able.co.jp/detail/Detail.do?bk=000000710038383006&prefkey=kyoto |
| 1.39 | アイル竹嶋 | 2LDK | 48.0 | 120,000 | 15000 | なし/-- / 25万/-- | 2.08 | 5/6 | Y | 1993/3 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000704042333000&prefkey=kyoto |
| 1.46 | パラド－ル御所 | 3LDK | 63.18 | 130,000 | 15000 | 13万/-- / 26万/-- | 2.0 | 5/7 | Y | 1984/2 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000707028552003&prefkey=kyoto |
| 1.58 | i.レジデンス御所北 | 2LDK | 54.08 | 134,000 | 7000 | なし/-- / 20万/-- | 1.49 | 1/4 | n | 2014/3 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000707494778005&prefkey=kyoto |
| 1.58 | 藤波ﾋﾞﾙ | 2LDK | 48.0 | 114,000 | 4000 | 5万/-- / 10万/-- | 0.88 | 2/4 | n | 1990/3 | 鉄骨 | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000707031043005&prefkey=kyoto |
| 1.6 | リッツ岡崎 | 2LDK | 68.0 | 130,000 | 12000 | 10万/-- / 10万/-- | 0.77 | 2/3 | Y | 1990/2 | RC | 有料駐車場1台(22,000円/月) ※駐車場の | old | https://www.able.co.jp/detail/Detail.do?bk=000000710014969007&prefkey=kyoto |
| 1.61 | メゾンミュゲ | 2LDK | 64.98 | 130,000 | 5000 | 13万/-- / 26万/-- | 2.0 | 2/2 | n | 2020/6 | 軽量鉄骨 | 有料駐車場1台(12,000円/月) ※駐車場の | A | https://www.able.co.jp/detail/Detail.do?bk=000000710756439001&prefkey=kyoto |
| 1.66 | 相国寺門前町貸家 | 2LDK+S | 62.72 | 120,000 | 0 | なし/-- / 10万/-- | 0.83 | 1/2 | n | 1911/1 | 木造 | なし | house | https://www.able.co.jp/detail/Detail.do?bk=000000707611308001&prefkey=kyoto |
| 1.71 | セラヴィー119 | 2LDK | 63.52 | 140,000 | 10000 | 14万/-- / 14万/-- | 1.0 | 5/5 | Y | 1989/6 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710020916007&prefkey=kyoto |
| 1.73 | 高野ロイヤルハイツ | 2LDK | 46.0 | 68,000 | 7000 | なし/-- / 8万/-- | 1.18 | 3/4 | Y | 1977/10 | RC | 有料駐車場1台(16,500円/月) ※駐車場の | old | https://www.able.co.jp/detail/Detail.do?bk=000000710050926038&prefkey=kyoto |
| 1.74 | ピアレス円勝寺 | 2LDK | 62.41 | 120,000 | 20000 | 12万/-- / 12万/-- | 1.0 | 2/3 | Y | 1984/11 | RC | 有料駐車場1台(27,000円/月) ※駐車場の | old | https://www.able.co.jp/detail/Detail.do?bk=000000710020630011&prefkey=kyoto |
| 1.79 | プラネシア星の子御所西 | 2LDK | 60.2 | 114,000 | 9000 | なし/-- / 17.1万/-- | 1.5 | 4/6 | n | 1973/5 | 鉄骨 | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000707084399013&prefkey=kyoto |
| 1.79 | プラネシア星の子御所西 | 2LDK | 52.0 | 117,000 | 9000 | なし/-- / 11.7万/-- | 1.0 | 2/6 | n | 1973/5 | 鉄骨 | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000707084399010&prefkey=kyoto |
| 1.91 | サンレジデンス錦綾東堀川(904) | 3LDK | 74.8 | 120,000 | 10000 | 12万/-- / 12万/-- | 1.0 | 9/11 | n | 1982/11 | その他 | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000707757586001&prefkey=kyoto |
| 1.93 | 浄土寺下南田町借家 | 3LDK | 70.0 | 100,000 | 0 | 10万/-- / 10万/-- | 1.0 | 2/2 | n | 1974/4 | 木造 | なし | house | https://www.able.co.jp/detail/Detail.do?bk=000000710133740001&prefkey=kyoto |
| 2.01 | マサール哲学の道 | 2LDK | 58.57 | 107,000 | 3500 | なし/-- / 10.7万/-- | 1.0 | 2/2 | n | 2015/3 | 木造 | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000710516280006&prefkey=kyoto |
| 2.1 | カストルム洛北 | 3LDK | 64.9 | 113,000 | 12000 | 10万/-- / 10万/-- | 0.88 | 2/7 | Y | 1983/4 | RC | 有料駐車場1台(22,000円/月) ※駐車場の | old | https://www.able.co.jp/detail/Detail.do?bk=000000710022514041&prefkey=kyoto |
| 2.1 | カストルム洛北 | 3LDK | 67.65 | 113,000 | 12000 | 10万/-- / 10万/-- | 0.88 | 3/7 | Y | 1983/4 | RC | 有料駐車場1台(22,000円/月) ※駐車場の | old | https://www.able.co.jp/detail/Detail.do?bk=000000710022514015&prefkey=kyoto |
| 2.14 | シェモア鞍馬口Ⅱ（１０６） | 2LDK | 54.86 | 105,000 | 10000 | 10.5万/-- / 10.5万/-- | 1.0 | 1/3 | n | 1984/11 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000707752705001&prefkey=kyoto |
| 2.2 | グレ－スコ－ト堀川 | 2LDK | 50.0 | 87,000 | 5000 | なし/-- / 15万/-- | 1.72 | 4/5 | Y | 1988/7 | 鉄骨 | バイク置場あり ※駐車場の金額表示は1台分の表示 | old | https://www.able.co.jp/detail/Detail.do?bk=000000707112150014&prefkey=kyoto |
| 2.21 | 京都一乗寺コーポラス(610) | 3DK | 45.37 | 85,000 | 0 | なし/-- / 8.5万/-- | 1.0 | 6/7 | Y | 1976/7 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710752300001&prefkey=kyoto |
| 2.24 | ファ－ストコ－ト今出川北 | 3LDK | 60.32 | 98,000 | 10000 | なし/-- / 9.8万/-- | 1.0 | 5/7 | Y | 1981/8 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000707093138001&prefkey=kyoto |
| 2.28 | GRANDEUR　KAMANZA | 2LDK | 52.56 | 140,000 | 7000 | 14万/-- / なし/-- | 0.0 | 2/5 | Y | 2011/11 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000714560281002&prefkey=kyoto |
| 2.29 | カ－ネルヒル | 2LDK | 51.1 | 105,000 | 8000 | 10万/-- / なし/-- | 0.0 | 2/5 | Y | 1989/10 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000714142864012&prefkey=kyoto |
| 2.29 | カ－ネルヒル | 2LDK | 51.1 | 106,000 | 8000 | 10万/-- / なし/-- | 0.0 | 4/5 | Y | 1989/10 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000714142864004&prefkey=kyoto |
| 2.3 | シャトー高野 | 2LDK | 52.2 | 81,000 | 4000 | なし/-- / なし/-- | 0.0 | 4/4 | n | 1978/9 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710018597018&prefkey=kyoto |
| 2.31 | CASA SHIMEI | 2LDK | 53.0 | 92,000 | 10000 | なし/-- / 9.2万/-- | 1.0 | 2/4 | n | 1991/7 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000707057001002&prefkey=kyoto |
| 2.31 | グラシオン西陣 | 2LDK | 56.83 | 124,000 | 8000 | 20万/-- / 20万/-- | 1.61 | 3/11 | Y | 2004/3 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000707163816003&prefkey=kyoto |
| 2.33 | ラヴィエール北白川 | 2LDK | 60.96 | 122,000 | 7000 | 12.2万/-- / 12.2万/-- | 1.0 | 1/2 | n | 2025/2 | 木造 | 有料駐車場1台(15,000円/月) ※駐車場の | A | https://www.able.co.jp/detail/Detail.do?bk=000000710754657001&prefkey=kyoto |
| 2.38 | 大晋メゾネ西陣今出川 | 3LDK | 74.81 | 130,000 | 9000 | 13万/-- / 13万/-- | 1.0 | 5/10 | Y | 1998/3 | SRC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000707572043009&prefkey=kyoto |
| 2.38 | 大晋メゾネ西陣今出川 | 2LDK+S | 65.55 | 125,000 | 9000 | 12.5万/-- / 12.5万/-- | 1.0 | 3/10 | Y | 1998/3 | SRC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000707572043010&prefkey=kyoto |
| 2.38 | メゾンアルマ | 2LDK | 51.88 | 110,000 | 10000 | 11万/-- / 22万/-- | 2.0 | 5/6 | Y | 1989/3 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000714126810004&prefkey=kyoto |
| 2.39 | ヴューキャッスル | 3DK | 62.59 | 105,000 | 10000 | なし/-- / なし/-- | 0.0 | 3/5 | Y | 1992/6 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000707732948004&prefkey=kyoto |
| 2.4 | 堀川シティハイツ(901) | 2LDK | 53.61 | 90,000 | 5000 | 9万/-- / 9万/-- | 1.0 | 9/11 | Y | 1976/9 | SRC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000707490463001&prefkey=kyoto |
| 2.42 | ベルスーズ西陣 | 3LDK | 65.02 | 120,000 | 9500 | なし/-- / 12万/-- | 1.0 | 5/6 | Y | 1998/7 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000707680960003&prefkey=kyoto |
| 2.42 | ベルスーズ西陣 | 3LDK | 65.02 | 120,000 | 9500 | なし/-- / 12万/-- | 1.0 | 3/6 | Y | 1998/7 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000707680960002&prefkey=kyoto |
| 2.43 | コスモ星の子ハイツ | 3DK | 55.0 | 90,000 | 9000 | なし/-- / 9万/-- | 1.0 | 4/7 | Y | 1985/9 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000707052596014&prefkey=kyoto |
| 2.58 | パインフィールド二条城 | 2LDK | 52.77 | 139,000 | 8000 | なし/-- / なし/-- | 0.0 | 8/10 | Y | 1995/10 | RC | 有料駐車場1台(25,000円/月) ※駐車場の | B | https://www.able.co.jp/detail/Detail.do?bk=000000726095543006&prefkey=kyoto |
| 2.58 | パインフィールド二条城 | 2LDK | 50.45 | 139,000 | 8000 | なし/-- / なし/-- | 0.0 | 5/10 | Y | 1995/10 | SRC | 有料駐車場1台(27,500円/月)/バイク置場 | B | https://www.able.co.jp/detail/Detail.do?bk=000000726095543003&prefkey=kyoto |
| 2.62 | フェリーチェ白川東 | 2LDK | 71.54 | 138,000 | 0 | 13.8万/-- / 27.6万/-- | 2.0 | 2/2 | n | 2026/5 | 木造 | 無料駐車場1台 ※駐車場の金額表示は1台分の表示 | house | https://www.able.co.jp/detail/Detail.do?bk=000000710757768001&prefkey=kyoto |
| 2.65 | ルネ紫野 | 2LDK | 59.8 | 85,000 | 4000 | 5万/-- / 10万/-- | 1.18 | 2/2 | n | 2005/4 | 木造 | 有料駐車場1台(15,000円/月) ※駐車場の | A | https://www.able.co.jp/detail/Detail.do?bk=000000707135113005&prefkey=kyoto |
| 2.73 | ペレニアルフラックス | 2LDK | 75.5 | 120,000 | 6000 | 12万/-- / 12万/-- | 1.0 | 2/3 | n | 1992/8 | RC | 有料駐車場1台(15,400円/月) ※駐車場の | B | https://www.able.co.jp/detail/Detail.do?bk=000000710664218003&prefkey=kyoto |
| 2.75 | 詩仙ハイム | 2LDK | 47.0 | 90,000 | 5000 | 9万/-- / 9万/-- | 1.0 | 3/4 | n | 1979/6 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000710022770009&prefkey=kyoto |
| 2.76 | せんぼん有彩館 | 3LDK | 71.2 | 133,000 | 15000 | なし/-- / なし/-- | 0.0 | 3/10 | Y | 1997/8 | 鉄骨 | 有料駐車場1台(25,300円/月)/バイク置場 | B | https://www.able.co.jp/detail/Detail.do?bk=000000707665335012&prefkey=kyoto |
| 2.76 | せんぼん有彩館 | 3LDK | 71.2 | 134,000 | 15000 | なし/-- / なし/-- | 0.0 | 5/10 | Y | 1997/8 | 鉄骨 | 有料駐車場1台(25,300円/月)/バイク置場 | B | https://www.able.co.jp/detail/Detail.do?bk=000000707665335011&prefkey=kyoto |
| 2.76 | せんぼん有彩館 | 3LDK | 71.2 | 132,000 | 15000 | なし/-- / なし/-- | 0.0 | 2/10 | Y | 1997/8 | 鉄骨 | バイク置場あり ※駐車場の金額表示は1台分の表示 | B | https://www.able.co.jp/detail/Detail.do?bk=000000707665335007&prefkey=kyoto |
| 2.78 | ユアメゾン 白川１ | 2LDK | 63.0 | 125,000 | 6000 | 12.5万/-- / 25万/-- | 2.0 | 2/2 | n | 2026/10 | 鉄骨 | 有料駐車場1台(15,400円/月) ※駐車場の | A | https://www.able.co.jp/detail/Detail.do?bk=000000710757540004&prefkey=kyoto |
| 2.84 | 嶋津マンション | 3LDK | 60.0 | 125,000 | 10000 | 12.5万/-- / 12.5万/-- | 1.0 | 4/7 | Y | 1991/7 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000714022069010&prefkey=kyoto |
| 2.84 | グランディール錦 | 2LDK | 58.87 | 110,000 | 18000 | なし/-- / なし/-- | 0.0 | 1/7 | Y | 1986/4 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000714013584011&prefkey=kyoto |
| 2.85 | カーサ葵 | 3LDK | 68.14 | 140,000 | 10000 | 14万/-- / 14万/-- | 1.0 | 3/3 | Y | 2001/3 | RC | 有料駐車場1台(20,900円/月) ※駐車場の | A | https://www.able.co.jp/detail/Detail.do?bk=000000726635967001&prefkey=kyoto |
| 2.87 | Ｄ-ＲＯＯＭ一乗寺 | 2LDK | 52.79 | 136,000 | 8000 | なし/-- / 13.6万/-- | 1.0 | 2/3 | n | 2024/10 | 軽量鉄骨 | 有料駐車場1台(14,300円/月) ※駐車場の | A | https://www.able.co.jp/detail/Detail.do?bk=000000710715084004&prefkey=kyoto |
| 2.87 | Ｄ-ＲＯＯＭ一乗寺 | 2LDK | 52.79 | 134,000 | 8000 | なし/-- / 13.4万/-- | 1.0 | 1/3 | n | 2024/10 | 鉄骨 | 有料駐車場1台(14,300円/月) ※駐車場の | A | https://www.able.co.jp/detail/Detail.do?bk=000000710715084001&prefkey=kyoto |
| 2.9 | シャトレ西陣 | 2LDK | 45.0 | 90,000 | 5000 | 9万/-- / 9万/-- | 1.0 | 7/7 | Y | 1974/4 | RC | なし | old | https://www.able.co.jp/detail/Detail.do?bk=000000707183327006&prefkey=kyoto |
