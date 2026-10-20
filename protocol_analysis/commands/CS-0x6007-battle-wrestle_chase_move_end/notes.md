# 分析笔记 —— CS-0x6007-battle-wrestle_chase_move_end

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xA; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 2 = 8 ≤ 容量 0xA=10（富余 2）`

## 与其他命令的关联

- 与 S→C `SC-0xED22-battle-wrestle_chase_move_end_r` 构成请求/应答对（同族还有 `0x049D` 起始侧）。

## 未决 / 存疑

- 日志名序（`frame_count=`→`AI_ent_id=`）与线序一致。
- 打印器：`frame_count`→`sub_B03580`(u32)、`AI_ent_id`→`sub_B032A0`(u16)，与线宽互相印证。
- 与 S→C `SC-0xED22-battle-wrestle_chase_move_end_r` 构成请求/应答对（同族还有 `0x049D` 起始侧）。
