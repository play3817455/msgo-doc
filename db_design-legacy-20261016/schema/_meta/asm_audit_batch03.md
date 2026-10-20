# ASM 复核 · 批次 #3（10 表）

> 日期：2026-09-20  
> 工具：`ida_extract_wire_vas.py 3` → `apply_asm_vas.py --vas ida_wire_vas_batch3.json` → `_patch_asm_batch3.py` → `audit_asm_batch.py 3`

## 范围

| # | 表 | 读/写器 | 线长 | 成员 | IDA 解析 total |
|---|---|---|---|---|---|
| 1 | tbl_item_list | sub_B458A0 | 23 | 7 | 23 |
| 2 | tbl_party_member_stat | sub_B432C0 | 31 | 7 | 37 |
| 3 | tbl_order | sub_B46420 | 10 | 5 | 10 |
| 4 | tbl_rankself | sub_B464A0 | 40 | 6 | 16 |
| 5 | tbl_ranking | sub_B46560 | 95 | 12 | 47 |
| 6 | tbl_toppilots | (= ranking) | 95 | 12 | — |
| 7 | tbl_ranking_info | (= order) | 10 | 5 | — |
| 8 | tbl_special_a_info | (= rankself) | 40 | 6 | — |
| 9 | tbl_special_a_next | sub_B46CD0 | 12 | 3 | 12 |
| 10 | tbl_sort_info | sub_B461E0 | 18 | 12 | 18 |

## 结论

| 检查项 | 结果 |
|---|---|
| evidence_va 逐字段（IDA 读器取证） | **7/7 有成员 composite · 0 缺口** |
| layout_same_as 别名表 | **3/3 已 stamp（成员见源 composite）** |
| 成员 offset 链 = length（严格 wire 链） | **5/10 通过** |
| wire_sources 与成员 offset/length 一致 | **10/10 通过** |

### evidence_va 覆盖率

| composite | 有 VA | 缺 VA | 备注 |
|---|---|---|---|
| item_list | 7/7 | 0 | 5×u32 + u8 + u16 @ sub_B458A0 |
| party_member_stat | 7/7 | 0 | avatar 内嵌 sub_B068B0 |
| order | 5/5 | 0 | 5×sub_B02DF0 @ sub_B46420 |
| rankself | 6/6 | 0 | 两组 7×u16 loop @ 0xB464FF/536 |
| ranking | 12/12 | 0 | name/clan_name loop；avatar call @ 0xB46668 |
| special_a_next | 3/3 | 0 | 3×u32 @ sub_B46CD0 |
| sort_info | 12/12 | 0 | 尾 style_value @ 0xB462C4 |
| special_a_info | — | — | layout_same_as rankself |
| ranking_info | — | — | layout_same_as order |
| toppilots | — | — | layout_same_as ranking |

## 严格 offset 链未过（槽内对齐 vs 线紧凑）

| 表 | 现象 |
|---|---|
| tbl_item_list | stock 槽 22 vs 线 21（末段 1B 槽填充） |
| tbl_party_member_stat | rate_vslocal/mission_id/avatar 槽偏移 |
| tbl_ranking / tbl_toppilots | clan_id/score/avatar 槽填充 |
| tbl_sort_info | time_value 槽 16 vs 线 13 |

## IDA 取证要点

- **item_list**：shop_lineup 23B 闭合；勿与 sub_B45350（9193 8B form）混用
- **rankself / special_a_info**：7×u16 双数组；cmp edx,7 @ 0xB4650D/544
- **ranking / toppilots**：0x19 name + 0x1F clan_name loop；score 后 sub_B068B0
- **sort_info**：C→S sub_B41F60 / S→C sub_B461E0；claim 24 ≠ 线 18

## 缺口补全（2026-09-20）

工具：`tools/_patch_asm_batch3.py`（12 字段 + ranking 读器 VA 修正 + 3 个别名 stamp）
