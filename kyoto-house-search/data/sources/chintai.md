# CHINTAI (chintai.net) — summary

Run: 2026-10-01T23:30:14+09:00 (JST). Elapsed 107s. ~1 request/s, Chrome UA, plain requests+bs4.

## Server-side filters used
`/kyoto/area/<ward>/list/?ct=100&sf=45&m=6&m=8&m=9&m=A&m=B&m=C&m=D&m=E` (+`h=7` for tier A = 築25年以内, or `kz=1` 鉄筋系 with no age cap for tier-B candidates).
ct = 賃料上限 10万円 (管理費を含まない: `k=1` not sent), sf = 専有面積 45㎡以上, m = 2LDK/3DK/3LDK/4K/4DK/4LDK/5K・5DK/5LDK+.
Not available server-side: floor ≠ 1F (only an *include 1F* checkbox exists), elevator, 礼金 ≤ 1 month, exact year range 1991–2000 → applied client-side.
Pagination: `/list/pageN/` URLs built by the script (the site's 次へ link drops the multi-valued `m=` params).
Rooms beyond 3 per building are collapsed (残りN件) and normally loaded via `/api/list/buildingProperties/` (robots.txt: Disallow /api/) → not called; instead the affected ward/query lists were re-read sorted by rent asc/desc (o=2/o=3) to surface those rooms.

## Pages scanned
| ward | query | site total | units seen | pages | extra sort pages |
|---|---|---|---|---|---|
| 下京区 | A | 0 | 0 | 1 | 0 |
| 下京区 | B | 3 | 3 | 1 | 0 |
| 中京区 | A | 0 | 0 | 1 | 0 |
| 中京区 | B | 3 | 3 | 1 | 0 |
| 南区 | A | 6 | 6 | 1 | 0 |
| 南区 | B | 30 | 30 | 2 | 0 |
| 右京区 | A | 10 | 10 | 1 | 0 |
| 右京区 | B | 57 | 55 | 2 | 4 |
| 上京区 | A | 1 | 1 | 1 | 0 |
| 上京区 | B | 4 | 4 | 1 | 0 |
| 西京区 | A | 10 | 10 | 1 | 0 |
| 西京区 | B | 100 | 99 | 4 | 8 |
| 東山区 | A | 0 | 0 | 1 | 0 |
| 東山区 | B | 2 | 2 | 1 | 0 |
| 北区 | A | 3 | 3 | 1 | 0 |
| 北区 | B | 8 | 8 | 1 | 0 |
| 伏見区 | A | 22 | 20 | 1 | 2 |
| 伏見区 | B | 65 | 60 | 3 | 6 |
| 左京区 | A | 8 | 8 | 1 | 0 |
| 左京区 | B | 21 | 21 | 1 | 0 |

Buildings with collapsed rooms on the list page (残りN件) and how many unique rooms were collected:
- 賃貸マンション 嵯峨野ロイヤルハイツ: 3 shown + 1 hidden → 4 unique rooms collected
- 賃貸マンション シャトー嵐望Ⅰ: 3 shown + 1 hidden → 4 unique rooms collected
- 賃貸マンション エントリ－ト木村: 3 shown + 1 hidden → 4 unique rooms collected
- 賃貸マンション ロイヤルメドウ: 3 shown + 2 hidden → 4 unique rooms collected
- 賃貸マンション ｲﾝﾍﾟﾘｱﾙﾊﾟﾚｽ ﾘﾊﾞ-ｻｲﾄﾞ: 3 shown + 2 hidden → 5 unique rooms collected
- 賃貸マンション ＡＺハウス: 3 shown + 1 hidden → 4 unique rooms collected

Unique units collected from lists: **335**; after list-level pre-filter: **111**; detail pages fetched: 111; **kept: 60** (A: 3, B: 57, house: 0).

List-level rejections: age/structure rule: 142, 1F: 43, reikin>1 month: 39

## Dropped after detail fetch
- ラ・メゾン・ボヌール (3LDK, 87000円, 4F, 1994) — floor 4 without confirmed elevator (elevator=False) — https://www.chintai.net/detail/bk-0000007060000000000132220000/
- サンシャインガーデン嵯峨嵐山A (2LDK, 93000円, 2F, 2017) — distance 6.32 km > 5.5 — https://www.chintai.net/detail/bk-0000007230000000005598530009/
- コープ・ミール花園 (3LDK, 93000円, 4F, 1992) — floor 4 without confirmed elevator (elevator=False) — https://www.chintai.net/detail/bk-0000007230000000007137330002/
- ハッピ－パレスＴ．Ｔ (3LDK, 97000円, 6F, 1997) — distance 6.42 km > 5.5 — https://www.chintai.net/detail/bk-0000007060000000000387210024/
- メゾン･ド･リッツ (2LDK, 72000円, 4F, 1994) — distance 6.87 km > 5.5 — https://www.chintai.net/detail/bk-0000007060000000000140830006/
- ロイヤルコート ワダ (2LDK, 85000円, 3F, 1993) — distance 6.67 km > 5.5 — https://www.chintai.net/detail/bk-0000007060000000000100250011/
- エントリ－ト木村 (2LDK, 55000円, 3F, 1994) — distance 6.57 km > 5.5 — https://www.chintai.net/detail/bk-0000007060000000001290910001/
- エントリ－ト木村 (2LDK, 55000円, 3F, 1994) — distance 6.57 km > 5.5 — https://www.chintai.net/detail/bk-0000007060000000001290910012/
- エントリ－ト木村 (2LDK, 54000円, 4F, 1994) — floor 4 without confirmed elevator (elevator=False) — https://www.chintai.net/detail/bk-0000007060000000001290910002/
- エントリ－ト木村 (2LDK, 55000円, 3F, 1994) — distance 6.57 km > 5.5 — https://www.chintai.net/detail/bk-0000007060000000001290910005/
- ShaMaison THE SHIP NISHIGAMO (2LDK, 98000円, 2F, 2016) — distance 7.74 km > 5.5 — https://www.chintai.net/detail/bk-0000007070000000006746260005/
- ルモール・北 (2LDK, 67000円, 2F, 1994) — distance 8.27 km > 5.5 — https://www.chintai.net/detail/bk-2000000180000000000020610008/
- プレアデス京都北山 (2LDK, 75000円, 2F, 1993) — distance 6.82 km > 5.5 — https://www.chintai.net/detail/bk-0000007070000000000739760013/
- スクエアコート (2LDK, 67000円, 2F, 1991) — distance 5.84 km > 5.5 — https://www.chintai.net/detail/bk-0000007070000000007285550004/
- スクエアコート (2LDK, 70000円, 3F, 1991) — distance 5.84 km > 5.5 — https://www.chintai.net/detail/bk-0000007070000000007285550002/
- 賃貸アパート 翆-SUI-I番邸 (2LDK, 79000円, 2F, 2026) — distance 6.54 km > 5.5 — https://www.chintai.net/detail/bk-2000000180000000000070640001/
- ロイヤルメドウ (2LDK, 72000円, 3F, 2010) — distance 7.1 km > 5.5 — https://www.chintai.net/detail/bk-0000007080000000001744750018/
- ロイヤルメドウ (2LDK, 72000円, 3F, 2010) — distance 7.1 km > 5.5 — https://www.chintai.net/detail/bk-0000007080000000001744750004/
- ロイヤルメドウ (2LDK, 72000円, 3F, 2010) — distance 7.1 km > 5.5 — https://www.chintai.net/detail/bk-0000007080000000001744750009/
- メゾン・カナール (3LDK, 100000円, 2F, 2015) — distance 6.89 km > 5.5 — https://www.chintai.net/detail/bk-2000000180000000000038230013/
- メゾン・カナール (3LDK, 100000円, 2F, 2015) — distance 6.89 km > 5.5 — https://www.chintai.net/detail/bk-0000007080000000005168120011/
- Nourish Cosiyo (2LDK, 82500円, 2F, 2014) — distance 7.21 km > 5.5 — https://www.chintai.net/detail/bk-0000007080000000005048540007/
- パステルヒルズ (2LDK, 71000円, 3F, 2009) — distance 7.6 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000001594920008/
- パステルヒルズ (2LDK, 72000円, 2F, 2009) — distance 7.6 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000001594920001/
- ヴェルドミール (2LDK, 77000円, 4F, 2003) — floor 4 without confirmed elevator (elevator=False) — https://www.chintai.net/detail/bk-0000007080000000006360050003/
- ヴェルドミール (2LDK, 77000円, 3F, 2003) — distance 7.43 km > 5.5 — https://www.chintai.net/detail/bk-0000007080000000006360050001/
- ヴェルドミール (2LDK, 77000円, 3F, 2003) — distance 7.43 km > 5.5 — https://www.chintai.net/detail/bk-0000007080000000006360050004/
- エクラ丹波橋 (3LDK, 83000円, 6F, 1994) — distance 6.18 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000000434290025/
- ＨＩＬＬ　ＴＯＰ (2LDK, 69000円, 2F, 1992) — distance 8.45 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000001023400004/
- カ－サ・ＮＡＫＡＭＵＲＡ (3DK, 65000円, 3F, 1995) — distance 7.2 km > 5.5 — https://www.chintai.net/detail/bk-0000007080000000000218480005/
- ルミエ－ル森東 (3LDK, 74000円, 2F, 1997) — distance 8.49 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000000362040008/
- フォ－チュン淀 (3LDK, 79000円, 3F, 1995) — distance 10.53 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000005464910011/
- ＣＨＥＺ　ＬＡ　ＭＥＲＥ (2LDK, 85000円, 3F, 2000) — distance 6.26 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000005452690018/
- ｲﾝﾍﾟﾘｱﾙﾊﾟﾚｽ ﾘﾊﾞ-ｻｲﾄﾞ (2LDK, 72000円, 3F, 1991) — distance 8.13 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000000179990058/
- ｲﾝﾍﾟﾘｱﾙﾊﾟﾚｽ ﾘﾊﾞ-ｻｲﾄﾞ (3LDK, 85000円, 5F, 1991) — distance 8.13 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000000179990084/
- 第七長栄マンション (2LDK, 69000円, 3F, 1995) — distance 8.59 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000006343710006/
- ソーラー21 (2LDK, 68000円, 3F, 2000) — distance 6.62 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000000658960033/
- ＡＺハウス (3LDK, 89000円, 5F, 1995) — distance 8.88 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000000549250045/
- ＡＺハウス (3LDK, 84000円, 4F, 1995) — distance 8.88 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000000549250008/
- ＡＺハウス (3LDK, 89000円, 5F, 1995) — distance 8.88 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000000549250047/
- カ－サ・ＮＡＫＡＭＵＲＡ　２ (3DK, 70000円, 4F, 1999) — floor 4 without confirmed elevator (elevator=False) — https://www.chintai.net/detail/bk-0000007080000000000608830014/
- ＡＺハウス (3LDK, 89000円, 5F, 1995) — distance 8.88 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000000549250035/
- ｲﾝﾍﾟﾘｱﾙﾊﾟﾚｽ ﾘﾊﾞ-ｻｲﾄﾞ (2LDK, 74000円, 7F, 1991) — distance 8.13 km > 5.5 — https://www.chintai.net/detail/bk-0000007050000000000179990032/
- フォレスト桜坂 (2LDK, 55000円, 2F, 2002) — distance 11.11 km > 5.5 — https://www.chintai.net/detail/bk-0000007100000000000882190007/
- レジーナフォレスタ (3LDK, 90000円, 2F, 2016) — distance 8.78 km > 5.5 — https://www.chintai.net/detail/bk-0000007100000000005476890006/
- ソフィスタ洛北 (3LDK, 97000円, 2F, 2003) — distance 9.53 km > 5.5 — https://www.chintai.net/detail/bk-0000007100000000007084070002/
- レグルス (2LDK, 96000円, 2F, 2013) — distance 8.09 km > 5.5 — https://www.chintai.net/detail/bk-0000007100000000005028560005/
- レジデンス岩倉 (2LDK, 85000円, 3F, 1994) — distance 8.95 km > 5.5 — https://www.chintai.net/detail/bk-0000007100000000000091840011/
- ヒルズ宝ケ池 (3DK, 82000円, 2F, 1994) — distance 8.89 km > 5.5 — https://www.chintai.net/detail/bk-0000007100000000001521650004/
- シンフォニー宝ヶ池(301) (3LDK, 92000円, 3F, 1998) — distance 8.5 km > 5.5 — https://www.chintai.net/detail/bk-0000007100000000007472910001/
- カサグランデ雅 (2LDK, 68000円, 2F, 1991) — distance 10.08 km > 5.5 — https://www.chintai.net/detail/bk-0000007100000000000791330013/

## Kept units
| tier | building | layout | ㎡ | rent | 管理費 | floor | built | struct | km | parking | url |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | コンフィアンサ桂 | 2LDK | 59.22 | 91,000 | 12000 | 2/5 EV | 2003.3 | RC | 3.33 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000000903150005/ |
| A | アントレデウブリ－ズ | 2LDK | 50.4 | 78,000 | 8000 | 2/2 | 2004.11 | RC | 4.7 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007060000000001713310009/ |
| A | ｇｌａｎｚ　CLK　いちご館 | 2LDK | 62.09 | 86,000 | 4100 | 2/3 | 2019.9 | 木造 | 5.11 | 有料駐車場 1台 （7,700円/月） / 自転車置き場 ※駐車場の金額表示は1 | https://www.chintai.net/detail/bk-0000007080000000005896150005/ |
| B | プレジオ東寺 | 2LDK+S | 57.8 | 99,000 | 8000 | 6/6 EV | 1997.2 | RC | 1.94 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007090000000000278560004/ |
| B | グランビュ－葛野 | 2LDK | 56.91 | 84,000 | 10000 | 3/4 EV | 1997.2 | RC | 2.47 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007030000000001869700006/ |
| B | ｻﾆ-ｸﾚｽﾄ祥山 | 3LDK | 60.96 | 80,000 | 9000 | 3/7 EV | 1999.3 | RC | 2.55 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007090000000000585860017/ |
| B | コンフォール | 3LDK | 65.0 | 89,000 | 9500 | 5/7 EV | 1995.10 | RC | 2.65 | 有料駐車場 1台 （12,100円/月） / 自転車置き場 / バイク可 ※駐車 | https://www.chintai.net/detail/bk-0000007090000000006354430001/ |
| B | コンフォール | 2LDK | 65.16 | 89,000 | 9500 | 5/7 EV | 1995.10 | RC | 2.65 | 有料駐車場 1台 （12,100円/月） / 自転車置き場 / バイク可 ※駐車 | https://www.chintai.net/detail/bk-0000007090000000006354430007/ |
| B | Ｒｏｓｙ　Ｇａｒｄｅｎ | 2LDK | 48.87 | 87,000 | 8000 | 3/3 | 1994.4 | RC | 2.95 | 有料駐車場 1台 （22,000円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007040000000000439820009/ |
| B | サンクスシティFUKUI | 3LDK | 60.42 | 84,000 | 9000 | 3/5 EV | 1995.11 | RC | 3.1 | 有料駐車場 1台 （14,300円/月） / 自転車置き場 / バイク可 ※駐車 | https://www.chintai.net/detail/bk-0000007060000000005396920006/ |
| B | サンハイム井上 | 2LDK | 66.63 | 86,000 | 11500 | 3/5 EV | 1996.8 | RC | 3.18 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007060000000005613090007/ |
| B | サンハイム井上 | 2LDK | 66.63 | 90,000 | 11500 | 5/5 EV | 1996.8 | RC | 3.18 | 有料駐車場 1台 （11,000円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000005613090005/ |
| B | プレミエｰルクラーテ | 2LDK | 49.05 | 81,000 | 8000 | 3/7 EV | 1997.1 | RC | 3.21 | 有料駐車場 1台 （9,900円/月） / 自転車置き場 ※駐車場の金額表示は1 | https://www.chintai.net/detail/bk-0000007060000000000289850023/ |
| B | レクイエ上桂 | 3LDK | 65.0 | 93,000 | 5000 | 3/3 | 1994.3 | RC | 3.34 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007060000000000707380011/ |
| B | GARNET RESIDENCE上桂 | 3LDK | 65.0 | 96,000 | 8000 | 2/5 EV | 1991.9 | RC | 3.35 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000001423830003/ |
| B | GARNET RESIDENCE上桂 | 3LDK | 69.89 | 91,000 | 8000 | 3/5 EV | 1991.9 | RC | 3.35 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000001423830007/ |
| B | プリメ－ル桂 | 2LDK | 55.0 | 69,000 | 8000 | 2/5 EV | 1993.4 | RC | 3.4 |  | https://www.chintai.net/detail/bk-0000007060000000001286280001/ |
| B | ラティエール桂 | 2LDK | 56.76 | 75,000 | 5000 | 3/4 | 1994.6 | RC | 3.46 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007060000000006752540010/ |
| B | ラティエール桂 | 2LDK | 55.07 | 70,000 | 5000 | 3/4 | 1994.6 | RC | 3.46 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007060000000006752540011/ |
| B | ナチュールＫＩＣＨＩ | 3LDK | 58.0 | 72,000 | 9000 | 4/4 EV | 1991.7 | RC | 3.47 | 有料駐車場 1台 （10,000円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000000581150004/ |
| B | ラビリント川島 | 3LDK | 65.23 | 87,000 | 8000 | 4/6 EV | 1993.11 | RC | 3.48 | 有料駐車場 1台 （8,800円/月） / 自転車置き場 ※駐車場の金額表示は1 | https://www.chintai.net/detail/bk-0000007060000000000082400008/ |
| B | カノン | 2LDK | 53.49 | 80,000 | 8000 | 4/5 EV | 1994.11 | RC | 3.5 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 / バイク可 その他 | https://www.chintai.net/detail/bk-0000007030000000005955420015/ |
| B | カノン | 3LDK | 64.89 | 92,000 | 8000 | 2/5 EV | 1994.11 | RC | 3.5 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 / バイク可 その他 | https://www.chintai.net/detail/bk-0000007030000000005955420007/ |
| B | グランド－ル桂川畔 | 2LDK | 56.38 | 78,000 | 0 | 4/6 EV | 1995.3 | RC | 3.61 | 有料駐車場 1台 （9,000円/月） / 自転車置き場 ※駐車場の金額表示は1 | https://www.chintai.net/detail/bk-0000007060000000000288000013/ |
| B | メゾン桂川 | 2LDK | 54.04 | 67,000 | 9000 | 5/7 EV | 1995.2 | RC | 3.67 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000001090430037/ |
| B | メゾン桂川 | 2LDK | 50.42 | 65,000 | 9000 | 2/7 EV | 1995.2 | RC | 3.67 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000001090430016/ |
| B | メゾン桂川 | 3LDK | 61.68 | 75,000 | 9000 | 5/7 EV | 1995.2 | RC | 3.67 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000001090430011/ |
| B | Sun　Bird　桂 | 3LDK | 64.18 | 85,000 | 8000 | 3/6 EV | 1997.3 | RC | 3.75 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007060000000000865660002/ |
| B | クォーク桂東 | 2LDK | 56.1 | 80,000 | 6000 | 2/3 | 1997.3 | RC | 3.81 | 有料駐車場 1台 （11,000円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000000361860007/ |
| B | サンシャイン梅津 | 3LDK | 63.0 | 92,000 | 10000 | 7/7 EV | 1994.5 | RC | 3.83 | 有料駐車場 1台 （10,000円/月） / 自転車置き場 / バイク可 ※駐車 | https://www.chintai.net/detail/bk-0000007230000000001138720009/ |
| B | ノイシュロス御室南 | 3DK | 60.0 | 79,000 | 7000 | 6/6 EV | 1993.11 | RC | 3.85 | 有料駐車場 1台 （14,300円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007230000000006183420010/ |
| B | アメニティ双ヶ丘 | 3LDK | 69.0 | 95,000 | 15000 | 6/6 EV | 1991.4 | RC | 4.0 | 有料駐車場 1台 （16,500円/月） / 自転車置き場 その他特徴： バイク | https://www.chintai.net/detail/bk-0000007230000000000664860015/ |
| B | カルム常盤 | 2LDK | 52.74 | 78,000 | 7000 | 2/3 | 1995.9 | RC | 4.19 | 有料駐車場 1台 （14,300円/月） / 自転車置き場 / バイク可 ※駐車 | https://www.chintai.net/detail/bk-0000007230000000000426240014/ |
| B | Ｍ レヴェンテ | 2LDK | 55.05 | 81,000 | 10000 | 4/6 EV | 1995.4 | RC | 4.35 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000000128410018/ |
| B | サントル西京 | 2LDK | 57.9 | 78,000 | 7000 | 6/7 EV | 1996.11 | RC | 4.47 | 有料駐車場 1台 （14,300円/月） / 自転車置き場 / バイク可 その他 | https://www.chintai.net/detail/bk-0000007060000000000288150003/ |
| B | WEST　SQUARE－Ⅱ | 3LDK | 69.75 | 100,000 | 5000 | 3/5 EV | 1993.5 | RC | 4.48 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007230000000005945260005/ |
| B | ラ・メゾン・ボヌール | 3LDK | 64.45 | 86,000 | 10000 | 4/7 EV | 1994.9 | RC | 4.49 | 有料駐車場 1台 （16,500円/月） / 自転車置き場 / バイク可 ※駐車 | https://www.chintai.net/detail/bk-0000007060000000000132220042/ |
| B | ラ・メゾン・ボヌール | 3LDK | 65.55 | 86,000 | 10000 | 6/7 EV | 1994.9 | RC | 4.49 | 有料駐車場 1台 （16,500円/月） / 自転車置き場 / バイク可 ※駐車 | https://www.chintai.net/detail/bk-0000007060000000000132220028/ |
| B | カサ・デ・高の手 | 2LDK | 56.7 | 100,000 | 0 | 5/7 EV | 1995.3 | RC | 4.55 | 無料駐車場 1台 / 自転車置き場 | https://www.chintai.net/detail/bk-0000007060000000000132170022/ |
| B | エクセル清涼 | 2LDK | 52.86 | 88,000 | 10000 | 3/6 EV | 1996.3 | RC | 4.58 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000000192370008/ |
| B | リジョイス桂 | 3LDK | 69.27 | 89,000 | 10500 | 2/3 | 1999.3 | RC | 4.58 | 有料駐車場 1台 （13,200円/月） ※駐車場の金額表示は1台分の表示となり | https://www.chintai.net/detail/bk-0000007060000000005841820005/ |
| B | グランビア京都 | 3DK | 60.55 | 90,000 | 0 | 4/7 EV | 1997.4 | RC | 4.62 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007060000000000314180003/ |
| B | ロイヤル清涼 | 2LDK | 55.89 | 86,000 | 10000 | 3/6 EV | 1992.11 | RC | 4.62 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000000154370014/ |
| B | ロイヤル清涼 | 3LDK | 61.02 | 95,000 | 10000 | 3/6 EV | 1992.11 | RC | 4.62 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000000154370001/ |
| B | ロイヤル清涼 | 3LDK | 61.02 | 95,000 | 10000 | 3/6 EV | 1992.11 | RC | 4.62 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000000154370012/ |
| B | ヴェルデ三番館 | 3LDK | 70.06 | 96,000 | 0 | 3/3 | 1993.3 | RC | 4.69 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007060000000000082990021/ |
| B | ヴェルデ三番館 | 3LDK | 66.17 | 88,000 | 0 | 3/3 | 1993.3 | RC | 4.69 | 無料駐車場 1台 / 自転車置き場 | https://www.chintai.net/detail/bk-0000007060000000000082990012/ |
| B | グランシャリオ | 3LDK | 66.6 | 85,000 | 5000 | 2/3 | 1998.1 | RC | 4.76 | 有料駐車場 1台 （11,000円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000000504350004/ |
| B | ロ－ファス小島 | 3LDK | 62.02 | 88,000 | 0 | 2/3 | 1992.4 | RC | 4.82 | 無料駐車場 1台 / 自転車置き場 | https://www.chintai.net/detail/bk-0000007060000000000082700006/ |
| B | ア－バンエステ－トイトヤ | 3LDK | 60.0 | 95,000 | 0 | 3/3 | 1994.4 | RC | 4.83 | 有料駐車場 1台 （11,000円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000000825710008/ |
| B | プロスペクト桂 | 2LDK | 62.16 | 93,000 | 10000 | 2/5 EV | 1996.3 | RC | 4.83 | 有料駐車場 1台 （11,000円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007060000000000145020020/ |
| B | カサグランデ嵯峨野 | 3DK | 54.0 | 74,000 | 0 | 3/4 | 1991.3 | RC | 4.84 | 有料駐車場 1台 （11,000円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007230000000000009000007/ |
| B | 日本鉱産ビルグラハイツ | 3LDK | 62.37 | 95,000 | 4000 | 7/7 EV | 1993.11 | RC | 4.87 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007080000000000548500008/ |
| B | CASA SHIMEI | 2LDK | 53.0 | 92,000 | 10000 | 2/4 | 1991.7 | RC | 4.98 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007070000000000570010002/ |
| B | ABC BLDG. | 2LDK | 48.0 | 78,000 | 8000 | 3/5 EV | 1995.1 | RC | 5.0 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007050000000000369050001/ |
| B | セントラルヴィレッジ | 3LDK | 69.13 | 88,000 | 8000 | 3/3 | 2000.2 | RC | 5.03 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007230000000006105850005/ |
| B | グレ－スダイン | 3DK | 65.99 | 95,000 | 9000 | 7/7 EV | 1995.9 | RC | 5.03 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007050000000000264700011/ |
| B | グレース ナカミヤ | 2LDK | 55.57 | 88,000 | 9000 | 5/6 EV | 1997.9 | RC | 5.14 | 有料駐車場 1台 （13,200円/月） / 自転車置き場 ※駐車場の金額表示は | https://www.chintai.net/detail/bk-0000007050000000000429970023/ |
| B | ｸﾞﾚｰｽ菱屋2 | 2LDK | 56.0 | 90,000 | 3000 | 2/3 | 2000.2 | RC | 5.2 | 自転車置き場 | https://www.chintai.net/detail/bk-0000007050000000000677550006/ |
| B | ELESPA 24 | 3LDK | 58.39 | 73,000 | 8500 | 2/6 EV | 1994.10 | RC | 5.36 | 有料駐車場 1台 （7,700円/月） / 自転車置き場 ※駐車場の金額表示は1 | https://www.chintai.net/detail/bk-0000007060000000000140910004/ |

## Problems / notes
- No blocks or captchas; all pages 200.
- The site's result counts are per unit (rooms), buildings are grouped on the list page.
- `elevator` = true when 設備 text lists エレベーター, false when the listing has a 設備 section without it, null when no 設備 section.
- Coordinates come from the listing's own map link (building-level); geo.py (GSI) used as fallback/cross-check.
- 左京区 (26103) was also scanned since its SW corner is within 5.5 km; distance filter applied to everything.
