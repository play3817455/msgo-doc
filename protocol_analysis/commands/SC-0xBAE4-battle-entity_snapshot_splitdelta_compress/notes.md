# 未决问题 / 记录 —— SC-0xBAE4-battle-entity_snapshot_splitdelta_compress

- 本批（批次-13）定稿：按 SOP §4/§5 复核，类型全部由汇编判定。
- 3 个定长 u32 的字段名取自块内日志串 `frame_count=` / `remain_msec=` / `zbuff={`；第 3 个（数组长度）日志未打印标签，其名 `zbuff_num` 由「上限 0x7500 + 驱动数组循环」判定（含义确证、命名为推定）。
- 去向 4 个实参中有 2 个来源于内存结构（`mov ecx,[..]; mov eax,[ecx]`），非全部线上字段直传。
- 关联：见 `README.md` §3 帧格式表与 `asm.md`。
