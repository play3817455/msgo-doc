# 未决问题 / 记录 —— SC-0x9F94-lounge-friend_history_get_xworld_r

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `sub_B43100` 内部含字面量循环（`cmp eax,19h` 25 次、`cmp eax,1Fh` 31 次）⇒ 消费量必须**整函数 + 循环展开**统计（=113），自动统计会把循环体只算 1 次而系统性低估。
- 数组 2 的 `block_widlist_cnt` 走 `sub_B02DD0` 直接读入栈变量（无预留原语伴随）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
