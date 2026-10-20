# 分析笔记 —— CS-0x51EF-lounge-cmdline_exec

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xBA; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 181(串槽) = 183 ≤ 容量 0xBA=186（富余 3）`

## 与其他命令的关联

- 与 S→C `SC-0x914B-lounge-cmdline_exec_r` 构成请求/应答对（同族 181 字节串槽）。

## 未决 / 存疑

- 日志名序（`cmd="`）与线序一致；日志名含开引号 `cmd="`，串本身不带引号。
- 与 S→C `SC-0x914B-lounge-cmdline_exec_r` 构成请求/应答对（同族 181 字节串槽）。

## 服务端实现（2026-09-30，§㊺ 杂项收尾族）

- 实现：`serverv/internal/lounge/misc.go` 的 `onCmdlineExec`；注册点
  `registerMiscHandlers`（← `internal/lounge/server.go` 的 `registerHandlers`）。
- ★定源（§⑫ 当初的"不能盲接"）：客户端侧它只有**控制台/调试指令**这一个发送形态 ——
  `sub_472AC0`（聊天输入框分发器）开头探一次 `sub_408530(0, 1, asc_F62B6C, 1)`，
  **探失败时**整段输入框文本不分频道一律走 `sub_AFEC50`（= 本条）；`sub_624B20`
  （设置界面数值滑杆）的 `case 9` 直接调 `sub_AFEC50("/hoju")`，一条硬编码调试指令。
- 处置：**有 `_r`** 但本服**绝不执行**客户端送来的一串命令（否则等于把 RCE/后门留在协议上）
  ⇒ 解码 + 留证 + 拒答 `SC-0x914B`，`result = -10002`（`errcode.Wire(ErrCodeInvalidNumber)`，
  §㊶ 定下的"这条不接"通用可发码）。
- 验收：`internal/lounge/misc_test.go` 的 `TestMiscDeniedHandlersReply/cmdline_exec`
  （恰好一帧、`result = -10002`、`res` 空串）、`TestMiscHandlersTolerateBadBody`。
- 配对：S→C `SC-0x914B-lounge-cmdline_exec_r`（`result` + `res`）。
- 留账：`res`（执行结果文本）**恒为空串** —— 不执行就没有结果可回，回显自造文案等于
  编造客户端可见语义（见 docs/01 §㊺④）。
