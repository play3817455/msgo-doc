# 未决问题 / 记录 —— SC-0xDBDB-lounge-btlroom_coop_roomlist_get_r

- 本批（批次-14）定稿：容量 `0xA8C4 = 4 + 300×144` 精确吻合（上限 300 由 `cmp ebx,12Ch` 确证）。
- ★元素线长 **135**（复合读取器 `sub_B44880` 整函数扫描：u32 + 73×u8 + u32 + u8 + 3×u32 + 2×u8 + 3×u16 + 2×u32 + 25×u8）≠ 槽步进 **144**（`sub_B41650` 的 `add dword ptr [edx],90h`）。
- **未定案项**：`roomlist` 元素内部成员未逐一命名。
- 关联：与 `CS-0x0xx`（btlroom_coop_roomlist_get 请求）成对；与 `0x1D02`（channellobby_members_get_r）同为「大上限列表」族。
