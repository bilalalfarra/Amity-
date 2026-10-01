# sumaity — スマイティ (sumaity.com), fetched 2026-10-01

## Method
- Server-side filters via https://sumaity.com/chintai/area_list/list.php: acity_id (ward), madori[]=2LDK/3DK/3LDK/4DK/4LDK以上 (2DK, 2K excluded by the site; 2SLDK/3SLDK come through as 2LDK/3LDK variants), price_high=100000, foot_print_low=45. No server-side filter for floor / elevator / 礼金 / built-year tier (the site offers build_date=25年以内 but tier B needs 26–35 y, so age was filtered client-side).
- Wards scanned: 下京(28), 中京(40), 南(139), 右京(326), 上京(22), 西京(319), 東山(12), 北(151), 伏見(509) room-listings = 1546 unique rooms over 44 list pages (30 buildings/page). Raw list pages: out/raw/sumaity/list_<ward>_p<N>.html; detail pages: out/raw/sumaity/detail/prop_<id>.html.
- Client-side funnel: age/structure tier fail 1086 (築26+ non-RC or 築36+), 1F 105, >5.5 km 155 → 200 candidates → fetched all 200 detail pages (HTTP 200) → applied 礼金≤1ヶ月 (−62), 4F+ without elevator / 1F (−3) → **135 kept**.
- Kept by tier: {'house': 3, 'B': 116, 'A': 16}; elevator yes/no: {False: 40, True: 95}; by ward: {'下京区': 4, '中京区': 2, '右京区': 25, '南区西': 1, '南区': 3, '南区吉': 8, '南区上': 4, '西京区': 41, '東山区': 1, '南区久': 30, '伏見区': 10, '北区衣': 3, '北区': 3}.
- Geocoding: GSI geocoder on the town-level address shown on the list card (sumaity hides block numbers), so distances are town-centroid accuracy (±300 m).
- Caveats: sumaity aggregates several agencies; the same room can appear under several bldg/prop IDs with different 礼金 — duplicates of the same unit (same building+floor+area) are possible. `agency` is often null because the detail page lists multiple handling agencies (captured in raw HTML). 仲介手数料/保証会社 are 'ask the agency' on this site. Listings titled '[あとN日]' expire in N days.

## Best examples (closest first, tier A = built 2001+, B = 1991–2000 RC/SRC)
| km | building | layout | m² | rent | 管理費 | 敷/礼 | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.4 | ＪＲ山陰本線丹波口駅まで徒歩7分 | 2LDK | 48.0 | 95,000 | 3000 | 9.5万円(-)/0円 | 1/2 | n | 2003/3 | 木造 | 近隣400m18000円 | house | https://sumaity.com/chintai/kyoto_prop/prop_412430370/ |
| 0.78 | グランベール西七条 | 2LDK | 52.16 | 98,000 | 8000 | 0円(-)/0円 | 7/8 | Y | 1996/3 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_410073068/ |
| 0.87 | アリコス壬生 | 2LDK | 54.0 | 98,000 | 8000 | 10万円(-)/0円 | 2/10 | Y | 2002/3 | RC | なし | A | https://sumaity.com/chintai/kyoto_prop/prop_342919570/ |
| 0.98 | ブランシェ八甲 | 2LDK | 47.0 | 75,000 | 9000 | 1ヶ月(-)/1ヶ月 | 5/5 | Y | 1992/10 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_411661592/ |
| 1.36 | グラン・フォルム西院 | 2LDK | 48.33 | 85,000 | 9000 | 0円(-)/8.5万円 | 4/6 | Y | 1992/3 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_410500356/ |
| 1.43 | ＪＲ東海道本線西大路駅まで徒歩13分 | 3DK | 62.66 | 89,000 | 0 | 0円(-)/8.9万円 | 1/3 | n | 2007/9 | 木造 | 付無料 | house | https://sumaity.com/chintai/kyoto_prop/prop_261580622/ |
| 1.56 | ノブレカーサ西院 | 3LDK | 65.92 | 99,000 | 5000 | 0円(-)/1ヶ月 | 5/6 | Y | 2002/8 | RC | 近隣　16500円 | A | https://sumaity.com/chintai/kyoto_prop/prop_413105962/ |
| 1.56 | ノブレカーサ西院 | 3LDK | 65.92 | 95,000 | 5000 | 1ヶ月(-)/1ヶ月 | 5/6 | Y | 2002/8 | RC | - | A | https://sumaity.com/chintai/kyoto_prop/prop_413105824/ |
| 2.05 | プレジオ東寺 | 2SLDK | 57.8 | 99,000 | 8000 | 0円(-)/0円 | 6/6 | Y | 1997/2 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_409142770/ |
| 2.12 | [あと6日]クレアール弐番館 | 2LDK | 48.6 | 77,000 | 5000 | 5万円(-)/7.7万円 | 4/6 | Y | 1998/5 | RC | 空有　11000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_411544806/ |
| 2.12 | カサ・デ・高ノ手 | 2LDK | 56.7 | 100,000 | 0 | 5万円(-)/10万円 | 5/7 | Y | 1995/3 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_411957052/ |
| 2.12 | カサ・デ・高ノ手 | 2LDK | 56.7 | 100,000 | 0 | 5万円(-)/10万円 | 4/7 | Y | 1995/3 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_411957196/ |
| 2.16 | スクリーン７７ | 2LDK | 52.8 | 94,000 | 9000 | 9.4万円(-)/9.4万円 | 5/6 | Y | 1997/3 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_412125036/ |
| 2.25 | クレアール弐番館 | 2LDK | 48.6 | 77,000 | 5000 | 5万円(-)/7.7万円 | 4/6 | Y | 1998/4 | RC | 敷地内11000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_411580604/ |
| 2.42 | クレアール弐番館 | 2LDK | 48.6 | 77,000 | 5000 | 5万円(-)/7.7万円 | 4/6 | Y | 1998/4 | RC | 敷地内11000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_411517040/ |
| 2.42 | ＪＲ東海道本線西大路駅まで徒歩9分 | 2LDK | 48.6 | 77,000 | 5000 | 5万円(-)/7.7万円 | 4/6 | Y | 1998/5 | RC | 敷地内14700円 | B | https://sumaity.com/chintai/kyoto_prop/prop_411580606/ |
| 2.53 | グランビュー葛野 | 2LDK | 57.51 | 84,000 | 10000 | 8.4万円(-)/8.4万円 | 3/4 | Y | 1997/2 | RC | 敷地内10000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_261991446/ |
| 2.56 | コンフォール | 3LDK | 65.0 | 89,000 | 9500 | 0円(-)/8.9万円 | 5/7 | Y | 1995/10 | RC | 敷地内11000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_412893644/ |
| 2.56 | コンフォール | 2LDK | 65.16 | 89,000 | 9500 | 0円(-)/8.9万円 | 5/7 | Y | 1995/10 | RC | 敷地内12100円/平置駐 | B | https://sumaity.com/chintai/kyoto_prop/prop_412920456/ |
| 2.56 | コンフォール | 2LDK | 65.16 | 89,000 | 9500 | 0円(-)/8.9万円 | 3/7 | Y | 1995/10 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_412893680/ |
| 2.56 | 近鉄京都線十条駅まで徒歩11分 | 3LDK | 65.0 | 89,000 | 9500 | 0円(-)/8.9万円 | 5/7 | Y | 1995/10 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_413754372/ |
| 2.67 | サニークレスト祥山 | 3LDK | 60.96 | 80,000 | 9000 | 8万円(-)/8万円 | 3/7 | Y | 1999/12 | RC | 敷地内13200円 | B | https://sumaity.com/chintai/kyoto_prop/prop_412711816/ |
| 2.67 | ＪＲ東海道本線西大路駅までバス約5分 | 3LDK | 60.96 | 80,000 | 9000 | 8万円(-)/8万円 | 3/7 | Y | 1999/3 | RC | 敷地内13200円 | B | https://sumaity.com/chintai/kyoto_prop/prop_412821968/ |
| 2.77 | [あと6日]広沢市営住宅 | 3DK | 61.5 | 65,000 | 7000 | 0円(-)/0円 | 3/6 | Y | 1994/1 | RC | 空有　7000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_387249468/ |
| 2.77 | [あと6日]大覚寺市営住宅 | 3DK | 61.5 | 65,000 | 5000 | 0円(-)/0円 | 3/3 | n | 1994/1 | RC | 空有　5000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_390364198/ |
| 2.77 | [あと6日]山陰線花園駅まで徒歩2分 | 2LDK | 57.75 | 85,000 | 0 | 0円(-)/8.5万円 | None/3 | n | 1991/12 | RC | 空有 | B | https://sumaity.com/chintai/kyoto_prop/prop_413817702/ |
| 2.77 | [あと6日]山陰線花園駅まで徒歩2分 | 2LDK | 57.75 | 85,000 | 0 | 0円(-)/0円 | None/3 | n | 1991/12 | RC | 空有 | B | https://sumaity.com/chintai/kyoto_prop/prop_413163210/ |
| 2.88 | グレース吉祥 | 3LDK | 64.25 | 84,000 | 9000 | 20万円(-)/0円 | 6/6 | Y | 2000/3 | RC | - | B | https://sumaity.com/chintai/kyoto_prop/prop_286322667/ |
| 2.88 | グレース吉祥 | 3LDK | 63.58 | 84,000 | 9000 | 20万円(-)/0円 | 6/6 | Y | 2000/12 | RC | 敷地内11000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_413925250/ |
| 2.95 | イーズコート桂２ | 2LDK | 68.59 | 98,000 | 0 | 0円(-)/0円 | 2/2 | n | 2003/11 | 軽量鉄骨 | 近隣200m10000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411289626/ |
| 2.99 | Rosy Garden | 2LDK | 51.17 | 87,000 | 8000 | 8.7万円(-)/8.7万円 | 3/3 | n | 1994/5 | RC | なし | B | https://sumaity.com/chintai/kyoto_prop/prop_412485678/ |
| 3.0 | パラッツォ桂 | 3LDK | 67.17 | 85,000 | 12000 | 8.5万円(-)/8.5万円 | 4/6 | Y | 1993/6 | RC | 敷地内8000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_408281284/ |
| 3.05 | フェアリージャム | 2LDK | 56.4 | 100,000 | 10000 | 15万円(-)/0円 | 2/6 | Y | 1996/11 | RC | 空有　16500円 | B | https://sumaity.com/chintai/kyoto_prop/prop_243913751/ |
| 3.06 | サンクスシティーFUKUI | 3LDK | 65.26 | 84,000 | 9000 | 0円(-)/0円 | 3/5 | Y | 1995/12 | RC | 敷地内13200円 | B | https://sumaity.com/chintai/kyoto_prop/prop_411661902/ |
| 3.06 | サンクスシティーFUKUI | 3LDK | 60.42 | 84,000 | 9000 | 0円(-)/1ヶ月 | 3/5 | Y | 1995/12 | RC | - | B | https://sumaity.com/chintai/kyoto_prop/prop_406061112/ |
| 3.08 | クレードル桂川 | 3LDK | 65.78 | 78,000 | 10000 | 7.8万円(-)/0円 | 3/6 | Y | 1994/12 | RC | 敷地内14300円 | B | https://sumaity.com/chintai/kyoto_prop/prop_413877810/ |
| 3.08 | ラ・ヴィータローザ | 2LDK | 60.77 | 88,000 | 4100 | 0円(-)/8.8万円 | 2/2 | n | 2017/6 | 木造 | 敷地内11000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_411897706/ |
| 3.08 | 阪急京都線西京極駅までバス約4分 | 2LDK | 60.77 | 88,000 | 4100 | 0円(-)/8.8万円 | 2/2 | n | 2017/6 | 木造 | 敷地内11000円 | A | https://sumaity.com/chintai/kyoto_prop/prop_327228118/ |
| 3.18 | サンハイム井上 | 2LDK | 66.63 | 90,000 | 11500 | 9万円(-)/9万円 | 5/5 | Y | 1996/9 | RC | 敷地内11000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_412893592/ |
| 3.18 | サンハイム井上 | 2LDK | 66.63 | 86,000 | 11500 | 8.6万円(-)/8.6万円 | 3/5 | Y | 1996/9 | RC | 敷地内11000円 | B | https://sumaity.com/chintai/kyoto_prop/prop_412893736/ |

(Full list of 135 units in out/sumaity.json.)