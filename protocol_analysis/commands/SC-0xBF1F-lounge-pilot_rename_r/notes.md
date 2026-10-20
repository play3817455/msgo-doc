# 未决问题 / 记录 —— SC-0xBF1F-lounge-pilot_rename_r

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 变长串之后的偏移不固定（`pilot_name` 长度可变），本表以线序 + 长度记录，偏移列留 `var`。
- 串槽预算 25（`sub_B02BA0` 第 3 实参）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
