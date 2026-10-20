# 分析笔记 —— CS-0xFC4B-lounge-xwar_booking_info_get

> 状态：`DONE`（2026-09-20，批次-23）。

## 结论要点与取证

- 分配器指纹：`mov ecx,[obj+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push <容量>; call edx`；写线游标由 `sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**（opcode 占 `buf+0..1`）。
- 字段名取证 = **提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; … call sub_41D990`），**日志名序 == 线序**。打印器宽度：`sub_B03580`=u32 / `sub_B032A0`=u16 / `sub_B08500`=u64 / `sub_B0C1F0`=单字节（`movsx`，仅打印符号扩展，不改线宽）。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`：`mov edx,[edi]; mov eax,[edx+58h]; sub <len>,<buf>; push <len>; push <buf>; mov ecx,<obj>; call eax`。
- 容量等式：`2 + 4 = 6 == 容量 0x6 = 6`（**精确相等**）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`；结构体/元素 1 字节成员按打印器 `movsx` 记 `i8`。
- 配对：S→C `SC-0xEA2C-lounge-xwar_booking_info_get_r`。
- 与 S→C `SC-0xEA2C-lounge-xwar_booking_info_get_r` 配对。

## 未决 / 存疑 / 备注

- 容量与线长**精确相等**（`2+4=6==0x6`）。
- `matching_type` 取值域 {0}（客户端只送 0：唯一生产者 `sub_AFF0E0` 的调用点 @`0x72AADF` 为 `push 0`）。同族 `0x61AF`/`0x6DF1` 从界面取值，本命令（预约查询）没有界面选择 ⇒ 恒 0。
- 附加通知 `[obj+79A8h]` 回调模块 id `0xA5`。

## 与其他命令的关联

- SC-0xEA2C-lounge-xwar_booking_info_get_r
