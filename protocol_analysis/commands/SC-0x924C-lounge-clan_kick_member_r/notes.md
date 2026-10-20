# 未决问题 / 记录 —— SC-0x924C-lounge-clan_kick_member_r

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `clan_kind` 顶层 1B：由派发侧 `movzx` 取用 ⇒ `u8`。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
