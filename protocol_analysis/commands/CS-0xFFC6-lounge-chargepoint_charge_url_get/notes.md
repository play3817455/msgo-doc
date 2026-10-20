# 分析笔记 —— CS-0xFFC6-lounge-chargepoint_charge_url_get

> 状态：`DONE`（2026-09-20，批次-23）。

## 结论要点与取证

- 分配器指纹：`mov ecx,[obj+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push <容量>; call edx`；写线游标由 `sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**（opcode 占 `buf+0..1`）。
- 字段名取证 = **提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; … call sub_41D990`），**日志名序 == 线序**。打印器宽度：`sub_B03580`=u32 / `sub_B032A0`=u16 / `sub_B08500`=u64 / `sub_B0C1F0`=单字节（`movsx`，仅打印符号扩展，不改线宽）。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`：`mov edx,[edi]; mov eax,[edx+58h]; sub <len>,<buf>; push <len>; push <buf>; mov ecx,<obj>; call eax`。
- 容量等式：`2（opcode）== 容量 0x2 = 2（零负载）`
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`；结构体/元素 1 字节成员按打印器 `movsx` 记 `i8`。
- 配对：S→C `SC-0x4DA5-lounge-chargepoint_charge_url_get_r`。
- 与 S→C `SC-0x4DA5-lounge-chargepoint_charge_url_get_r` 配对（应答返回充值 URL）。

## 未决 / 存疑 / 备注

- ★ **零负载 C→S 命令**（容量 2 == 线长 2）：判据 = ① 分配器容量恰为 **2**（opcode 宽度）；② 全函数**仅一条写线**（`mov word ptr [edi], 0FFC6h`），无任何字段写；③ 发送长度按「游标 − 缓冲首址」计算 = 2。与批次-16~22 已固化的零负载族同判据（本批新增 1 条：累计 **67 条** C→S 零负载）。
- ★ 本命令成功分支写作 `test al,al; jnz <成功>`（成功走**跳转**分支，而非顺序落下）——判「写线窗口结束」时不能假设成功后一定顺序执行（对照组：本批其余 12 条为 `jz <失败>`）。
- 附加通知 `[obj+79A8h]` 回调模块 id `0x43`。

## 与其他命令的关联

- SC-0x4DA5-lounge-chargepoint_charge_url_get_r
