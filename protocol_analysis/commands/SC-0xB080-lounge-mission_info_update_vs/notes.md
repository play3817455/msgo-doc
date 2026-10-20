# 未决问题 / 记录 —— SC-0xB080-lounge-mission_info_update_vs

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 三个 1 字节字段的 `u8` 判定来自派发侧三次 `movzx eax, byte ptr [eax]`（`B72AA1`/`B72AB1`/`B72AB9`）。
- 本命令是 P9 白屏修复的关键下行报文（见 `topics/07`）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
