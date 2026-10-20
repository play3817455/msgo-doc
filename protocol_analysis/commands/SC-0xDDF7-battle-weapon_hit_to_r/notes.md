# 未决问题 / 记录 —— SC-0xDDF7-battle-weapon_hit_to_r

- 本批（批次-14）定稿：6 个日志名与 6 个字段一一对位，容量 16 精确吻合。
- 三个坐标为 **u16**（`sub_B02DF0`），与 `0xBDC6`（f64 坐标）不同——同一语义在不同命令下宽度不同（SOP §6.2 高发错误 1），**不得互相套用**。
- 关联：与 `SC-0xD725-battle-weapon_fire__wrestle_r`、`SC-0x49C6`（weapon_hit_from）同族武器命中命令。
