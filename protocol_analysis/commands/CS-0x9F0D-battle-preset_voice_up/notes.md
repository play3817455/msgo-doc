# 分析笔记 —— CS-0x9F0D-battle-preset_voice_up

> 状态：`DONE`（2026-09-20，批次-20）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x00DA; call <reg>`（容量 `push` @ `0xB34976`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0xB34CA7`。
- 附加通知：`[obj+79A8h]` 回调模块 id `0x064` @ `0xB34CC2`（发送成功后的统计/日志钩子）。
- 容量等式：`2 + 4 + 2 + 4 + 4 + 1 + 1 + 181(串槽) + 1 + 1 = 201 ≤ 容量 0xDA = 218`（富余 17）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看目标/源操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），
  **不采用伪代码类型**。**顶层 1 字节字段按写线操作数宽度记 `u8`**（打印器 `sub_B0C1F0` 的 `movsx` 只表示打印时符号扩展，不改线宽）。

## 与其他命令的关联

- 配对命令：S→C `SC-0x1E0F-battle-preset_voice_down`（已 DONE）
- 相关命令：C→S `CS-0x34BE-battle-preset_voice_up_commander`（同族）

## 未决 / 存疑

- `voice_id` 对应哪张语音表未取证。
