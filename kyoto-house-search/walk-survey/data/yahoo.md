# yahoo — Yahoo!不動産 (realestate.yahoo.co.jp/rent), WALK survey (≤1.3 km of 京都技術科学センター, 左京区吉田河原町14), fetched 2026-10-18

## Method
- Filter format found in the site's JS (`common/Constants.js` SEARCH_CONDITION_KEY) and confirmed by the SSR echo (`formValues`):
  `/rent/search/06/26/<ward>/?ma_from=45&rl_dtl=7&rl_dtl=8&…&rl_dtl=14&page=N` (rl_dtl 7=2LDK 8=3K 9=3DK 10=3LDK 11=4K 12=4DK 13=4LDK 14=5K以上; ma_from = 専有面積下限 m²). Other keys: rent_from/rent_to, age, structure_type, kind, oaza, st, sort. No rent / age / floor filter used.
- Wards 左京区 26103, 上京区 26102, 中京区 26104 — site counts with the filter: 左京 1,025 rooms / 595 buildings, 上京 672 / 289, 中京 998 / 516 → 48 list pages (30 buildings each). Raw: out/raw/yahoo/list/*.html.gz.
- Every list page embeds `window.__SERVER_SIDE_CONTEXT__` JSON: each building carries `CoordinatesWgs` → 1,400 building cards, 1,188 > 1.45 km dropped at list stage (town-geocoded when no coordinates).
- Buildings showing fewer rooms than `PropertyCount` were expanded via `/rent/search/s/<structureId>/` (41 pages, unfiltered → filtered here: 2LDK+ and ≥45 m²).
- 356 candidate rooms → unit pages `/rent/detail/<PropertyId>/` all HTTP 200 (raw: out/raw/yahoo/detail/). Final distance from the unit page's own `CoordinatesWgs` (98 dropped > 1.3 km); 2 dropped as 1LDK+納戸 (the list bucket 2LDK includes 1SLDK).
- layout = first token of 間取り内訳 (the list bucket "5K以上" is replaced by the real 5DK/6DK/7SLDK…). `parking` = the unit page's 駐車場 cell verbatim (Yahoo prints "-" when the agent left it empty); `parking_fee` = ParkingCost. `elevator` = Yahoo equipment code "ev" (エレベーター) present → true, equipment list present without it → false.
- `building_name` is Yahoo's display name; when the agent hides the name (`CanDisplayBuildingName=false`) it is a generated "<line> <station> 地上N階建て 築N年" label (noted).
- Yahoo aggregates many agents (エリッツ, アパマンショップ, 京都ライフ, ハウスメイト, エイブル…), so many units here are also on SUUMO/HOME'S; merge.py dedupes. Other agents offering the same room are listed in `notes` (同じ部屋の他社掲載).

## Result
- **Kept 134 units** (after merging 122 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via nearest station (noted in `notes`), 0 of them dropped as >1.3 km.
- Within 1.0 km: 93; rent range kept: 87000–498000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'house': 39, 'B': 7, 'old': 20, 'A': 68}; 礼金 ≤1ヶ月 65, >1ヶ月 69, unknown 0 (no 礼金 limit in this survey).
- Elevator yes/no/unknown: 61/73/0; by ward: {'左京区': 63, '上京区': 50, '中京区': 21}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/yahoo/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.13 | 京阪鴨東線 出町柳駅 地上2階建 築22年 | 2LDK | 66.7 | 120,000 | 0 | なし / 24万円 | 2.0 | 1/2 | n | 2004/12 | 木造 | 近隣あり 22,000円 | house | https://realestate.yahoo.co.jp/rent/detail/_000008883900a902b815a1f1bf273be4cc0983c54aa4/ |
| 0.13 | 京阪鴨東線 出町柳駅 地上2階建て 築22年 | 2LDK | 66.7 | 120,000 | 0 | なし / 24万円 | 2.0 | None/2 | n | 2004/12 | 木造 | 近隣あり 18,000円 | house | https://realestate.yahoo.co.jp/rent/detail/_00000890140646ea0a8e711dfd00d73a6f9af2194906/ |
| 0.16 | 京阪鴨東線 神宮丸太町駅 地上2階建て 築4 | 3DK | 54.67 | 100,000 | 0 | 1ヶ月 / 20万円 | 2.0 | 1/2 | n | 1984/11 | 木造 | 近隣あり 18,000円 | house | https://realestate.yahoo.co.jp/rent/detail/_000005053869f759dd2ca72f9818b906b04cdbf1c648/ |
| 0.16 | 今智庵 | 3DK | 65.0 | 100,000 | 0 | 10万円 / 20万円 | 2.0 | 1/2 | n | 1984/11 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/00000505386973d13ec8c69758eea455277c5e4e840d/ |
| 0.17 | 今智庵 | 3DK | 61.06 | 100,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/3 | n | 1984/11 | 木造 | なし | house | https://realestate.yahoo.co.jp/rent/detail/00000513872998d786da400659720acb2d4f76ffbe19/ |
| 0.17 | エーデルハイム鴨川 | 3LDK | 65.77 | 138,000 | 10000 | 20万円 / 35万円 | 2.54 | 5/5 | Y | 1997/2 | RC | あり 21,000円 | B | https://realestate.yahoo.co.jp/rent/detail/0000016623355635ab89fdc976adb2958209aa43e7b5/ |
| 0.17 | エーデルハイム鴨川 | 3LDK | 65.0 | 138,000 | 10000 | 20万円 / 35万円 | 2.54 | 5/5 | Y | 1997/2 | RC | あり 21,000円 | B | https://realestate.yahoo.co.jp/rent/detail/000001662335194f40f950c85b3805c7286f33105502/ |
| 0.18 | 今智庵 | 3DK | 65.0 | 100,000 | 0 | 10万円 / 20万円 | 2.0 | None/3 | n | 1984/11 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/000009054095f8fae7f392c76ba09706d6ba7e5115a2/ |
| 0.27 | 上阿達谷口マンション | 2LDK | 46.12 | 110,000 | 6000 | 11万円 / 11万円 | 1.0 | 1/4 | n | 1989/5 | RC | - | old | https://realestate.yahoo.co.jp/rent/detail/000001116490fc95039ee35f6feaf290eb176ee75950/ |
| 0.28 | 上阿達谷口マンション | 3DK | 45.7 | 110,000 | 6000 | 1ヶ月※ / 11万円 | 1.0 | 1/4 | n | 1989/4 | RC | 近隣あり 18,000円 | old | https://realestate.yahoo.co.jp/rent/detail/000001116490ee1f5f4474616449592e0c19d1757cbe/ |
| 0.34 | 吉田上阿達町7-19　貸家 | 3LDK | 101.65 | 250,000 | 0 | 25万円 / 37.5万円 | 1.5 | 1/2 | n | 2019/2 | 木造 | あり 無料 | house | https://realestate.yahoo.co.jp/rent/detail/000009074905f8fae7f392c76ba09706d6ba7e5115a2/ |
| 0.38 | ザ・パークハウス京都鴨川御所東 | 2LDK | 104.1 | 465,000 | 0 | 46.5万円※ / 93万円※ | 2.0 | 5/5 | Y | 2017/3 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/000003960095e69d494abffffe24b8d6ff7b04feccdb/ |
| 0.41 | 梶井町貸家 | 5DK | 93.54 | 180,000 | 0 | 30万円 / 30万円 | 1.67 | 1/2 | n | 1970/4 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/0000018337477ec9e5abbb13f8b68f51a350aac5d8fa/ |
| 0.41 | 京阪鴨東線 出町柳駅 地上2階建て 築30年 | 5DK | 93.54 | 200,000 | 0 | 30万円 / 30万円 | 1.5 | None/2 | n | 1997/2 | 木造 | あり 無料 | house | https://realestate.yahoo.co.jp/rent/detail/_0000088928498f4a65e1cebd41aab8de809c58a7eb26/ |
| 0.44 | THE RESIDENCE御車道 | 2LDK | 68.58 | 205,000 | 10000 | 1ヶ月※ / 25万円※ | 1.22 | 1/4 | Y | 2026/8 | RC | 近隣あり 19,800円 | A | https://realestate.yahoo.co.jp/rent/detail/000009016407c5893e391ad317fbf5bda17dbc6d0de3/ |
| 0.45 | Grand　E’terna　京大正門前 | 3LDK | 71.07 | 169,500 | 9000 | なし / 33.9万円 | 2.0 | 2/5 | Y | 2008/10 | RC | あり 23,100円 | A | https://realestate.yahoo.co.jp/rent/detail/000004145425528252642e4eae31065750253f34518e/ |
| 0.45 | Grand　E’terna　京大正門前 | 2LDK | 64.2 | 160,500 | 9000 | なし / 32.1万円 | 2.0 | 2/5 | Y | 2008/10 | RC | あり 23,100円 | A | https://realestate.yahoo.co.jp/rent/detail/0000041454258ab7df2672ffe772acfe8fa2648c6f16/ |
| 0.45 | 京阪鴨東線 出町柳駅 4階建 築1年未満 | 2LDK | 59.7 | 179,000 | 10000 | 17.9万円 / 20万円 | 1.12 | 1/4 | Y | 2026/8 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_000009017692d86dbb368be32c9ae560edb33569455e/ |
| 0.45 | 京阪鴨東線 出町柳駅 4階建 築1年未満 | 2LDK | 59.7 | 192,000 | 10000 | 19.2万円 / 20万円 | 1.04 | 2/4 | Y | 2026/8 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_0000090176928f6854a3f9fce9c7b2dcb7152386290f/ |
| 0.46 | Grand E’terna 京大正門前 | 2LDK | 56.53 | 160,500 | 9000 | なし / 32.1万円 | 2.0 | 2/5 | Y | 2008/9 | RC | あり 23,100円 | A | https://realestate.yahoo.co.jp/rent/detail/0000041454258742cec1c6b5035910d05e0b90303c1e/ |
| 0.46 | 京阪鴨東線 神宮丸太町駅 5階建 築10年 | 2LDK | 104.01 | 465,000 | 0 | 46.5万円 / 93万円 | 2.0 | 5/5 | Y | 2017/6 | RC | あり 25,000円 | A | https://realestate.yahoo.co.jp/rent/detail/_000003960095873243da700d6d9a897621213f80eaa2/ |
| 0.49 | ノーベルテラス稔 | 2LDK | 87.76 | 220,000 | 8000 | 22万円 / 44万円 | 2.0 | 4/5 | Y | 2003/3 | 鉄骨 | - | A | https://realestate.yahoo.co.jp/rent/detail/000001620658f46aedf34daebad9df19d2cb91eac39f/ |
| 0.49 | 京阪鴨東線 神宮丸太町駅 2階建 築2年 | 2LDK | 61.69 | 179,000 | 6000 | なし / なし | 0.0 | 2/2 | n | 2025/9 | 木造 | あり 20,000円 | A | https://realestate.yahoo.co.jp/rent/detail/_0000086441747c8ed1933169d3934ce508f31f49be06/ |
| 0.5 | ノーベルテラス稔 | 2LDK | 54.86 | 220,000 | 8000 | 22万円 / 44万円 | 2.0 | 4/5 | Y | 2003/3 | 鉄骨 | - | A | https://realestate.yahoo.co.jp/rent/detail/000001620658abe7e51e465d97c228c73f655ab85346/ |
| 0.5 | ノーベルテラス稔 | 2LDK | 57.76 | 220,000 | 8000 | 1ヶ月※ (保証金 なし※) / 44万円※ | 2.0 | 4/5 | Y | 2003/3 | 鉄骨 | 近隣あり 18,000円 | A | https://realestate.yahoo.co.jp/rent/detail/000001620658bcbcde7a1fe64acf40b8efb27c9361a5/ |
| 0.5 | 京阪鴨東線 神宮丸太町駅 2階建 築2年 | 2LDK | 61.69 | 174,000 | 6000 | なし / 17.4万円 | 1.0 | 1/2 | n | 2025/9 | 木造 | あり 22,000円 | A | https://realestate.yahoo.co.jp/rent/detail/_00000864417446ebba8f5e089235f44d2a5e1061de73/ |
| 0.5 | BelleLead御所東 | 2SLDK | 53.0 | 159,000 | 6000 | なし / なし | 0.0 | 1/2 | n | 2025/9 | 木造 | あり 20,000円 | A | https://realestate.yahoo.co.jp/rent/detail/00000862808032679c8b1873333d8eb86ef1c606971f/ |
| 0.51 | 田中下柳町貸家13 | 5K | 56.82 | 120,000 | 0 | 24万円 / 12万円 | 1.0 | 1/2 | n | 1970/3 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/000008880213e2a8780498b1150fb6abfef60326a3e0/ |
| 0.57 | 荒神口貸家 | 5K | 46.6 | 90,000 | 0 | 9万円 / 9万円 | 1.0 | 1/2 | n | 1970/1 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/0000048116138bc53d2c6cf5774879abb8bfce08f75f/ |
| 0.58 | Foresta御所東 | 2LDK | 61.49 | 200,000 | 11500 | なし / なし | 0.0 | 1/3 | n | 2026/5 | 軽量鉄骨 | - | A | https://realestate.yahoo.co.jp/rent/detail/000008817072e68f78ef8f0e55ed442ffed60d9a1075/ |
| 0.6 | 京阪鴨東線 出町柳駅 地上6階建て 築19年 | 2LDK | 60.25 | 165,000 | 16000 | なし / 33万円 | 2.0 | 5/6 | Y | 2008/3 | RC | 近隣あり 15,000円 | A | https://realestate.yahoo.co.jp/rent/detail/_000001423099c4dc80a6f4e3bf30388457b99245f802/ |
| 0.6 | ピアハウス出町 | 4LDK | 145.42 | 280,000 | 0 | 28万円 / 56万円 | 2.0 | 1/3 | n | 1998/11 | 鉄骨 | - | house | https://realestate.yahoo.co.jp/rent/detail/00000773018967cea77ddeaaa8903f9d6f8732b652d9/ |
| 0.61 | ベリエ茶五 | 2LDK | 60.25 | 160,000 | 15000 | なし / 32万円 | 2.0 | 4/6 | Y | 2008/3 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/000002241956d8f9a3b8367a6be86f6eb6026018f028/ |
| 0.61 | ベリエ茶五 | 2LDK | 60.25 | 190,000 | 17000 | なし / 38万円 | 2.0 | 6/6 | Y | 2008/3 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/000002241956948279c7fea5dee02fab99ec031991d6/ |
| 0.61 | ベリエ茶五 | 2LDK | 54.72 | 150,000 | 15000 | なし / 30万円 | 2.0 | 3/6 | Y | 2008/3 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/000002241956f94293649aba9972e939e345c8a20934/ |
| 0.61 | ピアハウス出町 | 4LDK | 145.42 | 280,000 | 0 | 1ヶ月※ / 56万円※ | 2.0 | 2/3 | n | 1998/11 | 鉄骨 | 近隣あり 15,000円 | B | https://realestate.yahoo.co.jp/rent/detail/000007730189bee825f0fe69af3192377d3eb3b1e585/ |
| 0.62 | 京都市営地下鉄東西線 京都市役所前駅 3階建 | 2LDK | 48.6 | 95,000 | 7000 | 9.5万円 / 10万円 | 1.05 | 2/3 | n | 1988/9 | RC | - | old | https://realestate.yahoo.co.jp/rent/detail/_0000070792987ce883dcf614dfed86e6e71c31781133/ |
| 0.62 | エスタプレイス | 2LDK | 68.55 | 207,000 | 7500 | なし / 20.7万円 | 1.0 | 3/4 | n | 2027/4 | RC | あり 22,000円 | A | https://realestate.yahoo.co.jp/rent/detail/000009007874ed7012869daae40063ba57a0581c4347/ |
| 0.62 | エスタプレイス | 2LDK | 68.55 | 206,000 | 7500 | なし / 20.6万円 | 1.0 | 2/4 | n | 2027/4 | RC | あり 22,000円 | A | https://realestate.yahoo.co.jp/rent/detail/000009007874525008de29b442f6d6ba471aee2309e0/ |
| 0.62 | エスタプレイス | 2LDK | 73.03 | 215,000 | 7500 | なし / 21.5万円 | 1.0 | 2/4 | n | 2027/4 | RC | あり 22,000円 | A | https://realestate.yahoo.co.jp/rent/detail/000009007874864e01de64435805fd7b9ee0c1cde79a/ |
| 0.62 | エスタプレイス | 2LDK | 75.03 | 215,000 | 7500 | なし / 21.5万円 | 1.0 | 2/6 | Y | 2027/4 | RC | あり 22,000円 | A | https://realestate.yahoo.co.jp/rent/detail/00000889536065f06f207c292421fa6720a64fa954ed/ |
| 0.62 | エスタプレイス | 2LDK | 75.03 | 216,000 | 7500 | なし / 21.6万円 | 1.0 | 3/6 | Y | 2027/4 | RC | あり 22,000円 | A | https://realestate.yahoo.co.jp/rent/detail/0000088953601e17deebd9b048ed9aa1344c20218c40/ |
| 0.62 | エスタプレイス | 2LDK | 75.03 | 216,000 | 7500 | なし / 21.6万円 | 1.0 | 4/6 | Y | 2027/4 | RC | あり 22,000円 | A | https://realestate.yahoo.co.jp/rent/detail/000008895360cdf0e8d35bacefea8d5180f0c117ddc4/ |
| 0.62 | 京阪鴨東線 出町柳駅 地上6階建て 築1年未 | 2LDK | 68.55 | 206,000 | 7500 | なし / 20.6万円 | 1.0 | 2/6 | Y | 2027/3 | RC | 近隣あり 15,000円 | A | https://realestate.yahoo.co.jp/rent/detail/_000008895360525008de29b442f6d6ba471aee2309e0/ |
| 0.62 | 京阪鴨東線 出町柳駅 地上6階建て 築1年未 | 2LDK | 73.03 | 215,000 | 7500 | なし / 21.5万円 | 1.0 | 2/6 | Y | 2027/3 | RC | 近隣あり 15,000円 | A | https://realestate.yahoo.co.jp/rent/detail/_000008895360864e01de64435805fd7b9ee0c1cde79a/ |
| 0.62 | 京阪鴨東線 出町柳駅 地上6階建て 築1年未 | 2LDK | 68.55 | 207,000 | 7500 | なし / 20.7万円 | 1.0 | 3/6 | Y | 2027/3 | RC | 近隣あり 15,000円 | A | https://realestate.yahoo.co.jp/rent/detail/_000008895360ed7012869daae40063ba57a0581c4347/ |
| 0.63 | アルス丸太町山水庵 | 3LDK | 117.57 | 280,000 | 17100 | 28万円※ (保証金 なし※) / 56万円※ | 2.0 | 3/5 | Y | 2002/3 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/000005193806afa0183eaff0c40ab54152753d972d2a/ |
| 0.65 | アルス丸太町山水庵 | 3SLDK | 117.57 | 280,000 | 17000 | 28万円 / 56万円 | 2.0 | 5/6 | Y | 2002/3 | RC | あり 20,000円 | A | https://realestate.yahoo.co.jp/rent/detail/000005193806fc4b7cf9ff0eaafbe1b0cfa9457b7f7f/ |
| 0.65 | 京阪鴨東線 神宮丸太町駅 地上10階建て 築 | 3LDK | 113.88 | 402,000 | 18000 | 1ヶ月※ / なし | 0.0 | 9/10 | Y | 2007/9 | RC | あり 25,300円 | A | https://realestate.yahoo.co.jp/rent/detail/_00000088926564d63227c87a9a637e2db6609a250d78/ |
| 0.66 | 京阪鴨東線 神宮丸太町駅 6階建 築24年 | 3LDK | 78.04 | 215,000 | 10000 | 21.5万円 / 21.5万円 | 1.0 | 6/6 | Y | 2003/3 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_000008824789b4dbf2e643825cda2ad7d7dd06ab3f67/ |
| 0.66 | 京阪鴨東線 神宮丸太町駅 7階建 築24年 | 3LDK | 78.04 | 215,000 | 10000 | 21.5万円 / 21.5万円 | 1.0 | 6/7 | Y | 2003/10 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_00000883290558517c9e0dc766f248641d1246b6a2c9/ |
| 0.66 | 京阪鴨東線 神宮丸太町駅 10階建 築20年 | 3LDK | 113.88 | 402,000 | 18000 | 40.2万円 / 40.2万円 | 1.0 | 2/10 | Y | 2007/9 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_000000889265c2e4a11c8ebb956a834f62e91147485a/ |
| 0.67 | 上京区南町住宅 | 4DK | 111.94 | 168,000 | 0 | 15万円 / 20万円 | 1.19 | None/3 | n | 1994/2 | 木造 | あり 無料 | house | https://realestate.yahoo.co.jp/rent/detail/000009083030f8fae7f392c76ba09706d6ba7e5115a2/ |
| 0.67 | 京阪鴨東線 神宮丸太町駅 3階建 築40年 | 2LDK | 53.94 | 138,000 | 10000 | なし / 13.8万円 | 1.0 | 2/3 | n | 1987/2 | RC | - | old | https://realestate.yahoo.co.jp/rent/detail/_000002093229574f8fb6c4f994e0622a8bd41b85fad1/ |
| 0.67 | 京阪鴨東線 神宮丸太町駅 3階建 築40年 | 2LDK | 53.94 | 136,000 | 10000 | なし / 13.6万円 | 1.0 | 1/3 | n | 1987/2 | RC | あり 25,000円 | old | https://realestate.yahoo.co.jp/rent/detail/_00000209322924dbc7fb2ca40fae00839029ed5b9168/ |
| 0.68 | 南町貸家(513-1) | 4DK | 111.94 | 168,000 | 0 | 15万円 / 20万円 | 1.19 | 1/3 | n | 1994/2 | 木造 | あり | house | https://realestate.yahoo.co.jp/rent/detail/000009082989c8767541fdde10c27a66fe77ce78a69e/ |
| 0.7 | 京阪鴨東線 神宮丸太町駅 地上2階建て 築4 | 5DK | 103.68 | 250,000 | 0 | 1ヶ月 / 25万円 | 1.0 | 2/2 | n | 1987/1 | 木造 | 近隣あり 16,000円 | house | https://realestate.yahoo.co.jp/rent/detail/_000008030143a38d002f63ea90ab3a0f6ae99e3d4d3d/ |
| 0.71 | 仮称)D-room上京区米屋町ハイツ | 2LDK | 60.19 | 204,000 | 12000 | なし / 25万円 | 1.23 | 1/3 | n | 2026/11 | 軽量鉄骨 | - | A | https://realestate.yahoo.co.jp/rent/detail/0000090515230a98ed6d647f0991f6334be81eecdf10/ |
| 0.71 | 仮称)D-room上京区米屋町ハイツ | 2LDK | 62.73 | 207,000 | 12000 | なし / 25万円 | 1.21 | 1/3 | n | 2026/11 | 軽量鉄骨 | - | A | https://realestate.yahoo.co.jp/rent/detail/0000090515237d52d102d17bf38442ef1e7d63390361/ |
| 0.71 | 仮)D－room上京区米屋町ハイツ | 2LDK | 62.73 | 210,000 | 12000 | なし / 25万円 | 1.19 | 2/3 | n | 2026/11 | 軽量鉄骨 | あり 33,000円 | A | https://realestate.yahoo.co.jp/rent/detail/0000090813160cab85215c1b57d14a00f542277546af/ |
| 0.71 | 仮称)D-room上京区米屋町ハイツ | 2LDK | 60.19 | 208,000 | 12000 | なし / 25万円 | 1.2 | 2/3 | n | 2026/11 | 軽量鉄骨 | - | A | https://realestate.yahoo.co.jp/rent/detail/000009051523540a9b8661c2de7b60d24d5cdc65c8e3/ |
| 0.71 | 仮称)D-room上京区米屋町ハイツ | 2LDK | 60.19 | 210,000 | 12000 | なし / 25万円 | 1.19 | 3/3 | n | 2026/11 | 軽量鉄骨 | - | A | https://realestate.yahoo.co.jp/rent/detail/000009051523fad77ae166c27c4c7d4ebbaaff06dff4/ |
| 0.71 | 京阪鴨東線 出町柳駅 3階建 築1年未満 | 2LDK | 62.73 | 212,000 | 12000 | なし / 25万円 | 1.18 | 3/3 | n | 2026/11 | 軽量鉄骨 | - | A | https://realestate.yahoo.co.jp/rent/detail/_0000091037518319de41b3b0e65a2284ce2272411420/ |
| 0.71 | 京阪鴨東線 出町柳駅 地上2階建て 築33年 | 4LDK | 65.71 | 135,000 | 0 | なし / なし | 0.0 | 1/2 | n | 1994/4 | 木造 | 近隣あり 15,000円 | house | https://realestate.yahoo.co.jp/rent/detail/_00000909525539a4d82ced0e966f766a90bb7b5f234d/ |
| 0.72 | 京阪鴨東線 出町柳駅 地上2階建て 築56年 | 2LDK | 45.08 | 100,000 | 0 | 10万円 / 20万円 | 2.0 | 2/2 | n | 1970/11 | 木造 | 近隣あり 18,000円 | house | https://realestate.yahoo.co.jp/rent/detail/_000009063786c0468a0a0b6b589fae6a1d732f100419/ |
| 0.74 | 京阪鴨東線 神宮丸太町駅 6階建 築45年 | 3LDK | 59.14 | 130,000 | 8000 | なし / なし | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 | - | old | https://realestate.yahoo.co.jp/rent/detail/_0000075669896badf598ad8d04e460871a0cac267068/ |
| 0.75 | 京阪鴨東線 神宮丸太町駅 地上6階建て 築4 | 3LDK | 80.4 | 130,000 | 8000 | なし / なし | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 | 近隣あり 30,000円 | old | https://realestate.yahoo.co.jp/rent/detail/_00000756698940b6d61488cb23df5a5e39ee4d9b414f/ |
| 0.77 | 聖護院アパルトメント | 2LDK | 94.4 | 190,000 | 4000 | なし / なし | 0.0 | 4/4 | n | 1977/1 | RC | 近隣あり 20,000円 | old | https://realestate.yahoo.co.jp/rent/detail/00000830619119cdf04d7e110a8a16b68a4d8cebcb3f/ |
| 0.78 | シャリエ聖護院西町 | 4LDK | 100.77 | 295,000 | 33000 | 1ヶ月 / 29.5万円 | 1.0 | 5/5 | Y | 2013/1 | RC | 近隣あり 16,000円 | A | https://realestate.yahoo.co.jp/rent/detail/000005101391dfee7e6e7ddcec23858a5dee6c9f6d0b/ |
| 0.78 | 東丸太町貸家 | 3SLDK | 90.0 | 135,000 | 0 | なし / 13.5万円 | 1.0 | 1/2 | n | 1950/5 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/000006095406f8fae7f392c76ba09706d6ba7e5115a2/ |
| 0.78 | 京阪鴨東線 神宮丸太町駅 地上2階建て 築7 | 3LDK | 90.0 | 135,000 | 0 | なし / 13.5万円 | 1.0 | 2/2 | n | 1950/5 | 木造 | 近隣あり 20,000円 | house | https://realestate.yahoo.co.jp/rent/detail/_000006095406c356b0764ad5fec20a8bf913e683b857/ |
| 0.78 | 東丸太町貸家 | 3SLDK | 90.0 | 135,000 | 0 | なし (保証金 なし※) / 27万円※ | 2.0 | 1/2 | n | 1965/1 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/0000048278049ac54cc9214c33d6d30f1abbf20eb9b3/ |
| 0.79 | BRIGH　STONE御所北 | 2LDK | 52.01 | 174,000 | 10000 | 1ヶ月 / 2ヶ月 | 2.0 | 1/3 | Y | 2024/10 | RC | なし | A | https://realestate.yahoo.co.jp/rent/detail/0000080973789e73eb70285db551f2c000b87f7989ea/ |
| 0.8 | 阪急京都本線 烏丸駅 地上2階建て 築25年 | 2LDK | 49.66 | 87,000 | 3000 | なし / なし | 0.0 | 1/2 | n | 2002/7 | 木造 | 近隣あり 19,800円 | A | https://realestate.yahoo.co.jp/rent/detail/_0000067348879ff9d094575f378f92b08bdfc08cf401/ |
| 0.8 | リーガル京都聖護院 | 2LDK | 66.0 | 168,000 | 14030 | なし / 20万円 | 1.19 | 3/5 | Y | 2018/10 | RC | 近隣あり 16,000円 | A | https://realestate.yahoo.co.jp/rent/detail/000003316842f874a8a94654764addf189e692977edd/ |
| 0.8 | 吉田近衛町19-6 | 2LDK | 48.0 | 120,000 | 0 | 12万円 / 24万円 | 2.0 | 2/2 | n | 1993/10 | 木造 | - | B | https://realestate.yahoo.co.jp/rent/detail/0000088599881194940d1b9844fe517ba48697694cc8/ |
| 0.81 | リーガル京都聖護院 | 2LDK | 66.0 | 163,000 | 14030 | なし / 16.3万円※ | 1.0 | 1/5 | Y | 2018/10 | RC | 近隣あり 16,000円 | A | https://realestate.yahoo.co.jp/rent/detail/000003316842a5b7b5e0af0f8aa3d9a73e16ca94bbec/ |
| 0.83 | 吉田近衛町貸家 | 4LDK | 50.34 | 150,000 | 0 | 15万円 / 30万円 | 2.0 | 1/2 | n | 1975/1 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/000009007926f8fae7f392c76ba09706d6ba7e5115a2/ |
| 0.87 | 左京区吉田上大路町戸建 | 2LDK | 49.27 | 200,000 | 0 | 20万円 / 40万円 | 2.0 | 1/2 | n | 2025/10 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/000009088136f8fae7f392c76ba09706d6ba7e5115a2/ |
| 0.87 | 吉田近衛町8-6 貸家 | 4LDK | 92.3 | 150,000 | 0 | 15万円 / 30万円 | 2.0 | 1/2 | n | 1970/1 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/000008892368f8fae7f392c76ba09706d6ba7e5115a2/ |
| 0.87 | 吉田近衛町8－6貸家 | 4LDK | 50.34 | 150,000 | 0 | 15万円※ (保証金 なし※) / 30万円※ | 2.0 | 1/2 | n | 1970/1 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/000008892368a6a9aab45bd490302dc7b941dd5b903a/ |
| 0.87 | 吉田上大路町19-1 貸家 | 3SLDK | 94.92 | 230,000 | 0 | 23万円 / 46万円 | 2.0 | 1/2 | n | 2016/2 | 木造 | あり 無料 | house | https://realestate.yahoo.co.jp/rent/detail/000004357545f8fae7f392c76ba09706d6ba7e5115a2/ |
| 0.88 | 京都市営地下鉄東西線 東山駅 地上2階建て  | 3LDK | 50.34 | 150,000 | 0 | 1ヶ月 / 30万円 | 2.0 | 0/2 | n | 1964/4 | 木造 | 近隣あり 16,000円 | house | https://realestate.yahoo.co.jp/rent/detail/_00000909463233ddc137c8c91f3faf914c87706a248d/ |
| 0.89 | リソシエ鴨川グランディス | 3LDK | 78.04 | 190,000 | 0 | 19万円 / 38万円 | 2.0 | 3/7 | Y | 2000/10 | RC | - | B | https://realestate.yahoo.co.jp/rent/detail/0000034704800d07033bcaf4ee011330c64574b57f6d/ |
| 0.9 | 京阪鴨東線 神宮丸太町駅 3階建 築8年 | 2LDK | 54.56 | 124,000 | 12000 | なし / 5万円 | 0.4 | 1/3 | n | 2018/12 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_000005155135b23148bc6e7b88dea4449842284f05ce/ |
| 0.92 | 聖護院東町貸家 | 4SLDK | 145.0 | 230,000 | 0 | 30万円 / 40万円 | 1.74 | 1/3 | n | 1992/3 | 鉄骨 | あり 無料 | house | https://realestate.yahoo.co.jp/rent/detail/000002690779f8fae7f392c76ba09706d6ba7e5115a2/ |
| 0.95 | シャルト北苑 | 3LDK | 69.03 | 140,000 | 10000 | 2ヶ月 / 14万円 | 1.0 | 1/3 | n | 1984/1 | RC | 近隣あり 15,000円 | old | https://realestate.yahoo.co.jp/rent/detail/00000151453214cd07bdf71de478101d99ae744a68bc/ |
| 0.95 | シャルト北苑 | 3LDK | 71.72 | 145,000 | 10000 | 1ヶ月 / なし | 0.0 | 2/3 | n | 1984/1 | RC | あり 15,000円 | old | https://realestate.yahoo.co.jp/rent/detail/000001514532c8d9747f65272fb85fa5f3ee0c8193d5/ |
| 0.95 | シャルト北苑 | 4LDK | 69.03 | 135,000 | 10000 | 1ヶ月 / なし | 0.0 | 3/3 | n | 1984/1 | RC | あり 15,000円 | old | https://realestate.yahoo.co.jp/rent/detail/000001514532ac4f3868a2b43b5f39117c028956dca3/ |
| 0.99 | 京阪鴨東線 神宮丸太町駅 5階建 築1年未満 | 2LDK | 58.45 | 250,000 | 0 | 25万円 / 50万円 | 2.0 | 1/5 | Y | 2026/8 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_000009102615e494e28b6963171af44b9d735042d1c5/ |
| 0.99 | 京都グランドハイツ | 2LDK | 64.5 | 140,000 | 10000 | 14万円※ (保証金 なし※) / 14万円※ | 1.0 | 4/7 | Y | 1971/6 | RC | - | old | https://realestate.yahoo.co.jp/rent/detail/000001334108d8065aa1dca0b25e2dba9d735b339a2b/ |
| 0.99 | 京阪鴨東線 出町柳駅 地上2階建て 築37年 | 5LDK | 153.83 | 250,000 | 0 | 2ヶ月 / 25万円 | 1.0 | 1/2 | n | 1990/6 | 木造 | あり 無料 | house | https://realestate.yahoo.co.jp/rent/detail/_0000090341163667639623a638353424025cdb1928ac/ |
| 1.0 | 京阪鴨東線 神宮丸太町駅 5階建 築10年 | 2LDK | 56.13 | 210,000 | 10000 | 21万円 / 21万円 | 1.0 | 2/5 | Y | 2016/12 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_00000129305376e661062ee6335e45158940924aca8f/ |
| 1.01 | 京阪鴨東線 神宮丸太町駅 3階建 築10年 | 3LDK | 73.75 | 210,000 | 20000 | 21万円 / 42万円 | 2.0 | 1/3 | Y | 2017/1 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_000004018859374571855a7a6f58df5e3575b521b2cb/ |
| 1.01 | 上神輿町貸家 | 7SLDK | 156.91 | 220,000 | 0 | 22万円 / 22万円 | 1.0 | 1/3 | n | 1982/2 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/0000090550835af58480ccd322b9082f72bc4750ea2c/ |
| 1.02 | かぐら坂荘 | 2LDK | 60.23 | 127,000 | 7000 | なし / 12.7万円 | 1.0 | 3/3 | n | 2011/3 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/000000985671224bb24e48f9c16b7bcc408a73ca5b84/ |
| 1.03 | 京阪鴨東線 出町柳駅 地上2階建て 築45年 | 8LDK | 93.19 | 220,000 | 0 | 1ヶ月 / 22万円 | 1.0 | None/2 | n | 1982/2 | 木造 | 近隣あり 15,000円 | house | https://realestate.yahoo.co.jp/rent/detail/_0000090542101500433ad891d4fe8e849c3396450252/ |
| 1.03 | 中京区寺町通　貸戸建 | 4LDK | 132.36 | 220,000 | 0 | 22万円 / 22万円 | 1.0 | 1/2 | n | 1927/1 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/00000875338086e878863d24ca415f754a867daa34c4/ |
| 1.04 | 京都グランドハイツ | 2LDK | 64.5 | 140,000 | 10000 | 14万円 / 14万円 | 1.0 | 2/7 | Y | 1971/6 | RC | - | old | https://realestate.yahoo.co.jp/rent/detail/000001334108e707cbb56f8b077c90800a666cd674d0/ |
| 1.04 | 吉田中大路町34ー109貸家 | 3SLDK | 114.0 | 498,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1910/1 | 木造 | あり | house | https://realestate.yahoo.co.jp/rent/detail/0000084547659cb144d97ceb0ec8b45874dee08a9b57/ |
| 1.06 | 京都市営地下鉄烏丸線 丸太町駅 地上1階建て | 3DK | 69.35 | 90,000 | 0 | 9万円 / 9万円 | 1.0 | 1/1 | n | 2001/8 | 木造 | 近隣あり 16,000円 | house | https://realestate.yahoo.co.jp/rent/detail/_000008735676d14f0d9d2436202ded2dc48d1ef5d6ab/ |
| 1.06 | イスターナイマイ鴨川西 | 2LDK | 50.65 | 150,000 | 9000 | なし / 20万円 | 1.33 | 3/5 | Y | 2013/2 | RC | 近隣あり 46,095円 | A | https://realestate.yahoo.co.jp/rent/detail/0000038525698f82513ae17bbc58dd92fda44896d6a8/ |
| 1.06 | イスターナイマイ鴨川西 | 2LDK | 50.65 | 153,000 | 9000 | なし / 20万円 | 1.31 | 5/5 | Y | 2013/2 | RC | 近隣あり 46,095円 | A | https://realestate.yahoo.co.jp/rent/detail/000003852569cebd60d73f98ede3e95b0bac5bd3fb27/ |
| 1.07 | 京阪鴨東線 神宮丸太町駅 3階建 築21年 | 3LDK | 89.44 | 260,000 | 10000 | 26万円 / 52万円 | 2.0 | 3/3 | Y | 2006/3 | RC | あり 33,000円 | A | https://realestate.yahoo.co.jp/rent/detail/_0000029237353c696b67a30a71d3c6d0c9e2b9fb1910/ |
| 1.08 | グレーシー北白川 | 3LDK | 68.39 | 130,000 | 0 | 1ヶ月 / 13万円 | 1.0 | 3/3 | n | 1991/8 | RC | あり 20,000円 | B | https://realestate.yahoo.co.jp/rent/detail/0000034992905574e1cf8c6f4b563679489a30b1f8f9/ |
| 1.1 | 吉田本町5－66貸家 | 5DK | 138.54 | 330,000 | 0 | 33万円 / 33万円 | 1.0 | 1/2 | n | 1930/1 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/000003480393f06349d8eeded547d9224f1445faf79d/ |
| 1.1 | 京都市営地下鉄東西線 京都市役所前駅 7階建 | 2LDK | 61.12 | 195,000 | 10000 | 19.5万円 / 19.5万円 | 1.0 | 2/7 | Y | 2026/3 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_0000087661352101a7f36efbd6217b0beaf992aef837/ |
| 1.1 | 京都市営地下鉄東西線 京都市役所前駅 7階建 | 2LDK | 61.12 | 198,000 | 10000 | 19.8万円 / 19.8万円 | 1.0 | 5/7 | Y | 2026/3 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_0000087661359523accf93a7b46d42ea6a5a2caa003c/ |
| 1.12 | グランタック東山二条 | 2LDK | 57.75 | 130,000 | 8000 | 1ヶ月 / なし | 0.0 | 5/7 | Y | 1977/4 | RC | なし | old | https://realestate.yahoo.co.jp/rent/detail/000004470951f1efc71048c4e86bacd9946572585be3/ |
| 1.12 | グランタック東山二条 | 2LDK | 56.0 | 130,000 | 8000 | 1ヶ月 / なし | 0.0 | 5/6 | Y | 1977/1 | RC | - | old | https://realestate.yahoo.co.jp/rent/detail/0000044709517e815c4c1c27db3af40fec7f65304b4b/ |
| 1.13 | エルミタージュ下鴨東 | 2LDK | 55.43 | 125,000 | 8500 | なし / なし | 0.0 | 2/2 | n | 2024/7 | 軽量鉄骨 | - | A | https://realestate.yahoo.co.jp/rent/detail/000008143678e006e29fc6c31d86ad25b3fdec98dd95/ |
| 1.14 | KB.メゾンロータス | 2LDK | 51.17 | 121,000 | 4600 | なし / 12.1万円※ | 1.0 | 1/3 | n | 2011/3 | 鉄骨 | 近隣あり 46,095円 | A | https://realestate.yahoo.co.jp/rent/detail/00000106001757c6b2b5dbbbd81cdc2f602326a508a0/ |
| 1.16 | ベルリード　Millesime寺町 | 2LDK | 69.97 | 230,000 | 10000 | 23万円 / 23万円 | 1.0 | 2/3 | n | 2026/11 | 木造 | - | A | https://realestate.yahoo.co.jp/rent/detail/0000090425713fa8317a3103d2f65988e9ed832aa493/ |
| 1.17 | メゾンフジ | 3LDK | 80.0 | 135,000 | 5000 | なし / なし | 0.0 | 2/5 | n | 1985/10 | 鉄骨 | - | old | https://realestate.yahoo.co.jp/rent/detail/00000435046777d7ddccaaea6887c87372ff7a8f574e/ |
| 1.17 | 田中野神町6－18貸家 | 6DK | 145.36 | 150,000 | 0 | 15万円※ / 15万円 | 1.0 | 1/4 | n | 1976/8 | 鉄骨 | - | house | https://realestate.yahoo.co.jp/rent/detail/000008223247d351180f212c21bf53dd50ea60dfbeda/ |
| 1.17 | 叡山電鉄叡山本線 元田中駅 地上4階建て 築 | 6DK | 145.36 | 150,000 | 0 | 1ヶ月 / 30万円 | 2.0 | None/4 | n | 1976/8 | 鉄骨 | 近隣あり 16,500円 | house | https://realestate.yahoo.co.jp/rent/detail/_00000822324751d69fadb254ca8ac708bafb06a6543f/ |
| 1.18 | ヴィークコート京都河原町二条 | 3LDK | 75.13 | 380,000 | 0 | 1ヶ月※ / 76万円 | 2.0 | 7/7 | Y | 2023/8 | RC | 近隣あり 25,000円 | A | https://realestate.yahoo.co.jp/rent/detail/00000777248232cde54ee950df8cd1d4a4e553064197/ |
| 1.19 | 京阪鴨東線 神宮丸太町駅 5階建 築26年 | 3LDK | 72.57 | 168,000 | 12000 | なし / 20万円 | 1.19 | 3/5 | Y | 2001/6 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_000003275726e9d3f8eca538e55238f20fc0d316e2e5/ |
| 1.19 | 岡崎最勝寺町貸家 | 6DK | 118.57 | 228,000 | 0 | 22.8万円 / 25.08万円 | 1.1 | 1/2 | n | 1914/1 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/000008792197d034efc3a09361b9693f1292e48e080a/ |
| 1.21 | 北白川追分町貸家 | 5DK | 63.66 | 88,000 | 0 | 8.8万円 / 10万円 | 1.14 | 1/2 | n | 1988/8 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/0000090594258391547e231249dbe7fc0e0ed86b934a/ |
| 1.21 | コーポ富有 | 2LDK | 48.51 | 100,000 | 9000 | 10万円 / 10万円 | 1.0 | 2/4 | Y | 1985/7 | RC | - | old | https://realestate.yahoo.co.jp/rent/detail/0000019015614ae5cb62464c0a9dfe870afa456fd82e/ |
| 1.23 | 京都市営地下鉄東西線 三条京阪駅 地上5階建 | 3LDK | 66.97 | 125,000 | 10000 | なし / 12.5万円 | 1.0 | 5/5 | Y | 1999/11 | RC | 近隣あり 20,000円 | B | https://realestate.yahoo.co.jp/rent/detail/_000001694410f7b471e6699563b27f8a6278fa00288b/ |
| 1.23 | 京都市営地下鉄東西線 京都市役所前駅 7階建 | 2LDK | 66.49 | 240,000 | 0 | なし / 48万円 | 2.0 | 5/7 | Y | 2013/9 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_000005708613946bf5824dabae3758a2c9bec9086e93/ |
| 1.23 | ジオ御所南 河原町二条 | 2LDK | 73.46 | 230,000 | 20000 | 25万円 / 37.5万円 | 1.63 | 4/7 | Y | 2013/9 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/0000057086136c4e592ed9f6f98a217168202bf9b2eb/ |
| 1.23 | 京都市営地下鉄東西線 京都市役所前駅 地上7 | 2LDK | 66.49 | 230,000 | 17950 | 1ヶ月 / 1ヶ月 | 1.0 | 5/7 | Y | 2021/2 | RC | なし | A | https://realestate.yahoo.co.jp/rent/detail/_0000090606771650ac7d343f4a20d2dd4b031da99d34/ |
| 1.25 | 京都市営地下鉄烏丸線 丸太町駅 地上3階建て | 2LDK | 60.04 | 198,000 | 12000 | なし / 39.6万円 | 2.0 | 3/3 | Y | 2023/10 | RC | 近隣あり 25,000円 | A | https://realestate.yahoo.co.jp/rent/detail/_0000076227243387ddf74362ce0b89b552b3e1332f89/ |
| 1.25 | 京都市営地下鉄烏丸線 丸太町駅 5階建 築1 | 2LDK | 76.29 | 270,000 | 20000 | なし / 54万円 | 2.0 | 4/5 | Y | 2026/4 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_000008800578d17e4a4183b986918832d17d9c409e6a/ |
| 1.25 | ルアージュ御所南 | 2LDK | 76.29 | 265,000 | 20000 | なし (保証金 なし※) / 53万円※ | 2.0 | 3/5 | Y | 2026/4 | RC | あり 55,000円 | A | https://realestate.yahoo.co.jp/rent/detail/000008895385dc1c8212f19bc54b373751109603efb0/ |
| 1.26 | アルカンシェル御所 | 2LDK | 57.17 | 144,000 | 10000 | 1ヶ月 / 14.4万円 | 1.0 | 3/6 | Y | 1987/3 | RC | 近隣あり 25,000円 | old | https://realestate.yahoo.co.jp/rent/detail/00000151714132f43abcf21fb11105938df82770b103/ |
| 1.26 | フロンテージ堺町御門 | 2LDK | 68.44 | 225,000 | 9000 | 5万円 (保証金 なし※) / 45万円 | 2.0 | 2/3 | Y | 2023/3 | 鉄骨 | - | A | https://realestate.yahoo.co.jp/rent/detail/00000728440047b25266c6ff8fb85a8cd591657e0a91/ |
| 1.26 | 京都市営地下鉄烏丸線 丸太町駅 5階建 築1 | 2LDK | 76.29 | 260,000 | 20000 | なし / 52万円 | 2.0 | 2/5 | Y | 2026/4 | RC | - | A | https://realestate.yahoo.co.jp/rent/detail/_000008799340e92952b2d8e7120e7b1250d254d21d48/ |
| 1.27 | 布袋屋町496-5貸家 | 2LDK | 73.82 | 210,000 | 0 | 21万円 / 21万円 | 1.0 | 1/2 | n | 1970/5 | 木造 | - | house | https://realestate.yahoo.co.jp/rent/detail/000005517851087cf8a3c997a9f9d791206429955d14/ |
| 1.29 | 北白川コーポラス | 3DK | 57.0 | 100,000 | 8000 | 1ヶ月 / 10万円 | 1.0 | 3/4 | n | 1970/10 | RC | あり 8,000円 | old | https://realestate.yahoo.co.jp/rent/detail/000001865376ecb655ac395555c046c75d304dbb0880/ |
| 1.3 | 北白川コーポラス | 3LDK | 66.0 | 100,000 | 8000 | 10万円 / 10万円 | 1.0 | 3/4 | n | 1970/3 | RC | あり 8,000円 | old | https://realestate.yahoo.co.jp/rent/detail/0000018653765b0d01f03c710e8c6e0b5b6b07519369/ |
