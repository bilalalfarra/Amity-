# sumaity — スマイティ (sumaity.com), WALK3 survey (≤3.0 km of 京都技術科学センター, 左京区吉田河原町14; rent ≤140,000), fetched 2026-10-18

## Method
- Server-side filters (https://sumaity.com/chintai/area_list/list.php): acity_id = ward, madori[] = 2LDK/3DK/3LDK/4DK/4LDK以上, price_high=140000 (賃料≤14万), foot_print_low=45. No 礼金 / age / floor / elevator rules (none applied anywhere).
- Wards (site room counts): kita 269, kamigyo 148, sakyo 393, nakagyo 125, higashiyama 30, shimogyo 86 → 28 list pages, 1051 unique room listings (raw: out/raw/sumaity/list_<ward>_p<N>.html).
- List-stage funnel: total 1051, candidates 491, station walk ⇒ > 3.0 km 296, geocode contradicts station (kept) 17, far (> 3.5 km town-level) 190, layout 10, far (station approx) 54, no location 8, area<45 2, list duplicates (same room, other agency) not fetched 75. List-stage distance is town-level (sumaity hides block numbers; Kyoto 通り名 addresses reduced to ward+町名 by kgeo.py) so the cut there was lenient (3.5 km); every geocode was also checked against the listed 駅徒歩N分 (≤ N×80 m from the station): impossible ones dropped, contradicting geocodes not trusted.
- All 424 candidate unit pages fetched (raw: out/raw/sumaity/detail/; HTTP {200: 318, 404: 1}). Final distance: the unit page's own lat/lng when published (exact) → keep ≤ 3.0 km; otherwise town-level GSI geocode → keep ≤ 3.2 km (flagged in notes, ±300 m). Detail-stage drops: {'> 3.0 km (site coords)': 50, 'http 404': 1, '> 3.2 km (town-level)': 7}.
- Rate limit: Cloudflare answered HTTP 429 twice in this run (Retry-After 22 and 30 min). Every 429 was honoured: fetching stopped at the first 429, the pace was slowed to 8.0 s/request, and the next attempt waited past Retry-After. List-level duplicates (same 町名/floor/layout/area/築年数/階建/rent from several agencies) were not fetched — their URLs are in the representative's notes. Unit pages still unfetched when a 429 stopped the run: 0 → out/sumaity_unfetched.json (list data only, URL not verified).
- Caveats: sumaity aggregates several agencies; the same room can appear under several prop IDs (merged by post.py on town+floor+area+built+floors; other URLs in `notes`). 仲介手数料/保証会社 are often 'ask the agency'. Nameless buildings show the station text as the name.
- Station plausibility check (geofix.py; Kyoto town names repeat, GSI returns one): {'checked': 108, 'no_station': 14, 'inconsistent_moved': 7, 'dropped_lower_bound': 1, 'roughly_consistent_kept': 2}; dropped (cannot be ≤3.0 km given the listed 駅徒歩): 1 → out/sumaity_geodropped.json.

## Result
- **Kept 322 units** (after merging 43 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 21 located via the same building name in another listing with a full address, 67 approximated from the nearest station (uncertain — bounds in `notes`), 0 of them dropped as too far.
- Within 1.0 km: 23; rent range kept: 55000–140000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'house': 86, 'B': 55, 'old': 99, 'A': 82}; 礼金 ≤1ヶ月 199, >1ヶ月 123, unknown 0 (no 礼金 limit in this survey).
- Location precision (`geo_precision`): {'site': 219, 'station': 71, 'town': 25, 'site (same building, other listing)': 7} — 'site' = the listing's own map coordinates, 'town' = 町名 centroid (±300 m), 'station' = only the ward is published (or the 町名 geocode contradicted the listed 駅徒歩), position = nearest station (bounds in notes).
- Elevator yes/no/unknown: 136/186/0; by ward: {'左京区': 108, '上京区': 101, '中京区': 38, '北区': 57, '東山区': 3, '下京区': 15}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/sumaity/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.12 | 京阪鴨東線出町柳駅まで徒歩10分 | 3LDK | 66.7 | 120,000 | 0 | 0円(-) / 24万円 | 2.0 | 1/2 | n | 2004/12 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_411268278/ |
| 0.13 | 京阪鴨東線出町柳駅まで徒歩11分 | 2LDK | 66.7 | 120,000 | 0 | 0円(-) / 24万円 | 2.0 | None/2 | n | 2004/12 | 木造 | 近隣　18000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_411186002/ |
| 0.16 | 京阪鴨東線神宮丸太町駅まで徒歩6分 | 3DK | 54.67 | 100,000 | 0 | 1ヶ月(-) / 2ヶ月 | 2.0 | 1/2 | n | 1984/11 | 木造 | 近隣　18000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_412197276/ |
| 0.18 | ＥＤＥＬＨＥＩＭ鴨川 | 3LDK | 65.77 | 138,000 | 10000 | 20万円(-) / 35万円 | 2.54 | 5/5 | Y | 1997/2 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_411517530/ |
| 0.18 | 京阪鴨東線神宮丸太町駅まで徒歩8分 | 3DK | 65.0 | 100,000 | 0 | 10万円(-) / 20万円 | 2.0 | None/3 | n | 1984/11 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_412221194/ |
| 0.32 | 京阪鴨東線出町柳駅まで徒歩7分 | 3DK | 59.2 | 95,000 | 0 | 9.5万円(-) / 15万円 | 1.58 | 2/2 | n | 1954/11 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413939708/ |
| 0.6 | 京阪鴨東線神宮丸太町駅まで徒歩8分 | 3DK | 65.0 | 100,000 | 0 | 10万円(-) / 20万円 | 2.0 | None/2 | n | 1984/11 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_406678310/ |
| 0.62 | 地下鉄東西線京都市役所前駅まで徒歩12分 | 2LDK | 48.6 | 95,000 | 7000 | 9.5万円(-) / 10万円 | 1.05 | 2/3 | n | 1988/9 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414227120/ |
| 0.68 | 京阪鴨東線神宮丸太町駅まで徒歩8分 | 2LDK | 53.94 | 136,000 | 10000 | 0円(-) / 13.6万円 | 1.0 | 1/3 | n | 1987/2 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_408772224/ |
| 0.68 | グランレブリー御所東２ | 2LDK | 53.94 | 138,000 | 10000 | 0円(-) / 1ヶ月 | 1.0 | 2/3 | n | 1987/2 | RC | 空有　27500円 | old | https://sumaity.com/chintai/kyoto_prop/prop_413162436/ |
| 0.71 | 京阪鴨東線出町柳駅まで徒歩9分 | 4LDK | 65.71 | 135,000 | 0 | 0円(-) / 0円 | 0.0 | 1/2 | n | 1994/4 | 木造 | 近隣　15000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_414386332/ |
| 0.72 | 京阪鴨東線出町柳駅まで徒歩5分 | 2LDK | 45.08 | 100,000 | 0 | 10万円(-) / 20万円 | 2.0 | 2/2 | n | 1970/11 | 木造 | 近隣　18000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_413106128/ |
| 0.75 | サンアートビル | 3LDK | 59.41 | 130,000 | 8000 | 0円(-) / 0円 | 0.0 | 5/6 | Y | 1981/12 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_409656178/ |
| 0.75 | サンアートビル | 3LDK | 80.4 | 130,000 | 8000 | 0円(-) / 0円 | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 | 近隣　30000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_410851644/ |
| 0.75 | サンアートビル | 3LDK | 59.14 | 130,000 | 8000 | 0円(-) / 0円 | 0.0 | 5/6 | Y | 1981/12 | 鉄骨 | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_351584776/ |
| 0.78 | 京阪鴨東線神宮丸太町駅まで徒歩3分 | 3LDK | 90.0 | 135,000 | 0 | 0円(-) / 1ヶ月 | 1.0 | 2/2 | n | 1950/5 | 木造 | 近隣　20000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_412197272/ |
| 0.78 | 京阪鴨東線神宮丸太町駅まで徒歩4分 | 3SLDK | 90.0 | 135,000 | 0 | 0円(-) / 13.5万円 | 1.0 | None/2 | n | 1950/4 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414616330/ |
| 0.8 | 吉田近衛町19-6 | 2LDK | 48.0 | 120,000 | 0 | 12万円(-) / 24万円 | 2.0 | 2/2 | n | 1993/10 | 木造 | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_408373890/ |
| 0.9 | 京阪鴨東線神宮丸太町駅まで徒歩13分 | 2LDK | 54.56 | 124,000 | 12000 | 0円(-) / 5万円 | 0.4 | 1/3 | n | 2018/12 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414598536/ |
| 0.94 | シャルト北苑 | 4LDK | 69.03 | 135,000 | 10000 | 1ヶ月(-) / 0円 | 0.0 | 3/3 | n | 1984/1 | RC | 近隣　15000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_409165206/ |
| 0.94 | シャルト北苑 | 3LDK | 71.72 | 140,000 | 10000 | 2ヶ月(-) / 1ヶ月 | 1.0 | 2/3 | n | 1984/1 | RC | 近隣　15000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_409081830/ |
| 0.94 | シャルト北苑 | 3LDK | 69.03 | 140,000 | 10000 | 2ヶ月(-) / 1ヶ月 | 1.0 | 1/3 | n | 1984/1 | RC | 近隣　15000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_395604664/ |
| 0.95 | 吉田中大路町アパート | 2LDK | 49.66 | 87,000 | 3000 | 0円(-) / 0円 | 0.0 | 1/2 | n | 2002/10 | 木造 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_326815360/ |
| 1.02 | かぐら坂荘 | 2LDK | 60.23 | 127,000 | 7000 | 0円(-) / 12.7万円 | 1.0 | 3/3 | n | 2011/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_408351658/ |
| 1.03 | 京都グランドハイツ | 2LDK | 64.5 | 140,000 | 10000 | 14万円(-) / 14万円 | 1.0 | 4/7 | Y | 1971/6 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414227714/ |
| 1.06 | 京阪鴨東線神宮丸太町駅まで徒歩18分 | 3DK | 69.35 | 90,000 | 0 | 9万円(-) / 9万円 | 1.0 | 1/1 | n | 2001/8 | 木造 | 近隣　16000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_400486690/ |
| 1.09 | グレーシー北白川 | 3LDK | 68.39 | 130,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 3/3 | n | 1991/8 | RC | - | B | https://sumaity.com/chintai/kyoto_prop/prop_405890208/ |
| 1.12 | 京阪鴨東線神宮丸太町駅まで徒歩18分 | 3SLDK | 107.96 | 135,000 | 0 | 0円(-) / 0円 | 0.0 | 1/3 | n | 1995/4 | 木造 | 付無料 | house | https://sumaity.com/chintai/kyoto_prop/prop_409567420/ |
| 1.13 | エルミタージュ下鴨東 | 2LDK | 55.43 | 125,000 | 8500 | 0円(-) / 0円 | 0.0 | 2/2 | n | 2024/7 | 軽量鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414381988/ |
| 1.15 | グランタック東山二条 | 2LDK | 56.0 | 130,000 | 8000 | 1ヶ月(-) / 0円 | 0.0 | 5/6 | Y | 1977/1 | RC | 近隣　20000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_410952538/ |
| 1.18 | メゾンフジ | 3DK | 80.0 | 135,000 | 5000 | 0円(-) / 0円 | 0.0 | 2/5 | n | 1985/10 | 鉄骨 | 近隣　20000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_406033418/ |
| 1.21 | 叡山電鉄叡山本線元田中駅まで徒歩6分 | 5DK | 63.66 | 88,000 | 0 | 8.8万円(-) / 10万円 | 1.14 | 1/2 | n | 1988/8 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_412481246/ |
| 1.23 | 山和小路 | 3LDK | 66.97 | 125,000 | 10000 | 0円(-) / 1ヶ月 | 1.0 | 5/5 | Y | 1999/11 | RC | 空有　23100円 | B | https://sumaity.com/chintai/kyoto_prop/prop_413282120/ |
| 1.28 | コーポ富有 | 2LDK | 48.51 | 100,000 | 9000 | 10万円(-) / 10万円 | 1.0 | 2/4 | Y | 1985/7 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_411996406/ |
| 1.3 | 北白川コーポラス | 3LDK | 66.0 | 100,000 | 8000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 3/5 | n | 1988/3 | RC | 空有　8000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_412630416/ |
| 1.32 | ランブラス二条御幸町 | 2LDK | 57.03 | 129,000 | 15000 | 10万円(-) / 0円 | 0.0 | 5/6 | Y | 1997/9 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_410274482/ |
| 1.37 | アイル竹嶋 | 2LDK | 52.0 | 120,000 | 15000 | 0円(-) / 25万円 | 2.08 | 5/6 | Y | 1993/3 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_414808576/ |
| 1.39 | 叡山電鉄叡山本線元田中駅まで徒歩7分 | 3DK | 50.71 | 95,000 | 0 | 0円(-) / 9.5万円 | 1.0 | None/2 | n | 1985/3 | 木造 | 付無料 | house | https://sumaity.com/chintai/kyoto_prop/prop_411454224/ |
| 1.41 | 地下鉄東西線京都市役所前駅まで徒歩4分 | 2LDK | 46.59 | 114,000 | 10000 | 20万円(-) / 35万円 | 3.07 | 5/5 | Y | 2009/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_407572498/ |
| 1.42 | 二条麩屋町ビューハイツ | 3SLDK | 72.8 | 140,000 | 0 | 14万円(-) / 14万円 | 1.0 | 6/9 | Y | 1981/10 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_413546894/ |
| 1.42 | 烏丸線今出川駅まで徒歩18分 | 4DK | 79.0 | 105,000 | 0 | 10.5万円(-) / 10.5万円 | 1.0 | None/3 | n | 1996/10 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413098446/ |
| 1.42 | 烏丸線今出川駅まで徒歩2分 | 2LDK | 60.0 | 115,000 | 0 | 11.5万円(-) / 11.5万円 | 1.0 | None/3 | n | 1998/7 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_321088556/ |
| 1.46 | パラドール御所 | 3LDK | 63.18 | 130,000 | 15000 | 1ヶ月(-) / 2ヶ月 | 2.0 | 5/7 | Y | 1984/3 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_370863618/ |
| 1.46 | 地下鉄烏丸線今出川駅まで徒歩2分 | 3LDK | 63.18 | 130,000 | 15000 | 13万円(-) / 26万円 | 2.0 | 5/7 | Y | 1985/3 | RC | 敷地内20000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_372962098/ |
| 1.5 | 烏丸線今出川駅まで徒歩13分 | 3LDK | 65.93 | 99,000 | 0 | 9.9万円(-) / 9.9万円 | 1.0 | None/2 | n | 1991/5 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_384737418/ |
| 1.54 | 地下鉄烏丸線鞍馬口駅まで徒歩10分 | 4DK | 66.21 | 93,000 | 0 | 9.3万円(-) / 9.3万円 | 1.0 | 1/2 | n | 1979/1 | 木造 | 付無料/屋根付駐 | house | https://sumaity.com/chintai/kyoto_prop/prop_404860488/ |
| 1.54 | 烏丸線鞍馬口駅まで徒歩7分 | 4DK | 76.21 | 93,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 1/2 | n | 1970/1 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_405147604/ |
| 1.57 | 地下鉄烏丸線今出川駅まで徒歩3分 | 2LDK | 60.0 | 115,000 | 0 | 11.5万円(-) / 11.5万円 | 1.0 | 2/3 | n | 1998/7 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_409636794/ |
| 1.58 | メゾンミュゲ | 2LDK | 64.98 | 130,000 | 5000 | 13万円(-) / 26万円 | 2.0 | 2/2 | n | 2020/7 | 軽量鉄骨 | 敷地内13200円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411037838/ |
| 1.58 | 烏丸線今出川駅まで徒歩3分 | 2LDK | 65.8 | 115,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 2/3 | n | 1998/7 | 木造 | 近隣　14300円 | house | https://sumaity.com/chintai/kyoto_prop/prop_405355920/ |
| 1.58 | ｉ・レジデンス御所北 | 2LDK | 54.08 | 134,000 | 7000 | 0円(-) / 20万円 | 1.49 | 1/4 | n | 2014/4 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_408070238/ |
| 1.58 | 藤波ビル | 2LDK | 47.52 | 114,000 | 4000 | 5万円(-) / 10万円 | 0.88 | 2/4 | n | 1990/3 | 鉄骨 | 近隣　22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_404651772/ |
| 1.6 | リッツ岡崎 | 2LDK | 69.0 | 130,000 | 12000 | 10万円(-) / 10万円 | 0.77 | 1/3 | Y | 1990/2 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414647008/ |
| 1.6 | 烏丸線今出川駅まで徒歩3分 | 2LDK | 51.88 | 115,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 1/3 | n | 1998/7 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_405557292/ |
| 1.61 | 烏丸線今出川駅まで徒歩8分 | 3DK | 54.37 | 78,000 | 0 | 0円(-) / 1ヶ月 | 1.0 | 1/2 | n | 1960/1 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_407987456/ |
| 1.61 | 京阪鴨東線出町柳駅まで徒歩31分 | 3LDK | 65.93 | 99,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 2/2 | n | 1999/5 | 木造 | 近隣　27500円 | house | https://sumaity.com/chintai/kyoto_prop/prop_384687956/ |
| 1.64 | 地下鉄烏丸線丸太町駅まで徒歩12分 | 2LDK | 65.93 | 99,000 | 0 | 9.9万円(-) / 9.9万円 | 1.0 | 1/5 | n | 1984/12 | 鉄骨 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_384837266/ |
| 1.65 | 叡山電鉄叡山本線出町柳駅まで徒歩26分 | 3LDK | 71.0 | 125,000 | 0 | 12.5万円(-) / 12.5万円 | 1.0 | None/2 | n | 1982/6 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414616386/ |
| 1.65 | コンフォール北白川３ | 2LDK | 50.4 | 115,000 | 5000 | 12万円(-) / 0円 | 0.0 | 3/3 | n | 2006/2 | RC | 空有　20000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_396559172/ |
| 1.66 | 地下鉄烏丸線鞍馬口駅まで徒歩5分 | 2SLDK | 62.72 | 120,000 | 0 | 0円(-) / 10万円 | 0.83 | 1/2 | n | 1911/1 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414292098/ |
| 1.66 | 京阪鴨東線神宮丸太町駅まで徒歩28分 | 2LDK | 69.93 | 130,000 | 0 | 1ヶ月(-) / 1.5ヶ月 | 1.5 | 1/2 | n | 1983/8 | 木造 | 近隣　16500円 | house | https://sumaity.com/chintai/kyoto_prop/prop_404452808/ |
| 1.66 | アベニューエンジュ | 3LDK | 53.46 | 113,000 | 0 | 11.3万円(-) / 0円 | 0.0 | 1/3 | n | 1992/5 | SRC | 敷地内10000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_411675906/ |
| 1.66 | ロイヤルステイツ御所南 | 2LDK | 45.03 | 132,000 | 10000 | 13.2万円(-) / 13.2万円 | 1.0 | 6/9 | Y | 2009/2 | SRC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_386705410/ |
| 1.67 | 烏丸線鞍馬口駅まで徒歩8分 | 3DK | 50.0 | 100,000 | 0 | 0円(-) / 1ヶ月 | 1.0 | None/2 | n | 1980/1 | 木造 | 近隣　13200円 | house | https://sumaity.com/chintai/kyoto_prop/prop_413050746/ |
| 1.67 | コンフォール北白川２ | 3DK | 52.46 | 110,000 | 0 | 10万円(-) / 0円 | 0.0 | 3/3 | n | 1994/2 | 鉄骨 | - | B | https://sumaity.com/chintai/kyoto_prop/prop_246586133/ |
| 1.68 | 地下鉄東西線東山駅まで徒歩7分 | 2LDK | 60.0 | 120,000 | 20000 | 12万円(-) / 12万円 | 1.0 | 2/3 | Y | 1984/11 | RC | 敷地内27000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_414598496/ |
| 1.69 | ピアレス円勝寺 | 2LDK | 53.0 | 120,000 | 20000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 2/3 | Y | 1984/12 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_413944766/ |
| 1.7 | 烏丸線鞍馬口駅まで徒歩6分 | 4DK | 66.21 | 93,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 2/2 | n | 1930/1 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_404918650/ |
| 1.71 | セラヴィー１１９ | 2LDK | 63.52 | 140,000 | 10000 | 14万円(-) / 14万円 | 1.0 | 5/5 | Y | 1989/6 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_401340818/ |
| 1.71 | セラヴィ119 | 2LDK | 63.52 | 140,000 | 10000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 5/5 | Y | 1988/3 | RC | 近隣　15400円 | old | https://sumaity.com/chintai/kyoto_prop/prop_402245400/ |
| 1.71 | ロイヤルセンタービルディングコバヤシ | 2LDK | 56.28 | 87,000 | 8000 | 8.7万円(-) / 17.4万円 | 2.0 | 3/5 | Y | 1987/12 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_388430528/ |
| 1.71 | 地下鉄烏丸線今出川駅まで徒歩13分 | 7DK | 113.39 | 140,000 | 0 | 28万円(-) / 14万円 | 1.0 | None/2 | n | 1970/6 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413216006/ |
| 1.72 | エルシア御池間之町 | 2LDK | 56.55 | 140,000 | 10000 | 14万円(-) / 28万円 | 2.0 | 8/11 | Y | 2008/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_379971430/ |
| 1.72 | ベルメゾン一条 | 2LDK | 53.33 | 100,000 | 3000 | 3万円(-) / 20万円 | 2.0 | 2/3 | n | 1989/2 | RC | 空有　15000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_404039540/ |
| 1.75 | ＣＨＥＲＲＹＶＩＥＷ | 2LDK | 57.87 | 110,000 | 5000 | 11万円(-) / 22万円 | 2.0 | 2/3 | n | 1990/4 | 鉄骨 | 空無　25000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_282251335/ |
| 1.77 | 京都グランデ | 2LDK | 63.56 | 140,000 | 5000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 3/3 | n | 2019/10 | 木造 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_374670252/ |
| 1.77 | ＦａｒＥａｓｔ東山 | 2LDK | 59.87 | 134,000 | 12000 | 13.4万円(-) / 26.8万円 | 2.0 | 1/3 | n | 2015/6 | RC | 敷地内15000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414227374/ |
| 1.78 | レジデンス古橋 | 2LDK | 61.53 | 128,000 | 10000 | 0円(-) / 0円 | 0.0 | 4/6 | Y | 1978/10 | RC | 空有　22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_406715930/ |
| 1.79 | プラネシア星の子御所西 | 2LDK | 60.2 | 114,000 | 9000 | 0円(-) / 17.25万円 | 1.51 | 4/4 | n | 2001/2 | 鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413139326/ |
| 1.79 | プラネシア星の子御所西 | 2LDK | 52.0 | 117,000 | 9000 | 0円(-) / 0円 | 0.0 | 2/6 | n | 1973/5 | 鉄骨 | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_409695468/ |
| 1.79 | プラネシア星の子御所西 | 2LDK | 51.43 | 117,000 | 9000 | 0円(-) / 11.7万円 | 1.0 | 2/5 | n | 2001/2 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_402346974/ |
| 1.8 | 地下鉄烏丸線今出川駅まで徒歩9分 | 2LDK | 61.9 | 114,000 | 9000 | 0円(-) / 17.1万円 | 1.5 | 4/5 | n | 2001/2 | 鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413139278/ |
| 1.8 | 北白川松園 | 3DK | 53.0 | 108,000 | 0 | 10.8万円(-) / 10.8万円 | 1.0 | 3/4 | n | 1969/10 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414564654/ |
| 1.81 | 地下鉄烏丸線今出川駅まで徒歩10分 | 6K | 72.78 | 98,000 | 0 | 19.6万円(-) / 9.8万円 | 1.0 | None/2 | n | 1950/1 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_393739858/ |
| 1.83 | 地下鉄烏丸線丸太町駅まで徒歩15分 | 3SDK | 71.65 | 80,000 | 0 | 8万円(-) / 8万円 | 1.0 | None/2 | n | 1970/10 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_412187556/ |
| 1.83 | 下鴨スタイル | 2LDK | 55.37 | 122,500 | 5800 | 0円(-) / 12.25万円 | 1.0 | 1/2 | n | 2008/12 | 木造 | 敷地内19800円 | A | https://sumaity.com/chintai/kyoto_prop/prop_413877678/ |
| 1.84 | 東大路高野第１住宅１棟 | 3DK | 60.94 | 98,000 | 0 | 0円(-) / 1ヶ月 | 1.0 | 7/7 | Y | 1979/11 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_408070324/ |
| 1.86 | 烏丸線丸太町駅まで徒歩15分 | 2LDK | 51.08 | 80,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 1/2 | n | 1950/3 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_367917208/ |
| 1.86 | カストルム洛北 | 3LDK | 64.9 | 115,000 | 12000 | 10万円(-) / 25万円 | 2.17 | 5/7 | Y | 1983/4 | RC | 空有　22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_413300298/ |
| 1.86 | 京阪鴨東線出町柳駅までバス約11分 | 3DK | 55.83 | 110,000 | 0 | 1ヶ月(-) / 2ヶ月 | 2.0 | 1/2 | n | 1983/10 | 木造 | 近隣　15400円 | house | https://sumaity.com/chintai/kyoto_prop/prop_410448256/ |
| 1.86 | ロートレック中京 | 2LDK | 52.17 | 125,000 | 15000 | 25万円(-) / 25万円 | 2.0 | 9/11 | Y | 1984/1 | SRC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_405172654/ |
| 1.87 | 第２高原町マンション | 2LDK | 50.0 | 75,000 | 5000 | 7.5万円(-) / 7.5万円 | 1.0 | 3/5 | n | 1998/4 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_297231495/ |
| 1.89 | グリーンヒル北白川 | 3LDK | 54.85 | 130,000 | 3850 | 0円(-) / 26万円 | 2.0 | 1/2 | n | 1985/3 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_412346228/ |
| 1.9 | カバーロ京都御池 | 2LDK | 48.37 | 120,000 | 5000 | 0円(-) / 2ヶ月 | 2.0 | 3/8 | Y | 1994/5 | 鉄骨 | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_414202396/ |
| 1.91 | 叡電茶山・京都芸術大学駅まで徒歩3分 | 3DK | 57.37 | 110,000 | 0 | 11万円(-) / 11万円 | 1.0 | None/2 | n | 1984/12 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_411866622/ |
| 1.92 | サンレジデンス錦綾東堀川 | 3LDK | 74.8 | 120,000 | 10000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 9/11 | Y | 1982/11 | SRC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_413685830/ |
| 1.93 | 地下鉄東西線蹴上駅まで徒歩15分 | 2LDK | 61.53 | 128,000 | 10000 | 0円(-) / 0円 | 0.0 | 4/6 | Y | 1980/3 | RC | 敷地内20000円/平置屋根付駐 | old | https://sumaity.com/chintai/kyoto_prop/prop_413707434/ |
| 1.94 | サンレジデンス錦綾東堀川 | 3LDK | 76.14 | 130,000 | 10000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 3/11 | Y | 1982/10 | SRC | 近隣　17600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_403667200/ |
| 1.94 | グランディール下鴨 | 4DK | 80.19 | 90,000 | 5000 | 0円(-) / 0円 | 0.0 | 1/3 | n | 1983/4 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414682338/ |
| 1.94 | マナーハウス | 2LDK | 62.31 | 115,000 | 10000 | 11.5万円(-) / 11.5万円 | 1.0 | 1/4 | Y | 1996/1 | RC | 近隣80m26000円/機械式駐 | B | https://sumaity.com/chintai/kyoto_prop/prop_414227520/ |
| 1.95 | メイゾン鞍馬口 | 3LDK | 64.0 | 114,000 | 6000 | 11.4万円(-) / 15万円 | 1.32 | 2/4 | n | 1986/1 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_408564970/ |
| 1.96 | 叡電元田中駅まで徒歩16分 | 4DK | 74.72 | 89,000 | 6000 | 1ヶ月(-) / 1ヶ月 | 1.0 | None/2 | n | 1979/9 | 木造 | 近隣　16500円 | house | https://sumaity.com/chintai/kyoto_prop/prop_413606858/ |
| 1.97 | 白川セントラルハイツ | 3DK | 50.22 | 75,000 | 9800 | 8.5万円(-) / 1ヶ月 | 1.0 | 5/5 | Y | 1981/9 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_405445956/ |
| 1.98 | プラネシア神宮道 | 2LDK | 55.77 | 139,000 | 8000 | 0円(-) / 20.85万円 | 1.5 | 2/5 | Y | 2010/6 | RC | 敷地内16500円 | A | https://sumaity.com/chintai/kyoto_prop/prop_408785504/ |
| 1.99 | 叡山電鉄叡山本線元田中駅まで徒歩29分 | 3LDK | 80.9 | 98,000 | 0 | 9.8万円(-) / 19.6万円 | 2.0 | None/2 | n | 1960/1 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_403099872/ |
| 1.99 | スペシャリー堀川 | 3LDK | 65.75 | 120,000 | 7500 | 1ヶ月(-) / 1ヶ月 | 1.0 | 7/11 | Y | 1997/9 | SRC | 空有　27500円 | B | https://sumaity.com/chintai/kyoto_prop/prop_270886927/ |
| 2.0 | マサール哲学の道 | 2LDK | 58.57 | 107,000 | 3500 | 0円(-) / 10.7万円 | 1.0 | 2/2 | n | 2015/3 | 木造 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_410744408/ |
| 2.01 | エルソレイユ | 3LDK | 64.76 | 134,000 | 4400 | 0円(-) / 13.4万円 | 1.0 | 2/3 | n | 2005/2 | 鉄骨 | 敷地内29700円 | A | https://sumaity.com/chintai/kyoto_prop/prop_395905620/ |
| 2.02 | 地下鉄烏丸線丸太町駅まで徒歩15分 | 2LDK | 60.54 | 130,000 | 0 | 26万円(-) / 13万円 | 1.0 | None/3 | n | 2014/9 | 木造 | 付無料 | house | https://sumaity.com/chintai/kyoto_prop/prop_397633192/ |
| 2.03 | 地下鉄烏丸線丸太町駅まで徒歩8分 | 6DK | 66.0 | 135,000 | 0 | 13.5万円(-) / 0円 | 0.0 | 1/2 | n | 1957/9 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_397836246/ |
| 2.04 | 叡電茶山・京都芸術大学駅まで徒歩15分 | 5DK | 47.72 | 70,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 2/2 | n | 1967/1 | 木造 | 近隣　16500円 | house | https://sumaity.com/chintai/kyoto_prop/prop_408147502/ |
| 2.04 | シャーメゾン西伊織 | 2LDK | 60.87 | 130,000 | 6000 | 3万円(-) / 27万円 | 2.08 | 2/2 | n | 2014/9 | 軽量鉄骨 | 敷地内14300円/平置駐 | A | https://sumaity.com/chintai/kyoto_prop/prop_413944684/ |
| 2.05 | 叡山電鉄叡山本線茶山・京都芸術大学駅まで徒歩 | 5DK | 47.72 | 70,000 | 0 | 7万円(-) / 7万円 | 1.0 | 1/2 | n | 1940/3 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_408617932/ |
| 2.06 | 京都東西線蹴上駅まで徒歩20分 | 3LDK | 58.0 | 90,000 | 0 | 0円(-) / 20万円 | 2.22 | 1/2 | n | 1964/3 | 木造 | 近隣　15400円 | house | https://sumaity.com/chintai/kyoto_prop/prop_247912804/ |
| 2.08 | カストルム洛北 | 3LDK | 67.65 | 113,000 | 12000 | 10万円(-) / 10万円 | 0.88 | 2/7 | Y | 1983/4 | 鉄骨 | 敷地内22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_411641146/ |
| 2.09 | カストルム洛北 | 3LDK | 67.65 | 113,000 | 12000 | 10万円(-) / 10万円 | 0.88 | 3/7 | Y | 1983/3 | RC | 敷地内22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_402003298/ |
| 2.09 | カストルム洛北 | 2LDK | 67.65 | 115,000 | 12000 | 10万円(-) / 10万円 | 0.87 | 5/7 | Y | 1983/3 | RC | 敷地内22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_413167772/ |
| 2.09 | カストルム洛北 | 3LDK | 64.9 | 115,000 | 12000 | 10万円(-) / 10万円 | 0.87 | 2/7 | Y | 1983/4 | RC | 空有　22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_379293076/ |
| 2.09 | グローバル北白川 | 2LDK | 53.42 | 120,000 | 5000 | 0円(-) / 12万円 | 1.0 | 4/7 | Y | 1997/2 | RC | 空有　14300円 | B | https://sumaity.com/chintai/kyoto_prop/prop_412982276/ |
| 2.13 | ラヴィエール北白川 | 2LDK | 60.96 | 122,000 | 7000 | 12.2万円(-) / 12.2万円 | 1.0 | 1/2 | n | 2025/1 | 木造 | 敷地内15000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_379810054/ |
| 2.14 | アネックス | 3LDK | 64.43 | 129,300 | 9000 | 1ヶ月(-) / 0円 | 0.0 | 6/10 | Y | 2001/2 | SRC | 近隣　18150円 | A | https://sumaity.com/chintai/kyoto_prop/prop_388817520/ |
| 2.14 | アネックス | 3LDK | 64.43 | 129,300 | 9000 | 1ヶ月(-) / 0円 | 0.0 | 5/10 | Y | 2001/2 | SRC | 近隣　18150円 | A | https://sumaity.com/chintai/kyoto_prop/prop_388817476/ |
| 2.14 | アネックス | 3LDK | 64.43 | 126,800 | 9000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 7/10 | Y | 2001/4 | RC | 空有　27500円 | A | https://sumaity.com/chintai/kyoto_prop/prop_406269862/ |
| 2.14 | アネックス | 3LDK | 65.55 | 130,700 | 9000 | 1ヶ月(-) / 0円 | 0.0 | 4/10 | Y | 2001/2 | SRC | 近隣　18150円 | A | https://sumaity.com/chintai/kyoto_prop/prop_373779054/ |
| 2.14 | アネックス | 3LDK | 65.55 | 132,700 | 9000 | 1ヶ月(-) / 0円 | 0.0 | 8/10 | Y | 2001/2 | SRC | 近隣　18150円 | A | https://sumaity.com/chintai/kyoto_prop/prop_368148180/ |
| 2.14 | 下鴨フラッツ | 2LDK | 52.0 | 98,000 | 6000 | 10万円(-) / 10万円 | 1.02 | 2/3 | n | 1993/4 | RC | 空有　19800円 | B | https://sumaity.com/chintai/kyoto_prop/prop_413162456/ |
| 2.14 | 下鴨フラッツ | 2LDK | 48.0 | 98,000 | 6000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 2/3 | n | 1993/4 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_245724152/ |
| 2.14 | シェモア鞍馬口２ | 2LDK | 54.86 | 100,000 | 5000 | 10万円(-) / 10万円 | 1.0 | 1/3 | n | 1984/11 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_413281870/ |
| 2.14 | 京阪鴨東線神宮丸太町駅まで徒歩24分 | 4LDK | 75.0 | 130,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 1/2 | n | 1926/1 | 木造 | 近隣　16500円 | house | https://sumaity.com/chintai/kyoto_prop/prop_410026228/ |
| 2.15 | 叡山電鉄叡山本線茶山・京都芸術大学駅まで徒歩 | 5DK | 99.68 | 100,000 | 0 | 10万円(-) / 10万円 | 1.0 | 1/2 | n | 1973/9 | 軽量鉄骨 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_360259834/ |
| 2.2 | Ｋ．Ｔマンション２号館 | 2LDK | 56.23 | 125,000 | 8000 | 0円(-) / 12.5万円 | 1.0 | 5/6 | Y | 1989/4 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_409059312/ |
| 2.2 | グレースコート堀川 | 2LDK | 50.0 | 87,000 | 5000 | 0円(-) / 15万円 | 1.72 | 4/5 | Y | 1988/7 | 鉄骨 | 敷地内19800円 | old | https://sumaity.com/chintai/kyoto_prop/prop_351469256/ |
| 2.21 | 京阪鴨東線出町柳駅まで徒歩30分 | 3LDK | 115.5 | 120,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 1/2 | n | 1950/1 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_410026210/ |
| 2.21 | ファーストコート今出川北 | 3LDK | 60.32 | 98,000 | 10000 | 0円(-) / 1ヶ月 | 1.0 | 5/7 | Y | 1981/10 | RC | 近隣　14300円 | old | https://sumaity.com/chintai/kyoto_prop/prop_403609422/ |
| 2.21 | 地下鉄烏丸線鞍馬口駅まで徒歩7分 | 4LDK | 74.01 | 140,000 | 0 | 15万円(-) / 15万円 | 1.07 | None/2 | n | 1977/8 | 木造 | 付無料 | house | https://sumaity.com/chintai/kyoto_prop/prop_412340052/ |
| 2.22 | ラフィーネ御池 | 2LDK | 62.72 | 120,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 4/11 | Y | 1989/4 | SRC | 空有　33000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_260729390/ |
| 2.24 | 三条室町パーク・ホームズ | 2LDK | 52.99 | 135,000 | 10000 | 10万円(-) / 20万円 | 1.48 | 2/11 | Y | 1996/3 | RC | 空有　20000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_412485718/ |
| 2.24 | ライオンズマンション二条城東 | 3DK | 61.07 | 138,000 | 0 | 13.8万円(-) / 13.8万円 | 1.0 | 10/11 | Y | 1991/2 | SRC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_410744454/ |
| 2.24 | アレックス堀川寺之内 | 3LDK | 63.21 | 102,000 | 8000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 6/11 | Y | 1990/2 | SRC | 近隣　14300円 | old | https://sumaity.com/chintai/kyoto_prop/prop_414146072/ |
| 2.26 | 叡山電鉄叡山本線茶山・京都芸術大学駅までバス | 4DK | 72.9 | 87,000 | 0 | 8.7万円(-) / 0円 | 0.0 | 1/2 | n | 1980/3 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414122190/ |
| 2.27 | 京阪鴨東線出町柳駅まで徒歩22分 | 2LDK | 53.86 | 78,000 | 0 | 5万円(-) / 8万円 | 1.03 | None/2 | n | 1967/4 | 木造 | 近隣　15000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_266568439/ |
| 2.27 | 薬師町マンション | 2LDK | 59.77 | 124,000 | 8000 | 20万円(-) / 20万円 | 1.61 | 3/11 | Y | 2004/3 | RC | 空有　20900円 | A | https://sumaity.com/chintai/kyoto_prop/prop_404915022/ |
| 2.28 | 京阪鴨東線出町柳駅まで徒歩4分 | 2LDK | 49.2 | 98,000 | 6000 | 9.8万円(-) / 9.8万円 | 1.0 | 2/3 | n | 1993/4 | RC | 敷地内16500円 | B | https://sumaity.com/chintai/kyoto_prop/prop_413925282/ |
| 2.3 | シャトー高野 | 2LDK | 52.2 | 81,000 | 4000 | 0円(-) / 0円 | 0.0 | 4/4 | n | 1978/9 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_401056674/ |
| 2.3 | シャトー高野 | 3LDK | 60.0 | 90,000 | 4000 | 0円(-) / 0円 | 0.0 | 1/4 | n | 1978/9 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_411253724/ |
| 2.31 | 玉屋山三小路 | 3LDK | 71.06 | 115,000 | 9000 | 11.5万円(-) / 0円 | 0.0 | 3/5 | Y | 1998/10 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_408789886/ |
| 2.31 | 玉屋山三小路 | 3DK | 64.42 | 115,000 | 9000 | 11.5万円(-) / 0円 | 0.0 | 2/5 | Y | 1998/10 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_413332486/ |
| 2.31 | カーネルヒル | 2LDK | 51.1 | 105,000 | 8000 | 10万円(-) / 0円 | 0.0 | 2/5 | Y | 1989/1 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_413636404/ |
| 2.31 | カーネルヒル | 2LDK | 51.1 | 106,000 | 8000 | 10万円(-) / 0円 | 0.0 | 4/5 | n | 1989/10 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_397207800/ |
| 2.31 | カーサ紫明 | 2LDK | 56.0 | 92,000 | 10000 | 0円(-) / 9.2万円 | 1.0 | 2/4 | n | 1991/7 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_403044104/ |
| 2.32 | コトールノール | 2LDK | 50.76 | 88,000 | 8000 | 1ヶ月(-) / 0円 | 0.0 | 3/3 | n | 1989/3 | RC | 近隣　13200円 | old | https://sumaity.com/chintai/kyoto_prop/prop_402311716/ |
| 2.33 | イヌイ星の子ハイツ | 3LDK | 61.91 | 114,000 | 10000 | 0円(-) / 2.4ヶ月 | 2.4 | 5/6 | Y | 1980/8 | RC | 空有　17600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_412466370/ |
| 2.33 | イヌイ星の子ハイツ | 2LDK | 60.62 | 114,000 | 10000 | 0円(-) / 2.4ヶ月 | 2.4 | 5/8 | Y | 1980/8 | RC | - | old | https://sumaity.com/chintai/kyoto_prop/prop_411719088/ |
| 2.33 | イヌイ星の子ハイツ | 3DK | 60.62 | 116,000 | 10000 | 0円(-) / 2.4ヶ月 | 2.4 | 3/6 | Y | 1980/8 | RC | 空有　17600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_412466800/ |
| 2.33 | イヌイ星の子ハイツ | 2LDK | 60.02 | 116,000 | 10000 | 0円(-) / 2.4ヶ月 | 2.4 | 3/8 | Y | 1980/8 | RC | - | old | https://sumaity.com/chintai/kyoto_prop/prop_411719056/ |
| 2.33 | イヌイ星の子ハイツ | 2LDK | 55.03 | 120,000 | 10000 | 0円(-) / 2.4ヶ月 | 2.4 | 5/6 | Y | 1980/8 | RC | 空有　17600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_412467070/ |
| 2.33 | イヌイ星の子ハイツ | 2LDK | 60.31 | 120,000 | 10000 | 0円(-) / 2.4ヶ月 | 2.4 | 5/8 | Y | 1980/8 | RC | - | old | https://sumaity.com/chintai/kyoto_prop/prop_409116808/ |
| 2.33 | イヌイ星の子ハイツ | 3LDK | 60.62 | 120,000 | 10000 | 0円(-) / 2.4ヶ月 | 2.4 | 5/6 | Y | 1980/8 | RC | 空有　17600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_414227150/ |
| 2.33 | イヌイ星の子ハイツ | 2LDK | 64.46 | 123,000 | 10000 | 0円(-) / 2.4ヶ月 | 2.4 | 6/6 | Y | 1980/8 | RC | 空有　17600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_412466128/ |
| 2.33 | イヌイ星の子ハイツ | 2LDK | 62.62 | 123,000 | 10000 | 0円(-) / 2.4ヶ月 | 2.4 | 6/8 | Y | 1980/8 | RC | 近隣　17600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_407460150/ |
| 2.33 | イヌイ星の子ハイツ | 3LDK | 65.05 | 135,000 | 10000 | 0円(-) / 2.4ヶ月 | 2.4 | 6/6 | Y | 1980/8 | RC | 空有　17600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_412466530/ |
| 2.33 | イヌイ星の子ハイツ | 3LDK | 61.91 | 135,000 | 10000 | 0円(-) / 2.4ヶ月 | 2.4 | 6/8 | Y | 1980/8 | RC | 近隣　17600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_407460210/ |
| 2.34 | エクシオ京都御池 | 2LDK | 57.05 | 128,000 | 0 | 10万円(-) / 15万円 | 1.17 | 4/11 | Y | 1992/10 | SRC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_413077710/ |
| 2.36 | ライオンズマンション一条智恵光院 | 2LDK | 49.7 | 83,000 | 10000 | 0円(-) / 8.3万円 | 1.0 | 2/6 | Y | 1989/6 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414682400/ |
| 2.36 | ライオンズマンション一条智恵光院 | 2LDK | 59.4 | 100,000 | 10000 | 10万円(-) / 10万円 | 1.0 | 2/6 | Y | 1989/6 | RC | 近隣150m20000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_414436752/ |
| 2.36 | 京都東西線二条城前駅まで徒歩19分 | 4LDK | 76.05 | 120,000 | 0 | 12万円(-) / 24万円 | 2.0 | 1/2 | n | 1982/12 | 木造 | 近隣　16500円 | house | https://sumaity.com/chintai/kyoto_prop/prop_413948346/ |
| 2.36 | ハイツサイプリスA棟 | 3LDK | 55.89 | 93,000 | 5000 | 0円(-) / 9.3万円 | 1.0 | 3/3 | n | 1984/8 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_404688294/ |
| 2.37 | メゾンアルマ | 2LDK | 53.55 | 110,000 | 10000 | 11万円(-) / 22万円 | 2.0 | 5/6 | Y | 1989/4 | RC | 近隣　28000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_385365398/ |
| 2.38 | ヴューキャッスル | 3DK | 62.59 | 105,000 | 10000 | 0円(-) / 0円 | 0.0 | 3/5 | Y | 1992/6 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_414597816/ |
| 2.38 | 大晋メゾネ西陣今出川 | 2SLDK | 65.55 | 125,000 | 9000 | 12.5万円(-) / 12.5万円 | 1.0 | 3/10 | Y | 1998/3 | SRC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_359332308/ |
| 2.38 | 大晋メゾネ西陣今出川 | 3LDK | 74.81 | 130,000 | 9000 | 13万円(-) / 13万円 | 1.0 | 5/10 | Y | 1998/4 | SRC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_392990826/ |
| 2.38 | リーガル京都二条城東 | 2LDK | 57.45 | 135,000 | 12180 | 0円(-) / 20万円 | 1.48 | 6/11 | Y | 2005/11 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_411552508/ |
| 2.38 | リーガル京都二条城東 | 2LDK | 57.45 | 138,000 | 12180 | 0円(-) / 26万円 | 1.88 | 2/11 | Y | 2005/11 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_403585018/ |
| 2.4 | 地下鉄東西線二条城前駅まで徒歩3分 | 3DK | 58.3 | 79,000 | 0 | 10万円(-) / 10万円 | 1.27 | None/2 | n | 1976/11 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414890180/ |
| 2.41 | エステムプラザ京都四条烏丸 | 2LDK | 53.42 | 140,000 | 15000 | 0円(-) / 1ヶ月 | 1.0 | 8/11 | Y | 2004/2 | SRC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413371846/ |
| 2.43 | ベルスーズ西陣 | 3LDK | 65.05 | 120,000 | 9500 | 39.03万円(-) / 0円 | 0.0 | 5/6 | Y | 1998/9 | RC | 空有　20000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_414178548/ |
| 2.43 | ベルスーズ西陣 | 3LDK | 65.05 | 120,000 | 9500 | 0円(-) / 0円 | 0.0 | 3/6 | Y | 1998/9 | RC | 空有　20000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_414179180/ |
| 2.44 | コスモ星の子ハイツ | 3DK | 56.0 | 90,000 | 9000 | 0円(-) / 9万円 | 1.0 | 4/7 | Y | 1985/9 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_398341850/ |
| 2.48 | ハイムフロイデン一乗寺 | 3LDK | 55.0 | 115,000 | 10000 | 0円(-) / 2ヶ月 | 2.0 | 4/6 | Y | 1984/1 | RC | 近隣　12000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_412564812/ |
| 2.48 | ハイムフロイデン一乗寺 | 3DK | 63.0 | 140,000 | 10000 | 0円(-) / 2ヶ月 | 2.0 | 6/6 | Y | 1984/1 | RC | 近隣　12000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_378863066/ |
| 2.49 | 藤原マンション | 2LDK | 45.0 | 90,000 | 5000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 1/3 | n | 1974/3 | RC | 空有　19800円 | old | https://sumaity.com/chintai/kyoto_prop/prop_370995306/ |
| 2.49 | ハイムフロイデン一乗寺 | 3DK | 51.0 | 100,000 | 10000 | 0円(-) / 2ヶ月 | 2.0 | 2/6 | Y | 1983/4 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_383283990/ |
| 2.49 | ハイムフロイデン一乗寺 | 2LDK | 50.0 | 100,000 | 10000 | 0円(-) / 2ヶ月 | 2.0 | 1/6 | Y | 1983/4 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414295306/ |
| 2.49 | ハイムフロイデン一乗寺 | 3LDK | 54.44 | 105,000 | 10000 | 0円(-) / 2ヶ月 | 2.0 | 4/6 | Y | 1983/4 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414295244/ |
| 2.49 | ハイムフロイデン一乗寺 | 3LDK | 60.0 | 130,000 | 10000 | 0円(-) / 2ヶ月 | 2.0 | 6/6 | Y | 1983/4 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414295050/ |
| 2.53 | ｗｉｔｈ京Ｇｒａｎｄｅｓ | 2LDK | 50.24 | 139,000 | 13000 | 13.9万円(-) / 20万円 | 1.44 | 1/5 | Y | 2019/1 | RC | 敷地内33000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_381852474/ |
| 2.55 | 烏丸線今出川駅まで徒歩18分 | 4DK | 65.0 | 105,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 1/3 | n | 1996/10 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414701250/ |
| 2.55 | ハイツ白川 | 3LDK | 70.69 | 90,000 | 10000 | 0円(-) / 0円 | 0.0 | 3/9 | Y | 1976/2 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_386665966/ |
| 2.55 | 京福電鉄北野線北野白梅町駅まで徒歩20分 | 3DK | 83.14 | 85,000 | 0 | 8.5万円(-) / 8.5万円 | 1.0 | 2/2 | n | 1976/1 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414556990/ |
| 2.56 | コーポシャルマン | 2LDK | 56.46 | 125,000 | 8000 | 12.5万円(-) / 12.5万円 | 1.0 | 2/4 | n | 1980/10 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_413333020/ |
| 2.57 | 地下鉄東西線二条城前駅まで徒歩4分 | 2LDK | 55.44 | 115,000 | 6500 | 11.5万円(-) / 11.5万円 | 1.0 | 3/10 | Y | 1989/3 | SRC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_411317590/ |
| 2.57 | コーポシャルマン | 2LDK | 61.65 | 140,000 | 8000 | 1ヶ月(-) / 2ヶ月 | 2.0 | 3/4 | n | 1980/10 | RC | 近隣　22000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_414061928/ |
| 2.58 | 烏丸線今出川駅まで徒歩18分 | 4DK | 95.0 | 105,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 1/3 | n | 1997/10 | 木造 | 近隣　16500円 | house | https://sumaity.com/chintai/kyoto_prop/prop_413050736/ |
| 2.58 | 地下鉄烏丸線今出川駅まで徒歩21分 | 4DK | 89.1 | 105,000 | 0 | 10.5万円(-) / 10.5万円 | 1.0 | 1/3 | n | 1997/10 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413091694/ |
| 2.58 | 地下鉄烏丸線今出川駅まで徒歩15分 | 4DK | 89.1 | 105,000 | 0 | 10.5万円(-) / 10.5万円 | 1.0 | 3/3 | n | 1996/10 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413039206/ |
| 2.58 | 阪急京都線京都河原町駅まで徒歩5分 | 2LDK | 61.65 | 140,000 | 8000 | 14万円(-) / 28万円 | 2.0 | 4/4 | n | 1989/3 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414807844/ |
| 2.59 | コト北小路 | 3LDK | 67.5 | 130,500 | 9500 | 1ヶ月(-) / 1ヶ月 | 1.0 | 7/9 | Y | 2001/2 | SRC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_409142966/ |
| 2.61 | 地下鉄烏丸線今出川駅まで徒歩19分 | 4LDK | 89.1 | 105,000 | 0 | 10.5万円(-) / 10.5万円 | 1.0 | 1/3 | n | 1996/10 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414616316/ |
| 2.61 | 一乗寺野田町テラスハウス中 | 2LDK | 71.54 | 138,000 | 0 | 1ヶ月(-) / 2ヶ月 | 2.0 | 1/2 | n | 2026/6 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_413637682/ |
| 2.62 | URESIDENCE二条城 | 2LDK | 50.04 | 114,000 | 9000 | 0円(-) / 1ヶ月 | 1.0 | 9/10 | Y | 1991/12 | SRC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_412788400/ |
| 2.62 | 叡電一乗寺駅まで徒歩13分 | 3DK | 51.0 | 70,000 | 0 | 7万円(-) / 0円 | 0.0 | None/2 | n | 1990/3 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_369987220/ |
| 2.62 | D-ROOM | 2LDK | 56.43 | 125,000 | 7000 | 0円(-) / 10万円 | 0.8 | 2/2 | n | 2025/10 | 軽量鉄骨 | 空無　13200円 | A | https://sumaity.com/chintai/kyoto_prop/prop_412143820/ |
| 2.62 | 叡電一乗寺駅まで徒歩12分 | 2LDK | 70.0 | 138,000 | 0 | 13.8万円(-) / 27.6万円 | 2.0 | None/2 | n | 2026/6 | 木造 | 空無 | house | https://sumaity.com/chintai/kyoto_prop/prop_413664526/ |
| 2.63 | メゾン・ド・プレパント | 3LDK | 76.78 | 140,000 | 5000 | 1ヶ月(-) / 1ヶ月 | 1.0 | 3/3 | n | 2002/4 | 鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_409753172/ |
| 2.64 | ポルトボヌール | 2LDK | 48.97 | 105,000 | 6900 | 0円(-) / 13万円 | 1.24 | 4/5 | n | 2016/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_411937058/ |
| 2.64 | ポルトボヌール | 2LDK | 48.97 | 105,000 | 6900 | 0円(-) / 10.5万円 | 1.0 | 3/5 | Y | 2016/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_411317242/ |
| 2.65 | 地下鉄烏丸線鞍馬口駅まで徒歩17分 | 2LDK | 51.0 | 116,000 | 7500 | 0円(-) / 11.6万円 | 1.0 | 4/5 | Y | 2015/8 | RC | 敷地内16500円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411207230/ |
| 2.65 | グレース北園 | 3DK | 72.42 | 140,000 | 10000 | 5万円(-) / 15万円 | 1.07 | 2/2 | n | 1988/3 | RC | 敷地内13000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_409918556/ |
| 2.65 | ルネ紫野 | 2LDK | 59.8 | 85,000 | 4000 | 5万円(-) / 10万円 | 1.18 | 2/2 | n | 2005/5 | 木造 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_405597406/ |
| 2.65 | 地下鉄烏丸線北大路駅まで徒歩8分 | 2LDK | 46.33 | 130,000 | 5000 | 0円(-) / 13万円 | 1.0 | 2/3 | n | 2022/11 | 木造 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414723156/ |
| 2.66 | セレーナ北大路 | 2LDK | 46.33 | 130,000 | 5000 | 0円(-) / 13万円 | 1.0 | 2/3 | n | 2023/1 | 木造 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414893824/ |
| 2.66 | グランメゾン上賀茂 | 2LDK | 50.86 | 65,000 | 5000 | 0円(-) / 0円 | 0.0 | 2/3 | n | 1993/1 | RC | 空有　5000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_354793754/ |
| 2.66 | 烏丸線北大路駅まで徒歩25分 | 3DK | 56.0 | 70,000 | 0 | 7万円(-) / 0円 | 0.0 | None/2 | n | 1980/3 | 木造 | 空有　11000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_413817710/ |
| 2.66 | ヴィレッヂ西賀茂 | 2LDK | 55.28 | 75,000 | 5000 | 7.5万円(-) / 7.5万円 | 1.0 | 2/4 | Y | 1994/5 | RC | 空有　13200円 | B | https://sumaity.com/chintai/kyoto_prop/prop_376888904/ |
| 2.66 | コアロード鷹ヶ峯 | 2LDK | 48.3 | 75,000 | 6000 | 10万円(-) / 0円 | 0.0 | 3/3 | n | 1994/1 | RC | 空無　10000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_389357522/ |
| 2.66 | 烏丸線北山駅まで徒歩45分 | 4DK | 65.0 | 75,000 | 1000 | 0円(-) / 5万円 | 0.67 | None/2 | n | 1989/7 | 木造 | 空有　5000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_387014454/ |
| 2.66 | メゾンミソノ | 3LDK | 50.0 | 78,000 | 12000 | 0円(-) / 7.8万円 | 1.0 | 5/6 | Y | 1984/5 | RC | 空無　12600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_314444686/ |
| 2.66 | メゾンミソノ | 3LDK | 64.0 | 78,000 | 12000 | 0円(-) / 7.8万円 | 1.0 | 1/6 | Y | 1984/5 | RC | 空無　12600円 | old | https://sumaity.com/chintai/kyoto_prop/prop_412435108/ |
| 2.66 | 烏丸線北大路駅まで徒歩32分 | 5LDK | 105.02 | 100,000 | 0 | 0円(-) / 10万円 | 1.0 | None/3 | n | 1991/9 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_412948234/ |
| 2.66 | フェリス紫竹 | 2LDK | 73.94 | 125,000 | 5000 | 7.2万円(-) / 0円 | 0.0 | 2/2 | n | 2016/9 | 鉄骨 | 空有　16500円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414424996/ |
| 2.66 | グランメゾン | 2LDK | 60.0 | 125,000 | 8000 | 5万円(-) / 18.7万円 | 1.5 | 1/3 | n | 2026/9 | 鉄骨 | 空有　12100円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414773966/ |
| 2.66 | グランメゾン | 2LDK | 60.14 | 125,000 | 8000 | 5万円(-) / 18.7万円 | 1.5 | 1/3 | n | 2026/9 | 鉄骨 | 空有　12100円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414773822/ |
| 2.66 | グランメゾン | 2LDK | 60.0 | 128,000 | 8000 | 5万円(-) / 18.6万円 | 1.45 | 2/3 | n | 2026/9 | 鉄骨 | 空有　12100円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414773962/ |
| 2.66 | グランメゾン | 2LDK | 60.14 | 128,000 | 8000 | 5万円(-) / 18.6万円 | 1.45 | 2/3 | n | 2026/9 | 鉄骨 | 空有　12100円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414774014/ |
| 2.66 | シャーメゾン | 2LDK | 63.7 | 129,000 | 9500 | 0円(-) / 25万円 | 1.94 | 1/3 | Y | 2026/1 | 鉄骨 | 空無　12100円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414244494/ |
| 2.66 | 烏丸線北大路駅まで徒歩11分 | 3LDK | 82.0 | 130,000 | 0 | 13万円(-) / 13万円 | 1.0 | None/2 | n | 1988/1 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_403155554/ |
| 2.66 | グランメゾン | 2LDK | 60.0 | 131,000 | 8000 | 5万円(-) / 18.4万円 | 1.4 | 3/3 | n | 2026/9 | 鉄骨 | 空有　12100円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414773938/ |
| 2.66 | グランメゾン | 2LDK | 60.14 | 131,000 | 8000 | 5万円(-) / 18.4万円 | 1.4 | 3/3 | n | 2026/9 | 鉄骨 | 空有　12100円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414773886/ |
| 2.66 | コテージ玄琢 | 3LDK | 91.08 | 134,000 | 0 | 0円(-) / 13.4万円 | 1.0 | None/2 | n | 1988/3 | RC | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_414132174/ |
| 2.66 | グランメゾン | 2LDK | 63.84 | 135,000 | 8000 | 5万円(-) / 18.2万円 | 1.35 | 3/3 | n | 2026/9 | 鉄骨 | 空有　12100円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414774004/ |
| 2.66 | グランメゾン | 2LDK | 66.94 | 138,000 | 8000 | 5万円(-) / 18.1万円 | 1.31 | 2/3 | n | 2026/9 | 鉄骨 | 空有　12100円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414773946/ |
| 2.67 | 地下鉄烏丸線北大路駅まで徒歩6分 | 3LDK | 65.8 | 98,000 | 0 | 0円(-) / 19.6万円 | 2.0 | None/2 | n | 1960/12 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413889834/ |
| 2.69 | メガロコープ西陣A棟 | 3LDK | 58.44 | 110,000 | 0 | 0円(-) / 11万円 | 1.0 | 5/11 | Y | 1972/6 | SRC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_371950728/ |
| 2.69 | 山陰線二条駅まで徒歩10分 | 2LDK | 59.5 | 95,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 1/2 | n | 1970/1 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414701282/ |
| 2.7 | メガロコープ西陣A棟 | 4LDK | 58.44 | 110,000 | 0 | 0円(-) / 1ヶ月 | 1.0 | 5/13 | Y | 1972/6 | SRC | 近隣　15000円 | old | https://sumaity.com/chintai/kyoto_prop/prop_371622398/ |
| 2.7 | 阪急京都線京都河原町駅まで徒歩5分 | 3LDK | 56.99 | 140,000 | 13300 | 28万円(-) / 28万円 | 2.0 | 3/11 | Y | 2001/6 | SRC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413282156/ |
| 2.7 | シンフォニー四条河原町 | 2LDK | 53.46 | 130,000 | 20820 | 13万円(-) / 26万円 | 2.0 | 3/10 | Y | 2001/10 | SRC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_396592792/ |
| 2.7 | シンフォニー四条河原町 | 3LDK | 56.99 | 140,000 | 13300 | 28万円(-) / 28万円 | 2.0 | 3/10 | Y | 2001/10 | SRC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_411278274/ |
| 2.71 | 藤和シティホームズ三条堀川 | 2LDK | 58.72 | 135,000 | 10000 | 13.5万円(-) / 27万円 | 2.0 | 6/11 | Y | 1997/3 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_266832502/ |
| 2.71 | シンフォニー四条河原町 | 2LDK | 53.46 | 130,000 | 20820 | 13万円(-) / 26万円 | 2.0 | 3/11 | Y | 2001/6 | SRC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_395537968/ |
| 2.72 | 詩仙ハイム | 2LDK | 47.0 | 90,000 | 5000 | 9万円(-) / 9万円 | 1.0 | 3/4 | n | 1979/6 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_409005130/ |
| 2.73 | ペレニアルフラックス | 2LDK | 75.5 | 120,000 | 6000 | 12万円(-) / 12万円 | 1.0 | 2/3 | n | 1992/8 | RC | 敷地内15400円 | B | https://sumaity.com/chintai/kyoto_prop/prop_301648575/ |
| 2.75 | Uresidence二条城 | 2LDK | 50.04 | 120,000 | 9000 | 0円(-) / 12万円 | 1.0 | 4/10 | Y | 1991/12 | SRC | 近隣170m18000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_412259678/ |
| 2.75 | 地下鉄東西線二条駅まで徒歩11分 | 2LDK | 59.5 | 95,000 | 0 | 9.5万円(-) / 9.5万円 | 1.0 | 1/2 | n | 1965/11 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_410619712/ |
| 2.76 | せんぼん有彩館 | 3LDK | 71.2 | 132,000 | 15000 | 0円(-) / 0円 | 0.0 | 2/10 | Y | 1997/8 | SRC | 敷地内25300円 | B | https://sumaity.com/chintai/kyoto_prop/prop_409030440/ |
| 2.76 | せんぼん有彩館 | 3LDK | 71.2 | 133,000 | 15000 | 0円(-) / 0円 | 0.0 | 3/10 | Y | 1997/9 | SRC | 敷地内25300円 | B | https://sumaity.com/chintai/kyoto_prop/prop_410479196/ |
| 2.76 | せんぼん有彩館 | 3LDK | 71.2 | 134,000 | 15000 | 0円(-) / 0円 | 0.0 | 5/10 | Y | 1997/9 | SRC | 敷地内25300円 | B | https://sumaity.com/chintai/kyoto_prop/prop_409030444/ |
| 2.76 | De′lead今出川通 | 3LDK | 63.72 | 110,000 | 10000 | 5万円(-) / 15万円 | 1.36 | 10/11 | Y | 1995/10 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_412781588/ |
| 2.8 | STANDZ京都二条 | 2LDK | 48.33 | 135,000 | 20000 | 6.75万円(-) / 0円 | 0.0 | 2/7 | Y | 2026/1 | RC | 近隣　16500円 | A | https://sumaity.com/chintai/kyoto_prop/prop_404659820/ |
| 2.81 | ＳＡＫＩＺＯＶｉｌｌａ烏丸四条 | 3LDK | 54.55 | 120,000 | 9000 | 0円(-) / 2ヶ月 | 2.0 | 5/10 | Y | 1981/5 | RC | 空有　40700円 | old | https://sumaity.com/chintai/kyoto_prop/prop_410365684/ |
| 2.82 | 地下鉄烏丸線鞍馬口駅まで徒歩17分 | 3LDK | 87.09 | 100,000 | 0 | 20万円(-) / 10万円 | 1.0 | 1/2 | n | 1920/1 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_412187540/ |
| 2.83 | ユアメゾン白川1 | 2LDK | 63.0 | 125,000 | 6000 | 12.5万円(-) / 25万円 | 2.0 | 2/2 | n | 2026/10 | 軽量鉄骨 | 敷地内15400円 | A | https://sumaity.com/chintai/kyoto_prop/prop_413423212/ |
| 2.83 | Weaving | 2LDK | 56.2 | 125,000 | 6000 | 12.5万円(-) / 18.75万円 | 1.5 | 3/3 | n | 2027/2 | 木造 | 敷地内16500円 | A | https://sumaity.com/chintai/kyoto_prop/prop_414682188/ |
| 2.83 | Weaving | 2LDK | 56.2 | 125,000 | 6000 | 12.5万円(-) / 18.75万円 | 1.5 | 2/3 | n | 2027/2 | 木造 | 敷地内16500円/駐2台可 | A | https://sumaity.com/chintai/kyoto_prop/prop_414682128/ |
| 2.83 | ラスパルマス京小町 | 2LDK | 54.86 | 135,000 | 10000 | 0円(-) / 13.5万円 | 1.0 | 2/5 | Y | 2025/6 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_382387804/ |
| 2.84 | メゾン洛北 | 3LDK | 67.16 | 115,000 | 8000 | 10万円(-) / 25万円 | 2.17 | 5/7 | Y | 1971/11 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_303499925/ |
| 2.84 | 嶋津マンション | 3LDK | 60.0 | 125,000 | 10000 | 12.5万円(-) / 12.5万円 | 1.0 | 4/7 | Y | 1991/7 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_413026414/ |
| 2.84 | 嶋津マンション | 3LDK | 74.0 | 125,000 | 10000 | 12.5万円(-) / 12.5万円 | 1.0 | 4/7 | Y | 1991/4 | RC | 近隣400m30000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_352394660/ |
| 2.85 | D-ROOM 一乗寺 | 2LDK | 52.79 | 136,000 | 8000 | 0円(-) / 13.6万円 | 1.0 | 2/3 | n | 2024/10 | 軽量鉄骨 | 敷地内14300円 | A | https://sumaity.com/chintai/kyoto_prop/prop_413167848/ |
| 2.85 | 西陣グランドハイツ | 4LDK | 62.78 | 100,000 | 10000 | 10万円(-) / 10万円 | 1.0 | 3/8 | Y | 1975/4 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414723026/ |
| 2.85 | カーサ葵 | 3LDK | 68.14 | 140,000 | 10000 | 14万円(-) / 14万円 | 1.0 | 3/3 | Y | 2001/4 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_407859426/ |
| 2.85 | 阪急京都線大宮駅まで徒歩7分 | 3LDK | 68.14 | 140,000 | 10000 | 14万円(-) / 14万円 | 1.0 | 2/3 | n | 2001/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_408724552/ |
| 2.86 | ヴァンヴェールII | 2LDK | 53.87 | 90,000 | 3000 | 0円(-) / 20万円 | 2.22 | 2/2 | n | 1999/1 | 軽量鉄骨 | 空有　10000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_354777492/ |
| 2.86 | 洛翠舎 | 3LDK | 69.4 | 128,000 | 0 | 1ヶ月(-) / 2ヶ月 | 2.0 | 8/9 | Y | 2001/2 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_332177298/ |
| 2.86 | 洛翠舎 | 3LDK | 69.26 | 128,000 | 11000 | 1ヶ月(-) / 2ヶ月 | 2.0 | 4/9 | Y | 2001/2 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_411817272/ |
| 2.87 | D-ROOM一乗寺 | 2LDK | 52.79 | 134,000 | 8000 | 0円(-) / 13.4万円 | 1.0 | 1/3 | n | 2024/10 | 軽量鉄骨 | 空有　14300円 | A | https://sumaity.com/chintai/kyoto_prop/prop_410293764/ |
| 2.9 | コスモトゥデイ | 2LDK | 61.64 | 120,000 | 0 | 12万円(-) / 24万円 | 2.0 | 11/11 | Y | 1989/11 | SRC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_412015896/ |
| 2.9 | シャトレ西陣 | 2LDK | 45.0 | 90,000 | 5000 | 0円(-) / 9万円 | 1.0 | 7/7 | Y | 1974/4 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414808598/ |
| 2.91 | ティファール | 3LDK | 69.35 | 140,000 | 11000 | 5万円(-) / 20万円 | 1.43 | 6/10 | Y | 1999/9 | SRC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_374763954/ |
| 2.92 | ティファール | 3LDK | 69.08 | 138,000 | 11000 | 5万円(-) / 20万円 | 1.45 | 6/10 | Y | 1999/8 | RC | 空有　30800円 | B | https://sumaity.com/chintai/kyoto_prop/prop_413455230/ |
| 2.93 | シャーメゾン京都六角大宮 | 2LDK | 59.5 | 140,000 | 8000 | 3万円(-) / 28万円 | 2.0 | 2/3 | Y | 2022/3 | 鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413515158/ |
| 2.93 | サンパティ | 3LDK | 68.0 | 122,000 | 5000 | 12.2万円(-) / 12.2万円 | 1.0 | 2/2 | n | 1993/3 | 木造 | 敷地内15000円/平置駐 | B | https://sumaity.com/chintai/kyoto_prop/prop_413199356/ |
| 2.94 | コスモ二条 | 2LDK | 55.0 | 82,000 | 8000 | 10万円(-) / 15万円 | 1.83 | 5/11 | Y | 1985/11 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_411904896/ |
| 2.95 | 地下鉄烏丸線鞍馬口駅まで徒歩18分 | 5DK | 77.8 | 110,000 | 0 | 11万円(-) / 11万円 | 1.0 | 1/2 | n | 1970/1 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_412544108/ |
| 2.95 | 観タワーハウス | 2LDK | 46.01 | 95,000 | 0 | 10万円(-) / 10万円 | 1.05 | 4/10 | Y | 1987/4 | SRC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_311818851/ |
| 2.96 | シャトレ西陣 | 2LDK | 45.38 | 90,000 | 5000 | 0円(-) / 9万円 | 1.0 | 7/7 | Y | 1976/4 | RC | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_414808600/ |
| 2.98 | 叡電一乗寺駅まで徒歩9分 | 2LDK | 45.0 | 75,000 | 0 | 0円(-) / 13万円 | 1.73 | 1/2 | n | 1970/3 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413639136/ |
| 3.0 | 四条大宮シャトー朝日 | 2LDK | 53.28 | 100,000 | 10000 | 10万円(-) / 20万円 | 2.0 | 10/11 | Y | 1991/1 | SRC | 空無　26000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_410623778/ |
| 3.0 | De′lead四条大宮 | 3LDK | 60.68 | 113,000 | 7000 | 10万円(-) / 40万円 | 3.54 | 3/7 | Y | 1994/10 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_405410782/ |
| 3.0 | R-Grants大宮五条 | 2LDK | 75.0 | 130,000 | 10000 | 0円(-) / 13万円 | 1.0 | 7/5 | Y | 1985/10 | 鉄骨 | なし | old | https://sumaity.com/chintai/kyoto_prop/prop_404492256/ |
| 3.09 | ビラ妙松館 | 2LDK | 70.32 | 136,000 | 12000 | 13.6万円(-) / 13.6万円 | 1.0 | 1/4 | Y | 1997/9 | RC | 空有　14700円 | B | https://sumaity.com/chintai/kyoto_prop/prop_405637232/ |
| 3.11 | クレール井ノ口 A.B | 2LDK | 50.0 | 70,000 | 4000 | 0円(-) / 0円 | 0.0 | 1/2 | n | 2001/7 | 軽量鉄骨 | 空有　7000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411817240/ |
| 3.11 | ハイツやすらい | 2LDK | 52.84 | 85,000 | 5000 | 0円(-) / 17万円 | 2.0 | 2/2 | n | 1999/1 | 軽量鉄骨 | 空有　7700円 | B | https://sumaity.com/chintai/kyoto_prop/prop_402416462/ |
| 3.11 | ハイツやすらい | 2LDK | 52.84 | 85,000 | 5000 | 0円(-) / 17万円 | 2.0 | 1/2 | n | 1999/1 | 軽量鉄骨 | 空有　7700円 | B | https://sumaity.com/chintai/kyoto_prop/prop_402416418/ |
| 3.11 | ドミールカンザカ | 2LDK | 46.11 | 90,000 | 3000 | 3万円(-) / 10万円 | 1.11 | 2/2 | n | 1989/11 | 軽量鉄骨 | 空有　7700円 | old | https://sumaity.com/chintai/kyoto_prop/prop_399083522/ |
| 3.11 | パークアベニュー北山 | 2LDK | 52.25 | 93,000 | 3000 | 5万円(-) / 20万円 | 2.15 | 1/2 | n | 2008/11 | 軽量鉄骨 | 空有　12000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_365074088/ |
| 3.11 | Verde | 3DK | 59.1 | 96,000 | 3000 | 10万円(-) / 10万円 | 1.04 | 2/2 | n | 2001/3 | 軽量鉄骨 | 空有 | A | https://sumaity.com/chintai/kyoto_prop/prop_412063124/ |
| 3.11 | 烏丸線北山駅まで徒歩19分 | 4DK | 72.71 | 102,000 | 0 | 10.2万円(-) / 10.2万円 | 1.0 | None/2 | n | 1986/5 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_413721562/ |
| 3.11 | フレグランス上賀茂 | 2LDK | 59.0 | 103,000 | 4000 | 0円(-) / 15万円 | 1.46 | 2/2 | n | 1989/8 | 軽量鉄骨 | 空有　9900円 | old | https://sumaity.com/chintai/kyoto_prop/prop_413893738/ |
| 3.11 | ジェンティール北山 | 2LDK | 59.0 | 109,000 | 5000 | 0円(-) / 25万円 | 2.29 | 1/2 | n | 2002/2 | 軽量鉄骨 | 空有　11000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_413300188/ |
| 3.11 | 正和フラット上賀茂 | 2LDK | 65.1 | 110,000 | 10000 | 11万円(-) / 11万円 | 1.0 | 1/4 | n | 1992/11 | RC | 空有　11000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_414697256/ |
| 3.11 | メゾン・サンマルタン | 2LDK | 60.18 | 114,000 | 11000 | 11.4万円(-) / 11.4万円 | 1.0 | 2/4 | Y | 1995/11 | RC | 空有　11000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_406745228/ |
| 3.11 | メゾン・サンマルタン | 2LDK | 60.18 | 115,000 | 11000 | 11.5万円(-) / 11.5万円 | 1.0 | 3/4 | Y | 1995/11 | RC | 空有　11000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_410500274/ |
| 3.11 | ファミール北山 | 3LDK | 65.27 | 117,500 | 7500 | 11.75万円(-) / 11.75万円 | 1.0 | 2/2 | n | 2002/4 | RC | 空有　9900円 | A | https://sumaity.com/chintai/kyoto_prop/prop_406370908/ |
| 3.11 | シャーメゾン北山上賀茂 | 2LDK | 56.1 | 130,000 | 5000 | 0円(-) / 20万円 | 1.54 | 1/3 | n | 2022/3 | 鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413683384/ |
| 3.13 | 京都グランデ二条駅南 | 2LDK | 48.07 | 133,000 | 0 | 0円(-) / 5万円 | 0.38 | 2/3 | n | 2023/6 | 木造 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_414699822/ |
| 3.2 | 嵐電北野線北野白梅町駅まで徒歩15分 | 3LDK | 62.09 | 95,000 | 0 | 1ヶ月(-) / 1ヶ月 | 1.0 | 1/2 | n | 1975/12 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414701256/ |
| 3.2 | 山陰線二条駅まで徒歩8分 | 4DK | 80.1 | 120,000 | 0 | 12万円(-) / 12万円 | 1.0 | None/3 | n | 1995/2 | 鉄骨 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_412700476/ |
| 3.2 | ビオラ朱雀大路 | 2LDK | 53.03 | 127,000 | 11000 | 0円(-) / 25万円 | 1.97 | 1/3 | n | 2021/4 | 軽量鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_413003822/ |
| 3.2 | セントリヴィエ二条 | 2LDK | 55.83 | 132,000 | 8000 | 13.2万円(-) / 26.4万円 | 2.0 | 1/6 | Y | 2015/7 | RC | 空無　20000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_412225326/ |
| 3.32 | 叡電修学院駅まで徒歩8分 | 4DK | 72.1 | 85,000 | 0 | 17万円(-) / 0円 | 0.0 | None/2 | n | 1987/9 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_404247626/ |
| 3.32 | 叡電修学院駅まで徒歩8分 | 3SLDK | 60.34 | 89,000 | 0 | 8.9万円(-) / 17.8万円 | 2.0 | None/2 | n | 1985/4 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_353070982/ |
| 3.32 | U residence修学院 | 3LDK | 63.3 | 110,000 | 5000 | 11万円(-) / 0円 | 0.0 | 5/5 | Y | 1997/9 | RC | 空有　16500円 | B | https://sumaity.com/chintai/kyoto_prop/prop_405247048/ |
| 3.32 | U residence修学院 | 3LDK | 63.3 | 110,000 | 5000 | 11万円(-) / 0円 | 0.0 | 3/5 | Y | 1997/9 | RC | 空有　16500円 | B | https://sumaity.com/chintai/kyoto_prop/prop_413097148/ |
| 3.42 | バインオークCENT | 2LDK | 47.71 | 140,000 | 12000 | 0円(-) / 14万円 | 1.0 | 5/5 | Y | 2004/3 | 鉄骨 | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_409005814/ |
| 3.89 | サンビレッジ大北山 | 2LDK | 52.84 | 69,000 | 3000 | 0円(-) / 0円 | 0.0 | 2/2 | n | 1995/4 | 軽量鉄骨 | 空有　6000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_413003810/ |
| 3.89 | 烏丸線北大路駅まで徒歩60分 | 3LDK | 59.52 | 70,000 | 0 | 0円(-) / 0円 | 0.0 | None/3 | n | 1989/7 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_414661726/ |
| 3.89 | Arietta | 2LDK | 53.9 | 79,000 | 5000 | 7.9万円(-) / 0円 | 0.0 | 1/2 | n | 2025/7 | 木造 | 空有　5500円 | A | https://sumaity.com/chintai/kyoto_prop/prop_399796820/ |
| 3.89 | 嵐電北野線北野白梅町駅まで徒歩39分 | 4DK | 109.34 | 80,000 | 5000 | 8万円(-) / 0円 | 0.0 | None/3 | n | 1987/12 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_412621850/ |
| 3.89 | 嵐電北野線北野白梅町駅まで徒歩13分 | 5K | 68.19 | 98,000 | 0 | 18万円(-) / 12万円 | 1.22 | None/2 | n | 1997/10 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_411676804/ |
| 3.89 | Cave | 2LDK | 58.56 | 115,000 | 5500 | 0円(-) / 15万円 | 1.3 | 1/3 | n | 2017/10 | 鉄骨 | 空無　14300円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411223028/ |
| 3.89 | 嵐電北野線北野白梅町駅まで徒歩15分 | 3DK | 58.0 | 128,000 | 0 | 12.8万円(-) / 12.8万円 | 1.0 | None/2 | n | 2004/5 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414137820/ |
| 3.92 | 山陰線円町駅まで徒歩16分 | 2LDK | 57.38 | 100,000 | 0 | 5万円(-) / 10万円 | 1.0 | None/2 | n | 2004/5 | 軽量鉄骨 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414376620/ |
| 5.36 | 嵐電北野線御室仁和寺駅まで徒歩34分 | 3DK | 53.41 | 55,000 | 0 | 5万円(-) / 0円 | 0.0 | None/2 | n | 1981/3 | 木造 | なし | house | https://sumaity.com/chintai/kyoto_prop/prop_414741538/ |
| 5.6 | ファミーリャ・フェリーチェ八瀬I・II | 3LDK | 60.0 | 80,000 | 3000 | 0円(-) / 8万円 | 1.0 | None/2 | n | 2021/12 | 木造 | 空有　5500円 | house | https://sumaity.com/chintai/kyoto_prop/prop_414619006/ |
| 6.05 | 三宅タウンA | 3SDK | 69.0 | 110,000 | 0 | 11万円(-) / 11万円 | 1.0 | None/2 | n | 1995/5 | 木造 | 空有 | house | https://sumaity.com/chintai/kyoto_prop/prop_413097046/ |
| None | 叡電修学院駅まで徒歩14分 | 4LDK | 76.01 | 78,000 | 0 | 7.8万円(-) / 7.8万円 | 1.0 | None/2 | n | 1986/10 | 木造 | 空無 | house | https://sumaity.com/chintai/kyoto_prop/prop_410882882/ |
| None | FAMILLE | 2LDK | 61.91 | 133,000 | 9000 | 0円(-) / 20万円 | 1.5 | 1/2 | n | 2026/11 | 軽量鉄骨 | 空有　8800円 | A | https://sumaity.com/chintai/kyoto_prop/prop_409575108/ |
| None | FAMILLE | 2LDK | 61.11 | 135,000 | 9000 | 0円(-) / 20万円 | 1.48 | 1/2 | n | 2026/11 | 軽量鉄骨 | 空有　8800円 | A | https://sumaity.com/chintai/kyoto_prop/prop_409575078/ |
| None | FAMILLE | 2LDK | 64.61 | 133,000 | 9000 | 0円(-) / 20万円 | 1.5 | 1/2 | n | 2026/11 | 軽量鉄骨 | 空有　8800円 | A | https://sumaity.com/chintai/kyoto_prop/prop_409530024/ |
| None | FAMILLE | 2LDK | 64.12 | 137,000 | 9000 | 0円(-) / 20万円 | 1.46 | 1/2 | n | 2026/11 | 軽量鉄骨 | 空有　8800円 | A | https://sumaity.com/chintai/kyoto_prop/prop_409575186/ |
| None | 鷹峯旧土居町貸家 | 4SLDK | 120.14 | 80,000 | 0 | 0円(-) / 12万円 | 1.5 | None/3 | n | 1990/7 | 木造 | 空無 | house | https://sumaity.com/chintai/kyoto_prop/prop_409858084/ |
