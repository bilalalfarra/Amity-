# chintai — CHINTAI (chintai.net), WALK survey (≤1.3 km of 京都技術科学センター, 左京区吉田河原町14)

Run: 2026-10-18T12:14:01+09:00 (JST). Elapsed 106s. ~1 request/s, Chrome UA, plain requests+bs4.

## Server-side filters used
`/kyoto/area/<ward>/list/?sf=45&m=6&m=8&m=9&m=A&m=B&m=C&m=D&m=E` — sf = 専有面積 45㎡以上, m = 2LDK/3DK/3LDK/4K/4DK/4LDK/5K・5DK/5LDK+. No rent cap (ct omitted = 上限なし), no age / structure / floor filter.
Wards: 左京区 26103, 上京区 26102, 中京区 26104. Distance ≤ 1.3 km applied client-side on the list card's own map coordinates (building level), GSI geocode as fallback.
Pagination: `/list/pageN/` URLs built by the script (the site's 次へ link drops the multi-valued `m=` params).
Rooms beyond 3 per building are collapsed (残りN件) and normally loaded via `/api/list/buildingProperties/` (robots.txt: Disallow /api/) → not called; instead the affected ward/query lists were re-read sorted by rent asc/desc (o=2/o=3) to surface those rooms.

## Pages scanned
| ward | query | site total | units seen | pages | extra sort pages |
|---|---|---|---|---|---|
| 左京区 | all | 127 | 120 | 5 | 10 |
| 上京区 | all | 109 | 86 | 3 | 6 |
| 中京区 | all | 159 | 139 | 5 | 0 |

Buildings with collapsed rooms on the list page (残りN件) and how many unique rooms were collected:
- 賃貸マンション GrandEterna京大正門前 (0.45 km): 3 shown + 1 hidden → 4 unique rooms collected
- 新築 賃貸ハイツ ラフィーネ松ヶ崎 (2.67 km): 3 shown + 2 hidden → 5 unique rooms collected
- 新築 賃貸ハイツ FAMILLE　MAISON (4.21 km): 3 shown + 3 hidden → 6 unique rooms collected
- 賃貸マンション リーガル京都聖護院 (0.86 km): 3 shown + 1 hidden → 4 unique rooms collected
- 新築 賃貸マンション ウエストフィールド (2.81 km): 3 shown + 5 hidden → 9 unique rooms collected
- 賃貸マンション sawarabi御所 (1.41 km): 3 shown + 3 hidden → 5 unique rooms collected
- 賃貸マンション 御所西ロイヤルプラザ (2.03 km): 3 shown + 1 hidden → 4 unique rooms collected
- 賃貸マンション グランレブリー御所東Ⅱ (0.68 km): 3 shown + 1 hidden → 6 unique rooms collected
- 新築 賃貸マンション 仮)D-room上京区米屋町ハイツ (1.91 km): 3 shown + 3 hidden → 6 unique rooms collected
- 新築 賃貸マンション エスタプレイス (0.62 km): 3 shown + 2 hidden → 5 unique rooms collected
- 賃貸マンション ベリエ茶五 (0.62 km): 3 shown + 3 hidden → 7 unique rooms collected
- 賃貸マンション せんぼん有彩館 (2.76 km): 3 shown + 1 hidden → 4 unique rooms collected
- 賃貸マンション LiveCasa千本今出川 (3.08 km): 3 shown + 3 hidden → 3 unique rooms collected
- 新築 賃貸マンション LiveCasa千本今出川 (3.08 km): 3 shown + 3 hidden → 2 unique rooms collected
- 賃貸アパート ヴァン　ソレイユ　二条 (2.97 km): 3 shown + 1 hidden → 3 unique rooms collected
- 新築 賃貸マンション attrice円町 (3.92 km): 3 shown + 6 hidden → 3 unique rooms collected
- 新築 賃貸マンション デュオフラッツ京都四条 (2.74 km): 3 shown + 1 hidden → 3 unique rooms collected
- 賃貸マンション IL ROSSO堀川六角 (2.68 km): 3 shown + 3 hidden → 3 unique rooms collected
- 新築 賃貸マンション カーサ壬生寺道 (3.45 km): 3 shown + 5 hidden → 3 unique rooms collected
- 新築 賃貸マンション GRAN　LUXE御所南 (1.54 km): 3 shown + 4 hidden → 3 unique rooms collected

Unique units collected from lists: **370**; after list-level pre-filter: **56**; detail pages fetched: 56; **unit pages kept: 56** (before merging the same unit listed by several agencies; tiers after merging: see Result). Rent range kept: 100000–402000 円.

List-level rejections: > 1.3 km (list coords): 314

## Dropped after detail fetch

## Problems / notes
- No blocks or CAPTCHAs; every list and unit page used is an HTTP 200 copy saved under out/raw/chintai/ (12:08–12:13 JST, 左京区 p1–5 refreshed 12:48). A later refresh at 12:48 JST got 504 / read timeouts from chintai.net for the other pages, so the earlier copies (same session, < 1 h old) were used — nothing was retried aggressively.
- Rooms beyond 3 per building are collapsed on the list page; every building within 1.5 km that had collapsed rooms was re-read sorted by rent asc/desc and all its rooms were recovered (see list above).
- The same unit is often listed by several agencies under different bk- ids → merged by post.py (other URLs in notes).
- Coordinates come from each listing's own map link (building level), so distances are accurate to the building.
- tier: house = 一戸建て/テラスハウス/貸家, A = built 2001+, B = 1991–2000, old = before 1991.

## Result
- **Kept 39 units** (after merging 17 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via the same building name in another listing with a full address, 0 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 27; rent range kept: 100000–402000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'old': 8, 'A': 28, 'house': 2, 'B': 1}; 礼金 ≤1ヶ月 20, >1ヶ月 19, unknown 0 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'site': 39} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 29/10/0; by ward: {'左京区': 19, '上京区': 14, '中京区': 6}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/chintai/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.28 | 上阿達谷口マンション | 3DK | 46.12 | 110,000 | 6000 | 110,000円 (1.0ヶ月) / 110,000円 (1.0ヶ月) | 1.0 | 1/4 | n | 1989/4 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007100000000000643140018/ |
| 0.45 | GrandEterna京大正門前 | 2LDK | 64.2 | 160,500 | 9000 | 0円 / 321,000円 (2.0ヶ月) | 2.0 | 2/5 | Y | 2008/9 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007100000000001542520016/ |
| 0.45 | GrandEterna京大正門前 | 2LDK | 64.9 | 163,000 | 9000 | 0円 / 326,000円 (2.0ヶ月) | 2.0 | 4/5 | Y | 2008/9 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007100000000001542520005/ |
| 0.45 | GrandEterna京大正門前 | 2LDK | 64.2 | 163,500 | 9000 | 0円 / 327,000円 (2.0ヶ月) | 2.0 | 3/5 | Y | 2008/9 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007100000000001542520026/ |
| 0.45 | GrandEterna京大正門前 | 3LDK | 71.07 | 168,500 | 11000 | 0円 / 337,000円 (2.0ヶ月) | 2.0 | 2/5 | Y | 2008/9 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007100000000001542520024/ |
| 0.45 | THE　Residence　御車道 | 2LDK | 59.7 | 192,000 | 10000 | 192,000円 (1.0ヶ月) / 200,000円 (1.0ヶ月) | 1.0 | 2/4 | Y | 2026/8 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007070000000007536630005/ |
| 0.5 | ノーベルテラス稔 | 2LDK | 57.76 | 220,000 | 8000 | 220,000円 (1.0ヶ月) / 440,000円 (2.0ヶ月) | 2.0 | 4/5 | Y | 2003/3 | 鉄骨 | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007100000000006404270003/ |
| 0.61 | ベリエ茶五 | 2LDK | 54.72 | 150,000 | 15000 | 0円 / 300,000円 (2.0ヶ月) | 2.0 | 3/6 | Y | 2008/3 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007070000000001469890013/ |
| 0.62 | ベリエ茶五 | 2LDK | 53.96 | 145,000 | 15000 | 0円 / 217,500円 (1.5ヶ月) | 1.5 | 2/6 | Y | 2008/3 | RC | 自転車置き場 / バイク可 その他特徴： バイク | A | https://www.chintai.net/detail/bk-C010100181111500031748570001/ |
| 0.62 | ベリエ茶五 | 2LDK | 60.25 | 155,000 | 15000 | 0円 / 310,000円 (2.0ヶ月) | 2.0 | 2/6 | Y | 2008/3 | RC | 自転車置き場 / バイク可 その他特徴： バイク | A | https://www.chintai.net/detail/bk-C010100181111500053850060001/ |
| 0.62 | 賃貸マンション エスタプレイス | 2LDK | 68.55 | 206,000 | 7500 | 0円 / 206,000円 (1.0ヶ月) | 1.0 | 2/6 | Y | 2027/4 | RC | 有料駐車場 1台 （22,000円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007100000000007557360001/ |
| 0.62 | 賃貸マンション エスタプレイス | 2LDK | 68.55 | 207,000 | 7500 | 0円 / 207,000円 (1.0ヶ月) | 1.0 | 3/6 | Y | 2027/4 | RC | 有料駐車場 1台 （22,000円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007100000000007557360005/ |
| 0.62 | 賃貸マンション エスタプレイス | 2LDK | 73.03 | 215,000 | 7500 | 0円 / 215,000円 (1.0ヶ月) | 1.0 | 2/6 | Y | 2027/4 | RC | 有料駐車場 1台 （22,000円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007100000000007557360004/ |
| 0.62 | 賃貸マンション エスタプレイス | 2LDK | 73.03 | 216,000 | 7500 | 0円 / 216,000円 (1.0ヶ月) | 1.0 | 4/6 | Y | 2027/4 | RC | 有料駐車場 1台 （22,000円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007100000000007557360010/ |
| 0.62 | 賃貸マンション エスタプレイス | 2LDK | 73.03 | 216,000 | 7500 | 0円 / 216,000円 (1.0ヶ月) | 1.0 | 3/6 | Y | 2027/4 | RC | 有料駐車場 1台 （22,000円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007100000000007557360008/ |
| 0.65 | イーグルコート聖護院(605) | 3LDK | 78.04 | 215,000 | 10000 | 215,000円 (1.0ヶ月) / 215,000円 (1.0ヶ月) | 1.0 | 6/7 | Y | 2003/3 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007100000000007471490001/ |
| 0.65 | レジディア御所東 | 3LDK | 113.88 | 402,000 | 18000 | 402,000円 (1.0ヶ月) / 0円 | 0.0 | 9/10 | Y | 2007/9 | RC | 有料駐車場 1台 （25,300円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007100000000001376480002/ |
| 0.68 | グランレブリー御所東Ⅱ | 2LDK | 53.94 | 136,000 | 10000 | 0円 / 136,000円 (1.0ヶ月) | 1.0 | 1/3 | n | 1987/3 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007100000000005368040002/ |
| 0.68 | グランレブリー御所東Ⅱ | 2LDK | 53.94 | 138,000 | 10000 | 0円 / 138,000円 (1.0ヶ月) | 1.0 | 2/3 | n | 1987/3 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007100000000005368040003/ |
| 0.75 | サンアートビル | 3DK | 59.14 | 130,000 | 8000 | 0円 / 0円 | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 |  | old | https://www.chintai.net/detail/bk-0000007100000000007552830001/ |
| 0.76 | 聖護院アパルトメント | 2LDK | 94.4 | 190,000 | 4000 | 0円 / 0円 | 0.0 | 4/4 | n | 1977/1 | RC | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007100000000000294430013/ |
| 0.79 | BRIGH　STONE　御所北 | 2LDK | 52.01 | 174,000 | 10000 | 174,000円 (1.0ヶ月) / 348,000円 (2.0ヶ月) | 2.0 | 1/3 | Y | 2024/9 | 鉄骨 | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007070000000007126300010/ |
| 0.86 | リーガル京都聖護院 | 2LDK | 66.0 | 165,000 | 14030 | 0円 / 200,000円 (1.2ヶ月) | 1.2 | 1/5 | Y | 2018/11 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-C010106042875200059517740001/ |
| 0.86 | リーガル京都聖護院 | 2LDK | 66.0 | 168,000 | 14030 | 0円 / 200,000円 (1.2ヶ月) | 1.2 | 3/5 | Y | 2018/11 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-C010106042875200059584690001/ |
| 0.87 | 吉田上大路町19番地1貸家 | 3LDK+S | 94.92 | 230,000 | 0 | 230,000円 (1.0ヶ月) / 460,000円 (2.0ヶ月) | 2.0 | 1/2 | n | 2016/1 | 木造 | 無料駐車場 1台 / 自転車置き場 | house | https://www.chintai.net/detail/bk-0000007100000000007540850001/ |
| 0.9 | ドルフ聖護院 | 2LDK | 54.56 | 124,000 | 12000 | 0円 / 50,000円 (0.4ヶ月) | 0.4 | 1/3 | n | 2018/11 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-C010106042875200070072400001/ |
| 0.98 | ベレヴュー聖護院（６０１） | 3LDK | 65.28 | 150,000 | 0 | 150,000円 (1.0ヶ月) / 150,000円 (1.0ヶ月) | 1.0 | 6/7 | Y | 1994/12 | RC | 自転車置き場 | B | https://www.chintai.net/detail/bk-0000007100000000007518180001/ |
| 1.03 | 京都グランドハイツ | 2LDK | 64.5 | 140,000 | 10000 | 140,000円 (1.0ヶ月) / 140,000円 (1.0ヶ月) | 1.0 | 4/7 | Y | 1971/6 | RC | 自転車置き場 / バイク可 その他特徴： バイク | old | https://www.chintai.net/detail/bk-C010106042875200074890950001/ |
| 1.06 | サンシティ御所南 | 3LDK | 89.44 | 260,000 | 10000 | 260,000円 (1.0ヶ月) / 520,000円 (2.0ヶ月) | 2.0 | 3/3 | Y | 2006/3 | RC | 有料駐車場 1台 （30,000円/月） / 自 | A | https://www.chintai.net/detail/bk-0000007140000000001163850008/ |
| 1.11 | 岡崎東福ノ川町貸家 | 3LDK+S | 107.96 | 135,000 | 0 | 0円 / 0円 | 0.0 | 1/3 | n | 1995/4 | 木造 | 無料駐車場 1台 / 自転車置き場 | house | https://www.chintai.net/detail/bk-0000007040000000007630790001/ |
| 1.14 | ＫＢ．メゾンロ－タス | 2LDK | 51.17 | 121,000 | 4600 | 0円 / 121,000円 (1.0ヶ月) | 1.0 | 1/3 | n | 2011/3 | 鉄骨 | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007100000000001822400002/ |
| 1.17 | メゾンフジ | 3LDK | 80.0 | 135,000 | 5000 | 0円 / 0円 | 0.0 | 2/5 | n | 1985/10 | 鉄骨 | 自転車置き場 | old | https://www.chintai.net/detail/bk-0000007040000000006120090005/ |
| 1.19 | フォルム聖護院別邸(303) | 3LDK | 72.57 | 168,000 | 12000 | 0円 / 200,000円 (1.2ヶ月) | 1.2 | 3/5 | Y | 2001/6 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007100000000007590540001/ |
| 1.22 | ジオ御所南河原町二条(501) | 2LDK | 66.49 | 230,000 | 17950 | 230,000円 (1.0ヶ月) / 247,950円 (1.1ヶ月) | 1.1 | 5/7 | Y | 2013/9 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007140000000007567860001/ |
| 1.25 | ベルフォーレ御所南 | 2LDK | 60.04 | 198,000 | 12000 | 0円 / 396,000円 (2.0ヶ月) | 2.0 | 3/3 | Y | 2023/9 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-C010106042875200073800510001/ |
| 1.27 | 賃貸マンション 仮)ROUAGE御所南 | 2LDK | 76.29 | 260,000 | 20000 | 0円 / 520,000円 (2.0ヶ月) | 2.0 | 2/5 | Y | 2026/4 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007140000000007458430002/ |
| 1.27 | 賃貸マンション 仮)ROUAGE御所南 | 2LDK | 76.29 | 265,000 | 20000 | 0円 / 530,000円 (2.0ヶ月) | 2.0 | 3/5 | Y | 2026/4 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007140000000007458430004/ |
| 1.27 | 賃貸マンション 仮)ROUAGE御所南 | 2LDK | 76.29 | 270,000 | 20000 | 0円 / 540,000円 (2.0ヶ月) | 2.0 | 4/5 | Y | 2026/4 | RC | 自転車置き場 | A | https://www.chintai.net/detail/bk-0000007140000000007458430006/ |
| 1.3 | 北白川コーポラス | 3DK | 66.0 | 100,000 | 8000 | 100,000円 (1.0ヶ月) / 100,000円 (1.0ヶ月) | 1.0 | 3/4 | n | 1970/10 | RC | 有料駐車場 1台 （8,000円/月） / 自転 | old | https://www.chintai.net/detail/bk-0000007100000000000383830006/ |
