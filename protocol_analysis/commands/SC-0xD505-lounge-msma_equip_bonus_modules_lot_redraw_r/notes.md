# 未决问题 / 记录 —— SC-0xD505-lounge-msma_equip_bonus_modules_lot_redraw_r

- 本批（批次-14）定稿：**定长数组（无线上 count）** —— `sub_B41460` 一次推进 `0xC`(=12) 整块，循环上界为字面量 3（`cmp edi,3; jb`@`B7CFE8`）⇒ `u32[3]`。
- 预留原语 `sub_B41470`(4)、`sub_B41A10`(8)、`sub_B41460`(0xC) 仅推游标、不是字段。
- `uniqid_ms`（u64）去向按 cdecl 拆「低 32 位在前、高 32 位在后」。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
