# CS-0x34A9-battle-proto_version_check

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x34A9` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle_client` |
| 命令名 | `proto_version_check` |
| 名字符串 | `)<-_proto_battle_client::send_proto_version_check(` @ `0xee0540` |
| 代码位置 | sub_B318D0 @ `0x00b318d0`（`0x00b318d0`..`0x00b31b06`） |
| opcode 写入/分发证据 | `0xb31949`（opcode 写入指令）|
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0xE`（14） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽 @`0xB31A95`）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | `CS-0x34A9-auth-proto_version_check` / `CS-0x34A9-lounge-proto_version_check` |

## 2. 结论摘要

- 结论：协议版本校验（battle 协议类，字段与 auth/lounge 完全一致）。
- 字段数：**4**（含 opcode）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载`）。
- 是否分帧：否（单帧命令）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 分发给对应协议类的处理块（C→S 无 case 块） | `0x34A9` | `0xB31949` | 确证 |
| 1 | 2 | 4 | u32 | `version` | 协议版本号 | 来源=入参 arg_0（`0xB31955`）；内联 `mov [游标], reg`；服务端校验版本，不匹配则拒绝进入 | - | `0xB31959` | 确证 |
| 2 | 6 | 4 | u32 | `crc` | 资源 CRC 校验值 | 来源=入参 arg_4（`0xB31968`）；内联 `mov [游标], reg`；服务端校验客户端资源完整性 | - | `0xB31974` | 确证 |
| 3 | 10 | 4 | u32 | `gentime` | 资源生成时间戳 | 来源=入参 arg_8（`0xB31977`）；经写原语 `sub_B02D80`；服务端与 CRC 一并校验客户端资源版本 | - | `0xB3197C` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- `sub_B318D0` @ `0x00b318d0`；分配器指纹 `mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push 0xE; call <reg>` 取得组包缓冲（游标自 `buf+2` 起，opcode 占 `buf+0..1`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块日志串，**日志名序 == 线序**。

### 4.2 长度闭合
- 2 + 4 + 4 + 4 = **14** == 容量 `0xE`（精确相等）

### 4.3 存疑点
- 与 `CS-0x34A9-auth-proto_version_check` / `CS-0x34A9-lounge-proto_version_check` 字段完全一致（同 opcode 跨协议类）。
- 详见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接
