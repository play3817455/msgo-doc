# CS-0xF5C9-lounge-gacha_exec_w_buy_ticket

> 状态：`DONE`（2026-09-20，批次-22）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xF5C9` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `gacha_exec_w_buy_ticket` |
| 名字符串 | `)<-_proto_lounge_client::send_gacha_exec_w_buy_ticket(` @ `0x00EEC524` |
| 代码位置 | `sub_B9E240` @ `0x00B9E240`（`0x00B9E240`..`0x00B9E5CC`） |
| opcode 写入证据 | `0x00B9E2BC` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x022`（34） |
| 容量申请证据 | `0x00B9E286`（分配器 `[obj+0Ch]` 的 `vt[0x78]`） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` @ `0x00B9E558` |
| 提交 | `sub_B02FF0` @ `0x00B9E3DD` |
| 配对命令 | S→C `SC-0xF66B-lounge-gacha_exec_w_buy_ticket_r` |

## 2. 结论摘要

- 字段数：**9**（含 opcode 第 0 项）
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）
- 是否分帧：否（单帧命令）
- 容量等式：`2 + 4 + 1 + 4 + 1 + 1 + 4 + 4 + 1 = 22 == 容量 0x22 = 22（精确相等）`

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**（写线指令操作数宽度 / 写线原语），禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | 0xF5C9 | `00B9E2BC` | 确证 |
| 1 | 0 | 4 | u32 | `shopitemid` | 商店物品 ID | 来源=入参 `arg_0`（`mov esi,dword ptr [esp+arg_0]` @`0xB9E2C8`）→ 内联写 `[ecx],esi`（@`0xB9E2CC`） | - | `0xB9E2C8`;`0xB9E2CC` | 确证 |
| 2 | 4 | 1 | u8 | `id_type` | ID 类型 | 来源=入参 `arg_4`（`mov al,byte ptr [esp+arg_4]` @`0xB9E2D9`）→ 内联写 `[edx],al`（@`0xB9E2E5`） | ? | `0xB9E2D9`;`0xB9E2E5` | 确证 |
| 3 | 5 | 4 | u32 | `num` | 购买数量 | 来源=入参 `arg_8` → 写原语 `sub_B02D80`（u32 @`0xB9E2ED`） | - | `0xB9E2ED` | 确证 |
| 4 | 9 | 1 | u8 | `tab_type` | 页签类型 | 来源=入参 `arg_C` → 写原语 `sub_B061C0`（u8 @`0xB9E307`） | ? | `0xB9E307` | 确证 |
| 5 | 10 | 1 | u8 | `is_cp` | 是否使用 CP 点数 | 来源=入参 `arg_10` → 写原语 `sub_B061C0`（u8 @`0xB9E321`） | 0/1 | `0xB9E321` | 确证 |
| 6 | 11 | 4 | u32 | `total_price` | 总价 | 来源=入参 `arg_14` → 写原语 `sub_B02D80`（u32 @`0xB9E33B`） | - | `0xB9E33B` | 确证 |
| 7 | 15 | 4 | u32 | `gacha_id` | 扭蛋 ID | 来源=入参 `arg_18` → 写原语 `sub_B02D80`（u32 @`0xB9E355`） | - | `0xB9E355` | 确证 |
| 8 | 19 | 1 | u8 | `is_bundle` | 是否捆绑购买 | 来源=入参 `arg_1C` → 写原语 `sub_B061C0`（u8 @`0xB9E36F`） | 0/1 | `0xB9E36F` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>`（容量申请 `push 0x22` @ `0x00B9E286`）。
- 写线游标：`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0x00B9E2BC`。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …`），**日志名序 == 线序**。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`（`sub <len>,<buf首址>` = 游标 − 缓冲首址）。

### 4.2 长度闭合
- `2 + 4 + 1 + 4 + 1 + 1 + 4 + 4 + 1 = 22 == 容量 0x22 = 22（精确相等）`

### 4.3 存疑点
- 见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / `notes.md`）
