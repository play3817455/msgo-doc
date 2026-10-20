# 分析笔记 —— CS-0x6486-battle-commander_support_execute

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x1A; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 2 + 2 + 2 + 1 + 4 = 17 ≤ 容量 0x1A=26（富余 9）`

## 与其他命令的关联

- 与 S→C `SC-0xDC00-battle-commander_support_execute_r` 构成请求/应答对。

## 未决 / 存疑

- 日志名序（`support_type=`→`target_x=`→`target_y=`→`target_z=`→`spt_spot_index=`→`val=`）与线序一致。
- 打印器：`support_type`/`val`→`sub_B03580`(u32)、坐标三值→`sub_B032A0`(u16)、`spt_spot_index`→`sub_B0C1F0`(u8)——与线宽互相印证。
- 与 S→C `SC-0xDC00-battle-commander_support_execute_r` 构成请求/应答对。
