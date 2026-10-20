# 未决问题 / 记录 —— SC-0x9105-battle-entity_msma_dead

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `is_resurrect` / `is_extend_style_change_limit` 顶层 1B 字段由派发侧 `movzx` 取用 ⇒ 记 `u8`（打印器 `sub_B0C1F0` 内的 `movsx` 仅打印）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
