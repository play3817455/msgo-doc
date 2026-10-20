# 未决问题 / 记录 —— SC-0xB40C-battle-weapon_fire__grenade_r

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 与 `0xA9E7`（`weapon_fire__damage_field_r`）**共享前 36B 前缀**（ent_id→charge_lv 逐字段同名同序），本命令多出 `impact_wall`/`action` 两个 u8 ⇒ 容量 41 vs 39。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
