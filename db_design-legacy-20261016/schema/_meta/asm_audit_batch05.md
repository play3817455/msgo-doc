# ASM 复核 · 批次 #5（10 表）

> 日期：2026-09-20  
> 工具：`ida_extract_wire_vas.py 5` → `apply_asm_vas.py --vas ida_wire_vas_batch5.json` → `_patch_asm_batch5.py` → `audit_asm_batch.py 5`

## 范围

| # | 表 | 读/写器 | 线长 | 成员 | IDA 解析 total |
|---|---|---|---|---|---|
| 1 | tbl_phase_info | sub_B46D20 | 13 | 4 | 13 |
| 2 | tbl_bracket_info | sub_B46D80 | 46 | 11 | 38 |
| 3 | tbl_block_detail | (= lpcard) | 113 | 20 | — |
| 4 | tbl_buildup_info | sub_B44050 | 42 | 2 | 30 |
| 5 | tbl_challenge_info | sub_B07540 | 13 | 4 | 13 |
| 6 | tbl_trchallenge_info | (= challenge_info) | 13 | 4 | — |
| 7 | tbl_check_quest | sub_B06C00 | 133 | 10 | 37 |
| 8 | tbl_wave_res | sub_B08020 | 34 | 15 | 34 |
| 9 | tbl_appear_info | sub_B07EC0 | 86 | 17 | 47 |
| 10 | tbl_avatar | sub_B068B0 | 18 | 10 | 18 |

## 结论

| 检查项 | 结果 |
|---|---|
| evidence_va 逐字段 | **8/8 有成员 composite · 0 缺口** |
| layout_same_as 别名 | **2/2**（block_detail → lpcard，trchallenge_info → challenge_info） |
| 成员 offset 链 = length（严格 wire 链） | **4/10 通过** |
| wire_sources 与成员 offset 一致 | **部分表槽/线双路径** |

### evidence_va 覆盖率

| composite | 有 VA | 缺 VA | 备注 |
|---|---|---|---|
| phase_info | 4/4 | 0 | D784 i8+3×u32 @ 0xB46D36..6D |
| bracket_info | 11/11 | 0 | 9B name loop + 3×sub_B02DD0 尾 |
| buildup_info | 2/2 | 0 | 7×u16 + 7×u32 loop @ 0xB44071/8F |
| challenge_info | 4/4 | 0 | 3×u32 + u8 @ sub_B07540 |
| check_quest | 10/10 | 0 | 0x61 title + 尾 u32×8 @ 0xB06C35..C3 |
| wave_res | 15/15 | 0 | helper 链 @ sub_B08020 |
| appear_info | 17/17 | 0 | 嵌 sub_B075A0 snapshot @ 0xB07F9C |
| avatar | 10/10 | 0 | sub_B068B0；E536 读路径已补 0x |
| block_detail | — | — | layout_same_as lpcard（batch #2 已复核） |
| trchallenge_info | — | — | layout_same_as challenge_info |

## 严格 offset 链 / wire_sources 未过

| 表 | 现象 |
|---|---|
| phase_info / bracket_info | D784 槽 padding（i8 后 +3B）；bracket 线 46 vs 槽 52 |
| buildup_info | up_param 槽 16 vs 线 14 |
| check_quest | 成就字段槽 +3B vs 线紧凑 |
| wave_res | 打印器 pipe 偏移 vs 成员槽 offset 并用 |
| appear_info | 057A 线 86 vs 槽 96；snapshot 嵌套 |

## IDA 取证要点

- **buildup_info**：cmp v2,7 / cmp v3,7 双 loop（14+28=42）
- **check_quest**：cmp i,61h 定长 title；a1[26..33] 顺序 u32
- **appear_info**：sub_B075A0 嵌入 snapshot(39B)；尾 buildup_eff_range @ 0xB0800B
- **avatar**：独立 helper sub_B068B0（18B 线）；与 sub_B06290 写路径分离

## 缺口补全（2026-09-20）

工具：`tools/_patch_asm_batch5.py`（46 字段 + 2 别名 stamp + avatar E536 读路径）
