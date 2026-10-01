# ur — UR賃貸住宅 (www.ur-net.go.jp), fetched 2026-10-01

## Coverage / method
- Enumerated every UR 団地 in 京都府 from the static pages: /chintai/kansai/kyoto/ (top), /list/ (41 estates, IDs 80_XXXX), /map/, ward pages /area/{101,102,104,107,108,109,110,111}.html, and fetched all 41 estate pages (80_XXXX.html) + 41 団地レポート pages (80_XXXX_report.html). 30 estates are inside 京都市; **15 are within 5.5 km** of KRP (list below). 嵯峨 (80_0120) is 5.78 km → excluded; everything in 伏見区 south of 深草, 山科, 洛西 (西京区 大枝/大原野) is 6.7–9.6 km.
- **Live vacancy is NOT verifiable from this environment**: the room list on every estate page is loaded from chintai.sumai.ur-net.go.jp, which this environment's egress policy blocks (CONNECT 502). All numbers below are the estate-level static catalogue (家賃レンジ, 間取り/床面積レンジ, 構造, 管理年数). Check live on the estate URL or call UR京都営業センター / 空家情報フリーコール 0120-23-3456.
- Because unit-level data is unavailable, out/ur.json has **one object per estate** (not per unit): `layout`/`area_m2`/`rent` = upper end of the estate range, `layout_range`/`area_range`/`rent_range` = full range, `big_units_in_catalogue` = whether a 2LDK+/3DK+ ≥45 m² type with rent starting ≤100,000 exists in the estate at all. `built_year` is estimated as 2026 − 管理年数 (flag `built_year_approx`). `elevator` is true only where the 団地レポート mentions one; otherwise null with an inference in `notes`.
- UR terms (all estates): 礼金なし・仲介手数料なし・更新料なし・保証人不要; 敷金 = 家賃2ヶ月分. 共益費 shown per estate.
- **Age rule**: every UR estate in Kyoto city except 京都十条 was built before 1991 (管理年数 44–59 years), so by the spec's building-age rule only 京都十条 (built ≈1998–2000, RC, tier B) passes. The other 14 are included with `tier: "old"` + an explicit AGE RULE FAIL note so they can be weighed separately (UR stock is RC/SRC/PC concrete, often renovated — e.g. 西京極駅前 was fully リノベーション).

## Estates within 5.5 km (sorted by distance)
| km | estate | id | built≈ | structure / floors | elevator | layouts / area | rent (共益費) | 2LDK+/45㎡+/≤10万 exists | nearest station |
|---|---|---|---|---|---|---|---|---|---|
| 0.8 | UR 壬生相合 | 80_1971 | 1973 (old) | RC 9F | None | 1R～2DK / 26–41㎡ | 43,100–68,500円 (4,700円) | no | 阪急京都線「大宮」駅から徒歩5分 |
| 1.04 | UR 西院 | 80_1491 | 1969 (old) | RC 10F | None | 1DK～2DK / 30–47㎡ | 47,200–68,400円 (3,700円) | no | 阪急京都線「西院」駅から徒歩3分 |
| 1.21 | UR 壬生坊城第2 | 80_2290 | 1977 (old) | RC 11F | None | 1DK～3DK / 32–53㎡ | 59,300–90,400円 (3,900円) | YES | 阪急京都線「大宮」駅 徒歩3～7分 京福電気鉄道嵐山本線「四条大宮」駅バス2分 徒歩2～4 |
| 1.49 | UR 西京極 | 80_2880 | 1982 (old) | RC 5F | None | 2DK+S～3DK / 61–61㎡ | 75,600–93,400円 (3,080円) | YES | 阪急京都線「西京極」駅 徒歩9～10分 JR東海道・山陽本線「西大路」駅 徒歩22～23分 |
| 1.96 | UR 西京極駅前 | 80_2140 | 1975 (old) | SRC 10F | True | 1DK～2DK / 31–44㎡ | 53,800–73,200円 (5,000円) | no | 阪急京都線「西京極」駅 徒歩1分 |
| 1.98 | UR 九条大宮 | 80_1440 | 1969 (old) | RC 7F | True | 1DK～3DK / 29–85㎡ | 40,600–97,500円 (3,900円) | YES | JR･地下鉄烏丸線･近鉄京都線「京都」駅から市バス12分「東寺南門前」下車徒歩2分 |
| 2.13 | UR 九条 | 80_1230 | 1967 (old) | SRC 10F | None | 1DK～2DK / 30–45㎡ | 36,300–55,600円 (3,000円) | no | JR東海道・山陽本線「京都」駅バス10分 徒歩1分 近鉄京都線「東寺」駅 徒歩10分 京都 |
| 2.47 | UR 菅田町 | 80_2081 | 1974 (old) | RC 11F | True | 1DK～2DK / 28–42㎡ | 43,800–65,300円 (3,300円) | no | 近鉄京都線「十条」駅から徒歩5分 |
| 2.51 | UR 京都十条 | 80_4120 | 2000 (B) | RC 6F | None | 1LDK～4LDK / 47–83㎡ | 77,600–133,300円 (4,340円) | YES | 近鉄京都線「十条」駅 徒歩15～17分 JR東海道・山陽本線「西大路」駅 徒歩20分 JR |
| 2.97 | UR 北野 | 80_1680 | 1971 (old) | RC 5F | None | 1DK / 29–29㎡ | 43,100–44,600円 (2,730円) | no | JR山陰本線・京都市営東西線「二条」駅から市バス5分「千本中立売」下車徒歩4分 |
| 3.07 | UR 松ノ木町 | 80_2220 | 1979 (old) | SRC 11F | None | 1R～2DK / 29–42㎡ | 44,800–66,200円 (3,200円) | no | 京都市営地下鉄烏丸線「九条」駅 徒歩9～10分 京都市営地下鉄烏丸線「十条」駅 徒歩9～1 |
| 3.68 | UR 花園 | 80_2600 | 1980 (old) | RC 5F | None | 1LDK～3LDK / 54–66㎡ | 71,000–103,500円 (3,660円) | YES | JR山陰本線「花園」駅 徒歩12～16分 京福電気鉄道北野線「等持院・立命館大学衣笠キャン |
| 4.36 | UR 上桂 | 80_2530 | 1979 (old) | RC 6F | None | 3DK / 55–55㎡ | 71,600–75,600円 (5,100円) | YES | 阪急嵐山線「上桂」駅から徒歩12分 又は阪急京都線「桂」駅から徒歩22分 |
| 4.76 | UR 深草 | 80_1470 | 1969 (old) | RC 7F | True | 1DK～3DK / 29–58㎡ | 39,000–64,600円 (中層：1,900円・高層：3,600円) | YES | 京阪本線「藤森」駅 徒歩7分 近鉄京都線「竹田」駅 徒歩11分 JR奈良線「JR藤森」駅  |
| 5.25 | UR 紫野 | 80_1620 | 1970 (old) | RC 5F | None | 1DK～2DK / 30–41㎡ | 46,200–64,500円 (5,300円) | no | 京都市営烏丸線「北大路」駅から徒歩6分 |

## Estates with family-size types (2LDK+/3DK+, ≥45 m²) and rent range reaching ≤100,000
- **UR 壬生坊城第2** (1.21 km, 京都府京都市中京区壬生坊城町48番3): 1DK～3DK 32–53㎡, 59,300–90,400円 + 共益費 3,900円, RC 11F, built≈1977 → tier old, elevator None, parking: None — https://www.ur-net.go.jp/chintai/kansai/kyoto/80_2290.html
- **UR 西京極** (1.49 km, 京都府京都市右京区西京極三反田町1番地 他): 2DK+S～3DK 61–61㎡, 75,600–93,400円 + 共益費 3,080円, RC 5F, built≈1982 → tier old, elevator None, parking: None — https://www.ur-net.go.jp/chintai/kansai/kyoto/80_2880.html
- **UR 九条大宮** (1.98 km, 京都府京都市南区西九条南田町9番地): 1DK～3DK 29–85㎡, 40,600–97,500円 + 共益費 3,900円, RC 7F, built≈1969 → tier old, elevator True, parking: None — https://www.ur-net.go.jp/chintai/kansai/kyoto/80_1440.html
- **UR 京都十条** (2.51 km, 京都府京都市南区吉祥院南落合町40番地): 1LDK～4LDK 47–83㎡, 77,600–133,300円 + 共益費 4,340円, RC 6F, built≈2000 → tier B, elevator None, parking: 敷地内あり（団地レポート記載、料金不明） — https://www.ur-net.go.jp/chintai/kansai/kyoto/80_4120.html
- **UR 花園** (3.68 km, 京都府京都市右京区花園鷹司町1・8-1・25・25-1): 1LDK～3LDK 54–66㎡, 71,000–103,500円 + 共益費 3,660円, RC 5F, built≈1980 → tier old, elevator None, parking: なし（団地レポート: 駐車場を持たない） — https://www.ur-net.go.jp/chintai/kansai/kyoto/80_2600.html
- **UR 上桂** (4.36 km, 京都府京都市西京区上桂森下町25番地1): 3DK 55–55㎡, 71,600–75,600円 + 共益費 5,100円, RC 6F, built≈1979 → tier old, elevator None, parking: None — https://www.ur-net.go.jp/chintai/kansai/kyoto/80_2530.html
- **UR 深草** (4.76 km, 京都府京都市伏見区深草西浦町六丁目65番地): 1DK～3DK 29–58㎡, 39,000–64,600円 + 共益費 中層：1,900円・高層：3,600円, RC 7F, built≈1969 → tier old, elevator True, parking: None — https://www.ur-net.go.jp/chintai/kansai/kyoto/80_1470.html

## Which estate is the friend's 'tall UR building with elevator near JR 京都駅'?
No UR estate exists in 下京区. The high-rise UR estates nearest 京都駅 are all in 南区:
- **松ノ木町 (80_2220)** — 南区東九条南松ノ木町1-1, SRC 10–11F × 3 buildings, 707 units, ≈1 km south-east of 京都駅 八条口 (地下鉄 九条駅 徒歩9–10分), built ≈1976–79, 1R–2DK 29–42 m², 44,800–66,200円. Largest and tallest → most likely the friend's building.
- **九条 (80_1230)** — 南区西九条南田町1-3, SRC 10F (1–3F = 南区役所), 154 units, 近鉄 東寺駅 徒歩1分 / 京都駅 バス10分, built ≈1967, 1DK–2DK 30–45 m², 36,300–55,600円.
- **菅田町 (80_2081)** — 南区西九条菅田町27-2, PC造 11F, 142 units, 近鉄 十条駅 徒歩5分, built ≈1974, 1DK–2DK 28–42 m², 43,800–65,300円; レポート: 'エレベーター付き物件'.
- (九条大宮 80_1440, RC 7F, 62 units, 東寺駅 徒歩8分, has elevator and 3DK up to 85 m² — the only one of these four with family-size units, 40,600–97,500円.)
None of these four passes the age rule (all 1967–1979); only 京都十条 (80_4120, 南区吉祥院南落合町40, 近鉄 十条駅 徒歩15分 / JR 西大路駅 徒歩20分, RC 5–6F, 1LDK–4LDK 47–83 m², 77,600–133,300円, built ≈1998–2000) is tier B.

## Raw files
- out/raw/ur/80_XXXX.html (estate pages), 80_XXXX_report.html (団地レポート), list_index.html, area_109/110.html, map_dir.html; estates_basic.json / estates_kyoto_geo.json (parsed + geocoded).