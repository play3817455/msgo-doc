# ASM 复核 · 批次 #7（10 表）

> 日期：2026-09-20  
> 工具：`ida_extract_wire_vas.py 7` → `apply_asm_vas.py --vas ida_wire_vas_batch7.json` → `_patch_asm_batch7.py` → `audit_asm_batch.py 7`

## 范围

| # | 表 | 读/写器 | 线长 | 成员 | IDA 解析 total |
|---|---|---|---|---|---|
| 1 | tbl_member | (= leaders) | 52 | 7 | — |
| 2 | tbl_intro_info | sub_B46140 | 547 | 4 | 4 |
| 3 | tbl_hack_check | sub_B065D0 写 | 79 | 30 | 51 |
| 4 | tbl_lvjudge_hist | sub_B44750 | 369 | 8 | 277 |
| 5 | tbl_mprogress | (= progress) | 46 | 14 | — |
| 6 | tbl_netcafe_challenge_info | (= challenge_info) | 13 | 4 | — |
| 7 | tbl_unlocked_navi | sub_B434B0 | 8 | 2 | 8 |
| 8 | tbl_pointdmg | sub_B45760 | 12 | 1 | 12 |
| 9 | tbl_total_result_wave | sub_B45580 | 19 | 7 | 20 |
| 10 | tbl_recruit | sub_B45400 | 74 | 7 | 20 |

## 结论

| 检查项 | 结果 |
|---|---|
| evidence_va 逐字段 | **7/7 有成员 composite · 0 缺口** |
| layout_same_as 别名 | **3/3** |
| 成员 offset 链 = length（严格 wire 链） | **8/10 通过** |
| wire_sources 与成员 offset 一致 | **8/10 通过** |

### evidence_va 覆盖率

| composite | 有 VA | 缺 VA | 备注 |
|---|---|---|---|
| intro_info | 4/4 | 0 | 4×28 feature loop + 433B notice @ 0xB4618A/B1 |
| hack_check | 30/30 | 0 | C→S 写线 sub_B065D0；尾 perf 链 sub_B061E0 |
| lvjudge_hist | 8/8 | 0 | 多段 loop：96B lv + 48×2 xwar + 65B term + 100B term_old |
| unlocked_navi | 2/2 | 0 | 2×u32 @ sub_B434B0 |
| pointdmg | 1/1 | 0 | cmp 3 × u32 loop @ 0xB45784 |
| total_result_wave | 7/7 | 0 | helper 链 rank/container/total @ sub_B45580 |
| recruit | 7/7 | 0 | 61B comment loop + 尾 sub_B02DF0/DD0 |
| member | — | — | layout_same_as leaders（batch #2） |
| mprogress | — | — | layout_same_as progress（batch #4） |
| netcafe_challenge_info | — | — | layout_same_as challenge_info（batch #5） |

## 严格 offset 链 / wire_sources 未过

| 表 | 现象 |
|---|---|
| member | 继承 leaders 槽 52 vs 线 34；avatar/pstat 槽步进 |
| mprogress | 继承 progress 槽 48 vs 线 46；rule_* 槽 +2B |

## IDA 取证要点

- **intro_info**：cmp v5, 0x1C 内层 ×4 行；cmp v6, 0x1B1 notice_body
- **hack_check**：写线器 sub_B065D0；尾 7×sub_B061E0(f32) + sub_B061C0(u8)
- **lvjudge_hist**：0x18×u32 lv_history；0x18×u16 xwar 双段；0x41 byte + 0x19×u32 term_old
- **recruit**：cmp v2, 0x3D comment；pstat/is_lock @ 0xB45487/9D

## 缺口补全（2026-09-20）

工具：`tools/_patch_asm_batch7.py`（10 字段缺口 + 59 读/写路径 0x 前缀 + 3 别名 stamp）
