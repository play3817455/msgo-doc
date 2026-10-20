# 未决问题 / 记录 —— SC-0xCADA-lounge-msma_equip_bonus_modules_update_r

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `eq_bonus_modules` 读取为「预留 4B + 循环内 u32」，实测循环上界字面量 1 ⇒ 线长 4 == claim 4。
- 与 `0xB5D6`（msma_equip_bonus_modules_lot_draw_r）成对。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
