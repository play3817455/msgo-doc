# CS-0x61AF-lounge-btlroom_enter

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x61AF` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `btlroom_enter` |
| 名字符串 | `)<-_proto_lounge_client::send_btlroom_enter(` @ `0xeeade8` |
| 代码位置 | sub_B8FE80 @ `0xb8fe80`（`0xb8fe80`..`0xb90196`） |
| opcode 写入证据 | `0xb8fefc` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x32`（50） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | 见 §4.3 与其他命令的关联 / INDEX 反向表 |

## 2. 结论摘要

- 结论：进入对战房间：匹配类型 + 房间 id + 房间密码 + 是否观众 + 观众侧 + 扩展规则 id。
- 字段数：**7**（含 opcode）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 4 + 4 + 25 + 1 + 1 + 4 = 41 ≤ 容量 0x32=50（富余 9）`

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 分发给 lounge 协议类处理块（C→S 无 case 块） | 0x61AF | `0xB8FEFC` | 确证 |
| 1 | 2 | 4 | u32 | `matching_type` | 匹配类型 | 来源=入参 arg_0（@0xB8FF08）；内联 `mov [eax],esi`；经 `vt[0x58]` 发送 | - | `0xB8FF0C` | 确证 |
| 2 | 6 | 4 | u32 | `room_id` | 房间 id | 来源=入参 arg_4（@0xB8FF1B）；内联 `mov [eax],ecx`；经 `vt[0x58]` 发送 | - | `0xB8FF29` | 确证 |
| 3 | 10 | var | bytes | `room_pw` | 房间密码（NUL 结尾） | 来源=入参 arg_8（@0xB8FF2B）；写线原语 `sub_B02B40`；服务端据此校验入房密码 | slot 预算 25（`push 0x19`@0xB8FF23） | `0xB8FF31` | 确证 |
| 4 | var | 1 | u8 | `is_audience` | 是否以观众身份进入 | 来源=入参 arg_C（@0xB8FF46）；写线原语 `sub_B061C0`(u8)；经 `vt[0x58]` 发送 | 0/1 | `0xB8FF4B` | 确证 |
| 5 | var | 1 | u8 | `audience_teamside` | 观众所属阵营侧 | 来源=入参 arg_10（@0xB8FF60）；写线原语 `sub_B061C0`(u8)；经 `vt[0x58]` 发送 | - | `0xB8FF65` | 确证 |
| 6 | var | 4 | u32 | `extrule_id` | 扩展规则 id | 来源=入参 arg_14（@0xB8FF7A）；写线原语 `sub_B02D80`(u32)；经 `vt[0x58]` 发送 | - | `0xB8FF7F` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲（游标自 `buf+2` 起，opcode 占 `buf+0..1`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），**日志名序 == 线序**。

### 4.2 长度闭合
- 2 + 4 + 4 + 25 + 1 + 1 + 4 = 41 ≤ 容量 0x32=50（富余 9）

### 4.3 存疑点
- 日志名序（`matching_type=`→`room_id=`→`room_pw=`→`is_audience=`→`audience_teamside=`→`extrule_id=`）与线序一致。
- 1 字节字段打印器 `sub_B0C1F0`；宽度由写线原语 `sub_B061C0`(u8) 确证。
- ★ 与 `CS-0x6DF1-lounge-btlroom_create` 共享 `matching_type`/`room_pw`(25 槽) 两字段（同族互证）。
- 与 S→C `SC-0x5383-lounge-btlroom_enter_r` 构成请求/应答对。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §4 / notes.md）
