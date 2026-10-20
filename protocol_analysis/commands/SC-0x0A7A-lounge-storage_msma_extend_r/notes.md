# 未决问题 —— SC-0x0A7A-lounge-storage_msma_extend_r

> 结论变更时**不要删除**原结论，按「原结论 / 推翻依据 / 新结论 / 日期」追加。

## 待确认

| 编号 | 问题 | 当前判断 | 阻塞原因 | 日期 |
|---|---|---|---|---|
| Q1 | `result` 的扩容结果码枚举 | 未知（块内仅十进制打印） | 未交叉结果码表 | 2026-09-20 |
| Q2 | `slot_num` 是「扩容后总机位数」还是「本次新增数」 | 倾向**总数**（与 `0x2ACF msma_init_get_r_begin` 的 `slot_num` 同名同义） | 块内无加减运算；未与 `0x2ACF` 逐字段对齐 | 2026-09-20 |
| Q3 | 与 C→S `0xE591 storage_msma_extend`（容量 `0x12`=18）的字段对应 | 请求容量 18 > 应答 8 ⇒ 请求可能带票券/数量等更多字段 | C→S 侧本轮未分析 | 2026-09-20 |

## 结论变更记录

| 日期 | 原结论 | 推翻依据 | 新结论 |
|---|---|---|---|
| — | — | — | — |

## 与其他命令的关联

- 配对请求：`../CS-0xE591-lounge-storage_msma_extend/`（`sub_BA3E90`，容量 `0x12`）。
- 相关：`../SC-0xB718-lounge-storage_msma_extend_buy_ticket_r/`(DRAFT)、`../CS-0x379D-lounge-storage_msma_extend_buy_ticket/`(DRAFT)。
- `slot_num` 命名先例：`SC-0x2ACF msma_init_get_r_begin`（机体列表 `begin`，`slot_num`）。
