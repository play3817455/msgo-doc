# 未决问题 / 记录 —— SC-0xC452-lounge-result_open_item_r

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `id_type` 为顶层 1 字节字段，去向侧 `movzx ecx, byte ptr [eax]`@`B77E82` ⇒ 记 `u8`（非 i8）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
