# 分析笔记 —— CS-0x26F2-lounge-you9_cps_SCAN_response

> 状态：`DONE`（2026-09-20，批次-17）。

## 结论要点与取证

- 字段名取自同函数**提交后** trace 块日志串；线序 == 日志序。
- 声明容量 `0x2336`；分配器指纹 @ `0xBA5516`。
- 去向槽：`vt[0x58]`（发送）@ `0xBA5753`。
- ★ 变长段：`buffer_size`(u32，上限 0x2000) + `buffer[]`（逐字节内联拷贝）。

## 与其他命令的关联

- （本批次内无同 opcode 反向命令；见 INDEX 交叉参照）

## 未决 / 存疑

- `buffer_size` 字段日志未打标签（命名为**推定**）。

## 服务端实现（2026-09-29，`其他`桶收尾 · §㊹）

- 已注册：`serverv/internal/lounge/anticheat.go` 的 `onYou9CpsSCANResponse`
  （`registerAnticheatHandlers`，经 `lounge/server.go` 的 `registerHandlers` 挂上）。
- 验收：`serverv/internal/lounge/anticheat_test.go`（`TestAnticheatScanBufferIsFixed8192` 等四组）。
- 处置口径：**解码 + 留证日志，零回包、不落库**。配对 `SC-0x30E1-lounge-you9_cps_SCAN_request`；
  本服**不出题**（§㊹①）⇒ 无可判、可拒、可落库的东西。
- ★生成码把 `buffer` 解成**定长 8192**（field 表 `array<u8,8192>`），而本表 `buffer_size` 自述
  "服务端据此解析 buffer" ⇒ "线上定长还是按 `buffer_size` 变长"**没有真机证据**：本批按定长解，
  日志把 `buffer_size` 与 `len(buffer)` **并排打出**，并只打前 16B hex（`hexBrief`）以免冲垮日志。
  单测 `TestAnticheatScanBufferIsFixed8192` 钉住这条线形契约（§㊹③④）。
