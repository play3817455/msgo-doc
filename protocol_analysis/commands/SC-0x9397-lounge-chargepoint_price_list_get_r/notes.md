# 未决问题 / 记录 —— SC-0x9397-lounge-chargepoint_price_list_get_r

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 3 个 `*_days` 顶层 1B 字段由派发侧 `movzx` 取用 ⇒ `u8`（打印器 `sub_B0C1F0` 仅打印）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
