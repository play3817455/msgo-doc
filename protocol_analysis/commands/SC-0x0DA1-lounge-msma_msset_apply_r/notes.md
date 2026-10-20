# 未决问题 —— SC-0x0DA1-lounge-msma_msset_apply_r

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `result` 的结果码枚举 | 未知（块内仅十进制打印） | 未交叉结果码表 | 2026-09-20 |
| Q2 | `deck_type` 的枚举取值 | 未知（u16；`sub_B032A0` 十进制打印） | 未交叉 `datatables` 卡组类型表 | 2026-09-20 |
| Q3 | `slot` 是否即 `character_msdeck` 的槽位（≤5） | 推测（命令名 `msma_msset_apply` + 卡组语义） | 未分析 C→S `0x7306` | 2026-09-20 |
| Q4 | `vt[0x308]` 的业务定名 | 未知（槽号 `0x308` 已确证） | 未交叉 UI 侧实现 | 2026-09-20 |
| Q5 | 与 C→S `0x7306 msma_msset_apply`（容量 `0xA`）的字段对应 | 未知（该条仍 DRAFT） | C→S 侧本轮未分析 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 配对请求：`../CS-0x7306-lounge-msma_msset_apply/`（`0x7306`，声明容量 `0xA`；容量 10 ≥ 8+2，与「请求 ≤ 应答」的常见形态一致）。
- 同族（`result` + 业务 ID → `vt[0xNN]`）：`../SC-0x0C41-lounge-exchange_play_bonus_r/`（`vt[0x3BC]`）、`../SC-0x0A7A-lounge-storage_msma_extend_r/`（DONE，`vt[0x4B4]`）。
- 槽号对照（本批）：本命令 `vt[0x308]`。

## 取证来源

- 全部汇编证据取自 IDB `unpacked\GundamOnline_CHINA_v15.exe.i64`，块 `0xB55234..0xB5546D`（批次-4 落盘 `_b4_dump.txt`），无需要走 `unpacked\shell` dump 的情形。
