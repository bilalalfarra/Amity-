# Yahoo!不動産 (realestate.yahoo.co.jp/rent/) — quick probe only (not crawled)

Probed 2026-10-01 23:1x JST with plain requests (Chrome UA), 5 requests total. Raw pages under `out/raw/yahoo/`.

- `/rent/` → 200 (SPA-ish top page). `/rent/search/26/` and `/rent/search/26/26106/` → 404 (these were the "obvious" URLs that failed earlier).
- Working URL scheme discovered: area code first → `/rent/06/26/` = 京都府 (06 = 近畿, 26 = 京都府), ward search = `/rent/search/06/26/26106/` (下京区, 200, **5,482件** unfiltered, SSR HTML 1.9 MB with the listings inline).
- Detail URLs look like `/rent/detail/<40-hex-id>/`; pagination `?page=N`.
- The filter controls on the ward page are JS-driven `<select>`s with empty `value` attributes (sort / 賃料下限 / 上限 / 面積 …), so the query-string format for rent/area/layout/age filters could not be read from the HTML; it would need a Playwright session to submit the form and read the resulting URL.
- Not pursued further (time was spent on CHINTAI and at home); nothing from Yahoo is in the JSON outputs. Kyoto ward codes for later: 26106 下京区, 26104 中京区, 26107 南区, 26108 右京区, 26102 上京区, 26111 西京区, 26105 東山区, 26101 北区, 26109 伏見区, 26103 左京区.
