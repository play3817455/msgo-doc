# 未决问题 / 记录 —— SC-0xD467-lounge-clan_search_r

- 本批（批次-14）定稿：按 SOP §5 复核，类型全部由汇编判定。
- ★元素线长（**114**）≠ 槽步进（**120** = `sub_B417A0` 的 `add dword ptr [edx],78h`）；容量按「槽步进 × 上限」记账。
- 元素读取器 = 复合读取器 `sub_B45BA0`（`0xB45BA0..0xB45D1A`，整函数扫描）；其中三段定长字节数组由 `cmp edi,1Fh`/`cmp edi,19h` 循环展开：31/31/25 字节。
- 元素成员名取自「元素打印器」`sub_B4E680`（依次打印 `clan_id=`/`emb_base=`/`emb_parts1=`/`emb_parts2=`/`clan_name=`/`level=`/`offer_body=`/`leader_name=`/`member_num=`/`member_max=`/`offer_is_active=`/`clan_kind=`/`active_time_bits=`/`play_style=`/`capture_unlock_num=`），与线序一一对位。
- 结构体步进 120 = 线长 114 + 6 字节填充（`clan_name` 后 `level` 对齐到 u32 边界）。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
