# 分析笔记 —— CS-0x55D6-lounge-clan_text_offer_set

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x5E; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 49 + 31 + 1 = 87 ≤ 容量 0x5E=94（富余 7）`

## 与其他命令的关联

- 与 S→C `SC-0x5F72-lounge-clan_text_offer_set_r` 构成请求/应答对。

## 未决 / 存疑

- ★ 类型以写线原语宽度为准：`is_active` 是 **u32**（`mov [eax],ecx`），不因语义像布尔而记 u8。
- 日志名序（`is_active=`→`subj=`→`body=`→`clan_kind=`）与线序一致。
- 与 S→C `SC-0x5F72-lounge-clan_text_offer_set_r` 构成请求/应答对。
