# 分析笔记 —— CS-0xF7BD-lounge-msma_weapon_buildup_estimate

> 状态：`DONE`（2026-09-20，批次-23）。

## 结论要点与取证

- 分配器指纹：`mov ecx,[obj+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push <容量>; call edx`；写线游标由 `sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**（opcode 占 `buf+0..1`）。
- 字段名取证 = **提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; … call sub_41D990`），**日志名序 == 线序**。打印器宽度：`sub_B03580`=u32 / `sub_B032A0`=u16 / `sub_B08500`=u64 / `sub_B0C1F0`=单字节（`movsx`，仅打印符号扩展，不改线宽）。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`：`mov edx,[edi]; mov eax,[edx+58h]; sub <len>,<buf>; push <len>; push <buf>; mov ecx,<obj>; call eax`。
- 容量等式：`2 + 8 + 4 + 4 + 2 + 2 = 22 ≤ 容量 0x1A = 26`（富余 4；容量口径为 `容量 ≥ 负载 + 2`）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`；结构体/元素 1 字节成员按打印器 `movsx` 记 `i8`。
- 配对：S→C `SC-0x9932-lounge-msma_weapon_buildup_estimate_r`。
- 本命令（估算）与 S→C `SC-0x9932-..._estimate_r`（估算应答）配对。

## 未决 / 存疑 / 备注

- ★ `uniqid_ms` 为 **u64**：组包块里写作**两次内联存储**（`mov [eax],esi` + `mov [eax+4],esi`，低 32 位在前）⇒ 只统计「无位移存储」的机械抽取器会把草案记成两个独立 `u32`（草案 #1/#2），定稿按 8 字节合并（第 ㉒ 坑，承批次-21/22）。
- 容量 26 > 线长 22（富余 4）——C→S 容量是预留上限，`容量 ≥ 负载 + 2` 即成立，不要求相等。
- 附加通知：发送成功后 `[obj+79A8h]` 回调（模块 id `0x113`）。

## 与其他命令的关联

- SC-0x9932-lounge-msma_weapon_buildup_estimate_r
