# Refined survey around the office (3 km)

Same as ../walk/spec_walk.md, with these changes:
- Workspace: /tmp/claude-0/-home-user-Amity-/22382558-b3a7-5365-bb7f-d8dac5ad9eda/scratchpad/walk3/ — write walk3/out/<source>.json (+ .md), raw pages to walk3/out/raw/<source>/. walk3/geo.py has CENTER = the office.
- Radius: keep listings ≤ 3.0 km straight-line from CENTER (final filter = bike route ≈ 3 km / ~12 min for apartments, walking ≤ 15 min for detached houses).
- Wards: 北区 26101, 上京区 26102, 左京区 26103, 中京区 26104, 東山区 26105, 下京区 26106.
- Rent (賃料, without 管理費) ≤ 140,000 yen. Server-side rent cap 14万 is fine.
- Still 2LDK+ and ≥ 45 m². No 礼金 filter, no age filter, no floor filter (the report applies: detached houses built before 1980 are dropped; 礼金 > 2 months or > 250,000 yen goes to a separate list).
- Same schema; copy the 駐車場 text exactly; geo_precision as before.
