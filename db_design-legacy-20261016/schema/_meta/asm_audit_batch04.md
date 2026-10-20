# ASM 复核 · 批次 #4（10 表）

> 日期：2026-09-20  
> 工具：`ida_extract_wire_vas.py 4` → `apply_asm_vas.py --vas ida_wire_vas_batch4.json` → `_patch_asm_batch4.py` → `audit_asm_batch.py 4`

## 范围

| # | 表 | 读/写器 | 线长 | 成员 | IDA 解析 total |
|---|---|---|---|---|---|
| 1 | tbl_ext_subrule | sub_B456F0 | 20 | 2 | 12 |
| 2 | tbl_xwar_ext_rule | sub_B08160 | 514 | 6 | 130 |
| 3 | tbl_extrarule_xwar_info | (= xwar_ext_rule) | 514 | 6 | — |
| 4 | tbl_wbonus | sub_B453B0 | 4 | 3 | 4 |
| 5 | tbl_eq_bonus_modules_lot | @0xB71220 | 12 | 3 | — |
| 6 | tbl_buffitem | sub_B07E70 | 6 | 3 | 6 |
| 7 | tbl_buffitem_ex | (= buffitem) | 6 | 3 | — |
| 8 | tbl_config | sub_B077B0 | 34 | 10 | 34 |
| 9 | tbl_progress | sub_B07880 | 46 | 14 | 46 |
| 10 | tbl_bgm_desc | sub_B07E00 | 14 | 5 | 14 |

## 结论

| 检查项 | 结果 |
|---|---|
| evidence_va 逐字段 | **8/8 有成员 composite · 0 缺口** |
| layout_same_as 别名 | **2/2**（extrarule_xwar_info、buffitem_ex） |
| 成员 offset 链 = length（严格 wire 链） | **5/10 通过** |
| wire_sources 与成员 offset/length 一致 | **部分表多命令线/槽偏移并存** |

### evidence_va 覆盖率

| composite | 有 VA | 缺 VA | 备注 |
|---|---|---|---|
| ext_subrule | 2/2 | 0 | 2×u16 + 8×u16 loop @ 0xB45711/738 |
| xwar_ext_rule | 6/6 | 0 | u16 + 128×u32 双循环 @ 0xB0817A/191 |
| wbonus | 3/3 | 0 | u8×2 + u16 @ sub_B453B0 |
| eq_bonus_modules_lot | 3/3 | 0 | cmp edi,3 @ 0xB71226（sub_B51930 内联） |
| buffitem | 3/3 | 0 | u32 + u8×2 @ sub_B07E70 |
| config | 10/10 | 0 | reader\|printer 双证据 + A5DA 读 VA |
| progress | 14/14 | 0 | 4×u32 链 + helper 尾 @ sub_B07880 |
| bgm_desc | 5/5 | 0 | u8 + 3×u32 + u8 @ sub_B07E00 |

## 严格 offset 链 / wire_sources 未过

| 表 | 现象 |
|---|---|
| xwar_ext_rule / extrarule_xwar_info | param 槽 4 vs 线 2；row 槽步进 0x80 vs 线 124；链 512 vs 514 |
| config / progress / bgm_desc | game_begin 与 authenticate/bgm_change 线偏移不一致（wire_sources 双路径） |

## IDA 取证要点

- **ext_subrule**：外层 v4<0xA 两轮×4 u16；CCDF xwar 子结构 20B
- **xwar_ext_rule**：4×32 u32 写槽 / 4×31 u32 打印；`v2+=32` 外循环 @ 0xB081A0
- **eq_bonus_modules_lot**：无独立读函数；A812 handler 内 `call sub_B02DD0`×3
- **config/progress/bgm_desc**：1365 game_begin 与 A5DA/DC1E 共用读器、线槽注释已标注

## 缺口补全（2026-09-20）

工具：`tools/_patch_asm_batch4.py`（xwar row1–3 + bgm is_one_shot + 2 别名 stamp）
