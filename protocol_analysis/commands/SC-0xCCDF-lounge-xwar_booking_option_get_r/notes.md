# 未决问题 / 记录 —— SC-0xCCDF-lounge-xwar_booking_option_get_r

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `ext_subrule` 线长 == claim == 20。
- `xwar_ext_rule` 线长 514 / 槽 516（读取器 `sub_B08160`：u16 + 4 行 ×32 个 u32）；打印器 `sub_B0BEC0` 给出成员名 `extra_rule`(u16)、`param`(u32)、4 行 ×31 个 u32（行距 0x80）。与批次-11 `0xA5DA-battle.extrarule`（514/516）同族印证。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
