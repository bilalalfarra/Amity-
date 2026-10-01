# Re-run spec (correct workplace)

The first run used the WRONG reference point (KRP, 下京区). The real workplace is
**公益財団法人 京都技術科学センター, 京都市左京区吉田河原町14 (〒606-8305)** — lat **35.023968**, lon **135.773178**
(near 出町柳 / 荒神橋, east bank of the 鴨川).

Workspace: `/tmp/claude-0/-home-user-Amity-/22382558-b3a7-5365-bb7f-d8dac5ad9eda/scratchpad/sakyo/`
- `sakyo/geo.py` = same helper as before but CENTER = the new point. Import it from scripts placed in `sakyo/`.
- Write outputs to `sakyo/out/<source>.json` (+ `.md`), raw pages to `sakyo/out/raw/<source>/`.
- The old scripts in the parent scratchpad dir are reusable — COPY them into `sakyo/` and adapt (wards, center, output dir). Do not modify the originals or anything in `../out/`.

Wards to cover: 左京区 26103, 上京区 26102, 北区 26101, 中京区 26104, 東山区 26105, 下京区 26106 (north part). Keep anything ≤ 5.5 km straight-line from CENTER.

Listing filters are the same as `../spec.md` EXCEPT 礼金: keep **礼金 ≤ 2 months** (the final report splits ≤1 month and 1–2 months).
Output schema is the same as `../spec.md`.
