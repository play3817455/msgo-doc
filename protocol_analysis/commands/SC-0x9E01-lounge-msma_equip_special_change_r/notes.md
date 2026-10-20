# 未决问题 / 记录 —— SC-0x9E01-lounge-msma_equip_special_change_r

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `uniqid_ms` 为 u64（读原语 `sub_B06200` 游标步进 8），下传时按 cdecl 拆成两个 32 位实参（去向实参数 4 = 2 + 2）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
