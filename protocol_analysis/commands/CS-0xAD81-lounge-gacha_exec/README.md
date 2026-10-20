# CS-0xAD81-lounge-gacha_exec

> 状态：`DONE`（2026-09-20，批次-20）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xAD81` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `gacha_exec` |
| 名字符串 | `)<-_proto_lounge_client::send_gacha_exec(` @ `0xEEC4F8` |
| 代码位置 | sub_B9E000 @ `0xB9E000`（`0xB9E000`..`0xB9E23C`） |
| opcode 写入证据 | `0xB9E07C` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x000E`（14） |
| 容量申请证据 | `0xB9E046`（`push 0x000E`） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` @ `0xB9E1CA` |
| 附加通知 | `[obj+79A8h]` 回调，模块 id `0x190` @ `0xB9E1E5` |
| 配对命令 | S→C `SC-0x467F-lounge-gacha_exec_r`（已 DONE；相关 `SC-0xF66B-lounge-gacha_exec_w_buy_ticket_r`） |

## 2. 结论摘要

- 结论：执行扭蛋（可选连抽）。
- 字段数：**4**（含 opcode 第 0 项）
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）
- 是否分帧：否（单帧命令）
- 容量等式：`2 + 4 + 4 + 1 = 11 ≤ 容量 0xE = 14`（富余 3）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**（写线指令操作数宽度 / 写线原语），禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | 0xAD81 | `0xB9E07C` | 确证 |
| 1 | 2 | 4 | u32 | `gacha_id` | 扭蛋机 id | 来源=入参 `arg_0`（内联 `mov [eax],esi`） | - | `0xB9E08C` | 确证 |
| 2 | 6 | 4 | u32 | `exec_type` | 执行方式 | 来源=入参 `arg_4`（`mov ecx,dword ptr [esp+48h+arg_4]` → 内联 `mov [eax],ecx`） | 取值域 {1,2,3}（`sub_869ED0` 传 1@`0x869F9C`/`0x869FB3`、3@`0x869FFF`、2@`0x86A0CE`；`sub_8708B0` 传 2@`0x870A00`/`0x870971`；1=单次 / 2=连抽 / 3=特殊） | `0xB9E0A7` | 确证 |
| 3 | 10 | 1 | u8 | `is_bundle` | 是否连抽 | 来源=入参 `arg_8`；写线原语 `sub_B061C0`(u8) | 0/1 | `0xB9E0AF` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量申请 `push 0x000E` @ `0xB9E046`）。
- 写线游标：`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xB9E07C`（`mov     word ptr [ebp+0], 0AD81h`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …`），**日志名序 == 线序**。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`（`sub <len>,<buf首址>` = 游标 − 缓冲首址）。

### 4.2 长度闭合
- `2 + 4 + 4 + 1 = 11 ≤ 容量 0xE = 14`（富余 3）

### 4.3 存疑点
- `is_bundle` 打印器 `sub_B0C1F0`（`movsx`）；线宽 1 字节记 `u8`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / notes.md）
