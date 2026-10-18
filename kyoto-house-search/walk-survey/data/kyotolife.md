# kyotolife — 京都ライフ (kyoto-life.co.jp), WALK survey (≤1.3 km of 京都技術科学センター, 左京区吉田河原町14), fetched 2026-10-18

## Method
- Own search (server-side HTML): `/app/search.php?__mode=search&by=area&search_type=building&prefecture_city_code[]=26-103&floor_plan_category_code[]=…&limit=50&offset=N`.
  floor_plan_category_code = RR0T1 (RR rooms, T 2=K 3=DK 4=LDK 5=SDK 6=SLDK): 2LDK/2SLDK, 3K/3DK/3LDK/3SDK/3SLDK, 4…6 rooms all types. No rent / area / age filter (area checked here).
- Site totals (buildings): 左京区 208, 上京区 95, 中京区 180 → 11 list pages, 483 buildings / 656 rooms. Raw: out/raw/kyotolife/list/.
- List addresses are town-level only → town geocode (通り名 stripped) with a 1.7 km margin: 501 rooms dropped as far, 7 by layout/area.
- 144 candidate unit pages `/app/search.php?__mode=room&room_code=<12 digits>` — all HTTP 200 (raw: out/raw/kyotolife/detail/). Final distance from the map pin embedded in the unit page (「この物件の周辺地図」 Google-maps iframe q=lat,lon): 85 dropped > 1.3 km.
- `parking` = 駐車場 cell verbatim (e.g. 「有 22,000円」「無し」); `elevator` from 条件・設備 (エレベーター). 京都ライフ is the 元付/管理 agent for many of these, several are not on the big portals.

## Result
- **Kept 58 units** (after merging 1 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via nearest station (noted in `notes`), 0 of them dropped as >1.3 km.
- Within 1.0 km: 43; rent range kept: 87000–470000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'house': 13, 'B': 2, 'old': 8, 'A': 35}; 礼金 ≤1ヶ月 30, >1ヶ月 28, unknown 0 (no 礼金 limit in this survey).
- Elevator yes/no/unknown: 35/23/0; by ward: {'左京区': 29, '上京区': 22, '中京区': 7}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/kyotolife/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.13 | 吉田中阿達町貸家 | 2LDK | 66.7 | 120,000 | 0 | - / 2ヶ月 | 2.0 | 1/2 | n | 2004/12 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000709278 |
| 0.16 | 今智庵 | 3DK | 65.0 | 100,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/2 | n | 1984/11 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000183992 |
| 0.17 | エーデルハイム鴨川 | 3LDK | 65.77 | 138,000 | 10000 | 20万円 / 35万円 | 2.54 | 5/5 | Y | 1997/2 | RC | 有 21,000円 | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000033844 |
| 0.28 | 上阿達谷口マンション | 3DK | 45.7 | 110,000 | 6000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/4 | n | 1989/4 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000034399 |
| 0.3 | 吉田上阿達町貸家 | 3DK | 45.75 | 100,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1960/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000711119 |
| 0.44 | Ｔｈｅ　Ｒｅｓｉｄｅｎｃｅ　御車道 | 2LDK | 59.7 | 192,000 | 10000 | 1ヶ月 / 20万円 | 1.04 | 2/4 | Y | 2026/8 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000707940 |
| 0.45 | Ｇｒａｎｄ　Ｅ’ｔｅｒｎａ　京大正門前 | 3LDK | 71.07 | 169,500 | 9000 | - / 2ヶ月 | 2.0 | 2/5 | Y | 2008/10 | RC | 有 23,100円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000259244 |
| 0.45 | Ｇｒａｎｄ　Ｅ’ｔｅｒｎａ　京大正門前 | 2LDK | 64.2 | 160,500 | 9000 | - / 2ヶ月 | 2.0 | 2/5 | Y | 2008/10 | RC | 有 23,100円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000259232 |
| 0.5 | ノーベルテラス稔 | 2LDK | 54.86 | 220,000 | 8000 | 1ヶ月 / 2ヶ月 | 2.0 | 4/5 | Y | 2003/3 | 鉄骨 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000067645 |
| 0.5 | ＢｅｌｌｅＬｅａｄ御所東 | 2LDK | 53.0 | 154,000 | 6000 | - / 1ヶ月 | 1.0 | 1/2 | n | 2025/9 | 木造 | 有 22,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000708214 |
| 0.5 | ＢｅｌｌｅＬｅａｄ御所東 | 2LDK | 61.69 | 174,000 | 6000 | - / 1ヶ月 | 1.0 | 1/2 | n | 2025/9 | 木造 | 有 22,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000708215 |
| 0.53 | 田中下柳町貸家 | 5K | 82.7 | 120,000 | 0 | 2ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1945/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000709842 |
| 0.59 | レジディア御所東 | 3LDK | 113.88 | 402,000 | 18000 | 1ヶ月 / - | 0.0 | 9/10 | Y | 2007/9 | RC | 有 25,300円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000227800 |
| 0.61 | ベリエ茶五 | 2LDK | 53.96 | 145,000 | 15000 | - / 1.5ヶ月 | 1.5 | 2/6 | Y | 2008/3 | RC | 有 16,500円 ～ 27,500円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000246039 |
| 0.61 | ベリエ茶五 | 2LDK | 54.72 | 150,000 | 15000 | - / 2ヶ月 | 2.0 | 3/6 | Y | 2008/3 | RC | 有 16,500円 ～ 27,500円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000246044 |
| 0.61 | ベリエ茶五 | 2LDK | 60.25 | 165,000 | 16000 | - / 2ヶ月 | 2.0 | 5/6 | Y | 2008/3 | RC | 有 16,500円 ～ 27,500円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000246049 |
| 0.61 | ベリエ茶五 | 2LDK | 60.25 | 190,000 | 17000 | - / 2ヶ月 | 2.0 | 6/6 | Y | 2008/3 | RC | 有 16,500円 ～ 27,500円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000473535 |
| 0.61 | ベリエ茶五 | 2LDK | 60.25 | 155,000 | 15000 | - / 2ヶ月 | 2.0 | 2/6 | Y | 2008/3 | RC | 有 16,500円 ～ 27,500円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000246051 |
| 0.61 | ベリエ茶五 | 2LDK | 60.25 | 160,000 | 15000 | - / 2ヶ月 | 2.0 | 4/6 | Y | 2008/3 | RC | 有 16,500円 ～ 27,500円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000246053 |
| 0.61 | ピアハウス出町 | 4LDK | 145.42 | 280,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/3 | n | 1998/11 | 鉄骨 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=270000633512 |
| 0.61 | 鴨川グランドコーポ | 2LDK | 95.22 | 470,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 4/5 | Y | 1981/5 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000706226 |
| 0.62 | エスタプレイス | 2LDK | 75.03 | 216,000 | 7500 | - / 1ヶ月 | 1.0 | 4/6 | Y | 2027/4 | RC | 有 22,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000707666 |
| 0.62 | エスタプレイス | 2LDK | 75.03 | 215,000 | 7500 | - / 1ヶ月 | 1.0 | 2/6 | Y | 2027/4 | RC | 有 22,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000707667 |
| 0.62 | エスタプレイス | 2LDK | 68.55 | 206,000 | 7500 | - / 1ヶ月 | 1.0 | 2/6 | Y | 2027/4 | RC | 有 22,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=130000706526 |
| 0.62 | エスタプレイス | 2LDK | 75.03 | 216,000 | 7500 | - / 1ヶ月 | 1.0 | 3/6 | Y | 2027/4 | RC | 有 22,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000707655 |
| 0.62 | エスタプレイス | 2LDK | 68.55 | 207,000 | 7500 | - / 1ヶ月 | 1.0 | 3/6 | Y | 2027/4 | RC | 有 22,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000707661 |
| 0.65 | 上京区南町貸家 | 4DK | 111.94 | 168,000 | 0 | 15万円 / 20万円 | 1.19 | 1/3 | n | 1994/2 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000329932 |
| 0.66 | イーグルコート聖護院 | 3LDK | 78.04 | 215,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 6/7 | Y | 2003/10 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=130000703084 |
| 0.67 | アルス丸太町山水庵 | 3LDK | 117.57 | 280,000 | 17100 | 1ヶ月 / 2ヶ月 | 2.0 | 5/5 | Y | 2002/3 | RC | 有 23,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=130000711027 |
| 0.68 | グランレブリー御所東Ⅱ | 2LDK | 53.94 | 138,000 | 10000 | - / 1ヶ月 | 1.0 | 2/3 | n | 1987/3 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000157006 |
| 0.68 | グランレブリー御所東Ⅱ | 2LDK | 53.94 | 136,000 | 10000 | - / 1ヶ月 | 1.0 | 1/3 | n | 1987/3 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000225273 |
| 0.74 | サンアートビル | 3LDK | 59.14 | 130,000 | 8000 | - / - | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=040000159928 |
| 0.78 | 東丸太町貸家 | 3SLDK | 90.0 | 135,000 | 0 | - / 1ヶ月 | 1.0 | 1/2 | n | 1950/5 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000532383 |
| 0.8 | ＢＲＩＧＨ　ＳＴＯＮＥ御所北 | 2LDK | 52.03 | 174,000 | 10000 | 1ヶ月 / 2ヶ月 | 2.0 | 1/3 | Y | 2024/10 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=130000703995 |
| 0.81 | 吉田中大路町アパート | 2LDK | 49.66 | 87,000 | 3000 | - / - | 0.0 | 1/2 | n | 2002/10 | 木造 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000569511 |
| 0.83 | 吉田近衛町貸家 | 4LDK | 50.34 | 150,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/2 | n | 1975/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000705334 |
| 0.85 | リーガル京都聖護院 | 2LDK | 66.0 | 163,000 | 14030 | - / 1ヶ月 | 1.0 | 1/5 | Y | 2018/10 | RC | 有 22,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000467730 |
| 0.85 | リーガル京都聖護院 | 2LDK | 66.0 | 165,000 | 14030 | - / 20万円 | 1.21 | None/5 | Y | 2018/10 | RC | 有 22,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000467731 |
| 0.85 | リーガル京都聖護院 | 2LDK | 66.0 | 168,000 | 14030 | - / 20万円 | 1.19 | 3/5 | Y | 2018/10 | RC | 有 22,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000467853 |
| 0.91 | ザ・パークハウス京都聖護院 | 2LDK | 58.45 | 250,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/5 | Y | 2026/8 | 鉄骨 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000713029 |
| 0.91 | 聖護院東町貸家 | 4SLDK | 145.0 | 230,000 | 0 | 30万円 / 40万円 | 1.74 | 1/3 | n | 1992/3 | 鉄骨 | 込 | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000424214 |
| 0.96 | かぐら坂荘 | 2LDK | 60.23 | 128,000 | 7000 | - / 12.8万円 | 1.0 | 3/3 | n | 2011/3 | RC | 有 19,800円 ～ 22,000円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000319551 |
| 1.0 | プレージア京都聖護院ノ邸 | 3LDK | 73.75 | 210,000 | 20000 | 1ヶ月 / 2ヶ月 | 2.0 | 1/3 | Y | 2017/1 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000449787 |
| 1.01 | ファインフラッツ京都神宮 | 2LDK | 54.25 | 185,000 | 15000 | 1ヶ月 / 1ヶ月 | 1.0 | 2/5 | Y | 2013/11 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000712182 |
| 1.02 | ザ・京都レジデンス御所南 | 2LDK | 56.13 | 210,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 2/5 | Y | 2016/12 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000564768 |
| 1.03 | 京都グランドハイツ | 2LDK | 64.5 | 140,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 4/7 | Y | 1971/6 | SRC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=260000633818 |
| 1.03 | 中京区寺町通　貸戸建 | 4LDK | 132.36 | 220,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1927/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=030000547543 |
| 1.04 | サンシティ御所南 | 3LDK | 89.44 | 260,000 | 10000 | 1ヶ月 / 2ヶ月 | 2.0 | 3/3 | Y | 2006/3 | RC | 有 33,000円 ～ 3,300円 | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=210000708979 |
| 1.09 | 吉田本町洋風外観京町家 | 5DK | 138.54 | 330,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1930/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000696614 |
| 1.16 | フォルム聖護院別邸 | 3LDK | 72.57 | 168,000 | 12000 | - / 20万円 | 1.19 | 3/5 | n | 2001/6 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000707632 |
| 1.16 | ベルリード　Ｍｉｌｌｅｓｉｍｅ寺町 | 2LDK | 69.97 | 230,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 2/3 | n | 2026/11 | 木造 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=130000707877 |
| 1.17 | 田中野神町貸家 | 6DK | 145.36 | 150,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/4 | n | 1976/8 | 鉄骨 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000637390 |
| 1.17 | ヴィークコート京都河原町二条 | 3LDK | 75.13 | 380,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 7/7 | Y | 2023/6 | RC | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=210000710122 |
| 1.19 | 岡崎最勝寺町貸家 | 6DK | 118.57 | 228,000 | 0 | 1ヶ月 / 25.08万円 | 1.1 | 1/2 | n | 1914/1 | 木造 | 無し | house | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000701881 |
| 1.21 | コーポ富有 | 2LDK | 48.51 | 100,000 | 9000 | 10万円 / 10万円 | 1.0 | 2/4 | Y | 1985/7 | RC | 無し | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=210000685310 |
| 1.23 | 山和小路 | 3DK | 66.97 | 125,000 | 10000 | - / 1ヶ月 | 1.0 | 5/5 | Y | 1999/11 | RC | 無し | B | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000221493 |
| 1.26 | フロンテージ堺町御門 | 2LDK | 68.44 | 225,000 | 9000 | 5万円 / 45万円 | 2.0 | 2/3 | Y | 2023/3 | 重量鉄骨 | 無し | A | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=210000708694 |
| 1.3 | 北白川コーポラス | 3LDK | 66.0 | 100,000 | 8000 | 10万円 / 10万円 | 1.0 | 3/4 | n | 1970/3 | RC | 有 8,000円 | old | https://www.kyoto-life.co.jp/app/search.php?__mode=room&room_code=120000219169 |
