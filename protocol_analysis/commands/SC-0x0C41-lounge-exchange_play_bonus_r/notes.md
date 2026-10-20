# 未决问题 —— SC-0x0C41-lounge-exchange_play_bonus_r

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `result` 的兑换结果码枚举 | 未知（块内仅十进制打印） | 未交叉结果码表 | 2026-09-20 |
| Q2 | 与 C→S `0x5FFE exchange_play_bonus`（容量 `0x6`=6）的字段对应 | 请求容量 6 ⇒ 可能只带 1 个 u32（≤ 6-2=4） | C→S 侧本轮未分析 | 2026-09-20 |
| Q3 | `reward_id` 的来源表 | 未知（可能是道具表/奖励表 ID） | 未交叉 `datatables` 奖励表 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 配对请求：`../CS-0x5FFE-lounge-exchange_play_bonus/`（`sub_B9D450`，容量 `0x6`）。
- 同族（`result` + 业务 ID → `vt[0xNN]`）：`SC-0x0A7A storage_msma_extend_r`（本批）、`SC-0x2467 shop_buy_r`(DRAFT)、`SC-0x24CF gacha_enter_r`(DRAFT)。
