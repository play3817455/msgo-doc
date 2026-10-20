# CS-0x753A-lounge-block_list_remove

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x753A` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `block_list_remove` |
| 名字符串 | `)<-_proto_lounge_client::send_block_list_remove(` @ `0xeec168` |
| 代码位置 | sub_B9B720 @ `0xb9b720`（`0xb9b720`..`0xb9b9ae`） |
| opcode 写入证据 | `0xb9b79c` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x2A`（42） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | S→C `SC-0xDEE3-lounge-block_list_remove_r` |

## 2. 结论摘要

- 结论：从黑名单移除一名驾驶员：pilotid + world_id + 被移除者名字 + 是否发系统提示。
- 字段数：**5**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 4 + 4 + 25(串槽) + 4 = 39 ≤ 容量 0x2A = 42`（富余 3）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x753A` | `0xb9b79c` | 确证 |
| 1 | 2 | 4 | u32 | `pilotid` | 被移除驾驶员的 id | 来源=入参 arg_0；内联 `mov [eax],esi`；服务端据此删除黑名单项 | - | `0xB9B7AC` | 确证 |
| 2 | 6 | 4 | u32 | `world_id` | 所在大区（world）id | 来源=入参 arg_4；内联 `mov [eax],ecx`；服务端据此定位跨服黑名单 | - | `0xB9B7C9` | 确证 |
| 3 | 10 | var | bytes | `to_pilot_name` | 被移除者名字（NUL 串） | 来源=入参 arg_8；写线原语 `sub_B02B40`；用于日志/回显 | 串槽预算 25（`push 19h`@0xB9B7C3） | `0xB9B7D1` | 确证 |
| 4 | var | 4 | u32 | `send_sysmes` | 是否发送系统提示 | 来源=入参 arg_C；写线原语 `sub_B02D80`；服务端据此决定是否公告 | 0/1 | `0xB9B7EB` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xb9b766`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xb9b79c`（`mov word ptr [...], 0x753A`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2 + 4 + 4 + 25(串槽) + 4 = 39 ≤ 容量 0x2A = 42`（富余 3）

### 4.3 存疑点
- `send_sysmes` 为 u32（写线原语 `sub_B02D80`），非 u8——按写线原语判定。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
