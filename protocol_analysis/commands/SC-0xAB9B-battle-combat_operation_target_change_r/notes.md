# 未决问题 / 记录 —— SC-0xAB9B-battle-combat_operation_target_change_r

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 去向槽 `vt[0x2F8]` 与 `0xAA33` 相同，但实参个数不同（6 vs 4）⇒ **槽号相同不代表语义相同**，须以实参个数/块归属辨析。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
