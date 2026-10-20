# 未决问题 / 记录 —— SC-0xC779-lounge-pilot_personal_emblem_unlock_r

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `hav_emblem` 为定长数组（无线上 count）：预留 `sub_B05ED0` 一次推进 0x40=64，配字面量循环上界 8（`cmp edi,8`），每元素 u64 ⇒ 线长 64 == claim 64。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
