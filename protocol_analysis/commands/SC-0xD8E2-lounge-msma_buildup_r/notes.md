# 未决问题 / 记录 —— SC-0xD8E2-lounge-msma_buildup_r

- 本批（批次-14）定稿：9 个日志名与 9 个字段一一对位，容量 32 精确吻合。
- ★容量抽取注意：`push 20h ; char`（行尾 ASCII 注释）会使机械抽取器漏读 ⇒ 本批对全部窗口改为「先去除行尾注释」再匹配。
- `uniqid_ms`（u64）去向按 cdecl 拆「低 32 位在前、高 32 位在后」⇒ 10 实参 = 9 字段 + 1。
- 关联：与 `0xDE68`（msma_weapon_buildup_complete_r）、`0x0876`（msma_weapon_buildup_r）同族。
