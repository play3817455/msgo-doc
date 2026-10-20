# Memory Offset 人工核对 — Batch #1

**日期:** 2026-09-20  
**方法:** IDA 反编译读/写器，逐字段对比 wire `offset` 与 `a1+N` 写槽；仅 diverge 字段打 `memory_offset`。

## 已完成

| 表 | 读/写器 | 线长 | 槽长 | 打标字段 | 说明 |
|---|---|---:|---:|---:|---|
| item | sub_B434F0 | 22 | 22 | 0 | wire==mem 全长 |
| ms_set | sub_B43B00 | 95 | 95 | 0 | wire==mem 全长 |
| missionunit_set | sub_B43BE0 | 12 | 12 | 0 | wire==mem 全长 |
| equip_set | sub_B41C60 (写) | 121 | 123 | 7 | slot 后 +2B 对齐；eq_weapon@12…setname@80 |
| roominfo | sub_B44880 | 135 | 141 | 13 | room_name 后 +3B；95B 短形槽至 is_lock@100 |
| pilot | sub_B06980 | 159 | 176 | 18 | byword 后 +2B；avatar 槽 22B；尾 4B 步进填充 |
| pcard / pilots_list | sub_B42BB0 | 398 | 424 | 56 | 同读器/打印器；name 后 +3B；comment 槽 116B |
| cinfo | sub_B45940 | 639 | 648 | 23 | troops 后 +3B；notice 后 +2B 对齐 |
| pilot_detail | sub_B42640 | 51672 | 56080 | 46 | deckcost 后 +2B；favms 槽 72B；尾 2B 填充 |

### roominfo 槽图（sub_B44880）

```
wire 0   mem 0   room_id
wire 4   mem 4   room_name[73]
wire 77  mem 80  room_type      (+3 pad)
wire 81  mem 84  room_stat
wire 82  mem 88  play_elapsed
wire 86  mem 92  mission_id
wire 90  mem 96  extrule_id
wire 94  mem 100 is_lock
wire 95  mem 101 is_vsclan … master_name@116
```

### pilot 前缀 wire==mem

`pilot_id`, `name`, `troops`, `level`, `mil_class`, `byword` — 至 wire@34 / mem@34。

自 `cmdr_fame` 起：`mem = wire + 2`（至 level_point 前），avatar@52（+4），clan 段 +10，尾 dword 段 +13。

### pcard 槽图要点（sub_B42BB0 / sub_B48C10）

- wire==mem：`pilot_id`, `name`
- `last_in`@32（name 后 3B pad）
- `avatar`@44（22B 槽）；`cmdr_fame`@68
- `rec_vs`…`score_support` 槽@80–188（wire 66–174，+14）
- `comment`@192（0x74=116B）；`clan_id`@308
- 尾 `capture_bonus_limit`@416；槽步进 424

### cinfo 槽图要点（sub_B45940 / sub_B4E240）

- wire==mem：`clan_id`, `troops`
- `npc_id`@8（troops 后 3B pad）；`clan_name`@16
- `notice_body`@89（433B）；`active_time_bits`@524
- `feature_word`@536（4×28B）；槽步进 648

### pilot_detail 槽图要点（sub_B42640 / sub_B48010）

- wire==mem：`exp`…`deckcost`（0–24）
- 自 `last_battle`@28：`deckcost` 后 2B 对齐
- `comment`@68（115B）；`hav_medal`@184 … `hav_modules`@1720
- `examination_state`@2232（68B）；`rokaku_*`@2304–2324
- `cshist`@2328（槽 256B / 线 192B）；`hav_rental_modules`@2592
- `favms_arr`@3620（720×72B 槽）；尾字段自@55460
- `beginner_challenge_info`@55624；槽步进 **56080**

## Batch #1 状态

**10/10 完成**（2026-09-20）
