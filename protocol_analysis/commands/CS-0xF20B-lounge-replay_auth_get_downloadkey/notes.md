# 分析笔记 —— CS-0xF20B-lounge-replay_auth_get_downloadkey

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00BA49B6`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00BA4A74`。
- 容量等式：`2（opcode）== 容量 0x2 = 2（零负载）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0x4632-lounge-replay_auth_get_downloadkey_r`。

## 未决 / 存疑 / 备注

- **零负载命令**：仅 `mov word ptr [edi], 0F20Bh`（`0xBA49C9`）写 opcode，容量 2 == 线长 2。

## 与其他命令的关联

- SC-0x4632-lounge-replay_auth_get_downloadkey_r

## 服务端实现（2026-09-30，§㊺ 杂项收尾族）

- 实现：`serverv/internal/lounge/misc.go` 的 `onReplayAuthGetDownloadkey`；注册点
  `registerMiscHandlers`（← `internal/lounge/server.go` 的 `registerHandlers`）。
- 处置：**有 `_r`** 但本服签不出可用的钥匙 ⇒ 拒答 `SC-0x4632`，`result = -10002`
  （`errcode.Wire(ErrCodeInvalidNumber)`），`download_key`/`secret_key` 都回空串。
- 理由：这是**回放服**的下载/校验密钥；本服没有回放子系统（没有回放服地址、也没有
  密钥签发算法的任何证据）⇒ 无从签发（见 docs/01 §㊺④）。
- 验收：`internal/lounge/misc_test.go` 的
  `TestMiscDeniedHandlersReply/replay_auth_get_downloadkey`（恰好一帧、`result = -10002`、
  两把钥匙空串）、`TestMiscHandlersTolerateBadBody`（零负载命令多 1 字节 ⇒ 零帧）。
- 配对：S→C `SC-0x4632-lounge-replay_auth_get_downloadkey_r`。
- 留账：回放服密钥的**签发链**（本服接回放服时要补）未取证。
