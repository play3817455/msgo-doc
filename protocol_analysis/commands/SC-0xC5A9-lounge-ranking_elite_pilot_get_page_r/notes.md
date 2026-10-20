# 未决问题 / 记录 —— SC-0xC5A9-lounge-ranking_elite_pilot_get_page_r

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `ranking` 元素线长 188 / 槽步进 200（`add var_2C48,0C8h`@`B78856`）。
- 元素成员（读取器 `sub_B46840` + 打印器 `sub_B4FE20`）：`rank`(u32)、`score`(u32)、`pilot_id`(u32)、`name`(25B)、`troops`(i8)、`world_id`(u32)、`season_class_lv`(u32)、`tm_upd`(f64)、`avatar`(18B)、`msdeck`(36B)、`msdeck2`(36B)、`last_score`(u32)、`last_rank`(u32)、`clan_name`(31B)、`emb_base`(i8)、`emb_parts1..3`(i8)；元素尾字节（偏移 0xC3）打印器未给名字，暂记 `f_c3`(`?`)。
- `ranking_num` 日志未打标签（按「上限 100 + 驱动数组」判定）；`term_str` 之后的字段偏移随串长浮动。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
