# CS-0x16BD-chat_whisper_up

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x16BD` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `chat_whisper_up` |
| 名字符串 | `)<-_proto_lounge_client::send_chat_whisper_up( ` @ `0xeea8f0` |
| 代码位置 | sub_B8D3D0 @ `0xb8d3d0`（`0xb8d3d0`..`0xb8d602`） |
| opcode 写入/分发证据 | `0xb8d459`（opcode 写入指令）|
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0xD6`（214） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽 @`0x00B8D593`）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | （本批次内无同 opcode 反向命令） |

## 2. 结论摘要

- 结论：2 字段 + opcode：私聊上行（对象名 + 文本）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发给对应协议类的处理块 | `0x16BD` | `0xb8d459` | 确证 |
| 1 | 0 | var | str | `to_pilot_name` | 私聊对象角色名（NUL 结尾） | 来源=入参 arg_0（`0xB8D44D mov edx,[esp+arg_0]`），写串原语 `sub_B02B40` | 串槽预算 25（`push 19h`） | `0xB8D463` | 确证 |
| 2 | var | var | str | `msg` | 私聊文本（NUL 结尾） | 来源=入参 arg_4（`0xB8D473 mov ecx,[esp+arg_4]`），写串原语 `sub_B02B40` | 串槽预算 181（`push 0B5h`） | `0xB8D482` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- `send_chat_whisper_up` @ `0xB8D3D0`；分配器指纹 `mov <reg>,[<obj+0Ch>]` → `mov edx,[eax+78h]` → `push 0xD6; call edx` 取得组包缓冲，游标自 `buf+2` 起（opcode 占 `buf+0..1`）。

### 4.2 长度闭合
- 容量 `0xD6`=214 ≥ 2 + 26 + 182 = 210 ✓。

### 4.3 存疑点
- 见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 <= 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接
