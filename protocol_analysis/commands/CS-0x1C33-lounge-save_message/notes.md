# 分析笔记 —— CS-0x1C33-save_message

> 状态：`DONE`（2026-09-20，批次-16）。

## 结论要点与取证

- 字段名取自 trace 日志串 `msg=\"` / `type=` / `is_save_db=`（@`0xBA697D` 起）。
- 容量 `0x30E`=782 ≥ 2 + 770 + 4 + 1 = 777 ✓。

## 与其他命令的关联

- （无同 opcode 反向命令）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。

## 服务端实现笔记（2026-09-22）

查调用点可确认这条命令是什么：`sub_B00DB0`（唯一的写入器）只有三个调用者
（`sub_BB1000`、`sub_431570`、`sub_89B9F0`），前两个都是**用 `wnsprintfW` 拼一条内部
状态串**、再以 `type=1` / `type=7`、`is_save_db=1` 发出去（`sub_BB1000` 拼的是
`"connection%u request%u processes%u complete%u lastserver%u step%u"` 这类诊断串）。
⇒ 这是客户端的**诊断/日志上报**通道，**不是**玩家公告板：公告板是 `SC-0x5A3D` /
`CS-0x0680 activity_request`，两者名字相近但目的不同。

因此服务端**没有**把它落进 `game/srv` 的任何表（`db_design` 的 fsm 里本来也没有它的实体：
S→C 侧无对应结构，`type` 枚举与 `msg` 语义都未取证）。当前实现是「字段级解码 + 落服务端
日志」（`internal/lounge/lobby_fsm.go` 的 `onSaveMessage`），命令**没有应答**、客户端
也不等应答。`is_save_db=1` 表达的是「服务端请保存」，等日志留存口径（归属 schema、
保留多久）定下来再接 DB。
