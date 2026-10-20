# CS-0x6B74-lounge-bugtrace_report

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x6B74` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `bugtrace_report` |
| 名字符串 | `)<-_proto_lounge_client::send_bugtrace_report(` @ `0xeed1a8` |
| 代码位置 | sub_BA5BE0 @ `0xba5be0`（`0xba5be0`..`0xba5ece`） |
| opcode 写入证据 | `0xba5c62` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x1816`（6166） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | 见 §4.3 与其他命令的关联 / INDEX 反向表 |

## 2. 结论摘要

- 结论：崩溃/异常上报：发生时间 + pc + 调用栈串 + 异常码 + 附加信息串。
- 字段数：**6**（含 opcode）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 4 + 4 + 3073 + 4 + 3073 = 6160 ≤ 容量 0x1816=6166（富余 6，上限场景）`

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 分发给 lounge 协议类处理块（C→S 无 case 块） | 0x6B74 | `0xBA5C62` | 确证 |
| 1 | 2 | 4 | u32 | `occured_time` | 异常发生时间（客户端时间戳） | 来源=入参 arg_0（@0xBA5C6E）；内联 `mov [eax],esi`；经 `vt[0x58]` 发送 | - | `0xBA5C72` | 确证 |
| 2 | 6 | 4 | u32 | `pc` | 异常指令指针（pc） | 来源=入参 arg_4（@0xBA5C81）；内联 `mov [eax],ecx`；经 `vt[0x58]` 发送 | - | `0xBA5C92` | 确证 |
| 3 | 10 | var | bytes | `stack` | 调用栈文本（NUL 结尾） | 来源=入参 arg_8（@0xBA5C94）；写线原语 `sub_B02B40`；服务端据此定位崩溃点 | slot 预算 3073（`push 0xC01`@0xBA5C89） | `0xBA5C9A` | 确证 |
| 4 | var | 4 | u32 | `excode` | 异常码 | 来源=入参 arg_C（@0xBA5CAF）；写线原语 `sub_B02D80`(u32)；经 `vt[0x58]` 发送 | - | `0xBA5CB4` | 确证 |
| 5 | var | var | bytes | `exinfo` | 附加异常信息（NUL 结尾） | 来源=入参 arg_10（@0xBA5CC4）；写线原语 `sub_B02B40`；经 `vt[0x58]` 发送 | slot 预算 3073（`push 0xC01`@0xBA5CC8） | `0xBA5CD3` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲（游标自 `buf+2` 起，opcode 占 `buf+0..1`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），**日志名序 == 线序**。

### 4.2 长度闭合
- 2 + 4 + 4 + 3073 + 4 + 3073 = 6160 ≤ 容量 0x1816=6166（富余 6，上限场景）

### 4.3 存疑点
- 日志名序（`occured_time=`→`pc=`→`stack=`→`excode=`→`exinfo=`）与线序一致。
- 两个串槽预算均为 3073（`push 0xC01`）⇒ 容量按串槽计。
- ★ 与本项目 `topics\20-客户端崩溃取证SOP.md` 的崩溃链一致：`0x6B74` 即客户端崩溃上报（`go_srv.err 0x6B74` 的线上对应命令）。
- 与 S→C `SC-0x6B74-lounge-bugtrace_report_r`（若存在）构成请求/应答对；INDEX 反向表见交叉参照。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §4 / notes.md）
