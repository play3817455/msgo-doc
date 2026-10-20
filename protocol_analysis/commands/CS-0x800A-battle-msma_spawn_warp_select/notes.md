# 分析笔记 —— CS-0x800A-battle-msma_spawn_warp_select

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x12; call <reg>`（容量 `push` @ `0xb34436`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 4 + 1 + 2 = 13 ≤ 容量 0x12 = 18`（富余 5）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 `CS-0x7B52-battle-msma_spawn_warp_start`（开始/取消传送）配对。
- 与 S→C `SC-0xD1B3-battle-game_respawn_post_update`（已 DONE）同族（重生点）。

## 未决 / 存疑

- `is_btlship_ride` 线上 1 字节（`sub_B061C0`），`respawn_ent_id` 2 字节（`sub_B02DA0`）——按写线原语判定。
