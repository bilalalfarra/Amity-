# homes — LIFULL HOME'S (homes.co.jp), WALK survey (≤1.3 km of 京都技術科学センター, 左京区吉田河原町14), fetched 2026-10-18

## Method
- Ward list URL https://www.homes.co.jp/chintai/kyoto/<ward>/list/ with server-side cond: 専有面積≥45㎡, 2LDK/3DK/3LDK/4DK/4LDK以上 only (**no rent cap, no age / structure condition**), sort 築年数が新しい順. Wards kyoto_sakyo / kamigyo / nakagyo-city; site unit totals {'all_kyoto_sakyo-city': 1194, 'all_kyoto_kamigyo-city': 1357, 'all_kyoto_nakagyo-city': 1776}; 68 list pages (raw: out/raw/homes/listall_*).
- **Fetching (AWS WAF)**: python never requested HOME'S. Every list and unit page was loaded by headless Chromium (`homes_fetch.js`: HTML document only, 10–14 s between pages, fresh browser context every 9 pages with a 45 s pause, MAX_CAPTCHA=1 = stop at the first CAPTCHA). Browser runs: 3; pages ok 262, failed 0, CAPTCHAs 0, contexts 31, unfetched 0. No CAPTCHA was solved or bypassed.
- Funnel: list_units 4363, pr_units 136, drop_layout_list 14, drop_area_list 0, dup_same_unit 2409, drop_station_bound_list 1335, geocode_inconsistent_list 53, drop_far_list 230, geocode_fail_list 0, detail_fetched 194, detail_http_fail 0, drop_far 17, dup_same_unit_detail 8, kept 169. Same unit listed by several agencies merged (cheapest kept; other URLs in notes).
- Distance: Kyoto 通り名 addresses reduced to ward+町名 (kgeo.py) and geocoded with GSI (mostly 町名 level, ±300 m → kept up to 1.5 km, flagged); every position checked against the listing's 駅徒歩N分 (≤ N×80 m from that station) — impossible ones dropped already at list stage, contradicting geocodes replaced by the station position (geofix.py).
- `elevator=false` means the unit page's 設備 list exists but has no エレベーター; null if no list. Nameless buildings (HOME'S shows the access text) have building_name null. `http_status` = status of the unit page as loaded by the browser.
- Station plausibility check (geofix.py; Kyoto town names repeat, GSI returns one): {'checked': 169, 'no_station': 0, 'inconsistent_moved': 3, 'dropped_lower_bound': 2, 'roughly_consistent_kept': 1}; dropped (cannot be ≤1.3 km given the listed 駅徒歩): 2 → out/homes_geodropped.json.

## Result
- **Kept 160 units** (after merging 7 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via the same building name in another listing with a full address, 0 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 81; rent range kept: 79000–500000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'B': 6, 'house': 35, 'old': 36, 'A': 83}; 礼金 ≤1ヶ月 87, >1ヶ月 73, unknown 0 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'town': 148, 'address (GSI)': 9, 'station': 3} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 89/70/1; by ward: {'左京区': 62, '上京区': 65, '中京区': 33}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/homes/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.03 | エーデルハイム鴨川 | 3LDK | 65.77 | 138,000 | 10000 | 20万円 / 35万円 | 2.54 | 5/5 | Y | 1997/2 | RC | 空有 21,000円(税込) | B | https://www.homes.co.jp/chintai/room/cc25937737dd6f34fdefc0cda60a87bc8926d5c0/ |
| 0.21 |  | 2LDK | 66.7 | 120,000 | 0 | 無 / 24万円 | 2.0 | None/2 | n | 2004/12 | 木造 | 近隣 18,000円(税無) 物件からの距離23 | house | https://www.homes.co.jp/chintai/room/98c957bdc4b189e5652bbc8fbb45541cb562be06/ |
| 0.25 | 今智庵 | 3DK | 65.0 | 100,000 | 0 | 10万円 / 20万円 | 2.0 | None/2 | n | 1984/11 | 木造 | 無 | house | https://www.homes.co.jp/chintai/b-1051710235991/ |
| 0.25 |  | 3DK | 54.67 | 100,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/2 | n | 1984/11 | 木造 | 近隣 18,000円(税無) 物件からの距離44 | house | https://www.homes.co.jp/chintai/room/bb200d5bb411a04e8184c60230571419ddcdd2a7/ |
| 0.27 | 上阿達谷口マンション | 2LDK | 46.12 | 110,000 | 6000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/4 | n | 1989/5 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/eda163bbff370e625d2daeb44e267a9c3f2755d3/ |
| 0.27 | 上阿達谷口マンション | 3DK | 45.7 | 110,000 | 6000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/4 | n | 1989/4 | RC | 近隣 18,000円(税無) 物件からの距離42 | old | https://www.homes.co.jp/chintai/room/281e9539f62174c1156c7f09b9aa3a449129a55f/ |
| 0.29 | 吉田上阿達町7-19 貸家 | 3LDK | 101.65 | 250,000 | 0 | 1ヶ月 / 1.5ヶ月 | 1.5 | 1/2 | n | 2019/2 | 木造 | 空有 無料 | house | https://www.homes.co.jp/chintai/room/5796cea6e124388502e3fe04190d1848ecbdeb6f/ |
| 0.34 | THE RESIDENCE御車道 | 2LDK | 59.7 | 179,000 | 10000 | 1ヶ月 / 20万円 | 1.12 | 1/4 | Y | 2026/8 | RC | 近隣 19,800円(税込) 物件からの距離19 | A | https://www.homes.co.jp/chintai/room/827820aae035ef444a6a2dddbf11fa70892efc55/ |
| 0.34 | 梶井町貸家 | 5DK | 93.54 | 180,000 | 0 | 30万円 / 30万円 | 1.67 | None/2 | n | 1970/4 | 木造 | 空無 | house | https://www.homes.co.jp/chintai/room/325358f678163f48c7959f6251e74d38a87af786/ |
| 0.34 | THE RESIDENCE御車道 | 2LDK | 59.7 | 192,000 | 10000 | 1ヶ月 / 20万円 | 1.04 | 2/4 | Y | 2026/8 | RC | 近隣 19,800円(税込) 物件からの距離19 | A | https://www.homes.co.jp/chintai/room/f8696e339ca4b31bf433ca1a47eafd3fda5f2cc3/ |
| 0.34 |  | 5DK | 93.54 | 200,000 | 0 | 30万円 / 30万円 | 1.5 | None/2 | n | 1997/2 | 木造 | 空有 (1台) 無料 | house | https://www.homes.co.jp/chintai/room/a149cb2e94f3db2e4a9baef84963ab58e049ec71/ |
| 0.34 | THE RESIDENCE御車道 | 2LDK | 68.58 | 205,000 | 10000 | 1ヶ月 / 25万円 | 1.22 | 1/4 | Y | 2026/8 | RC | 近隣 19,800円(税込) 物件からの距離19 | A | https://www.homes.co.jp/chintai/room/be181900316cb7ec37aabfa4e4dbd9893953d497/ |
| 0.34 | エスタプレイス | 2LDK | 68.55 | 206,000 | 7500 | 無 / 20.6万円 | 1.0 | 2/6 | Y | 2027/4 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/08388d3fe399da45ece0e5903556f4be23f5b75c/ |
| 0.34 | エスタプレイス | 2LDK | 68.55 | 207,000 | 7500 | 無 / 20.7万円 | 1.0 | 3/6 | Y | 2027/4 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/616cc0e9decd5dc06d1f065c3ec566b001bb09e3/ |
| 0.34 | エスタプレイス | 2LDK | 68.55 | 208,000 | 7500 | 無 / 1ヶ月 | 1.0 | 5/6 | Y | 2027/3 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/9b40a9faba14dd852574bc9a6c879d3c61fc1c72/ |
| 0.34 | エスタプレイス | 2LDK | 75.03 | 215,000 | 7500 | 無 / 21.5万円 | 1.0 | 2/6 | Y | 2027/4 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/20fa44d912d30dc16a670bad68d3096c6d1909a9/ |
| 0.34 |  | 2LDK | 73.03 | 215,000 | 7500 | 無 / 21.5万円 | 1.0 | 2/6 | Y | 2027/4 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/a5ac89470bb8f47d1caf3c85190807433b76946c/ |
| 0.34 | エスタプレイス | 2LDK | 75.03 | 216,000 | 7500 | 無 / 21.6万円 | 1.0 | 4/6 | Y | 2027/4 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/69f62e0a2c371038b2171f9b43c9430388a0c206/ |
| 0.34 | エスタプレイス | 2LDK | 75.03 | 216,000 | 7500 | 無 / 21.6万円 | 1.0 | 3/6 | Y | 2027/4 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/74939d35852400f571d0648dbc1839e586e98ec1/ |
| 0.34 |  | 2LDK | 73.03 | 216,000 | 7500 | 無 / 21.6万円 | 1.0 | 4/6 | Y | 2027/4 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/3db628beac1855d0adb42ed2b38d4bb5dccd89c1/ |
| 0.34 |  | 2LDK | 73.03 | 216,000 | 7500 | 無 / 21.6万円 | 1.0 | 3/6 | Y | 2027/4 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/8837db7fe2fb6d0597f66e7424ae8d8d4f18b4a9/ |
| 0.41 | ＢｅｌｌｅＬｅａｄ御所東 | 2LDK | 61.69 | 174,000 | 6000 | 無 / 17.4万円 | 1.0 | 1/2 | n | 2025/9 | 木造 | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/8b1078d3d3bea25d38995a344001c4894a6c31cb/ |
| 0.46 | ノーベルテラス稔 | 2LDK | 57.76 | 220,000 | 8000 | 22万円 / 44万円 | 2.0 | 4/5 | Y | 2003/3 | その他 | 無 | A | https://www.homes.co.jp/chintai/room/a007a13ad7b7fd476d88b6d37379c3ecb759a6ec/ |
| 0.47 | ザ・パークハウス京都鴨川御所東 | 2LDK | 104.1 | 465,000 | 0 | 46.5万円 / 93万円 | 2.0 | 5/5 | Y | 2017/3 | RC | 空無 | A | https://www.homes.co.jp/chintai/room/bd68fad6e15cc5198ddd69593f32f2be2c1ef048/ |
| 0.49 | BelleLead御所東 | 2SLDK | 53.0 | 159,000 | 6000 | 無 / 無 | 0.0 | 1/2 | n | 2025/9 | 木造 | 空有 (1台) 20,000円(税込) 小型車に | A | https://www.homes.co.jp/chintai/b-1014960007052/ |
| 0.49 | BelleLead御所東 | 2SLDK | 61.69 | 179,000 | 6000 | 無 / 無 | 0.0 | 2/2 | n | 2025/9 | 木造 | 空有 (1台) 20,000円(税込) 小型車に | A | https://www.homes.co.jp/chintai/b-1014960007053/ |
| 0.5 |  | 2LDK | 64.2 | 160,500 | 9000 | 無 / 32.1万円 | 2.0 | 2/5 | Y | 2008/10 | RC | 空有 23,100円(税込) | A | https://www.homes.co.jp/chintai/room/82f76fa1162152b630cfbc9b9dd0ef28fe5c4622/ |
| 0.5 | Grand E’terna 京大正門前 | 2LDK | 56.53 | 160,500 | 9000 | 無 / 2ヶ月 | 2.0 | 2/5 | Y | 2008/9 | RC | 空有 (1台) 23,100円(税込) | A | https://www.homes.co.jp/chintai/room/46a53ad23d21f53e013e71771e70883dda3432ca/ |
| 0.5 |  | 3LDK | 71.07 | 169,500 | 9000 | 無 / 33.9万円 | 2.0 | 2/5 | Y | 2008/10 | RC | 空有 23,100円(税込) | A | https://www.homes.co.jp/chintai/room/f748682e1d5c9464f6f01725ff756e30c9e8c2c8/ |
| 0.54 | ノーベルテラス稔 | 2LDK | 54.86 | 220,000 | 8000 | 22万円 / 44万円 | 2.0 | 4/5 | Y | 2003/3 | その他 | 無 | A | https://www.homes.co.jp/chintai/room/f937fde9fe4393fe96ccae575db68acb9e98f3ec/ |
| 0.56 |  | 2LDK | 94.4 | 190,000 | 4000 | 無 / 無 | 0.0 | 4/4 | n | 1977/1 | RC | 近隣 20,000円(税込) 物件からの距離36 | old | https://www.homes.co.jp/chintai/room/bb1637fcb57f282abe50433a6cec16ba03f75092/ |
| 0.56 |  | 3LDK | 78.04 | 215,000 | 10000 | 21.5万円 / 21.5万円 | 1.0 | 6/7 | Y | 2003/10 | RC | 無 | A | https://www.homes.co.jp/chintai/room/2c29c4270c821917b02bb618b23799fdb1aa3d29/ |
| 0.59 | ベリエ茶五 | 2LDK | 53.96 | 145,000 | 15000 | 無 / 1.5ヶ月 | 1.5 | 2/6 | Y | 2008/3 | RC | 空有 20,000円(税込) | A | https://www.homes.co.jp/chintai/room/930e5969f8dbf89ccc898a6cb1c6f0c12188badc/ |
| 0.59 | ベリエ茶五 | 2LDK | 54.72 | 150,000 | 15000 | 無 / 2ヶ月 | 2.0 | 3/6 | Y | 2008/3 | RC | 空有 20,000円(税込) | A | https://www.homes.co.jp/chintai/room/07e1dc3cc51552ba74acb24dfe0846e529e92922/ |
| 0.59 | ベリエ茶五 | 2LDK | 60.25 | 155,000 | 15000 | 無 / 2ヶ月 | 2.0 | 2/6 | Y | 2008/3 | RC | - | A | https://www.homes.co.jp/chintai/b-1558350000193/ |
| 0.59 | ベリエ茶五 | 2LDK | 60.25 | 160,000 | 15000 | 無 / 32万円 | 2.0 | 4/6 | Y | 2008/3 | RC | 近隣 15,000円(税無) 物件からの距離47 | A | https://www.homes.co.jp/chintai/room/d0e80a68f93e2c64914bc83bdbc3ddd7d76e87c9/ |
| 0.59 | ベリエ茶五 | 2LDK | 60.25 | 165,000 | 16000 | 無 / 33万円 | 2.0 | 5/6 | Y | 2008/3 | RC | 空有 16,500円(税込) 駐車料金：1650 | A | https://www.homes.co.jp/chintai/b-13670265170/ |
| 0.59 | ベリエ茶五 | 2LDK | 60.25 | 190,000 | 17000 | 無 / 2ヶ月 | 2.0 | 6/6 | Y | 2008/3 | RC | 空有 20,000円(税込) | A | https://www.homes.co.jp/chintai/room/7022777fa184cdadcc806e9c831ef70566c21146/ |
| 0.61 | 鴨川グランドコーポ | 3LDK | 78.67 | 235,000 | 15000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/5 | Y | 1981/5 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/fb68f22db9d77e714e85c309b6954c9e883132be/ |
| 0.61 | 鴨川グランドコーポ | 2LDK | 95.22 | 470,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 4/5 | Y | 1981/5 | RC | 無 | old | https://www.homes.co.jp/chintai/room/4f130ad8562f8db748a6238e5c0f376fd33a2f2f/ |
| 0.62 | ピアハウス出町 | 4LDK | 145.42 | 280,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 2/3 | n | 1998/11 | 鉄骨 | 近隣 15,000円(税無) 物件からの距離39 | B | https://www.homes.co.jp/chintai/room/1cd785fc6e449a0d6a96dd01e7e08f565a677304/ |
| 0.62 | ピアハウス出町 | 4LDK | 145.42 | 280,000 | 0 | 28万円 / 56万円 | 2.0 | None/3 | n | 1998/11 | その他 | 空無 | house | https://www.homes.co.jp/chintai/room/3956f16377f0e409a5aafcf761e855a3ed450f01/ |
| 0.63 | グランレブリー御所東II | 2LDK | 53.94 | 136,000 | 10000 | 無 / 13.6万円 | 1.0 | 1/3 | n | 1987/3 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/288f82f728d45b858fe7483d5c2be2660485a621/ |
| 0.63 | グランレブリー御所東II | 2LDK | 53.94 | 138,000 | 10000 | 無 / 13.8万円 | 1.0 | 2/3 | n | 1987/3 | RC | 空無 | old | https://www.homes.co.jp/chintai/b-13670322765/ |
| 0.63 |  | 3LDK | 113.88 | 402,000 | 18000 | 40.2万円 / 40.2万円 | 1.0 | 9/10 | Y | 2007/9 | RC | 空有 25,300円(税込) | A | https://www.homes.co.jp/chintai/room/d5710a76b95a8fac081a0fd0b6821d21cea8987a/ |
| 0.64 | 南向・部屋数多い貸戸建 | 4LDK | 123.8 | 160,000 | 0 | 2ヶ月 / 1ヶ月 | 1.0 | None/2 | n | 1982/10 | 軽量鉄骨 | 空無 | house | https://www.homes.co.jp/chintai/room/781c38e95f4023a19ec845a51fde9326beea4577/ |
| 0.68 | 南町貸家 | 4DK | 111.94 | 168,000 | 0 | 15万円 / 20万円 | 1.19 | 1/3 | n | 1994/2 | 木造 | 空有 料金：賃料に含む | house | https://www.homes.co.jp/chintai/room/43ec5fc5b681a7f8968d0095fd98f7be2c0dca27/ |
| 0.7 |  | 4LDK | 50.34 | 150,000 | 0 | 15万円 / 30万円 | 2.0 | None/2 | n | 1975/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/1ae95d13bd431f0b544434d3a2c2d0aa06d93d63/ |
| 0.7 |  | 3LDK | 50.34 | 150,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | None/2 | n | 1964/4 | 木造 | 近隣 16,000円(税無) 物件からの距離32 | house | https://www.homes.co.jp/chintai/room/0ce07d0294f09ec96884159f4de409cd09f5491b/ |
| 0.71 |  | 3SLDK | 90.0 | 135,000 | 0 | 無 / 27万円 | 2.0 | None/2 | n | 1965/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/ce0dc691f55f153e66f61db0b7254dd9b221d330/ |
| 0.71 |  | 3LDK | 90.0 | 135,000 | 0 | 無 / 1ヶ月 | 1.0 | 2/2 | n | 1950/5 | 木造 | 近隣 20,000円(税込) 物件からの距離30 | house | https://www.homes.co.jp/chintai/room/617cc9de45f8d2dc5a0eda9fe5df51c142f884b1/ |
| 0.71 | 東丸太町貸家 | 3SLDK | 90.0 | 135,000 | 0 | 無 / 13.5万円 | 1.0 | None/2 | n | 1950/5 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/2783e5b6657c7efef8c19a9eb304062b9d7c9d7e/ |
| 0.71 | アルス丸太町山水庵 | 3LDK | 117.57 | 280,000 | 17100 | 28万円 / 56万円 | 2.0 | 3/5 | Y | 2002/3 | RC | 無 | A | https://www.homes.co.jp/chintai/room/fb7f5440307b0fda6e6fd87e165da52b9c0096a7/ |
| 0.74 |  | 4LDK | 65.71 | 135,000 | 0 | 無 / 無 | 0.0 | 1/2 | n | 1994/4 | 木造 | 近隣 15,000円(税無) 物件からの距離41 | house | https://www.homes.co.jp/chintai/room/f713330d165da124cca63de98480e2802bd07d0c/ |
| 0.75 | サンアートビル | 3LDK | 80.4 | 130,000 | 8000 | 無 / 無 | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 | 近隣 30,000円(税込) 物件からの距離14 | old | https://www.homes.co.jp/chintai/room/0b7153a2114e2732959a686a1473ff946226b7a4/ |
| 0.75 | サンアートビル | 3LDK | 59.41 | 130,000 | 8000 | 無 / 無 | 0.0 | 5/6 | Y | 1981/12 | RC | 無 | old | https://www.homes.co.jp/chintai/room/3324aee3c94e5e6b398f792595933820b2bcd1e1/ |
| 0.75 | サンアートビル | 3DK | 59.14 | 130,000 | 8000 | 無 / 無 | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 | 無 | old | https://www.homes.co.jp/chintai/room/5346e66824a3b5c13c14da724aaa9ebd0bd5fdde/ |
| 0.75 |  | 5DK | 103.68 | 250,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 2/2 | n | 1987/1 | 木造 | 近隣 16,000円(税無) 物件からの距離46 | house | https://www.homes.co.jp/chintai/room/a464dd83cc1e92a4ca4d332af46dbd2dd9b68ca2/ |
| 0.75 | シャリエ聖護院西町 | 4LDK | 100.77 | 295,000 | 33000 | 1ヶ月 / 1ヶ月 | 1.0 | 5/5 | Y | 2013/1 | RC | 近隣 16,000円(税無) 物件からの距離44 | A | https://www.homes.co.jp/chintai/room/28637cdf3e1c4c21d78b70b69434b30c0aec6d8f/ |
| 0.8 | ファーストコート今出川北 | 3LDK | 60.32 | 98,000 | 10000 | 無 / 1ヶ月 | 1.0 | 5/7 | Y | 1981/8 | RC | 無 | old | https://www.homes.co.jp/chintai/room/17266f6676927856654366176767c784f282a3da/ |
| 0.8 | 上神輿町貸家 | 7SLDK | 156.91 | 220,000 | 0 | 22万円 / 22万円 | 1.0 | None/3 | n | 1982/2 | 木造 | 空有 無料 | house | https://www.homes.co.jp/chintai/room/467a49ba251bff334ca268f15a407be2622baf73/ |
| 0.81 | 吉田近衛町19-6 | 2LDK | 48.0 | 120,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 2/2 | n | 1993/10 | 木造 | 無 | B | https://www.homes.co.jp/chintai/room/a51100c90e353d693478787d8da39e701b65fe2d/ |
| 0.84 |  | 2LDK | 45.08 | 100,000 | 0 | 10万円 / 20万円 | 2.0 | 2/2 | n | 1970/11 | 木造 | 近隣 18,000円(税無) 物件からの距離46 | house | https://www.homes.co.jp/chintai/room/b38723b6a8e9b62bbb41414831a776de8eff07d9/ |
| 0.86 | ドルフ聖護院 | 2LDK | 54.56 | 124,000 | 12000 | 無 / 5万円 | 0.4 | 1/3 | n | 2018/11 | RC | - | A | https://www.homes.co.jp/chintai/room/6c871728296ee170ac7bb434ba6666e9fd106e41/ |
| 0.86 | ＢＲＩＧＨ　ＳＴＯＮＥ御所北 | 2LDK | 52.01 | 174,000 | 10000 | 17.4万円 / 34.8万円 | 2.0 | 1/3 | Y | 2024/10 | RC | 無 | A | https://www.homes.co.jp/chintai/room/b4b7eea41c27a2b66ba671f355f9effe419594ce/ |
| 0.87 | 吉田近衛町8-6 貸家 | 4LDK | 92.3 | 150,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/2 | n | 1970/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/5ef1df6526b38132de68c3333d05b0db96aeba21/ |
| 0.87 |  | 5DK | 138.54 | 330,000 | 0 | 33万円 / 33万円 | 1.0 | None/2 | n | 1930/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/dcac9ba87acf47033c4b1b890cc2a5e8f5c50638/ |
| 0.88 | ルネ紫野 | 2LDK | 59.8 | 85,000 | 4000 | 5万円 / 10万円 | 1.18 | 2/2 | n | 2005/5 | 木造 | 空無 | A | https://www.homes.co.jp/chintai/room/6d74d357f9900144513b4837e306713a6cd1a6d3/ |
| 0.88 | ルネ紫野 | 2LDK | 55.0 | 85,000 | 4000 | 5万円 / 10万円 | 1.18 | 2/2 | n | 2005/5 | 木造 | 近隣 18,700円(税込) 物件からの距離39 | A | https://www.homes.co.jp/chintai/room/dba4662cd76a061445bc9d333f556d531f8bd83c/ |
| 0.88 | ルネ紫野 | 2LDK | 56.7 | 85,000 | 4000 | 5万円 / 10万円 | 1.18 | 2/2 | n | 2005/5 | 木造 | 無 | A | https://www.homes.co.jp/chintai/room/8444b06498c7550a5a2f71c36a38e08a944df3e4/ |
| 0.88 | ルネ紫野 | 2LDK | 59.8 | 85,000 | 4000 | 5万円 / 10万円 | 1.18 | 1/2 | n | 2005/4 | 木造 | 空有 15,000円(税無) | A | https://www.homes.co.jp/chintai/room/201c0de92aaa32479891b50cde3722ec17d204e3/ |
| 0.88 | リソシエ鴨川グランディス | 3LDK | 78.04 | 190,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 3/7 | Y | 2000/10 | RC | - | B | https://www.homes.co.jp/chintai/room/2c5343f1837e17704040684e41486b749b1be6b5/ |
| 0.89 | リーガル京都聖護院 | 2LDK | 66.0 | 163,000 | 14030 | 無 / 16.3万円 | 1.0 | 1/5 | Y | 2018/10 | RC | 空有 22,000円(税無) | A | https://www.homes.co.jp/chintai/room/9072913dfbcd4acb7a3868ea938b545ce6d39dd0/ |
| 0.89 | リーガル京都聖護院 | 2LDK | 66.0 | 168,000 | 14030 | 無 / 20万円 | 1.19 | 3/5 | Y | 2018/10 | RC | 空有 22,000円(税無) | A | https://www.homes.co.jp/chintai/room/d82cbe39c4e60118ec4c337e70fe2b8a76800745/ |
| 0.91 | 左京区吉田上大路町戸建 | 2LDK | 49.27 | 200,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/2 | n | 2025/10 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/f1438f2c3ebb91439ebcd62aa0de0c80a2e6c422/ |
| 0.91 |  | 3LDK | 94.92 | 230,000 | 0 | 23万円 / 46万円 | 2.0 | None/2 | n | 2016/2 | 木造 | 空有 無料 | house | https://www.homes.co.jp/chintai/room/c61e0e25000955cb70885ad388c24d5b15840872/ |
| 0.95 | 吉田中大路町アパート | 2LDK | 49.66 | 87,000 | 3000 | 無 / 無 | 0.0 | 1/2 | n | 2002/10 | 木造 | 無 | A | https://www.homes.co.jp/chintai/room/3b8c35c792fba3cb566463412d9e63b2e59dd256/ |
| 0.96 | プレージア京都聖護院ノ邸 | 3LDK | 73.75 | 210,000 | 20000 | 21万円 / 42万円 | 2.0 | 1/3 | Y | 2017/1 | RC | 無 | A | https://www.homes.co.jp/chintai/room/c8ff75e7705392727dff3fc3d2cc2b074d5c1555/ |
| 0.96 | 聖護院東町貸家 | 4SLDK | 145.0 | 230,000 | 0 | 30万円 / 40万円 | 1.74 | None/3 | n | 1992/3 | 鉄骨 | 空有 無料 | house | https://www.homes.co.jp/chintai/room/67717f7e726975f291080054bff4c58a19ff4d9c/ |
| 0.99 | ザ・京都レジデンス御所南 | 2LDK | 56.13 | 210,000 | 10000 | 21万円 / 21万円 | 1.0 | 2/5 | Y | 2016/12 | RC | 無 | A | https://www.homes.co.jp/chintai/room/da7ca321bd2d7177f60eb8ec716fb96a27aed303/ |
| 0.99 | 中京区毘沙門町貸家 | 6DK | 125.27 | 500,000 | 0 | 150万円 / 50万円 | 1.0 | None/1 | n | 1914/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/f62a7e673fb3e610bbc57a6ac244b43b88785f91/ |
| 1.01 |  | 2LDK | 60.23 | 128,000 | 7000 | 無 / 12.8万円 | 1.0 | 3/3 | n | 2011/3 | RC | 空有 19,800円(税込) 駐車料金：1980 | A | https://www.homes.co.jp/chintai/room/1fee00f494fc7e37f684e14e2a1be95e70f4c190/ |
| 1.01 |  | 2LDK | 64.5 | 140,000 | 10000 | 14万円 / 14万円 | 1.0 | 4/7 | Y | 1971/6 | RC | 無 | old | https://www.homes.co.jp/chintai/room/8c179a27cb2bfc118bea6a2d1412b1b0013845b0/ |
| 1.01 | ファインフラッツ京都神宮 | 2LDK | 54.25 | 185,000 | 15000 | 18.5万円 / 18.5万円 | 1.0 | 2/5 | Y | 2013/11 | RC | 無 | A | https://www.homes.co.jp/chintai/room/4f5b4291d400e8a4fd66c31238e0a965da9b6588/ |
| 1.01 |  | 8LDK | 93.19 | 220,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | None/2 | n | 1982/2 | 木造 | 近隣 15,000円(税無) 物件からの距離16 | house | https://www.homes.co.jp/chintai/room/f6b47224d534fc1ac6f9688f5c757ea35e986676/ |
| 1.01 | ザ・パークハウス京都聖護院 | 2LDK | 58.45 | 250,000 | 0 | 25万円 / 50万円 | 2.0 | 1/5 | Y | 2026/8 | RC | 無 | A | https://www.homes.co.jp/chintai/room/db82d4c6e86f27e79d449870082131f4f7619902/ |
| 1.03 |  | 5LDK | 153.83 | 250,000 | 0 | 2ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1990/6 | 木造 | 空有 (2台) 無料 | house | https://www.homes.co.jp/chintai/room/914a3fa850bda7aa3d458d44cb81ce376a6118d2/ |
| 1.03 | サンシティ御所南 | 3LDK | 89.44 | 260,000 | 10000 | 26万円 / 52万円 | 2.0 | 3/3 | Y | 2006/3 | RC | 空有 33,000円(税込) | A | https://www.homes.co.jp/chintai/room/f02a0f6c99f1f0a8464fe33dfcd05ec64936002e/ |
| 1.04 | ＫＢ．メゾンロータス | 2LDK | 51.17 | 121,000 | 4600 | 無 / 12.1万円 | 1.0 | 1/3 | n | 2011/3 | 鉄骨 | 無 | A | https://www.homes.co.jp/chintai/room/a044bf99f2e6a495e2536a6678a700113b6f7b21/ |
| 1.06 |  | 3DK | 69.35 | 90,000 | 0 | 9万円 / 9万円 | 1.0 | 1/1 | n | 2001/8 | 木造 | 近隣 16,000円(税無) 物件からの距離23 | house | https://www.homes.co.jp/chintai/room/43f92b3dc4a294aaa7037c66bbd2e673c8288448/ |
| 1.07 | ＣＡＬＭ河原町二条 | 2LDK | 61.12 | 195,000 | 10000 | 19.5万円 / 19.5万円 | 1.0 | 2/7 | Y | 2026/3 | RC | 無 | A | https://www.homes.co.jp/chintai/room/103dae9105774d7183097532e2617fe335591b4f/ |
| 1.07 | ＣＡＬＭ河原町二条 | 2LDK | 61.12 | 198,000 | 10000 | 19.8万円 / 19.8万円 | 1.0 | 5/7 | Y | 2026/3 | RC | 無 | A | https://www.homes.co.jp/chintai/room/7344c511792879b75451da7f4c0185ba83011ad3/ |
| 1.07 | ＣＡＬＭ河原町二条 | 2LDK | 61.12 | 198,000 | 10000 | 19.8万円 / 19.8万円 | 1.0 | 4/7 | Y | 2026/3 | RC | 無 | A | https://www.homes.co.jp/chintai/room/0701c57c6b33e53a089c775e098cfe754b6e2b9f/ |
| 1.09 | イスターナイマイ鴨川西 | 2LDK | 50.65 | 150,000 | 9000 | 無 / 20万円 | 1.33 | 3/5 | Y | 2013/2 | RC | 近隣 46,095円(税込) 物件からの距離20 | A | https://www.homes.co.jp/chintai/room/b6bd667f9762c5a486887ad58ec82aa91579bc0f/ |
| 1.09 | イスターナイマイ鴨川西 | 2LDK | 50.65 | 153,000 | 9000 | 無 / 20万円 | 1.31 | 5/5 | Y | 2013/2 | RC | 近隣 46,095円(税込) 物件からの距離20 | A | https://www.homes.co.jp/chintai/room/0d49c8e7016aa3abbb449ca868eb9cddfa2ee4c6/ |
| 1.09 | 中京区寺町通　貸戸建 | 4LDK | 132.36 | 220,000 | 0 | 22万円 / 22万円 | 1.0 | None/2 | n | 1927/1 | 木造 | 空無 | house | https://www.homes.co.jp/chintai/room/c6a6ea7a9ccd21a1455cf50293d090554789cd80/ |
| 1.12 | グランタック東山二条 | 2LDK | 56.0 | 130,000 | 8000 | 1ヶ月 / 無 | 0.0 | 5/6 | Y | 1977/1 | RC | 近隣 20,000円(税込) 物件からの距離15 | old | https://www.homes.co.jp/chintai/room/2eccf9d168dd113af079efcb982b22f832a00e6f/ |
| 1.14 | エルミタージュ下鴨東 | 2LDK | 55.43 | 129,000 | 8500 | 無 / 1ヶ月 | 1.0 | 2/2 | n | 2024/7 | 軽量鉄骨 | 無 | A | https://www.homes.co.jp/chintai/room/2b159fd4d7b4ef9cc309a701dbbd1a304c494fcd/ |
| 1.17 | フォルム聖護院別邸 | 3LDK | 72.57 | 168,000 | 12000 | 無 / 20万円 | 1.19 | 3/5 | Y | 2001/6 | RC | 近隣 16,000円(税無) 物件からの距離41 | A | https://www.homes.co.jp/chintai/room/649a56071e032c90ec59d2850de9ec352ce85f6a/ |
| 1.21 |  | 6DK | 145.36 | 150,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | None/4 | n | 1976/8 | 鉄骨 | 近隣 16,500円(税込) 物件からの距離40 | house | https://www.homes.co.jp/chintai/room/9da7bb9bc72a5a7d314886e0dec6e9d7286ec2a0/ |
| 1.21 | ベルリード　Ｍｉｌｌｅｓｉｍｅ寺町 | 2LDK | 69.97 | 230,000 | 10000 | 23万円 / 23万円 | 1.0 | 2/3 | n | 2026/11 | 木造 | 無 | A | https://www.homes.co.jp/chintai/room/b36285f013942406f29492c75fbce62d0b9e3436/ |
| 1.22 | 北白川追分町貸家 | 5DK | 63.66 | 88,000 | 0 | 1ヶ月 / 10万円 | 1.14 | 1/2 | ? | 1988/8 | 木造 | - | house | https://www.homes.co.jp/chintai/room/cc782e59d6412951da4bb7279386dc52bc5ebbfc/ |
| 1.23 | グレーシー北白川 | 3LDK | 68.39 | 130,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 3/3 | n | 1991/8 | RC | 空有 20,000円(税込) | B | https://www.homes.co.jp/chintai/room/ec27a4bcb25d02ce204bc3f6593a9d3f268aea6c/ |
| 1.25 | メゾンフジ | 3DK | 80.0 | 135,000 | 5000 | 無 / 無 | 0.0 | 2/5 | n | 1985/10 | 鉄骨 | 無 | old | https://www.homes.co.jp/chintai/room/a6cd9e39d774787814593c7c3e0551d786aecba9/ |
| 1.26 | コーポ富有 | 2LDK | 48.51 | 100,000 | 9000 | 10万円 / 10万円 | 1.0 | 2/4 | Y | 1985/7 | RC | 無 | old | https://www.homes.co.jp/chintai/room/a0afe803db5f1e62606faf05e19b1ea1209a52f6/ |
| 1.26 | アルカンシェル御所 | 2LDK | 57.17 | 144,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/6 | Y | 1987/3 | RC | 近隣 25,000円(税無) 物件からの距離37 | old | https://www.homes.co.jp/chintai/room/591ea60ca1385f2bb7b0108625edabdda84d9a59/ |
| 1.26 | ベルフォーレ御所南 | 2LDK | 60.04 | 198,000 | 12000 | 無 / 2ヶ月 | 2.0 | 3/3 | Y | 2023/10 | RC | 近隣 25,000円(税無) 物件からの距離41 | A | https://www.homes.co.jp/chintai/room/31a5c827f29a12437c7877c8957dc9e4d86677dc/ |
| 1.27 |  | 3LDK | 66.97 | 125,000 | 10000 | 無 / 12.5万円 | 1.0 | 5/5 | Y | 1999/11 | RC | 空有 23,100円(税込) | B | https://www.homes.co.jp/chintai/room/a61ee712a4e3adfb87afee88f359a8cda2a51b7d/ |
| 1.27 | 布袋屋町496-5貸家 | 2LDK | 73.82 | 210,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | None/2 | n | 1970/5 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/29c0ec48e7c06c81963a568129ca4df3156cb845/ |
| 1.3 | クラッシィハウス京都御苑ザ・テラス | 2LDK | 58.01 | 210,000 | 10000 | 1ヶ月 / 2ヶ月 | 2.0 | 1/5 | Y | 2026/5 | RC | 近隣 25,000円(税無) 物件からの距離22 | A | https://www.homes.co.jp/chintai/room/c7e95d097eea241ffa8605b058d79d0343612b5b/ |
| 1.31 | フロンテージ堺町御門 | 2LDK | 68.44 | 225,000 | 9000 | 5万円 / 45万円 | 2.0 | 2/3 | Y | 2023/3 | 鉄骨 | 無 | A | https://www.homes.co.jp/chintai/room/a44d5367ad8adc58f3cc7d4de8c2678475142b36/ |
| 1.31 |  | 3LDK | 86.14 | 225,000 | 20000 | 無 / 30万円 | 1.33 | 5/6 | Y | 1989/9 | RC | 空有 33,000円(税込) | old | https://www.homes.co.jp/chintai/room/874e4e7c197a6a58865636ba713f5a5ca01fabe5/ |
| 1.32 | エルザ京都御所西 | 3LDK | 126.72 | 245,000 | 0 | 2ヶ月 / 2ヶ月 | 2.0 | 5/6 | Y | 1989/8 | RC | 空有 25,000円(税無) | old | https://www.homes.co.jp/chintai/room/d9cffa0fb709f423ccd752986926b8f25cf3824a/ |
| 1.33 | 岡崎最勝寺町貸家 | 6DK | 118.57 | 228,000 | 0 | 22.8万円 / 25.08万円 | 1.1 | None/2 | n | 1914/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/3e912eb50d8798ff79b9b92dbbaca3ab7aa2f7e6/ |
| 1.34 | パークホームズ堺町御門 | 3LDK | 74.32 | 261,000 | 20000 | 28.1万円 / 56.2万円 | 2.15 | 4/5 | Y | 2014/10 | RC | 空有 37,800円(税込) | A | https://www.homes.co.jp/chintai/room/b1f77cf1fa828f2ce17c069cb9b0f6f9f50c6b40/ |
| 1.35 |  | 3DK | 54.0 | 100,000 | 0 | 10万円 / 10万円 | 1.0 | 1/4 | n | 1979/7 | RC | 近隣 (1台) 25,000円 物件からの距離4 | old | https://www.homes.co.jp/chintai/room/408270dfe50222d9ff3f6a1e2890d42ee36955bd/ |
| 1.35 | 乾ハイツ | 3DK | 54.0 | 100,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/4 | n | 1974/7 | RC | 近隣 (1台) 25,000円 物件からの距離2 | old | https://www.homes.co.jp/chintai/room/8d86946117deb4a55c569e92cc561f660f59af11/ |
| 1.35 | ルミエール下鴨 | 2SLDK | 70.54 | 156,000 | 4600 | 無 / 15.6万円 | 1.0 | 2/2 | n | 2014/6 | 木造 | 空無 | A | https://www.homes.co.jp/chintai/room/d5a23c7970bb19312ae127776c47297cb1a4e270/ |
| 1.35 | T’Sスクエア下鴨 | 3LDK | 63.85 | 183,000 | 8500 | 無 / 無 | 0.0 | 1/2 | n | 2021/3 | 軽量鉄骨 | 空有 19,800円(税込) | A | https://www.homes.co.jp/chintai/room/40407a3edf4a25e2a55c5b84571b1d67e784c4c5/ |
| 1.35 | Ｔ‘ｓスクエア下鴨 | 3LDK | 64.98 | 183,000 | 8500 | 無 / 無 | 0.0 | 1/2 | n | 2021/3 | 軽量鉄骨 | 空有 (1台) 18,000円 物件からの距離0 | A | https://www.homes.co.jp/chintai/room/2d0bb2f1c9cdbf9845a8d17974ad274d0b4bac4c/ |
| 1.36 |  | 2LDK | 58.88 | 141,000 | 13000 | 無 / 20万円 | 1.42 | 2/5 | Y | 2007/11 | RC | 空無 | A | https://www.homes.co.jp/chintai/room/2d13a532df2d1bbb577ae278773e6eed1ef1f0ee/ |
| 1.36 |  | 2LDK | 58.88 | 150,000 | 15000 | 無 / 20万円 | 1.33 | 3/5 | Y | 2007/11 | RC | 空無 | A | https://www.homes.co.jp/chintai/room/09329373b2db33cb5a3957702475060d3bfda850/ |
| 1.36 | くわでん | 3LDK | 77.02 | 250,000 | 13000 | 無 / 25万円 | 1.0 | 2/2 | n | 2012/9 | 鉄骨 | 空無 | A | https://www.homes.co.jp/chintai/room/0c995460e0064ffec29400b982d96de23950d4bc/ |
| 1.36 | パーシモン御所南 | 3LDK | 110.12 | 435,000 | 10000 | 43.5万円 / 87万円 | 2.0 | 2/5 | Y | 2024/4 | RC | 近隣 33,000円(税込) 物件からの距離48 | A | https://www.homes.co.jp/chintai/room/d67663fcacb38f1c7795cc77dc266ab1908aaf90/ |
| 1.37 | プラザ晴明館 | 3DK | 56.0 | 150,000 | 0 | 15万円 / 15万円 | 1.0 | 5/5 | Y | 1989/5 | 鉄骨 | 無 | old | https://www.homes.co.jp/chintai/room/2f8a67de91b3763a9d4e09d1d7ac9f3233a5cf43/ |
| 1.37 | プラザ晴明館 | 3DK | 46.0 | 155,000 | 0 | 15.5万円 / 15.5万円 | 1.0 | 5/5 | Y | 1989/4 | その他 | 無 | old | https://www.homes.co.jp/chintai/room/cda6d1af217aa2a8c323acee19888495b007d53a/ |
| 1.37 | プラザ晴明館 | 3LDK | 85.0 | 178,000 | 0 | 17.8万円 / 17.8万円 | 1.0 | 5/5 | Y | 1989/5 | 鉄骨 | 無 | old | https://www.homes.co.jp/chintai/room/50ec5b7f32317e7a0bdb2be39763fefbf5a8d877/ |
| 1.37 | プラザ晴明館 | 3LDK | 66.0 | 178,000 | 0 | 17.8万円 / 17.8万円 | 1.0 | 5/5 | Y | 1989/5 | 鉄骨 | 無 | old | https://www.homes.co.jp/chintai/room/00de048b9323332c6286d739ff2df922c746abaf/ |
| 1.37 | エリシア　御所南 | 2LDK | 68.7 | 260,000 | 15000 | 5万円 / 60万円 | 2.31 | 1/4 | Y | 2027/1 | 鉄骨 | 空無 | A | https://www.homes.co.jp/chintai/room/91174b825999ce41a274cd85019529c0c65bd1d2/ |
| 1.37 | エリシア　御所南 | 2LDK | 67.84 | 285,000 | 15000 | 5万円 / 60万円 | 2.11 | 2/4 | Y | 2027/1 | 鉄骨 | 空無 | A | https://www.homes.co.jp/chintai/room/c6d7fad2119e4fdc3c81d840f55e9fca952448fe/ |
| 1.38 | 下鴨泉川町貸家 | 4DK | 66.78 | 92,000 | 0 | 9.2万円 / 9.2万円 | 1.0 | None/2 | n | 1972/3 | 木造 | 空無 | house | https://www.homes.co.jp/chintai/room/59f26cfe147858501adbb8b4476514734eb8d095/ |
| 1.38 |  | 2LDK | 97.23 | 160,000 | 0 | 無 / 無 | 0.0 | 1/2 | n | 1995/2 | 鉄骨 | 近隣 13,200円(税込) 物件からの距離48 | house | https://www.homes.co.jp/chintai/room/58bca1097ed85a4a5b47859ef287b65e27085f8d/ |
| 1.38 | グラン・シティオ下鴨四季彩館406号室 | 4LDK | 116.0 | 280,000 | 0 | 28万円 / 28万円 | 1.0 | 4/5 | Y | 2002/4 | RC | 無 | A | https://www.homes.co.jp/chintai/room/ba533874e0a3cc2e5ae964e1c4ec2ff8071f3cf4/ |
| 1.38 | アステシオ清和院 | 3LDK | 117.56 | 380,000 | 0 | 76万円 / 無 | 0.0 | 1/3 | Y | 1988/4 | RC | 無 | old | https://www.homes.co.jp/chintai/room/2f39c3967a9ffcdc8b0a4fa6f928a20a1287c505/ |
| 1.38 | アステシオ清和院 | 3LDK | 143.58 | 450,000 | 0 | 90万円 / 無 | 0.0 | 3/3 | Y | 1988/4 | RC | 無 | old | https://www.homes.co.jp/chintai/room/6c4b70b4616f6401807ca1df2afe1dd6ea3ad252/ |
| 1.39 | エスポワール麩屋町 | 2LDK | 46.59 | 114,000 | 10000 | 20万円 / 35万円 | 3.07 | 5/5 | Y | 2009/3 | RC | 無 | A | https://www.homes.co.jp/chintai/room/f6ab4f43236cfd9599c4f3de01f47a9471a08f38/ |
| 1.39 | 二条麩屋町ビューハイツ | 3SLDK | 72.8 | 140,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 6/9 | Y | 1981/10 | SRC | - | old | https://www.homes.co.jp/chintai/room/45184da6c8de9ebf58049be02ecf4c129d8a9c73/ |
| 1.39 |  | 3LDK | 72.69 | 140,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 6/9 | Y | 1981/10 | SRC | 空無 月額30,000〜35,000円 | old | https://www.homes.co.jp/chintai/room/2d936588982eca6873c85044af5736c41b74434d/ |
| 1.39 | ラ・サール御所 | 4LDK | 76.23 | 150,000 | 15000 | 無 / 1ヶ月 | 1.0 | 3/3 | Y | 1988/10 | RC | 空無 敷地内駐車場完備。 | old | https://www.homes.co.jp/chintai/room/82ef96a9cd810e11cbe8db90e7547bc1d905e45e/ |
| 1.39 | グリシーヌ御所西I | 3LDK | 78.38 | 209,000 | 6000 | 3万円 / 35万円 | 1.67 | 2/3 | n | 2021/10 | 鉄骨 | 空有 契約必須 33,000円(税込) | A | https://www.homes.co.jp/chintai/b-37231760000278/ |
| 1.39 | グラン・リソシエ京都御苑 | 2LDK | 61.78 | 210,000 | 10000 | 無 / 21万円 | 1.0 | 2/5 | Y | 2013/2 | RC | 空有 21,000円(税無) | A | https://www.homes.co.jp/chintai/room/f026222cdd8cb86dea6f4cfde13cb791976315af/ |
| 1.39 | グラン・リソシエ京都御苑 | 2SLDK | 63.44 | 230,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 4/5 | Y | 2013/2 | RC | 無 | A | https://www.homes.co.jp/chintai/room/66ca3b27161ecf1b8d7ed45843ed7757f9b1f9ae/ |
| 1.42 |  | 6LDK | 142.55 | 180,000 | 0 | 無 / 1ヶ月 | 1.0 | 2/3 | n | 1991/9 | 木造 | 近隣 27,500円(税込) 物件からの距離41 | house | https://www.homes.co.jp/chintai/room/2f9c23b2b66ba7205bd294a3bfe4d6773e03b355/ |
| 1.44 | ｓａｗａｒａｂｉ御所 | 2LDK | 75.07 | 174,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/5 | Y | 2006/3 | RC | 近隣 22,000円(税込) 物件からの距離46 | A | https://www.homes.co.jp/chintai/room/92bedb130b1f6032a996630ed8996842ec9e26ac/ |
| 1.44 | ｓａｗａｒａｂｉ御所 | 2LDK | 72.98 | 174,000 | 10000 | 17.4万円 / 17.4万円 | 1.0 | 3/5 | Y | 2006/3 | RC | 空無 | A | https://www.homes.co.jp/chintai/room/de3f1c0494c6761f2ec4f659708eaf5e04ec7ca9/ |
| 1.44 | ｓａｗａｒａｂｉ御所 | 2LDK | 75.16 | 175,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 4/5 | Y | 2006/3 | RC | 近隣 22,000円(税込) 物件からの距離46 | A | https://www.homes.co.jp/chintai/room/7f507eda2722bf96d0e3eda268ca34e9e9ee73f7/ |
| 1.44 | ｓａｗａｒａｂｉ御所 | 2LDK | 75.14 | 175,000 | 10000 | 17.5万円 / 17.5万円 | 1.0 | 4/5 | Y | 2006/3 | RC | 空無 | A | https://www.homes.co.jp/chintai/room/9355f387d54ff7dadb0166ee92f1005a2c19a095/ |
| 1.46 | 北白川コーポラス | 3LDK | 66.0 | 100,000 | 8000 | 10万円 / 10万円 | 1.0 | 3/5 | n | 1988/3 | RC | 空有 8,000円(税込) | old | https://www.homes.co.jp/chintai/room/22e8555d87048862dd31c37876b8d0c35a12fc8e/ |
| 1.46 | 北白川コーポラス | 3DK | 57.0 | 100,000 | 8000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/4 | n | 1970/10 | RC | 空有 8,000円(税無) | old | https://www.homes.co.jp/chintai/room/df352b6f59b3c869783f59d701e53b9c6d1dbfc8/ |
| 1.47 | パラドール御所 | 3LDK | 63.18 | 130,000 | 15000 | 1ヶ月 / 2ヶ月 | 2.0 | 5/7 | Y | 1984/3 | RC | 空有 (1台) 22,000円(税込) | old | https://www.homes.co.jp/chintai/room/2c15620f6f5a7e0ac135ee962ac5b9228e275af4/ |
| 1.47 | ヴィークコート京都河原町二条 | 3LDK | 75.13 | 380,000 | 0 | 38万円 / 76万円 | 2.0 | 7/7 | Y | 2023/8 | RC | 無 | A | https://www.homes.co.jp/chintai/room/7fcda45b51c290f90224b79d225a4b7bf5e2e648/ |
| 1.48 | 黒谷町303 | 2LDK | 98.36 | 150,000 | 0 | 15万円 / 30万円 | 2.0 | 3/4 | n | 1987/9 | 鉄骨 | 無 | old | https://www.homes.co.jp/chintai/room/f29e4d94ea74a7ca5aaf34f112ea2c65b639f761/ |
| 1.49 | グレーシー高野 | 3DK | 47.8 | 79,000 | 4000 | 無 / 7.9万円 | 1.0 | 3/5 | n | 1979/3 | RC | 空有 11,000円(税込) 駐車料金：1100 | old | https://www.homes.co.jp/chintai/room/1e5f695a4dddcc68ccbc1fd6a9476afe6d40d297/ |
| 1.49 | グレーシー高野 | 3DK | 49.0 | 79,000 | 4000 | 無 / 7.9万円 | 1.0 | 3/5 | n | 1972/4 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/b9eed297e24e608885fbd25323eff6f099a47686/ |
| 1.49 | グレーシー高野 | 3DK | 51.0 | 79,000 | 4000 | 無 / 1ヶ月 | 1.0 | 3/5 | n | 1972/1 | RC | 空有 16,500円(税込) | old | https://www.homes.co.jp/chintai/room/57a2221b4ff715aad614adb91d41be3ab08dc13e/ |
| 1.5 | エスポワール丸太町 | 2SLDK | 83.41 | 210,000 | 8000 | 9万円 / 42万円 | 2.0 | 2/3 | n | 2015/1 | その他 | 空無 | A | https://www.homes.co.jp/chintai/room/94801eaa3185abae1fc2a0b916870f271ac34bc0/ |
| 1.5 | ヴィークコート京都河原町二条 | 3LDK | 88.21 | 430,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 3/7 | Y | 2023/8 | RC | 無 | A | https://www.homes.co.jp/chintai/room/20be7d7c3e336e13a09b3cf62e34c6874f30bb48/ |
| 1.5 | パラドール御所西グランデ | 3LDK | 72.3 | 240,000 | 20000 | 1ヶ月 / 2ヶ月 | 2.0 | 2/5 | Y | 2024/2 | RC | 近隣 25,000円(税込) 物件からの距離15 | A | https://www.homes.co.jp/chintai/room/df63b0b9df4b69fdd07eeae5913f1a54fc53ae27/ |
| 1.5 | パラドール御所西グランデ | 2LDK | 66.31 | 250,000 | 0 | 無 / 2ヶ月 | 2.0 | 3/5 | Y | 2024/2 | RC | 空有 (1台) 22,000円 物件からの距離0 | A | https://www.homes.co.jp/chintai/room/9d4f8052b5f9488f9ed162a86bec7f2ac74e930a/ |
| 1.5 | パラドール御所西グランデ | 3LDK | 72.2 | 270,000 | 0 | 無 / 2.5ヶ月 | 2.5 | 1/5 | Y | 2024/2 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/11bc74251848a5c295d25c01538ff8683b03d9ed/ |
