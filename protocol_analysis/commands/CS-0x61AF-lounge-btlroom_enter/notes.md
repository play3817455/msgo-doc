# 分析笔记 —— CS-0x61AF-lounge-btlroom_enter

> 状态：`DONE`（2026-09-20，批次-18）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0x32; call <reg>`。
- 字段名取自**提交后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)`。
- 容量等式：`2 + 4 + 4 + 25 + 1 + 1 + 4 = 41 ≤ 容量 0x32=50（富余 9）`

## 与其他命令的关联

- ★ 与 `CS-0x6DF1-lounge-btlroom_create` 共享 `matching_type`/`room_pw`(25 槽) 两字段（同族互证）。
- 与 S→C `SC-0x5383-lounge-btlroom_enter_r` 构成请求/应答对。

## 未决 / 存疑

- 日志名序（`matching_type=`→`room_id=`→`room_pw=`→`is_audience=`→`audience_teamside=`→`extrule_id=`）与线序一致。
- 1 字节字段打印器 `sub_B0C1F0`；宽度由写线原语 `sub_B061C0`(u8) 确证。
- ★ 与 `CS-0x6DF1-lounge-btlroom_create` 共享 `matching_type`/`room_pw`(25 槽) 两字段（同族互证）。
- 与 S→C `SC-0x5383-lounge-btlroom_enter_r` 构成请求/应答对。
