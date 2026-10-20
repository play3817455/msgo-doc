# 未决问题 / 记录 —— SC-0xCB1B-lounge-heroms_set_r

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `grants` 为定长数组：预留 `sub_B418C0` 一次推进 0x28=40，配字面量循环上界 10（`cmp edi,0Ah`）、每元素 u32 ⇒ 线长 40 == claim 40。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
