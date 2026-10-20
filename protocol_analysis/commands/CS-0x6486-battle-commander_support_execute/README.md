# CS-0x6486-battle-commander_support_execute

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x6486` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle_client` |
| 命令名 | `commander_support_execute` |
| 名字符串 | `)<-_proto_battle_client::send_commander_support_execute(` @ `0xee14c4` |
| 代码位置 | sub_B3E580 @ `0xb3e580`（`0xb3e580`..`0xb3e882`） |
| opcode 写入证据 | `0xb3e5fc` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x1A`（26） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | 见 §4.3 与其他命令的关联 / INDEX 反向表 |

## 2. 结论摘要

- 结论：指挥官支援发动：支援类型 + 目标坐标(x,y,z) + 支援点索引 + 值。
- 字段数：**7**（含 opcode）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 4 + 2 + 2 + 2 + 1 + 4 = 17 ≤ 容量 0x1A=26（富余 9）`

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 分发给 battle 协议类处理块（C→S 无 case 块） | 0x6486 | `0xB3E5FC` | 确证 |
| 1 | 2 | 4 | u32 | `support_type` | 支援类型 | 来源=入参 arg_0（@0xB3E608）；内联 `mov [ecx],esi`（4 字节目标）；经 `vt[0x58]` 发送 | - | `0xB3E60C` | 确证 |
| 2 | 6 | 2 | u16 | `target_x` | 目标 X 坐标 | 来源=入参 arg_4 的低 16 位（@0xB3E619）；内联 `mov [edx],ax`；经 `vt[0x58]` 发送 | - | `0xB3E626` | 确证 |
| 3 | 8 | 2 | u16 | `target_y` | 目标 Y 坐标 | 来源=入参 arg_8（@0xB3E62A）；写线原语 `sub_B02DA0`(u16)；经 `vt[0x58]` 发送 | - | `0xB3E62F` | 确证 |
| 4 | 10 | 2 | u16 | `target_z` | 目标 Z 坐标 | 来源=入参 arg_C（@0xB3E644）；写线原语 `sub_B02DA0`(u16)；经 `vt[0x58]` 发送 | - | `0xB3E649` | 确证 |
| 5 | 12 | 1 | u8 | `spt_spot_index` | 支援点索引 | 来源=入参 arg_10（@0xB3E65E）；写线原语 `sub_B061C0`(u8)；经 `vt[0x58]` 发送 | - | `0xB3E663` | 确证 |
| 6 | 13 | 4 | u32 | `val` | 支援参数值 | 来源=入参 arg_14（@0xB3E678）；写线原语 `sub_B02D80`(u32)；经 `vt[0x58]` 发送 | - | `0xB3E67D` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲（游标自 `buf+2` 起，opcode 占 `buf+0..1`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），**日志名序 == 线序**。

### 4.2 长度闭合
- 2 + 4 + 2 + 2 + 2 + 1 + 4 = 17 ≤ 容量 0x1A=26（富余 9）

### 4.3 存疑点
- 日志名序（`support_type=`→`target_x=`→`target_y=`→`target_z=`→`spt_spot_index=`→`val=`）与线序一致。
- 打印器：`support_type`/`val`→`sub_B03580`(u32)、坐标三值→`sub_B032A0`(u16)、`spt_spot_index`→`sub_B0C1F0`(u8)——与线宽互相印证。
- 与 S→C `SC-0xDC00-battle-commander_support_execute_r` 构成请求/应答对。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §4 / notes.md）
