# eheya — いい部屋ネット (eheya.net, 大東建託), fetched 2026-10-01

## Method
- The site is a Next.js app; its filter panel builds the result client-side (no URL query parameters are exposed, and headless Chromium gets a CloudFront 403), so the SSR ward pages https://www.eheya.net/kyoto/area/<city>/search/?page=N were crawled **unfiltered** with curl (plain requests-lib sessions got 403 on ?page≥2; curl with a Chrome UA worked).
- Wards: 下京 291, 中京 218, 南 642, 右京 495, 上京 325, 西京 320, 東山 27, 北 178, 伏見 526 listings (site counts) → 73 list pages, 1799 unique room cards parsed (building, 築年, 階建, address, floor, rent, 管理費, 敷/礼, layout, area).
- Client-side funnel: layout not 2LDK+ 1453, area<45 3, rent>100,000 214, 築36+ 41, 1F 29, >5.5 km 22 → 37 candidates → detail pages fetched (HTTP 200; fields read from the page's __NEXT_DATA__ JSON: constructionDate, buildingStructure, story, propertyFeatures incl. LIFT, parkingText, keyMoney, renewal fees, specialNotes) → dropped: {'age/structure': 11, 'reikin': 6} → **20 kept**.
- Kept by tier: {'B': 17, 'A': 3}; elevator yes/no: {True: 8, False: 12}. Geocoding by town-level address (block numbers not shown) → ±300 m.
- Caveats: most いい部屋ネット stock is 大東建託 light-steel/wood apartments (軽量鉄骨/木造) — these pass only if built 2001+ (tier A). 礼金 is often quoted in yen (e.g. 130,000円 on a 99,000 rent = 1.31 months → dropped). 保証会社 fees and 'ruumサポート費用' etc. are in `other_initial`.

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷/礼 | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.36 | グラン・フォルム西院 | 2LDK | 48.33 | 85,000 | 9000 | 0円/1ヶ月 | 4/6 | Y | 1992/4 | RC | 無 | B | https://www.eheya.net/detail/300000832003767000001/ |
| 2.56 | コンフォール | 3LDK | 65 | 89,000 | 9500 | 0円/1ヶ月 | 5/7 | Y | 1995/10 | RC | 有 月12,100円(税込) | B | https://www.eheya.net/detail/300000472004013000009/ |
| 3.08 | LA・VITAROSA | 2LDK | 60.77 | 88,000 | 4100 | 0円/1ヶ月 | 2/2 | n | 2017/6 | 木造 | 有(敷地内) 月11,000円(税込) | A | https://www.eheya.net/detail/300000830000648005584/ |
| 3.2 | メゾンプルミエール桂 | 2LDK | 53 | 100,000 | 0 | 50,000円/0円 | 4/5 | Y | 1991/3 | RC | 有 | B | https://www.eheya.net/detail/300000832002915000005/ |
| 3.39 | 花園貸家5号地 | 2LDK | 66.45 | 85,000 | 0 | 0円/85,000円 | None/3 | n | 1992/6 | RC | 有 | B | https://www.eheya.net/detail/300000832009506000001/ |
| 3.62 | セントフローレンスパレス桂 311号室 | 3LDK | 68.42 | 90,000 | 0 | 0円/90,000円 | 3/7 | Y | 1995/11 | RC | 無 | B | https://www.eheya.net/detail/300000832009094000001/ |
| 4.07 | アメニティ双ヶ丘 | 3LDK | 69 | 95,000 | 15000 | 0円/0円 | 6/6 | Y | 1991/4 | RC | 有 月16,500円(税込) | B | https://www.eheya.net/detail/300000832003119000016/ |
| 4.22 | カルム常盤 | 2LDK | 52.74 | 78,000 | 7000 | 0円/0円 | 2/3 | n | 1995/9 | RC | 有 月14,300円(税込) | B | https://www.eheya.net/detail/300000832007455000003/ |
| 4.47 | ウエストコート大利 | 3LDK | 73.12 | 85,000 | 9000 | 0円/0円 | 5/5 | Y | 1998/5 | RC | 有 月13,200円(税込) | B | https://www.eheya.net/detail/300000832006622000003/ |
| 4.76 | ヴェルデ三番館 | 3LDK | 70.06 | 96,000 | 0 | 0円/0円 | 3/3 | n | 1993/3 | RC | 有 | B | https://www.eheya.net/detail/300000832000682000015/ |
| 4.76 | ヴェルデ三番館 | 3LDK | 66.17 | 88,000 | 0 | 0円/0円 | 3/3 | n | 1993/3 | RC | 有 | B | https://www.eheya.net/detail/300000832000682000009/ |
| 4.77 | グラン・シャリオ | 3LDK | 66 | 85,000 | 5000 | 0円/85,000円 | 2/3 | n | 1998/2 | RC | 有 月11,000円(税込) | B | https://www.eheya.net/detail/300000832009445000001/ |
| 4.78 | ローファス小島 | 3LDK | 62.02 | 88,000 | 0 | 0円/0円 | 2/3 | n | 1992/5 | RC | 有 | B | https://www.eheya.net/detail/300000832003937000001/ |
| 4.84 | アントレデゥブリーズ | 2LDK | 50.4 | 78,000 | 8000 | 0円/0円 | 2/2 | n | 2004/11 | RC | 無 | A | https://www.eheya.net/detail/300000832003214000001/ |
| 4.86 | カサグランデ嵯峨野 | 3DK | 57.54 | 74,000 | 0 | 0円/74,000円 | 3/4 | n | 1991/3 | RC | 有 月11,000円(税込) | B | https://www.eheya.net/detail/300000832009099000001/ |
| 4.87 | プロスペクト桂 | 2LDK | 62.16 | 93,000 | 10000 | 0円/0円 | 2/5 | Y | 1996/3 | RC | 有 月11,000円(税込) | B | https://www.eheya.net/detail/300000832005911000010/ |
| 4.91 | レジディア太秦 | 2LDK | 62.19 | 82,000 | 10000 | 1ヶ月/0円 | 2/7 | n | 2000/1 | RC | 要問い合わせ | B | https://www.eheya.net/detail/300000832006445000010/ |
| 5.09 | クレセント・オークス | 2LDK | 56.8 | 70,000 | 4000 | 1ヶ月/1ヶ月 | 2/3 | n | 1995/8 | RC | 有 月8,000円(税込) | B | https://www.eheya.net/detail/300000832003178000003/ |
| 5.3 | glanz CLK いちご館 | 2LDK | 62.09 | 86,000 | 4100 | 0円/1ヶ月 | 2/3 | n | 2019/9 | 木造 | 有(敷地内) 月7,700円(税込) | A | https://www.eheya.net/detail/300000470000926007301/ |
| 5.35 | エレスパ24 | 3LDK | 58.39 | 73,000 | 8500 | 1ヶ月/0円 | 2/6 | Y | 1994/10 | RC | 有 月7,700円(税込) | B | https://www.eheya.net/detail/300000832002975000004/ |