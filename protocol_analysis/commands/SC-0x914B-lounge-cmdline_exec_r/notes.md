# 未决问题 / 记录 —— SC-0x914B-lounge-cmdline_exec_r

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `res` 为 NUL 结尾变长串（读原语 `sub_B02BA0`，内部 `call sub_CC56B0` memcpy）⇒ 容量按**槽预算 181** 记，线长为 `串长+1`。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
