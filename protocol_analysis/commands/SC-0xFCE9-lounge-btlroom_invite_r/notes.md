# 分析笔记 —— SC-0xFCE9-btlroom_invite_r

> 状态：`DONE`（2026-09-20，批次-16）。

## 结论要点与取证

- 字段名取自块内 trace 日志串 `result=` / `refuse_pilot_id=` / `reason=`（@`0xB889B0` 起）。
- ★ 容量校验：`0xC`=12 = 4+4+4 ✓；闭合点 `0xB8891D cmp ebx,[var_2C40]; jz loc_B8893F`（游标==末尾）。

## 与其他命令的关联

- （无同 opcode 反向命令）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。
