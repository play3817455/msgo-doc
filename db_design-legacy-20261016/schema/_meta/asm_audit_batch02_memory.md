# Memory Offset 人工核对 — Batch #2

**日期:** 2026-09-20  
**状态:** 完成（逐表 IDA 读器 walk，无批量脚本改 JSON）

## 汇总

| 表 | 读器 | 线/槽 | 打标 | wire==mem 前缀 |
|---|---|---:|---:|---|
| lpcard | sub_B45180 | 132/132 | 18/20 | pilot_id, name |
| ms | sub_B45780 | 264/264 | 42/43 | uniqid |
| snapshot | sub_B45380 | 44/44 | 4/8 | 前 4 字段 |
| funnelss | sub_B45280 | — | 已标 | — |
| unlockw | sub_B45300 | 32/32 | 已标 | — |
| adop_list | sub_B45080 | — | 已标 | — |
| recruits | sub_B45400 | 80/84 | 6/9 | channel_id, party_id, troops |
| leaders | sub_B454D0 | 64/64 | 2/8 | 前 6 字段 |
| bracket | sub_B45580 | — | 已标 | — |
| AI | sub_B45680 | 168/168 | 27/29 | type, name |

## recruits 要点（sub_B45400）

- `member_count` 槽@10（wire@9，troops 后 1B 填充）
- `comment` 循环 `a1+12`，定长 0x3D
- `pstat`@73, `is_lock`@74, `remain_minutes`@76, `party_type`@80

## leaders 要点（sub_B454D0）

- 仅 `avatar`@36、`pstat`@60 与 wire 不同
- 前缀 channel/party/troops/name 等 wire==mem

## ms 要点

- 自 `msma_id` 起 wire 比 mem 大 4（线上紧凑、槽内 +4 对齐）
