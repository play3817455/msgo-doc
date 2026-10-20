# 分析笔记 —— CS-0xDDD4-lounge-btlroom_ev_caravan_mission_start

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00B90876`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00B9096B`。
- 容量等式：`2 + 4 = 6 == 容量 0x6 = 6（精确相等）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。

## 未决 / 存疑 / 备注

- INDEX 中无同名 S→C 应答命令（`btlroom_ev_caravan_mission_start_r` 不存在）。

## 与其他命令的关联

- （无同名 S→C 应答命令）
