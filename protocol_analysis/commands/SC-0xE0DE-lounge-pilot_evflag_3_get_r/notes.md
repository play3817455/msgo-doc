# 未决问题 / 记录 —— SC-0xE0DE-lounge-pilot_evflag_3_get_r

- 本批（批次-14）定稿：单 u64 字段，容量 8 精确吻合。
- ★去向槽 `vt[0xA4]` **小于 0x100**（自动抽取器只扫 ≥0x100），本批人工补抓。
- 关联：与 `0xCB1B`（heroms_set_r，`grants` 定长数组）、`0xAF02`（pilot_medal_update，`hav_medal`=`u64[16]`）同为「标志位组」族。
