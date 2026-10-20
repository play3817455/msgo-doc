# 未决问题 / 记录 —— SC-0xD725-battle-weapon_fire__wrestle_r

- 本批（批次-14）定稿：10 个日志名与 10 个字段一一对位，容量 21 精确吻合。
- 1 字节字段 `charge_lv`/`action`/`is_dp_damage_cut` 为**顶层**字段、均以 `sub_B06230` 无符号读入 ⇒ `u8`。
- 关联：与 `SC-0xDDF7-battle-weapon_hit_to_r`、`SC-0x0372` 等同族武器事件命令。
