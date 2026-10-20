# 未决问题 / 记录 —— SC-0xB92F-lounge-clan_mshipbid_request_cancel_r

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `clan_kind` 的 `u8` 判定来自派发侧 `movzx eax, byte ptr [ecx]`@`B7633E`。
- 与 `0xB606`（`clan_mshipbid_response_r`）同族，仅结果码/去向槽不同。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
