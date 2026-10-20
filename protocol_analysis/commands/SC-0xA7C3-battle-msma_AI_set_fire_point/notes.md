# 未决问题 / 记录 —— SC-0xA7C3-battle-msma_AI_set_fire_point

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 7 个坐标字段均按有符号打印（`fmt_i`）；线类型由读原语 `sub_B02DF0` 判为 `u16`（SOP §6 判定表：读侧 `movzx` ⇒ u16）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
