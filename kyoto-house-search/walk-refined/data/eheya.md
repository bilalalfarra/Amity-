# eheya — いい部屋ネット (eheya.net, 大東建託), WALK3 survey (≤3.0 km of 京都技術科学センター, 左京区吉田河原町14; rent ≤140,000), fetched 2026-10-18

## Method
- Next.js site; its filter panel works client-side only (no URL parameters) and headless Chromium gets a CloudFront 403, so the SSR ward pages https://www.eheya.net/kyoto/area/<city>/search/?page=N were crawled **unfiltered with curl** (Chrome UA, 1.3 s apart). HTTP codes: {'200': 32}.
- Wards 北 26101, 上京 26102, 左京 26103, 中京 26104, 東山 26105, 下京 26106 (site building counts {'北区': {'buildings': 77}, '上京区': {'buildings': 146}, '左京区': {'buildings': 97}, '中京区': {'buildings': 132}, '東山区': {'buildings': 26}, '下京区': {'buildings': 118}}) → 32 list pages, 1166 search-result rooms (1166 unique incl. recommendation blocks), parsed from __NEXT_DATA__.
- Client-side funnel (hard rules: 2LDK+, ≥45 m², rent ≤140,000; no 礼金 / age / floor / elevator rule): total 1166, layout not 2LDK+ 974, > 3.2 km (town-level) 15, rent>140,000 118, station walk ⇒ > 3.0 km 42, candidates 15, area<45 2 → unit pages fetched (HTTP {'200': 15}) → detail-stage drops none.
- Geocoding: eheya shows only town-level addresses → GSI town centroid (±300 m; Kyoto 通り名 addresses reduced to ward+町名 by kgeo.py); kept up to 3.2 km (flagged in notes). Because Kyoto town names repeat, every geocode is checked against the listed 駅徒歩N分 (≤ N×80 m from that station): listings that cannot be ≤1.3 km are dropped, contradicting geocodes are not trusted (station decides).
- 仲介手数料 / 保証会社 fees are not on the unit JSON; 更新料 and specialNotes are in `other_initial`.
- Station plausibility check (geofix.py; Kyoto town names repeat, GSI returns one): {'checked': 15, 'no_station': 0, 'inconsistent_moved': 0, 'dropped_lower_bound': 0}; dropped (cannot be ≤3.0 km given the listed 駅徒歩): 0 → out/eheya_geodropped.json.

## Result
- **Kept 15 units** (after merging 0 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via the same building name in another listing with a full address, 0 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 0; rent range kept: 100000–140000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'A': 10, 'old': 2, 'B': 3}; 礼金 ≤1ヶ月 14, >1ヶ月 1, unknown 0 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'town': 15} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 8/7/0; by ward: {'左京区': 8, '中京区': 4, '上京区': 3}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/eheya/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.01 | かぐら坂荘 | 2LDK | 60.23 | 128,000 | 7000 | 0円 / 128,000円 | 1.0 | 3/3 | n | 2011/3 | RC | 有 月22,000円(税込) | A | https://www.eheya.net/detail/300000832007706000002/ |
| 1.83 | 下鴨スタイル | 2LDK | 55.37 | 122,500 | 5800 | 0円 / 1ヶ月 | 1.0 | 1/2 | n | 2008/12 | 木造 | 有(敷地内) 月19,800円(税込) | A | https://www.eheya.net/detail/300000830000333002095/ |
| 2.0 | マサール哲学の道 | 2LDK | 58.57 | 107,000 | 3500 | 0円 / 1ヶ月 | 1.0 | 2/2 | n | 2015/3 | 木造 | 無 | A | https://www.eheya.net/detail/300000830000585004850/ |
| 2.05 | シャーメゾン西伊織 | 2LDK | 60.87 | 130,000 | 6000 | 30,000円 / 270,000円 | 2.08 | 2/2 | n | 2014/9 | 軽量鉄骨 | 有 月14,300円(税込) | A | https://www.eheya.net/detail/300000832006780000003/ |
| 2.18 | KTマンションⅡ号館 | 2LDK | 56.23 | 125,000 | 8000 | 0円 / 1ヶ月 | 1.0 | 5/6 | Y | 1989/6 | RC | 無 | old | https://www.eheya.net/detail/300000832009049000001/ |
| 2.28 | ライオンズマンション二条城東 | 3DK | 61.07 | 138,000 | 0 | 138,000円 / 138,000円 | 1.0 | 10/11 | Y | 1991/2 | その他 | 無 | B | https://www.eheya.net/detail/300000832004398000003/ |
| 2.33 | ライオンズマンション一条智恵光院 | 2LDK | 59.4 | 100,000 | 10000 | 100,000円 / 100,000円 | 1.0 | 2/6 | Y | 1989/5 | RC | 無 | old | https://www.eheya.net/detail/300000832004360000004/ |
| 2.4 | 大晋メゾネ西陣今出川 | 2SLDK | 65.55 | 125,000 | 9000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/10 | Y | 1998/3 | その他 | 無 | B | https://www.eheya.net/detail/300000832008940000002/ |
| 2.4 | 大晋メゾネ西陣今出川 | 3LDK | 74.81 | 130,000 | 9000 | 1ヶ月 / 1ヶ月 | 1.0 | 5/10 | Y | 1998/3 | その他 | 無 | B | https://www.eheya.net/detail/300000832008940000003/ |
| 2.6 | ポルト ボヌール | 2LDK | 48.97 | 105,000 | 6900 | 0円 / 1ヶ月 | 1.0 | 4/5 | Y | 2016/3 | RC | 無 | A | https://www.eheya.net/detail/300000830000617005256/ |
| 2.6 | ポルト ボヌール | 2LDK | 48.97 | 105,000 | 6900 | 0円 / 1ヶ月 | 1.0 | 3/5 | Y | 2016/3 | RC | 無 | A | https://www.eheya.net/detail/300000830000617005253/ |
| 2.77 | D-ROOM 一乗寺 | 2LDK | 52.79 | 136,000 | 8000 | 0円 / 136,000円 | 1.0 | 2/3 | n | 2024/10 | 軽量鉄骨 | 有 月14,300円(税込) | A | https://www.eheya.net/detail/300000832007379000009/ |
| 2.89 | カーサ葵 | 3LDK | 68.14 | 140,000 | 10000 | 1ヶ月 / 1ヶ月 | 1.0 | 3/3 | Y | 2001/3 | RC | 無 | A | https://www.eheya.net/detail/300000832006010000004/ |
| 3.11 | D-ROOM Sagarimatsu | 2LDK | 56.43 | 125,000 | 7000 | 0円 / 0円 | 0.0 | 2/2 | n | 2025/10 | 軽量鉄骨 | 有 月13,200円(税込) | A | https://www.eheya.net/detail/300000832008073000003/ |
| 3.13 | 京都グランデ二条駅南 | 2LDK | 48.07 | 133,000 | 0 | 0円 / 50,000円 | 0.38 | 2/3 | n | 2023/6 | 木造 | 無 | A | https://www.eheya.net/detail/300000832009393000001/ |
