# 分析笔记 —— CS-0xE4B8-lounge-you9_cps_HDB_response

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00BA5176`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00BA526B`。
- 容量等式：`2 + 4 = 6 == 容量 0x6 = 6（精确相等）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0x2775-lounge-you9_cps_HDB_request`。

## 未决 / 存疑 / 备注

- 对端为**请求侧** `SC-0x2775-lounge-you9_cps_HDB_request`（`you9_cps_HDB_request`，非 `_r` 后缀）。
- `cps_result` 取值域 {0,1}（0=通过 / 1=异常；包装 `sub_B00BE0` 的唯一调用点 @`0xAF74A7` 在 SEH 反外挂桩内、值来自寄存器 ⇒ 仅「0/非 0」口径确证）。

## 与其他命令的关联

- SC-0x2775-lounge-you9_cps_HDB_request

## 服务端实现（2026-09-29，`其他`桶收尾 · §㊹）

- 已注册：`serverv/internal/lounge/anticheat.go` 的 `onYou9CpsHDBResponse`
  （`registerAnticheatHandlers`，经 `lounge/server.go` 的 `registerHandlers` 挂上）。
- 验收：`serverv/internal/lounge/anticheat_test.go`（`TestAnticheatHandlersSendNothing` 等四组）。
- 处置口径：**解码 + 留证日志，零回包、不落库**。配对 `SC-0x2775-lounge-you9_cps_HDB_request`
  （`hdb_size(4)｜hdbdat[N]`）。
- ★回话**只回结果码、不回任何被查内容**（与 SCAN 那条不同）⇒ 服务端若不出题，手里连"查的是哪块
  数据"都不知道，这一格只能进日志；本服**不出题**（§㊹①）。
- `cps_result` 取值域 {0,1}（0=通过 / 1=异常；包装 `sub_B00BE0` 的唯一调用点 @`0xAF74A7` 在 SEH 反外挂桩内、值来自寄存器 ⇒ 仅「0/非 0」口径确证）（原「不判定」的留账仍未销：取值表本身取不到）。
