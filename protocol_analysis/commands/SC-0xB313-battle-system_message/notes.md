# 未决问题 / 记录 —— SC-0xB313-battle-system_message

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `battle` 与 `lounge` 各实现一份 `system_message`（同 opcode `0xB313`），两侧线形相同但去向槽不同（`vt[0x364]` vs `vt[0x51C]`）。
- 去向槽 `vt[0x364]` 与 `0xAB93`（`online_notice`）相同，但实参个数不同（2 vs 4）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
