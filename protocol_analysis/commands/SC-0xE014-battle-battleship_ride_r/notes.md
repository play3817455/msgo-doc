# 未决问题 / 记录 —— SC-0xE014-battle-battleship_ride_r

- 本批（批次-14）定稿：9 个日志名与 9 个字段一一对位，容量 32 精确吻合。
- 两个实体 ID 为 **u16**；HP 组为 **u32**（与 `0xE4DB`（entity_msma_show_hp）等命令的 HP 宽度需各自以汇编判定，不得套用）。
- 关联：与 `0x4C36`（rideable_msma_get_down_r）、`0x1EC7`（battleship_get_down_r）同族搭乘命令。
