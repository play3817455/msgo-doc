# 分析笔记 —— CS-0xE1DB-lounge-clan_kick_member

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00BA1456`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00BA1586`。
- 容量等式：`2 + 4 + 1 = 7 ≤ 容量 0xA = 10（富余 3）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0x924C-lounge-clan_kick_member_r`。

## 未决 / 存疑 / 备注

- `clan_kind` 取值域 {0,1}（0=部隊 1=大会チーム）；打印器 `sub_B0C1F0` 以 `movsx` 打印，线宽由写线目标 `cl` 确证为 u8。

## 与其他命令的关联

- SC-0x924C-lounge-clan_kick_member_r
