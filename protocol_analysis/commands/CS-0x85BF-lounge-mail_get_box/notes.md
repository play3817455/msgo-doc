# 分析笔记 —— CS-0x85BF-lounge-mail_get_box

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xA; call <reg>`（容量 `push` @ `0xb9bf66`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 1 = 7 ≤ 容量 0xA = 10`（富余 3）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x5281-lounge-mail_get_box_r`（已 DONE）构成请求/应答对。
- 与 `CS-0x7D9B-lounge-mail_get_present`（领取附件）配对。

## 未决 / 存疑

- `box_type` 取值域 {0,1,2}（0=主箱 1=系统/礼物 2=运营日志）；`sub_64B510` 三分支。
