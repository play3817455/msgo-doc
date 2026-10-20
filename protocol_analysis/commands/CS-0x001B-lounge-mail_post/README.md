# CS-0x001B-mail_post

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x001B` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `mail_post` |
| 名字符串 | `)<-_proto_lounge_client::send_mail_post( ` @ `0xeec19c` |
| 代码位置 | sub_B9B9B0 @ `0xb9b9b0`（`0xb9b9b0`..`0xb9bc7c`） |
| opcode 写入/分发证据 | `0xb9ba39`（opcode 写入指令）|
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x36E`（878） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽 @`0x00B9BC0A`）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | （本批次内无同 opcode 反向命令） |

## 2. 结论摘要

- 结论：4 字段 + opcode；两个变长串（收件人名/标题/正文）紧随 opcode 与类别之后。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发给对应协议类的处理块 | `0x001B` | `0xb9ba39` | 确证 |
| 1 | 0 | var | str | `to_pilot_name` | 收件人角色名（NUL 结尾） | 来源=入参 arg_0（`0xB9BA2D mov edx,[esp+arg_0]`），经写串原语 `sub_B02B40` 写线；服务端据此定位收件人 | 串槽预算 25（`push 19h`） | `0xB9BA43` | 确证 |
| 2 | var | 4 | u32 | `kind` | 邮件类别 | 来源=入参 arg_4（`0xB9BA64 mov edx,[esp+arg_4]`），内联 `mov [ecx],edx` 写线；服务端按类别分流处理 | - | `0xB9BA72` | 确证 |
| 3 | var | var | str | `subject` | 邮件标题（NUL 结尾） | 来源=入参 arg_8（`0xB9BA74 mov ecx,[esp+arg_8]`），写串原语 `sub_B02B40`；服务端存库并推送 | 串槽预算 73（`push 49h`） | `0xB9BA7A` | 确证 |
| 4 | var | var | str | `body` | 邮件正文（NUL 结尾） | 来源=入参 arg_C（`0xB9BA8A mov eax,[esp+arg_C]`），写串原语 `sub_B02B40`；服务端存库并推送 | 串槽预算 766（`push 2FEh`） | `0xB9BA99` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- `send_mail_post` @ `0xB9B9B0`；分配器指纹 `mov <reg>,[<obj+0Ch>]` → `mov edx,[eax+78h]` → `push 0x36E; call edx` 取得组包缓冲，游标自 `buf+2` 起（opcode 占 `buf+0..1`）。

### 4.2 长度闭合
- 声明容量 `0x36E`=878 ≥ 负载上限 873（2 + (25+1) + 4 + (73+1) + (766+1)），符合 C→S「容量 ≥ 负载 + 2」。

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
