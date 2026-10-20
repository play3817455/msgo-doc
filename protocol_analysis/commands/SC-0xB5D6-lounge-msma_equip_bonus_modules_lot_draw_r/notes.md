# 未决问题 / 记录 —— SC-0xB5D6-lounge-msma_equip_bonus_modules_lot_draw_r

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 与已 DONE 的 `SC-0xA812`（`msma_equip_bonus_modules_lot_get_r`）为**读取/抽选**对照命令：`0xA812` 用一次 `sub_B41460`+单次 u32 读记 12B 结构体，本命令为 `sub_B41460` 后**循环 3 次 u32**，线长同为 12 ⇒ 同一内存布局的两种读法。
- `u64` 去向按 cdecl 拆低/高 32 位（不影响线长）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
