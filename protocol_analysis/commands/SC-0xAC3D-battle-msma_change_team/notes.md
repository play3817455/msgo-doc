# 未决问题 / 记录 —— SC-0xAC3D-battle-msma_change_team

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 两个 1 字节顶层字段的 `u8` 判定来自派发侧 `movzx eax, byte ptr [eax]`@`B28766`/`B2876E`。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
