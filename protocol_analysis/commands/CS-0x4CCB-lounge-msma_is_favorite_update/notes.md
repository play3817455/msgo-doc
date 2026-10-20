# 分析笔记 —— CS-0x4CCB-lounge-msma_is_favorite_update

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xE; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 8 + 4 = 14 = 容量 0xE（精确相等）`

## 与其他命令的关联

- （见 INDEX 反向表交叉参照）

## 未决 / 存疑

- ★ 类型以写线原语宽度为准：`is_favorite` 是 **u32**（`mov [edx],ecx` 写 4 字节），不因语义像布尔而记 u8。
- 日志名序（`uniqid=`→`is_favorite=`）与线序一致。
