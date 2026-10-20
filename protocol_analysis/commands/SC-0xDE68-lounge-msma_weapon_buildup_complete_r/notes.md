# 未决问题 / 记录 —— SC-0xDE68-lounge-msma_weapon_buildup_complete_r

- 本批（批次-14）定稿：10 个日志名与 10 个字段一一对位，容量 36 精确吻合。
- 与 `SC-0xD8E2-lounge-msma_buildup_r`（机体强化）**同族不同构**：本条多 `item_id`/`param_target`，少 `mech_npcpict`? —— 实际两条均含 `mech_npcpict`，差异在 `param_target` 与字段序，见各自 `fields.csv`（SOP §6.2：同族不得互相套用）。
- `uniqid_ms`（u64）去向按 cdecl 拆「低 32 位在前、高 32 位在后」⇒ 11 实参 = 10 字段 + 1。
- 关联：`SC-0xD8E2`（机体强化）、`0x0876`（msma_weapon_buildup_r，请求侧）。
