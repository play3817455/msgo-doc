# 未决问题 / 记录 —— SC-0xA90E-lounge-chat_all_down

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 两个 NUL 串的**槽位预算**分别 25 / 181（`push 19h`@`B714AF`、`push 0B5h`@`B714CE`）；`msg` 之后的偏移浮动，偏移列记 `var`（不编造偏移）。
- 本命令是全体频道下行（`chat_all_down`），与其他 chat_*_down 家族的线形同构。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
