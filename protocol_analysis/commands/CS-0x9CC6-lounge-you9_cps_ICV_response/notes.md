# 分析笔记 —— CS-0x9CC6-lounge-you9_cps_ICV_response

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x000A; call <reg>`（容量 `push` @ `0xBA4F86`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xBA50B4`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x218` @ `0xBA50CF`（发送成功后的统计/日志钩子）。
- 容量等式：`2 + 4 + 4 = 10 == 容量 0xA = 10`（精确相等）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0xF0B1-lounge-you9_cps_ICV_request`（已 DONE）
- 相关命令：C→S `CS-0x70E9-lounge-you9_cps_CLientCheck_response` / `CS-0x2659-lounge-you9_cps_RAC_response`（同为 CPS 校验应答族）

## 未决 / 存疑

- 无。

## 服务端实现（2026-09-29，`其他`桶收尾 · §㊹）

- 已注册：`serverv/internal/lounge/anticheat.go` 的 `onYou9CpsICVResponse`
  （`registerAnticheatHandlers`，经 `lounge/server.go` 的 `registerHandlers` 挂上）。
- 验收：`serverv/internal/lounge/anticheat_test.go`（`TestAnticheatHandlersSendNothing` 等四组）。
- 处置口径：**解码 + 留证日志，零回包、不落库**。配对 `SC-0xF0B1-lounge-you9_cps_ICV_request`
  （出题那条只有 `factor`）；与 `CS-0x2659` 逐格同形，差别只在出题侧。本服**不出题**（§㊹①）
  ⇒ `factor`/`cps_result` 只进日志，不比对、不判定。
- `cps_result` 取值域 {0,1}（0=通过 / 1=异常；包装 `sub_B00BB0` 的唯一调用点 @`0xAF745A` 在 SEH 反外挂桩内、值来自寄存器 ⇒ 仅「0/非 0」口径确证）（原「不翻译成通过/失败」的留账仍未销：取值表本身取不到）。
