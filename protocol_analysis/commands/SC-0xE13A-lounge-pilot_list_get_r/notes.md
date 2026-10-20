# 未决问题 / 记录 —— SC-0xE13A-lounge-pilot_list_get_r

- 本批（批次-14）定稿：★**容量逐项精确相等**（`0x501 = 4 + 424 + 424 + 5×4 + 4 + 16×24 + 1 + 5×4`），据此确认：两个 `pilots_*` 结构 claim 各 424、`bmgpack_list` 上限 16（`cmp ebx,10h`）、尾部 5 个 u32。
- 「固定 1 元数组」形态：`del_remain_sec_eff` 等 5 个字段由「`sub_B41470`(claim 4) + 循环 `cmp edi,1; jb`」构成 ⇒ 线长恒为 4。
- ★元素线长 **23**（`sub_B458A0`）≠ 槽步进 **24**（`sub_B416C0`）。
- **未定案项**：`pilots_eff`/`pilots_zeon` 结构（各 398B）内部成员未逐一命名（打印器 `sub_B48C10` 体积大，本批未展开）。
- 关联：与 `0xE7C5`（pilot_lvpt_update）、`0x986D`（pilot_delete_r）同族飞行员列表命令。
