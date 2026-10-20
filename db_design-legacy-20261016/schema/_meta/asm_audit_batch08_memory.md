# Memory Offset 人工核对 — Batch #8

**日期:** 2026-09-20  
**方法:** IDA 读/写器逐字段 walk；仅 wire≠mem 打 `memory_offset`。

## 汇总

| 表 | 读器 | 线/槽 | 打标 | 说明 |
|---|---|---:|---:|---|
| replay_info | sub_B47340 | 38/40 | 5/10 | u64/id wire==mem；2×u8 后 u32 槽 @20–36 |
| season_rb_conf | sub_B471E0 | 52/56 | 0 | 全长 wire==mem；尾 +4B pad |
| precord | sub_B440B0 | 242/252 | 8/61 | 60×u32 wire==mem；尾 8×u16 @212–240 |

## replay_info 要点（sub_B47340）

- `id` u64 @0 wire==mem（移除误标 memory_offset@4）
- `missionId`/`time` @8/12 wire==mem
- `troopsA`/`troopsB` @16/17 wire==mem
- `endDate` wire@18 → mem@20；后续 4×u32 +2B 步进

## precord 要点

- 前缀 60×u32（wire@0–239）wire==mem
- 尾段 u16 字段 wire 208–238 → mem 212–240（+2B 对齐，8 标已存在）
