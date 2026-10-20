# 未决问题 / 记录 —— SC-0xACB0-battle-commander_get_pilotinfo_r

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `target_member` 的 `u8` 判定来自派发侧 `movzx eax, byte ptr [eax]`@`B2852E`。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
