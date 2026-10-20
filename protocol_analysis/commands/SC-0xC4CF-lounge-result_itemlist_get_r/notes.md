# 未决问题 / 记录 —— SC-0xC4CF-lounge-result_itemlist_get_r

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 元素线长 8 / 槽步进 20（`add var_2C48,14h`@`B782D6`）⇒ 槽步进 ≠ 元素线长。
- 元素成员（读取器 `sub_B45350` + 打印器 `sub_B4D6E0`）：`id_type`(i8)、`itemid`(u32)、`is_itmbox`(i8)、`amount`(u16)。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
