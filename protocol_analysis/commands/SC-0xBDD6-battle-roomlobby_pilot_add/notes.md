# 未决问题 / 记录 —— SC-0xBDD6-battle-roomlobby_pilot_add

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `pilot` 结构体线长 **159**（读取器 `sub_B06980` 整函数 + 循环展开实算），容量按缓冲区槽步进 **176**（`sub_B05F00` = 0xB0/槽）计 ⇒ claim≠线长。
- `pilot` 成员（偏移取自打印器 `sub_B08AD0` 与读取序一致）：`pilot_id`(u32)、`name`(25B)、`troops`(i8)、`level`(i8)、`mil_class`(i8)、`byword`(u16)、`cmdr_fame`(u32)、`rate_vslocal`(u16)、`rate_vslocal_4ev`(u16)、`rate_vslocal_clan`(u16)、`level_point`(u32)、`avatar`(18B)、`clan_id`(u32)、`clan_name`(31B)、`clan_emb_base`(i8)、`clan_emb_parts1`(i8)…（未逐一命名的尾部按线序记账）。
- 11 个实参全部以栈槽指针下传（尾部连续 `push`）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
