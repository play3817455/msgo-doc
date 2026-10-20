# 分析笔记 —— CS-0x05CA-wrestle_chase_move_start

> 状态：`DONE`（2026-09-20，批次-16）。

## 结论要点与取证

- 字段名取自 trace 日志串 `frame_count=` / `dir_h=` / `wrestle_id=` / `chase_time_msec=` / `target_ent_id=` / `target_pos_x=` / `target_pos_y=` / `target_pos_z=` / `AI_ent_id=`（@`0xB40CBD` 起），9 个日志名与 9 个字段线序一一对应。
- 容量 `0x26`=38 ≥ 线长 26 ✓。

## 与其他命令的关联

- （无同 opcode 反向命令）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。
