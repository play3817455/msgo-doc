# 分析笔记 —— CS-0x34A9-auth-proto_version_check

> 状态：`DONE`（2026-09-20，批次-17）。

## 结论要点与取证

- 字段名取自同函数**提交后** trace 块日志串；线序 == 日志序。
- 声明容量 `0xE`；分配器指纹 @ `0xB04CB3`。
- 去向槽：`vt[0x58]`（发送）@ `0xB04E35`。

## 与其他命令的关联

- `CS-0x34A9-battle-proto_version_check` / `CS-0x34A9-lounge-proto_version_check`（同 opcode 跨协议类）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。
