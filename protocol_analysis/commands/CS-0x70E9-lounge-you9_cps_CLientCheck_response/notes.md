# 分析笔记 —— CS-0x70E9-lounge-you9_cps_CLientCheck_response

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xA42; call <reg>`（容量 `push` @ `0xba5816`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 97 + 97 + 4 + 97 + 769 + 769 + 769 = 2608 ≤ 容量 0xA42 = 2626`（富余 18）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 `CS-0x5F28-lounge-speedhack_check_response`（已 DONE）同属反外挂上报族；本命令为「客户端自检（CLientCheck）」应答。
- 服务端侧对应实现见 `server\docs\MEMORY.md` 与 `topics\15`（CPS/CPF 握手）。

## 未决 / 存疑

- `caller_md_base` / `caller_md_entry` 在线上是**字符串**（写线原语 `sub_B02B40`），不是整数——按写线指令判定，不得按语义直觉改成 u32。
- `cps_result` 取值域 {0,1}（0=通过 / 1=异常；反外挂侧 `sub_A1D110` 以字面量 1 调包装 `sub_B00C30`@`0xA1D182`）。
- 容量 0xA42 为「上限场景」：Σ 线长 2608 ≤ 2626（富余 18）。

## 服务端实现（2026-09-29，`其他`桶收尾 · §㊹）

- 已注册：`serverv/internal/lounge/anticheat.go` 的 `onYou9CpsCLientCheckResponse`
  （`registerAnticheatHandlers`，经 `lounge/server.go` 的 `registerHandlers` 挂上）。
- 验收：`serverv/internal/lounge/anticheat_test.go`（`TestAnticheatHandlersSendNothing` 等四组）。
- 处置口径：**解码 + 留证日志，零回包、不落库**。
- ★本目录里**没有出题侧**（README 自述"无同名 S→C 应答"）⇒ 它被什么触发**未取证**；真机对版
  要看它是否与 `CS-0x2659`/`CS-0x9CC6` 成对出现（§㊹③）。
- ★`caller_md_base`/`caller_md_entry` 生成码按**串**解，日志照抄，**不解析成整数**（沿用本文件的
  存疑点）。客户端串用 `strBrief` 的 `%q` 打出，防换行伪造日志行（§㊹④）。
