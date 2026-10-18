# homes — LIFULL HOME'S (homes.co.jp), WALK3 survey (≤3.0 km of 京都技術科学センター, 左京区吉田河原町14; rent ≤140,000), fetched 2026-10-18

## Method
- Ward list URL https://www.homes.co.jp/chintai/kyoto/<ward>/list/ with server-side cond: 賃料≤14万 (管理費別), 専有面積≥45㎡, 2LDK/3DK/3LDK/4DK/4LDK以上 (no age / structure condition), sort 築年数が新しい順. Wards kyoto_kita / kamigyo / sakyo / nakagyo / higashiyama / shimogyo-city; site unit totals {'all_kyoto_kita-city': 475, 'all_kyoto_kamigyo-city': 557, 'all_kyoto_sakyo-city': 884, 'all_kyoto_nakagyo-city': 353, 'all_kyoto_higashiyama-city': 108, 'all_kyoto_shimogyo-city': 238}; 46 list pages (raw: out/raw/homes/listall_*).
- **Fetching (AWS WAF)**: python never requested HOME'S. Every list and unit page was loaded by headless Chromium (`homes_fetch.js`: HTML document only, 10–14 s between pages, fresh browser context every 9 pages with a 45 s pause, MAX_CAPTCHA=1 = stop at the first CAPTCHA). Browser runs this survey: 3 (unit pages already fetched in the walk survey a few hours earlier, ≤1.5 km, were reused from ../walk/out/raw/homes/); pages ok 375, failed 0, CAPTCHAs 0, contexts 43, unfetched 0. No CAPTCHA was solved or bypassed.
- Funnel: list_units 2659, pr_units 92, drop_layout_list 17, drop_area_list 0, dup_same_unit 1477, drop_station_bound_list 356, geocode_inconsistent_list 32, drop_far_list 249, geocode_fail_list 0, detail_fetched 375, detail_http_fail 0, drop_far 5, dup_same_unit_detail 21, kept 349. Same unit listed by several agencies merged (cheapest kept; other URLs in notes).
- Distance: Kyoto 通り名 addresses reduced to ward+町名 (kgeo.py) and geocoded with GSI (mostly 町名 level, ±300 m → kept up to 3.2 km, flagged); every position checked against the listing's 駅徒歩N分 (≤ N×80 m from that station) — impossible ones dropped already at list stage, contradicting geocodes replaced by the station position (geofix.py).
- `elevator=false` means the unit page's 設備 list exists but has no エレベーター; null if no list. Nameless buildings (HOME'S shows the access text) have building_name null. `http_status` = status of the unit page as loaded by the browser.
- Station plausibility check (geofix.py; Kyoto town names repeat, GSI returns one): {'checked': 347, 'no_station': 2, 'inconsistent_moved': 6, 'dropped_lower_bound': 4, 'roughly_consistent_kept': 7}; dropped (cannot be ≤3.0 km given the listed 駅徒歩): 4 → out/homes_geodropped.json.

## Result
- **Kept 328 units** (after merging 17 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via the same building name in another listing with a full address, 0 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 27; rent range kept: 70000–140000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'B': 64, 'house': 63, 'old': 137, 'A': 64}; 礼金 ≤1ヶ月 204, >1ヶ月 123, unknown 1 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'town': 304, 'station': 6, 'address (GSI)': 18} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 165/160/3; by ward: {'左京区': 110, '上京区': 123, '中京区': 50, '北区': 17, '東山区': 9, '下京区': 19}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/homes/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.03 | エーデルハイム鴨川 | 3LDK | 65.77 | 138,000 | 10000 | 20万円 / 35万円 | 2.54 | 5/5 | Y | 1997/2 | RC | 空有 21,000円(税込) | B | https://www.homes.co.jp/chintai/room/cc25937737dd6f34fdefc0cda60a87bc8926d5c0/ |
| 0.21 |  | 2LDK | 66.7 | 120,000 | 0 | 無 / 24万円 | 2.0 | None/2 | n | 2004/12 | 木造 | 近隣 18,000円(税無) 物件からの距離23 | house | https://www.homes.co.jp/chintai/room/98c957bdc4b189e5652bbc8fbb45541cb562be06/ |
| 0.25 |  | 3DK | 54.67 | 100,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/2 | n | 1984/11 | 木造 | 近隣 18,000円(税無) 物件からの距離44 | house | https://www.homes.co.jp/chintai/room/bb200d5bb411a04e8184c60230571419ddcdd2a7/ |
| 0.25 | 今智庵 | 3DK | 65.0 | 100,000 | 0 | 10万円 / 20万円 | 2.0 | None/2 | n | 1984/11 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/1711de0f3af54f3af03c132ae218970a90ee2255/ |
| 0.27 | 上阿達谷口マンション | 2LDK | 46.12 | 110,000 | 6000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/4 | n | 1989/5 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/eda163bbff370e625d2daeb44e267a9c3f2755d3/ |
| 0.27 | 上阿達谷口マンション | 3DK | 45.7 | 110,000 | 6000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/4 | n | 1989/4 | RC | 近隣 18,000円(税無) 物件からの距離42 | old | https://www.homes.co.jp/chintai/room/f67d611ff87eff46a47d5ff4b9ef1e7d060b12c0/ |
| 0.6 | グランレブリー御所東II | 2LDK | 53.94 | 136,000 | 10000 | 無 / 1ヶ月 | 1.0 | 1/3 | n | 1987/2 | RC | 近隣 22,000円(税込) 物件からの距離33 | old | https://www.homes.co.jp/chintai/room/401b4f5a46941434e128d78099ecebc9ea59dc1c/ |
| 0.6 | グランレブリー御所東II | 2LDK | 53.94 | 138,000 | 10000 | 無 / 1ヶ月 | 1.0 | 2/3 | n | 1987/2 | RC | 近隣 22,000円(税込) 物件からの距離33 | old | https://www.homes.co.jp/chintai/room/f32cd061205e2612214317f13af33ee75f2837a4/ |
| 0.63 | グランレブリー御所東II | 2LDK | 53.94 | 136,000 | 10000 | 無 / 13.6万円 | 1.0 | 1/3 | n | 1987/3 | RC | 空無 | old | https://www.homes.co.jp/chintai/b-13670308848/ |
| 0.63 | グランレブリー御所東II | 2LDK | 53.94 | 138,000 | 10000 | 無 / 13.8万円 | 1.0 | 2/3 | n | 1987/3 | RC | 空無 | old | https://www.homes.co.jp/chintai/b-13670322765/ |
| 0.7 | シャルト北苑 | 4LDK | 69.03 | 130,000 | 10000 | 2ヶ月 / 1ヶ月 | 1.0 | 3/3 | n | 1984/1 | RC | 近隣 15,000円(税無) 物件からの距離28 | old | https://www.homes.co.jp/chintai/room/5ef38a8acc5899f0af03b40f868ee632baf0004e/ |
| 0.7 | シャルト北苑 | 3LDK | 71.72 | 140,000 | 10000 | 2ヶ月 / 1ヶ月 | 1.0 | 2/3 | n | 1984/1 | RC | 近隣 15,000円(税無) 物件からの距離28 | old | https://www.homes.co.jp/chintai/room/a0262d25044a8dd280a67ce88981a800c6dec019/ |
| 0.7 | シャルト北苑 | 3LDK | 69.03 | 140,000 | 10000 | 2ヶ月 / 1ヶ月 | 1.0 | 1/3 | n | 1984/1 | RC | 近隣 15,000円(税無) 物件からの距離28 | old | https://www.homes.co.jp/chintai/room/d1e3d227e4c1897e511dfed126569cd90afa9eb6/ |
| 0.71 |  | 3SLDK | 90.0 | 135,000 | 0 | 無 / 27万円 | 2.0 | None/2 | n | 1965/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/ce0dc691f55f153e66f61db0b7254dd9b221d330/ |
| 0.71 |  | 3LDK | 90.0 | 135,000 | 0 | 無 / 1ヶ月 | 1.0 | 2/2 | n | 1950/5 | 木造 | 近隣 20,000円(税込) 物件からの距離30 | house | https://www.homes.co.jp/chintai/room/617cc9de45f8d2dc5a0eda9fe5df51c142f884b1/ |
| 0.71 | 東丸太町貸家 | 3SLDK | 90.0 | 135,000 | 0 | 無 / 13.5万円 | 1.0 | None/2 | n | 1950/5 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/2783e5b6657c7efef8c19a9eb304062b9d7c9d7e/ |
| 0.74 |  | 4LDK | 65.71 | 135,000 | 0 | 無 / 無 | 0.0 | 1/2 | n | 1994/4 | 木造 | 近隣 15,000円(税無) 物件からの距離41 | house | https://www.homes.co.jp/chintai/room/f713330d165da124cca63de98480e2802bd07d0c/ |
| 0.75 | サンアートビル | 3LDK | 80.4 | 130,000 | 8000 | 無 / 無 | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 | 近隣 30,000円(税込) 物件からの距離14 | old | https://www.homes.co.jp/chintai/room/f51515f1fec7e78d08f282e73d65bd45782a06ce/ |
| 0.75 | サンアートビル | 3LDK | 59.41 | 130,000 | 8000 | 無 / 無 | 0.0 | 5/6 | Y | 1981/12 | RC | 無 | old | https://www.homes.co.jp/chintai/room/3324aee3c94e5e6b398f792595933820b2bcd1e1/ |
| 0.75 | サンアートビル | 3DK | 59.14 | 130,000 | 8000 | 無 / 無 | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 | 無 | old | https://www.homes.co.jp/chintai/room/5346e66824a3b5c13c14da724aaa9ebd0bd5fdde/ |
| 0.81 | 吉田近衛町19-6 | 2LDK | 48.0 | 120,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 2/2 | n | 1993/10 | 木造 | 無 | B | https://www.homes.co.jp/chintai/room/a51100c90e353d693478787d8da39e701b65fe2d/ |
| 0.84 |  | 2LDK | 45.08 | 100,000 | 0 | 10万円 / 20万円 | 2.0 | 2/2 | n | 1970/11 | 木造 | 近隣 18,000円(税無) 物件からの距離46 | house | https://www.homes.co.jp/chintai/room/b38723b6a8e9b62bbb41414831a776de8eff07d9/ |
| 0.86 | ドルフ聖護院 | 2LDK | 54.56 | 124,000 | 12000 | 無 / 5万円 | 0.4 | 1/3 | n | 2018/11 | RC | - | A | https://www.homes.co.jp/chintai/room/6c871728296ee170ac7bb434ba6666e9fd106e41/ |
| 0.88 | ルネ紫野 | 2LDK | 59.8 | 85,000 | 4000 | 5万円 / 10万円 | 1.18 | 2/2 | n | 2005/5 | 木造 | 空無 | A | https://www.homes.co.jp/chintai/room/6d74d357f9900144513b4837e306713a6cd1a6d3/ |
| 0.88 | ルネ紫野 | 2LDK | 55.0 | 85,000 | 4000 | 5万円 / 10万円 | 1.18 | 2/2 | n | 2005/5 | 木造 | 近隣 18,700円(税込) 物件からの距離39 | A | https://www.homes.co.jp/chintai/room/3a224a095a4c7039159d6c9bd7efcb85395632ac/ |
| 0.88 | ルネ紫野 | 2LDK | 56.7 | 85,000 | 4000 | 5万円 / 10万円 | 1.18 | 2/2 | n | 2005/5 | 木造 | 無 | A | https://www.homes.co.jp/chintai/room/8444b06498c7550a5a2f71c36a38e08a944df3e4/ |
| 0.95 | 吉田中大路町アパート | 2LDK | 49.66 | 87,000 | 3000 | 無 / 無 | 0.0 | 1/2 | n | 2002/10 | 木造 | 無 | A | https://www.homes.co.jp/chintai/room/3b8c35c792fba3cb566463412d9e63b2e59dd256/ |
| 1.01 | かぐら坂荘 | 2LDK | 60.23 | 128,000 | 7000 | 無 / 12.8万円 | 1.0 | 3/3 | n | 2011/3 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/e91096ca0260afee0163fe77cac8fc6a1f9c3f1d/ |
| 1.01 |  | 2LDK | 64.5 | 140,000 | 10000 | 14万円 / 14万円 | 1.0 | 4/7 | Y | 1971/6 | RC | 無 | old | https://www.homes.co.jp/chintai/room/8c179a27cb2bfc118bea6a2d1412b1b0013845b0/ |
| 1.04 | ＫＢ．メゾンロータス | 2LDK | 51.17 | 121,000 | 4600 | 無 / 12.1万円 | 1.0 | 1/3 | n | 2011/3 | 鉄骨 | 無 | A | https://www.homes.co.jp/chintai/room/a044bf99f2e6a495e2536a6678a700113b6f7b21/ |
| 1.06 |  | 3DK | 69.35 | 90,000 | 0 | 9万円 / 9万円 | 1.0 | 1/1 | n | 2001/8 | 木造 | 近隣 16,000円(税無) 物件からの距離23 | house | https://www.homes.co.jp/chintai/room/43f92b3dc4a294aaa7037c66bbd2e673c8288448/ |
| 1.12 | グランタック東山二条 | 2LDK | 56.0 | 130,000 | 8000 | 1ヶ月 / 無 | 0.0 | 5/6 | Y | 1977/1 | RC | 近隣 20,000円(税込) 物件からの距離15 | old | https://www.homes.co.jp/chintai/room/bb8ff3c5032fd29e51108b294148ff5925149640/ |
| 1.14 | エルミタージュ下鴨東 | 2LDK | 55.43 | 129,000 | 8500 | 無 / 1ヶ月 | 1.0 | 2/2 | n | 2024/7 | 軽量鉄骨 | 無 | A | https://www.homes.co.jp/chintai/room/2b159fd4d7b4ef9cc309a701dbbd1a304c494fcd/ |
| 1.22 | 北白川追分町貸家 | 5DK | 63.66 | 88,000 | 0 | 1ヶ月 / 10万円 | 1.14 | 1/2 | ? | 1988/8 | 木造 | - | house | https://www.homes.co.jp/chintai/room/cc782e59d6412951da4bb7279386dc52bc5ebbfc/ |
| 1.23 | グレーシー北白川 | 3LDK | 68.39 | 130,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 3/3 | n | 1991/8 | RC | 空有 20,000円(税込) | B | https://www.homes.co.jp/chintai/room/ec27a4bcb25d02ce204bc3f6593a9d3f268aea6c/ |
| 1.25 | メゾンフジ | 3DK | 80.0 | 135,000 | 5000 | 無 / 無 | 0.0 | 2/5 | n | 1985/10 | 鉄骨 | 無 | old | https://www.homes.co.jp/chintai/room/a6cd9e39d774787814593c7c3e0551d786aecba9/ |
| 1.26 | コーポ富有 | 2LDK | 48.51 | 100,000 | 9000 | 10万円 / 10万円 | 1.0 | 2/4 | Y | 1985/7 | RC | 無 | old | https://www.homes.co.jp/chintai/b-1228500328211/ |
| 1.27 | 山和小路 | 3LDK | 66.97 | 125,000 | 10000 | 無 / 1ヶ月 | 1.0 | 5/5 | Y | 1999/11 | RC | 近隣 20,000円(税込) 物件からの距離21 | B | https://www.homes.co.jp/chintai/room/261f7f0092c4f523e537f11c69dba15ed1d8e7ca/ |
| 1.35 |  | 3DK | 54.0 | 100,000 | 0 | 10万円 / 10万円 | 1.0 | 1/4 | n | 1979/7 | RC | 近隣 (1台) 25,000円 物件からの距離4 | old | https://www.homes.co.jp/chintai/room/408270dfe50222d9ff3f6a1e2890d42ee36955bd/ |
| 1.35 | 乾ハイツ | 3DK | 54.0 | 100,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/4 | n | 1974/7 | RC | 近隣 (1台) 25,000円 物件からの距離2 | old | https://www.homes.co.jp/chintai/room/8d86946117deb4a55c569e92cc561f660f59af11/ |
| 1.38 | 下鴨泉川町貸家 | 4DK | 66.78 | 92,000 | 0 | 9.2万円 / 9.2万円 | 1.0 | None/2 | n | 1972/3 | 木造 | 空無 | house | https://www.homes.co.jp/chintai/room/59f26cfe147858501adbb8b4476514734eb8d095/ |
| 1.39 | エスポワール麩屋町 | 2LDK | 46.59 | 114,000 | 10000 | 20万円 / 35万円 | 3.07 | 5/5 | Y | 2009/3 | RC | 無 | A | https://www.homes.co.jp/chintai/room/f6ab4f43236cfd9599c4f3de01f47a9471a08f38/ |
| 1.39 | アイル竹嶋 | 2LDK | 52.0 | 120,000 | 15000 | 無 / 25万円 | 2.08 | 5/6 | Y | 1993/3 | RC | 無 | B | https://www.homes.co.jp/chintai/room/23be1e00118124c0ed39aa864a0101ac72d2ac28/ |
| 1.39 | アイル竹嶋 | 2LDK | 61.0 | 130,000 | 0 | 無 / 30万円 | 2.31 | 5/6 | Y | 1993/3 | RC | 無 | B | https://www.homes.co.jp/chintai/room/826781d0397ba1313ca84adaeb277fa2fa043bda/ |
| 1.39 | 二条麩屋町ビューハイツ | 3SLDK | 72.8 | 140,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 6/9 | Y | 1981/10 | SRC | - | old | https://www.homes.co.jp/chintai/room/45184da6c8de9ebf58049be02ecf4c129d8a9c73/ |
| 1.39 |  | 3LDK | 72.69 | 140,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 6/9 | Y | 1981/10 | SRC | 空無 月額30,000〜35,000円 | old | https://www.homes.co.jp/chintai/room/2d936588982eca6873c85044af5736c41b74434d/ |
| 1.42 | メガロコープ西陣A棟 | 3LDK | 58.44 | 110,000 | 0 | 無 / 1ヶ月 | 1.0 | 5/13 | Y | 1972/6 | RC | - | old | https://www.homes.co.jp/chintai/room/9506ca50981f35cb13689fb5678a7d92d569ba4c/ |
| 1.46 | 北白川コーポラス | 3LDK | 66.0 | 100,000 | 8000 | 10万円 / 10万円 | 1.0 | 3/5 | n | 1988/3 | RC | 空有 8,000円(税込) | old | https://www.homes.co.jp/chintai/room/22e8555d87048862dd31c37876b8d0c35a12fc8e/ |
| 1.46 | 北白川コーポラス | 3DK | 57.0 | 100,000 | 8000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/4 | n | 1970/10 | RC | 空有 8,000円(税無) | old | https://www.homes.co.jp/chintai/room/42b93eeb625f6939f9938a5692d9e18757c123b9/ |
| 1.47 | パラドール御所 | 3LDK | 63.18 | 130,000 | 15000 | 1ヶ月 / 2ヶ月 | 2.0 | 5/7 | Y | 1984/3 | RC | 空有 (1台) 22,000円(税込) | old | https://www.homes.co.jp/chintai/room/2c15620f6f5a7e0ac135ee962ac5b9228e275af4/ |
| 1.47 |  | 3LDK | 63.18 | 130,000 | 15000 | 1ヶ月 / 2ヶ月 | 2.0 | 5/7 | Y | 1983/3 | RC | 近隣 22,000円(税込) 物件からの距離43 | old | https://www.homes.co.jp/chintai/room/04d6fce5d97a7b98a0e625c903733e0d35c60a28/ |
| 1.49 | グレーシー高野 | 3DK | 47.8 | 79,000 | 4000 | 無 / 7.9万円 | 1.0 | 3/5 | n | 1979/3 | RC | 空有 11,000円(税込) 駐車料金：1100 | old | https://www.homes.co.jp/chintai/room/1e5f695a4dddcc68ccbc1fd6a9476afe6d40d297/ |
| 1.49 | グレーシー高野 | 3DK | 49.0 | 79,000 | 4000 | 無 / 7.9万円 | 1.0 | 3/5 | n | 1972/4 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/b9eed297e24e608885fbd25323eff6f099a47686/ |
| 1.49 | グレーシー高野 | 3DK | 51.0 | 79,000 | 4000 | 無 / 1ヶ月 | 1.0 | 3/5 | n | 1972/1 | RC | 空有 16,500円(税込) | old | https://www.homes.co.jp/chintai/room/57a2221b4ff715aad614adb91d41be3ab08dc13e/ |
| 1.53 | リッツ岡崎 | 2LDK | 69.0 | 128,000 | 12000 | 10万円 / 19.2万円 | 1.5 | 1/3 | Y | 1990/2 | RC | 空有 22,000円(税込) | old | https://www.homes.co.jp/chintai/room/9c67e3d2e193063ffa72eba3ae05d31017c65289/ |
| 1.54 | 出雲路俵町4−4貸家 | 4DK | 76.21 | 93,000 | 0 | 9.3万円 / 9.3万円 | 1.0 | None/2 | n | 1970/1 | 木造 | 空有 無料 | house | https://www.homes.co.jp/chintai/room/915cceae368e0f6964cfdd6d12cb7498107d2eb0/ |
| 1.54 |  | 4DK | 66.21 | 93,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 2/2 | n | 1930/1 | 木造 | 空有 (1台) 無料 | house | https://www.homes.co.jp/chintai/room/1fd8454c0ce47d132859fc7dd459684cd7c028a2/ |
| 1.54 |  | 3DK | 50.0 | 100,000 | 0 | 無 / 1ヶ月 | 1.0 | None/2 | n | 1980/1 | 木造 | 近隣 13,200円(税込) 物件からの距離29 | house | https://www.homes.co.jp/chintai/room/21f022a6841b64effc2322684ed2c2362934f58e/ |
| 1.55 |  | 2LDK | 69.93 | 130,000 | 0 | 1ヶ月 / 1.5ヶ月 | 1.5 | 1/2 | n | 1983/8 | 木造 | 近隣 16,500円(税込) 物件からの距離38 | house | https://www.homes.co.jp/chintai/room/40c43c16d68f76a2f0e09eb7e0f9df843e02801d/ |
| 1.56 | コンフォール北白川II | 3DK | 52.46 | 110,000 | 0 | 10万円 / 無 | 0.0 | 3/3 | n | 1994/2 | 鉄骨 | 空有 20,000円(税無) | B | https://www.homes.co.jp/chintai/room/0b0442f24fd04139636cc430974980325d98b7b0/ |
| 1.56 | コンフォール北白川III | 2LDK | 50.4 | 115,000 | 5000 | 12万円 / 無 | 0.0 | 3/3 | n | 2006/2 | RC | 空有 20,000円(税無) | A | https://www.homes.co.jp/chintai/room/1f9fbaeeb97e569fd90dace290539323078cafcd/ |
| 1.6 | 裏築地町貸家 | 2LDK | 60.0 | 115,000 | 0 | 11.5万円 / 11.5万円 | 1.0 | None/3 | n | 1998/7 | 木造 | 無 | house | https://www.homes.co.jp/chintai/b-1429410208697/ |
| 1.6 |  | 2LDK | 51.88 | 115,000 | 0 | 11.5万円 / 11.5万円 | 1.0 | None/3 | n | 1998/7 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/bba206f8342072c935232e2c202cd6123e22ef2f/ |
| 1.6 |  | 2LDK | 65.8 | 115,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 2/3 | n | 1998/7 | 木造 | 近隣 14,300円(税込) 物件からの距離47 | house | https://www.homes.co.jp/chintai/room/a8464f81a79795d20b02e256ff643be508cb394b/ |
| 1.6 | i.レジデンス御所北 | 2LDK | 54.08 | 133,000 | 7000 | 無 / 20万円 | 1.5 | 1/4 | n | 2014/3 | RC | 空無 | A | https://www.homes.co.jp/chintai/room/feadebeccc02b7bf6e21c173a687761dc7349a87/ |
| 1.61 | 上京区元真如堂町貸家 | 3DK | 54.37 | 78,000 | 0 | 無 / 7.8万円 | 1.0 | None/2 | n | 1960/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/b-1051710239228/ |
| 1.61 | 藤波ビル | 2LDK | 47.52 | 114,000 | 4000 | 5万円 / 10万円 | 0.88 | 2/4 | n | 1990/3 | 鉄骨 | 近隣 22,000円(税込) 物件からの距離35 | old | https://www.homes.co.jp/chintai/room/851f586a297d8914784adac21cff002d105e9b99/ |
| 1.61 | 藤波ビル | 2LDK | 47.0 | 114,000 | 4000 | 5万円 / 10万円 | 0.88 | 2/4 | n | 1990/3 | その他 | 無 | old | https://www.homes.co.jp/chintai/room/834e1a38d2da8a06b7271b4fa6f128623b0c6c62/ |
| 1.61 |  | 3LDK | 71.0 | 125,000 | 0 | 12.5万円 / 12.5万円 | 1.0 | None/2 | n | 1982/6 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/b72484666b31937f382df4d1837a1aa599dd11dd/ |
| 1.61 | メゾンミュゲ | 2LDK | 64.98 | 130,000 | 5000 | 1ヶ月 / 2ヶ月 | 2.0 | 2/2 | n | 2020/6 | 軽量鉄骨 | 空有 13,200円(税無) | A | https://www.homes.co.jp/chintai/b-1014960004338/ |
| 1.61 |  | 2LDK | 66.8 | 135,000 | 5000 | 10万円 / 10万円 | 0.74 | 2/3 | n | 1993/5 | RC | 空有 10,000円 | B | https://www.homes.co.jp/chintai/room/be77d7391c7f734b866d1b7432828a948d19f11d/ |
| 1.61 | セラヴィ119 | 2LDK | 63.52 | 140,000 | 10000 | 14万円 / 14万円 | 1.0 | 5/5 | Y | 1989/6 | RC | 無 | old | https://www.homes.co.jp/chintai/room/80298fefed8825a8fb4b112251bd943c16282443/ |
| 1.62 |  | 3LDK | 65.93 | 99,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 2/2 | n | 1999/5 | 木造 | 近隣 27,500円(税込) 物件からの距離49 | house | https://www.homes.co.jp/chintai/room/ac253f8ff95972c5b675659e6d93c2aa75d6a569/ |
| 1.62 | グランタック御所西　貸家 | 3LDK | 65.93 | 99,000 | 0 | 9.9万円 / 9.9万円 | 1.0 | None/2 | n | 1991/5 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/09e40c8861b9579450d5ccb15ba3a58ecfaece69/ |
| 1.62 | 上京区藪之内町貸家 | 2LDK | 65.93 | 99,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | None/5 | n | 1984/12 | 鉄骨 | - | house | https://www.homes.co.jp/chintai/room/1b76229184248dc41c0c89067acbc99cd9a40d37/ |
| 1.63 | ロイヤルセンタービルコバヤシ | 2LDK | 56.28 | 87,000 | 8000 | 8.7万円 / 17.4万円 | 2.0 | 3/5 | Y | 1988/1 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/34b7b3f9e8b31a414fc23ad9259c59c6dd797db8/ |
| 1.63 | チェリービューマンション | 2LDK | 57.87 | 110,000 | 5000 | 11万円 / 22万円 | 2.0 | 2/3 | n | 1990/5 | RC | 空有 27,500円(税込) | old | https://www.homes.co.jp/chintai/room/48300c8fe475fb82b0a8c97b9348e6bab1d06179/ |
| 1.63 | ピアレス円勝寺 | 2LDK | 62.41 | 120,000 | 20000 | 1ヶ月 / 1ヶ月 | 1.0 | 2/3 | Y | 1984/11 | RC | 空有 (1台) 27,500円(税込) | old | https://www.homes.co.jp/chintai/room/2dd93fe36825fdbbbebfc42dc8920686516fc9d9/ |
| 1.63 | ピアレス円勝寺 | 2LDK | 53.0 | 120,000 | 20000 | 12万円 / 12万円 | 1.0 | 2/3 | Y | 1984/12 | RC | 無 | old | https://www.homes.co.jp/chintai/room/a8ebcfab3e1cf483cfa70f5a07ed18e1fcd081dc/ |
| 1.63 |  | 2LDK | 60.0 | 120,000 | 20000 | 12万円 / 12万円 | 1.0 | 2/3 | Y | 1984/11 | RC | 空有 27,000円 物件からの距離0m | old | https://www.homes.co.jp/chintai/room/8d3e1bfc37046dcde3639890824be48c630a84ac/ |
| 1.66 |  | 2LDK | 45.0 | 83,000 | 8000 | 無 / 18万円 | 2.17 | 4/4 | n | 1991/8 | RC | 空無 | B | https://www.homes.co.jp/chintai/b-13670321176/ |
| 1.66 |  | 2LDK | 45.0 | 83,000 | 8000 | 無 / 18万円 | 2.17 | 3/4 | n | 1991/8 | RC | 空無 | B | https://www.homes.co.jp/chintai/room/fc295cfefec72d10dba24b0b62019616fe144b73/ |
| 1.69 | ロイヤルステイツ御所南 | 2LDK | 45.03 | 132,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 6/9 | Y | 2009/2 | SRC | 無 | A | https://www.homes.co.jp/chintai/room/b5d83a42929c2e22902aa241a6b9b226458824ce/ |
| 1.7 | パラドール御所 | 3LDK | 63.18 | 130,000 | 15000 | 13万円 / 26万円 | 2.0 | 5/7 | Y | 1984/2 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/89f1cd9d56e701d5df7a5d2e62a1bddf220a186a/ |
| 1.72 | ロイヤルセンタービル小林 | 2LDK | 50.94 | 80,000 | 8000 | 1ヶ月 / 2ヶ月 | 2.0 | 3/5 | Y | 1987/12 | RC | - | old | https://www.homes.co.jp/chintai/room/1ff1269a0ddcc881b63424440a532da288fb7c68/ |
| 1.72 | 御所西エリアの二世帯も可能な大型戸建 | 7DK | 113.39 | 140,000 | 0 | 28万円 / 14万円 | 1.0 | None/2 | n | 1950/5 | 木造 | - | house | https://www.homes.co.jp/chintai/room/cd41f31e9c453353a3146497ded40b1a915d465e/ |
| 1.75 | Far East東山 | 2LDK | 59.87 | 134,000 | 12000 | 1ヶ月 / 2ヶ月 | 2.0 | 1/3 | n | 2015/6 | RC | 空有 (1台) 15,000円(税込) | A | https://www.homes.co.jp/chintai/room/e49f7bc7a52d9e543685e04785ebfb43dcd29ba0/ |
| 1.76 | チェリービューマンション | 2LDK | 57.87 | 110,000 | 5000 | 1ヶ月 / 2ヶ月 | 2.0 | 2/3 | n | 1990/5 | その他 | 空無 | old | https://www.homes.co.jp/chintai/room/a170ba5355d104d64bd138060acadb738fd25829/ |
| 1.77 | 京都グランデ　II番館 | 2LDK | 63.56 | 140,000 | 5000 | 14万円 / 14万円 | 1.0 | 3/3 | n | 2019/10 | 木造 | 無 | A | https://www.homes.co.jp/chintai/room/51c48e3240b5cda258528bb27af064f84acce674/ |
| 1.8 |  | 4DK | 74.72 | 89,000 | 6000 | 1ヶ月 / 1ヶ月 | 1.0 | None/2 | n | 1979/9 | 木造 | 近隣 16,500円(税込) 物件からの距離18 | house | https://www.homes.co.jp/chintai/room/0a5bf70b19bf826d4d76b2cd160958edee13542c/ |
| 1.8 | プラネシア神宮道 | 2LDK | 55.77 | 139,000 | 8000 | 無 / 1.5ヶ月 | 1.5 | 2/5 | Y | 2010/6 | RC | 近隣 27,500円(税込) 物件からの距離22 | A | https://www.homes.co.jp/chintai/room/76e3e87c19749ba6e1da1c2a6fd9568a5868c9e9/ |
| 1.81 | プラネシア星の子御所西 | 2LDK | 60.2 | 114,000 | 9000 | 無 / 1.5ヶ月 | 1.5 | 4/5 | n | 1973/5 | 鉄骨 | 近隣 17,600円(税込) 物件からの距離34 | old | https://www.homes.co.jp/chintai/room/e780719a56a3cba4957de06f46232780cf20474c/ |
| 1.81 |  | 2LDK | 61.9 | 114,000 | 9000 | 無 / 17.1万円 | 1.5 | 4/4 | n | 1973/5 | その他 | 無 | old | https://www.homes.co.jp/chintai/room/b97fba75e58b27ec453485ab27fc3118e77b8b3f/ |
| 1.81 | プラネシア星の子御所西 | 2LDK | 60.2 | 114,000 | 9000 | 無 / 1.5ヶ月 | 1.5 | 5/6 | n | 2001/3 | 鉄骨 | 無 | A | https://www.homes.co.jp/chintai/room/6b37137759e9b80759292a4d2998039ba1f7d65e/ |
| 1.81 | プラネシア星の子御所西 | 2LDK | 51.93 | 114,000 | 9000 | 無 / 17.1万円 | 1.5 | 4/5 | n | 2001/2 | 鉄骨 | 無 | A | https://www.homes.co.jp/chintai/room/bfb9d4fae0dc2b8f4c0dca7e0747f4ce26917ea5/ |
| 1.81 | プラネシア星の子御所西 | 2LDK | 61.9 | 114,000 | 9000 | 無 / 17.1万円 | 1.5 | 4/6 | n | 1973/5 | その他 | 無 | old | https://www.homes.co.jp/chintai/room/5364230f3af99d91729c423b2dda38876e4f5515/ |
| 1.81 | プラネシア星の子御所西 | 2LDK | 52.0 | 117,000 | 9000 | 無 / 無 | 0.0 | 2/4 | n | 1973/5 | その他 | 無 | old | https://www.homes.co.jp/chintai/b-13670277078/ |
| 1.81 | プラネシア星の子御所西 | 2LDK | 52.0 | 117,000 | 9000 | 無 / 無 | 0.0 | 2/6 | n | 1973/5 | その他 | 無 | old | https://www.homes.co.jp/chintai/room/4a58641f2aeec558bf22e005bb27660f111ced79/ |
| 1.81 | プラネシア星の子御所西 | 2LDK | 52.0 | 117,000 | 9000 | 無 / 無 | 0.0 | 3/5 | n | 1973/5 | 鉄骨 | 近隣 17,600円(税込) 物件からの距離34 | old | https://www.homes.co.jp/chintai/room/38ee701f7f942eb0b13b7963cda74d24e25d1441/ |
| 1.81 | プラネシア星の子御所西 | 2LDK | 53.0 | 117,000 | 9000 | 無 / 1ヶ月 | 1.0 | 2/4 | n | 2001/2 | 鉄骨 | 空無 | A | https://www.homes.co.jp/chintai/room/dcb5a97be7758f1562f6c258fa4107b098288f10/ |
| 1.81 | プラネシア星の子御所西 | 2LDK | 51.43 | 117,000 | 9000 | 無 / 1ヶ月 | 1.0 | 2/5 | n | 2001/2 | RC | - | A | https://www.homes.co.jp/chintai/room/20145985ce3c3196f482d30e3420c4069dca0704/ |
| 1.81 | プラネシア星の子御所西 | 2LDK | 51.43 | 117,000 | 9000 | 無 / 無 | 0.0 | 3/6 | n | 1973/5 | 鉄骨 | 無 | old | https://www.homes.co.jp/chintai/room/6aa0edca1a942af8e68e79757f07f6ef2192b3fa/ |
| 1.83 | 下鴨スタイル | 2LDK | 55.37 | 122,500 | 5800 | 無 / 1ヶ月 | 1.0 | 1/2 | n | 2008/12 | 木造 | 空有 (2台) 19,800円(税込) | A | https://www.homes.co.jp/chintai/room/3a9f04393733baca9dde85b07686c80298bb2803/ |
| 1.85 | 北白川松園 | 3DK | 53.0 | 108,000 | 0 | 10.8万円 / 10.8万円 | 1.0 | 3/4 | n | 1969/10 | RC | 空有 11,000円(税込) | old | https://www.homes.co.jp/chintai/room/ee54417f339c5be2538b97fbfdd2f4ef7dfdb879/ |
| 1.86 | 御所西　東向きの陽当りの良い戸建 | 2LDK | 51.08 | 80,000 | 0 | 8万円 / 8万円 | 1.0 | None/2 | n | 1950/3 | 木造 | - | house | https://www.homes.co.jp/chintai/room/0243bb19f76e5e3d1d680aabb674b514fe67fd49/ |
| 1.86 | カストルム洛北 | 3LDK | 67.65 | 113,000 | 12000 | 無 / 10万円 | 0.88 | 2/7 | Y | 1983/4 | RC | 空有 22,000円(税込) | old | https://www.homes.co.jp/chintai/room/fa069941b6689e6f623decfc78178a8e959efd11/ |
| 1.86 | カストルム洛北 | 3LDK | 64.9 | 113,000 | 12000 | 10万円 / 10万円 | 0.88 | 3/7 | Y | 1983/4 | RC | 空有 22,000円(税込) | old | https://www.homes.co.jp/chintai/room/1eaacb30ac5ae09643d455f238ada696a7ad40c9/ |
| 1.86 | カストルム洛北 | 3LDK | 64.9 | 113,000 | 12000 | 10万円 / 10万円 | 0.88 | 2/7 | Y | 1983/4 | RC | 空有 22,000円(税込) | old | https://www.homes.co.jp/chintai/room/615ec640b610cb3c7ddb0473897e07445cbcc0cb/ |
| 1.86 | カストルム洛北 | 3LDK | 67.65 | 113,000 | 12000 | 10万円 / 10万円 | 0.88 | 3/7 | Y | 1983/3 | RC | 空有 22,000円(税込) | old | https://www.homes.co.jp/chintai/room/6c92868070a4184872b01b207faa037de137a7f8/ |
| 1.87 | 東大路高野第1住宅1棟 | 3DK | 60.94 | 98,000 | 0 | 無 / 9.8万円 | 1.0 | 7/7 | Y | 1979/11 | RC | 無 | old | https://www.homes.co.jp/chintai/room/e65fa9448ddd38e8109c37a5077f5b51e1f550f1/ |
| 1.88 | レジデンス古橋 | 2LDK | 61.53 | 128,000 | 10000 | 無 / 無 | 0.0 | 4/6 | Y | 1978/10 | RC | 空有 22,000円(税込) | old | https://www.homes.co.jp/chintai/room/64e529ec20ac547f8dfeeb476a1c0dff572f232b/ |
| 1.88 | グリーンヒル北白川 | 3LDK | 60.0 | 130,000 | 3850 | 無 / 2ヶ月 | 2.0 | 1/2 | n | 1985/3 | RC | 近隣 13,200円(税込) 物件からの距離23 | old | https://www.homes.co.jp/chintai/room/b9f6da2f804436ebbdd83b72a0f052b3639d21f9/ |
| 1.88 | グリーンヒル北白川 | 3LDK | 54.85 | 130,000 | 3850 | 無 / 26万円 | 2.0 | 1/2 | n | 1985/1 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/2571865b93064177029d8413bdd7485336edba9e/ |
| 1.89 | マナーハウス | 2LDK | 62.31 | 115,000 | 10000 | 11.5万円 / 11.5万円 | 1.0 | 1/4 | Y | 1996/1 | RC | 空有 25,300円(税込) 駐車料金：2530 | B | https://www.homes.co.jp/chintai/room/e02ca4cd4789167a22b1f05081470f89d7822ad1/ |
| 1.89 | マナーハウス | 2LDK | 62.31 | 115,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 2/4 | Y | 1996/1 | RC | 近隣 23,000円 物件からの距離10m | B | https://www.homes.co.jp/chintai/room/ecc64447c7027f95fe6c354f6dea153a2750610e/ |
| 1.9 | カバーロ京都御池 | 2LDK | 48.37 | 120,000 | 5000 | 無 / 24万円 | 2.0 | 3/8 | Y | 1994/5 | その他 | 無 | B | https://www.homes.co.jp/chintai/room/59b03e0cd703fc71014742c3e50e798977f5f585/ |
| 1.92 |  | 3LDK | 74.8 | 120,000 | 10000 | 12万円 / 12万円 | 1.0 | 9/11 | Y | 1982/11 | SRC | 空無 | old | https://www.homes.co.jp/chintai/room/feaba8aa23fc7d7b633fbcc6f54da12f38032d4c/ |
| 1.92 | サンレジデンス錦綾東堀川 | 3LDK | 76.14 | 130,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/11 | Y | 1982/10 | SRC | 近隣 17,600円(税込) 物件からの距離20 | old | https://www.homes.co.jp/chintai/room/8e7a8d7ae81ae48171483a41b532438a429bdba1/ |
| 1.95 | 白川セントラルハイツ | 3DK | 50.22 | 75,000 | 9800 | 8.5万円 / 1ヶ月 | 1.0 | 5/5 | Y | 1981/9 | RC | 近隣 13,200円(税込) 物件からの距離41 | old | https://www.homes.co.jp/chintai/room/049aae00f0c1b8b396df1e23f6228b581ec41309/ |
| 1.96 | 下南田町大前邸III | 3LDK | 80.9 | 98,000 | 0 | 9.8万円 / 19.6万円 | 2.0 | None/2 | n | 1960/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/c21c2aeaf6a2fdecdc451a175c2bdc39cc0c18ee/ |
| 1.96 |  | 3DK | 55.83 | 110,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 1/2 | n | 1983/10 | 木造 | 近隣 15,400円(税込) 物件からの距離29 | house | https://www.homes.co.jp/chintai/room/ce2f7c60a2edc4860ee734b4f6042221050ea807/ |
| 1.97 | 上京区西山崎町貸家 | 2LDK | 65.45 | 130,000 | 0 | 無 / 2ヶ月 | 2.0 | 1/2 | n | 1970/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/f9a15a4df300d430f0d8e9a3cf1a3f9fed2179d2/ |
| 1.99 | プラネシア神宮道 | 2LDK | 50.97 | 139,000 | 8000 | 無 / 20.85万円 | 1.5 | 2/5 | Y | 2010/6 | RC | 空有 (1台) 16,500円(税込) ※道幅が | A | https://www.homes.co.jp/chintai/room/5283231766d070bad417f397393e5b17eb565b47/ |
| 2.0 |  | 5DK | 47.72 | 70,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 2/2 | n | 1967/1 | 木造 | 近隣 16,500円(税込) 物件からの距離30 | house | https://www.homes.co.jp/chintai/room/c1966ad9bb41fd83f2e118875d42e7c520058298/ |
| 2.0 |  | 5DK | 50.0 | 70,000 | 0 | 7万円 / 7万円 | 1.0 | None/2 | n | 1960/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/7e4ec5c27c8f14f1d1a0b052d2cb6f88c3b7cc7f/ |
| 2.0 | 下鴨貸家 | 5DK | 47.72 | 70,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | ? | 1940/3 | 木造 | 無 | old | https://www.homes.co.jp/chintai/room/c6ed17edca9d26ddad2f2e366dfa046001bfa42d/ |
| 2.0 | マサール哲学の道 | 2LDK | 58.57 | 107,000 | 3500 | 無 / 10.7万円 | 1.0 | 2/2 | n | 2015/3 | 木造 | 無 | A | https://www.homes.co.jp/chintai/room/827337fe51ebfab44c7537ebeadebc63fbc71243/ |
| 2.0 | スペシャリー堀川 | 3LDK | 65.75 | 120,000 | 7500 | 12万円 / 12万円 | 1.0 | 7/11 | Y | 1997/9 | SRC | 空有 27,500円(税込) | B | https://www.homes.co.jp/chintai/room/29ba00ad7e2e0d8aa2bdec35f61ca1480f278082/ |
| 2.0 | スペシャリー堀川 | 3LDK | 65.05 | 120,000 | 7500 | 1ヶ月 / 1ヶ月 | 1.0 | 7/11 | Y | 1997/8 | SRC | 空有 27,500円(税込) | B | https://www.homes.co.jp/chintai/room/9e4a3580de8545ecf5deb8d496f7705dbf2d9a16/ |
| 2.01 | 左京区田中上古川町戸建住宅 | 3DK | 57.37 | 110,000 | 0 | 11万円 / 11万円 | 1.0 | None/2 | n | 1984/12 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/63718dcfa331bda8fa4c54adff6c85c45714c7fb/ |
| 2.01 | グローバル北白川 | 2LDK | 53.42 | 120,000 | 5000 | 無 / 12万円 | 1.0 | 4/7 | Y | 1997/2 | RC | 空有 14,300円(税込) | B | https://www.homes.co.jp/chintai/room/0a4f213bd4a7c788fdd6fb82ebfdedd6a1493b79/ |
| 2.01 | エル　ソレイユ | 3LDK | 64.76 | 134,000 | 4400 | 無 / 1ヶ月 | 1.0 | 2/3 | n | 2005/2 | 鉄骨 | 空有 29,700円(税込) | A | https://www.homes.co.jp/chintai/room/0967ba84c9f5d47bff04a0c5ae1fcb3a2f422528/ |
| 2.03 | 橋本町469貸家 | 6DK | 66.0 | 135,000 | 0 | 1ヶ月 / 無 | 0.0 | 1/2 | n | 1957/9 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/6f88dc6c4dc7401a025b29744a5bd2adcddd2401/ |
| 2.05 | 下鴨森ケ前町30-8貸家 | 4DK | 47.72 | 70,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 2/2 | n | 1940/3 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/a814f2b49fa0a075066a1c75eee350f2e34325ba/ |
| 2.05 |  | 3LDK | 58.0 | 90,000 | 0 | 無 / 20万円 | 2.22 | 1/2 | n | 1964/3 | 木造 | 近隣 15,400円(税込) 物件からの距離49 | house | https://www.homes.co.jp/chintai/room/f3c3fca59c8d88913e50b74f7ff73e3514632a66/ |
| 2.05 | シャーメゾン西伊織 | 2LDK | 60.87 | 130,000 | 6000 | 3万円 / 27万円 | 2.08 | 2/2 | n | 2014/10 | 軽量鉄骨 | 空有 14,300円(税込) | A | https://www.homes.co.jp/chintai/room/d75985071e861f23bca5deae2b0ec6048ef5a301/ |
| 2.08 | カストルム洛北 | 2LDK | 64.9 | 115,000 | 12000 | 10万円 / 10万円 | 0.87 | 5/7 | Y | 1983/4 | RC | 空有 22,000円(税込) | old | https://www.homes.co.jp/chintai/room/e50821c44bf3b9d98cee2aa4ea5a450dff1b3b4c/ |
| 2.11 | ロートレック中京 | 2LDK | 52.17 | 125,000 | 15000 | 25万円 / 25万円 | 2.0 | 9/11 | Y | 1984/1 | SRC | 無 | old | https://www.homes.co.jp/chintai/b-1429410192584/ |
| 2.13 |  | 3LDK | 64.43 | 125,800 | 9000 | 12.58万円 / 12.58万円 | 1.0 | 5/10 | Y | 2001/4 | RC | 空有 27,500円(税込) | A | https://www.homes.co.jp/chintai/room/4059240641b71d181e184942c2f9a72b2eb814d8/ |
| 2.13 |  | 3LDK | 64.43 | 125,800 | 9000 | 1ヶ月 / 1ヶ月 | 1.0 | 6/10 | Y | 2001/2 | SRC | 空有 27,500円(税込) | A | https://www.homes.co.jp/chintai/room/048d97db164208184ec6c815e5f0a6324c796665/ |
| 2.13 |  | 3LDK | 64.43 | 126,800 | 9000 | 1ヶ月 / 1ヶ月 | 1.0 | 7/10 | Y | 2001/2 | SRC | 空有 27,500円(税込) | A | https://www.homes.co.jp/chintai/room/e7a9d816c4d99f0b5168b6720d381a06e0d2047d/ |
| 2.13 |  | 3LDK | 65.55 | 127,200 | 9000 | 1ヶ月 / 1ヶ月 | 1.0 | 4/10 | Y | 2001/2 | SRC | 空有 27,500円(税込) | A | https://www.homes.co.jp/chintai/room/008184feb980bc614f97b96523bf0c6582b1c97a/ |
| 2.13 |  | 3LDK | 65.55 | 129,200 | 9000 | 1ヶ月 / 1ヶ月 | 1.0 | 8/10 | Y | 2001/2 | SRC | 空有 27,500円(税込) | A | https://www.homes.co.jp/chintai/room/72abdd8852070368785c670040515674d2edf7c8/ |
| 2.14 | 下鴨フラッツ | 2LDK | 48.0 | 98,000 | 6000 | 9.8万円 / 9.8万円 | 1.0 | 2/3 | n | 1993/4 | RC | 無 | B | https://www.homes.co.jp/chintai/room/5a1e3edc5731e08b94b3b0d01d71a01a427c0d63/ |
| 2.14 | 下鴨フラッツ | 2LDK | 52.0 | 98,000 | 6000 | 10万円 / 10万円 | 1.02 | 2/3 | n | 1993/4 | RC | 空有 19,800円(税込) | B | https://www.homes.co.jp/chintai/room/f5016929a5f647b78d3a8bea489f49d7d06f2e4d/ |
| 2.18 |  | 2LDK | 56.23 | 125,000 | 8000 | 無 / 12.5万円 | 1.0 | 5/5 | Y | 1989/6 | RC | 空有 33,000円(税込) | old | https://www.homes.co.jp/chintai/room/6ddd20070069278d67be5faa275a97eca808dacf/ |
| 2.18 | KTマンション2号館 | 3LDK | 56.23 | 125,000 | 8000 | 無 / 1ヶ月 | 1.0 | 5/6 | Y | 1989/7 | RC | 空有 (1台) 25,000円(税込) 物件から | old | https://www.homes.co.jp/chintai/room/d49f62f340bfab3b6201687da0d95ccac51ef273/ |
| 2.2 |  | 2LDK | 53.86 | 78,000 | 0 | 5万円 / 8万円 | 1.03 | None/2 | n | 1967/4 | 木造 | 無 | house | https://www.homes.co.jp/chintai/b-1000170270719/ |
| 2.2 | グレースコート堀川 | 2LDK | 50.0 | 87,000 | 5000 | 無 / 15万円 | 1.72 | 4/5 | Y | 1988/7 | その他 | 無 | old | https://www.homes.co.jp/chintai/b-1399350181396/ |
| 2.2 |  | 3LDK | 115.5 | 120,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1950/1 | 木造 | 空有 (1台) 無料 | house | https://www.homes.co.jp/chintai/room/9d5edbe765049795ca99a0e8d63828c5fba941ff/ |
| 2.22 |  | 2LDK | 52.2 | 81,000 | 4000 | 無 / 無 | 0.0 | 4/4 | n | 1978/9 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/b564924e9b486eec6272f9a357b64c2923040635/ |
| 2.22 |  | 3LDK | 60.0 | 90,000 | 4000 | 無 / 無 | 0.0 | 1/4 | n | 1978/9 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/cee86381829fa0e011d892678698003c09e40382/ |
| 2.23 | ラフィーネ御池 | 2LDK | 63.72 | 120,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 4/11 | Y | 1989/2 | SRC | 無 | old | https://www.homes.co.jp/chintai/room/5d266c404c66230db067a7547dd5df17cc766b53/ |
| 2.23 |  | 2LDK | 60.96 | 122,000 | 7000 | 12.2万円 / 12.2万円 | 1.0 | 1/2 | n | 2025/3 | 木造 | 空有 15,000円(税無) | A | https://www.homes.co.jp/chintai/room/0143eb0b7577a6eee39f0a63b289c1128e1d93e2/ |
| 2.23 | 西陣　町家エリアの路地にある京町家 | 3LDK | 62.3 | 130,000 | 0 | 1ヶ月 / 1.5ヶ月 | 1.5 | 2/2 | n | 1950/1 | 木造 | - | house | https://www.homes.co.jp/chintai/room/caf980b6046caad04971957558fe85d8e464aaae/ |
| 2.24 | シェモア鞍馬口II | 2LDK | 54.86 | 100,000 | 5000 | 1ヶ月 / 1ヶ月 | 1.0 | 1/3 | n | 1984/11 | RC | - | old | https://www.homes.co.jp/chintai/room/c5e61bed43713464696177843b64c618f5daa370/ |
| 2.24 | 三条室町パーク・ホームズ | 2LDK | 52.99 | 135,000 | 10000 | 10万円 / 20万円 | 1.48 | 2/11 | Y | 1996/3 | RC | 空有 20,000円(税無) | B | https://www.homes.co.jp/chintai/room/c192e2e5ee2055be68cfa4d1b0ddf99d12711402/ |
| 2.25 | ファーストコート今出川北 | 3LDK | 55.84 | 98,000 | 10000 | 無 / 9.8万円 | 1.0 | 5/7 | Y | 1981/8 | RC | 無 | old | https://www.homes.co.jp/chintai/b-13670292453/ |
| 2.25 | ファーストコート今出川北 | 3LDK | 60.32 | 98,000 | 10000 | 無 / 1ヶ月 | 1.0 | 5/7 | Y | 1981/10 | RC | 近隣 14,300円(税込) 物件からの距離38 | old | https://www.homes.co.jp/chintai/room/fee1d32072318a71297fc31ef44bdbfa56f29392/ |
| 2.27 | 北白川仕伏町貸家 | 4DK | 72.9 | 87,000 | 0 | 1ヶ月 / 無 | 0.0 | 1/2 | n | 1980/3 | 木造 | - | house | https://www.homes.co.jp/chintai/room/1b34df374c95fd6f196ecf656e93ed668cc32c88/ |
| 2.27 |  | 2LDK | 59.77 | 124,000 | 8000 | 無 / 20万円 | 1.61 | 3/11 | Y | 2004/3 | RC | 空有 17,600円(税込) 駐車料金：1760 | A | https://www.homes.co.jp/chintai/room/5bff82181fc056e2fcdc76a72e38ead849aa65a0/ |
| 2.27 | グラシオン西陣 | 2LDK | 56.83 | 124,000 | 8000 | 無 / 20万円 | 1.61 | 3/11 | Y | 2004/3 | RC | 空有 17,600円(税無) | A | https://www.homes.co.jp/chintai/room/72296b2e58607cb5b38549773649716f4f7ebebb/ |
| 2.28 | 永観堂町貸家 | 4LDK | 75.0 | 130,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1926/1 | 木造 | 近隣 16,500円(税込) 物件からの距離33 | house | https://www.homes.co.jp/chintai/room/6268aa9a7f9671bde4f176c5a935ca8eb17a12d0/ |
| 2.28 | ライオンズマンション二条城東 | 3SDK | 67.79 | 138,000 | 0 | 13.8万円 / 13.8万円 | 1.0 | 10/11 | Y | 1991/3 | SRC | 近隣 30,800円(税込) 物件からの距離15 | B | https://www.homes.co.jp/chintai/room/0f2f6174f952bf31f41502d547050157bb4fe302/ |
| 2.28 | ライオンズマンション二条城東 | 3DK | 61.07 | 138,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 10/11 | Y | 1991/2 | SRC | 空無 周辺の駐車場相場は28、000円前後になり | B | https://www.homes.co.jp/chintai/room/f6f1f5277b8848388cfd359442f4795eef47e54e/ |
| 2.28 | 小山東花池町貸家 | 4LDK | 74.01 | 140,000 | 0 | 15万円 / 15万円 | 1.07 | None/2 | n | 1977/8 | 木造 | 空有 無料 | house | https://www.homes.co.jp/chintai/room/8d7395651e9d2206505063afd0a9a69148494d28/ |
| 2.29 | コトールノール | 2LDK | 50.76 | 84,000 | 8000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/3 | n | 1989/3 | RC | 空有 22,000円(税込) | old | https://www.homes.co.jp/chintai/room/f27faabca2ded356b8c21357f43791a983cf0485/ |
| 2.29 | レジデンス西陣中央 | 3LDK | 60.44 | 114,000 | 10000 | 2ヶ月 / 2ヶ月 | 2.0 | 1/5 | Y | 2002/3 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/150f80e8dae8b046cf0803bf2348f4f62a8d8aac/ |
| 2.29 | レジデンス西陣中央 | 3LDK | 60.44 | 124,000 | 10000 | 2ヶ月 / 2ヶ月 | 2.0 | 5/5 | Y | 2002/3 | RC | 空有 22,000円(税込) | A | https://www.homes.co.jp/chintai/room/de2138ec4ad17c0e4ac0531ef874fdaee24646a2/ |
| 2.33 | ライオンズマンション一条智恵光院 | 2LDK | 49.7 | 83,000 | 10000 | 無 / 1ヶ月 | 1.0 | 2/6 | Y | 1989/6 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/531e672dfb64e0ff1d1b6dc886f8b352e1c5fef2/ |
| 2.33 | ＶＥＧＡ999 | 2LDK | 61.0 | 100,000 | 5000 | 無 / 20万円 | 2.0 | 4/5 | Y | 1991/12 | RC | 空有 18,700円(税込) | B | https://www.homes.co.jp/chintai/room/a311707bec414877fbd6f7ce4f5ead8c69d3d089/ |
| 2.33 | ライオンズマンション一条智恵光院 | 2LDK | 59.4 | 100,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 2/6 | Y | 1989/6 | RC | 近隣 17,600円(税込) 物件からの距離29 | old | https://www.homes.co.jp/chintai/room/73daef76f071bf5b0bce5116210faf1db8214f9d/ |
| 2.33 | アレックス堀川寺之内 | 3LDK | 63.21 | 102,000 | 8000 | 1ヶ月 / 1ヶ月 | 1.0 | 6/11 | Y | 1990/2 | SRC | 近隣 14,300円(税込) 物件からの距離35 | old | https://www.homes.co.jp/chintai/room/2b0ccd09a98320bac744f930d43596386f2422a8/ |
| 2.33 | 玉屋・山三小路 | 3LDK | 71.06 | 115,000 | 9000 | 1ヶ月 / 無 | 0.0 | 3/5 | Y | 1998/10 | RC | 空無 | B | https://www.homes.co.jp/chintai/room/7ab090fcbf01a341aea0177b8534f92d95dda2c8/ |
| 2.33 | 玉屋・山三小路 | 3DK | 64.42 | 115,000 | 9000 | 1ヶ月 / 無 | 0.0 | 2/5 | Y | 1998/10 | RC | 空無 | B | https://www.homes.co.jp/chintai/room/075999bc7190d9173a4524b010632fd4e8817694/ |
| 2.34 | カーネルヒル | 2LDK | 52.65 | 105,000 | 8000 | 10万円 / 無 | 0.0 | 2/5 | Y | 1989/11 | RC | 近隣 30,000円 物件からの距離500m | old | https://www.homes.co.jp/chintai/room/dece54d68d2d572088a7678329d7e04a29a31361/ |
| 2.34 | カーネルヒル | 2LDK | 51.1 | 105,000 | 8000 | 10万円 / 無 | 0.0 | 2/5 | Y | 1989/11 | RC | 無 | old | https://www.homes.co.jp/chintai/room/bc02e8be53ff70796d835956b5cd42c59c5ac2e2/ |
| 2.34 | カーネルヒル | 2LDK | 50.31 | 105,000 | 8000 | 10万円 / 無 | 0.0 | 2/5 | Y | 1989/10 | RC | 近隣 22,000円(税込) 物件からの距離49 | old | https://www.homes.co.jp/chintai/room/14662b09cb7d7061076cc1a040ca52d063787f6e/ |
| 2.34 |  | 2LDK | 50.0 | 105,000 | 8000 | 10万円 / 無 | 0.0 | 2/5 | Y | 1989/10 | RC | 近隣 30,800円(税込) 物件からの距離43 | old | https://www.homes.co.jp/chintai/room/fae89157a7fcc4ef1c4de2cf82575001bd725089/ |
| 2.34 |  | 2LDK | 51.0 | 105,000 | 8000 | 10万円 / 無 | 0.0 | 2/5 | Y | 1989/10 | RC | 無 | old | https://www.homes.co.jp/chintai/room/30d94236a514cfd911fbb91df1f09a5f886ef0a3/ |
| 2.34 | カーネルヒル | 2LDK | 51.1 | 106,000 | 8000 | 10万円 / 無 | 0.0 | 4/5 | Y | 1989/11 | RC | 無 | old | https://www.homes.co.jp/chintai/room/4c0580e9040268cfe281448af876c5845ce0dbeb/ |
| 2.34 | カーネルヒル | 2LDK | 52.65 | 106,000 | 8000 | 10万円 / 無 | 0.0 | 4/5 | Y | 1989/11 | RC | 無 | old | https://www.homes.co.jp/chintai/room/96b913aa697e481c29e056229d7c60ba17b00ef1/ |
| 2.34 | カーネルヒル | 2LDK | 50.31 | 106,000 | 8000 | 10万円 / 無 | 0.0 | 4/5 | Y | 1989/10 | RC | 近隣 22,000円(税込) 物件からの距離49 | old | https://www.homes.co.jp/chintai/room/c5a1a08c38b5c9caf680615480e3cdf7d7fe137d/ |
| 2.34 |  | 2LDK | 50.0 | 106,000 | 8000 | 10万円 / 無 | 0.0 | 4/5 | Y | 1989/10 | RC | 近隣 30,800円(税込) 物件からの距離43 | old | https://www.homes.co.jp/chintai/room/02d5abae4c8c07ec2ec1d64a640e3bcc91149ffa/ |
| 2.34 |  | 4LDK | 76.05 | 120,000 | 0 | 12万円 / 24万円 | 2.0 | None/2 | n | 1982/12 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/41697b322265c1ae3490472cd593ff2040a17eb8/ |
| 2.35 | エクシオ京都御池 | 2LDK | 57.05 | 128,000 | 0 | 10万円 / 15万円 | 1.17 | 4/11 | Y | 1992/10 | SRC | 無 | B | https://www.homes.co.jp/chintai/room/37c56aecffe13d56f7083a16e4da9be563344e71/ |
| 2.36 |  | 3LDK | 61.91 | 114,000 | 10000 | 無 / 27.36万円 | 2.4 | 5/6 | Y | 1980/8 | RC | 空有 17,600円(税込) | old | https://www.homes.co.jp/chintai/room/2f7c150d1d60b972a41bb5544e24e89781880998/ |
| 2.36 |  | 2LDK | 60.62 | 114,000 | 10000 | 無 / 2.4ヶ月 | 2.4 | 5/8 | Y | 1980/8 | RC | 空有 17,600円(税込) | old | https://www.homes.co.jp/chintai/room/6885ae65a99424ab1fd94a9aa4b8c4b146af0270/ |
| 2.36 |  | 3DK | 60.62 | 116,000 | 10000 | 無 / 27.84万円 | 2.4 | 3/6 | Y | 1980/8 | RC | 空有 17,600円(税込) | old | https://www.homes.co.jp/chintai/room/1f96166cdf11d915a433b01131551aff57d5a16d/ |
| 2.36 |  | 2LDK | 60.02 | 116,000 | 10000 | 無 / 2.4ヶ月 | 2.4 | 3/8 | Y | 1980/8 | RC | 空有 17,600円(税込) | old | https://www.homes.co.jp/chintai/room/d00ae4d63fc24aaf75cbd29a876fde925b77c5e3/ |
| 2.36 |  | 3LDK | 60.62 | 120,000 | 10000 | 無 / 28.8万円 | 2.4 | 5/6 | Y | 1980/8 | RC | 空有 17,600円(税込) | old | https://www.homes.co.jp/chintai/room/8e4c6afaaa40d40d65b64f10cfb4d5c0f11381fa/ |
| 2.36 |  | 2LDK | 60.31 | 120,000 | 10000 | 無 / 2.4ヶ月 | 2.4 | 5/8 | Y | 1980/8 | RC | 空有 17,600円(税込) | old | https://www.homes.co.jp/chintai/room/66c80a76dd56e3ae36905a306defe81504edcf21/ |
| 2.36 | イヌイ星の子ハイツ | 2LDK | 55.03 | 120,000 | 10000 | 無 / 28.8万円 | 2.4 | 5/6 | Y | 1980/8 | RC | 空有 17,600円(税込) | old | https://www.homes.co.jp/chintai/room/93f3624e4712758e726ae2fd841b0f888c21d51e/ |
| 2.36 |  | 2LDK | 64.46 | 123,000 | 10000 | 無 / 29.52万円 | 2.4 | 6/6 | Y | 1980/8 | RC | 空有 17,600円(税込) | old | https://www.homes.co.jp/chintai/room/faa632e0fe327ebda7ec5ffd6e0853e1dd99dc1b/ |
| 2.36 |  | 2LDK | 62.62 | 123,000 | 10000 | 無 / 2.4ヶ月 | 2.4 | 6/8 | Y | 1980/8 | RC | 近隣 17,600円(税込) 物件からの距離42 | old | https://www.homes.co.jp/chintai/room/b906d3596e05e820718ef6266bbd52e63d225cc0/ |
| 2.36 |  | 3LDK | 65.05 | 135,000 | 10000 | 無 / 32.4万円 | 2.4 | 6/6 | Y | 1980/8 | RC | 空有 17,600円(税込) | old | https://www.homes.co.jp/chintai/room/bc48e632f44663937ab70692f7d40b97a8f192af/ |
| 2.36 |  | 3LDK | 61.91 | 135,000 | 10000 | 無 / 2.4ヶ月 | 2.4 | 6/8 | Y | 1980/8 | RC | 近隣 17,600円(税込) 物件からの距離42 | old | https://www.homes.co.jp/chintai/room/efcb2a8e45c6b357bbdb4d5d23b6113404e17c81/ |
| 2.36 | イヌイ星の子ハイツ | 3LDK | 65.64 | 135,000 | 10000 | 無 / 32.4万円 | 2.4 | 6/6 | Y | 1980/8 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/c5da668386331a1308667cbcdf03fcbf6cb79006/ |
| 2.37 |  | 2LDK | 53.0 | 92,000 | 10000 | 無 / 9.2万円 | 1.0 | 2/4 | n | 1991/8 | RC | 無 | B | https://www.homes.co.jp/chintai/room/5c738dca67ca8942c4b50ff9ac01ffc58ed1659a/ |
| 2.37 |  | 2LDK | 56.0 | 92,000 | 10000 | 無 / 9.2万円 | 1.0 | 2/4 | n | 1991/7 | RC | 無 | B | https://www.homes.co.jp/chintai/room/bfa748b927dcb7c96f1e45cd95162cf97587dafd/ |
| 2.37 | CASA SHIMEI | 2LDK | 52.0 | 92,000 | 10000 | 無 / 9.2万円 | 1.0 | 4/4 | n | 1991/7 | RC | 空有 21,000円 物件からの距離0m | B | https://www.homes.co.jp/chintai/room/8fc76289c9fc757e7a809d8ebf21994f994fe366/ |
| 2.37 | ハイムフロイデン一乗寺 | 3LDK | 55.0 | 115,000 | 10000 | 無 / 2ヶ月 | 2.0 | 4/6 | Y | 1984/1 | RC | 近隣 12,000円(税込) 物件からの距離34 | old | https://www.homes.co.jp/chintai/room/a18f3d294b5d26d9c43fd1399fef768c2637a307/ |
| 2.37 | ハイムフロイデン一乗寺 | 3DK | 63.0 | 140,000 | 10000 | 無 / 2ヶ月 | 2.0 | 6/6 | Y | 1984/1 | RC | 近隣 12,000円(税込) 物件からの距離34 | old | https://www.homes.co.jp/chintai/room/c7ac4697f46762a845c843770a6e620a2eaeb5ca/ |
| 2.4 |  | 3LDK | 65.55 | 125,000 | 9000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/10 | Y | 1998/4 | SRC | 近隣 16,500円(税込) 物件からの距離21 | B | https://www.homes.co.jp/chintai/room/106e8e0c9c7874607f9cd452d737dff3c612003f/ |
| 2.4 |  | 3LDK | 74.81 | 130,000 | 9000 | 13万円 / 13万円 | 1.0 | 5/10 | Y | 1998/4 | SRC | 無 | B | https://www.homes.co.jp/chintai/room/37954aff5193705836d0cc42227fdaad43405c14/ |
| 2.42 | ベルスーズ西陣 | 3LDK | 65.02 | 120,000 | 9500 | 無 / 1ヶ月 | 1.0 | 5/6 | Y | 1998/9 | RC | 空無 | B | https://www.homes.co.jp/chintai/room/7df9af1ee2de4186fb2238e65d6b3d4a8622b7a5/ |
| 2.42 | ベルスーズ西陣 | 3LDK | 65.02 | 120,000 | 9500 | 無 / 1ヶ月 | 1.0 | 3/6 | Y | 1998/9 | RC | 空無 | B | https://www.homes.co.jp/chintai/room/89d6282944547282d199498bc60650ab4271058c/ |
| 2.43 | コスモ星の子ハイツ | 3DK | 57.23 | 90,000 | 9000 | 無 / 9万円 | 1.0 | 4/7 | Y | 1985/10 | RC | 無 | old | https://www.homes.co.jp/chintai/room/85e444cefdf1edfd80642951a01db4895d5e482e/ |
| 2.43 | コスモ星の子ハイツ | 3DK | 48.0 | 90,000 | 9000 | 無 / 1ヶ月 | 1.0 | 4/7 | Y | 1985/9 | SRC | 無 | old | https://www.homes.co.jp/chintai/room/b5daf98912420016e971158e98cbf624d8f2e47f/ |
| 2.43 | ＬＥＧＡＬ京都二条城東 | 2LDK | 57.45 | 135,000 | 12180 | 無 / 20万円 | 1.48 | 6/11 | Y | 2005/12 | RC | 近隣 30,800円(税込) 物件からの距離15 | A | https://www.homes.co.jp/chintai/room/9a3c94ed1fec55a6cfb2fa33c52ee09da9496690/ |
| 2.43 | ＬＥＧＡＬ京都二条城東 | 2LDK | 57.45 | 138,000 | 12180 | 無 / 26万円 | 1.88 | 2/11 | Y | 2005/12 | RC | 近隣 30,800円(税込) 物件からの距離15 | A | https://www.homes.co.jp/chintai/room/2f7f81613ce4f6801d512ca97e09889663b08cf5/ |
| 2.44 | コスモ星の子ハイツ | 3DK | 56.0 | 90,000 | 9000 | 無 / 1ヶ月 | 1.0 | 4/7 | Y | 1985/9 | RC | - | old | https://www.homes.co.jp/chintai/room/c5e60069dae5cb8ca361acf22e574ce1a5b0b217/ |
| 2.44 | 藤原マンション | 2LDK | 45.0 | 90,000 | 5000 | 9万円 / 9万円 | 1.0 | 1/3 | n | 1974/3 | RC | 空有 19,800円(税込) | old | https://www.homes.co.jp/chintai/room/7663e1a9347206d309a747f06ef11dde59de152f/ |
| 2.44 | ハイムフロイデン一乗寺 | 3LDK | 55.0 | 100,000 | 10000 | 無 / 20万円 | 2.0 | 2/6 | Y | 1988/3 | SRC | 空無 | old | https://www.homes.co.jp/chintai/room/7dc185e03693e86b7e13c64c3a67ef31d4fb1f71/ |
| 2.44 | ハイムフロイデン一乗寺 | 2LDK | 55.0 | 100,000 | 10000 | 無 / 20万円 | 2.0 | 1/6 | n | 1988/3 | SRC | 空無 | old | https://www.homes.co.jp/chintai/room/ec61fec462fe28a3f47580d1d8673ef0d40e643b/ |
| 2.44 | ハイムフロイデン一乗寺 | 3DK | 51.0 | 100,000 | 10000 | 無 / 20万円 | 2.0 | 2/6 | Y | 1983/4 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/9bf4dcf6e39fe0f25fdde428cf53ed3968487e19/ |
| 2.44 | ハイムフロイデン一乗寺 | 3LDK | 55.0 | 105,000 | 10000 | 無 / 21万円 | 2.0 | 4/6 | Y | 1988/3 | SRC | 空無 | old | https://www.homes.co.jp/chintai/room/ad6cdb6490364ad4dc247b703e12cdcb76bed3c4/ |
| 2.44 | ハイムフロイデン一乗寺 | 3LDK | 54.44 | 105,000 | 10000 | 無 / 21万円 | 2.0 | 4/6 | Y | 1983/4 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/723df6f66271c79c9dcedd7d66005c1e17aaeb37/ |
| 2.44 | ハイムフロイデン一乗寺 | 3DK | 60.0 | 130,000 | 10000 | 無 / 26万円 | 2.0 | 6/6 | Y | 1988/3 | SRC | 空無 | old | https://www.homes.co.jp/chintai/room/5c0b7ca6c4319f66cc9b9297a74a182c895e77c3/ |
| 2.44 | ハイムフロイデン一乗寺 | 3LDK | 60.0 | 130,000 | 10000 | 無 / 26万円 | 2.0 | 6/6 | Y | 1983/4 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/eb3f2a819f20f9883ffed5728180eb509d5064f6/ |
| 2.44 | ハイムフロイデン一乗寺 | 3DK | 63.0 | 140,000 | 10000 | 無 / 2ヶ月 | 2.0 | 6/6 | Y | 1984/1 | RC | 近隣 12,000円(税込) 物件からの距離34 | old | https://www.homes.co.jp/chintai/room/0ed52ae55e7848e74b2e096f5596f2008a83bb1c/ |
| 2.47 | エステムプラザ京都四条烏丸 | 2LDK | 53.42 | 140,000 | 15000 | 無 / 14万円 | 1.0 | 8/11 | Y | 2004/2 | SRC | 無 | A | https://www.homes.co.jp/chintai/room/98be4f679bb12dd158e5165f0821e1b02b00226f/ |
| 2.5 | メゾン・ド・プレパント | 3LDK | 76.78 | 140,000 | 5000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/3 | n | 2002/3 | 鉄骨 | 近隣 17,600円(税込) 物件からの距離31 | A | https://www.homes.co.jp/chintai/room/b0aa223b95c9ebcad7072bc3370658545b583d13/ |
| 2.52 | Ｗｉｔｈ京Ｇｒａｎｄｅｓ | 2LDK | 50.24 | 139,000 | 13000 | 13.9万円 / 20万円 | 1.44 | 1/5 | Y | 2019/2 | RC | 無 | A | https://www.homes.co.jp/chintai/room/5a821fb128703698bf3d1d499ce17a51e5fc318f/ |
| 2.55 |  | 4DK | 95.0 | 105,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/3 | n | 1997/10 | 木造 | 近隣 16,500円(税込) 物件からの距離20 | house | https://www.homes.co.jp/chintai/room/9fd54c6b8e11cd72d1d3339ca904aabe3b0edba5/ |
| 2.55 |  | 4DK | 65.0 | 105,000 | 0 | 10.5万円 / 10.5万円 | 1.0 | None/3 | n | 1996/10 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/5d717278223c7100689aa1c8aae1514b45aabcc7/ |
| 2.55 | 伊佐町貸家 | 4DK | 89.1 | 105,000 | 0 | 10.5万円 / 10.5万円 | 1.0 | 3/3 | n | 1996/10 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/a1190cfcd9bd08c1c078d285c1cfbffa3610ccae/ |
| 2.55 |  | 4DK | 79.0 | 105,000 | 0 | 10.5万円 / 10.5万円 | 1.0 | None/3 | n | 1996/10 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/e24f6ee8ab344cfeb7042e586e1b616312620d53/ |
| 2.55 | ロザーンジュ堀川 | 2LDK | 55.44 | 115,000 | 6500 | 1ヶ月 / 1ヶ月 | 1.0 | 3/10 | Y | 1995/12 | SRC | 空無 近隣の駐車場相場は23000円前後になりま | B | https://www.homes.co.jp/chintai/room/9382bbb53757f64484168358af9b3f0270dfc762/ |
| 2.55 | ロザーンジュ堀川 | 2LDK | 56.42 | 118,000 | 6500 | 1ヶ月 / 1ヶ月 | 1.0 | 4/10 | Y | 1995/12 | SRC | 空無 近隣の駐車場相場は23000円前後になりま | B | https://www.homes.co.jp/chintai/room/2727884b9810ee477c27f37dbcf677fb7570ffd5/ |
| 2.56 | コーポシャルマン | 2LDK | 61.65 | 140,000 | 8000 | 1ヶ月 / 2ヶ月 | 2.0 | 3/4 | n | 1989/3 | RC | 無 | old | https://www.homes.co.jp/chintai/room/c0bf8007a637b704885f4164e05a1bd1ab4e167a/ |
| 2.56 |  | 2LDK | 61.65 | 140,000 | 8000 | 1ヶ月 / 2ヶ月 | 2.0 | 4/4 | n | 1989/3 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/19da57c99eb7b8a7477818af799c0896217a5cc3/ |
| 2.56 |  | 2LDK | 61.65 | 140,000 | 8000 | 1ヶ月 / 2ヶ月 | 2.0 | 3/4 | n | 1980/10 | RC | 近隣 22,000円(税込) 物件からの距離15 | old | https://www.homes.co.jp/chintai/room/203c370ce033ad9331bc47712f386e0a89fffcd8/ |
| 2.58 | 伊佐町貸家 | 4DK | 89.1 | 105,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/3 | n | 1997/10 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/52cf4d93f724c7ea96a532c336359ce27547de09/ |
| 2.59 |  | 2LDK | 51.0 | 116,000 | 7500 | 無 / 11.6万円 | 1.0 | 4/5 | Y | 2015/8 | RC | 無 | A | https://www.homes.co.jp/chintai/room/53e4ab7336e592148640bddb2eeb9b56e590e31e/ |
| 2.6 | ポルト　ボヌール | 2LDK | 48.97 | 105,000 | 6900 | 無 / 10.5万円 | 1.0 | 4/5 | Y | 2016/3 | RC | 無 | A | https://www.homes.co.jp/chintai/room/8089bbaec7a5c43e80ae54bbbf3641c4b8f48114/ |
| 2.6 | ポルト・ボヌール | 2LDK | 48.97 | 105,000 | 6900 | 無 / 1ヶ月 | 1.0 | 3/5 | Y | 2016/3 | RC | 近隣 12,000円(税込) 物件からの距離39 | A | https://www.homes.co.jp/chintai/room/af392538a3f99f66c34c1fb3ea8d549088c856b8/ |
| 2.61 | コト北小路 | 3LDK | 67.5 | 130,500 | 9500 | 13.05万円 / 13.05万円 | 1.0 | 7/9 | Y | 2000/12 | SRC | 空無 | B | https://www.homes.co.jp/chintai/room/73f7ef0008629bd6e8c703b1e1b55c2b643d0030/ |
| 2.61 |  | 2LDK | 71.54 | 138,000 | 0 | 13.8万円 / 27.6万円 | 2.0 | None/2 | n | 2026/6 | 木造 | 空有 無料 | house | https://www.homes.co.jp/chintai/room/81ee816e7646d3a6b02bcb6b509170c01351acca/ |
| 2.61 |  | 2LDK | 70.0 | 138,000 | 0 | 13.8万円 / 27.6万円 | 2.0 | None/2 | n | 2026/6 | 木造 | 空無 | house | https://www.homes.co.jp/chintai/room/c41d50e8d8d6d6981a2dcb413f94204bf6ce2c97/ |
| 2.62 |  | 2LDK | 50.04 | 119,000 | 9000 | 無 / 11.9万円 | 1.0 | 9/10 | Y | 1991/12 | SRC | 無 | B | https://www.homes.co.jp/chintai/room/15579240e2de28b2bf8c600760d88afdac4f1a08/ |
| 2.62 | Uresidence二条城 | 2LDK | 50.04 | 120,000 | 9000 | 無 / 1ヶ月 | 1.0 | 4/10 | Y | 1991/12 | SRC | 近隣 18,000円(税込) 物件からの距離17 | B | https://www.homes.co.jp/chintai/room/9858c8fbc3cc9edd2655e4d1cecf64631461348a/ |
| 2.62 | パインフィールド二条城 | 2LDK | 50.45 | 137,000 | 8000 | 無 / 無 | 0.0 | 8/10 | Y | 1995/12 | SRC | 空有 27,500円(税込) | B | https://www.homes.co.jp/chintai/room/afd5fd669cf4c7c3ba78df6b779c850ecd74115a/ |
| 2.62 | パインフィールド二条城 | 2LDK | 50.45 | 139,000 | 8000 | 無 / 無 | 0.0 | 5/10 | Y | 1997/2 | RC | 空無 | B | https://www.homes.co.jp/chintai/room/90e091234266bddd02a85890e477e1d06fad52ca/ |
| 2.62 |  | 3DK | 72.42 | 140,000 | 10000 | 5万円 / 15万円 | 1.07 | 2/2 | n | 1988/3 | RC | 空有 13,000円(税込) | old | https://www.homes.co.jp/chintai/room/ae053921429bfb00871064eddff565c25fc54a93/ |
| 2.62 |  | 3LDK | 75.56 | 140,000 | 10000 | 5万円 / 15万円 | 1.07 | 2/2 | n | 1988/3 | RC | 近隣 11,000円(税無) 物件からの距離39 | old | https://www.homes.co.jp/chintai/room/4be5b0b3e45e03dd3ce670220fe4355bc44aae04/ |
| 2.64 |  | 3DK | 83.14 | 85,000 | 0 | 8.5万円 / 8.5万円 | 1.0 | None/2 | n | 1976/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/e865d4fa19b3a802d3d500a3457c3a60a5264404/ |
| 2.64 | フィエルテ四条烏丸シュッド | 3LDK | 60.0 | 130,000 | 0 | 無 / 13万円 | 1.0 | 10/10 | Y | 1996/9 | RC | 無 | B | https://www.homes.co.jp/chintai/room/11220da406199da594fe257a23cbf196efe7bd72/ |
| 2.66 | ルネ紫野 | 2LDK | 59.8 | 85,000 | 4000 | 5万円 / 10万円 | 1.18 | 1/2 | n | 2005/4 | 木造 | 空有 15,000円(税無) | A | https://www.homes.co.jp/chintai/room/093c4e07146e0fb2c328ef149507e76295797b14/ |
| 2.67 | ベルメゾン一条 | 3DK | 53.33 | 100,000 | 3000 | 3万円 / 20万円 | 2.0 | 2/3 | n | 1989/2 | RC | 近隣 17,600円(税込) 物件からの距離42 | old | https://www.homes.co.jp/chintai/room/75664ab2e6c35332302ad0ba62bdf4d2c1bac719/ |
| 2.67 | メガロコープ西陣 | 3LDK | 58.44 | 110,000 | 0 | 無 / 11万円 | 1.0 | 5/11 | Y | 1972/4 | SRC | 無 | old | https://www.homes.co.jp/chintai/room/27eec2abe344e00ecb7597d216510de142a8d527/ |
| 2.67 | ペレニアルフラックス | 2LDK | 75.5 | 120,000 | 6000 | 12万円 / 12万円 | 1.0 | 2/3 | n | 1992/10 | RC | 空有 15,400円(税無) | B | https://www.homes.co.jp/chintai/room/c9ba445fd1cd78494ac20497a9aa865d25053348/ |
| 2.7 | セレーナ北大路 | 2LDK | 46.33 | 130,000 | 5000 | 無 / 13万円 | 1.0 | 2/3 | n | 2023/1 | 木造 | 無 | A | https://www.homes.co.jp/chintai/room/666c8257f230c2226815659b25ae102a3c56289e/ |
| 2.72 | 主税町戸建西棟 | 2LDK | 59.5 | 95,000 | 0 | 9.5万円 / 9.5万円 | 1.0 | 1/2 | n | 1965/11 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/5f89eddf60971fd2cc8b517f16f1d31c5e7ed919/ |
| 2.73 | サニーハイツ | 2LDK | 45.0 | 81,000 | 3000 | 1ヶ月 / 1ヶ月 | 1.0 | 2/3 | n | 1979/9 | 鉄骨 | 無 | old | https://www.homes.co.jp/chintai/room/ba5359ff6e2d78de6d516c4114bf4764f9a28d8e/ |
| 2.73 | シンフォニー四条河原町 | 3LDK | 57.0 | 140,000 | 13300 | 2ヶ月 / 2ヶ月 | 2.0 | 3/11 | Y | 2001/10 | SRC | 無 | A | https://www.homes.co.jp/chintai/room/9f420ccf8cab3448a6a28729b4630a932d6f17c8/ |
| 2.74 | せんぼん有彩館 | 3LDK | 71.23 | 132,000 | 15000 | 無 / 無 | 0.0 | 2/10 | Y | 1997/9 | SRC | 空有 25,300円(税込) | B | https://www.homes.co.jp/chintai/room/8fb7a97ecce0393e680f7932a5626df487a2a446/ |
| 2.74 | せんぼん有彩館 | 3LDK | 71.23 | 133,000 | 15000 | 無 / 無 | 0.0 | 3/10 | Y | 1997/9 | SRC | 空有 25,300円(税込) | B | https://www.homes.co.jp/chintai/room/e03976532d3b1d7a434d995b335757fca7693835/ |
| 2.74 | せんぼん有彩館 | 3LDK | 71.23 | 134,000 | 15000 | 無 / 無 | 0.0 | 5/10 | Y | 1997/8 | SRC | 空有 25,300円(税込) | B | https://www.homes.co.jp/chintai/room/5c9b78b3003a13e048f8ae76d0829bd2cea48baa/ |
| 2.76 | 詩仙ハイムI | 2LDK | 47.0 | 90,000 | 5000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/4 | n | 1979/6 | RC | - | old | https://www.homes.co.jp/chintai/room/c1c661356f1e7a197fb9a42e881468eb139c303b/ |
| 2.76 | 藤和シティホームズ三条堀川 | 2LDK | 58.72 | 135,000 | 10000 | 13.5万円 / 27万円 | 2.0 | 6/11 | Y | 1997/3 | RC | 空無 | B | https://www.homes.co.jp/chintai/room/f5506322364aab37f06d3529d79d9208c71ba9df/ |
| 2.77 | 詩仙ハイム | 3DK | 46.53 | 90,000 | 5000 | 9万円 / 9万円 | 1.0 | 3/4 | n | 1979/1 | RC | 無 | old | https://www.homes.co.jp/chintai/room/a4bccca0c9f9fd53c89ee2af6936bd29aa6fabf2/ |
| 2.77 | 詩仙ハイムI | 2LDK | 50.0 | 90,000 | 5000 | 9万円 / 9万円 | 1.0 | 3/4 | n | 1979/1 | RC | 空有 10,000円(税無) | old | https://www.homes.co.jp/chintai/room/8a3f775c204f0eda0535aa0750ec46ac113353ba/ |
| 2.77 | Ｄ−ＲＯＯＭ一乗寺 | 2LDK | 52.79 | 134,000 | 8000 | 無 / 13.4万円 | 1.0 | 1/3 | n | 2024/10 | 軽量鉄骨 | 空有 14,300円(税無) | A | https://www.homes.co.jp/chintai/room/a8ff76f0fb4aa293189922b1c230630e02961034/ |
| 2.77 | Ｄ−ＲＯＯＭ一乗寺 | 2LDK | 52.79 | 136,000 | 8000 | 無 / 13.6万円 | 1.0 | 2/3 | n | 2024/10 | 軽量鉄骨 | 空有 14,300円(税無) | A | https://www.homes.co.jp/chintai/room/ea31fa53e4baf2eb3f9df05b8cc0d064042b90e7/ |
| 2.79 | 西陣グランドハイツ | 4LDK | 62.78 | 100,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/8 | Y | 1975/6 | RC | 近隣 16,500円(税込) 物件からの距離47 | old | https://www.homes.co.jp/chintai/room/fc187976bb46d5d7b36b99a2e38f5eca509474ab/ |
| 2.79 | ユアメゾン白川　1 | 2LDK | 63.0 | 125,000 | 6000 | 1ヶ月 / 2ヶ月 | 2.0 | 2/2 | n | 2026/11 | 軽量鉄骨 | 空有 15,400円 物件からの距離0m | A | https://www.homes.co.jp/chintai/room/f343b6ae7e790b48b23926d88db323572c3381c6/ |
| 2.79 | STANDZ京都二条 | 2LDK | 48.33 | 135,000 | 20000 | 6.75万円 / 無 | 0.0 | 2/7 | Y | 2026/1 | RC | 近隣 16,500円(税込) 物件からの距離81 | A | https://www.homes.co.jp/chintai/room/806233c912b349a653a5e2cfca48ec517334438c/ |
| 2.8 | 紫野東藤ノ森町貸家 | 3LDK | 87.09 | 100,000 | 0 | 2ヶ月 / 1ヶ月 | 1.0 | 1/2 | ? | 1920/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/bf339a0611142b15cd3a99f3c03c2683d9d22058/ |
| 2.8 | Ｄｅ’ｌｅａｄ今出川通 | 3LDK | 63.72 | 110,000 | 10000 | 5万円 / 15万円 | 1.36 | 10/11 | Y | 1995/10 | RC | 無 | B | https://www.homes.co.jp/chintai/room/68559bc5440d553134e0b82d1400cf28b5c893b5/ |
| 2.8 | ＧＥＮ　ＳＡＫＩＺＯ　ＶＩＬＬＡ烏丸四条 | 3LDK | 54.55 | 120,000 | 9000 | 無 / 24万円 | 2.0 | 5/10 | Y | 1981/5 | SRC | 空有 40,700円(税込) | old | https://www.homes.co.jp/chintai/room/ec63b077eeb16bdab63082faf0e230f4cd08fa9b/ |
| 2.8 | GEN SAKIZO VILLA烏丸四条 | 3LDK | 54.55 | 120,000 | 8250 | 無 / 2ヶ月 | 2.0 | 5/11 | Y | 1981/1 | SRC | 空有 40,700円(税込) | old | https://www.homes.co.jp/chintai/room/d33070119d7b5f881fa981b1c2978a8e74592e60/ |
| 2.82 | 二条城北エリアのガレージ付戸建 | 2LDK | 60.54 | 130,000 | 0 | 2ヶ月 / 1ヶ月 | 1.0 | None/3 | n | 2014/10 | 木造 | 空有 (1台) 無料 軽自動車または小型サイズ | house | https://www.homes.co.jp/chintai/room/2d242eb1fdc77ca326a61e253ed69b06d3328da9/ |
| 2.83 | 嶋津マンション | 3LDK | 60.0 | 125,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 4/7 | Y | 1991/8 | RC | 空無 | B | https://www.homes.co.jp/chintai/room/57db22e25d1b2f8dcc24bdaefae3b16e2330a844/ |
| 2.83 | 嶋津マンション | 3LDK | 74.0 | 125,000 | 10000 | 12.5万円 / 12.5万円 | 1.0 | 4/7 | Y | 1991/4 | RC | 近隣 (1台) 30,000円(税込) 物件から | B | https://www.homes.co.jp/chintai/room/72dc984b578b6f71977964e7fef3970e7585d153/ |
| 2.86 | ヴァンヴェールII | 2LDK | 53.87 | 90,000 | 3000 | 無 / 20万円 | 2.22 | 2/2 | n | 1999/1 | 軽量鉄骨 | 空有 10,000円(税無) | B | https://www.homes.co.jp/chintai/room/9cff56ceb38ea8fd6597aa2f1d88b68e1e422db1/ |
| 2.87 | 紫野西藤ノ森町貸家 | 5DK | 77.8 | 110,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/2 | n | 1970/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/c99270d6105e07c772400ff5782bc0394eb87f00/ |
| 2.87 |  | 2LDK | 61.64 | 120,000 | 0 | 12万円 / 24万円 | 2.0 | 11/11 | Y | 1989/11 | SRC | 無 | old | https://www.homes.co.jp/chintai/room/720fbfb27ffdc22dd809caf7b4242659aefbc27e/ |
| 2.87 | ラス・パルマス京小町 | 2LDK | 54.86 | 135,000 | 10000 | 無 / 13.5万円 | 1.0 | 2/5 | Y | 2025/6 | RC | 無 | A | https://www.homes.co.jp/chintai/room/72f669617f95a7f489f9ac7b1e26f0f5bf0953b1/ |
| 2.89 | 洛翠舎 | 3LDK | 69.26 | 128,000 | 11000 | 12.8万円 / 25.6万円 | 2.0 | 4/9 | Y | 2001/2 | RC | 無 | A | https://www.homes.co.jp/chintai/b-1409990267832/ |
| 2.89 |  | 3LDK | 69.4 | 128,000 | 0 | 12.8万円 / 25.6万円 | 2.0 | 8/9 | Y | 2001/2 | RC | 無 | A | https://www.homes.co.jp/chintai/room/631cfd49f9de084bfc8064a17d4144e8951ecdbe/ |
| 2.89 | カーサ葵 | 3LDK | 68.14 | 140,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/3 | Y | 2001/4 | RC | 近隣 22,000円(税込) 物件からの距離45 | A | https://www.homes.co.jp/chintai/room/59139e1dc11582e0a44d324be6f30beb378e0c8b/ |
| 2.89 | カーサ葵 | 3LDK | 68.14 | 140,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 2/3 | Y | 2001/4 | RC | 無 | A | https://www.homes.co.jp/chintai/room/dba743af96a5d96a5cd39b988f897b3204cb6af0/ |
| 2.89 | カーサ葵 | 3LDK | 65.81 | 140,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/3 | Y | 2001/4 | RC | 近隣 (1台) 18,000円 物件からの距離4 | A | https://www.homes.co.jp/chintai/room/b95d7d605eef13b4615dacaf191af34742359095/ |
| 2.92 | コスモ二条 | 2LDK | 55.0 | 82,000 | 8000 | 10万円 / 15万円 | 1.83 | 5/11 | Y | 1985/11 | RC | 無 | old | https://www.homes.co.jp/chintai/room/8ff0bc5b1232d397307f811cbd1f1809c5a62e9e/ |
| 2.92 | コスモ二条 | 2LDK | 48.0 | 82,000 | 8000 | 10万円 / 15万円 | 1.83 | 5/11 | Y | 1985/11 | SRC | 無 | old | https://www.homes.co.jp/chintai/room/de12757589fe0437d2a9bb35ce8d98a975aea4d3/ |
| 2.92 | プリムローズ四条 | 2LDK | 52.67 | 117,000 | 5000 | 無 / 1ヶ月 | 1.0 | 7/10 | Y | 2007/11 | RC | 空無 マンション周辺のガレージ相場は、30、00 | A | https://www.homes.co.jp/chintai/room/5cef33c3a3ac6643fd5cdc452a9ad0ce30892695/ |
| 2.92 | ティファール | 3LDK | 69.35 | 138,000 | 11000 | 5万円 / 20万円 | 1.45 | 6/10 | Y | 1999/9 | SRC | 近隣 (1台) 28,000円 物件からの距離4 | B | https://www.homes.co.jp/chintai/room/79eaa0d02f25c8e4852154261af18405582599b4/ |
| 2.92 | ティファール | 3LDK | 69.08 | 138,000 | 11000 | 5万円 / 20万円 | 1.45 | 6/10 | Y | 1999/9 | SRC | 空有 30,800円(税込) | B | https://www.homes.co.jp/chintai/room/9dcc763f8f81be9340ce5f29e7166fa4517cc62c/ |
| 2.92 | ティファール | 3LDK | 69.35 | 138,000 | 11000 | 5万円 / 15万円 | 1.09 | 4/10 | Y | 1999/8 | RC | 近隣 25,300円(税無) 物件からの距離37 | B | https://www.homes.co.jp/chintai/room/71340ecd2d16a73bdc118da0b7015a522a0179ff/ |
| 2.92 | ティファール | 3LDK | 69.35 | 138,000 | 11000 | 5万円 / 15万円 | 1.09 | 3/10 | Y | 1999/8 | RC | 近隣 25,300円(税無) 物件からの距離37 | B | https://www.homes.co.jp/chintai/room/920de9e2e04ff898de78d15fd5debe7a8be26405/ |
| 2.93 | 観タワーハウス | 2LDK | 46.01 | 95,000 | 0 |  /  | None | 4/10 | Y | 1987/4 | SRC |  | old | https://www.homes.co.jp/chintai/room/31c514b2a62114e4d19dc580c9f4048f1acc2037/ |
| 2.96 | シャトレ西陣 | 2LDK | 45.0 | 90,000 | 5000 | 無 / 9万円 | 1.0 | 7/7 | Y | 1977/4 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/23c19ecd15770ad3c2611d8edbc66d8a90fc1903/ |
| 2.96 | シャトレ西陣 | 2LDK | 45.38 | 90,000 | 5000 | 9万円 / 9万円 | 1.0 | 7/7 | Y | 1976/4 | RC | 無 | old | https://www.homes.co.jp/chintai/room/80f25044f7d2585e01661c471e320f54937da664/ |
| 2.96 | 北野の京町家 | 3DK | 58.06 | 130,000 | 0 | 13万円 / 14.3万円 | 1.1 | None/2 | n | 1950/1 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/ca1559b74187dc9a9c9dc93e8af57d02381665a7/ |
| 2.96 | リーガル京都烏丸東 | 2LDK | 57.26 | 140,000 | 17110 | 無 / 20万円 | 1.43 | 2/5 | Y | 2016/3 | RC | 空有 (1台) 35,000円(税込) | A | https://www.homes.co.jp/chintai/room/587027491d375c728f16b846c38db6167f40b910/ |
| 2.97 | サンパティ | 3LDK | 68.0 | 122,000 | 5000 | 1ヶ月 / 1ヶ月 | 1.0 | 2/2 | n | 1993/3 | 木造 | 空有 (1台) 料金：賃料に含む 物件からの距離 | B | https://www.homes.co.jp/chintai/room/24f08827746e9e6962d036f605ab228ea81922ec/ |
| 2.98 | 赤井氏貸家 | 2LDK | 50.0 | 75,000 | 0 | 無 / 13万円 | 1.73 | None/2 | n | 1970/3 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/c84af4f68f46fb2205e1bbbf4eba1f81fbe2a2b2/ |
| 2.98 |  | 2LDK | 45.0 | 75,000 | 0 | 無 / 13万円 | 1.73 | None/2 | n | 1970/3 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/d1986de05787ebc7e7e5f7de17781df757ab94b8/ |
| 2.98 | メゾンエイワ | 2LDK | 51.37 | 86,000 | 5000 | 5万円 / 10万円 | 1.16 | 2/2 | n | 1994/12 | 軽量鉄骨 | 空有 (1台) 17,000円 物件からの距離0 | B | https://www.homes.co.jp/chintai/room/89310b33f0fe031ff95d8bf445cd210c749d8ee8/ |
| 2.99 | クラスカ西陣 | 2LDK | 61.7 | 100,000 | 5000 | 12万円 / 無 | 0.0 | 3/6 | Y | 1973/1 | RC | 空有 19,800円(税込) | old | https://www.homes.co.jp/chintai/room/54478dbefad8c847024cc3a3a01c596f33df5fce/ |
| 2.99 |  | 3SDK | 80.41 | 110,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 2/2 | n | 1926/1 | 木造 | 近隣 (1台) 16,500円 物件からの距離4 | house | https://www.homes.co.jp/chintai/room/19d315b299af580699b2dcc4aacc3e5b5efc14ab/ |
| 3.0 | 第8パールハイツ安井 | 2LDK | 53.0 | 75,000 | 5000 | 5万円 / 10万円 | 1.33 | 3/4 | Y | 1990/5 | RC | 空無 | old | https://www.homes.co.jp/chintai/room/6d5ba0ef03fb23509363add15d1d79f24bd10a71/ |
| 3.0 | レジデンス東山 | 2LDK | 48.5 | 90,000 | 0 | 無 / 9万円 | 1.0 | 3/3 | Y | 1993/4 | その他 | 空有 22,000円(税込) | B | https://www.homes.co.jp/chintai/room/3a9f489d7bf15f18e9f4b1d52c7cdb75bc82ab6c/ |
| 3.0 | レジデンス東山 | 2LDK | 48.5 | 90,000 | 0 | 無 / 9万円 | 1.0 | 2/3 | Y | 1993/4 | その他 | 空有 22,000円(税込) | B | https://www.homes.co.jp/chintai/room/cc2d75f0968365c4f911854c05c7af89abdd3408/ |
| 3.01 |  | 4DK | 80.1 | 120,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 3/3 | n | 1995/2 | 鉄骨 | 近隣 15,000円(税無) 物件からの距離36 | house | https://www.homes.co.jp/chintai/room/d1b1306ef85b906ac72b578691f705d28e41d791/ |
| 3.01 |  | 4DK | 80.1 | 120,000 | 0 | 12万円 / 12万円 | 1.0 | 2/3 | n | 1995/2 | 鉄骨 | 無 | B | https://www.homes.co.jp/chintai/room/c6ae85a263e7ddf43c7bee4f9b1b8e348b0ae0f6/ |
| 3.02 | 紫野下門前町戸建て | 3SLDK | 94.05 | 125,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | 1/3 | n | 1995/4 | 木造 | 空有 無料 | house | https://www.homes.co.jp/chintai/room/d6079adfd5ea6af7b2d8bf2594fbae7ea5b9ecd7/ |
| 3.03 | デ・リード四条大宮 | 3LDK | 60.88 | 113,000 | 7000 | 10万円 / 40万円 | 3.54 | 3/7 | Y | 1994/11 | RC | 無 | B | https://www.homes.co.jp/chintai/room/84d511bf98a61e94a19d0985ab41a981743bb40b/ |
| 3.03 | デ・リード四条大宮 | 3LDK | 60.68 | 113,000 | 7000 | 10万円 / 40万円 | 3.54 | 3/7 | Y | 1994/10 | RC | 無 | B | https://www.homes.co.jp/chintai/room/b34746e6054532e5c7e534e3d3e23c648bf005cd/ |
| 3.04 | Ｃａｖｅ　ｄｅ　Ｋ | 2LDK | 58.56 | 115,000 | 5500 | 無 / 15万円 | 1.3 | 1/3 | n | 2017/10 | 鉄骨 | 空無 | A | https://www.homes.co.jp/chintai/room/d7fd763f2e2222b342c31dfab0bc84c4f4f62fd5/ |
| 3.04 | KOHEEII | 3LDK | 69.07 | 129,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 4/5 | Y | 1999/6 | RC | 空無 | B | https://www.homes.co.jp/chintai/room/4dd17f23f84798ca9b7cc54fa5a982e8fddb44c1/ |
| 3.08 |  | 2LDK | 46.0 | 75,000 | 2000 | 5万円 / 15万円 | 2.0 | 1/2 | n | 1988/3 | 鉄骨 | 空有 13,200円(税込) | old | https://www.homes.co.jp/chintai/room/175ef53fdb37a8c57a95344d4449c3290d4a33cc/ |
| 3.08 |  | 2LDK | 45.0 | 75,000 | 2000 | 5万円 / 15万円 | 2.0 | 1/2 | n | 1985/3 | 鉄骨 | 空無 | old | https://www.homes.co.jp/chintai/room/589c929a145c66d8508d2f11c7dc853c4cf5361f/ |
| 3.08 | GRACEとーべえ | 2LDK | 58.13 | 123,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/6 | Y | 1995/3 | RC | 空有 11,000円 | B | https://www.homes.co.jp/chintai/room/4b4b6509d9de0e3d5b25f6a049bc092d8b48c3b4/ |
| 3.08 |  | 2LDK | 70.32 | 136,000 | 12000 | 13.6万円 / 13.6万円 | 1.0 | 1/4 | Y | 1997/11 | RC | 空有 15,400円(税込) | B | https://www.homes.co.jp/chintai/room/91066d0ee804bca5a6a345c78e9835eeba27fe76/ |
| 3.1 | ラフィーネ北山 | 2LDK | 52.5 | 115,000 | 4500 | 3万円 / 18万円 | 1.57 | 2/2 | n | 1992/1 | 軽量鉄骨 | 空有 11,000円(税込) | B | https://www.homes.co.jp/chintai/room/a396d06f2181400ef9084264f001497c065a0911/ |
| 3.1 |  | 2LDK | 53.03 | 127,000 | 11000 | 無 / 25万円 | 1.97 | 1/3 | n | 2021/4 | 軽量鉄骨 | 無 | A | https://www.homes.co.jp/chintai/room/2d7b5cdaf942059ccab5dc90b978c2c0b26da07e/ |
| 3.11 | Ｄ−ＲＯＯＭ　Ｓａｇａｒｉｍａｔｓｕ | 2LDK | 56.43 | 125,000 | 7000 | 無 / 10万円 | 0.8 | 2/2 | n | 2025/11 | 軽量鉄骨 | 空有 13,200円(税無) | A | https://www.homes.co.jp/chintai/room/21e41dc532adc8ec7fbfa5836875c1f4d287c323/ |
| 3.12 | 大徳寺貸家 | 5DK | 122.08 | 80,000 | 0 | 1ヶ月 / 1ヶ月 | 1.0 | None/1 | n | 1982/6 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/9f0f16dfa24cea39e55623f08574dce9ab92f7b3/ |
| 3.12 | メゾンドール四条大宮 | 2LDK | 52.52 | 98,000 | 10000 | 9.8万円 / 9.8万円 | 1.0 | 8/11 | Y | 1982/3 | SRC | 無 | old | https://www.homes.co.jp/chintai/room/531be66fde9c51bbb5628239c1570ff1f46650f4/ |
| 3.12 |  | 2LDK | 49.95 | 140,000 | 12000 | 無 / 14万円 | 1.0 | 5/6 | Y | 2004/3 | その他 | 無 | A | https://www.homes.co.jp/chintai/room/277a8db06c39d39840ceaf8849599c84eba33fd1/ |
| 3.12 |  | 2LDK | 47.71 | 140,000 | 12000 | 無 / 14万円 | 1.0 | 5/5 | Y | 2004/3 | 鉄骨 | 無 | A | https://www.homes.co.jp/chintai/room/1435975febb077bcdd177e8cdb0bbe2fc9f87c5e/ |
| 3.13 |  | 2LDK | 48.07 | 133,000 | 0 | 無 / 5万円 | 0.38 | 2/3 | n | 2023/6 | 木造 | 無 | A | https://www.homes.co.jp/chintai/room/48a9aa63a8e11cb25ca1f125f09cf18f0c1cd6c9/ |
| 3.14 | 井狩邸貸家 | 2LDK | 57.38 | 100,000 | 0 | 5万円 / 10万円 | 1.0 | None/2 | n | 2004/5 | 軽量鉄骨 | 無 | house | https://www.homes.co.jp/chintai/room/ca0a37de832439577b85c9733602f4cb1200f95a/ |
| 3.2 | 柏清盛町貸家 | 3LDK | 62.09 | 95,000 | 0 | 9.5万円 / 9.5万円 | 1.0 | None/2 | n | 1975/12 | 木造 | 無 | house | https://www.homes.co.jp/chintai/room/32230b6a73a253a22de04be3e49bb41ddf88bab4/ |
| 3.2 | ルネ河原町 | 2SLDK | 75.0 | 115,000 | 0 | 2ヶ月 / 2ヶ月 | 2.0 | 3/10 | n | 1985/8 | SRC | 空無 | old | https://www.homes.co.jp/chintai/room/3cb0f6417cb88da4e17439ab25f2ea8955f79661/ |
| 3.2 | ルネ・河原町 | 2SLDK | 74.3 | 120,000 | 0 | 24万円 / 24万円 | 2.0 | 9/10 | Y | 1985/8 | SRC | 無 | old | https://www.homes.co.jp/chintai/room/3b9ac038123cecf28fe84a121f950ec1d4d334fc/ |
