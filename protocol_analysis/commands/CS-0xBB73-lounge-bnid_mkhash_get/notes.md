# 分析笔记 —— CS-0xBB73-lounge-bnid_mkhash_get

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x0002; call <reg>`（容量 `push` @ `0xB8CCE6`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB8CDA4`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x045` @ `0xB8CDE6`（发送成功后的统计/日志钩子）。
- 容量等式：`2 == 容量 0x2 = 2`（**零负载**：无任何字段写线）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0xBC1C-lounge-bnid_mkhash_get_r`（已 DONE；相关 `SC-0xAEAA-lounge-bnid_mkhash_get_for_tournament_r`）

## 未决 / 存疑

- **零负载命令**：容量 `0x2` == 线长 2，仅写 opcode。

## 服务端实现（2026-09-30，§㊺ 杂项收尾族）

- 实现：`serverv/internal/lounge/misc.go` 的 `onBnidMkhashGet`；注册点
  `registerMiscHandlers`（← `internal/lounge/server.go` 的 `registerHandlers`）。
- 处置：**有 `_r`** 但本服算不出 `mkhash` ⇒ 拒答 `SC-0xBC1C`，`result = -10002`
  （`errcode.Wire(ErrCodeInvalidNumber)`），`mkhash` 空串。
- 理由：`mkhash` 是 **BNID 机器哈希**；BNID 是认证侧（`internal/agent` 承接的独立前置服）
  持有的账号身份，而 game 库**没有任何一列**装它（`game.pilot*` 全表找不出 BNID/机器指纹）
  ⇒ 服务端无从计算（见 docs/01 §㊺④）。
- 验收：`internal/lounge/misc_test.go` 的 `TestMiscDeniedHandlersReply/bnid_mkhash_get`
  （恰好一帧、`result = -10002`、`mkhash` 空串）、`TestMiscHandlersTolerateBadBody`
  （零负载命令多 1 字节 ⇒ 解码失败、零帧）。
- 配对：S→C `SC-0xBC1C-lounge-bnid_mkhash_get_r`。
- 留账：服务端 BNID/机器哈希的**来源整条链**（认证侧 vs game 库）未取证。
