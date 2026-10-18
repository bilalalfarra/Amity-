# kyotolife — 京都ライフ (kyoto-life.co.jp), WALK3 survey (≤3.0 km of 左京区吉田河原町14, rent ≤ 14万, 2LDK+, ≥45 m²), fetched 2026-10-18

## Method (walk3/kyotolife_walk.py, copy of walk/kyotolife_walk.py)
- Own search (server-side HTML): `/app/search.php?__mode=search&by=area&search_type=building&rent_fee_upper_limit=140000&prefecture_city_code[]=26-10X&floor_plan_category_code[]=…&limit=50&offset=N`
  for 北区 26-101, 上京区 26-102, 左京区 26-103, 中京区 26-104, 東山区 26-105, 下京区 26-106 (floor_plan_category_code RR0T1 = 2LDK/2SLDK, 3K…6SLDK).
- List addresses are town-level → town geocode (通り名 stripped) with a 3.4 km margin; list rent > 14万 and layout/area misses dropped.
- Unit pages `/app/search.php?__mode=room&room_code=…`: pages already fetched (HTTP 200) earlier today by the walk/ run are re-used when the room is still in today's list; the rest fetched now. Final distance from the map pin in the unit page (「この物件の周辺地図」).
- `parking` = 駐車場 cell verbatim; `elevator` from 条件・設備.

## Result
- **Kept 139 units** (after merging 2 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via the same building name in another listing with a full address, 0 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 12; rent range kept: 55000–140000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'house': 23, 'B': 30, 'old': 57, 'A': 29}; 礼金 ≤1ヶ月 88, >1ヶ月 47, unknown 4 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'site': 139} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 77/62/0; by ward: {'左京区': 52, '上京区': 50, '中京区': 25, '北区': 4, '東山区': 3, '下京区': 5}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/kyotolife/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.13 | 吉田中阿達町貸家 | 2LDK | 66.7 | 120,000 | 0 | - / 2ヶ月 | 2.0 | 1/2 | n | 2004/12 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000709278 |
| 0.16 | 今智庵 | 3DK | 65.0 | 100,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/2 | n | 1984/11 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000183992 |
| 0.17 | エーデルハイム鴨川 | 3LDK | 65.77 | 138,000 | 10000 | 20万円 / 35万円 | 2.54 | 5/5 | Y | 1997/2 | RC | 有 21,000円 | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000033844 |
| 0.28 | 上阿達谷口マンション | 3DK | 45.7 | 110,000 | 6000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/4 | n | 1989/4 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000034399 |
| 0.3 | 吉田上阿達町貸家 | 3DK | 45.75 | 100,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1960/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000711119 |
| 0.53 | 田中下柳町貸家 | 5K | 82.7 | 120,000 | 0 | 2ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1945/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000709842 |
| 0.68 | グランレブリー御所東Ⅱ | 2LDK | 53.94 | 138,000 | 10000 | - / 1ヶ月 | 1.0 | 2/3 | n | 1987/3 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000157006 |
| 0.68 | グランレブリー御所東Ⅱ | 2LDK | 53.94 | 136,000 | 10000 | - / 1ヶ月 | 1.0 | 1/3 | n | 1987/3 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000225273 |
| 0.74 | サンアートビル | 3LDK | 59.14 | 130,000 | 8000 | - / - | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000159928 |
| 0.78 | 東丸太町貸家 | 3SLDK | 90.0 | 135,000 | 0 | - / 1ヶ月 | 1.0 | 1/2 | n | 1950/5 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000532383 |
| 0.81 | 吉田中大路町アパート | 2LDK | 49.66 | 87,000 | 3000 | - / - | 0.0 | 1/2 | n | 2002/10 | 木造 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000569511 |
| 0.96 | かぐら坂荘 | 2LDK | 60.23 | 128,000 | 7000 | - / 12.8万円 | 1.0 | 3/3 | n | 2011/3 | RC | 有 19,800円 ～ 22,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000319551 |
| 1.03 | 京都グランドハイツ | 2LDK | 64.5 | 140,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 4/7 | Y | 1971/6 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=260000633818 |
| 1.21 | コーポ富有 | 2LDK | 48.51 | 100,000 | 9000 | 10万円 / 10万円 | 1.0 | 2/4 | Y | 1985/7 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=210000685310 |
| 1.23 | 山和小路 | 3DK | 66.97 | 125,000 | 10000 | - / 1ヶ月 | 1.0 | 5/5 | Y | 1999/11 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000221493 |
| 1.3 | 北白川コーポラス | 3LDK | 66.0 | 100,000 | 8000 | 10万円 / 10万円 | 1.0 | 3/4 | n | 1970/3 | RC | 有 8,000円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000219169 |
| 1.39 | アイル竹嶋 | 2LDK | 52.0 | 130,000 | 0 | - / 30万円 | 2.31 | 5/6 | Y | 1993/3 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000465446 |
| 1.43 | 二条麩屋町ビューハイツ | 3LDK | 72.8 | 140,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 6/9 | Y | 1981/10 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000403755 |
| 1.47 | パラドール御所 | 3LDK | 63.18 | 130,000 | 15000 | 1ヶ月 / 2ヶ月 | 2.0 | 5/7 | Y | 1984/2 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000099925 |
| 1.56 | 下鴨泉川町貸家 | 4DK | 66.78 | 92,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1972/3 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000442720 |
| 1.57 | グレーシー高野 | 3DK | 47.8 | 79,000 | 4000 | - / 1ヶ月 | 1.0 | 3/5 | n | 1979/3 | RC | 有 11,000円 ～ 16,500円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000544811 |
| 1.58 | 裏築地町貸家 | 2LDK | 60.0 | 115,000 | 0 | 11.5万円 / 11.5万円 | 1.0 | 2/3 | n | 1998/7 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000246563 |
| 1.58 | ｉ．レジデンス御所北 | 2LDK | 54.08 | 134,000 | 7000 | - / 20万円 | 1.49 | 1/4 | n | 2014/3 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000375273 |
| 1.59 | 藤波ビル | 2LDK | 47.0 | 114,000 | 4000 | 5万円 / 10万円 | 0.88 | 2/4 | n | 1990/3 | 鉄骨 | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000251648 |
| 1.59 | ライオンズマンション二条高倉 | 2SLDK | 54.54 | 135,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 7/9 | Y | 1984/12 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000217877 |
| 1.61 | グランタック御所西　貸家 | 3LDK | 65.93 | 99,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1991/5 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000354715 |
| 1.61 | リッツ岡崎 | 2LDK | 69.0 | 128,000 | 12000 | 10万円 / 19.2万円 | 1.5 | 1/3 | Y | 1990/2 | RC | 有 22,000円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000029515 |
| 1.63 | メゾンミュゲ | 2LDK | 64.98 | 130,000 | 5000 | 1ヶ月 / 2ヶ月 | 2.0 | 2/2 | n | 2020/6 | 軽量鉄骨 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=500000682431 |
| 1.65 | 浄土寺上馬場町貸家 | 3LDK | 71.0 | 125,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1982/6 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000707596 |
| 1.66 | 上京区元真如堂町貸家 | 3DK | 54.37 | 78,000 | 0 | - / 1ヶ月 | 1.0 | 1/2 | n | 1960/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000613216 |
| 1.67 | センチュリープラザ | 2LDK | 45.0 | 83,000 | 8000 |  /  | None | 3/4 | n | 1991/8 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000115416 |
| 1.67 | センチュリープラザ | 2LDK | 45.0 | 83,000 | 8000 |  /  | None | 4/4 | n | 1991/8 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000200745 |
| 1.68 | ピアレス円勝寺 | 2LDK | 62.41 | 120,000 | 20000 | 1ヶ月 / 1ヶ月 | 1.0 | 2/3 | Y | 1984/10 | RC | 有 27,500円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000039610 |
| 1.69 | 出雲路俵町貸家 | 4DK | 66.21 | 93,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1979/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000299452 |
| 1.72 | ベルメゾン一条 | 2LDK | 53.33 | 100,000 | 3000 | 3万円 / 20万円 | 2.0 | 2/3 | n | 1989/2 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000100113 |
| 1.72 | ロイヤルセンタービルコバヤシ | 2LDK | 56.28 | 87,000 | 8000 | 1ヶ月 / 2ヶ月 | 2.0 | 3/5 | Y | 1988/1 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000203725 |
| 1.75 | エルシア御池間之町 | 2LDK | 56.55 | 140,000 | 10000 | 1ヶ月 / 2ヶ月 | 2.0 | 8/11 | Y | 2008/3 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000344662 |
| 1.75 | ＣＨＥＲＲＹ　ＶＩＥＷ | 2LDK | 57.87 | 110,000 | 5000 |  / 22万円 | 2.0 | 2/3 | n | 1990/4 | 鉄骨 | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000513789 |
| 1.77 | レジデンス古橋 | 2LDK | 61.53 | 128,000 | 10000 | - / - | 0.0 | 4/6 | Y | 1978/10 | RC | 有 22,000円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000185471 |
| 1.8 | プラネシア星の子御所西 | 2LDK | 61.9 | 114,000 | 9000 | - / 1.5ヶ月 | 1.5 | 4/4 | n | 1973/5 | 鉄骨 | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000117118 |
| 1.8 | プラネシア星の子御所西 | 2LDK | 52.0 | 117,000 | 9000 | - / - | 0.0 | 2/4 | n | 1973/5 | 鉄骨 | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000246064 |
| 1.8 | 北白川松園 | 3DK | 53.0 | 108,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 3/4 | n | 1969/10 | RC | 有 11,000円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000306234 |
| 1.83 | 京都グランデⅡ番館 | 2LDK | 63.56 | 140,000 | 5000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/3 | n | 2019/9 | 木造 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000510525 |
| 1.84 | 東大路高野第１住宅１棟 | 3DK | 60.94 | 98,000 | 0 | - / 1ヶ月 | 1.0 | 7/7 | Y | 1979/7 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=340000649043 |
| 1.85 | ロートレック中京 | 2LDK | 52.17 | 125,000 | 15000 | 2ヶ月 / 2ヶ月 | 2.0 | 9/11 | Y | 1984/1 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000362717 |
| 1.87 | 上京区橋本町貸家 | 2LDK | 51.08 | 80,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1950/3 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000626323 |
| 1.89 | グリーンヒル北白川 | 3LDK | 54.85 | 130,000 | 3850 | - / 2ヶ月 | 2.0 | 1/2 | n | 1985/1 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000192539 |
| 1.91 | サンレジデンス錦綾東堀川 | 3LDK | 74.8 | 120,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 9/11 | Y | 1982/11 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000227584 |
| 1.95 | マナーハウス | 2LDK | 62.31 | 115,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/4 | Y | 1996/1 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000325176 |
| 1.96 | グランディール下鴨 | 4DK | 60.62 | 85,000 | 5000 | - / - | 0.0 | 1/4 | n | 1983/4 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000114119 |
| 1.96 | 下鴨蓼倉町貸家 | 4DK | 74.72 | 89,000 | 6000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1979/9 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000533831 |
| 1.97 | 白川セントラルハイツ | 3LDK | 50.22 | 75,000 | 9800 | 8.5万円 / 1ヶ月 | 1.0 | 5/5 | Y | 1981/9 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000256990 |
| 1.97 | プラネシア神宮道 | 2LDK | 55.77 | 139,000 | 8000 | - / 1.5ヶ月 | 1.5 | 2/5 | Y | 2010/6 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000297486 |
| 1.99 | マサール哲学の道 | 2LDK | 58.57 | 107,000 | 3500 | - / 1ヶ月 | 1.0 | 2/2 | n | 2015/3 | 木造 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000394381 |
| 1.99 | 下南田町大前邸Ⅰ・Ⅲ | 3LDK | 80.9 | 98,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/2 | n | 1975/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000510178 |
| 2.02 | 橋本町４６９貸家 | 6DK | 66.0 | 135,000 | 0 | 1ヶ月 / - | 0.0 | 1/2 | n | 1957/9 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000632630 |
| 2.03 | シャーメゾン西伊織 | 2LDK | 60.87 | 130,000 | 5000 | 3万円 /  | None | 2/2 | n | 2014/10 | 軽量鉄骨 | 有 14,300円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000382740 |
| 2.03 | カバーロ京都御池 | 2LDK | 48.37 | 120,000 | 5000 | - / 2ヶ月 | 2.0 | 3/8 | Y | 1992/5 | 鉄骨 | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000531106 |
| 2.08 | 田中上古川町貸家 | 3DK | 57.37 | 110,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1984/12 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000709879 |
| 2.08 | 下鴨フラッツ | 2LDK | 52.0 | 98,000 | 6000 | 10万円 / 10万円 | 1.02 | 2/3 | n | 1993/4 | RC | 有 19,800円 | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000323036 |
| 2.08 | 下鴨貸家 | 5DK | 50.0 | 70,000 | None | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1940/3 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000579775 |
| 2.09 | グローバル北白川 | 2LDK | 53.42 | 120,000 | 5000 | - / 1ヶ月 | 1.0 | 4/7 | Y | 1997/2 | RC | 有 14,300円 | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=130000704260 |
| 2.09 | カストルム洛北 | 3LDK | 64.9 | 113,000 | 12000 | 10万円 / 10万円 | 0.88 | 3/7 | Y | 1983/4 | RC | 有 22,000円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000116989 |
| 2.09 | カストルム洛北 | 3LDK | 64.9 | 115,000 | 12000 | 10万円 / 10万円 | 0.87 | 2/7 | Y | 1983/4 | RC | 有 22,000円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000117032 |
| 2.09 | カストルム洛北 | 3LDK | 64.9 | 115,000 | 12000 | 10万円 / 25万円 | 2.17 | 5/7 | Y | 1983/4 | RC | 有 22,000円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000117056 |
| 2.13 | ラヴィエール北白川 | 2LDK | 60.96 | 122,000 | 7000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 2025/1 | 木造 | 有 15,000円 ～ 0円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=500000682460 |
| 2.15 | シェモア鞍馬口Ⅱ | 2LDK | 54.86 | 100,000 | 5000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/3 | n | 1984/12 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=130000702299 |
| 2.19 | グレースコート堀川 | 2LDK | 50.0 | 87,000 | 5000 | - / 15万円 | 1.72 | 4/5 | Y | 1988/7 | 鉄骨 | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000150308 |
| 2.19 | ＫＴマンションⅡ号館 | 2LDK | 56.26 | 125,000 | 8000 | - / 1ヶ月 | 1.0 | 5/6 | Y | 1989/7 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000055829 |
| 2.21 | ファーストコート今出川北 | 3LDK | 55.84 | 98,000 | 10000 | - / 1ヶ月 | 1.0 | 5/7 | Y | 1981/8 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000154662 |
| 2.22 | エバグリーンヴィラ堀川 | 5K | 71.04 | 84,700 | 9680 | 7.7万円 / - | 0.0 | 6/6 | n | 1984/2 | 鉄骨 | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000634152 |
| 2.23 | アレックス堀川寺之内 | 3LDK | 60.16 | 102,000 | 8000 | 1ヶ月 / 1ヶ月 | 1.0 | 6/11 | Y | 1990/2 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000250963 |
| 2.23 | 石薬師町貸家 | 3LDK | 62.3 | 130,000 | 0 | 1ヶ月 / 1.5ヶ月 | 1.5 | 1/2 | n | 1950/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=130000712512 |
| 2.26 | ライオンズマンション二条城東 | 3SDK | 67.79 | 138,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 10/11 | Y | 1991/3 | SRC | 近隣 30,800円 | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000005556 |
| 2.31 | カーサ紫明 | 2LDK | 56.0 | 92,000 | 10000 | - / 9.2万円 | 1.0 | 2/4 | n | 1991/7 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000211476 |
| 2.31 | グラシオン西陣 | 2LDK | 59.77 | 124,000 | 8000 |  /  | None | 3/11 | Y | 2004/3 | RC | 有 17,600円 ～ 20,900円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000103305 |
| 2.31 | カーネルヒル | 2LDK | 50.0 | 105,000 | 8000 | 10万円 / - | 0.0 | 2/5 | Y | 1989/10 | RC | 近隣 30,800円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=210000686670 |
| 2.31 | カーネルヒル | 2LDK | 50.0 | 106,000 | 8000 | 10万円 / - | 0.0 | 4/5 | Y | 1989/10 | RC | 近隣 30,800円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=210000686676 |
| 2.32 | 玉屋・山三小路 | 3LDK | 71.06 | 115,000 | 9000 | 11.5万円 / - | 0.0 | 3/5 | Y | 1998/10 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000178950 |
| 2.32 | 玉屋・山三小路 | 3DK | 64.42 | 115,000 | 9000 | 1ヶ月 / - | 0.0 | 2/5 | Y | 1998/10 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000178963 |
| 2.32 | コスモ星の子ハイツ | 3DK | 57.23 | 90,000 | 9000 | - / 1ヶ月 | 1.0 | 4/7 | Y | 1985/10 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000085011 |
| 2.32 | シャトー高野 | 2LDK | 52.2 | 81,000 | 4000 | - / - | 0.0 | 4/4 | n | 1978/9 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=330000350938 |
| 2.32 | シャトー高野 | 3LDK | 60.0 | 90,000 | 4000 | - / - | 0.0 | 1/4 | n | 1978/9 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=340000630261 |
| 2.34 | エクシオ京都御池 | 2LDK | 57.05 | 128,000 | 0 | 10万円 / 15万円 | 1.17 | 4/11 | Y | 1992/10 | SRC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000224757 |
| 2.35 | イヌイ星の子ハイツ | 3LDK | 65.64 | 135,000 | 10000 | - / 2.4ヶ月 | 2.4 | 6/6 | Y | 1980/8 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000080856 |
| 2.35 | イヌイ星の子ハイツ | 2LDK | 55.03 | 120,000 | 10000 | - / 2.4ヶ月 | 2.4 | 5/6 | Y | 1980/8 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000080761 |
| 2.35 | イヌイ星の子ハイツ | 3LDK | 64.46 | 123,000 | 10000 | - / 2.4ヶ月 | 2.4 | 6/6 | Y | 1980/8 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000080836 |
| 2.36 | ライオンズマンション一条智恵光院 | 2LDK | 59.4 | 124,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 2/6 | Y | 1989/6 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000701510 |
| 2.36 | メイゾン御池 | 2LDK | 47.52 | 99,000 | 11000 | - / 1ヶ月 | 1.0 | 4/11 | Y | 1981/2 | SRC | 近隣 30,800円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=210000703128 |
| 2.37 | 天秤町貸家 | 4LDK | 76.05 | 120,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/2 | n | 1982/12 | 木造 | 込 | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000532436 |
| 2.37 | メゾンアルマ | 2LDK | 53.55 | 110,000 | 10000 | 1ヶ月 / 2ヶ月 | 2.0 | 5/6 | Y | 1989/4 | RC | 近隣 28,000円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000226071 |
| 2.38 | ＬＥＧＡＬ京都二条城東 | 2LDK | 57.45 | 135,000 | 12180 | - / 20万円 | 1.48 | 6/11 | Y | 2005/12 | RC | 近隣 30,800円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000168406 |
| 2.38 | ＬＥＧＡＬ京都二条城東 | 2LDK | 57.45 | 138,000 | 12180 | - / 26万円 | 1.88 | 2/11 | Y | 2005/12 | RC | 近隣 30,800円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000168409 |
| 2.39 | 大晋メゾネ西陣今出川 | 3LDK | 74.81 | 130,000 | 9000 | 1ヶ月 / 1ヶ月 | 1.0 | 5/10 | Y | 1998/4 | SRC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000164413 |
| 2.39 | 大晋メゾネ西陣今出川 | 2SLDK | 65.55 | 125,000 | 9000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/10 | Y | 1998/4 | SRC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000175936 |
| 2.42 | ベルスーズ西陣 | 3LDK | 65.05 | 120,000 | 9500 | - / 12万円 | 1.0 | 5/6 | Y | 1998/7 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000383954 |
| 2.42 | ベルスーズ西陣 | 3LDK | 65.05 | 120,000 | 9500 | - / 1ヶ月 | 1.0 | 3/6 | Y | 1998/7 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000189624 |
| 2.46 | 上京区五辻町貸家 | 4K | 58.7 | 55,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1970/3 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000367503 |
| 2.47 | ハイムフロイデン一乗寺 | 3LDK | 55.0 | 100,000 | 10000 |  / 2ヶ月 | 2.0 | 2/6 | Y | 1988/3 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000035184 |
| 2.47 | ハイムフロイデン一乗寺 | 2LDK | 55.0 | 100,000 | 10000 | - / 2ヶ月 | 2.0 | 1/6 | n | 1988/3 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000385801 |
| 2.47 | ハイムフロイデン一乗寺 | 3DK | 60.0 | 130,000 | 10000 | - / 2ヶ月 | 2.0 | 6/6 | Y | 1988/3 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000624720 |
| 2.47 | ハイムフロイデン一乗寺 | 3LDK | 55.0 | 105,000 | 10000 | - / 2ヶ月 | 2.0 | 4/6 | Y | 1988/3 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=130000704055 |
| 2.52 | 東西俵屋町貸家 | 4K | 57.06 | 85,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1974/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000480577 |
| 2.52 | Ｗｉｔｈ京Ｇｒａｎｄｅｓ | 2LDK | 50.24 | 139,000 | 13000 | 1ヶ月 / 20万円 | 1.44 | 1/5 | Y | 2019/2 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000471770 |
| 2.57 | ロザーンジュ堀川 | 2LDK | 55.44 | 115,000 | 6500 | 1ヶ月 / 1ヶ月 | 1.0 | 3/10 | Y | 1995/12 | SRC | 近隣 28,000円 | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=210000690353 |
| 2.57 | ロザーンジュ堀川 | 2LDK | 56.42 | 118,000 | 6500 | 1ヶ月 / 1ヶ月 | 1.0 | 4/10 | Y | 1995/12 | SRC | 近隣 28,000円 | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=210000690352 |
| 2.58 | 伊佐町貸家 | 4DK | 79.0 | 105,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/3 | n | 1996/10 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000299886 |
| 2.58 | パインフィールド二条城 | 2LDK | 50.45 | 139,000 | 8000 | - / - | 0.0 | 5/10 | Y | 1997/2 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000099775 |
| 2.59 | コト北小路 | 3LDK | 67.5 | 130,500 | 9500 | 1ヶ月 / 1ヶ月 | 1.0 | 7/9 | Y | 2000/12 | SRC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000192868 |
| 2.62 | （仮）一乗寺野田町貸家 | 2LDK | 70.0 | 138,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/2 | n | 2026/6 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000705739 |
| 2.63 | メゾン・ド・プレパント | 3LDK | 76.78 | 140,000 | 5000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/3 | n | 2002/3 | 鉄骨 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=130000707604 |
| 2.65 | グラン佐竹 | 2LDK | 51.0 | 116,000 | 7500 | - / 1ヶ月 | 1.0 | 4/5 | Y | 2015/8 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000405021 |
| 2.65 | ポルト　ボヌール | 2LDK | 48.97 | 105,000 | 6900 | - / 1ヶ月 | 1.0 | 3/5 | Y | 2016/3 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000415838 |
| 2.65 | ポルト　ボヌール | 2LDK | 48.97 | 105,000 | 6900 | - / 1ヶ月 | 1.0 | 4/5 | Y | 2016/3 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000415839 |
| 2.65 | フィエルテ四条烏丸シュッド | 3LDK | 60.0 | 130,000 | 0 | - / 13万円 | 1.0 | 10/10 | Y | 1996/8 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000232691 |
| 2.66 | セレーナ北大路 | 2LDK | 46.33 | 130,000 | 5000 | - / 1ヶ月 | 1.0 | 2/3 | n | 2023/1 | 木造 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=270000585129 |
| 2.66 | ルネ紫野 | 2LDK | 59.8 | 85,000 | 4000 | 5万円 / 10万円 | 1.18 | 1/2 | n | 2005/4 | 木造 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000152227 |
| 2.66 | グレース北園 | 3DK | 72.42 | 140,000 | 10000 | 5万円 / 15万円 | 1.07 | 2/2 | n | 1988/3 | RC | 有 13,000円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000104258 |
| 2.68 | 藤和シティホームズ三条堀川 | 2LDK | 58.72 | 135,000 | 10000 | 1ヶ月 / 2ヶ月 | 2.0 | 6/11 | Y | 1997/4 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000409303 |
| 2.7 | メガロコープ西陣 | 3LDK | 58.44 | 110,000 | 0 | - / 1ヶ月 | 1.0 | 5/11 | Y | 1972/4 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000615268 |
| 2.7 | シンフォニー四条河原町 | 2LDK | 53.46 | 130,000 | 20820 | 1ヶ月 / 2ヶ月 | 2.0 | 3/10 | Y | 2001/10 | SRC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000164710 |
| 2.7 | シンフォニー四条河原町 | 3LDK | 56.99 | 140,000 | 13300 | 2ヶ月 / 2ヶ月 | 2.0 | 3/10 | Y | 2001/10 | SRC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000281505 |
| 2.73 | 詩仙ハイムⅠ | 2LDK | 50.0 | 90,000 | 5000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/4 | n | 1979/1 | RC | 有 10,000円 ～ 0円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=130000706510 |
| 2.75 | せんぼん有彩館 | 3LDK | 71.23 | 133,000 | 15000 | - / - | 0.0 | 3/10 | Y | 1997/8 | SRC | 有 25,300円 | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000175356 |
| 2.75 | せんぼん有彩館 | 3LDK | 71.23 | 132,000 | 15000 | - / - | 0.0 | 2/10 | Y | 1997/8 | SRC | 有 25,300円 | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000175348 |
| 2.75 | せんぼん有彩館 | 3LDK | 71.23 | 134,000 | 15000 | - / - | 0.0 | 5/10 | Y | 1997/8 | SRC | 有 25,300円 | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000175352 |
| 2.76 | ペレニアルフラックス | 2LDK | 75.5 | 120,000 | 6000 | 1ヶ月 / 1ヶ月 | 1.0 | 2/3 | n | 1992/10 | RC | 有 15,400円 | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000222317 |
| 2.78 | ユアメゾン白川　１ | 2LDK | 63.0 | 125,000 | 6000 | 1ヶ月 / 2ヶ月 | 2.0 | 2/2 | n | 2026/10 | 軽量鉄骨 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000711583 |
| 2.84 | ラス・パルマス京小町 | 2LDK | 54.86 | 135,000 | 10000 | - / 1ヶ月 | 1.0 | 2/5 | Y | 2025/6 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=270000628349 |
| 2.85 | カーサ葵 | 3LDK | 68.14 | 140,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/3 | Y | 2001/4 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000172820 |
| 2.85 | 嶋津マンション | 3LDK | 60.0 | 125,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 4/7 | Y | 1991/8 | 鉄骨 | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000251258 |
| 2.87 | Ｄ－ＲＯＯＭ一乗寺 | 2LDK | 52.79 | 134,000 | 8000 | - / 1ヶ月 | 1.0 | 1/3 | n | 2024/10 | 軽量鉄骨 | 有 14,300円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=270000617008 |
| 2.87 | Ｄ－ＲＯＯＭ一乗寺 | 2LDK | 52.79 | 136,000 | 8000 | - / 1ヶ月 | 1.0 | 2/3 | n | 2024/10 | 軽量鉄骨 | 有 14,300円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=270000617010 |
| 2.87 | 洛翠舎 | 3LDK | 69.26 | 128,000 | 11000 | 1ヶ月 / 2ヶ月 | 2.0 | 4/9 | Y | 2001/2 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000173132 |
| 2.9 | コスモトゥデイ | 2LDK | 61.64 | 120,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 11/11 | Y | 1989/11 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000456892 |
| 2.9 | シャトレ西陣 | 2LDK | 45.0 | 90,000 | 5000 | - / 1ヶ月 | 1.0 | 7/7 | Y | 1977/4 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000099832 |
| 2.91 | ティファール | 3LDK | 69.08 | 138,000 | 11000 | 5万円 / 20万円 | 1.45 | 6/10 | Y | 1999/9 | SRC | 有 30,800円 | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000172533 |
| 2.92 | プリムローズ四条 | 2LDK | 52.67 | 117,000 | 5000 | - / 1ヶ月 | 1.0 | 7/10 | Y | 2007/11 | 鉄骨 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000229645 |
| 2.93 | コスモ二条 | 2LDK | 48.0 | 82,000 | 8000 | 10万円 / 15万円 | 1.83 | 5/11 | Y | 1985/11 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=020000366819 |
