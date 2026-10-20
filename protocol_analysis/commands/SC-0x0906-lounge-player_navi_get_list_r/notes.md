# 未决问题 —— SC-0x0906-lounge-player_navi_get_list_r

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `status` 的枚举取值（导航解锁状态） | 未知（块内仅打印整数，无分支按值区分） | 未交叉 `datatables` 导航表 | 2026-09-20 |
| Q2 | `count = 0` 是否合法（空列表） | 倾向合法（`0xB549A9 jbe` ⇒ 跳过循环、仍交 `vt[0x57C]`(基址, 0)） | 无块内分支区分「未解锁」与「空表」 | 2026-09-20 |
| Q3 | 与 C→S `0xF0C4 player_navi_get_list`（容量 `0x2`）的对应 | 请求应为无体/单字段请求（容量 2 仅够 opcode） | C→S 侧本轮未分析 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 配对请求：`../CS-0xF0C4-lounge-player_navi_get_list/`（`sub_BA7240`，容量 `0x2`）。
- 同族：`SC-0x19B2 player_navi_exchange_r`(DRAFT)、`SC-0xA0BB player_navi_unlock_r`(DRAFT)、`CS-0x65FD player_navi_exchange`、`CS-0xFC2B player_navi_unlock`。
- **本批取证要点**：数组元素由复合读取器 `sub_B434B0` 读取（非 bounded IO 原语），必须整函数扫描 `0xB434B0..0xB434E3` 才能得到元素成员 = 2×u32、消费 8B。
