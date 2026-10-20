# 未决问题 / 记录 —— SC-0xA812-lounge-msma_equip_bonus_modules_lot_get_r

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 结构体 `eq_bonus_modules_lot` 的 claim（12，来自 `sub_B41460` 的 `add [ecx],0Ch`）与读取器消费量一致。
- 打印器成对打印两个值（首值为 `sub_B02DD0` 读入的 u32），内部第三值未单独定名。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
