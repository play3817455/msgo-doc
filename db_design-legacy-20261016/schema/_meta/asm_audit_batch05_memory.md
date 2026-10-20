# Memory Offset 人工核对 — Batch #5

**日期:** 2026-09-20  
**方法:** IDA 读/写器逐字段 walk；仅 wire≠mem 打 `memory_offset`。

## 汇总

| 表 | 读器 | 线/槽 | 打标 | 说明 |
|---|---|---:|---:|---|
| phase_info | sub_B46D20 | 13/16 | 3/4 | phase@0 wire==mem；round/open/close +3B pad |
| bracket_info | sub_B46D80 | 46/52 | 10/11 | i8 后 3B pad；name 9B 后 3B pad（已标） |
| block_detail | sub_B43100 | 113/132 | — | layout_same_as lpcard（18 标继承） |
| buildup_info | sub_B44050 | 42/44 | 1/2 | up_param wire@14 → mem@16 |
| challenge_info | sub_B07540 | 13/20 | 0 | wire==mem @0/4/8/12 |
| trchallenge_info | sub_B07540 | 13/200 | — | layout_same_as challenge_info |
| check_quest | sub_B06C00 | 133/136 | 8/10 | title 后尾 8×u32 +3B pad |
| wave_res | sub_B08020 | 34/44 | 12/15 | 首 3×u8 wire==mem；后续槽对齐 |
| appear_info | sub_B07EC0 | 86/96 | 15/17 | snapshot 嵌套 @36（sub_B075A0） |
| avatar | sub_B068B0 | 18/24 | 6/10 | 前缀 @0–6 wire==mem；u16/u32 后 pad |

## avatar 要点（sub_B068B0）

- wire==mem：`avatar_id`@0、`gender`@4、`face`@5、`skincolor`@6
- `clothes` wire@7 → mem@8（+1B pad）
- `hair` wire@9 → mem@12（+3B pad）
- `accessory`/`frame`/`voice` wire@13–15 → mem@16–18（+3B）
- `byword` wire@16 → mem@20（+4B）；claim 0x18=24

## 提取器假阳性（人工 override）

- **bracket_info** `bracket_name`@16：循环 `a1+16+i`
- **appear_info** `snapshot`@36：`sub_B075A0(a1+36)` 嵌套读
