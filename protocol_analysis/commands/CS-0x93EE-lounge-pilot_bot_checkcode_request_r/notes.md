# 分析笔记 —— CS-0x93EE-lounge-pilot_bot_checkcode_request_r

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x12; call <reg>`（容量 `push` @ `0xb8c656`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 13(串槽) = 15 ≤ 容量 0x12 = 18`（富余 3）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0x0D24-lounge-pilot_bot_checkcode_request`（已 DONE）构成请求/应答对。
- 与 `CS-0x5C82-auth-authenticate_you9otp_input_r`（已 DONE，串槽 17+9）同族（校验码输入）。

## 未决 / 存疑

- 容量按**串槽预算**记：`push 0Dh`=13（紧邻 `sub_B02B40`）⇒ `容量 = 2 + 13 + 3`。

## 服务端实现（2026-09-29，`其他`桶收尾 · §㊹）

- 已注册：`serverv/internal/lounge/anticheat.go` 的 `onPilotBotCheckcodeRequestR`
  （`registerAnticheatHandlers`，经 `lounge/server.go` 的 `registerHandlers` 挂上）。
- 验收：`serverv/internal/lounge/anticheat_test.go`（`TestAnticheatHandlersSendNothing` 等四组）。
- 处置口径：**解码 + 留证日志，零回包、不落库**。
- ★这一条是 **`_r`**（**服务端→客户端请求的回话**，名字里的后缀就是 "reply"）：只在服务端出过题
  之后才会到。本服**不出题**（§㊹①）⇒ 收到的必然是**客户端自发**的（真机对版第一看点）。
- ★判分与回执（`SC-0xCA2C-lounge-pilot_bot_checkcode_result`，体只有 `remain`）都属"出题"那一半
  ⇒ 整条链留账：这里既不比对 `code`，也不回 `0xCA2C`（§㊹③）。
