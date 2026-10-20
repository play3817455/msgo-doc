# 未决问题 / 记录 —— SC-0xAB6F-battle-msma_spawn_list_get_r_end

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 零负载判据（累计第 9 例）：① 无 `vt[0x78]` 缓冲申请；② 入口即「游标 == 报文末尾」；③ 去向无实参。
- 配对：`SC-0x9951-battle-msma_spawn_list_get_r_begin`（已 DONE）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
