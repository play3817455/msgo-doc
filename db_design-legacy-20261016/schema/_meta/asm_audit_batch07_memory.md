# Memory Offset 人工核对 — Batch #7

**日期:** 2026-09-20  
**方法:** IDA 读/写器逐字段 walk；仅 wire≠mem 打 `memory_offset`。

## 汇总

| 表 | 读器 | 线/槽 | 打标 | 说明 |
|---|---|---:|---:|---|
| member | sub_B454D0 | 52/64 | — | layout_same_as leaders（2 标继承） |
| intro_info | sub_B46140 | 547/547 | 0 | wire==mem 全长；循环写 notice_body |
| hack_check | sub_B065D0 | 79/88 | 25/29 | u16 后 2B 对齐（已标） |
| lvjudge_hist | sub_B44750 | 369/372 | 1/8 | 仅 `term_old`@272（termstr 后 +3B） |
| mprogress | sub_B07880 | 46/64 | — | layout_same_as progress（6 标继承） |
| netcafe_challenge_info | sub_B07540 | 13/60 | 0 | layout_same_as challenge_info |
| unlocked_navi | sub_B434B0 | 8/8 | 0 | 2×u32 wire==mem |
| pointdmg | sub_B45760 | 12/24 | 0 | gaugedmg 3×u32 wire==mem（移除误标@4） |
| total_result_wave | sub_B4DCC0 槽 | 19/20 | 4/7 | 3×u8 +1B pad；u32@4/8/12/16 |
| recruit | sub_B45400 | 74/84 | 4/7 | 已校正；comment@12 循环写 |

## total_result_wave 要点

- 前缀 `end_wave`/`result_coop`/`rank` wire==mem @0–2
- 打印器 `sub_B4DCC0` 槽：`rank_score`@4、`container_comp`@8、`enemyobj_comp`@12、`total_score`@16

## lvjudge_hist 要点

- 前缀至 `termstr_now`@204 wire==mem
- `term_old` wire@269 → mem@272（a1+68×4）

## pointdmg 修正

- 先前 `gaugedmg`@4 为误标；读器 `a1+4*(v2+i)` 首项 @0
