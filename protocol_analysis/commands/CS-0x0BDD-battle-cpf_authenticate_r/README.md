# CS-0x0BDD-cpf_authenticate_r

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0BDD` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle_client` |
| 命令名 | `cpf_authenticate_r` |
| 名字符串 | `)<-_proto_battle_client::send_cpf_authenticate_r( ` @ `0xee184c` |
| 代码位置 | sub_B40520 @ `0xb40520`（`0xb40520`..`0xb40763`） |
| opcode 写入/分发证据 | `0xb405a3`（opcode 写入指令）|
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x86`（134） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽 @`0x00B406ED`）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | （本批次内无同 opcode 反向命令） |

## 2. 结论摘要

- 结论：2 字段 + opcode：CPF 反外挂握手应答（长度前缀 + 变长字节串）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发给对应协议类的处理块 | `0x0BDD` | `0xb405a3` | 确证 |
| 1 | 0 | 4 | u32 | `data_len` | 数据长度（上限 0x80=128，`cmp ebp,80h; ja 出错` @`0xB4059D`） | 来源=入参 arg_4（`0xB40599 mov ebp,[esp+arg_4]`），内联 `mov [eax],ebp`；服务端据此确定后续字节数 | ≤128 | `0xB405B9` | 确证 |
| 2 | 4 | data_len | bytes | `data` | CPF 握手数据块（变长字节串，无 NUL 结尾） | 来源=入参 arg_0（`0xB405D0 mov edx,[esp+arg_0]`），循环内联逐字节 `mov [esi],dl`（`cmp eax,ebp; jb`） | 长度 = data_len | `0xB405D7` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- `send_cpf_authenticate_r` @ `0xB40520`；分配器指纹 `mov <reg>,[<obj+0Ch>]` → `mov edx,[eax+78h]` → `push 0x86; call edx` 取得组包缓冲，游标自 `buf+2` 起（opcode 占 `buf+0..1`）。

### 4.2 长度闭合
- 容量 `0x86`=134 == 2 + 4 + 128（data_len 取上限 128）✓ —— 「容量 = 上限场景线长」。

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
