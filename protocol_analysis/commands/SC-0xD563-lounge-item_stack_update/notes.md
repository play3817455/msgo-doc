# 未决问题 / 记录 —— SC-0xD563-lounge-item_stack_update

- 本批（批次-14）定稿：两个日志名与两个字段一一对位，容量 10 精确吻合。
- `uniqid`（u64）去向按 cdecl 拆「低 32 位在前、高 32 位在后」。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
