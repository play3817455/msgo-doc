# 未决问题 / 记录 —— SC-0xA5DA-battle-authenticate_r

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `room_name` 之后的字段偏移全浮动（串在前）⇒ 偏移列记 `var`。
- 三个结构体均为「claim（缓冲跨度）> 线长」形态 ⇒ 容量按 claim 记账、线长按读取器实算；config/progress 内部成员未逐一命名。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
