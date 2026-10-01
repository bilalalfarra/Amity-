# Kyoto rental search — shared spec for all search agents

## Goal
Find rental homes in Kyoto city for a tenant who works at **Kyoto Technoscience Center (京都技術科学センター)**,
inside Kyoto Research Park (KRP), 京都市下京区中堂寺南町134, next to JR 丹波口駅.
Reference point (CENTER): **lat 34.9951, lon 135.7405**.

Commute is by bicycle, max ~20 min → collect everything within **5.5 km straight-line** of CENTER
(we filter later; record the distance for every listing). Wards in range: 下京区, 中京区, 南区, 右京区 (east half: 西院/西京極/太秦/花園/山ノ内),
上京区 (south half), 西京区 (桂 area), 東山区 (west part), 北区 (south edge), 伏見区 (north edge: 竹田/久我) — skip anything > 5.5 km.

## Hard filters (collect only listings that satisfy ALL)
- Layout: **2LDK or bigger** (2LDK, 2SLDK, 3DK, 3LDK, 3SLDK, 4DK, 4LDK …). NOT 1LDK, NOT 2DK, NOT 2K.
- Floor area: **≥ 45 m²**.
- Rent (賃料, excluding 管理費/共益費): **≤ 100,000 yen**. Record 管理費 separately.
- Key money 礼金: **≤ 1 month of rent** (0 is best). Deposit 敷金 is fine (record it).
- Floor: **NOT the 1st floor (1階)**. 2F–3F fine with or without elevator. **4F or higher only if the building has an elevator.**
  Detached houses (一戸建て/テラスハウス) are acceptable but lower priority — collect them in a separate tier (`tier: "house"`).
- Building age — two tiers, record `tier`:
  - `tier: "A"` → built **2001 or later** (築25年以内). Any structure.
  - `tier: "B"` → built **1991–2000** (築26–35年) **only if** structure is RC / SRC (鉄筋コンクリート / 鉄骨鉄筋コンクリート). Skip older than 1991 entirely. Skip 軽量鉄骨 / 木造 older than 2001.
  (Reason: tenant must have real thermal insulation — avoid old light-steel/wood buildings.)
- Parking: record exactly what the listing says (敷地内 駐車場 with monthly fee / 近隣 / 空無 / なし). Listings **without** parking are still collected — we match nearby monthly lots later.

## For EVERY listing you keep, you MUST record a direct URL to that specific unit (not the search page), and verify it returns HTTP 200 and still shows the unit.

## Output
Write a JSON array to `/tmp/claude-0/-home-user-Amity-/22382558-b3a7-5365-bb7f-d8dac5ad9eda/scratchpad/out/<source>.json`
(one file per site; sources: suumo, homes, athome, chintai, ur, jkosha, sumaity, eheya, able, other).
Each object:
```json
{
  "source": "suumo",
  "url": "https://suumo.jp/chintai/jnc_000012345678/",
  "building_name": "○○マンション",
  "address": "京都府京都市南区西九条○○町12",
  "lat": 34.98, "lon": 135.74, "distance_km": 1.9,
  "rent": 95000, "kanrihi": 5000,
  "shikikin": "95,000円 (1ヶ月)", "reikin": "0円", "other_initial": "仲介手数料 1ヶ月, 保証会社 必須 …",
  "layout": "2LDK", "area_m2": 55.2,
  "floor": 3, "building_floors": 5, "elevator": true,
  "built_year": 2008, "built_month": 3, "age_years": 18,
  "structure": "RC",
  "parking": "敷地内 12,000円/月 空有", "parking_fee": 12000,
  "nearest_station": "JR 丹波口 徒歩8分",
  "tier": "A",
  "notes": "ペット相談可, 南向き, オートロック …",
  "fetched_at": "2026-10-01T14:00:00+09:00"
}
```
Use `null` for unknown values — never guess. `elevator` must be true/false/null from the listing's 設備 text (エレベーター).
`structure` ∈ {"RC","SRC","重量鉄骨","軽量鉄骨","鉄骨","木造","その他"} (鉄骨造 with unknown weight → "鉄骨").

## Geocoding / distance
Use `python3 geo.py "<address>"` in the scratchpad dir → prints `lat lon distance_km` (GSI geocoder, cached, polite 0.3 s sleep).
Or import it: `from geo import geocode, dist_km`. Town/chome-level precision is fine.

## Etiquette
- Max ~1 request/second per site, realistic Chrome User-Agent, retry once on 5xx. No parallel hammering.
- Save raw HTML of search pages under `out/raw/<source>/` so results can be audited.
- When done, also write a short `out/<source>.md` summary: how many pages scanned, how many kept, what filters the site could/couldn't apply server-side, any problems (blocks, captchas).
