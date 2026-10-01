# able — エイブル (able.co.jp), fetched 2026-10-01

## Method
- List URL pattern: https://www.able.co.jp/kyoto/area/<ward>/list/?m=5&m=6&m=7&m=8&m=9&m=A&m=B&sf=45&st=0&h=7&b=1&b=2&b=3&n=B (m = 2LDK(+S)/3K-3DK/3LDK(+S)/4K-4DK/4LDK(+S)/5K+/5LDK+, sf=45 m² min, h=7 → 築25年以内, b = アパート/マンション/戸建, n=B include 定期借家); pagination is `&i=N`. The rent cap `ct=` is ignored by the server, so rent ≤100,000 was applied client-side.
- Two sweeps: A (h=7, 築25年以内) 22 pages and B (h=99 no age limit, for 1991–2000 RC/SRC) 36 pages, 9 wards (下京/中京/南/右京/上京/西京/東山/北/伏見) → 954 unique room listings (bk keys).
- Client-side funnel: age/structure fail 268, rent >100,000: 509, 1F: 38, >5.5 km: 54 → 85 candidates → fetched every detail page (Detail.do?bk=…, all HTTP 200) → 礼金 >1ヶ月 −19, 4F+ without elevator −2 → **63 kept**. Distances use the exact lat/lon embedded in each list card (showGoogleMap), so they are block-level accurate.
- Kept by tier: {'B': 57, 'A': 6}; elevator yes/no: {True: 42, False: 21}; by ward: {'南区西': 1, '右京区': 10, '南区吉': 1, '南区上': 2, '東山区': 1, '西京区': 25, '南区久': 17, '北区紫': 1, '伏見区': 5}.
- Notes: エイブル lists 仲介手数料 0.55ヶ月 (half month) on most units; 諸費用 (鍵交換, 清掃, サポート費) are in `other_initial`. Some units are 空予定 (vacating later) — see `movein`. `parking` is quoted verbatim ('有料駐車場1台(13,200円/月)', 'なし' etc.).

## Kept units (closest first)
| km | building | layout | m² | rent | 管理費 | 敷/礼 | floor | EV | built | struct | parking | tier | url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.94 | プレジオ東寺 | 2LDK+S | 57.8 | 99,000 | 8000 | なし/--/なし/-- | 6/6 | Y | 1997/2 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000709027856004&prefkey=kyoto |
| 2.47 | グランビュ－葛野 | 2LDK | 56.91 | 84,000 | 10000 | 8.4万/--/8.4万/-- | 3/4 | Y | 1997/2 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000703186970006&prefkey=kyoto |
| 2.55 | ｻﾆ-ｸﾚｽﾄ祥山 | 3LDK | 60.96 | 80,000 | 9000 | 8万/--/8万/-- | 3/7 | Y | 1999/3 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000709058586017&prefkey=kyoto |
| 2.65 | コンフォール | 3LDK | 65.0 | 89,000 | 9500 | なし/--/8.9万/-- | 5/7 | Y | 1995/10 | RC | 有料駐車場1台(12,100円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000709635443001&prefkey=kyoto |
| 2.65 | コンフォール | 2LDK | 65.16 | 89,000 | 9500 | なし/--/8.9万/-- | 5/7 | Y | 1995/10 | RC | 有料駐車場1台(12,100円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000709635443007&prefkey=kyoto |
| 2.95 | Ｒｏｓｙ　Ｇａｒｄｅｎ | 2LDK | 48.87 | 87,000 | 8000 | 8.7万/--/8.7万/-- | 3/3 | n | 1994/4 | RC | 有料駐車場1台(22,000円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000704043982009&prefkey=kyoto |
| 3.1 | サンクスシティFUKUI | 3LDK | 60.42 | 84,000 | 9000 | なし/--/8.4万/-- | 3/5 | Y | 1995/11 | RC | 有料駐車場1台(14,300円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706539692006&prefkey=kyoto |
| 3.18 | サンハイム井上 | 2LDK | 66.63 | 86,000 | 11500 | 8.6万/--/8.6万/-- | 3/5 | Y | 1996/8 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000706561309007&prefkey=kyoto |
| 3.18 | サンハイム井上 | 2LDK | 66.63 | 90,000 | 11500 | 9万/--/9万/-- | 5/5 | Y | 1996/8 | RC | 有料駐車場1台(11,000円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706561309005&prefkey=kyoto |
| 3.21 | プレミエｰルクラーテ | 2LDK | 49.05 | 81,000 | 8000 | なし/--/8.1万/-- | 3/7 | Y | 1997/1 | RC | 有料駐車場1台(9,900円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706028985023&prefkey=kyoto |
| 3.33 | コンフィアンサ桂 | 2LDK | 59.22 | 91,000 | 12000 | なし/--/9.1万/-- | 2/5 | Y | 2003/3 | RC | 有料駐車場1台(13,200円/月)  | A | https://www.able.co.jp/detail/Detail.do?bk=000000706090315005&prefkey=kyoto |
| 3.34 | レクイエ上桂 | 3LDK | 65.0 | 93,000 | 5000 | なし/--/9.3万/-- | 3/3 | n | 1994/3 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000706070738011&prefkey=kyoto |
| 3.35 | GARNET RESIDENCE上桂 | 3LDK | 65.0 | 96,000 | 8000 | なし/--/なし/-- | 2/5 | Y | 1991/9 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706142383003&prefkey=kyoto |
| 3.35 | GARNET RESIDENCE上桂 | 3LDK | 69.89 | 91,000 | 8000 | なし/--/なし/-- | 3/5 | Y | 1991/9 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706142383007&prefkey=kyoto |
| 3.4 | プリメ－ル桂 | 2LDK | 55.0 | 69,000 | 8000 | なし/--/なし/-- | 2/5 | Y | 1993/4 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000706128628001&prefkey=kyoto |
| 3.46 | ラティエール桂 | 2LDK | 56.76 | 75,000 | 5000 | なし/--/なし/-- | 3/4 | n | 1994/6 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000706675254010&prefkey=kyoto |
| 3.46 | ラティエール桂 | 2LDK | 55.07 | 70,000 | 5000 | なし/--/なし/-- | 3/4 | n | 1994/6 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000706675254011&prefkey=kyoto |
| 3.47 | ナチュールＫＩＣＨＩ | 3LDK | 58.0 | 72,000 | 9000 | 10万/--/5万/-- | 4/4 | Y | 1991/7 | RC | 有料駐車場1台(10,000円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706058115004&prefkey=kyoto |
| 3.48 | ラビリント川島 | 3LDK | 65.23 | 87,000 | 8000 | なし/--/なし/-- | 4/6 | Y | 1993/11 | RC | 有料駐車場1台(8,800円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706008240008&prefkey=kyoto |
| 3.5 | カノン | 2LDK | 53.49 | 80,000 | 8000 | なし/--/なし/-- | 4/5 | Y | 1994/11 | RC | 有料駐車場1台(13,200円/月)/バイク置場あり  | B | https://www.able.co.jp/detail/Detail.do?bk=000000703595542015&prefkey=kyoto |
| 3.5 | カノン | 3LDK | 64.89 | 92,000 | 8000 | なし/--/なし/-- | 2/5 | Y | 1994/11 | RC | 有料駐車場1台(13,200円/月)/バイク置場あり  | B | https://www.able.co.jp/detail/Detail.do?bk=000000703595542007&prefkey=kyoto |
| 3.61 | グランド－ル桂川畔 | 2LDK | 56.38 | 78,000 | 0 | なし/10万/なし/10万円 | 4/6 | Y | 1995/3 | RC | 有料駐車場1台(9,000円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706028800013&prefkey=kyoto |
| 3.67 | メゾン桂川 | 2LDK | 54.04 | 67,000 | 9000 | 6.7万/--/6.7万/-- | 5/7 | Y | 1995/2 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706109043037&prefkey=kyoto |
| 3.67 | メゾン桂川 | 2LDK | 50.42 | 65,000 | 9000 | 6.5万/--/なし/-- | 2/7 | Y | 1995/2 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706109043016&prefkey=kyoto |
| 3.67 | メゾン桂川 | 3LDK | 61.68 | 75,000 | 9000 | 7.5万/--/7.5万/-- | 5/7 | Y | 1995/2 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706109043011&prefkey=kyoto |
| 3.75 | Sun　Bird　桂 | 3LDK | 64.18 | 85,000 | 8000 | なし/--/8.5万/-- | 3/6 | Y | 1997/3 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000706086566002&prefkey=kyoto |
| 3.81 | クォーク桂東 | 2LDK | 56.1 | 80,000 | 6000 | 8万/--/8万/-- | 2/3 | n | 1997/3 | RC | 有料駐車場1台(11,000円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706036186007&prefkey=kyoto |
| 3.83 | サンシャイン梅津 | 3LDK | 63.0 | 92,000 | 10000 | 9.2万/--/9.2万/-- | 7/7 | Y | 1994/5 | RC | 有料駐車場1台(10,000円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000723113872009&prefkey=kyoto |
| 3.85 | ノイシュロス御室南 | 3DK | 60.0 | 79,000 | 7000 | なし/--/なし/-- | 6/6 | Y | 1993/11 | RC | 有料駐車場1台(14,300円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000723618342010&prefkey=kyoto |
| 4.0 | アメニティ双ヶ丘 | 3LDK | 69.0 | 95,000 | 15000 | なし/--/なし/-- | 6/6 | Y | 1991/4 | RC | 有料駐車場1台(16,500円/月)/バイク置場あり  | B | https://www.able.co.jp/detail/Detail.do?bk=000000723066486015&prefkey=kyoto |
| 4.19 | カルム常盤 | 2LDK | 52.74 | 78,000 | 7000 | なし/--/なし/-- | 2/3 | n | 1995/9 | RC | 有料駐車場1台(14,300円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000723042624014&prefkey=kyoto |
| 4.35 | Ｍ レヴェンテ | 2LDK | 55.05 | 81,000 | 10000 | なし/--/8.1万/-- | 4/6 | Y | 1995/4 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706012841018&prefkey=kyoto |
| 4.36 | ラ・メゾン・ボヌール | 3LDK | 64.45 | 86,000 | 10000 | なし/--/8.6万/-- | 4/7 | Y | 1994/9 | RC | 有料駐車場1台(16,500円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706013222042&prefkey=kyoto |
| 4.36 | ラ・メゾン・ボヌール | 3LDK | 65.55 | 86,000 | 10000 | なし/--/8.6万/-- | 6/7 | Y | 1994/9 | RC | 有料駐車場1台(16,500円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706013222028&prefkey=kyoto |
| 4.45 | リントゥコト | 2LDK | 55.66 | 98,000 | 6000 | 9.8万/--/なし/-- | 2/2 | n | 2026/5 | 木造 | 有料駐車場1台(11,000円/月)  | A | https://www.able.co.jp/detail/Detail.do?bk=000000708746078004&prefkey=kyoto |
| 4.45 | リントゥコト | 2LDK | 55.66 | 98,000 | 6000 | 9.8万/--/なし/-- | 2/2 | n | 2026/5 | 木造 | 有料駐車場1台(11,000円/月)  | A | https://www.able.co.jp/detail/Detail.do?bk=000000708746078001&prefkey=kyoto |
| 4.47 | サントル西京 | 2LDK | 57.9 | 78,000 | 7000 | なし/7.8万/なし/7.8万円 | 6/7 | Y | 1996/11 | RC | 有料駐車場1台(14,300円/月)/バイク置場あり  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706028815003&prefkey=kyoto |
| 4.48 | WEST　SQUARE－Ⅱ | 3LDK | 69.75 | 100,000 | 5000 | 10万/--/なし/-- | 3/5 | Y | 1993/5 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000723594526005&prefkey=kyoto |
| 4.55 | カサ・デ・高の手 | 2LDK | 56.7 | 100,000 | 0 | 5万/--/10万/-- | 5/7 | Y | 1995/3 | RC | 無料駐車場1台  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706013217022&prefkey=kyoto |
| 4.58 | エクセル清涼 | 2LDK | 52.86 | 88,000 | 10000 | なし/--/8.8万/-- | 3/6 | Y | 1996/3 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706019237008&prefkey=kyoto |
| 4.58 | リジョイス桂 | 3LDK | 69.27 | 89,000 | 10500 | 8.9万/--/なし/-- | 2/3 | n | 1999/3 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706584182005&prefkey=kyoto |
| 4.62 | グランビア京都 | 3DK | 60.55 | 90,000 | 0 | なし/15万/なし/10万円 | 4/7 | Y | 1997/4 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000706031418003&prefkey=kyoto |
| 4.62 | ロイヤル清涼 | 3LDK | 61.02 | 95,000 | 10000 | なし/--/9.5万/-- | 3/6 | Y | 1992/11 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706015437012&prefkey=kyoto |
| 4.62 | ロイヤル清涼 | 2LDK | 55.89 | 86,000 | 10000 | なし/--/8.6万/-- | 3/6 | Y | 1992/11 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706015437014&prefkey=kyoto |
| 4.62 | ロイヤル清涼 | 3LDK | 61.02 | 95,000 | 10000 | なし/--/9.5万/-- | 3/6 | Y | 1992/11 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706015437001&prefkey=kyoto |
| 4.69 | ヴェルデ三番館 | 3LDK | 66.17 | 88,000 | 0 | なし/--/なし/-- | 3/3 | n | 1993/3 | RC | 無料駐車場1台  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706008299012&prefkey=kyoto |
| 4.69 | ヴェルデ三番館 | 3LDK | 70.06 | 96,000 | 0 | なし/--/なし/-- | 3/3 | n | 1993/3 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000706008299021&prefkey=kyoto |
| 4.7 | アントレデウブリ－ズ | 2LDK | 50.4 | 78,000 | 8000 | なし/--/なし/-- | 2/2 | n | 2004/11 | RC | なし | A | https://www.able.co.jp/detail/Detail.do?bk=000000706171331009&prefkey=kyoto |
| 4.76 | グランシャリオ | 3LDK | 66.6 | 85,000 | 5000 | なし/--/8.5万/-- | 2/3 | n | 1998/1 | RC | 有料駐車場1台(11,000円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706050435004&prefkey=kyoto |
| 4.82 | ロ－ファス小島 | 3LDK | 62.02 | 88,000 | 0 | なし/--/なし/-- | 2/3 | n | 1992/4 | RC | 無料駐車場1台  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706008270006&prefkey=kyoto |
| 4.83 | ア－バンエステ－トイトヤ | 3LDK | 60.0 | 95,000 | 0 | なし/--/9.5万/-- | 3/3 | n | 1994/4 | RC | 有料駐車場1台(11,000円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706082571008&prefkey=kyoto |
| 4.83 | プロスペクト桂 | 2LDK | 62.16 | 93,000 | 10000 | なし/--/なし/-- | 2/5 | Y | 1996/3 | RC | 有料駐車場1台(11,000円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706014502020&prefkey=kyoto |
| 4.84 | カサグランデ嵯峨野 | 3DK | 54.0 | 74,000 | 0 | なし/--/7.4万/-- | 3/4 | n | 1991/3 | RC | 有料駐車場1台(11,000円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000723000900007&prefkey=kyoto |
| 4.87 | 日本鉱産ビルグラハイツ | 3LDK | 62.37 | 95,000 | 4000 | 10万/--/9.5万/-- | 7/7 | Y | 1993/11 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000708054850008&prefkey=kyoto |
| 4.92 | サニ－ソシア21 | 2LDK | 60.49 | 79,500 | 8500 | なし/--/なし/-- | 3/3 | n | 2001/1 | 鉄骨 | 有料駐車場1台(11,000円/月)  | A | https://www.able.co.jp/detail/Detail.do?bk=000000706075362009&prefkey=kyoto |
| 4.98 | CASA SHIMEI | 2LDK | 53.0 | 92,000 | 10000 | なし/--/9.2万/-- | 2/4 | n | 1991/7 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000707057001002&prefkey=kyoto |
| 5.0 | ABC BLDG. | 2LDK | 48.0 | 78,000 | 8000 | なし/--/7.8万/-- | 3/5 | Y | 1995/1 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000705036905001&prefkey=kyoto |
| 5.03 | セントラルヴィレッジ | 3LDK | 69.13 | 88,000 | 8000 | 8.8万/--/8.8万/-- | 3/3 | n | 2000/2 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000723610585005&prefkey=kyoto |
| 5.03 | グレ－スダイン | 3DK | 65.99 | 95,000 | 9000 | なし/--/9.5万/-- | 7/7 | Y | 1995/9 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000705026470011&prefkey=kyoto |
| 5.11 | ｇｌａｎｚ　CLK　いちご館 | 2LDK | 62.09 | 86,000 | 4100 | なし/--/8.6万/-- | 2/3 | n | 2019/9 | 木造 | 有料駐車場1台(7,700円/月)  | A | https://www.able.co.jp/detail/Detail.do?bk=000000708589615005&prefkey=kyoto |
| 5.14 | グレース ナカミヤ | 2LDK | 55.57 | 88,000 | 9000 | なし/--/8.8万/-- | 5/6 | Y | 1997/9 | RC | 有料駐車場1台(13,200円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000705042997023&prefkey=kyoto |
| 5.2 | ｸﾞﾚｰｽ菱屋2 | 2LDK | 56.0 | 90,000 | 3000 | 9万/--/9万/-- | 2/3 | n | 2000/2 | RC | なし | B | https://www.able.co.jp/detail/Detail.do?bk=000000705067755006&prefkey=kyoto |
| 5.36 | ELESPA 24 | 3LDK | 58.39 | 73,000 | 8500 | 7.3万/--/なし/-- | 2/6 | Y | 1994/10 | RC | 有料駐車場1台(7,700円/月)  | B | https://www.able.co.jp/detail/Detail.do?bk=000000706014091004&prefkey=kyoto |