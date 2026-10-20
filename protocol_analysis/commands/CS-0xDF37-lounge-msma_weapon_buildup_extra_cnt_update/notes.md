# 分析笔记 —— CS-0xDF37-lounge-msma_weapon_buildup_extra_cnt_update

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00B96C76`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00B96DB2`。
- 容量等式：`2 + 8 + 2 = 12 ≤ 容量 0xE = 14（富余 2）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0x5B3F-lounge-msma_weapon_buildup_extra_cnt_update_r`。

## 未决 / 存疑 / 备注

- 无（全部字段 `确证`）。

## 与其他命令的关联

- SC-0x5B3F-lounge-msma_weapon_buildup_extra_cnt_update_r
