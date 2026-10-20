# ASM 复核 · 批次 #6（10 表）

> 日期：2026-09-20  
> 工具：`ida_extract_wire_vas.py 6` → `apply_asm_vas.py --vas ida_wire_vas_batch6.json` → `_patch_asm_batch6.py` → `audit_asm_batch.py 6`

## 范围

| # | 表 | 读/写器 | 线长 | 成员 | IDA 解析 total |
|---|---|---|---|---|---|
| 1 | tbl_beginner_challenge_info | sub_B42440 | 454 | 4 | 392 |
| 2 | tbl_adop_get | (= adop_list) | 13 | 3 | — |
| 3 | tbl_clan_eff | sub_B45F30 | 12 | 6 | 11 |
| 4 | tbl_clan_zeon | (= clan_eff) | 12 | 6 | — |
| 5 | tbl_dailycup_conf | sub_B46E80 | 73 | 14 | 73 |
| 6 | tbl_dailycup_conf_next | (= dailycup_conf) | 73 | 14 | — |
| 7 | tbl_dc_point | sub_B47120 | 41 | 7 | 41 |
| 8 | tbl_dcpoint_detail | (= dc_point) | 41 | 7 | — |
| 9 | tbl_exam_state | (= examination_state) | 68 | 8 | 108 |
| 10 | tbl_friend_histories | (= lpcard) | 113 | 20 | — |

## 结论

| 检查项 | 结果 |
|---|---|
| evidence_va 逐字段 | **5/5 有成员 composite · 0 缺口** |
| layout_same_as 别名 | **6/6** |
| 成员 offset 链 = length（严格 wire 链） | **8/10 通过** |
| wire_sources 与成员 offset 一致 | **8/10 通过** |

### evidence_va 覆盖率

| composite | 有 VA | 缺 VA | 备注 |
|---|---|---|---|
| beginner_challenge_info | 4/4 | 0 | 32×u16 archived loop @ 0xB42482；96×u32 @ 0xB424AC |
| clan_eff | 6/6 | 0 | 11B 线 + sub_B06230 尾；reserved 槽 @ 0xB45F93 |
| dailycup_conf | 14/14 | 0 | 73B 全链 @ sub_B46E80 |
| dc_point | 7/7 | 0 | 41B 线；bef/aft_next 嵌 sub_B46CD0（内存槽） |
| examination_state | 8/8 | 0 | 6×u32 + 5×sub_B434B0 + interval @ 0xB423D9 |
| adop_get | — | — | layout_same_as adop_list（batch #2） |
| clan_zeon | — | — | layout_same_as clan_eff |
| dailycup_conf_next | — | — | layout_same_as dailycup_conf |
| dcpoint_detail | — | — | layout_same_as dc_point |
| exam_state | — | — | layout_same_as examination_state |
| friend_histories | — | — | layout_same_as lpcard（batch #2） |

## 严格 offset 链 / wire_sources 未过

| 表 | 现象 |
|---|---|
| dc_point / dcpoint_detail | bef_next/aft_next 内存槽 @+0xC/+0x18 与 41B 线 reward 区重叠；链按线紧凑 41B 审计 |

## IDA 取证要点

- **beginner_challenge_info**：cmp v3, 0x20 archived loop；cmp v5, 0x60 value loop；IDA 未展开至 454B
- **clan_eff**：sub_B06230(a1+10) 读末字节；槽 12B 含 reserved[11]
- **dailycup_conf**：sub_B02DD0 / sub_B02DF0 helper 链，mission 4×u32 双 loop
- **dc_point**：线 41B 仅 is_dc..reward_item_nums；next 预览 sub_B46CD0 仅内存
- **examination_state**：063E 路径补 offset/length；interval_cnt @ 0xB423D9

## 缺口补全（2026-09-20）

工具：`tools/_patch_asm_batch6.py`（4 字段 VA + 16 条 063E offset + 6 别名 stamp）
