# 归位复核批次 · tbd

> 生命周期 TBD 成员：判定 PERSIST 还是 EVENT

待判 **62** 项。裁决写回 `schema/homing/_overrides.json`，然后 `python tools/review_homing.py --check`。

| 对象 | 字段 | 线类型 | 线视图 |
|---|---|---|---|
| `examination_info_entry` | `val_00` | `u32` | examination_info_entry |
| `examination_info_entry` | `val_04` | `u32` | examination_info_entry |
| `examination_info_entry` | `val_08` | `u32` | examination_info_entry |
| `examination_info_entry` | `val_0c` | `u32` | examination_info_entry |
| `fire_points` | `TBD` | `struct` | fire_points |
| `gimmick_progress_entry` | `access_ent_id` | `u16` | gimmick_progress_entry |
| `gimmick_progress_entry` | `gauge_now` | `u32` | gimmick_progress_entry |
| `gimmick_progress_entry` | `stat` | `i8` | gimmick_progress_entry |
| `mapgimmick_entry` | `param_1` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_2` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_3` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_4` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_5` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_6` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_7` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `param_8` | `u16` | mapgimmick_entry |
| `mapgimmick_entry` | `tail_1` | `u16` | mapgimmick_entry |
| `msdeck` | `grid_0` | `u32[10]` | msdeck |
| `msdeck` | `grid_1` | `u32[10]` | msdeck |
| `msdeck` | `grid_2` | `u32[10]` | msdeck |
| `msdeck` | `grid_3` | `u32[10]` | msdeck |
| `msdeck` | `row_0` | `u32[4]` | msdeck |
| `msdeck` | `row_1` | `u32[4]` | msdeck |
| `msdeck` | `row_2` | `u32[4]` | msdeck |
| `msdeck` | `row_3` | `u32[4]` | msdeck |
| `msdeck` | `row_4` | `u32[4]` | msdeck |
| `msdeck` | `row_5` | `u32[4]` | msdeck |
| `msdeck` | `row_6` | `u32[4]` | msdeck |
| `msdeck` | `row_7` | `u32[4]` | msdeck |
| `msdeck` | `tail_a` | `u32[4]` | msdeck |
| `msdeck` | `tail_b` | `u32[4]` | msdeck |
| `msdeck` | `tail_c` | `u8[4]` | msdeck |
| `quest_info` | `tail_1` | `u8` | quest_info |
| `rokaku_node_entry` | `val_00` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_04` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_08` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_0c` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_10` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_14` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_18` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_1c` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_20` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_24` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_28_u64` | `u64` | rokaku_node_entry |
| `rokaku_node_entry` | `val_30` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_34` | `u32` | rokaku_node_entry |
| `rokaku_node_entry` | `val_38` | `u32` | rokaku_node_entry |
| `srch_res` | `w00_u32` | `u32` | srch_res |
| `srch_res` | `w04_u8` | `u8` | srch_res |
| `srch_res` | `w05_u8` | `u8` | srch_res |
| `srch_res` | `w06_u8` | `u8` | srch_res |
| `srch_res` | `w07_char31` | `char[31]` | srch_res |
| `srch_res` | `w103_u8` | `u8` | srch_res |
| `srch_res` | `w104_u8` | `u8` | srch_res |
| `srch_res` | `w105_u32` | `u32` | srch_res |
| `srch_res` | `w109_u8` | `u8` | srch_res |
| `srch_res` | `w110_u32` | `u32` | srch_res |
| `srch_res` | `w38_u8` | `u8` | srch_res |
| `srch_res` | `w39_char31` | `char[31]` | srch_res |
| `srch_res` | `w70_char25` | `char[25]` | srch_res |
| `srch_res` | `w95_u32` | `u32` | srch_res |
| `srch_res` | `w99_u32` | `u32` | srch_res |

裁决写法：`"ignore": {"<对象>.<字段>": "<理由>"}`（不落库），或改 `catalog` 里的 disposition 后重跑。
