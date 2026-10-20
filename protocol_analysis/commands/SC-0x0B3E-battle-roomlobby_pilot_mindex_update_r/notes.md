# 未决问题 —— SC-0x0B3E-battle-roomlobby_pilot_mindex_update_r

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `result` 的结果码枚举 | 未知（块内仅十进制打印） | 未交叉结果码表 | 2026-09-20 |
| Q2 | `is_commander` 是否仅 0/1 | 倾向布尔（单字节打印器 `sub_B0C1F0`，与 `0x07E8 is_recruiting` 同款） | 块内无分支依赖 | 2026-09-20 |
| Q3 | `member_index` 的取值范围 | 未知（`?`；可能是 0..5 或 0..N） | 未交叉房间槽位上限 | 2026-09-20 |
| Q4 | 与 C→S `0x9B19 roomlobby_pilot_mindex_update`（容量 `0x6`=6）的字段对应 | 请求容量 6 ⇒ 可能只带 `pilot_id`+`member_index`（4+1=5 ≤ 6-2） | C→S 侧本轮未分析 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 配对请求：`../CS-0x9B19-battle-roomlobby_pilot_mindex_update/`（`sub_B31E20`，容量 `0x6`）。
- 同族字段命名先例：`world_id`/`pilot_id` 亦见 `SC-0x0BCE score_update_coopwave`（本批）；`is_commander` 见 `SC-0x0C5F commander_candidacy_start`(DRAFT)。
