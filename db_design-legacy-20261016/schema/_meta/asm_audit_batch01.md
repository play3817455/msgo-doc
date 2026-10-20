# ASM 复核 · 批次 #1（10 表）

> 日期：2026-09-20  
> 工具：`ida_extract_wire_vas.py` → `apply_asm_vas.py` → `audit_asm_batch.py 1`

## 范围

| # | 表 | 读/写器 | 线长 | 成员 |
|---|---|---|---|---|
| 1 | tbl_item | sub_B434F0 | 22 | 5 |
| 2 | tbl_ms_set | sub_B41B10 | 95 | 6 |
| 3 | tbl_equip_set | sub_B41C60 | 121 | 9 |
| 4 | tbl_pilot | sub_B06360 | 159 | 24 |
| 5 | tbl_missionunit_set | sub_B41BF0 | 12 | 3 |
| 6 | tbl_roominfo | sub_B44880 | 135 | 15 |
| 7 | tbl_cinfo | sub_B45940 | 639 | 25 |
| 8 | tbl_pilot_detail | sub_B42640 | 51672 | 53 |
| 9 | tbl_pilots_list | sub_B42BB0 | 398 | 58 |
| 10 | tbl_pcard | sub_B42BB0 | 398 | 58 |

## 结论

| 检查项 | 结果 |
|---|---|
| 成员 offset 链 = length | **10/10 通过** |
| wire_sources 与成员 offset/length 一致 | **10/10 通过** |
| evidence_va 逐字段（IDA 线偏移匹配） | **见下表** |

### evidence_va 覆盖率

| composite | 有 VA | 缺 VA | 备注 |
|---|---|---|---|
| item | 5/5 | 0 | |
| ms_set | 6/6 | 0 | 写器 loop 已对齐 |
| equip_set | 9/9 | 0 | |
| pilot | 24/24 | 0 | |
| missionunit_set | 3/3 | 0 | |
| roominfo | 15/15 | 0 | sub_B44880 @ 0xB44956..9A |
| cinfo | 25/25 | 0 | feature_word 4×28B @ 0xB45B65 |
| pilot_detail | 53/53 | 0 | 尾段 @ 0xB429BA..B42B91 |
| pilots_list | 58/58 | 0 | 尾段 wire 371–397 @ 0xB43065..E3 |
| pcard | 58/58 | 0 | 同 pilots_list |

## IDA 取证要点

- **item**：`8+4+4+4+2` @ sub_B434F0（0xB4350D…0xB4354B）
- **ms_set / equip_set**：写器 loop `cmp ecx, 2Bh` 定长串；equip `121B` 全匹配
- **pilot**：写器 159B = 25 名 + avatar(18) + 31 部队名 + penalty
- **pilots_list**：读器 58 段；`0x74` 字节块 + 多组 `0x1F` NUL 串 loop 已展开
- **pilot_detail**：主读器含 `0x73`/`0x10`/`0xA0` 等数组 loop + 嵌套 sub_B42330/sub_B423F0

## 缺口补全（2026-09-20）

工具：`tools/_patch_asm_gaps.py`（IDA disasm 逐字段补 `evidence_va`）

- **roominfo**：`sub_B02DF0`×3 + `sub_B02DD0`×2 @ 0xB44956
- **cinfo**：`feature_word` 4×28B @ 0xB45B65
- **pilots_list/pcard**：尾段 7 字段 @ 0xB43065..E3（含修正 accum/rank）
- **pilot_detail**：尾段 19 字段 @ 0xB429BA..B42B91
