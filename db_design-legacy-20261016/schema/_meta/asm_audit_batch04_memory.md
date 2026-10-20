# Memory Offset 人工核对 — Batch #4

**日期:** 2026-09-20  
**方法:** IDA 读/写器逐字段 walk；仅 wire≠mem 打 `memory_offset`。

## 汇总

| 表 | 读器 | 线/槽 | 打标 | 说明 |
|---|---|---:|---:|---|
| ext_subrule | sub_B456F0 | 20/20 | 0 | wire==mem；2×u16 + 8×u16 循环写 `a1+2*i` |
| xwar_ext_rule | sub_B08160 | 514/516 | 5/7 | `param`@4；4×row@8/132/260/388；claim 516 |
| extrarule_xwar_info | sub_B08160 | 514/516 | — | layout_same_as xwar_ext_rule |
| wbonus | sub_B453B0 | 4/4 | 0 | wire==mem 全长 |
| eq_bonus_modules_lot | sub_B02DD0×3 | 12/12 | 0 | wire==mem；B71220 内联 3×u32 |
| buffitem | sub_B07E70 | 6/8 | 0 | 字段 @0/4/5 wire==mem；槽步进 8（+2B tail pad） |
| buffitem_ex | sub_B07E70 | 6/8 | — | layout_same_as buffitem |
| config | sub_B077B0 | 34/40 | 9/10 | u16 后 2B 对齐 padding（已标） |
| progress | sub_B07880 | 46/48 | 6/14 | 前缀 wire==mem；尾段 u32 槽 +4B 对齐（已标） |
| bgm_desc | sub_B07E00 | 14/16 | 4/5 | u16 后 2B pad（已标） |

## xwar_ext_rule 要点（sub_B08160）

- 前缀 `rule_type` wire==mem @0
- `param` wire@2 → mem@4（+2B）
- 四行 u32 数组：wire 基址 6/130/258/386 → mem 8/132/260/388（各行 +2B 头 pad）
- 读器用 `a1[2*v2+2+2*i]` 索引写槽；`audit_memory_chain.py` 提取器漏捕（已知假阳性）

## wire==mem 表

`ext_subrule`、`wbonus`、`eq_bonus_modules_lot`、`buffitem` 字段槽位与线序一致，无需 `memory_offset`。
