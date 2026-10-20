# 未决问题 / 记录 —— SC-0xCE21-lounge-xwar_booking_waitbonus_notice

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 读取器 `sub_B453B0` 直接写入已预留的 4B 槽（i8 + i8 + u16）⇒ 线长 == claim == 4。
- 成员（打印器 `sub_B4D7A0`）：`lv`(i8)、`openbox`(i8)、`gp_rate`(u16)。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
