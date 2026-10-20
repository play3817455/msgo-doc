# CS-0xA791-lounge-clan_msgboard_msg_delete

> 状态：`DONE`（2026-09-20，批次-20）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xA791` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `clan_msgboard_msg_delete` |
| 名字符串 | `)<-_proto_lounge_client::send_clan_msgboard_msg_delete(` @ `0xEECBC4` |
| 代码位置 | sub_BA2280 @ `0xBA2280`（`0xBA2280`..`0xBA2474`） |
| opcode 写入证据 | `0xBA22F4` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x000E`（14） |
| 容量申请证据 | `0xBA22C6`（`push 0x000E`） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` @ `0xBA2402` |
| 附加通知 | `[obj+79A8h]` 回调，模块 id `0x1D9` @ `0xBA241D` |
| 配对命令 | S→C `SC-0xAD90-lounge-clan_msgboard_msg_delete_r`（已 DONE） |

## 2. 结论摘要

- 结论：删除战队留言板上的一条消息。
- 字段数：**3**（含 opcode 第 0 项）
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）
- 是否分帧：否（单帧命令）
- 容量等式：`2 + 8(u64) + 1 = 11 ≤ 容量 0xE = 14`（富余 3）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**（写线指令操作数宽度 / 写线原语），禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | 0xA791 | `0xBA22F4` | 确证 |
| 1 | 2 | 8 | u64 | `msg_id` | 留言板消息 id | 来源=入参 `arg_0`/`arg_4`（两次内联 `mov [eax],edi` / `mov [eax+4],edi`，低 32 位在前） | - | `0xBA2304, 0xBA230F` | 确证 |
| 2 | 10 | 1 | u8 | `clan_kind` | 战队类别 | 来源=入参 `arg_8`（`mov cl,[esp+40h+arg_8]` → 内联 `mov [edx],cl`） | - | `0xBA231C` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量申请 `push 0x000E` @ `0xBA22C6`）。
- 写线游标：`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xBA22F4`（`mov     word ptr [ebp+0], 0A791h`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …`），**日志名序 == 线序**。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`（`sub <len>,<buf首址>` = 游标 − 缓冲首址）。

### 4.2 长度闭合
- `2 + 8(u64) + 1 = 11 ≤ 容量 0xE = 14`（富余 3）

### 4.3 存疑点
- `clan_kind` 打印器 `sub_B0C1F0`（`movsx`）；线宽 1 字节记 `u8`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / notes.md）
