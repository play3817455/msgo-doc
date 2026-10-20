# 未决问题 / 记录 —— SC-0xCDE7-lounge-msma_adop_update

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `adop_get` 线长 13 / 槽 16（`sub_B43D90`：i8 + u32 + 4×u16 = 13B）。
- 成员（打印器 `sub_B4AC50`）：`db_index`(i8)、`equip_wid`(u32)、`adop_set`(u16) + 3×u16。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
