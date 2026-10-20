# 分析笔记 —— CS-0x0BDD-cpf_authenticate_r

> 状态：`DONE`（2026-09-20，批次-16）。

## 结论要点与取证

- 与 S→C `0xBA73-battle-cpf_authenticate` 配对（同 opcode 0x0BDD 家族的握手应答）。
- 字段名取自 trace 日志串 `data={`（@`0xB405F8` 起）。
- 容量 `0x86`=134 == 2 + 4 + 128（data_len 取上限 128）✓ —— 「容量 = 上限场景线长」。
- lounge 版（`sub_BA4B00`）逐指令同构，仅发送挂载点不同。

## 与其他命令的关联

- （无同 opcode 反向命令）

## 未决 / 存疑

- 无（本命令字段名、类型、线长均已定案）。
