# 未决问题 / 记录 —— SC-0xDA04-lounge-clan_search_random_r

- 本批（批次-14）定稿：容量 `0x4B5 = 4 + 10×120 + 1` 精确吻合（上限 10 由 `cmp ebx,0Ah` 确证）。
- ★与 `SC-0xD467-lounge-clan_search_r` **同构**（同一元素读取器 `sub_B45BA0`、同一槽步进 `sub_B417A0`=120、同一元素打印器 `sub_B4E680`）：元素线长 **114**，成员 15 项（`clan_id`/`emb_base`/`emb_parts1`/`emb_parts2`/`clan_name`(bytes[31])/`level`/`offer_body`(bytes[31])/`leader_name`(bytes[25])/`member_num`/`member_max`/`offer_is_active`/`clan_kind`/`active_time_bits`/`play_style`/`capture_unlock_num`，见 `0xD467` 的 `notes.md`）。
- 差异：本条**无** `result` 字段，首字段即计数。
- 关联：`SC-0xD467-lounge-clan_search_r`、`SC-0xDA04` 与 `CS` 侧 `CS-0x0xx`（clan_search）请求成对。
