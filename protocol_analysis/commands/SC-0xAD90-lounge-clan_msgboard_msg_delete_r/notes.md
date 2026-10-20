# 未决问题 / 记录 —— SC-0xAD90-lounge-clan_msgboard_msg_delete_r

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `clan_kind` 的 `u8` 判定来自派发侧 `movzx ecx, byte ptr [ecx]`@`B722C1`；日志用 `log1`(十六进制)。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
