# Price survey: homes within a 10-minute WALK of the office (no price / key-money limits)

Office: 京都技術科学センター, 京都市左京区吉田河原町14 — lat 35.023968, lon 135.773178 (near 出町柳 / 荒神橋).
Workspace: /tmp/claude-0/-home-user-Amity-/22382558-b3a7-5365-bb7f-d8dac5ad9eda/scratchpad/walk/
- walk/geo.py has CENTER = the office. Write outputs to walk/out/<source>.json (+ .md), raw pages to walk/out/raw/<source>/.
- Reuse the earlier scripts (in ../sakyo/ and the parent dir) by COPYING them into walk/ and adapting. Never modify the originals or other out/ dirs.

Wards: 左京区 26103, 上京区 26102, 中京区 26104 (only the part near 丸太町). Keep listings ≤ 1.3 km straight-line from CENTER
(the final report filters by real walking time ≤ 10 min, so don't filter tighter than 1.3 km).

KEEP (the only hard rules):
- 2LDK or bigger (2LDK, 2SLDK, 3DK, 3LDK, 4DK, 4LDK …) AND floor area ≥ 45 m². Detached houses / terrace houses (一戸建て・テラスハウス) count too if they meet these.

NO other filters: no rent limit, no 礼金 limit, any building age, any floor (1F allowed), any structure, elevator or not.
Record everything in the schema of ../spec.md (rent, kanrihi, shikikin, reikin, other_initial, layout, area_m2, floor, building_floors,
elevator, built_year, structure, parking text + fee, nearest_station, address, lat/lon, distance_km, url, notes) — parking is important:
copy the listing's 駐車場 text exactly. Set "tier": "house" for detached/terrace houses, otherwise "A" (built 2001+), "B" (1991–2000), "old" (before 1991).
Every kept URL must be the unit's own page and return HTTP 200.
