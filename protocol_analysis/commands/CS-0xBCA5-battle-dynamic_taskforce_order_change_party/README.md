# CS-0xBCA5-battle-dynamic_taskforce_order_change_party

> 状态：`DONE`（2026-09-20，批次-20）
> 方向：客户端 → 服务端（send）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xBCA5` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle_client` |
| 命令名 | `dynamic_taskforce_order_change_party` |
| 名字符串 | `)<-_proto_battle_client::send_dynamic_taskforce_order_change_party(` @ `0xEE1688` |
| 代码位置 | sub_B3F780 @ `0xB3F780`（`0xB3F780`..`0xB3F968`） |
| opcode 写入证据 | `0xB3F7F4` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x000A`（10） |
| 容量申请证据 | `0xB3F7C6`（`push 0x000A`） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` @ `0xB3F8F6` |
| 附加通知 | `[obj+79A8h]` 回调，模块 id `0x0FA` @ `0xB3F911` |
| 配对命令 | 相关：S→C `SC-0x483F-battle-dynamic_taskforce_order_result`（已 DONE） |

## 2. 结论摘要

- 结论：更改动态任务部队的编成队伍。
- 字段数：**3**（含 opcode 第 0 项）
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）
- 是否分帧：否（单帧命令）
- 容量等式：`2 + 1 + 4 = 7 ≤ 容量 0xA = 10`（富余 3）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**（写线指令操作数宽度 / 写线原语），禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | 0xBCA5 | `0xB3F7F4` | 确证 |
| 1 | 2 | 1 | u8 | `order_kind` | 指令种类 | 来源=入参 `arg_0`（`mov dl,byte ptr [esp+40h+arg_0]` → 内联 `mov [ecx],dl`） | 取值域 {1..15}（战术指挥指令种类；取值点 `sub_62D010(a1,a2)` 的 `switch` 返回 15 个不同值 1..15，@`0x62D030`..`0x62D0F7`） | `0xB3F809` | 确证 |
| 2 | 3 | 4 | u32 | `order_param` | 指令参数（队伍/编成 id） | 来源=入参 `arg_4`（`mov eax,[esp+40h+arg_4]` → 内联写 u32 `mov [reg],eax`） | - | `0xB3F815` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量申请 `push 0x000A` @ `0xB3F7C6`）。
- 写线游标：`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xB3F7F4`（`mov     word ptr [ebp+0], 0BCA5h`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …`），**日志名序 == 线序**。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`（`sub <len>,<buf首址>` = 游标 − 缓冲首址）。

### 4.2 长度闭合
- `2 + 1 + 4 = 7 ≤ 容量 0xA = 10`（富余 3）

### 4.3 存疑点
- `order_kind` 打印器 `sub_B0C1F0`（`movsx`）；线宽 1 字节记 `u8`。
- `order_param` 为 **u32**（内联 `mov [reg],eax`），不得因语义像索引而改窄。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / notes.md）
