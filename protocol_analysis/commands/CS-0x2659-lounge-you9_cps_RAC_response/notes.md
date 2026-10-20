# 分析笔记 —— CS-0x2659-lounge-you9_cps_RAC_response

> 状态：`DONE`（2026-09-20，批次-17）。

## 结论要点与取证

- 字段名取自同函数**提交后** trace 块日志串；线序 == 日志序。
- 声明容量 `0xA`；分配器指纹 @ `0xBA5326`。
- 去向槽：`vt[0x58]`（发送）@ `0xBA5454`。

## 与其他命令的关联

- （本批次内无同 opcode 反向命令；见 INDEX 交叉参照）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。

## 服务端实现（2026-09-29，`其他`桶收尾 · §㊹）

- 已注册：`serverv/internal/lounge/anticheat.go` 的 `onYou9CpsRACResponse`
  （`registerAnticheatHandlers`，经 `lounge/server.go` 的 `registerHandlers` 挂上）。
- 验收：`serverv/internal/lounge/anticheat_test.go`（`TestAnticheatHandlersSendNothing` 等四组）。
- 处置口径：**解码 + 留证日志，零回包、不落库**。它与 `SC-0x643D-lounge-you9_cps_RAC_request`
  是**出题 / 回话**对；本服**不出题**（出题+判分+执行三件缺一不可，而"执行"在本仓库没有承载，
  见 `docs/01-进度-S0-S9.md` §㊹①）⇒ `factor`/`cps_result` 只进日志，不比对、不判定。
- `cps_result` 取值域 {0,1}（0=通过 / 1=异常；包装 @`0xB00C1A` 在反外挂桩族内、值来自寄存器 ⇒ 仅「0/非 0」口径确证）（原「不翻译成通过/失败」的留账仍未销：取值表本身取不到）。
