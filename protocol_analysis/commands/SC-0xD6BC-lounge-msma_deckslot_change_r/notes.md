# 未决问题 / 记录 —— SC-0xD6BC-lounge-msma_deckslot_change_r

- 本批（批次-14）定稿：5 个日志名与 5 个字段按线序一一对位，容量 17 精确吻合。
- `uniqid`（u64）去向按 cdecl 拆「低 32 位在前、高 32 位在后」。
- 1 字节字段 `is_costover` 为**顶层**字段、派发侧用 `movzx` ⇒ 记 `u8`（非 i8）。
- 关联：与 `0xDCF2`（roomlobby_pilot_msdeck）、`0x356F`（msma_msset_get_r）同族。
