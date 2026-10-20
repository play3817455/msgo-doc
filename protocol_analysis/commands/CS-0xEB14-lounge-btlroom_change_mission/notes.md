# 分析笔记 —— CS-0xEB14-lounge-btlroom_change_mission

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00B90616`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00B907BD`。
- 容量等式：`2 + 73(room_name 槽预算) + 4 + 1 = 80 ≤ 容量 0x56 = 86（富余 6）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0xB317-lounge-btlroom_change_mission_r`。

## 未决 / 存疑 / 备注

- 写线窗口内共 3 个字段；打印块按 **日志名序 == 线序** 对位为 `room_name=`（字节串打印）/`mission_id=`（u32 打印）/`is_lock=`（`movsx` 字节打印）。
- `room_name` 线上为变长 NUL 串，其后的 `mission_id` 偏移浮动（记 `var`，不编造偏移）。

## 与其他命令的关联

- SC-0xB317-lounge-btlroom_change_mission_r
