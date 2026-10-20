# 分析笔记 —— CS-0x33CC-lounge-msma_missionunit_store

> 状态：`DONE`（2026-09-20，批次-17）。

## 结论要点与取证

- 字段名取自同函数**提交后** trace 块日志串；线序 == 日志序。
- 声明容量 `0xE`；分配器指纹 @ `0xB99896`。
- 去向槽：`vt[0x58]`（发送）@ `0xB999A5`。
- `missionunit_set` 由复合写入器 `sub_B41BF0` 写线（12B = u16+u16+2×u32）。

## 与其他命令的关联

- （本批次内无同 opcode 反向命令；见 INDEX 交叉参照）

## 未决 / 存疑

- `missionunit_set` 结构体各成员语义名未从打印器（`sub_B4A970`）逐一取证。
