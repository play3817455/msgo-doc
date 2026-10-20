# 分析笔记 —— CS-0x6C57-lounge-get_special_a_info

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x2; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 == 线长 2 == 容量 0x2（精确相等，零负载）`

## 与其他命令的关联

- 与 S→C `SC-0x8D4F-lounge-get_special_a_info_r` 构成请求/应答对。

## 未决 / 存疑

- ★ **零负载 C→S**：容量 2 == 线长 2，全块仅一条 opcode 写入（`mov word ptr [edi],6C57h`@0xBA5F29）。
- 判据同批次-16/17。
- 与 S→C `SC-0x8D4F-lounge-get_special_a_info_r` 构成请求/应答对。
