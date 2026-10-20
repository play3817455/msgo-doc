# CS-0x03AE-msma_buildup_complete

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x03AE` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `msma_buildup_complete` |
| 名字符串 | `)<-_proto_lounge_client::send_msma_buildup_complete( ` @ `0xeeb8f8` |
| 代码位置 | sub_B967E0 @ `0xb967e0`（`0xb967e0`..`0xb96a66`） |
| opcode 写入/分发证据 | `0xb9685c`（opcode 写入指令）|
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x16`（22） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽 @`0x00B969F4`）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | （本批次内无同 opcode 反向命令） |

## 2. 结论摘要

- 结论：4 字段 + opcode：机体强化完成上报（u64 机体唯一 ID + 券 + 用量 + 参数序号）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发给对应协议类的处理块 | `0x03AE` | `0xb9685c` | 确证 |
| 1 | 0 | 8 | u64 | `uniqid_ms` | 机体唯一 ID（64 位） | 来源=入参 arg_0/arg_4（`0xB96868 mov esi,[esp+arg_0]`、`0xB9686E mov esi,[esp+arg_4]`），内联两次 `mov [eax],esi` / `mov [eax+4],esi`（低 32 位在前）；服务端据此定位机体 | - | `0xB9686C,0xB96872` | 确证 |
| 2 | 8 | 4 | u32 | `ticket_id` | 使用的强化券 ID | 来源=入参 arg_8（`0xB96880 mov ecx,[esp+arg_8]`）；服务端据此扣券 | - | `0xB96884` | 确证 |
| 3 | 12 | 2 | u16 | `usenum` | 券使用数量 | 来源=入参 arg_C（`0xB9688F lea eax,[esp+arg_C]`）经写 u16 原语 `sub_B02DA0`；服务端据此累计消耗 | - | `0xB96894` | 确证 |
| 4 | 14 | 2 | u16 | `param_idx` | 强化参数序号（选择的分支） | 来源=入参 arg_10（`0xB968A9 lea edx,[esp+arg_10]`）经写 u16 原语 `sub_B02DA0`；服务端据此决定强化路线 | - | `0xB968AE` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- `send_msma_buildup_complete` @ `0xB967E0`；分配器指纹 `mov <reg>,[<obj+0Ch>]` → `mov edx,[eax+78h]` → `push 0x16; call edx` 取得组包缓冲，游标自 `buf+2` 起（opcode 占 `buf+0..1`）。

### 4.2 长度闭合
- 容量 `0x16`=22 ≥ 线长 18 ✓。

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
