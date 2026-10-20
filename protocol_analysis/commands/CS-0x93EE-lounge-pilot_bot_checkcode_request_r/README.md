# CS-0x93EE-lounge-pilot_bot_checkcode_request_r

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x93EE` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_bot_checkcode_request_r` |
| 名字符串 | `)<-_proto_lounge_client::send_pilot_bot_checkcode_request_r(` @ `0xeea74c` |
| 代码位置 | sub_B8C610 @ `0xb8c610`（`0xb8c610`..`0xb8c7e6`） |
| opcode 写入证据 | `0xb8c693` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x12`（18） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | S→C `SC-0x0D24-lounge-pilot_bot_checkcode_request`（已 DONE） |

## 2. 结论摘要

- 结论：提交机器人校验码（checkcode）：一条 NUL 结尾的校验码串。
- 字段数：**2**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 13(串槽) = 15 ≤ 容量 0x12 = 18`（富余 3）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x93EE` | `0xb8c693` | 确证 |
| 1 | 2 | var | bytes | `code` | 校验码（NUL 结尾字符串） | 来源=入参 arg_0；写线原语 `sub_B02B40`；服务端据此判定是否为机器人 | 串槽预算 13（`push 0Dh`@0xB8C68B） | `0xB8C69C` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xb8c656`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xb8c693`（`mov word ptr [...], 0x93EE`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2 + 13(串槽) = 15 ≤ 容量 0x12 = 18`（富余 3）

### 4.3 存疑点
- 容量按**串槽预算**记：`push 0Dh`=13（紧邻 `sub_B02B40`）⇒ `容量 = 2 + 13 + 3`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
