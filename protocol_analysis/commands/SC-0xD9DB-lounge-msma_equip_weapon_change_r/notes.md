# 未决问题 / 记录 —— SC-0xD9DB-lounge-msma_equip_weapon_change_r

- 本批（批次-14）定稿：4 个日志名与 4 个字段一一对位，容量 18 精确吻合。
- `uniqid_ms`（u64）去向按 cdecl 拆「低 32 位在前、高 32 位在后」⇒ 5 实参 = 4 字段 + 1。
- 关联：与 `0x2064`（msma_equip_weapon_exchange_r）、`0x9E01`（msma_equip_special_change_r）同族装备变更命令。
