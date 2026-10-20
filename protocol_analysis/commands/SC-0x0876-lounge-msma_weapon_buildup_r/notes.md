# 未决问题 —— SC-0x0876-lounge-msma_weapon_buildup_r

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `result` 的结果码枚举 | 未知（块内仅十进制打印，无分支按值区分） | 未见结果码表 | 2026-09-20 |
| Q2 | `param_target` / `up_param` 的取值域 | 未知（块内仅十六进制打印） | 需交叉 `datatables` 强化参数表，本轮未做 | 2026-09-20 |
| Q3 | 与 C→S `0x5FAB msma_weapon_buildup`（容量 `0x1A`=26）的字段对应 | 未核 | C→S 侧本轮未分析；容量 26 与应答 36 不对称，请求可能只带部分字段 | 2026-09-20 |
| Q4 | `usenum` 的语义（使用次数 vs 数量） | 倾向「使用数量」（打印为十六进制，与 `buildup_cnt` 同族） | 无块内用途分支 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 配对请求：`../CS-0x5FAB-lounge-msma_weapon_buildup/`（`sub_B96E30`，容量 `0x1A`）。
- 同族强化命令：`SC-0x00F0 msma_weapon_buildup_reset_r`(DONE)、`SC-0x5B3F msma_weapon_buildup_extra_cnt_update_r`(DRAFT)、`SC-0xDE68 msma_weapon_buildup_complete_r`(DRAFT)、`SC-0x9932 msma_weapon_buildup_estimate_r`(DRAFT)。
- u64 读取原语：`sub_B06200`（8B），配 `sub_B41A10` 预留 —— 本批首个 u64 全定长字段样例。
