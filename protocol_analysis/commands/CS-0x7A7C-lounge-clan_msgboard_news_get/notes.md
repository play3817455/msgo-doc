# 分析笔记 —— CS-0x7A7C-lounge-clan_msgboard_news_get

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x6; call <reg>`（容量 `push` @ `0xba1c76`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 1 = 3 ≤ 容量 0x6 = 6`（富余 3）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x1FC7-lounge-clan_msgboard_news_get_r`（已 DONE，容量 `0xE91 = 4+4+15×248+1`）构成请求/应答对。
- 与 `CS-0x55D6-lounge-clan_text_offer_set`、`CS-0x45E3-lounge-clan_msgboard_msg_insert`（已 DONE）同族。

## 未决 / 存疑

- 线上宽度 **1 字节**；`clan_kind` 取值域 {0,1}（0=部隊 1=大会チーム）；容量富余 3。
