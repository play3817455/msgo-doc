# 未决问题 / 记录 —— SC-0xD6E5-lounge-season_rankerbattle_team_info_get_r

- 本批（批次-14）定稿：容量 `0x320C = 4 + 4 + 4 + 200×64` 精确吻合（上限 200 由 `cmp ebx,0C8h` 确证）。
- ★元素线长 **55**（复合读取器 `sub_B472C0` 整函数扫描：u32 + 25×u8 + u32 + u32 + `sub_B068B0`(18)）≠ 槽步进 **64**（`sub_B41AC0`）。
- `pilots_num` 字段名按 `pilots={` 日志推断（该计数本身无独立日志串），标「命名推定」。
- 关联：与 `0x1CF0`（ranking_clan_get_r）等同族列表命令。
