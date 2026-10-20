# 分析笔记 —— CS-0xF705-lounge-pilot_select

> 状态：`DONE`（2026-09-20，批次-22）。

## 结论要点与取证

- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（@ `0x00B8A8F3`）。
- 字段名取自**提交（`sub_B02FF0`）之后** trace 打印块日志串；**线序 == 日志名序**。
- 发送去向：`vt[0x58](buf, 负载长度)` @ `0x00B8AAFB`。
- 容量等式：`2 + 4 + 4 + 1 + 4 + 4 = 19 ≤ 容量 0x16 = 22（富余 3）`。
- 类型判定：一律取**写线指令宽度**（内联 `mov [reg],src` 看操作数宽度；`sub_B02D80/B02DA0/B061C0/B06190/B061E0/B02B40`），**不采用伪代码类型**；顶层 1 字节字段按写线操作数宽度记 `u8`。
- 配对：S→C `SC-0x063E-lounge-pilot_select_r`。

## 未决 / 存疑 / 备注

- `dbg_comeback_disable` 语义像布尔，但写线原语为 `sub_B02D80`（u32）、打印器为 `sub_B03580`（u32）⇒ 线型记 **u32**。
- `troops` 取值域 {0,1}（0=联邦 / 1=吉翁；同库口径见长期记忆「计数按阵营」节（`game.pilot.troops`，证据 `troopsWire*` + 客户端 `L01_SansenWaiting-Single_01.nut`）；写侧取选择记录 `[+14h]`@`0x42ECCD` / `[+6F108h]`@`0x43AEFB`）。
- `channeling_type` 取值域 {0,1,2,3}（启动器下标：0=`9you` / 1=`msol_3rd_xiny` / 2=`msol_3rd_bili` / 3=`msol_3rd_wegame`；全局 `dword_1104680`，两个 4 趟循环 @`0xA28EF2`..`0xA28F13` / `0xA290A3`..`0xA290C4` 按名字表匹配后写下标，另有多处 `cmp dword_1104680,3` 的 WeGame 特化分支）（写侧 `sub_AFE850` 第 5 实参 = `sub_A1E880()`@`0x42ECC2`/`0x43AEE0`）。

## 与其他命令的关联

- SC-0x063E-lounge-pilot_select_r
