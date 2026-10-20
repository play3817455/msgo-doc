# 分析笔记 —— CS-0x6BCD-battle-msma_AI_hate_control

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xE; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 2 + 2 + 2 = 8 ≤ 容量 0xE=14（富余 6）`

## 与其他命令的关联

- （见 INDEX 反向表交叉参照）

## 未决 / 存疑

- 日志名序（`AI_ent_id=`→`target_ent_id=`→`hate_adjust=`）与线序一致。
- 三字段打印器均为 `sub_B032A0`(u16)，与线宽互相印证。
- 与 S→C `SC-0x9C14-battle-msma_AI_update_hate` 同属 AI 仇恨族（`0x9C14` 为服务端下发侧）。
