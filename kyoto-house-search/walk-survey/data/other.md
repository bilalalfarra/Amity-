# other — small agencies' own sites, WALK survey (≤1.3 km of 左京区吉田河原町14), fetched 2026-10-18

## Sources used
- **八清 (hachise.jp)** — 京町家 / 戸建 specialist, mostly own-managed or 専任 listings. Rental list `https://www.hachise.jp/rent/list/index.html` (one page, ~50 items incl. shops, land, share houses). Items in 左京/上京/中京 with 2LDK+ and ≥45 m² within ~1.5 km by town geocode → 4 unit pages fetched (HTTP 200) and kept (≤1.3 km). Skipped: 69573 (事業用 land, 俵屋町), 70547 (事業用, 新町錦), 70571 (2K), amu-kyoto (1LDK share), shops, and everything > 1.5 km. Rent = 居住用 rent; 築年 often 「築不詳」 (only a 明治/大正 record) → built_year null, record in notes.
- **三井のリハウス (rehouse.co.jp/rent)** — 分譲賃貸 listings: 左京区 4, 上京区 3, 中京区 21 (all 中京区 ones are 烏丸御池/四条/二条 > 1.7 km). 6 unit pages fetched (HTTP 200); only 上御霊アーバンライフ (1.19 km) is ≤ 1.3 km; the 岡崎 / 下鴨西林町 / 今出川新町 ones are 1.52–1.69 km.

## Tried, not usable
- エリッツ (eretz.co.jp): the session's egress proxy refuses the CONNECT (HTTP 502 "policy denial or upstream failure") for eretz.co.jp / www.eretz.co.jp → blocked here. (eretz.jp is an unrelated floor-heating maker.) エリッツ's listings do appear on Yahoo!不動産 (e.g. 株式会社エリッツ京都大学前店), so out/yahoo.json covers part of them.
- 長栄 (chouei.co.jp): every URL (incl. robots.txt via www) answers 403 Forbidden from the site's web server → blocked from this network; not pursued.
- ハウスメイト (housemate-navi.jp): works (`/look/result?pref_cd=26&city_cd=…&room_layout_type=…&square_lower=45`), but only 2 left-ward rooms (岩倉, 4.6 km) and one 上京区 house (千本下立売, ~2 km) → 0 kept (out/housemate.json = []).
- 京都R不動産 (realkyoto.jp): 403 Forbidden.

## Result
- **Kept 5 units** (after merging 0 duplicate listings of the same unit).
- Listings whose address is ward-only (no town): 0 located via nearest station (noted in `notes`), 0 of them dropped as >1.3 km.
- Within 1.0 km: 2; rent range kept: 130000–498000 円.
- By tier (A 2001+, B 1991–2000, old <1991, house): {'house': 4, 'B': 1}; 礼金 ≤1ヶ月 3, >1ヶ月 2, unknown 0 (no 礼金 limit in this survey).
- Elevator yes/no/unknown: 1/0/4; by ward: {'左京区': 4, '上京区': 1}.
- Every kept URL is the unit's own page, fetched with HTTP 200 during this run (raw copy under out/raw/other/).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷 / 礼 | 礼(月) | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.7 | 吉田近衛町の京町家（京都市左京区吉田近衛町） | 5K | 102.3 | 130,000 | None | 130,000円 (居住用) / 130,000円 (居住用) | 1.0 | None/2 | ? | None/None | 木造 | 駐輪スペース／駐車スペース: 無／無 | house | https://www.hachise.jp/rent/71507/index.html |
| 0.94 | 五山の送り火を望む、左京・吉田中大路の眺望邸 | 3LDK | 114.18 | 498,000 | None | 498,000円 / 498,000円 (居住用) | 1.0 | None/2 | ? | None/None | 木造 | 駐車スペース: 有 | house | https://www.hachise.jp/rent/70564/index.html |
| 1.1 | 平安神宮西　岡崎と暮らす家（京都市左京区岡崎 | 3DK | 52.4 | 150,000 | None | 150,000円 / 150,000円 | 1.0 | None/2 | ? | 1982/5 | 木造 | 駐輪スペース／駐車スペース: 無／無 | house | https://www.hachise.jp/rent/70580/ |
| 1.19 | 上御霊アーバンライフ | 3LDK | 94.44 | 200,000 | 20000 | 1ヶ月 / 2ヶ月 | 2.0 | 3/6 | Y | 1997/4 | RC | 空有 月額20,000円 | B | https://www.rehouse.co.jp/rent/bkdetail/4YL25265/ |
| 1.25 | 京都・岡崎エリア　事業の拠点となる改装済み一 | 6DK | 118.57 | 228,000 | None | 228,000円 (居住用) / 250,800円 (居住用) | 1.1 | None/2 | ? | None/None | 木造 | 駐輪スペース／駐車スペース: 無／無 | house | https://www.hachise.jp/rent/69576/ |
