# 未决问题 / 记录 —— SC-0xC664-lounge-ranking_elite_pilot_get_page_light_r

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 元素线长 73 / 槽步进 76（`add var_2C48,4Ch`@`B78CEB`）。
- 元素成员（读取器 `sub_B469F0` + 打印器 `sub_B501C0`）：`score`(u32)、`pilot_id`(u32)、`name`(25B)、`troops`(i8)、`world_id`(u32)、`season_class_lv`(u32)、`clan_name`(31B)。
- 容量等式与批次-11 的 `0x9F9B`（`4+10+4+200×76`）完全一致 ⇒ 同族命令互相印证。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
