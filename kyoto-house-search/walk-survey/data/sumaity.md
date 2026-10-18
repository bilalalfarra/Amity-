# sumaity — スマイティ (sumaity.com), WALK survey (≤1.3 km of 京都技術科学センター, 左京区吉田河原町14), fetched 2026-10-18

## Method
- Server-side filters (https://sumaity.com/chintai/area_list/list.php): acity_id = ward, madori[] = 2LDK/3DK/3LDK/4DK/4LDK以上, foot_print_low=45. **No rent cap**; no 礼金 / age / floor / elevator rules (none applied anywhere).
- Wards (site room counts): sakyo 663, kamigyo 482, nakagyo 786 → 44 list pages, 1916 unique room listings (raw: out/raw/sumaity/list_<ward>_p<N>.html).
- List-stage funnel: total 1916, station walk ⇒ > 1.3 km 1093, far (> 1.8 km town-level) 137, candidates 501, far (station approx) 178, geocode contradicts station (kept) 37, no location 7. List-stage distance is town-level (sumaity hides block numbers; Kyoto 通り名 addresses reduced to ward+町名 by kgeo.py) so the cut there was lenient (1.8 km); every geocode was also checked against the listed 駅徒歩N分 (≤ N×80 m from the station): impossible ones dropped, contradicting geocodes not trusted.
- All 508 candidate unit pages fetched (raw: out/raw/sumaity/detail/; HTTP all 200 (fetched earlier in this session and cached)). Final distance: the unit page's own lat/lng when published (exact) → keep ≤ 1.3 km; otherwise town-level GSI geocode → keep ≤ 1.5 km (flagged in notes, ±300 m). Detail-stage drops: {'> 1.3 km (site coords)': 176, '> 1.5 km (town-level)': 16}.
- Caveats: sumaity aggregates several agencies; the same room can appear under several prop IDs (merged by post.py on town+floor+area+built+floors; other URLs in `notes`). 仲介手数料/保証会社 are often 'ask the agency'. Nameless buildings show the station text as the name.
- Station plausibility check (geofix.py; Kyoto town names repeat, GSI returns one): {'checked': 124, 'no_station': 0, 'inconsistent_moved': 1, 'dropped_lower_bound': 25, 'roughly_consistent_kept': 3}; dropped (cannot be ≤1.3 km given the listed 駅徒歩): 25 → out/sumaity_geodropped.json.

## Result
- **Kept 176 units** (after merging 115 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 17 located via the same building name in another listing with a full address, 39 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 101; rent range kept: 87000–498000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'A': 93, 'house': 43, 'B': 8, 'old': 32}; 礼金 ≤1ヶ月 87, >1ヶ月 89, unknown 0 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'site': 102, 'town': 36, 'site (same building, other listing)': 6, 'station': 32} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 94/82/0; by ward: {'左京区': 66, '上京区': 80, '中京区': 30}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/sumaity/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.05 | エル・パークスクエア京都鴨川 | 3LDK | 96.68 | 315,000 | 15000 | 31.5万円(-) / 63万円 | 2.0 | 7/7 | Y | 2005/1 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413838190/ |
| 0.12 | 京阪鴨東線出町柳駅まで徒歩10分 | 3LDK | 66.7 | 120,000 | 0 | 0円(-) / 24万円 | 2.0 | 1/2 | n | 2004/12 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_411268278/ |
| 0.13 | 京阪鴨東線出町柳駅まで徒歩11分 | 2LDK | 66.7 | 120,000 | 0 | 0円(-) / 24万円 | 2.0 | None/2 | n | 2004/12 | 木造 | 近隣　18000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_411186002/ |
| 0.16 | 京阪鴨東線神宮丸太町駅まで徒歩6分 | 3DK | 54.67 | 100,000 | 0 | 1ヶ月(-) / 2ヶ月 | 2.0 | 1/2 | n | 1984/11 | 木造 | 近隣　18000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_412197276/ |
| 0.18 | 京阪鴨東線神宮丸太町駅まで徒歩8分 | 3DK | 65.0 | 100,000 | 0 | 10万円(-) / 20万円 | 2.0 | None/3 | n | 1984/11 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_412221194/ |
| 0.18 | 京阪鴨東線出町柳駅まで徒歩8分 | 3LDK | 65.77 | 138,000 | 10000 | 20万円(-) / 35万円 | 2.54 | 5/5 | Y | 1997/3 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_412822240/ |
| 0.32 | 京阪鴨東線出町柳駅まで徒歩7分 | 3DK | 59.2 | 95,000 | 0 | 9.5万円(-) / 15万円 | 1.58 | 2/2 | n | 1954/11 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413939708/ |
| 0.34 | エスタプレイス | 2LDK | 73.03 | 216,000 | 7500 | 0円(-) / 1ヶ月 | 1.0 | 4/6 | Y | 2027/4 | RC | 空有　22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_410055918/ |
| 0.34 | エスタプレイス | 2LDK | 73.03 | 216,000 | 7500 | 0円(-) / 1ヶ月 | 1.0 | 3/6 | Y | 2027/4 | RC | 空有　22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_410055528/ |
| 0.34 | エスタプレイス | 2LDK | 68.55 | 207,000 | 7500 | 0円(-) / 1ヶ月 | 1.0 | 3/6 | Y | 2027/4 | RC | 空有　22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_409946780/ |
| 0.34 | エスタプレイス | 2LDK | 73.03 | 215,000 | 7500 | 0円(-) / 1ヶ月 | 1.0 | 2/6 | Y | 2027/4 | RC | 空有　22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_410055412/ |
| 0.34 | エスタプレイス | 2LDK | 68.55 | 206,000 | 7500 | 0円(-) / 1ヶ月 | 1.0 | 2/6 | Y | 2027/4 | RC | 空有　22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_409946602/ |
| 0.34 | 京阪鴨東線出町柳駅まで徒歩8分 | 5DK | 93.54 | 200,000 | 0 | 30万円(-) / 30万円 | 1.5 | 1/2 | n | 1970/4 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_414701288/ |
| 0.34 | 京阪鴨東線出町柳駅まで徒歩6分 | 3LDK | 101.65 | 250,000 | 0 | 25万円(-) / 37.5万円 | 1.5 | 1/2 | n | 2019/2 | 木造 | 付無料 | house | https://sumaity.com/chintai/kyoto_prop/prop_413347014/ |
| 0.41 | 京阪鴨東線出町柳駅まで徒歩9分 | 5DK | 93.54 | 200,000 | 0 | 30万円(-) / 30万円 | 1.5 | None/2 | n | 1997/2 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_408789976/ |
| 0.41 | 京阪鴨東線出町柳駅まで徒歩9分 | 5DK | 60.0 | 180,000 | 0 | 30万円(-) / 30万円 | 1.67 | None/2 | n | 1950/1 | 木造 | 付無料 | house | https://sumaity.com/chintai/kyoto_prop/prop_414556918/ |
| 0.44 | THE RESIDENCE御車道 | 2LDK | 59.7 | 192,000 | 10000 | 1ヶ月(-) / 20万円 | 1.04 | 2/4 | Y | 2026/8 | RC | 近隣　19800円 | A | https://sumaity.com/chintai/kyoto_prop/prop_410667328/ |
| 0.44 | THE RESIDENCE御車道 | 2LDK | 68.58 | 205,000 | 10000 | 1ヶ月(-) / 25万円 | 1.22 | 1/4 | Y | 2026/8 | RC | 近隣　19800円 | A | https://sumaity.com/chintai/kyoto_prop/prop_410667298/ |
| 0.44 | THE RESIDENCE御車道 | 2LDK | 59.7 | 179,000 | 10000 | 1ヶ月(-) / 20万円 | 1.12 | 1/4 | Y | 2026/8 | RC | 近隣　19800円 | A | https://sumaity.com/chintai/kyoto_prop/prop_410667406/ |
| 0.44 | GRANDE′TERNA京大正門前 | 2LDK | 64.2 | 160,500 | 9000 | 0円(-) / 32.1万円 | 2.0 | 2/5 | Y | 2008/9 | RC | 敷地内24258円 | A | https://sumaity.com/chintai/kyoto_prop/prop_410187346/ |
| 0.45 | Grand E′terna 京大正門前 | 3LDK | 71.07 | 169,500 | 9000 | 0円(-) / 33.9万円 | 2.0 | 2/5 | Y | 2008/10 | RC | 空有　23100円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414425106/ |
| 0.46 | 京阪鴨東線神宮丸太町駅まで徒歩8分 | 2LDK | 104.01 | 465,000 | 0 | 46.5万円(-) / 93万円 | 2.0 | 5/5 | Y | 2017/6 | RC | 敷地内25000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414873266/ |
| 0.49 | 京阪鴨東線神宮丸太町駅まで徒歩12分 | 2LDK | 61.69 | 179,000 | 6000 | 0円(-) / 0円 | 0.0 | 2/2 | n | 2025/9 | 木造 | 敷地内20000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411161328/ |
| 0.49 | BelleLead御所東 | 2LDK | 53.0 | 159,000 | 6000 | 0円(-) / 0円 | 0.0 | 1/2 | n | 2025/9 | 木造 | 敷地内20000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411162016/ |
| 0.49 | ノーベルテラス稔 | 2LDK | 57.76 | 220,000 | 8000 | 1ヶ月(-) / 2ヶ月 | 2.0 | 4/5 | Y | 2003/3 | 鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_412583350/ |
| 0.5 | Grand | 2LDK | 64.2 | 160,500 | 9000 | 0円(-) / 32.1万円 | 2.0 | 2/6 | Y | 2008/9 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_410535312/ |
| 0.5 | BelleLead御所東 | 2LDK | 61.69 | 174,000 | 6000 | 0円(-) / 17.4万円 | 1.0 | 1/2 | n | 2025/9 | 木造 | 空有　22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411124904/ |
| 0.52 | 京阪鴨東線出町柳駅まで徒歩6分 | 2LDK | 68.58 | 208,000 | 10000 | 20.8万円(-) / 20万円 | 0.96 | 2/4 | Y | 2026/7 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413653384/ |
| 0.58 | FORESTA御所東 | 2LDK | 61.49 | 200,000 | 11500 | 0円(-) / 0円 | 0.0 | 1/3 | n | 2026/5 | 軽量鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_411849048/ |
| 0.59 | ベリエ茶五 | 2LDK | 60.25 | 190,000 | 17000 | 0円(-) / 2ヶ月 | 2.0 | 6/6 | Y | 2008/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_407125806/ |
| 0.59 | ベリエ茶五 | 2LDK | 60.25 | 165,000 | 16000 | 0円(-) / 2ヶ月 | 2.0 | 5/6 | Y | 2008/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_410927234/ |
| 0.59 | ベリエ茶五 | 2LDK | 60.25 | 160,000 | 15000 | 0円(-) / 2ヶ月 | 2.0 | 4/6 | Y | 2008/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_412891462/ |
| 0.59 | ベリエ茶五 | 2LDK | 54.72 | 150,000 | 15000 | 0円(-) / 2ヶ月 | 2.0 | 3/6 | Y | 2008/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_410555296/ |
| 0.59 | ベリエ茶五 | 2LDK | 53.96 | 145,000 | 15000 | 0円(-) / 1.5ヶ月 | 1.5 | 2/6 | Y | 2008/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_410927222/ |
| 0.59 | ベリエ茶五 | 2LDK | 60.25 | 155,000 | 15000 | 0円(-) / 2ヶ月 | 2.0 | 2/6 | Y | 2008/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_411478224/ |
| 0.6 | 京阪鴨東線出町柳駅まで徒歩4分 | 3DK | 81.27 | 200,000 | 0 | 40万円(-) / 60万円 | 3.0 | None/3 | n | 1986/9 | 鉄骨 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413158950/ |
| 0.6 | 京阪鴨東線出町柳駅まで徒歩23分 | 4SLDK | 145.0 | 230,000 | 0 | 30万円(-) / 40万円 | 1.74 | None/3 | n | 1992/3 | 鉄骨 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_411601500/ |
| 0.6 | 京阪鴨東線神宮丸太町駅まで徒歩8分 | 3DK | 65.0 | 100,000 | 0 | 10万円(-) / 20万円 | 2.0 | None/2 | n | 1984/11 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_406678310/ |
| 0.6 | ファインフラッツ京都神宮 | 2LDK | 54.25 | 185,000 | 15000 | 18.5万円(-) / 18.5万円 | 1.0 | 2/5 | Y | 2013/11 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413817498/ |
| 0.6 | 黒谷町303 | 2LDK | 98.36 | 150,000 | 0 | 15万円(-) / 30万円 | 2.0 | 3/4 | n | 1987/9 | 鉄骨 | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414491530/ |
| 0.61 | ピアハウス出町 | 4LDK | 145.42 | 280,000 | 0 | 0円(-) / 0円 | 0.0 | 2/3 | n | 1998/11 | 鉄骨 | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_407274502/ |
| 0.61 | ピアハウス出町 | 4LDK | 145.42 | 280,000 | 0 | 28万円(-) / 56万円 | 2.0 | 1/3 | n | 1998/11 | 鉄骨 | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_405173206/ |
| 0.61 | 鴨川グランドコーポ | 2LDK | 95.22 | 470,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 4/5 | Y | 1981/5 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_411065224/ |
| 0.62 | エスタプレイス | 2LDK | 68.55 | 208,000 | 7500 | 0円(-) / 20.8万円 | 1.0 | 5/6 | Y | 2027/3 | RC | 敷地内22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_410001616/ |
| 0.62 | 地下鉄東西線京都市役所前駅まで徒歩12分 | 2LDK | 48.6 | 95,000 | 7000 | 9.5万円(-) / 10万円 | 1.05 | 2/3 | n | 1988/9 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414227120/ |
| 0.62 | エスタプレイス | 2LDK | 75.03 | 216,000 | 7500 | 0円(-) / 21.6万円 | 1.0 | 4/6 | Y | 2027/4 | RC | 空有　22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_410018220/ |
| 0.62 | エスタプレイス | 2LDK | 75.03 | 216,000 | 7500 | 0円(-) / 21.6万円 | 1.0 | 3/6 | Y | 2027/4 | RC | 空有　22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_410018114/ |
| 0.62 | エスタプレイス | 2LDK | 75.03 | 215,000 | 7500 | 0円(-) / 21.5万円 | 1.0 | 2/6 | Y | 2027/4 | RC | 空有　22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_410018086/ |
| 0.63 | 鴨川グランドコーポ | 3LDK | 78.67 | 235,000 | 15000 | 23.5万円(-) / 23.5万円 | 1.0 | 1/5 | Y | 1981/5 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_409837960/ |
| 0.64 | アルス丸太町山水庵 | 3SLDK | 117.57 | 280,000 | 17000 | 28万円(-) / 56万円 | 2.0 | 5/6 | Y | 2002/3 | RC | 敷地内20000円/機械式駐 | A | https://sumaity.com/chintai/kyoto_prop/prop_409555220/ |
| 0.65 | レジディア御所東 | 3LDK | 113.88 | 402,000 | 18000 | 1ヶ月(-) / 0円 | 0.0 | 9/10 | Y | 2007/9 | RC | - | A | https://sumaity.com/chintai/kyoto_prop/prop_413517900/ |
| 0.66 | 京阪鴨東線神宮丸太町駅まで徒歩7分 | 3LDK | 113.88 | 402,000 | 18000 | 40.2万円(-) / 40.2万円 | 1.0 | 2/10 | Y | 2007/9 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_412982392/ |
| 0.66 | 京阪鴨東線神宮丸太町駅まで徒歩3分 | 3LDK | 78.04 | 215,000 | 10000 | 21.5万円(-) / 21.5万円 | 1.0 | 6/6 | Y | 2003/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_412322564/ |
| 0.67 | 京阪鴨東線神宮丸太町駅まで徒歩4分 | 4DK | 111.94 | 168,000 | 0 | 15万円(-) / 20万円 | 1.19 | None/3 | n | 1994/2 | 木造 | 付無料/駐2台可 | house | https://sumaity.com/chintai/kyoto_prop/prop_414292068/ |
| 0.67 | 京阪鴨東線神宮丸太町駅まで徒歩7分 | 2LDK | 53.94 | 138,000 | 10000 | 0円(-) / 13.8万円 | 1.0 | 2/3 | n | 1987/2 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_413242322/ |
| 0.67 | 京阪鴨東線神宮丸太町駅まで徒歩7分 | 2LDK | 53.94 | 136,000 | 10000 | 0円(-) / 13.6万円 | 1.0 | 1/3 | n | 1987/2 | RC | 敷地内25000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_398820224/ |
| 0.67 | イーグルコート聖護院 | 3LDK | 78.04 | 215,000 | 10000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 6/7 | Y | 2003/2 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_405324278/ |
| 0.7 | 京阪鴨東線出町柳駅まで徒歩7分 | 4LDK | 65.71 | 135,000 | 0 | 0円(-) / 0円 | 0.0 | 1/2 | n | 1994/4 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_411952958/ |
| 0.7 | 京阪鴨東線神宮丸太町駅まで徒歩11分 | 5DK | 103.68 | 250,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 2/2 | n | 1987/1 | 木造 | 近隣　16000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_413775966/ |
| 0.7 | 京阪鴨東線出町柳駅まで徒歩8分 | 7SLDK | 156.91 | 220,000 | 0 | 22万円(-) / 22万円 | 1.0 | None/3 | n | 1982/2 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_412225330/ |
| 0.7 | 京阪鴨東線出町柳駅まで徒歩5分 | 4LDK | 145.42 | 280,000 | 0 | 28万円(-) / 56万円 | 2.0 | None/3 | n | 1998/11 | 鉄骨 | 空無 | house | https://sumaity.com/chintai/kyoto_prop/prop_405247112/ |
| 0.7 | T′s スクエア下鴨 | 3LDK | 63.85 | 183,000 | 8500 | 0円(-) / 0円 | 0.0 | 1/2 | n | 2021/3 | 軽量鉄骨 | 空有　19800円 | A | https://sumaity.com/chintai/kyoto_prop/prop_413720646/ |
| 0.71 | （仮）D-room上京区米屋町ハイツ | 2LDK | 62.73 | 212,000 | 12000 | 0円(-) / 25万円 | 1.18 | 3/3 | n | 2026/11 | 軽量鉄骨 | 敷地内33000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_412525250/ |
| 0.71 | （仮）D-room上京区米屋町ハイツ | 2LDK | 60.19 | 210,000 | 12000 | 0円(-) / 25万円 | 1.19 | 3/3 | n | 2026/11 | 軽量鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414872644/ |
| 0.71 | （仮）D-room上京区米屋町ハイツ | 2LDK | 62.73 | 210,000 | 12000 | 0円(-) / 25万円 | 1.19 | 2/3 | n | 2026/11 | 軽量鉄骨 | 敷地内33000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_412376050/ |
| 0.71 | （仮）D-room上京区米屋町ハイツ | 2LDK | 60.19 | 208,000 | 12000 | 0円(-) / 25万円 | 1.2 | 2/3 | n | 2026/11 | 軽量鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414872676/ |
| 0.71 | （仮）D-room上京区米屋町ハイツ | 2LDK | 62.73 | 207,000 | 12000 | 0円(-) / 25万円 | 1.21 | 1/3 | n | 2026/11 | 軽量鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414872568/ |
| 0.71 | （仮）D-room上京区米屋町ハイツ | 2LDK | 60.19 | 204,000 | 12000 | 0円(-) / 25万円 | 1.23 | 1/3 | n | 2026/11 | 軽量鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414873226/ |
| 0.71 | アルス丸太町山水庵 | 3LDK | 117.57 | 280,000 | 17100 | 1ヶ月(-) / 2ヶ月 | 2.0 | 3/5 | Y | 2002/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_412952374/ |
| 0.72 | 京阪鴨東線神宮丸太町駅まで徒歩4分 | 3LDK | 81.05 | 215,000 | 10000 | 21.5万円(-) / 21.5万円 | 1.0 | 6/7 | Y | 2003/10 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_405389666/ |
| 0.72 | 京阪鴨東線出町柳駅まで徒歩5分 | 2LDK | 45.08 | 100,000 | 0 | 10万円(-) / 20万円 | 2.0 | 2/2 | n | 1970/11 | 木造 | 近隣　18000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_413106128/ |
| 0.75 | サンアートビル | 3LDK | 59.41 | 130,000 | 8000 | 0円(-) / 0円 | 0.0 | 5/6 | Y | 1981/12 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_409656178/ |
| 0.75 | サンアートビル | 3LDK | 80.4 | 130,000 | 8000 | 0円(-) / 0円 | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 | 近隣　30000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_410851644/ |
| 0.75 | サンアートビル | 3LDK | 59.14 | 130,000 | 8000 | 0円(-) / 0円 | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_351584776/ |
| 0.77 | 京阪鴨東線出町柳駅まで徒歩17分 | 4LDK | 123.8 | 160,000 | 0 | 32万円(-) / 16万円 | 1.0 | None/2 | n | 1982/10 | 軽量鉄骨 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_375225910/ |
| 0.77 | 京阪鴨東線神宮丸太町駅まで徒歩7分 | 2LDK | 94.4 | 190,000 | 4000 | 19万円(-) / 19万円 | 1.0 | 4/4 | n | 1977/10 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_404843414/ |
| 0.77 | シャリエ聖護院西町 | 4LDK | 100.77 | 295,000 | 33000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 5/5 | Y | 2013/1 | RC | 近隣　16000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_413258662/ |
| 0.78 | 京阪鴨東線神宮丸太町駅まで徒歩4分 | 3SLDK | 90.0 | 135,000 | 0 | 0円(-) / 13.5万円 | 1.0 | None/2 | n | 1950/4 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414616330/ |
| 0.78 | 京阪鴨東線神宮丸太町駅まで徒歩3分 | 3LDK | 90.0 | 135,000 | 0 | 0円(-) / 1ヶ月 | 1.0 | 2/2 | n | 1950/5 | 木造 | 近隣　20000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_412197272/ |
| 0.8 | ドムス鴨川 | 4LDK | 162.38 | 370,000 | 20000 | 20万円(-) / 50万円 | 1.35 | 3/3 | Y | 1989/12 | RC | 空有　28600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_392095218/ |
| 0.8 | ドムス鴨川 | 3LDK | 129.59 | 250,000 | 20000 | 20万円(-) / 50万円 | 2.0 | 1/3 | Y | 1989/12 | RC | 空有　28600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_383740888/ |
| 0.8 | 吉田近衛町19-6 | 2LDK | 48.0 | 120,000 | 0 | 12万円(-) / 24万円 | 2.0 | 2/2 | n | 1993/10 | 木造 | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_408373890/ |
| 0.8 | 吉田中大路町アパート | 2LDK | 49.66 | 87,000 | 3000 | 0円(-) / 0円 | 0.0 | 1/2 | n | 2002/7 | 木造 | 近隣　19800円 | A | https://sumaity.com/chintai/kyoto_prop/prop_330702150/ |
| 0.84 | 京阪鴨東線神宮丸太町駅まで徒歩8分 | 2LDK | 66.0 | 168,000 | 14030 | 0円(-) / 20万円 | 1.19 | 3/5 | Y | 2018/10 | RC | 敷地内22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_413623568/ |
| 0.86 | リーガル京都聖護院 | 2LDK | 66.0 | 163,000 | 14030 | 0円(-) / 1ヶ月 | 1.0 | 1/5 | Y | 2018/10 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413770652/ |
| 0.86 | BRIGH STONE御所北 | 2LDK | 52.01 | 174,000 | 10000 | 1ヶ月(-) / 2ヶ月 | 2.0 | 1/3 | Y | 2024/10 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_375136004/ |
| 0.87 | 京阪鴨東線神宮丸太町駅まで徒歩15分 | 4LDK | 92.3 | 150,000 | 0 | 15万円(-) / 30万円 | 2.0 | 1/2 | n | 1970/1 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413294960/ |
| 0.87 | 京阪鴨東線出町柳駅まで徒歩18分 | 3SLDK | 94.92 | 230,000 | 0 | 23万円(-) / 46万円 | 2.0 | 1/2 | n | 2016/1 | 木造 | 付無料 | house | https://sumaity.com/chintai/kyoto_prop/prop_412998564/ |
| 0.87 | 京阪鴨東線出町柳駅まで徒歩17分 | 3SLDK | 94.92 | 230,000 | 0 | 23万円(-) / 46万円 | 2.0 | None/2 | n | 2016/2 | 木造 | 付無料 | house | https://sumaity.com/chintai/kyoto_prop/prop_404030782/ |
| 0.88 | 京阪鴨東線神宮丸太町駅まで徒歩16分 | 3LDK | 50.34 | 150,000 | 0 | 1ヶ月(-) / 2ヶ月 | 2.0 | None/2 | n | 1964/4 | 木造 | 近隣　16000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_414301296/ |
| 0.9 | 京阪鴨東線神宮丸太町駅まで徒歩13分 | 2LDK | 54.56 | 124,000 | 12000 | 0円(-) / 5万円 | 0.4 | 1/3 | n | 2018/12 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414598536/ |
| 0.91 | 京阪鴨東線出町柳駅まで徒歩17分 | 2LDK | 49.27 | 200,000 | 0 | 20万円(-) / 40万円 | 2.0 | 1/2 | n | 2025/10 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413979642/ |
| 0.92 | リソシエ鴨川グランディス | 3LDK | 78.04 | 190,000 | 0 | 19万円(-) / 38万円 | 2.0 | 3/7 | Y | 2000/10 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_413877792/ |
| 0.92 | ザ・パークハウス京都聖護院 | 2LDK | 58.45 | 250,000 | 0 | 25万円(-) / 50万円 | 2.0 | 1/5 | Y | 2026/8 | その他 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414722792/ |
| 0.94 | シャルト北苑 | 4LDK | 69.03 | 135,000 | 10000 | 1ヶ月(-) / 0円 | 0.0 | 3/3 | n | 1984/1 | RC | 近隣　15000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_409165206/ |
| 0.94 | シャルト北苑 | 3LDK | 71.72 | 145,000 | 10000 | 1ヶ月(-) / 0円 | 0.0 | 2/3 | n | 1984/1 | RC | 近隣　15000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_408973034/ |
| 0.94 | シャルト北苑 | 3LDK | 69.03 | 140,000 | 10000 | 2ヶ月(-) / 1ヶ月 | 1.0 | 1/3 | n | 1984/1 | RC | 近隣　15000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_395604664/ |
| 0.95 | デ・リード府庁前 | 2LDK | 61.08 | 148,000 | 0 | 20万円(-) / 30万円 | 2.03 | 2/8 | Y | 1990/10 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414699834/ |
| 0.98 | ベレヴュー聖護院 | 3LDK | 65.28 | 150,000 | 0 | 15万円(-) / 15万円 | 1.0 | 6/7 | Y | 1994/12 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_412124948/ |
| 0.99 | 京阪鴨東線出町柳駅まで徒歩9分 | 5LDK | 153.83 | 250,000 | 0 | 2ヶ月(-) / 1ヶ月 | 1.0 | 1/2 | n | 1990/6 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_414502282/ |
| 1.0 | ザ・京都レジデンス御所南 | 2LDK | 56.13 | 210,000 | 10000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 2/5 | Y | 2016/12 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_411580920/ |
| 1.01 | 烏丸線今出川駅まで徒歩13分 | 6SLDK | 93.19 | 220,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 1/3 | n | 1982/2 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_414701260/ |
| 1.01 | 京阪鴨東線神宮丸太町駅まで徒歩12分 | 3LDK | 73.75 | 210,000 | 20000 | 1ヶ月(-) / 2ヶ月 | 2.0 | 1/3 | Y | 2017/1 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_400756450/ |
| 1.02 | かぐら坂荘 | 2LDK | 60.23 | 127,000 | 7000 | 0円(-) / 12.7万円 | 1.0 | 3/3 | n | 2011/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_408351658/ |
| 1.03 | 京都グランドハイツ | 2LDK | 64.5 | 140,000 | 10000 | 14万円(-) / 14万円 | 1.0 | 4/7 | Y | 1971/6 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414227714/ |
| 1.04 | 京阪鴨東線神宮丸太町駅まで徒歩20分 | 3SLDK | 114.18 | 498,000 | 0 | 49.8万円(-) / 49.8万円 | 1.0 | None/2 | n | 1926/1 | 木造 | 付無料 | house | https://sumaity.com/chintai/kyoto_prop/prop_409429372/ |
| 1.06 | サンシティ御所南 | 3LDK | 89.44 | 260,000 | 10000 | 26万円(-) / 52万円 | 2.0 | 3/3 | Y | 2006/3 | RC | 空有　33000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_345845768/ |
| 1.06 | CALM河原町二条 | 2LDK | 61.12 | 198,000 | 10000 | 19.8万円(-) / 39.6万円 | 2.0 | 4/7 | Y | 2026/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_412753276/ |
| 1.06 | イスターナイマイ鴨川西 | 2LDK | 50.65 | 153,000 | 9000 | 0円(-) / 20万円 | 1.31 | 5/5 | Y | 2013/2 | RC | 近隣200m46095円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411581020/ |
| 1.06 | イスターナイマイ鴨川西 | 2LDK | 50.65 | 150,000 | 9000 | 0円(-) / 20万円 | 1.33 | 3/5 | Y | 2013/2 | RC | 近隣200m46095円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411580682/ |
| 1.06 | 京阪鴨東線神宮丸太町駅まで徒歩18分 | 3DK | 69.35 | 90,000 | 0 | 9万円(-) / 9万円 | 1.0 | 1/1 | n | 2001/8 | 木造 | 近隣　16000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_400486690/ |
| 1.07 | 京阪鴨東線出町柳駅まで徒歩15分 | 5SDK | 138.54 | 330,000 | 0 | 33万円(-) / 33万円 | 1.0 | 1/2 | n | 1930/1 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_397911632/ |
| 1.08 | 吉田本町洋風外観京町家 | 5DK | 138.54 | 330,000 | 0 | 33万円(-) / 33万円 | 1.0 | None/2 | n | 1930/1 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_392701808/ |
| 1.09 | グレーシー北白川 | 3LDK | 68.39 | 130,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 3/3 | n | 1991/8 | RC | - | B | https://sumaity.com/chintai/kyoto_prop/prop_405890208/ |
| 1.1 | 地下鉄東西線京都市役所前駅まで徒歩5分 | 2LDK | 61.12 | 198,000 | 10000 | 19.8万円(-) / 19.8万円 | 1.0 | 5/7 | Y | 2026/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413654000/ |
| 1.1 | 地下鉄東西線京都市役所前駅まで徒歩5分 | 2LDK | 61.12 | 195,000 | 10000 | 19.5万円(-) / 19.5万円 | 1.0 | 2/7 | Y | 2026/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414598646/ |
| 1.1 | ジオ河原町二条 | 3LDK | 74.39 | 220,000 | 0 | 22万円(-) / 44万円 | 2.0 | 7/7 | Y | 2011/7 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_330901166/ |
| 1.12 | 京阪鴨東線神宮丸太町駅まで徒歩18分 | 3SLDK | 107.96 | 135,000 | 0 | 0円(-) / 0円 | 0.0 | 1/3 | n | 1995/4 | 木造 | 付無料 | house | https://sumaity.com/chintai/kyoto_prop/prop_409567420/ |
| 1.13 | エルミタージュ下鴨東 | 2LDK | 55.43 | 125,000 | 8500 | 0円(-) / 0円 | 0.0 | 2/2 | n | 2024/7 | 軽量鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414381988/ |
| 1.15 | グランタック東山二条 | 2LDK | 56.0 | 130,000 | 8000 | 1ヶ月(-) / 0円 | 0.0 | 5/6 | Y | 1977/1 | RC | 近隣　20000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_410952538/ |
| 1.17 | ＫＢ．メゾンロータス | 2LDK | 51.17 | 121,000 | 4600 | 0円(-) / 1ヶ月 | 1.0 | 1/3 | n | 2011/3 | 鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_296610199/ |
| 1.17 | 叡電元田中駅まで徒歩4分 | 6DK | 145.36 | 150,000 | 0 | 1ヶ月(-) / 2ヶ月 | 2.0 | None/4 | n | 1976/8 | 鉄骨 | 近隣　16500円 | house | https://sumaity.com/chintai/kyoto_prop/prop_414624060/ |
| 1.18 | ヴィークコート京都河原町二条 | 3LDK | 75.13 | 380,000 | 0 | 1ヶ月(-) / 2ヶ月 | 2.0 | 7/7 | Y | 2023/8 | RC | 近隣　25000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_412197026/ |
| 1.18 | ヴィークコート京都河原町二条 | 3LDK | 88.21 | 430,000 | 0 | 1ヶ月(-) / 2ヶ月 | 2.0 | 3/7 | Y | 2023/8 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_402276918/ |
| 1.18 | 京阪鴨東線神宮丸太町駅まで徒歩14分 | 3LDK | 72.57 | 168,000 | 12000 | 0円(-) / 20万円 | 1.19 | 3/5 | Y | 2001/6 | RC | 空有　27500円 | A | https://sumaity.com/chintai/kyoto_prop/prop_408772326/ |
| 1.18 | 叡山電鉄叡山本線元田中駅まで徒歩5分 | 6DK | 145.36 | 150,000 | 0 | 30万円(-) / 15万円 | 1.0 | 1/4 | n | 1976/8 | 鉄骨 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414734794/ |
| 1.18 | メゾンフジ | 3DK | 80.0 | 135,000 | 5000 | 0円(-) / 0円 | 0.0 | 2/5 | n | 1985/10 | 鉄骨 | 近隣　20000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_406033418/ |
| 1.21 | ベルリード MILLESIME寺町 | 2LDK | 69.97 | 230,000 | 10000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 2/3 | n | 2026/11 | 木造 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_410417726/ |
| 1.21 | 叡山電鉄叡山本線元田中駅まで徒歩6分 | 5DK | 63.66 | 88,000 | 0 | 8.8万円(-) / 10万円 | 1.14 | 1/2 | n | 1988/8 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_412481246/ |
| 1.22 | 地下鉄東西線京都市役所前駅まで徒歩4分 | 2LDK | 66.49 | 240,000 | 0 | 0円(-) / 48万円 | 2.0 | 5/7 | Y | 2013/9 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414099660/ |
| 1.23 | ジオ御所南河原町二条 | 2LDK | 73.46 | 230,000 | 20000 | 25万円(-) / 37.5万円 | 1.63 | 4/7 | Y | 2013/9 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413489716/ |
| 1.23 | 山和小路 | 3LDK | 66.97 | 125,000 | 10000 | 0円(-) / 1ヶ月 | 1.0 | 5/5 | Y | 1999/11 | RC | 空有　23100円 | B | https://sumaity.com/chintai/kyoto_prop/prop_413282120/ |
| 1.25 | ベルフォーレ御所南 | 2LDK | 60.04 | 198,000 | 12000 | 19.8万円(-) / 39.6万円 | 2.0 | 3/3 | Y | 2023/9 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413199462/ |
| 1.25 | 地下鉄烏丸線丸太町駅まで徒歩9分 | 2LDK | 76.29 | 270,000 | 20000 | 0円(-) / 54万円 | 2.0 | 4/5 | Y | 2026/4 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_404122054/ |
| 1.27 | 地下鉄東西線京都市役所前駅まで徒歩9分 | 2LDK | 73.82 | 210,000 | 0 | 21万円(-) / 21万円 | 1.0 | 1/2 | n | 1970/5 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_410797328/ |
| 1.27 | アルカンシエル御所 | 2LDK | 57.17 | 144,000 | 10000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 3/6 | Y | 1987/3 | RC | 近隣　25000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_414665070/ |
| 1.28 | 地下鉄烏丸線丸太町駅まで徒歩5分 | 2LDK | 48.51 | 100,000 | 9000 | 1万円(-) / 1万円 | 0.1 | 2/4 | Y | 1985/7 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414808248/ |
| 1.3 | 北白川コーポラス | 3LDK | 66.0 | 100,000 | 8000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 3/5 | n | 1988/3 | RC | 空有　8000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_412630416/ |
| 1.31 | フロンテージ堺町御門 | 2LDK | 68.44 | 225,000 | 9000 | 5万円(-) / 45万円 | 2.0 | 2/3 | Y | 2023/3 | 鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_410849900/ |
| 1.36 | くわでん | 3LDK | 77.02 | 250,000 | 13000 | 0円(-) / 1ヶ月 | 1.0 | 2/2 | n | 2012/9 | 鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_412562150/ |
| 1.36 | コモド御所南 | 2LDK | 58.88 | 150,000 | 13000 | 0円(-) / 20万円 | 1.33 | 3/5 | Y | 2007/10 | RC | 空有　30000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_409533712/ |
| 1.36 | コモド御所南 | 2LDK | 58.88 | 141,000 | 13000 | 1ヶ月(-) / 20万円 | 1.42 | 2/5 | Y | 2007/10 | RC | 空有　30000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414621790/ |
| 1.36 | パーシモン御所南 | 3LDK | 110.12 | 435,000 | 10000 | 1ヶ月(-) / 2ヶ月 | 2.0 | 2/5 | Y | 2024/4 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_380173792/ |
| 1.37 | エリシア御所南 | 2LDK | 67.84 | 285,000 | 15000 | 5万円(-) / 60万円 | 2.11 | 2/4 | Y | 2027/1 | 鉄骨 | 空有　44000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_408838030/ |
| 1.37 | エリシア御所南 | 2LDK | 68.7 | 260,000 | 15000 | 5万円(-) / 60万円 | 2.31 | 1/4 | Y | 2027/1 | 鉄骨 | 空有　44000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_408838042/ |
| 1.38 | アステシオ清和院 | 3LDK | 143.58 | 450,000 | 0 | 2ヶ月(-) / 0円 | 0.0 | 3/3 | Y | 1988/4 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_411286388/ |
| 1.38 | アステシオ清和院 | 2LDK | 148.06 | 480,000 | 0 | 2ヶ月(-) / 0円 | 0.0 | 2/3 | Y | 1988/4 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_411356430/ |
| 1.38 | アステシオ清和院 | 3LDK | 117.56 | 380,000 | 0 | 2ヶ月(-) / 0円 | 0.0 | 1/3 | Y | 1988/4 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_411356488/ |
| 1.39 | グリシーヌ御所西I | 3LDK | 78.38 | 209,000 | 6000 | 3万円(-) / 35万円 | 1.67 | 2/3 | n | 2021/10 | 鉄骨 | 空有　33000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_413800298/ |
| 1.39 | 二条麩屋町ビューハイツ | 3SLDK | 72.8 | 140,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 6/9 | Y | 1981/10 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_413665358/ |
| 1.42 | LiveCasa堀川今出川 | 2LDK | 47.07 | 145,000 | 10000 | 0円(-) / 0円 | 0.0 | 7/7 | Y | 2023/11 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413770694/ |
| 1.42 | 烏丸線今出川駅まで徒歩18分 | 4DK | 79.0 | 105,000 | 0 | 10.5万円(-) / 10.5万円 | 1.0 | None/3 | n | 1996/10 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413098446/ |
| 1.42 | 烏丸線今出川駅まで徒歩2分 | 2LDK | 60.0 | 115,000 | 0 | 11.5万円(-) / 11.5万円 | 1.0 | None/3 | n | 1998/7 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_321088556/ |
| 1.42 | 今出川コートハウス | 2LDK | 66.0 | 185,000 | 10000 | 18.5万円(-) / 37万円 | 2.0 | 1/2 | n | 2026/2 | 木造 | 空有　22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_397400164/ |
| 1.42 | パレロイヤル西陣 | 3LDK | 87.31 | 170,000 | 10000 | 0円(-) / 17万円 | 1.0 | 11/11 | Y | 1990/5 | RC | 空有　22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_412097274/ |
| 1.42 | リーガル京都堀川中立売II | 2LDK | 63.6 | 178,000 | 10000 | 17.8万円(-) / 17.8万円 | 1.0 | 4/7 | Y | 2024/2 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_373271848/ |
| 1.42 | グラン・リソシエ京都御苑 | 2LDK | 61.78 | 210,000 | 10000 | 0円(-) / 21万円 | 1.0 | 2/5 | Y | 2013/2 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_391820060/ |
| 1.42 | リーガル京都御所西II | 3LDK | 83.6 | 215,000 | 21840 | 0円(-) / 45万円 | 2.09 | 5/5 | Y | 2016/7 | RC | 空有　35000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411124698/ |
| 1.42 | リーガル京都御所西II | 2LDK | 70.52 | 181,560 | 18440 | 0円(-) / 30万円 | 1.65 | 4/5 | Y | 2016/7 | RC | 空有　35000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_407940480/ |
| 1.42 | ベルメゾン一条 | 2LDK | 53.33 | 100,000 | 3000 | 3万円(-) / 20万円 | 2.0 | 2/3 | n | 1989/2 | RC | 空無　15000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_404034060/ |
| 1.45 | 叡電元田中駅まで徒歩24分 | 3LDK | 71.0 | 125,000 | 0 | 12.5万円(-) / 12.5万円 | 1.0 | None/2 | n | 1982/6 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414661730/ |
| 1.45 | 京阪鴨東線出町柳駅まで徒歩24分 | 3LDK | 90.26 | 230,000 | 0 | 23万円(-) / 23万円 | 1.0 | None/2 | n | 2012/11 | 木造 | 空無 | house | https://sumaity.com/chintai/kyoto_prop/prop_413636628/ |
| 1.45 | 叡電元田中駅まで徒歩5分 | 3LDK | 85.56 | 190,000 | 5000 | 5万円(-) / 28万円 | 1.47 | None/2 | n | 2008/3 | 軽量鉄骨 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_413301696/ |
| 1.45 | EMINAS北白川 | 3LDK | 86.46 | 162,000 | 5000 | 16.2万円(-) / 20万円 | 1.23 | 2/2 | n | 2025/11 | 鉄骨 | 空有　14850円 | A | https://sumaity.com/chintai/kyoto_prop/prop_413300316/ |
| 1.5 | パラドール御所西グランデ | 3LDK | 72.2 | 240,000 | 20000 | 1ヶ月(-) / 2ヶ月 | 2.0 | 2/5 | Y | 2023/12 | RC | 空有　23000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_408208746/ |
| 1.5 | 御所西ロイヤルプラザ | 2LDK | 70.0 | 160,000 | 10000 | 0円(-) / 16万円 | 1.0 | 4/6 | n | 1988/10 | RC | 空有　22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_414054014/ |
| 1.5 | 御所西ロイヤルプラザ | 2LDK | 60.0 | 150,000 | 10000 | 0円(-) / 15万円 | 1.0 | 4/6 | Y | 1988/10 | RC | 空有　22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_413720714/ |
| 1.5 | 御所西ロイヤルプラザ | 2LDK | 60.0 | 150,000 | 10000 | 0円(-) / 15万円 | 1.0 | 3/6 | Y | 1988/10 | RC | 空有　22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_413720818/ |
| 1.5 | 御所西ロイヤルプラザ | 2LDK | 60.0 | 160,000 | 10000 | 0円(-) / 16万円 | 1.0 | 2/6 | Y | 1988/10 | RC | 空有　22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_414054090/ |
| 1.5 | パラドール御所西グランデ | 2LDK | 66.31 | 250,000 | 0 | 0円(-) / 50万円 | 2.0 | 3/5 | Y | 2023/12 | RC | 空無　22000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_366179974/ |
| 1.5 | HABITER | 2LDK | 61.37 | 213,000 | 9500 | 5万円(-) / 30万円 | 1.41 | 3/3 | Y | 2024/12 | 鉄骨 | 空有　29700円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414295128/ |
| 1.5 | 烏丸線今出川駅まで徒歩13分 | 3LDK | 65.93 | 99,000 | 0 | 9.9万円(-) / 9.9万円 | 1.0 | None/2 | n | 1991/5 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_384737418/ |
| 1.5 | エスポワール丸太町 | 2SLDK | 83.41 | 210,000 | 8000 | 9万円(-) / 42万円 | 2.0 | 2/3 | n | 2015/1 | 鉄骨 | 空無　27500円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414132104/ |
| 1.5 | ROUAGE御所南 | 2LDK | 76.29 | 265,000 | 20000 | 0円(-) / 53万円 | 2.0 | 3/5 | Y | 2026/4 | RC | 空無　55000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_409856800/ |
| 1.5 | ROUAGE御所南 | 2LDK | 76.29 | 260,000 | 20000 | 0円(-) / 52万円 | 2.0 | 2/5 | Y | 2026/4 | RC | 空無　55000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_409856834/ |
| 1.91 | ラヴィエール北白川 | 2LDK | 60.96 | 122,000 | 7000 | 12.2万円(-) / 12.2万円 | 1.0 | 1/2 | n | 2025/1 | 木造 | 空有　15000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411278306/ |
