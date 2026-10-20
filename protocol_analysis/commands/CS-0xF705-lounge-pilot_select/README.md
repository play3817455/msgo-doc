# CS-0xF705-lounge-pilot_select

> 状态：`DONE`（2026-09-20，批次-22）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xF705` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_select` |
| 名字符串 | `)<-_proto_lounge_client::send_pilot_select(` @ `0x00EEA3D0` |
| 代码位置 | `sub_B8A8B0` @ `0x00B8A8B0`（`0x00B8A8B0`..`0x00B8AB6A`） |
| opcode 写入证据 | `0x00B8A929` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x016`（22） |
| 容量申请证据 | `0x00B8A8F3`（分配器 `[obj+0Ch]` 的 `vt[0x78]`） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` @ `0x00B8AAFB` |
| 提交 | `sub_B02FF0` @ `0x00B8A9FE` |
| 配对命令 | S→C `SC-0x063E-lounge-pilot_select_r` |

## 2. 结论摘要

- 字段数：**6**（含 opcode 第 0 项）
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）
- 是否分帧：否（单帧命令）
- 容量等式：`2 + 4 + 4 + 1 + 4 + 4 = 19 ≤ 容量 0x16 = 22（富余 3）`

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**（写线指令操作数宽度 / 写线原语），禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | 0xF705 | `00B8A929` | 确证 |
| 1 | 0 | 4 | u32 | `troops` | 阵营 | 来源=入参 `arg_0`（`mov esi,[esp+arg_0]` @`0xB8A935`）→ 内联写 `[eax],esi`（@`0xB8A939`） | 取值域 {0,1}（0=联邦 / 1=吉翁；同库口径见长期记忆「计数按阵营」节（`game.pilot.troops`，证据 `troopsWire*` + 客户端 `L01_SansenWaiting-Single_01.nut`）；写侧取选择记录 `[+14h]`@`0x42ECCD` / `[+6F108h]`@`0x43AEFB`） | `0xB8A935`;`0xB8A939` | 确证 |
| 2 | 4 | 4 | u32 | `pilot_id` | 驾驶员 ID | 来源=入参 `arg_4`（`mov ecx,dword ptr [esp+arg_4]` @`0xB8A948`）→ 内联写 `[eax],ecx`（@`0xB8A954`） | - | `0xB8A948`;`0xB8A954` | 确证 |
| 3 | 8 | 1 | u8 | `is_tutorial_skip` | 是否跳过教程 | 来源=入参 `arg_8` → 写原语 `sub_B061C0`（u8 @`0xB8A95C`） | 0/1 | `0xB8A95C` | 确证 |
| 4 | 9 | 4 | u32 | `dbg_comeback_disable` | 调试：禁用回归标记 | 来源=入参 `arg_C` → 写原语 `sub_B02D80`（u32 @`0xB8A976`） | - | `0xB8A976` | 确证 |
| 5 | 13 | 4 | u32 | `channeling_type` | 频道类型 | 来源=入参 `arg_10` → 写原语 `sub_B02D80`（u32 @`0xB8A990`） | 取值域 {0,1,2,3}（启动器下标：0=`9you` / 1=`msol_3rd_xiny` / 2=`msol_3rd_bili` / 3=`msol_3rd_wegame`；全局 `dword_1104680`，两个 4 趟循环 @`0xA28EF2`..`0xA28F13` / `0xA290A3`..`0xA290C4` 按名字表匹配后写下标，另有多处 `cmp dword_1104680,3` 的 WeGame 特化分支） | `0xB8A990` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（容量申请 `push 0x16` @ `0x00B8A8F3`）。
- 写线游标：`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0x00B8A929`。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …`），**日志名序 == 线序**。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`（`sub <len>,<buf首址>` = 游标 − 缓冲首址）。

### 4.2 长度闭合
- `2 + 4 + 4 + 1 + 4 + 4 = 19 ≤ 容量 0x16 = 22（富余 3）`

### 4.3 存疑点
- 见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / `notes.md`）
