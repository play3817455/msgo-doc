# Memory Offset 人工核对 — Batch #3

**日期:** 2026-09-20  
**方法:** IDA 读/写器逐字段 walk；仅 wire≠mem 打 `memory_offset`。

## 汇总

| 表 | 读器 | 线/槽 | 打标 | 说明 |
|---|---|---:|---:|---|
| item_list | sub_B458A0 | 23/24 | 1/7 | 仅 `stock`@22（bit_eff 后 +1B） |
| party_member_stat | sub_B454D0 族 | 36/40 | 5/8 | avatar@16 等（已标） |
| order | sub_B46420 | 10/10 | 0 | wire==mem 全长 |
| rankself | sub_B464A0 | 40/40 | 0 | wire==mem 全长 |
| ranking | sub_B46560 | 95/104 | 7/12 | name 后 +1B；avatar 槽 22B |
| toppilots | sub_B46560 | 95/104 | — | layout_same_as ranking |
| ranking_info | sub_B46420 | 10/10 | 0 | layout_same_as order |
| special_a_info | sub_B464A0 | 40/40 | 0 | layout_same_as rankself |
| special_a_next | sub_B46CD0 | 12/12 | 0 | wire==mem 全长 |
| sort_info | sub_B461E0 | 18/24 | 2/12 | `order_offset`@16、`bit_show`@20 |

## ranking 要点（sub_B46560）

- 前缀 `rank`/`pilot_id`/`name`/`troops`/`level` wire==mem
- `clan_id`@36（wire@35）；`clan_name`@40；尾 `avatar`@80

## sort_info 要点（sub_B461E0）

- 前缀 byte/u16 字段 wire==mem @0–12
- `order_offset` wire@13 → mem@16（+3B pad）
- `bit_show` wire@17 → mem@20
