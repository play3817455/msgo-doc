# 未决问题 / 记录 —— SC-0xB985-lounge-ranking_pilot_get_r

- 本批（批次-12）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `order`/`rankself` 内部成员未逐一命名（打印器 `sub_B4F620`(order)、`sub_B4F710`(rankself) 可后续拆分）；`ranking`/`toppilots` 元素成员用 `sub_B4F890` 拆分。
- `term_str` 位于两数组之后，偏移浮动，偏移列记 `var`。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
