# 分析笔记 —— CS-0xF4B9-battle-battleship_get_down

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00B3FB66`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00B3FC5C`。
- 容量等式：`2 + 1 = 3 ≤ 容量 0x6 = 6（富余 3）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0x1EC7-battle-battleship_get_down_r`。

## 未决 / 存疑 / 备注

- `reason` 取值域 {0,1}（0=正常下舰 / 1=强制下舰；`sub_785260` 的 `switch(v5)` 两 case 分别调 `sub_B01840(0)`@`0x7853CD` / `sub_B01840(1)`@`0x7853F1`）（打印器 `sub_B0C1F0` 以 `movsx` 打印，线宽由写线目标 `cl` 确证为 u8）。

## 与其他命令的关联

- SC-0x1EC7-battle-battleship_get_down_r
