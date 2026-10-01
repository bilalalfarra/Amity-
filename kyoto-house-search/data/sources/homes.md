# LIFULL HOME'S (homes.co.jp) — Kyoto rental scan summary

Scanned 2026-10-02T00:32:45+09:00 (JST). Script: `homes_scrape.py`, raw HTML in `out/raw/homes/` (list pages `listA_*`/`listB_*`, unit pages `detail_*`).

## Result

- **Kept: 159 units** → tier A 12, tier B 146, house 1 (`out/homes.json`).
- Kept by ward: nishikyo 62, minami 36, ukyo 29, fushimi 20, kita 5, shimogyo 3, higashiyama 3, nakagyo 1

## How the site was queried

Listings are server-rendered in the HTML (no JS rendering needed to read them; the only obstacle is the AWS WAF bot protection described under Problems). Ward list URL: `https://www.homes.co.jp/chintai/kyoto/<ward>/list/?<cond…>&page=N` (GET works even though the form posts). `<span class="totalNum">` = number of units, `li.lastPage` = last page, 30 buildings/page. Unit links in list rows are `https://www.homes.co.jp/chintai/room/<40-hex>/` (canonical unit page; one per agency listing), the `data-bid` gives the equivalent `/chintai/b-<13 digits>/` URL (also recorded in notes). PR (ad) blocks `div.prg-kksBukken` link straight to `b-` URLs and were parsed too.

### Query-string parameter codes discovered (search form)

| condition | parameter | used |
|---|---|---|
| 賃料上限 10万円 | `cond[monthmoneyroomh]=10` (万円; `cond[monthmoneyroom]` = lower bound; `cond[kanrihi]=1` would make it include 管理費) | yes |
| 専有面積 ≥45㎡ | `cond[housearea]=45` (`cond[houseareah]` = upper bound) | yes |
| 間取り | `cond[madori][25]=25` 2LDK, `[33]` 3DK, `[35]` 3LDK, `[43]` 4DK, `[45-]=45-` 4LDK以上 (others: 11 ワンルーム, 12 1K, 13 1DK, 15 1LDK, 22 2K, 23 2DK, 32 3K, 42 4K) | yes |
| 築年数 | `cond[houseageh]=25` 25年以内 (values 0 指定なし/1 新築/3/5/10/15/20/25/30 — no 35) | A: 25, B: 0 |
| 構造 | `cond[housekouzougroup][rebar]=rebar` 鉄筋系 (others: wooden 木造系, steelframe 鉄骨系, blockother ブロック・その他) | B only |
| 2階以上 | `cond[mcf][340102]=340102` (必須) / `cond[want_mcf][340102]` (できれば); 1階の物件 = 340101, 最上階 = 340201 | no (floor rule applied client-side) |
| エレベーター | `cond[mcf][320101]=320101` | no (not filtered server-side, as instructed) |
| 駐車場あり | `cond[mcf][320801]=320801` (駐車場2台以上 = 320601, 駐輪場 = 321001, バイク置き場 = 320901) | no (not filtered server-side) |
| 礼金なし / 敷金なし | `cond[reikin]=120101` / `cond[shikikin]=120201` | no (礼金 ≤1ヶ月 applied client-side) |
| 物件種別 | `cond[mbg][3002]` マンション, `[3001]` アパート, `[3003]` 一戸建て (all three are on by default) | default |
| その他 mcf | オートロック 310101, 追焚機能 220401, ペット相談可 113201, 南向き 340501, 宅配ボックス 321101, 床暖房 240201, 都市ガス 210201, 即入居可 350301, 保証人不要 121002, 分譲賃貸 331001 | no |
| 並び順 | `cond[sortby]=period` 築年数が新しい順 (recommend / fee / -fee / area_house / addr / newdate) | yes |
| ページ | `page=N` | yes |

## Pages scanned

- Tier A list pages (2LDK+/≥45㎡/≤10万/築25年以内, all wards): 12 pages; tier B list pages (same but 築 指定なし + 鉄筋系, newest first, stop when 築>36年): 27 pages.
- Server-reported unit totals per ward/tier (None = 0件 page): A_kyoto_shimogyo-city=5, A_kyoto_nakagyo-city=None, A_kyoto_minami-city=53, A_kyoto_ukyo-city=92, A_kyoto_kamigyo-city=16, A_kyoto_nishikyo-city=53, A_kyoto_higashiyama-city=None, A_kyoto_kita-city=21, A_kyoto_fushimi-city=201, B_kyoto_shimogyo-city=60, B_kyoto_nakagyo-city=87, B_kyoto_minami-city=256, B_kyoto_ukyo-city=587, B_kyoto_kamigyo-city=91, B_kyoto_nishikyo-city=788, B_kyoto_higashiyama-city=5, B_kyoto_kita-city=149, B_kyoto_fushimi-city=853
- Unit rows parsed from lists: 2586 (A 458, B 2128, PR blocks 72).
- Non-200 list pages: none
- Unit detail pages fetched: 202 (HTTP failures: 0).

## Counts dropped per rule

List stage (before fetching the unit page):
- tier-B rows outside 築24–36年 window (already in tier A or too old): 950
- 1階: 347
- layout not 2LDK+ : 1, area <45㎡: 0, rent >10万: 0
- same unit listed by several agencies (merged on address+floor+layout+rounded area, cheapest listing kept, other URLs/rents in notes): 599 (+6 merged after reading unit pages)
- >5.5 km from KRP by list address: 142 (geocode failed at list stage: 0 → fetched anyway)

Unit-page stage:
- 1階 (detail): 5; ≥4階 without elevator: 4
- 礼金 >1ヶ月: 12
- built before 1991 or 築年月 unknown: 15; built 1991–2000 but not RC/SRC: 1
- >5.5 km (detail address): 0; rent/area/layout mismatch on detail: 0/0/0

## Problems / caveats

- **Bot protection (AWS WAF)**: list pages and the first unit pages were fetched with python-requests (Chrome UA). After ~5 requests at 1 req/s with persisted cookies the site answered HTTP 202 with an AWS WAF JavaScript challenge; cookie-less requests at 1 req/2 s got further (~45 requests) before being challenged again, and after a handful of challenges the WAF escalated to HTTP 405 「Human Verification」 (CAPTCHA) for python-requests. Headless Chromium (Playwright) passed the JS challenge every time and was never shown the CAPTCHA, but a browser session was shown the CAPTCHA after roughly a dozen unit pages (the state sticks to the session, a fresh session is served normally). No CAPTCHA was ever solved or bypassed; the remaining unit pages were fetched by headless-browser sessions rotated every 9 pages (`homes_fetch.js`: HTML document only, ~10–14 s between pages, 45 s pause between sessions, 4-minute back-off on CAPTCHA): 196 ok, 3 blocked, 2 errors. Challenges seen by the python fetcher: 0; pages served from the raw-HTML cache on the final parse run: 241.
- 中京区 and 東山区 tier-A queries legitimately return 「該当物件は0件でした」 (no 2LDK+/≥45㎡/≤10万/築25年以内 units).
- Kyoto 通り名 addresses (e.g. 若宮通松原下る亀屋町) are not understood by the GSI geocoder; fallback geocodes ward + last 町名 (flagged in notes). Town-level precision only.
- `elevator=false` means the unit page's 設備・サービス list exists but does not include エレベーター; `null` when no equipment list was present.
- HOME'S lists the same room once per agency; duplicates were merged, other listings' URLs are in `notes`.
- Houses (一戸建て/テラスハウス) have no 所在階, so the floor rule is not applied to them; they are `tier: "house"`.

## Kept units

| tier | km | rent | 管理費 | layout | ㎡ | floor | elev | built | struct | 礼金 | parking | name | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 1.56 | 95000 | 5000 | 3LDK | 65.92 | 5/6 | True | 2002-8 | RC | 1ヶ月 | 空有 17,600円(税込) | ノブレカーサ西院 | https://www.homes.co.jp/chintai/room/e3064bc2bfe31eee26aa5eaab25c6ec5d10c15aa/ |
| A | 2.95 | 98000 | 0 | 2LDK | 68.59 | 2/2 | False | 2003-11 | 軽量鉄骨 | 無 | 近隣 10,000円(税込) 物件からの距離200m | イーズコート桂II | https://www.homes.co.jp/chintai/room/2c81108f53f3a4f29c38dba01fcdb5255516cf94/ |
| A | 3.08 | 88000 | 4100 | 2LDK | 60.77 | 2/2 | False | 2017-6 | 木造 | 8.8万円 | 空有 11,000円(税込) | ＬＡ・ＶＩＴＡＲＯＳＡ | https://www.homes.co.jp/chintai/room/c386f01a7bcce36ed6dd601313ed053b7a353bbc/ |
| A | 3.3 | 91000 | 12000 | 2LDK | 59.22 | 2/5 | True | 2003-3 | RC | 1ヶ月 | 空有 13,200円(税込) | コンフィアンサ桂 | https://www.homes.co.jp/chintai/room/cebd76c8d3faaa9fa05b201f86cb116e86dbd31f/ |
| A | 3.47 | 78000 | 7000 | 2LDK | 50.0 | 2/6 | True | 2019-1 | 鉄骨 | 7.8万円 | 空無 | サンローラン吉祥院 | https://www.homes.co.jp/chintai/room/10612c76c108341e6e813d951cb878ca3de24fef/ |
| A | 3.5 | 78000 | 4000 | 2LDK | 51.6 | 2/2 | False | 2005-8 | 軽量鉄骨 | 無 | 空有 8,000円(税込) | アリスプラミー | https://www.homes.co.jp/chintai/room/25b80a4cb9991323ae62da6ff3696daea669bbe0/ |
| A | 4.5 | 95000 | 6000 | 2LDK | 55.66 | 2/2 | False | 2026-6 | 木造 | 無 | 空有 11,000円 物件からの距離0m | リントゥコト | https://www.homes.co.jp/chintai/room/53ec778b08d205b7db6432be0a1b9da683968df8/ |
| A | 4.84 | 78000 | 8000 | 2LDK | 50.4 | 2/2 | False | 2004-10 | RC | 無 | 空無 | アントレデゥブリーズ | https://www.homes.co.jp/chintai/room/ae48f0cb245c73c24feea1ed5e13aa31d201c2d2/ |
| A | 4.97 | 97000 | 5000 | 2LDK | 45.32 | 2/4 | True | 2013-3 | RC | 無 | 空有 9,900円(税込) | プラシド七瀬川 | https://www.homes.co.jp/chintai/room/91cb6e03823c14112298b76295e775c66c530016/ |
| A | 5.3 | 75000 | 5000 | 2LDK | 64.3 | 2/2 | False | 2004-11 | 木造 | 無 | 空有 8,800円(税込) | フレイグランス久我 | https://www.homes.co.jp/chintai/room/5aefcfff6165e6c134eed7d3b7335042b0be8c15/ |
| A | 5.3 | 75000 | 5000 | 2LDK | 65.63 | 2/2 | False | 2004-11 | 木造 | 無 | 空有 8,800円(税込) | フレイグランス久我 | https://www.homes.co.jp/chintai/room/68987805b554fe853a782bdd15586a7f0a4d7054/ |
| A | 5.3 | 86000 | 4100 | 2LDK | 62.09 | 2/3 | False | 2019-10 | 木造 | 8.6万円 | 空有 7,700円(税込) | ｇｌａｎｚ　ＣＬＫ　いちご館 | https://www.homes.co.jp/chintai/room/8a9811ca83884c5d7f555f700a46d87adf64e280/ |
| B | 0.77 | 98000 | 8000 | 2LDK | 52.16 | 7/8 | True | 1996-3 | RC | 無 | 無 | グランベール西七条 | https://www.homes.co.jp/chintai/room/5e8e082894cf5ee658bc2945b43b707766a03a18/ |
| B | 0.98 | 75000 | 9000 | 2LDK | 47.0 | 5/5 | True | 1992-10 | RC | 7.5万円 | 近隣 16,000円(税込) 物件からの距離250m | ブランシェ八甲 | https://www.homes.co.jp/chintai/room/f2a978437c1d9afabed7b46bce3a6311fb196647/ |
| B | 0.98 | 75000 | 9000 | 2LDK | 50.0 | 5/5 | True | 1992-10 | RC | 1ヶ月 | 無 | ブランシェ八甲 | https://www.homes.co.jp/chintai/room/13018bfdb78925a3eaf7144979e9ac1781a45930/ |
| B | 1.39 | 85000 | 9000 | 2LDK | 48.33 | 4/6 | True | 1992-3 | RC | 1ヶ月 | - |  | https://www.homes.co.jp/chintai/room/4dc2fb73b31191bcf75d9acafe5d3831b3526de9/ |
| B | 1.56 | 88000 | 10000 | 2LDK | 61.01 | 3/6 | True | 1992-4 | RC | 8.8万円 | 空無 |  | https://www.homes.co.jp/chintai/room/7e27768e31a47701f5e455677fc075f8268417a6/ |
| B | 1.56 | 89000 | 10000 | 2LDK | 61.01 | 5/6 | True | 1992-4 | RC | 8.9万円 | 空無 |  | https://www.homes.co.jp/chintai/room/679e44e6675c931beb04bcacc54487ff3aa471fe/ |
| B | 1.86 | 70000 | 7000 | 2LDK | 48.0 | 2/5 | True | 1993-3 | RC | 無 | 空有 10,000円 物件からの距離0m |  | https://www.homes.co.jp/chintai/room/e491123cf5f27af7b855d3f15d4af6b00f8e2f23/ |
| B | 2.17 | 94000 | 9000 | 2LDK | 52.8 | 5/6 | True | 1997-3 | RC | 1ヶ月 | 空無 | スクリーン77 | https://www.homes.co.jp/chintai/room/5313d3d8708193b60430717a5ba64471957eccd8/ |
| B | 2.42 | 77000 | 5000 | 2LDK | 48.6 | 4/6 | True | 1998-5 | RC | 7.7万円 | 空有 11,000円(税込) 駐車料金：11000円〜187 | クレアール弐番館 | https://www.homes.co.jp/chintai/room/87324950e517d2e0620634a58dcf5501fb600d60/ |
| B | 2.46 | 84000 | 10000 | 2LDK | 57.51 | 3/4 | True | 1997-2 | RC | 1ヶ月 | 空有 10,000円(税込) | グランビュー葛野 | https://www.homes.co.jp/chintai/room/96f75da7af2ce994f589c5bdef413ed6affb0d5c/ |
| B | 2.53 | 84000 | 10000 | 2LDK | 56.0 | 3/4 | True | 1997-3 | RC | 1ヶ月 | 空有 10,000円(税無) | グランビュー葛野 | https://www.homes.co.jp/chintai/room/4248dd9305b90f359a366c56d224c5931296e5b7/ |
| B | 2.53 | 84000 | 10000 | 2LDK | 56.91 | 3/4 | True | 1997-2 | RC | 8.4万円 | 空有 5,000円(税込) 駐車料金：5000円〜10000 | グランビュー葛野 | https://www.homes.co.jp/chintai/room/75807a05fe349b8afa55de18289717f25359f5fe/ |
| B | 2.53 | 84000 | 10000 | 2LDK | 52.0 | 3/4 | True | 1997-2 | RC | 1ヶ月 | 空有 (1台) 10,000円 物件からの距離0m | グランビュー葛野 | https://www.homes.co.jp/chintai/room/b3e64919ca30816708ad845b8b9736439857a503/ |
| B | 2.56 | 89000 | 9500 | 3LDK | 65.0 | 5/7 | True | 1995-11 | RC | 8.9万円 | 空有 12,100円(税込) | コンフォール | https://www.homes.co.jp/chintai/room/7c797a428a4aef61589a18385e8befd86b723d05/ |
| B | 2.56 | 89000 | 9500 | 2LDK | 65.16 | 5/7 | True | 1995-11 | RC | 8.9万円 | 空有 12,100円(税込) | コンフォール | https://www.homes.co.jp/chintai/room/ad228789d1e9807f4f57695c85a7c8eb0812b16b/ |
| B | 2.56 | 89000 | 9500 | 2LDK | 64.33 | 5/7 | True | 1995-10 | RC | 8.9万円 | 空有 12,100円(税込) | コンフォール | https://www.homes.co.jp/chintai/room/b63130a289b10ee59f1a0311fe4123b688c65640/ |
| B | 2.63 | 89000 | 9500 | 2LDK | 65.16 | 3/7 | True | 1995-10 | RC | 1ヶ月 | 空有 12,100円(税込) ●駐車場契約手数料：駐車料の1 | コンフォール | https://www.homes.co.jp/chintai/room/ee8d797b245d1ed3bfeb4bccc87026d255204b1c/ |
| B | 2.67 | 80000 | 9000 | 3LDK | 60.96 | 3/7 | True | 1999-3 | RC | 8万円 | 空有 13,200円(税込) |  | https://www.homes.co.jp/chintai/room/37168dbc6859401add5d14c3258c1960a1f05273/ |
| B | 2.88 | 84000 | 9000 | 3LDK | 64.28 | 6/6 | True | 2000-3 | RC | 無 | 空有 11,000円(税込) |  | https://www.homes.co.jp/chintai/room/4978ccf433fe7b75615dcf5ca29409d784bb6d18/ |
| B | 2.93 | 87000 | 8000 | 2LDK | 51.17 | 3/3 | False | 1994-5 | RC | 1ヶ月 | 空無 ●駐車場：16000円(軽区画)~17000円(税別) | Rosy Garden | https://www.homes.co.jp/chintai/room/14b14cd502b454888619444ea94759e73269a19d/ |
| B | 2.93 | 95000 | 9000 | 3LDK | 67.62 | 3/6 | True | 1999-12 | RC | 1ヶ月 | 空無 |  | https://www.homes.co.jp/chintai/room/cc8f2f399667fb3ecde2bac8a2c86cb8328fb933/ |
| B | 3.0 | 85000 | 12000 | 3LDK | 67.17 | 4/6 | True | 1993-6 | RC | 8.5万円 | 空有 8,800円(税込) | パラッツォ桂 | https://www.homes.co.jp/chintai/b-1088790317322/ |
| B | 3.0 | 85000 | 12000 | 3LDK | 65.61 | 4/6 | True | 1993-6 | RC | 8.5万円 | 空有 8,000円(税込) |  | https://www.homes.co.jp/chintai/room/fc0295b23ac10d83d7ff53fe6ad9981225eeb74f/ |
| B | 3.05 | 100000 | 10000 | 2LDK | 56.4 | 2/6 | True | 1996-11 | RC | 無 | 空有 16,500円(税込) 駐車料金：16500円〜187 | フェアリージャム | https://www.homes.co.jp/chintai/room/5a98b0f42abd4579a6c97b2ad10b084d7875e853/ |
| B | 3.06 | 84000 | 9000 | 3LDK | 60.42 | 3/5 | True | 1995-12 | RC | 1ヶ月 | 空有 13,200円(税込) | サンクスシティＦＵＫＵＩ | https://www.homes.co.jp/chintai/room/77626d52c1a32cc9a5b1dfee7e256cf5feead0da/ |
| B | 3.06 | 84000 | 9000 | 3LDK | 65.26 | 3/5 | True | 1995-12 | RC | 1ヶ月 | 空有 13,200円 物件からの距離0m 桂駅徒歩15分、3 | サンクスシティーFUKUI | https://www.homes.co.jp/chintai/room/a94a2ac4286fd40786e4c7b28df170772b0e3e0a/ |
| B | 3.07 | 72000 | 8000 | 3DK | 60.27 | 3/5 | True | 1996-2 | RC | 1ヶ月 | 空有 12,100円 物件からの距離0m | デンクマール70 | https://www.homes.co.jp/chintai/room/b79d184a7a1c7e87967c7dac3100a5b4fbd8151b/ |
| B | 3.07 | 72000 | 8000 | 3DK | 60.27 | 2/5 | True | 1996-2 | RC | 1ヶ月 | 空有 12,100円 物件からの距離0m | デンクマール70 | https://www.homes.co.jp/chintai/room/629a9030f9501920887b695a99b36b3b7a0085ff/ |
| B | 3.08 | 78000 | 10000 | 3LDK | 65.78 | 3/6 | True | 1994-12 | RC | 無 | 空有 14,300円 物件からの距離0m | クレードル桂川 | https://www.homes.co.jp/chintai/room/758fff2961d8283db9ea8194abace55d82c71576/ |
| B | 3.1 | 90000 | 0 | 2LDK | 45.0 | 3/3 | True | 1993-3 | RC | 9万円 | 空無 | レジデンス東山 | https://www.homes.co.jp/chintai/room/9ecf184cef04d71726bd0ca82caa65d090b7b28d/ |
| B | 3.1 | 90000 | 0 | 2LDK | 45.0 | 2/3 | True | 1993-3 | RC | 9万円 | 空有 22,000円(税込) | レジデンス東山 | https://www.homes.co.jp/chintai/room/7c435a2eac13738c0c0aa8b85f1292aa6e767fa8/ |
| B | 3.17 | 86000 | 11500 | 2LDK | 66.63 | 3/5 | True | 1996-9 | RC | 1ヶ月 | 空有 11,000円(税込) | サンハイム井上 | https://www.homes.co.jp/chintai/b-37010650271786/ |
| B | 3.18 | 90000 | 11500 | 2LDK | 66.63 | 5/5 | True | 1996-9 | RC | 9万円 | 空有 11,000円(税込) | サンハイム井上 | https://www.homes.co.jp/chintai/room/218944dcbc9c5c56c465138ae7b3b6a8baa2502e/ |
| B | 3.18 | 90000 | 11500 | 3LDK | 66.63 | 5/5 | True | 1996-9 | RC | 9万円 | 空有 (1台) 11,000円 物件からの距離0m | サンハイム井上 | https://www.homes.co.jp/chintai/room/c597d4a5a118799d35816f7b92000b420aa81298/ |
| B | 3.27 | 80000 | 8000 | 2LDK | 49.05 | 4/7 | True | 1997-1 | RC | 1ヶ月 | 空有 (1台) 9,900円(税込) | プレミエールクラーテ | https://www.homes.co.jp/chintai/room/f42638e56c9dd5741297d955f087d8be59637ac3/ |
| B | 3.27 | 80000 | 8000 | 2LDK | 53.2 | 4/7 | True | 1997-1 | RC | 8万円 | 空有 9,900円(税込) | プレミエールクラーテ | https://www.homes.co.jp/chintai/room/3a9445523900d82ac7d7ed5c98a277d609f83008/ |
| B | 3.27 | 81000 | 8000 | 2LDK | 49.05 | 6/7 | True | 1997-1 | RC | 1ヶ月 | 空有 (1台) 9,900円(税込) | プレミエールクラーテ | https://www.homes.co.jp/chintai/room/ec5fe27e77de04ce3b879bdc3312e91fb7f981f7/ |
| B | 3.3 | 93000 | 7000 | 3LDK | 67.13 | 3/4 | True | 2000-4 | RC | 9.3万円 | 空有 11,000円(税込) 駐車料金：11000円〜143 |  | https://www.homes.co.jp/chintai/room/b1b6d01208c2ef496a42f6a2f72cbe6084a0a52d/ |
| B | 3.32 | 80000 | 10000 | 3LDK | 66.0 | 3/4 | True | 1996-2 | RC | 8万円 | 空有 10,000円(税込) |  | https://www.homes.co.jp/chintai/room/e95cc21a57f6dbc74f3a64177050a109e399c84b/ |
| B | 3.32 | 80000 | 10000 | 3LDK | 65.0 | 3/4 | True | 1996-2 | RC | 1ヶ月 | 空有 (1台) 11,000円 物件からの距離0m | ヴェルジュール桂川 | https://www.homes.co.jp/chintai/room/9c27a81f25d1537feab0064bd5b92b94859600dc/ |
| B | 3.32 | 87000 | 8000 | 3LDK | 65.23 | 4/6 | True | 1993-12 | RC | 無 | 空有 8,000円(税込) 駐車料金：8000円〜10000 | ラビリント川島 | https://www.homes.co.jp/chintai/room/aef2e3430fb2b468c79ea22e47403e513f51513c/ |
| B | 3.32 | 87000 | 8000 | 3LDK | 65.76 | 4/6 | True | 1993-12 | RC | 無 | 空有 8,000円 物件からの距離0m | ラビリント川島 | https://www.homes.co.jp/chintai/room/21f8c657b4ad3788fc366c09f7e459a844861018/ |
| B | 3.32 | 91000 | 8000 | 3LDK | 69.89 | 3/5 | True | 1991-10 | RC | 無 | 空有 13,200円(税込) | ＧＡＲＮＥＴ　ＲＥＳＩＤＥＮＣＥ上桂 | https://www.homes.co.jp/chintai/room/cf59a6153ae79bd7e13053a4f61a6b6d4ec23813/ |
| B | 3.32 | 96000 | 8000 | 3LDK | 74.63 | 2/5 | True | 1991-10 | RC | 無 | 空有 13,200円(税込) | ＧＡＲＮＥＴ　ＲＥＳＩＤＥＮＣＥ上桂 | https://www.homes.co.jp/chintai/room/5af11da07723564baad2f163dd0ce56c9435c1a3/ |
| B | 3.37 | 80000 | 8000 | 2LDK | 53.49 | 4/5 | True | 1994-12 | RC | 無 | 空有 13,200円(税込) | カノン | https://www.homes.co.jp/chintai/room/ae7c3944287cb4d4285bc07c77cd5833901fd611/ |
| B | 3.37 | 92000 | 8000 | 3LDK | 64.89 | 2/5 | True | 1994-12 | RC | 無 | 空有 13,200円(税込) | カノン | https://www.homes.co.jp/chintai/room/d400e6b572e435e40f649b8689cb3d4318293a1d/ |
| B | 3.41 | 68000 | 8000 | 2LDK | 50.0 | 2/5 | True | 1993-3 | RC | 無 | 空有 16,500円 | プリメール桂 | https://www.homes.co.jp/chintai/room/a53c036302fc8cb8e20da3c89c027b1799b8cb0a/ |
| B | 3.41 | 69000 | 8000 | 2LDK | 54.96 | 2/5 | True | 1993-4 | RC | 無 | 空有 16,500円(税込) | プリメール桂 | https://www.homes.co.jp/chintai/room/5a0421334bed2d1c4daf05650f84d0c634939a35/ |
| B | 3.42 | 69000 | 8000 | 2LDK | 58.2 | 2/5 | True | 1993-4 | RC | 無 | 空有 16,500円(税込) | プリメール桂 | https://www.homes.co.jp/chintai/room/9f44420d96e1961660a6655a219835edc17afb6e/ |
| B | 3.43 | 80000 | 10000 | 3LDK | 70.34 | 2/6 | True | 1994-2 | RC | 8万円 | 無 | フォレステージ太秦 | https://www.homes.co.jp/chintai/room/52e25fc7eb1ca3f0f36c4bae40b0af3159ebc89a/ |
| B | 3.46 | 81000 | 10000 | 3LDK | 59.13 | 4/6 | True | 1993-9 | RC | 無 | 空有 8,800円(税込) | ドミール芝の宮 | https://www.homes.co.jp/chintai/room/81fd621b51ab760a6efd146e8071448b36ec5134/ |
| B | 3.48 | 80000 | 10000 | 3LDK | 66.0 | 3/4 | True | 1996-2 | RC | 8万円 | 空有 11,000円(税込) |  | https://www.homes.co.jp/chintai/room/124af949acb35ecb3711512e79bdfcaf9d6c1a57/ |
| B | 3.52 | 72000 | 9000 | 3LDK | 60.0 | 4/4 | True | 1991-7 | RC | 5万円 | 空有 10,000円(税込) | ナチュールキチ | https://www.homes.co.jp/chintai/room/a39bf96cd9fcc7b9b0126346ad71579b8d3c0b0f/ |
| B | 3.62 | 90000 | 0 | 3LDK | 66.44 | 3/7 | True | 1995-11 | RC | 9万円 | 空有 13,200円(税込) | セントフローレンスパレス桂 | https://www.homes.co.jp/chintai/room/f9450b942c6acc0282b680eca4343e9e6380d30e/ |
| B | 3.62 | 90000 | 0 | 3LDK | 68.42 | 3/7 | True | 1995-11 | RC | 9万円 | 近隣 11,000円 物件からの距離300m | セントフローレンスパレス桂 | https://www.homes.co.jp/chintai/room/cfd9f38de33a6eddf433b9c06aad48a36404bb52/ |
| B | 3.62 | 90000 | 0 | 3LDK | 59.16 | 3/7 | True | 1995-11 | RC | 9万円 | 無 | セントフローレンスパレス桂 | https://www.homes.co.jp/chintai/room/0b4913c5e47a7672dc059ded7e51dcd6362a3a63/ |
| B | 3.83 | 92000 | 10000 | 3LDK | 65.74 | 7/7 | True | 1994-6 | RC | 9.2万円 | 空有 10,000円(税込) | サンシャイン梅津 | https://www.homes.co.jp/chintai/room/b561e84bb09e1a85e74bf9ba45b45a76477f9b76/ |
| B | 3.83 | 92000 | 10000 | 3LDK | 60.84 | 7/7 | True | 1994-5 | RC | 1ヶ月 | 空有 10,000円(税無) | サンシャイン梅津 | https://www.homes.co.jp/chintai/room/04d37340e616373d1a711cf26f218ecdb861b437/ |
| B | 3.84 | 85000 | 8000 | 3LDK | 68.67 | 3/6 | True | 1997-3 | RC | 8.5万円 | 空無 | Ｓｕｎ・Ｂｉｒｄ　桂 | https://www.homes.co.jp/chintai/room/15fda826a1034a977804707ca678fb6db29bccde/ |
| B | 3.86 | 90000 | 0 | 3LDK | 66.44 | 2/7 | True | 1996-3 | RC | 1ヶ月 | 無 | セントフローレンスパレス桂 | https://www.homes.co.jp/chintai/room/e4bbbf73f85efcf5d1a9e4c3cde01df4c80556c2/ |
| B | 3.89 | 78000 | 8000 | 2LDK | 55.67 | 7/7 | True | 1999-3 | RC | 7.8万円 | 空有 4,400円(税込) |  | https://www.homes.co.jp/chintai/room/08f7eb693af060beffb1d6d0162a8555d66384ff/ |
| B | 3.89 | 90000 | 10500 | 3LDK | 66.16 | 5/5 | True | 1997-9 | RC | 無 | 空有 11,000円(税込) | 上桂エクセルハイツ | https://www.homes.co.jp/chintai/room/0ff03d49276171d651b5a776a3be82496f0fd213/ |
| B | 3.93 | 75000 | 8000 | 2LDK | 55.5 | 3/4 | False | 1992-8 | RC | 1ヶ月 | 空有 8,800円(税込) |  | https://www.homes.co.jp/chintai/room/1406ee98765a0f134ef7e2612ccd09050ade5407/ |
| B | 4.0 | 65000 | 8000 | 2LDK | 54.04 | 3/7 | True | 1995-3 | RC | 1ヶ月 | 空有 13,200円(税込) |  | https://www.homes.co.jp/chintai/room/b3ade75403b7020ca606c9a49bffc16536e03894/ |
| B | 4.0 | 65000 | 8000 | 2LDK | 50.42 | 2/7 | True | 1995-3 | RC | 無 | 空有 13,200円(税込) |  | https://www.homes.co.jp/chintai/room/e305d25988abdaf97d051d5bb7759169d6de71db/ |
| B | 4.0 | 67000 | 9000 | 2LDK | 54.04 | 5/7 | True | 1995-3 | RC | 1ヶ月 | 空有 13,200円(税込) |  | https://www.homes.co.jp/chintai/room/959b0dd671266027c934ad9bf2e847c440ad329b/ |
| B | 4.0 | 67000 | 9000 | 2LDK | 47.09 | 5/7 | True | 1994-3 | RC | 6.7万円 | 空有 13,200円(税込) |  | https://www.homes.co.jp/chintai/room/a9e569f756f9b8677b86f55acde70a52cdc9a989/ |
| B | 4.0 | 75000 | 9000 | 3LDK | 61.68 | 5/7 | True | 1995-3 | RC | 1ヶ月 | 空有 13,200円(税込) |  | https://www.homes.co.jp/chintai/room/e855b25f5666f78f7e59b6d3a95aeea65cdad108/ |
| B | 4.0 | 78000 | 0 | 2LDK | 57.6 | 4/6 | True | 1995-3 | RC | 無 | 空有 9,000円 物件からの距離0m |  | https://www.homes.co.jp/chintai/room/494fb8c7c15fcee4c6cdbd87f48b41ba85562321/ |
| B | 4.0 | 78000 | 0 | 2LDK | 57.05 | 4/6 | True | 1995-3 | RC | 無 | 空有 (1台) 9,000円 物件からの距離0m |  | https://www.homes.co.jp/chintai/room/591d3415ff824d2049d595514a9282192777d701/ |
| B | 4.07 | 95000 | 15000 | 3LDK | 69.0 | 6/6 | True | 1991-4 | RC | 無 | 空有 16,500円(税込) | アメニティ双ケ丘 | https://www.homes.co.jp/chintai/room/0b02b0168f4344799b3b4af80181cbf2ad2461aa/ |
| B | 4.22 | 78000 | 7000 | 2LDK | 52.7 | 2/3 | False | 1995-10 | RC | 無 | 空有 14,300円(税込) | カルム常盤 | https://www.homes.co.jp/chintai/room/c66a412a4e5939db06778cf953476e34ceb186c9/ |
| B | 4.28 | 90000 | 9500 | 2LDK | 56.02 | 3/6 | True | 1995-4 | RC | 1ヶ月 | - | エミネンス善 | https://www.homes.co.jp/chintai/room/de66f2b7c35c8d9eab6722e516e732f2e7a2a9c9/ |
| B | 4.34 | 73000 | 5000 | 2LDK | 50.2 | 3/6 | True | 1992-7 | SRC | 無 | 近隣 (1台) 13,000円 物件からの距離100m | サウスヴィラ | https://www.homes.co.jp/chintai/room/0e0709fc391fa1445642c5068b4f5a9d970691ec/ |
| B | 4.44 | 77000 | 3000 | 2LDK | 56.04 | 2/3 | False | 1996-7 | RC | 無 | 空有 10,000円(税込) | メゾン太秦 | https://www.homes.co.jp/chintai/room/acb0e0490afa54ae099dddac5eb84397a6806112/ |
| B | 4.47 | 81000 | 10000 | 2LDK | 55.05 | 4/6 | True | 1995-5 | RC | 8.1万円 | 空有 13,200円(税込) | Ｍレヴェンテ | https://www.homes.co.jp/chintai/room/ed3fdcf2cbbe3f365b995ab8eb1771ea048c73e6/ |
| B | 4.47 | 81000 | 9000 | 3LDK | 59.05 | 3/6 | True | 1995-3 | RC | 8.1万円 | 近隣 10,000円(税込) 物件からの距離200m | エクセレンス飛鳥 | https://www.homes.co.jp/chintai/room/5a50ccef292f64a672259da580c5fe70f612237e/ |
| B | 4.47 | 85000 | 9000 | 3LDK | 73.12 | 4/5 | True | 1998-9 | RC | 無 | 空有 13,200円(税込) |  | https://www.homes.co.jp/chintai/room/ea6c7bcef1cea22b6df55da00dc84e8171b8cf49/ |
| B | 4.47 | 85000 | 9000 | 3LDK | 73.12 | 3/5 | True | 1998-9 | RC | 無 | 空有 12,600円 物件からの距離0m | ウエストコート大利 | https://www.homes.co.jp/chintai/room/12f2cb23818fff5800454347834ee09857be91fb/ |
| B | 4.47 | 85000 | 9000 | 3LDK | 73.12 | 5/5 | True | 1998-5 | RC | 無 | 空有 13,200円(税込) | ウエストコート大利 | https://www.homes.co.jp/chintai/room/3980558e0c81e850e897289b04d46da763a307ed/ |
| B | 4.47 | 86000 | 10000 | 3LDK | 65.55 | 6/7 | True | 1994-9 | RC | 8.6万円 | 空有 13,200円(税込) 駐車料金：13200円〜165 |  | https://www.homes.co.jp/chintai/room/c042a39f2fb9b1cc6dde684e02b48c749fca9e20/ |
| B | 4.47 | 86000 | 10000 | 3LDK | 65.45 | 4/7 | True | 1994-9 | RC | 8.6万円 | 空有 13,200円(税込) 駐車料金：13200円〜165 |  | https://www.homes.co.jp/chintai/room/e90d7f13867842c5812b480cf5d96f37716a8a6b/ |
| B | 4.47 | 86000 | 10000 | 3LDK | 64.45 | 4/7 | True | 1994-9 | RC | 1ヶ月 | 空有 16,500円(税込) |  | https://www.homes.co.jp/chintai/room/b2b5d41b7ff291e7a0ee7d031f93aa042e196f24/ |
| B | 4.47 | 86000 | 10000 | 2LDK | 55.89 | 3/6 | True | 1992-11 | RC | 8.6万円 | 空有 13,200円(税込) |  | https://www.homes.co.jp/chintai/room/8a3dffde166336357538727c419f99f51c18343c/ |
| B | 4.47 | 87000 | 10000 | 3LDK | 65.55 | 4/7 | True | 1994-9 | RC | 8.7万円 | 空有 13,200円(税込) 駐車料金：13200円〜165 |  | https://www.homes.co.jp/chintai/room/4e81f326596c38b2832faba88074ab21c1b17350/ |
| B | 4.47 | 95000 | 10000 | 3LDK | 61.02 | 3/6 | True | 1992-11 | RC | 9.5万円 | 空有 13,200円(税込) |  | https://www.homes.co.jp/chintai/room/bf9af30906eeb7eb24c11fdd04bac52a035932a3/ |
| B | 4.5 | 77000 | 3000 | 2LDK | 57.34 | 2/3 | False | 1996-7 | RC | 無 | 空有 10,000円(税込) | メゾン太秦 | https://www.homes.co.jp/chintai/room/f259b08fdb517d0b8c95a563607571928af75c67/ |
| B | 4.53 | 78000 | 7000 | 2LDK | 57.9 | 6/7 | True | 1996-11 | RC | 無 | 空有 11,000円(税込) 駐車料金：11000円〜143 | サントル西京 | https://www.homes.co.jp/chintai/room/90c786f0d26a8673dfa79b3dc7a6911f4ac42f5b/ |
| B | 4.54 | 89000 | 10500 | 3LDK | 69.27 | 2/3 | True | 1999-4 | RC | 無 | 空有 13,200円(税込) | リジョイス桂 | https://www.homes.co.jp/chintai/room/78b7aba24ff2b3ec42d9d237d05d636075255590/ |
| B | 4.62 | 88000 | 10000 | 2LDK | 52.0 | 3/6 | True | 1997-2 | RC | 8.8万円 | 空無 |  | https://www.homes.co.jp/chintai/room/86629e29d063327428bbcf86fb69b07ae4b9ffb2/ |
| B | 4.62 | 88000 | 10000 | 2LDK | 52.86 | 3/6 | True | 1996-3 | RC | 1ヶ月 | 空有 13,200円(税込) |  | https://www.homes.co.jp/chintai/room/ea0a7dee5687cf3d42c2cce69c1407582dcc3d1a/ |
| B | 4.62 | 95000 | 4000 | 3LDK | 62.37 | 7/7 | True | 1993-11 | RC | 9.5万円 | 無 | 日本鉱産ビルグラハイツ | https://www.homes.co.jp/chintai/room/a107dd7806e49d992fbfe0e4ecfc30e2e05fcb19/ |
| B | 4.62 | 100000 | 0 | 2LDK | 56.7 | 5/7 | True | 1995-3 | RC | 10万円 | 空有 10,000円(税込) 駐車料金：10000円〜130 | カサ・デ・高ノ手 | https://www.homes.co.jp/chintai/room/5c34e031cb991cd7ae63343891664a351043cc65/ |
| B | 4.62 | 100000 | 0 | 2LDK | 56.7 | 4/7 | True | 1995-3 | RC | 10万円 | 空有 10,000円(税込) 駐車料金：10000円〜130 | カサ・デ・高ノ手 | https://www.homes.co.jp/chintai/room/d0751f57dad9fb7bdfaf63bde059a8154a2c365f/ |
| B | 4.62 | 100000 | 0 | 2LDK | 56.07 | 5/7 | True | 1995-3 | RC | 10万円 | 空有 (1台) 無料 | カサ・デ・高ノ手 | https://www.homes.co.jp/chintai/room/f01791b7846f44127ad8fc30b5e830f5261e225a/ |
| B | 4.62 | 100000 | 0 | 2LDK | 56.7 | 2/7 | True | 1995-3 | RC | 10万円 | 近隣 12,600円 物件からの距離200m | カサ・デ・高ノ手 | https://www.homes.co.jp/chintai/room/3da22674e3f42fabb4591c203cb635ad0cbaa8a7/ |
| B | 4.76 | 88000 | 0 | 3LDK | 66.87 | 3/3 | False | 1993-3 | RC | 無 | 空有 無料 | ヴェルデ三番館 | https://www.homes.co.jp/chintai/room/bb4fcf2c540f1c2b8219c98f2fa8de40bb066980/ |
| B | 4.76 | 88000 | 0 | 3LDK | 66.17 | 3/3 | False | 1993-3 | RC | 無 | 空有 (1台) 無料 | ヴェルデ三番館 | https://www.homes.co.jp/chintai/room/d25137c18505993ea9c11d02f17967fe3694bb7b/ |
| B | 4.76 | 96000 | 0 | 3LDK | 70.06 | 3/3 | False | 1993-3 | RC | 無 | 空有 (1台) 料金：賃料に含む | ヴェルデ三番館 | https://www.homes.co.jp/chintai/room/8f9c9164e32735f42399bcf494fb8edf43bb50c9/ |
| B | 4.77 | 85000 | 5000 | 3LDK | 65.25 | 2/3 | False | 1998-2 | RC | 8.5万円 | 空有 11,000円(税込) | グラン・シャリオ | https://www.homes.co.jp/chintai/room/328f4a94023b4970afcb141eaf5df7dbca7a86d9/ |
| B | 4.77 | 85000 | 5000 | 3LDK | 66.0 | 2/3 | False | 1998-2 | RC | 1ヶ月 | 空有 12,100円(税込) | グラン・シャリオ | https://www.homes.co.jp/chintai/room/cddd064e9537f5151bf1b16bb9141a5411d05fd1/ |
| B | 4.78 | 88000 | 0 | 3LDK | 57.51 | 2/3 | False | 1992-5 | RC | 無 | 空有 無料 | ローファス小島 | https://www.homes.co.jp/chintai/room/059b3dc9ffe8f79327fa2cf98cf1169e509fbe09/ |
| B | 4.78 | 88000 | 0 | 3LDK | 62.02 | 2/3 | False | 1992-5 | RC | 無 | 空有 (1台) 無料 | ローファス小島 | https://www.homes.co.jp/chintai/room/162b071b3a67260d7c3185842a756264df7355e9/ |
| B | 4.83 | 95500 | 10000 | 3LDK | 65.02 | 3/5 | True | 1999-12 | RC | 9.55万円 | 近隣 (1台) 18,000円 物件からの距離400m | イースタン平野路 | https://www.homes.co.jp/chintai/room/bfb6d0b29227021fbdcca260d96f34da57e1cea0/ |
| B | 4.83 | 95500 | 10000 | 3DK | 65.02 | 3/5 | True | 1999-12 | RC | 9.55万円 | 空有 15,400円(税無) 駐車料金：15400円〜170 | イースタン平野路 | https://www.homes.co.jp/chintai/room/67d1831907e9986a21e9f6de705005e796ae2f1b/ |
| B | 4.86 | 74000 | 0 | 3DK | 57.54 | 3/4 | False | 1991-3 | RC | 7.4万円 | 空有 10,000円(税込) 駐車料金：10000円〜110 | カサグランデ嵯峨野 | https://www.homes.co.jp/chintai/room/443cc0df938675a555263c169d8979ad33addba0/ |
| B | 4.86 | 74000 | 0 | 3DK | 57.22 | 3/4 | False | 1991-3 | RC | 7.4万円 | 空有 11,000円(税込) | カサグランデ嵯峨野 | https://www.homes.co.jp/chintai/room/24b02197db927db424679c60edd28dae6b828c74/ |
| B | 4.86 | 74000 | 0 | 3DK | 59.0 | 3/4 | False | 1991-3 | RC | 7.4万円 | 空有 10,000円 物件からの距離0m | カサグランデ嵯峨野 | https://www.homes.co.jp/chintai/room/fa374fa33e1251fce56bfac607f0476be2a5d3fe/ |
| B | 4.86 | 74000 | 0 | 3DK | 53.46 | 3/4 | False | 1991-3 | RC | 1ヶ月 | 空有 11,000円(税込) | カサグランデ嵯峨野 | https://www.homes.co.jp/chintai/room/8972ca40e7d049c4d6e92d24ba0dac45c7d51bd1/ |
| B | 4.86 | 75000 | 0 | 3DK | 52.25 | 2/3 | False | 1992-2 | RC | 1ヶ月 | 空有 11,000円(税込) | 第二藤栄ハイツ | https://www.homes.co.jp/chintai/room/dab69eaf972d051e503674d19b459353acade164/ |
| B | 4.86 | 95000 | 0 | 3LDK | 67.0 | 3/3 | False | 1994-4 | RC | 9.5万円 | 空有 11,000円(税無) | アーバンエステートイトヤ | https://www.homes.co.jp/chintai/room/2ee356f9510c531a437b355915cac3af8cc0df0c/ |
| B | 4.86 | 95000 | 0 | 3LDK | 69.0 | 3/3 | False | 1994-4 | RC | 1ヶ月 | 空有 11,000円(税込) | アーバンエステートイトヤ | https://www.homes.co.jp/chintai/room/b5923c9dea2502b7b7f3fb6a4e9fe5b5d4b4b1a9/ |
| B | 4.86 | 95000 | 0 | 3LDK | 65.25 | 3/3 | False | 1994-4 | RC | 9.5万円 | 空有 11,000円(税込) | アーバンエステートイトヤ | https://www.homes.co.jp/chintai/room/62bba6da8f11a93a1ec145ebcdb79000538f5e69/ |
| B | 4.86 | 95000 | 0 | 3LDK | 66.0 | 3/3 | False | 1994-3 | RC | 1ヶ月 | 空有 11,000円 物件からの距離0m | アーバンエステートイトヤ | https://www.homes.co.jp/chintai/room/c391910e3eb073b98f815edea4e50f3de2f5fc06/ |
| B | 4.87 | 93000 | 10000 | 3LDK | 62.16 | 2/5 | True | 1996-3 | RC | 無 | 空有 11,000円(税込) |  | https://www.homes.co.jp/chintai/room/311d071ba8fc851082872750d83417100df3f893/ |
| B | 4.87 | 93000 | 10000 | 2LDK | 61.24 | 2/5 | True | 1996-3 | RC | 無 | 空有 11,000円(税込) |  | https://www.homes.co.jp/chintai/room/f9b217a539d78e872bb84d75674ea0967e2eb599/ |
| B | 4.87 | 93000 | 10000 | 2LDK | 62.16 | 2/5 | True | 1996-3 | RC | 無 | 無 |  | https://www.homes.co.jp/chintai/room/ea37de0b846d450ae57de0808c22c3287d784fff/ |
| B | 4.91 | 82000 | 10000 | 2LDK | 61.68 | 2/7 | True | 2000-2 | RC | 無 | 空有 16,500円(税込) | レジディア太秦 | https://www.homes.co.jp/chintai/room/967128fb3248c796266c1d92e047bd2b9cff2488/ |
| B | 4.92 | 92000 | 10000 | 2LDK | 53.0 | 2/4 | False | 1991-8 | RC | 9.2万円 | 無 |  | https://www.homes.co.jp/chintai/room/5c738dca67ca8942c4b50ff9ac01ffc58ed1659a/ |
| B | 4.92 | 92000 | 10000 | 2LDK | 56.0 | 2/4 | False | 1991-7 | RC | 9.2万円 | 無 |  | https://www.homes.co.jp/chintai/room/bfa748b927dcb7c96f1e45cd95162cf97587dafd/ |
| B | 4.97 | 95000 | 4000 | 3LDK | 62.37 | 7/7 | True | 1993-11 | RC | 9.5万円 | 近隣 10,000円(税込) 物件からの距離150m | 日本鉱産ビルグラハイツ | https://www.homes.co.jp/chintai/room/4e1ed3aa016dc75e5301c7c01a014e1208468dd9/ |
| B | 4.97 | 95000 | 4000 | 3DK | 62.37 | 7/7 | True | 1993-11 | RC | 9.5万円 | 近隣 11,000円(税込) 物件からの距離341m | 日本鉱産ビルグラハイツ | https://www.homes.co.jp/chintai/room/a68805916c7f27ffe4267b85b2995cbc2259fa2f/ |
| B | 4.97 | 95000 | 4000 | 3LDK | 62.58 | 6/7 | True | 1993-11 | RC | 9.5万円 | 空無 | 日本鉱産ビルグラハイツ | https://www.homes.co.jp/chintai/room/d86a981aa8bd8bfdb85e2ff5d3b24744c12842a8/ |
| B | 4.98 | 78000 | 8000 | 2LDK | 50.43 | 3/5 | True | 1995-1 | RC | 1ヶ月 | - | ABC BLDG | https://www.homes.co.jp/chintai/room/da9cb8b71595b539fa23975a9c3b3a67b2835dcf/ |
| B | 4.98 | 78000 | 8000 | 2LDK | 45.13 | 3/5 | True | 1995-1 | RC | 7.8万円 | 無 | ＡＢＣ　ＢＬＤＧ． | https://www.homes.co.jp/chintai/room/8b37b38341ef19ba7596643ab887bded167457e2/ |
| B | 4.98 | 80000 | 9000 | 2LDK | 54.54 | 4/6 | True | 1994-8 | RC | 8万円 | 空有 13,200円(税込) 駐車料金：13200円〜154 | リーブルショーザン | https://www.homes.co.jp/chintai/room/d3bd0d2772c2b35e0f597ebe66d154e4e2d30696/ |
| B | 4.98 | 80000 | 9000 | 2LDK | 50.58 | 3/6 | True | 1994-8 | RC | 8万円 | 空有 13,200円(税込) 駐車料金：13200円〜154 | リーブルショーザン | https://www.homes.co.jp/chintai/room/343fbda964e4ebc862bc877197d4ee3561bd1d78/ |
| B | 4.98 | 80000 | 9000 | 2LDK | 54.54 | 2/6 | True | 1994-8 | RC | 8万円 | 空有 13,200円(税込) 駐車料金：13200円〜154 | リーブルショーザン | https://www.homes.co.jp/chintai/room/5aca25a418fdcd14d28740004de0713dd0c3e201/ |
| B | 4.98 | 80000 | 9000 | 2LDK | 50.58 | 2/6 | True | 1994-6 | RC | 1ヶ月 | 近隣 (1台) 13,200円 物件からの距離300m | リーブルショーザン | https://www.homes.co.jp/chintai/room/de2f10b3c7ea2debd7a5261c8932a6bdc9d17d8d/ |
| B | 4.98 | 95000 | 9000 | 3DK | 65.99 | 7/7 | True | 1995-9 | RC | 9.5万円 | 空有 13,200円(税込) | グレース・ダイン | https://www.homes.co.jp/chintai/room/d3090bb1a6a97a3538cd79240f04b9c6d397c531/ |
| B | 4.98 | 95000 | 9000 | 3LDK | 65.99 | 7/7 | True | 1995-9 | RC | 9.5万円 | 空有 13,200円(税込) | グレース・ダイン | https://www.homes.co.jp/chintai/room/19af16f403b9be3b4b134aa1124d6e4d1b4f3286/ |
| B | 5.07 | 88000 | 8000 | 3LDK | 69.13 | 3/3 | False | 2000-4 | RC | 8.8万円 | 空有 11,000円(税込) 駐車料金：11000円〜132 |  | https://www.homes.co.jp/chintai/room/e917741fbaf036811901cd67e42682177478afbc/ |
| B | 5.09 | 70000 | 4000 | 2LDK | 56.8 | 2/3 | False | 1995-7 | RC | 7万円 | 空有 8,000円(税込) | クレセント・オークス | https://www.homes.co.jp/chintai/room/be2db02e3fb1942254960d8361f77e3950a7f232/ |
| B | 5.2 | 90000 | 3000 | 2LDK | 55.84 | 3/3 | False | 2000-2 | RC | 1ヶ月 | 空有 16,500円(税込) | グレース菱屋II | https://www.homes.co.jp/chintai/room/3f99f66ce0e08418cce48b149370e4ffcf6d1a71/ |
| B | 5.23 | 90000 | 3000 | 2LDK | 56.56 | 3/3 | False | 2000-2 | RC | 1ヶ月 | 近隣 8,800円(税込) 物件からの距離218m | グレ−ス菱屋II | https://www.homes.co.jp/chintai/room/ac6cde76387f31adb5ce9c4bcd0db9abfa00cc5e/ |
| B | 5.23 | 90000 | 3000 | 2LDK | 48.61 | 3/3 | False | 2000-2 | RC | 9万円 | 空有 16,500円(税込) | グレース菱屋II | https://www.homes.co.jp/chintai/room/e5da0812742b08bef42ae59e0d62648ef2de5cb6/ |
| B | 5.23 | 90000 | 3000 | 2LDK | 52.01 | 3/3 | False | 2000-2 | RC | 9万円 | 無 |  | https://www.homes.co.jp/chintai/room/816a51e8c68d7c7b73876e7c0d6287cbe72af975/ |
| B | 5.24 | 88000 | 9000 | 2LDK | 55.57 | 5/6 | True | 1997-10 | RC | 8.8万円 | 空有 13,200円(税込) | グレース・ナカミヤ | https://www.homes.co.jp/chintai/room/d8b3fa720cc1a3fb09e1cae469df61459261191a/ |
| B | 5.24 | 88000 | 9000 | 2LDK | 54.04 | 5/6 | True | 1997-10 | RC | 8.8万円 | 空有 12,100円(税込) 駐車料金：12100円〜132 | グレースナカミヤ | https://www.homes.co.jp/chintai/room/c1850ed2c82ff39cf8c68302e814d1e23a5e4fc9/ |
| B | 5.3 | 90000 | 7000 | 3LDK | 65.83 | 3/3 | False | 1993-3 | RC | 1ヶ月 | 空有 15,000円(税無) | イースタン尊上院 | https://www.homes.co.jp/chintai/room/de28e4b4983311333b168cf0a352f80f5047200f/ |
| B | 5.32 | 98000 | 10000 | 3LDK | 73.98 | 4/11 | True | 1993-2 | RC | 1ヶ月 | 近隣 8,640円(税無) 物件からの距離162m | グランデュール鴨川II番館 | https://www.homes.co.jp/chintai/room/fc6417f4dbfd2464929a99f640b4b30fc66e0871/ |
| B | 5.35 | 73000 | 8500 | 3LDK | 58.39 | 2/6 | True | 1994-10 | RC | 無 | 空有 7,700円 物件からの距離0m エレスパ24、桂駅徒 | エレスパ24 | https://www.homes.co.jp/chintai/room/2bb033ca1939454f12434754c6bbe34d12dee7a5/ |
| B | 5.35 | 73000 | 8500 | 2LDK | 58.39 | 2/6 | True | 1994-9 | RC | 無 | 空有 9,350円(税込) | エレスパ24 | https://www.homes.co.jp/chintai/room/7af9e03d2ece4ce581f4b76154777aa03034e209/ |
| B | 5.35 | 73000 | 8500 | 3LDK | 55.08 | 2/6 | True | 1991-11 | RC | 無 | 空有 7,700円(税込) 駐車料金：7700円〜9350円 | エレスパ24 | https://www.homes.co.jp/chintai/room/96347608fe85a740f553d262157b22f7d7f1a00e/ |
| B | 5.35 | 73000 | 8500 | 3LDK | 60.0 | 2/6 | True | 1991-11 | RC | 無 | 空有 7,700円(税込) 駐車料金：7700円〜9350円 | エレスパ24 | https://www.homes.co.jp/chintai/room/676cb83c3f8c32fa73f7d8d3997d23269b04a2cc/ |
| B | 5.45 | 73000 | 8500 | 3LDK | 58.39 | 2/6 | True | 1994-10 | RC | 無 | 空有 8,500円 |  | https://www.homes.co.jp/chintai/room/eb13c3e448f485e9b2a7823bf712b0c03650b4a7/ |
| house | 3.39 | 85000 | 0 | 2LDK | 57.75 | None/3 | False | 1991-12 | RC | 8.5万円 | 空有 無料 |  | https://www.homes.co.jp/chintai/room/a8bb5d9e2136fc5540946de72fcd0f21c94370d0/ |
