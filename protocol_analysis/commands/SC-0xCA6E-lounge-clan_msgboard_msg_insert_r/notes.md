# 未决问题 / 记录 —— SC-0xCA6E-lounge-clan_msgboard_msg_insert_r

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `clan_kind` 为顶层 1 字节字段，去向侧 `movzx edx, byte ptr [ecx]`@`B7A806` ⇒ 记 `u8`。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
