# 未决问题 / 记录 —— SC-0xA0BB-lounge-player_navi_unlock_r

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 结构体 `unlocked_navi` 由内联边界检查型读取器 `sub_B434B0`（`2 × u32` = 8B）读取；打印器 `sub_B49C80` 证实成员为 `navi_id`/`status`。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
