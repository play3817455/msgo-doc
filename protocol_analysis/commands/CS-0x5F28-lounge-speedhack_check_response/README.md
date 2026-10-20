# CS-0x5F28-lounge-speedhack_check_response

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x5F28` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `speedhack_check_response` |
| 名字符串 | `)<-_proto_lounge_client::send_speedhack_check_response(` @ `0xeed04c` |
| 代码位置 | sub_BA4D50 @ `0xba4d50`（`0xba4d50`..`0xba4f3a`） |
| opcode 写入证据 | `0xba4dc4` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0xA`（10） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | 见 §4.3 与其他命令的关联 / INDEX 反向表 |

## 2. 结论摘要

- 结论：反外挂速度检测回执：是否检出调试器 + 进程引用计数。
- 字段数：**3**（含 opcode）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 2 + 2 = 6 ≤ 容量 0xA=10（富余 4）`

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 分发给 lounge 协议类处理块（C→S 无 case 块） | 0x5F28 | `0xBA4DC4` | 确证 |
| 1 | 2 | 2 | u16 | `debugger_found` | 是否检出调试器 | 来源=入参 arg_0 的低 16 位（@0xBA4DD0）；内联 `mov [eax],si`；经 `vt[0x58]` 发送 | 0/1 | `0xBA4DDA` | 确证 |
| 2 | 4 | 2 | u16 | `proc_ref_count` | 相关进程引用计数 | 来源=入参 arg_4 的低 16 位（@0xBA4DE3）；内联 `mov [edx],cx`；经 `vt[0x58]` 发送 | - | `0xBA4DE8` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲（游标自 `buf+2` 起，opcode 占 `buf+0..1`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），**日志名序 == 线序**。

### 4.2 长度闭合
- 2 + 2 + 2 = 6 ≤ 容量 0xA=10（富余 4）

### 4.3 存疑点
- 日志名序（`debugger_found=`→`proc_ref_count=`）与线序一致。
- 两个字段打印器均为 `sub_B032A0`(u16)，与线宽一致。
- 与 S→C `SC-0x0A78-lounge-speedhack_check_request` 构成**应答/请求对**（请求为 S→C、回执为 C→S）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §4 / notes.md）
