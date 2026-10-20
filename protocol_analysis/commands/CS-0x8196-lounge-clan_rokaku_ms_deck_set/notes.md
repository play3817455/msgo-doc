# 分析笔记 —— CS-0x8196-lounge-clan_rokaku_ms_deck_set

> 状态：`DONE`（2026-09-20，批次-19）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xE; call <reg>`（容量 `push` @ `0xba2d86`）。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8(u64) + 4 = 14 == 容量 0xE = 14`（精确相等）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。

## 与其他命令的关联

- 与 S→C `SC-0xC4CB-lounge-clan_rokaku_ms_deck_set_r` 构成请求/应答对。
- 与 `CS-0x9370-lounge-clan_rokaku_use_point`、`CS-0x93EC-lounge-clan_rokaku_ms_deck_check` 同属楼阁族。

## 未决 / 存疑

- `decktype` 取值域 {0,1}（编成套组，两分支绑界面按钮 1973056928/867979786）。
