# 未决问题 / 记录 —— SC-0x9F9B-lounge-season_rankerbattle_get_entitled_pilot_list_r

- 本批（批次-11）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- `ranking_info` 为**无 count 的定长结构体** ⇒ 单独一字段。
- `ranking` 槽步进 76 ≠ 元素线长 73（结构体跨度含填充）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
