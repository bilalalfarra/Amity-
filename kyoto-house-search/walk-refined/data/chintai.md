# chintai — CHINTAI (chintai.net), WALK3 survey (≤3.0 km of 京都技術科学センター, 左京区吉田河原町14; rent ≤140,000)

Run: 2026-10-18T17:07:18+09:00 (JST). Elapsed 179s. ~1 request/s, Chrome UA, plain requests+bs4.

## Server-side filters used
`/kyoto/area/<ward>/list/?ct=140&sf=45&m=6&m=8&m=9&m=A&m=B&m=C&m=D&m=E` — ct = 賃料上限14万円 (管理費別), sf = 専有面積 45㎡以上, m = 2LDK/3DK/3LDK/4K/4DK/4LDK/5K・5DK/5LDK+. No age / structure / floor filter.
Wards: 北区 26101, 上京区 26102, 左京区 26103, 中京区 26104, 東山区 26105, 下京区 26106. Distance ≤ 3.0 km applied client-side on the list card's own map coordinates (building level), GSI geocode as fallback.
Pagination: `/list/pageN/` URLs built by the script (the site's 次へ link drops the multi-valued `m=` params).
Rooms beyond 3 per building are collapsed (残りN件) and normally loaded via `/api/list/buildingProperties/` (robots.txt: Disallow /api/) → not called; instead the affected ward/query lists were re-read sorted by rent asc/desc (o=2/o=3) to surface those rooms.

## Pages scanned
| ward | query | site total | units seen | pages | extra sort pages |
|---|---|---|---|---|---|
| 北区 | all | 25 | 25 | 2 | 0 |
| 上京区 | all | 37 | 35 | 2 | 4 |
| 左京区 | all | 85 | 82 | 4 | 0 |
| 中京区 | all | 29 | 29 | 2 | 0 |
| 東山区 | all | 7 | 7 | 1 | 0 |
| 下京区 | all | 22 | 22 | 1 | 0 |

Buildings with collapsed rooms on the list page (残りN件) and how many unique rooms were collected:
- 賃貸マンション グランレブリー御所東Ⅱ (0.68 km): 3 shown + 1 hidden → 6 unique rooms collected
- 賃貸マンション せんぼん有彩館 (2.76 km): 3 shown + 1 hidden → 4 unique rooms collected
- 新築 賃貸ハイツ FAMILLE　MAISON (4.21 km): 3 shown + 3 hidden → 3 unique rooms collected

Unique units collected from lists: **202**; after list-level pre-filter: **81**; detail pages fetched: 81; **unit pages kept: 81** (before merging the same unit listed by several agencies; tiers after merging: see Result). Rent range kept: 68000–140000 円.

List-level rejections: > 3.0 km (list coords): 121

## Dropped after detail fetch

## Problems / notes
- No blocks or CAPTCHAs; all list and unit pages HTTP 200 (unit pages already fetched in the walk survey a few hours earlier were reused from ../walk/out/raw/chintai/).
- Rooms beyond 3 per building are collapsed on the list page; buildings within 3.2 km with collapsed rooms were re-read sorted by rent asc/desc (see list above).
- The same unit is often listed by several agencies under different bk- ids → merged by post.py (other URLs in notes).
- Coordinates come from each listing's own map link (building level).
- tier: house = 一戸建て/テラスハウス/貸家, A = built 2001+, B = 1991–2000, old = before 1991.

## Result
- **Kept 66 units** (after merging 15 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via the same building name in another listing with a full address, 0 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 5; rent range kept: 68000–140000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'old': 31, 'A': 16, 'house': 4, 'B': 15}; 礼金 ≤1ヶ月 51, >1ヶ月 15, unknown 0 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'site': 64, 'address (GSI)': 2} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 38/28/0; by ward: {'左京区': 25, '上京区': 28, '中京区': 10, '東山区': 1, '北区': 1, '下京区': 1}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/chintai/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.28 | 上阿達谷口マンション | 3DK | 46.12 | 110,000 | 6000 | 110,000円 (1.0ヶ月) / 110,000円 (1.0ヶ月) | 1.0 | 1/4 | n | 1989/4 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007100000000000643140018/ |
| 0.68 | グランレブリー御所東Ⅱ | 2LDK | 53.94 | 136,000 | 10000 | 0円 / 136,000円 (1.0ヶ月) | 1.0 | 1/3 | n | 1987/3 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007100000000005368040002/ |
| 0.68 | グランレブリー御所東Ⅱ | 2LDK | 53.94 | 138,000 | 10000 | 0円 / 138,000円 (1.0ヶ月) | 1.0 | 2/3 | n | 1987/3 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007100000000005368040003/ |
| 0.75 | サンアートビル | 3DK | 59.14 | 130,000 | 8000 | 0円 / 0円 | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 |  | old | https://www.chintai.net/detail/bk-0000007100000000007552830001/ |
| 0.9 | ドルフ聖護院 | 2LDK | 54.56 | 124,000 | 12000 | 0円 / 50,000円 (0.4ヶ月) | 0.4 | 1/3 | n | 2018/11 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-C010106042875200070072400001/ |
| 1.03 | 京都グランドハイツ | 2LDK | 64.5 | 140,000 | 10000 | 140,000円 (1.0ヶ月) / 140,000円 (1.0ヶ月) | 1.0 | 4/7 | Y | 1971/6 | RC | 自転車置き場 / バイク可 その他特徴： バイク | old | https://www.chintai.net/detail/bk-C010106042875200074890950001/ |
| 1.11 | 岡崎東福ノ川町貸家 | 3LDK+S | 107.96 | 135,000 | 0 | 0円 / 0円 | 0.0 | 1/3 | n | 1995/4 | 木造 | 無料駐車場 1台 / 自転車置き場 | house | https://www.chintai.net/detail/bk-0000007040000000007630790001/ |
| 1.14 | ＫＢ．メゾンロ－タス | 2LDK | 51.17 | 121,000 | 4600 | 0円 / 121,000円 (1.0ヶ月) | 1.0 | 1/3 | n | 2011/3 | 鉄骨 | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007100000000001822400002/ |
| 1.17 | メゾンフジ | 3LDK | 80.0 | 135,000 | 5000 | 0円 / 0円 | 0.0 | 2/5 | n | 1985/10 | 鉄骨 | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007040000000006120090005/ |
| 1.3 | 北白川コーポラス | 3DK | 66.0 | 100,000 | 8000 | 100,000円 (1.0ヶ月) / 100,000円 (1.0ヶ月) | 1.0 | 3/4 | n | 1970/10 | RC | 有料駐車場 1台 （8,000円/月） / 自転 | old | https://www.chintai.net/detail/bk-0000007100000000000383830006/ |
| 1.39 | アイル竹嶋 | 2LDK | 48.0 | 120,000 | 15000 | 0円 / 250,000円 (2.1ヶ月) | 2.1 | 5/6 | Y | 1993/3 | RC |  | B | https://www.chintai.net/detail/bk-0000007040000000000423330000/ |
| 1.46 | パラド－ル御所 | 3LDK | 63.18 | 130,000 | 15000 | 130,000円 (1.0ヶ月) / 260,000円 (2.0ヶ月) | 2.0 | 5/7 | Y | 1984/2 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007070000000000285520003/ |
| 1.58 | 藤波ﾋﾞﾙ | 2LDK | 48.0 | 114,000 | 4000 | 50,000円 (0.4ヶ月) / 100,000円 (0.9ヶ月) | 0.9 | 2/4 | n | 1990/3 | 鉄骨 | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007070000000000310430005/ |
| 1.58 | i.レジデンス御所北 | 2LDK | 54.08 | 134,000 | 7000 | 0円 / 200,000円 (1.5ヶ月) | 1.5 | 1/4 | n | 2014/3 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007070000000004947780005/ |
| 1.6 | リッツ岡崎 | 2LDK | 68.0 | 130,000 | 12000 | 100,000円 (0.8ヶ月) / 100,000円 (0.8ヶ月) | 0.8 | 2/3 | Y | 1990/2 | RC | 有料駐車場 1台 （22,000円/月） / 自 | old | https://www.chintai.net/detail/bk-0000007100000000000149690007/ |
| 1.61 | メゾンミュゲ | 2LDK | 64.98 | 130,000 | 5000 | 130,000円 (1.0ヶ月) / 260,000円 (2.0ヶ月) | 2.0 | 2/2 | n | 2020/6 | 軽量鉄骨 | 有料駐車場 1台 （12,000円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007100000000007564390001/ |
| 1.66 | 相国寺門前町貸家 | 2LDK+S | 62.72 | 120,000 | 0 | 0円 / 100,000円 (0.8ヶ月) | 0.8 | 1/2 | n | 1911/1 | 木造 | 自転車置き場 | house | https://www.chintai.net/detail/bk-0000007070000000006113080001/ |
| 1.71 | セラヴィー119 | 2LDK | 63.52 | 140,000 | 10000 | 140,000円 (1.0ヶ月) / 140,000円 (1.0ヶ月) | 1.0 | 5/5 | Y | 1989/6 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007100000000000209160007/ |
| 1.73 | 高野ロイヤルハイツ | 2LDK | 46.0 | 68,000 | 7000 | 0円 / 80,000円 (1.2ヶ月) | 1.2 | 3/4 | Y | 1977/10 | RC | 有料駐車場 1台 （16,500円/月） / 自 | old | https://www.chintai.net/detail/bk-0000007100000000000509260038/ |
| 1.74 | ピアレス円勝寺 | 2LDK | 62.41 | 120,000 | 20000 | 120,000円 (1.0ヶ月) / 120,000円 (1.0ヶ月) | 1.0 | 2/3 | Y | 1984/11 | RC | 有料駐車場 1台 （27,000円/月） / 自 | old | https://www.chintai.net/detail/bk-0000007100000000000206300011/ |
| 1.79 | プラネシア星の子御所西 | 2LDK | 60.2 | 114,000 | 9000 | 0円 / 171,000円 (1.5ヶ月) | 1.5 | 4/6 | n | 1973/5 | 鉄骨 | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007070000000000843990013/ |
| 1.79 | プラネシア星の子御所西 | 2LDK | 52.0 | 117,000 | 9000 | 0円 / 117,000円 (1.0ヶ月) | 1.0 | 2/6 | n | 1973/5 | 鉄骨 | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007070000000000843990010/ |
| 1.91 | サンレジデンス錦綾東堀川(904) | 3LDK | 74.8 | 120,000 | 10000 | 120,000円 (1.0ヶ月) / 120,000円 (1.0ヶ月) | 1.0 | 9/11 | n | 1982/11 | その他 | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007070000000007575860001/ |
| 1.93 | 浄土寺下南田町借家 | 3LDK | 70.0 | 100,000 | 0 | 100,000円 (1.0ヶ月) / 100,000円 (1.0ヶ月) | 1.0 | 1/2 | n | 1974/4 | 木造 | 自転車置き場 | house | https://www.chintai.net/detail/bk-0000007100000000001337400001/ |
| 1.93 | マナーハウス | 2LDK | 62.31 | 115,000 | 10000 | 115,000円 (1.0ヶ月) / 115,000円 (1.0ヶ月) | 1.0 | 1/4 | Y | 1996/1 | RC | 近隣駐車場 1台 （26,000円/月） ※80 | B | https://www.chintai.net/detail/bk-C010106042875200074892430001/ |
| 2.01 | マサール哲学の道 | 2LDK | 58.57 | 107,000 | 3500 | 0円 / 107,000円 (1.0ヶ月) | 1.0 | 2/2 | n | 2015/3 | 木造 | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007100000000005162800006/ |
| 2.1 | カストルム洛北 | 3LDK | 64.9 | 113,000 | 12000 | 100,000円 (0.9ヶ月) / 100,000円 (0.9ヶ月) | 0.9 | 2/7 | Y | 1983/4 | RC | 有料駐車場 1台 （22,000円/月） / 自 | old | https://www.chintai.net/detail/bk-0000007100000000000225140041/ |
| 2.1 | カストルム洛北 | 3LDK | 67.65 | 113,000 | 12000 | 100,000円 (0.9ヶ月) / 100,000円 (0.9ヶ月) | 0.9 | 3/7 | Y | 1983/4 | RC | 有料駐車場 1台 （22,000円/月） / 自 | old | https://www.chintai.net/detail/bk-0000007100000000000225140015/ |
| 2.14 | シェモア鞍馬口Ⅱ（１０６） | 2LDK | 54.86 | 105,000 | 10000 | 105,000円 (1.0ヶ月) / 105,000円 (1.0ヶ月) | 1.0 | 1/3 | n | 1984/11 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007070000000007527050001/ |
| 2.2 | グレ－スコ－ト堀川 | 2LDK | 50.0 | 87,000 | 5000 | 0円 / 150,000円 (1.7ヶ月) | 1.7 | 4/5 | Y | 1988/7 | 鉄骨 | 自転車置き場 / バイク可 その他特徴： バイク | old | https://www.chintai.net/detail/bk-0000007070000000001121500014/ |
| 2.21 | 京都一乗寺コーポラス(610) | 3DK | 45.37 | 85,000 | 0 | 0円 / 85,000円 (1.0ヶ月) | 1.0 | 6/7 | Y | 1976/7 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007100000000007523000001/ |
| 2.24 | ファ－ストコ－ト今出川北 | 3LDK | 60.32 | 98,000 | 10000 | 0円 / 98,000円 (1.0ヶ月) | 1.0 | 5/7 | Y | 1981/8 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007070000000000931380001/ |
| 2.28 | GRANDEUR　KAMANZA | 2LDK | 52.56 | 140,000 | 7000 | 140,000円 (1.0ヶ月) / 0円 | 0.0 | 2/5 | Y | 2011/11 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007140000000005602810002/ |
| 2.29 | カ－ネルヒル | 2LDK | 51.1 | 105,000 | 8000 | 100,000円 (1.0ヶ月) / 0円 | 0.0 | 2/5 | Y | 1989/10 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007140000000001428640012/ |
| 2.29 | カ－ネルヒル | 2LDK | 51.1 | 106,000 | 8000 | 100,000円 (0.9ヶ月) / 0円 | 0.0 | 4/5 | Y | 1989/10 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007140000000001428640004/ |
| 2.3 | シャトー高野 | 2LDK | 52.2 | 81,000 | 4000 | 0円 / 0円 | 0.0 | 4/4 | n | 1978/9 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007100000000000185970018/ |
| 2.31 | CASA SHIMEI | 2LDK | 53.0 | 92,000 | 10000 | 0円 / 92,000円 (1.0ヶ月) | 1.0 | 2/4 | n | 1991/7 | RC | 自転車置き場 | B | https://www.chintai.net/detail/bk-0000007070000000000570010002/ |
| 2.31 | グラシオン西陣 | 2LDK | 56.83 | 124,000 | 8000 | 200,000円 (1.6ヶ月) / 200,000円 (1.6ヶ月) | 1.6 | 3/11 | Y | 2004/3 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007070000000001638160003/ |
| 2.33 | ラヴィエール北白川 | 2LDK | 60.96 | 122,000 | 7000 | 122,000円 (1.0ヶ月) / 122,000円 (1.0ヶ月) | 1.0 | 1/2 | n | 2025/2 | 木造 | 有料駐車場 1台 （15,000円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007100000000007546570001/ |
| 2.38 | メゾンアルマ | 2LDK | 51.88 | 110,000 | 10000 | 110,000円 (1.0ヶ月) / 220,000円 (2.0ヶ月) | 2.0 | 5/6 | Y | 1989/3 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007140000000001268100004/ |
| 2.38 | 大晋メゾネ西陣今出川 | 2LDK+S | 65.55 | 125,000 | 9000 | 125,000円 (1.0ヶ月) / 125,000円 (1.0ヶ月) | 1.0 | 3/10 | Y | 1998/3 | SRC | 自転車置き場 | B | https://www.chintai.net/detail/bk-0000007070000000005720430010/ |
| 2.38 | 大晋メゾネ西陣今出川 | 3LDK | 74.81 | 130,000 | 9000 | 130,000円 (1.0ヶ月) / 130,000円 (1.0ヶ月) | 1.0 | 5/10 | Y | 1998/3 | SRC | 自転車置き場 | B | https://www.chintai.net/detail/bk-0000007070000000005720430009/ |
| 2.38 | 京都市営地下鉄東西線 二条城前駅 11階建  | 2LDK | 57.45 | 138,000 | 12180 | 0円 / 260,000円 (1.9ヶ月) | 1.9 | 2/11 | Y | 2005/11 | RC |  | A | https://www.chintai.net/detail/bk-C010106042875200068557290001/ |
| 2.39 | ヴューキャッスル | 3DK | 62.59 | 105,000 | 10000 | 0円 / 0円 | 0.0 | 3/5 | Y | 1992/6 | RC | 自転車置き場 | B | https://www.chintai.net/detail/bk-0000007070000000007329480004/ |
| 2.4 | 堀川シティハイツ(901) | 2LDK | 53.61 | 90,000 | 5000 | 90,000円 (1.0ヶ月) / 90,000円 (1.0ヶ月) | 1.0 | 9/11 | Y | 1976/9 | SRC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007070000000004904630001/ |
| 2.42 | ベルスーズ西陣 | 3LDK | 65.02 | 120,000 | 9500 | 0円 / 120,000円 (1.0ヶ月) | 1.0 | 5/6 | Y | 1998/7 | RC | 自転車置き場 | B | https://www.chintai.net/detail/bk-0000007070000000006809600003/ |
| 2.42 | ベルスーズ西陣 | 3LDK | 65.02 | 120,000 | 9500 | 0円 / 120,000円 (1.0ヶ月) | 1.0 | 3/6 | Y | 1998/7 | RC | 自転車置き場 | B | https://www.chintai.net/detail/bk-0000007070000000006809600002/ |
| 2.43 | コスモ星の子ハイツ | 3DK | 55.0 | 90,000 | 9000 | 0円 / 90,000円 (1.0ヶ月) | 1.0 | 4/7 | Y | 1985/9 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007070000000000525960014/ |
| 2.58 | パインフィールド二条城 | 2LDK | 52.77 | 139,000 | 8000 | 0円 / 0円 | 0.0 | 8/10 | Y | 1995/10 | RC | 有料駐車場 1台 （25,000円/月） ※駐車 | B | https://www.chintai.net/detail/bk-0000007260000000000955430006/ |
| 2.58 | パインフィールド二条城 | 2LDK | 50.45 | 139,000 | 8000 | 0円 / 0円 | 0.0 | 5/10 | Y | 1995/10 | SRC | 有料駐車場 1台 （27,500円/月） / 自 | B | https://www.chintai.net/detail/bk-0000007260000000000955430003/ |
| 2.62 | 賃貸テラスハウス フェリーチェ白川東 | 2LDK | 71.54 | 138,000 | 0 | 138,000円 (1.0ヶ月) / 276,000円 (2.0ヶ月) | 2.0 | 1/2 | n | 2026/5 | 木造 | 無料駐車場 1台 / 自転車置き場 / バイク可 | house | https://www.chintai.net/detail/bk-0000007100000000007577680001/ |
| 2.65 | ルネ紫野 | 2LDK | 59.8 | 85,000 | 4000 | 50,000円 (0.6ヶ月) / 100,000円 (1.2ヶ月) | 1.2 | 2/2 | n | 2005/4 | 木造 | 有料駐車場 1台 （15,000円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007070000000001351130005/ |
| 2.73 | ペレニアルフラックス | 2LDK | 75.5 | 120,000 | 6000 | 120,000円 (1.0ヶ月) / 120,000円 (1.0ヶ月) | 1.0 | 2/3 | n | 1992/8 | RC | 有料駐車場 1台 （15,400円/月） / 自 | B | https://www.chintai.net/detail/bk-0000007100000000006642180003/ |
| 2.75 | 詩仙ハイム | 2LDK | 47.0 | 90,000 | 5000 | 90,000円 (1.0ヶ月) / 90,000円 (1.0ヶ月) | 1.0 | 3/4 | n | 1979/6 | RC | 自転車置き場 / バイク可 | old | https://www.chintai.net/detail/bk-0000007100000000000227700009/ |
| 2.76 | せんぼん有彩館 | 3LDK | 71.2 | 132,000 | 15000 | 0円 / 0円 | 0.0 | 2/10 | Y | 1997/8 | 鉄骨 | 自転車置き場 その他特徴： バイク置場あり | B | https://www.chintai.net/detail/bk-0000007070000000006653350007/ |
| 2.76 | せんぼん有彩館 | 3LDK | 71.2 | 133,000 | 15000 | 0円 / 0円 | 0.0 | 3/10 | Y | 1997/8 | 鉄骨 | 有料駐車場 1台 （25,300円/月） / 自 | B | https://www.chintai.net/detail/bk-0000007070000000006653350012/ |
| 2.76 | せんぼん有彩館 | 3LDK | 71.2 | 134,000 | 15000 | 0円 / 0円 | 0.0 | 5/10 | Y | 1997/8 | 鉄骨 | 有料駐車場 1台 （25,300円/月） / 自 | B | https://www.chintai.net/detail/bk-0000007070000000006653350011/ |
| 2.78 | 賃貸マンション ユアメゾン 白川１ | 2LDK | 63.0 | 125,000 | 6000 | 125,000円 (1.0ヶ月) / 250,000円 (2.0ヶ月) | 2.0 | 2/2 | n | 2026/10 | 鉄骨 | 有料駐車場 1台 （15,400円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007100000000007575400004/ |
| 2.78 | リーガル京都二条城東 | 2LDK | 57.45 | 135,000 | 12180 | 0円 / 200,000円 (1.5ヶ月) | 1.5 | 6/11 | Y | 2005/11 | RC | 自転車置き場 / バイク可 その他特徴： バイク | A | https://www.chintai.net/detail/bk-C010106042875200059457890001/ |
| 2.84 | グランディール錦 | 2LDK | 58.87 | 110,000 | 18000 | 0円 / 0円 | 0.0 | 1/7 | Y | 1986/4 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007140000000000135840011/ |
| 2.84 | 嶋津マンション | 3LDK | 60.0 | 125,000 | 10000 | 125,000円 (1.0ヶ月) / 125,000円 (1.0ヶ月) | 1.0 | 4/7 | Y | 1991/7 | RC | 自転車置き場 | B | https://www.chintai.net/detail/bk-0000007140000000000220690010/ |
| 2.85 | カーサ葵 | 3LDK | 68.14 | 140,000 | 10000 | 140,000円 (1.0ヶ月) / 140,000円 (1.0ヶ月) | 1.0 | 3/3 | Y | 2001/3 | RC | 有料駐車場 1台 （20,900円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007260000000006359670001/ |
| 2.87 | Ｄ-ＲＯＯＭ一乗寺 | 2LDK | 52.79 | 134,000 | 8000 | 0円 / 134,000円 (1.0ヶ月) | 1.0 | 1/3 | n | 2024/10 | 鉄骨 | 有料駐車場 1台 （14,300円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007100000000007150840001/ |
| 2.87 | Ｄ-ＲＯＯＭ一乗寺 | 2LDK | 52.79 | 136,000 | 8000 | 0円 / 136,000円 (1.0ヶ月) | 1.0 | 2/3 | n | 2024/10 | 軽量鉄骨 | 有料駐車場 1台 （14,300円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007100000000007150840004/ |
| 2.9 | シャトレ西陣 | 2LDK | 45.0 | 90,000 | 5000 | 90,000円 (1.0ヶ月) / 90,000円 (1.0ヶ月) | 1.0 | 7/7 | Y | 1974/4 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007070000000001833270006/ |
| 2.94 | リーガル京都烏丸東 | 2LDK | 57.26 | 140,000 | 17110 | 0円 / 200,000円 (1.4ヶ月) | 1.4 | 2/5 | Y | 2016/3 | RC | 自転車置き場 / バイク可 その他特徴： バイク | A | https://www.chintai.net/detail/bk-C010106042875200059421580001/ |
