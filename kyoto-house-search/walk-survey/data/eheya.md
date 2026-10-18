# eheya — いい部屋ネット (eheya.net, 大東建託), WALK survey (≤1.3 km of 京都技術科学センター, 左京区吉田河原町14), fetched 2026-10-18

## Method
- Next.js site; its filter panel works client-side only (no URL parameters) and headless Chromium gets a CloudFront 403, so the SSR ward pages https://www.eheya.net/kyoto/area/<city>/search/?page=N were crawled **unfiltered with curl** (Chrome UA, 1.3 s apart). HTTP codes: {'200': 20}.
- Wards 左京 26103, 上京 26102, 中京 26104 (site building counts {'左京区': {'buildings': 99}, '上京区': {'buildings': 148}, '中京区': {'buildings': 134}}) → 20 list pages, 691 search-result rooms (691 unique incl. recommendation blocks), parsed from __NEXT_DATA__.
- Client-side funnel (only 2LDK+ and ≥45 m² are hard rules; no rent / 礼金 / age / floor / elevator rule): total 691, layout not 2LDK+ 551, > 1.5 km (town-level) 29, candidates 17, station walk ⇒ > 1.3 km 92, geocode contradicts station (kept) 1, area<45 2 → unit pages fetched (HTTP {'200': 17}) → detail-stage drops none.
- Geocoding: eheya shows only town-level addresses → GSI town centroid (±300 m; Kyoto 通り名 addresses reduced to ward+町名 by kgeo.py); kept up to 1.5 km (flagged in notes). Because Kyoto town names repeat, every geocode is checked against the listed 駅徒歩N分 (≤ N×80 m from that station): listings that cannot be ≤1.3 km are dropped, contradicting geocodes are not trusted (station decides).
- 仲介手数料 / 保証会社 fees are not on the unit JSON; 更新料 and specialNotes are in `other_initial`.
- Station plausibility check (geofix.py; Kyoto town names repeat, GSI returns one): {'checked': 17, 'no_station': 0, 'inconsistent_moved': 0, 'dropped_lower_bound': 2, 'roughly_consistent_kept': 1}; dropped (cannot be ≤1.3 km given the listed 駅徒歩): 2 → out/eheya_geodropped.json.

## Result
- **Kept 15 units** (after merging 0 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via the same building name in another listing with a full address, 0 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 9; rent range kept: 128000–465000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'A': 14, 'old': 1}; 礼金 ≤1ヶ月 12, >1ヶ月 3, unknown 0 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'town': 15} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 9/6/0; by ward: {'上京区': 10, '左京区': 3, '中京区': 2}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/eheya/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.34 | エスタプレイス | 2LDK | 68.55 | 206,000 | 7500 | 0円 / 1ヶ月 | 1.0 | 2/6 | Y | 2027/3 | RC | 有(敷地内) 月22,000円(税込) | A | https://www.eheya.net/detail/300000830001270000016/ |
| 0.34 | エスタプレイス | 2LDK | 68.55 | 207,000 | 7500 | 0円 / 1ヶ月 | 1.0 | 3/6 | Y | 2027/3 | RC | 有(敷地内) 月22,000円(税込) | A | https://www.eheya.net/detail/300000830001270000012/ |
| 0.34 | エスタプレイス | 2LDK | 68.55 | 208,000 | 7500 | 0円 / 1ヶ月 | 1.0 | 5/6 | Y | 2027/3 | RC | 有(敷地内) 月22,000円(税込) | A | https://www.eheya.net/detail/300000830001270000004/ |
| 0.34 | エスタプレイス | 2LDK | 73.03 | 215,000 | 7500 | 0円 / 1ヶ月 | 1.0 | 2/6 | Y | 2027/3 | RC | 有(敷地内) 月22,000円(税込) | A | https://www.eheya.net/detail/300000830001270000013/ |
| 0.34 | エスタプレイス | 2LDK | 73.03 | 216,000 | 7500 | 0円 / 1ヶ月 | 1.0 | 4/6 | Y | 2027/3 | RC | 有(敷地内) 月22,000円(税込) | A | https://www.eheya.net/detail/300000830001270000005/ |
| 0.34 | エスタプレイス | 2LDK | 73.03 | 216,000 | 7500 | 0円 / 1ヶ月 | 1.0 | 3/6 | Y | 2027/3 | RC | 有(敷地内) 月22,000円(税込) | A | https://www.eheya.net/detail/300000830001270000009/ |
| 0.41 | BelleLead御所東 | 2LDK | 53 | 154,000 | 6000 | 0円 / 1ヶ月 | 1.0 | 1/2 | n | 2025/9 | 木造 | 近隣駐車場 物件より60m 自走式 月22,00 | A | https://www.eheya.net/detail/300000832008246000001/ |
| 0.41 | BelleLead御所東 | 2LDK | 61.69 | 174,000 | 6000 | 0円 / 1ヶ月 | 1.0 | 2/2 | n | 2025/9 | 木造 | 近隣駐車場 物件より60m 自走式 月22,00 | A | https://www.eheya.net/detail/300000832008246000003/ |
| 0.47 | ザ・パークハウス京都鴨川御所東 | 2LDK | 104.01 | 465,000 | 0 | 465,000円 / 930,000円 | 2.0 | 5/5 | Y | 2017/3 | RC | 有 月49,500円(税込) | A | https://www.eheya.net/detail/300000832008197000002/ |
| 1.01 | かぐら坂荘 | 2LDK | 60.23 | 128,000 | 7000 | 0円 / 128,000円 | 1.0 | 3/3 | n | 2011/3 | RC | 有 月22,000円(税込) | A | https://www.eheya.net/detail/300000832007706000002/ |
| 1.34 | パークホームズ堺町御門 | 3LDK | 74.32 | 261,000 | 20000 | 281,000円 / 562,000円 | 2.15 | 4/5 | Y | 2014/10 | RC | 無 | A | https://www.eheya.net/detail/300000832008541000002/ |
| 1.35 | ルミエール下鴨 | 2SLDK | 70.54 | 156,000 | 4600 | 0円 / 1ヶ月 | 1.0 | 2/2 | n | 2014/5 | 木造 | 無 | A | https://www.eheya.net/detail/300000830000558004473/ |
| 1.35 | T's スクエア 下鴨 | 3LDK | 63.85 | 183,000 | 8500 | 0円 / 0円 | 0.0 | 1/2 | n | 2021/3 | 軽量鉄骨 | 有 月19,800円(税込) | A | https://www.eheya.net/detail/300000832003344000008/ |
| 1.39 | ラ・サール御所 | 4LDK | 75.59 | 150,000 | 15000 | 0円 / 1ヶ月 | 1.0 | 3/3 | n | 1988/3 | RC | 無 | old | https://www.eheya.net/detail/300000832009089000002/ |
| 1.47 | ヴィークコート京都 河原町二条 | 3LDK | 75.13 | 380,000 | 0 | 1ヶ月 / 2ヶ月 | 2.0 | 7/7 | Y | 2023/8 | RC | 無 | A | https://www.eheya.net/detail/300000832009514000001/ |
