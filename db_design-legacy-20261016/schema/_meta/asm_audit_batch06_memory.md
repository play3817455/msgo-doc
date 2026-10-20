# Memory Offset 人工核对 — Batch #6

**日期:** 2026-09-20  
**方法:** IDA 读/写器逐字段 walk；仅 wire≠mem 打 `memory_offset`。

## 汇总

| 表 | 读器 | 线/槽 | 打标 | 说明 |
|---|---|---:|---:|---|
| beginner_challenge_info | sub_B42440 | 454/456 | 1/4 | 仅 `value`@72（archived 后 +2B） |
| adop_get | sub_B43D90 | 13/16 | — | layout_same_as adop_list（2 标继承） |
| clan_eff | sub_B45F30 | 12/12 | 0 | @0–10 wire==mem；reserved@11 读器未消费 |
| clan_zeon | sub_B45F30 | 12/12 | — | layout_same_as clan_eff |
| dailycup_conf | sub_B46E80 | 73/80 | 0 | 全长 wire==mem；尾 +7B pad |
| dailycup_conf_next | sub_B46E80 | 73/80 | — | layout_same_as dailycup_conf |
| dc_point | sub_B47120 | 41/68 | 6/7 | i8 后 pad；仅内存 bef/aft_next；奖励数组 @36/@52 |
| dcpoint_detail | sub_B47120 | 41/68 | — | layout_same_as dc_point |
| exam_state | sub_B42330 | 68/68 | 0 | layout_same_as examination_state wire==mem |
| friend_histories | sub_B43100 | 113/132 | — | layout_same_as lpcard（18 标继承） |

## dc_point 要点（sub_B47120）

- `is_dc`@0 wire==mem
- `bef_dcpoint` wire@1 → mem@4；`aft_dcpoint` wire@5 → mem@8（i8 后 +3B pad）
- `bef_next`/`aft_next` @12/@24 仅内存（sub_B46CD0）
- `reward_item_ids` wire@9 → mem@36；`reward_item_nums` wire@25 → mem@52

## beginner_challenge_info 要点（sub_B42440）

- `begin_time`/`elapsed_days`/`archived` wire==mem @0/4/6
- `value` wire@70 → mem@72（32×u16 后 +2B 对齐至 u32 数组）
