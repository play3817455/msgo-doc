# 未决问题 —— SC-0x0943-battle-entity_msma_disappear

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `reason` 的消失原因枚举 | 未知（块内仅十进制打印） | 未交叉 `datatables` 原因表；`0x1EA5 entity_msma_reborn` 可能有同族枚举 | 2026-09-20 |
| Q2 | `not_use` 是否真「未使用」（原名字面） | 倾向保留字段/占位（名字即 `not_use`，块内无用途分支） | 无法从块内判定其业务含义；**按原名字面记录，不臆造** | 2026-09-20 |
| Q3 | `ent_id` 与 `SC-0x20F5 entity_msma_fix` 的 `ent_id` 是否同一命名空间 | 倾向同一（均为战场实体 ID） | 未逐字段对齐两份文档 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 同族实体生命周期命令：`SC-0x0120 entity_msma_show`(DONE)、`SC-0x130A entity_msma_hide`(DRAFT)、`SC-0x1EA5 entity_msma_reborn`(DRAFT)、`SC-0x20F5 entity_msma_fix`(DONE)。
- 虚表槽 `vt[0x15C]` 为战服实体事件入口（实参 `(ent_id, reason, not_use)`）。
- 本命令与 `0x0120`/`0x130A` 形态相似（小定长 + `vt[0xNN]` 去向），可作对照。
