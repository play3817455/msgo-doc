# 分析笔记 —— CS-0xFD3E-lounge-pilot_create

> 状态：`DONE`（2026-09-20，批次-23）。

## 结论要点与取证

- 分配器指纹：`mov ecx,[obj+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push <容量>; call edx`；写线游标由 `sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**（opcode 占 `buf+0..1`）。
- 字段名取证 = **提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; … call sub_41D990`），**日志名序 == 线序**。打印器宽度：`sub_B03580`=u32 / `sub_B032A0`=u16 / `sub_B08500`=u64 / `sub_B0C1F0`=单字节（`movsx`，仅打印符号扩展，不改线宽）。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`：`mov edx,[edi]; mov eax,[edx+58h]; sub <len>,<buf>; push <len>; push <buf>; mov ecx,<obj>; call eax`。
- 容量等式：`2 + 159 + 4 = 165 ≤ 容量 0xA6 = 166`（富余 1）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`；结构体/元素 1 字节成员按打印器 `movsx` 记 `i8`。
- 配对：S→C `SC-0xC43C-lounge-pilot_create_r`。
- 与 S→C `SC-0xC43C-lounge-pilot_create_r` 配对。

## 未决 / 存疑 / 备注

- ★ 结构体字段的线长**只能**由「写入器函数体逐字段累加」得出（第 ㉔ 坑，承批次-22）：`sub_B06360` 逐字段累加 = `4 + 25 + 1 + 1 + 1 + 2 + 4 + 2 + 2 + 2 + 4 + 18 + 4 + 31 + 1 + 1 + 1 + 4 + 31 + 4 + 4 + 4 + 4 + 4 = 159B`（`pilot` 成员内存跨度 0xAC = 172B ≠ 线长 159B）。
- ★ 成员定名法：**结构体打印器 `sub_B08AD0` 的 `[edi+off]` 偏移与写入器偏移逐一对位**（`pilot_id`@+0 / `name`@+4 / `troops`@+0x1D / … / `penalty`@+0xA8），两者完全吻合。
- 1 字节成员 `troops`/`level`/`mil_class`/`clan_emb_*`：写入器取 1 字节、打印器用 `movsx` ⇒ 记 **i8**（结构体成员口径，承批次-5/19）。
- 容量 166 > 线长 165（富余 1）。附加通知 `[obj+79A8h]` 回调模块 id `0xF`。

## 与其他命令的关联

- SC-0xC43C-lounge-pilot_create_r
