# 未决问题 / 记录 —— SC-0xC9BA-lounge-quest_list_init

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 元素线长 138 / 槽步进 144（`add var_2C48,90h`@`B79DE6`）。
- 元素成员（读取器 `sub_B46B90` + 打印器 `sub_B50490`）：`quest_id`(u32)、`title`(97B)、`is_event`(i8)、`is_known`(i8)、`achieve_trigger`(u16)、`achieve_denom`(u32)、`achieve_num`(u32)、`pay_gp`(u32)、后续 5×u32、尾 1B（未逐一命名，按线序记账）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
