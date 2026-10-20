# 分析笔记 —— CS-0x20F5-entity_msma_fix

> 状态：`DONE`（2026-09-20，批次-16）。

## 结论要点与取证

- 字段名取自 trace 日志串 `ent_id=` / `pos_x=` / `pos_y=` / `pos_z=` / `attach_parent_ent_id=` / `is_using_ss=`（@`0xB0CA33` 起）。
- ★ 该命令**不经分发器**：由 battle 分发器默认分支 `0xB31252` 调用 `sub_B0C210`(S→C) / `sub_B0C910`(C→S)，双向同 opcode `0x20F5`（见 `_meta\环境与工具约定.md` §4）。
- ★ **双侧对称交叉验证**：S→C `recv_entity_msma_fix` 的字段与 C→S 完全对称（见 `SC-0x20F5-battle-entity_msma_fix` 的 notes）。
- 容量 `0x1A`=26 ≥ 线长 11（2+10+1），符合「容量是预留上限，常有富余」。

## 与其他命令的关联

- 同 opcode 反向命令：[SC-0x20F5-battle-entity_msma_fix](SC-0x20F5-battle-entity_msma_fix)

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。
