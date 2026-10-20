# 分析笔记 —— CS-0xFBC1-battle-weapon_fire__funnel

> 状态：`DONE`（2026-09-20，批次-23）。

## 结论要点与取证

- 分配器指纹：`mov ecx,[obj+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push <容量>; call edx`；写线游标由 `sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**（opcode 占 `buf+0..1`）。
- 字段名取证 = **提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; … call sub_41D990`），**日志名序 == 线序**。打印器宽度：`sub_B03580`=u32 / `sub_B032A0`=u16 / `sub_B08500`=u64 / `sub_B0C1F0`=单字节（`movsx`，仅打印符号扩展，不改线宽）。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`：`mov edx,[edi]; mov eax,[edx+58h]; sub <len>,<buf>; push <len>; push <buf>; mov ecx,<obj>; call eax`。
- 容量等式：`2 + 4 + 1 + 4 + 12×6 = 83 ≤ 容量 0x56 = 86`（**上限场景**：`fire_points_num ≤ 12`；富余 3）
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`；结构体/元素 1 字节成员按打印器 `movsx` 记 `i8`。
- 配对：S→C `SC-0xA78D-battle-weapon_fire__funnel_r`。
- 与 S→C `SC-0xA78D-battle-weapon_fire__funnel_r` 配对（同类 `weapon_fire__*` 命令族）。

## 未决 / 存疑 / 备注

- ★ 变长数组：`fire_points_num`(u32) 后跟 N×6B 元素；**计数字段本身无独立日志名**（`fire_points={` 直接进数组）⇒ 命名为**推定**（`fire_points_num`），类型/上限/长度均已确证。
- 元素 `{x,y,z}` 3×u16 由三处独立证据闭合：写原语 `sub_B06580`（3 次 `mov [dst],si`，各 +2）、循环步进 `+6`、元素打印器 `sub_B0A5D0`（`x=`/`y=`/`z=` 全 `movzx word`）。
- `wslot_idx` 为 1 字节（`mov [edx],cl`）⇒ 顶层记 **u8**；打印器 `sub_B0C1F0` 的 `movsx` 不改线宽（承批次-19/20）。
- 容量 86 为**上限场景**（数组取满 12 元素时线长 83），故 `容量 > 线长` 属正常。
- 附加通知 `[obj+79A8h]` 回调模块 id `0x93`。

## 与其他命令的关联

- SC-0xA78D-battle-weapon_fire__funnel_r
