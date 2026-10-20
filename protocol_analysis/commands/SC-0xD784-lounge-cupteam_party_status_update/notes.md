# 未决问题 / 记录 —— SC-0xD784-lounge-cupteam_party_status_update

- 本批（批次-14）定稿：容量 `0x4C = 4+4+16+52` 精确吻合；两个结构体 claim（16/52）≠ 线长（13/46）。
- ★容量抽取注意：该块分配器写的是 `push 4Ch ; char`（IDA 行尾补了 ASCII 注释），机械抽取器会漏 ⇒ 本批改为「去除行尾注释后再匹配」。
- **未定案项**：`phase`（`sub_B46D20`，13B）与 `bracket`（`sub_B46D80`，46B）内部成员未逐一命名。
- 关联：与 `0xB553`（dailycup_get_bracket_r）、`0xDDCD`（dailycup_round_start_interval）同族。
