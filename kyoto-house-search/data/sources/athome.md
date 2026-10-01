# at home (athome.co.jp) — summary

Run: 2026-10-01T23:33:35+09:00 (JST). Result: **blocked by Imperva bot protection (puzzle CAPTCHA) after 4 filtered list pages — 0 verified listings.** `out/athome.json` is therefore an empty array; 6 unverified leads are listed below and in `out/athome_leads_unverified.json`.

## What happened
- Reconnaissance with headless Chromium (Playwright) and a few plain `requests` fetches worked normally: the Angular pages are server-side rendered and embed the BFF JSON in `<script id="serverApp-state">`, so the list/detail data can be read without any private API call.
- The filtered crawl (plain requests, Chrome UA, ~1 request/s, 4–5 MB SSR pages) got 4 list pages (下京区 A/B, 中京区 A/B), then from the 5th request on every response was a 9 KB interstitial: title 「【アットホーム】認証中」→「認証にご協力ください」, text 「通常のサイト閲覧を超える速度でリクエストを繰り返している…『Click to verify』からパズル認証を行ってください」, script `/eadjaxlayqcmrfpo`, cookie `reese84` (Imperva Advanced Bot Protection). Raw copies: `out/raw/athome/list_kyoto_*_p1.html` (the 9 KB ones).
- One polite retry after a 9-minute cool-down (single detail page `/chintai/1053646558/` in headless Chromium, `athome_retry.js`, `out/raw/athome/retry_detail_1053646558.html`) still returned the puzzle CAPTCHA → block confirmed as persistent for this egress IP; no further attempts.
- A single control render in real headless Chromium 45 s later (`athome_blocktest.js`, `out/raw/athome/blocktest_rendered.html`) still showed the puzzle CAPTCHA, i.e. it is not a self-resolving JS check. As instructed, no attempt was made to evade it (no CAPTCHA solving, no IP rotation). The 6 candidate detail pages could not be fetched/verified, so nothing is kept.

## What was learned (reusable)
- `/chintai/kyoto/kyoto-city/list/` (URL from the brief) always returns 0件. Real pages: `/chintai/kyoto/kyoto-locate/list/` (whole 京都市, 228,759 rooms) and per ward `/chintai/kyoto/kyoto_<ward>-city/list/` (kyoto_shimogyo, kyoto_nakagyo, kyoto_minami, kyoto_ukyo, kyoto_kamigyo, kyoto_nishikyo, kyoto_higashiyama, kyoto_kita, kyoto_fushimi, kyoto_sakyo).
- Filters go in the query string and are honoured only with `q=1`: `?basic=kc001,kc115,ke001,kt007,ki002,kj001,km010,km014,km015,km018,km019,km021,kn021&q=1&sort=33&limit=30`
  (kc115 賃料上限10万円, kt007 専有面積45㎡以上, km010/014/015/018/019/021 = 2LDK/3DK/3LDK/4K/4DK/4LDK以上, kn021 築25年以内, kn023 築35年以内, kh001 鉄筋系, ki002 定期借家含む; insistence codes via `kod=` e.g. P02 2階以上, O08 エレベーター). Pagination `/list/pageN/` with the same query. Full code dictionary: `out/raw/athome/athome_test_state.json` → first-view → conditions.
- Detail page `/chintai/<bukkenNo>/` SSR state (`property-detail/first-view`) carries everything the spec asks for: rentInfo (price, deposit, keyMoney, hoshokin, managementFee, madori, area, chikunengetsu, kaidateKai, lightSurface, address, hikiwatashi, buildingInfo.tatemonoKozo, biko), facilityFeatureList (駐車・駐輪, 条件, 設備…), costInfo, surroundingInfo.mapData.ido/keido (lat/lon), kaiinInfo.syogo (不動産会社), dimension.setsubi (設備 CSV incl. エレベーター). Parser: `athome_scrape.py` (`parse_list`, `parse_detail`).
- List rows carry `heyaNayoseBukkenNoList` (the same room offered by several agents) — `totalBukkenCount` counts those duplicates.

## Pages scanned before the block
| ward | query | site total listings | rooms seen | pages |
|---|---|---|---|---|
| 下京区 | A (≤25y) | 9 | 3 | 1 |
| 下京区 | B (≤35y, 鉄筋系) | 17 | 9 | 1 |
| 中京区 | A | 1 | 1 | 1 |
| 中京区 | B | 33 | 6 | 1 |
| 南区 … 左京区 | A/B | — | blocked | — |

16 unique rooms (after folding 2 名寄せ duplicates) → list-level filter rejected 10 (1F: 4, 礼金>1ヶ月: 6) → 6 candidates, none verifiable.

## Unverified leads (list-page data only; detail/verification blocked)
| ward | building / room | address | floor | rent | 管理費 | layout | ㎡ | built | 敷/礼 | agent | url |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 下京区 | 下京区七条御所ノ内西町（一戸建） ３DK | 京都市下京区七条御所ノ内西町 | － | 89,000 | 0 | 3DK | 62.66 | 2007.9 | なし/8.9万円 | ピタットハウス長岡京店　(有)ハローホーム長岡 | https://www.athome.co.jp/chintai/1037909086/ |
| 下京区 | ブランシェ八甲 ５０２ ２LDK | 京都市下京区西七条北衣田町 | 5階 | 75,000 | 9000 | 2LDK | 47.0 | 1992.10 | 7.5万円/7.5万円 | アパマンショップ京都駅前店（ウインズリンク(株)） | https://www.athome.co.jp/chintai/1011801201/ |
| 下京区 | グランベール西七条 ７０３ ２LDK | 京都市下京区西七条南東野町 | 7階 | 98,000 | 8000 | 2LDK | 52.16 | 1996.3 | なし/なし | (株)ハウスメイトショップ　京都西院店 | https://www.athome.co.jp/chintai/1053646558/ |
| 中京区 | アリコス壬生 7階 ２LDK | 京都市中京区壬生森前町 | 7階 | 98,000 | 8000 | 2LDK | 54.0 | 2002.3 | 10万円/なし | (株)京都賃貸スタイル | https://www.athome.co.jp/chintai/6982872244/ |
| 中京区 | 京都市中京区 西ノ京馬代町（円町駅） 2階 ２LDK | 京都市中京区西ノ京馬代町 | 2階 | 100,000 | 10000 | 2LDK | 56.4 | 1996.11 | なし/なし | 京都ライフ西院店（(株)京都ライフ　西院店） | https://www.athome.co.jp/chintai/1155549326/ |
| 中京区 | フェアリージャム ２０２ ２LDK | 京都市中京区西ノ京馬代町 | 2階 | 100,000 | 10000 | 2LDK | 56.4 | 1996.11 | なし/なし | (株)京都ライフ　三条烏丸店 | https://www.athome.co.jp/chintai/1155549726/ |

Notes on the leads: 「京都市中京区 西ノ京馬代町（円町駅） 2階」 and 「フェアリージャム 202」 are the same unit (same address/floor/area/rent, two agents). 「下京区七条御所ノ内西町（一戸建）」 is a house (tier "house"). 7F units (グランベール西七条 703, アリコス壬生 7階) need the elevator check; 1992/1996 buildings need the RC/SRC check — both only possible from the detail page.

## Yahoo!不動産
See `out/yahoo.md` (quick probe only).
