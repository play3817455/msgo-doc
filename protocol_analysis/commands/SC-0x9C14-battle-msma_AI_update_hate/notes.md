# 未决问题 / 记录 —— SC-0x9C14-battle-msma_AI_update_hate

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `ent_id_cnt` / `val_cnt` 走 `sub_B02DD0` 直接读入栈变量（无预留原语伴随）⇒ 计数列证据只记读原语地址。
- 数组 2 之后的字段偏移浮动 ⇒ 偏移列记 `var`。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
