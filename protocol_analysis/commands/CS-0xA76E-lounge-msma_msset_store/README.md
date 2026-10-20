# CS-0xA76E-lounge-msma_msset_store

> 状态：`DONE`（2026-09-20，批次-20）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xA76E` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `msma_msset_store` |
| 名字符串 | `)<-_proto_lounge_client::send_msma_msset_store(` @ `0xEEBC18` |
| 代码位置 | sub_B988D0 @ `0xB988D0`（`0xB988D0`..`0xB98A99`） |
| opcode 写入证据 | `0xB98951` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x0062`（98） |
| 容量申请证据 | `0xB98916`（`push 0x0062`） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` @ `0xB98A25` |
| 附加通知 | `[obj+79A8h]` 回调，模块 id `0x129` @ `0xB98A42` |
| 配对命令 | S→C `SC-0xB8BB-lounge-msma_msset_store_r`（已 DONE，`ms_set` 95B / 槽 96 —— **与本次 C→S 写入器独立算出同值**） |

## 2. 结论摘要

- 结论：保存机体套装（ms_set：机体唯一 id + 卡组槽 + 套装名 + 4 个机体 id + 4 个装备槽位）。
- 字段数：**7**（含 opcode 第 0 项）
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）
- 是否分帧：否（单帧命令）
- 容量等式：`2 + 95(结构体) = 97 ≤ 容量 0x62 = 98`（富余 1）
- 结构体/数组展开：`ms_set` = `uniq_id(u64) + deck_type(u16) + deck_slot(u16) + setname(u8[43]) + msma_uniq_ids(u64[4]) + equip_set_slots(u16[4])` = 8+2+2+43+32+8 = **95B**

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**（写线指令操作数宽度 / 写线原语），禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | 0xA76E | `0xB98951` | 确证 |
| 1 | 2 | 8 | u64 | `ms_set.uniq_id` | 套装记录唯一 id | 来源=入参 `arg_0` 指向的源结构 `[src+0]`/`[src+4]`（复合写入器 `sub_B41B10` 两次内联 `mov [ecx],edx` / `mov [ecx+4],edx`，低 32 位在前） | - | `0xB41B27, 0xB41B2B` | 确证 |
| 2 | 10 | 2 | u16 | `ms_set.deck_type` | 卡组类型 | 复合写入器 `sub_B41B10`：`mov dx,[edi+8]` → `mov [ecx],dx` | - | `0xB41B42` | 确证 |
| 3 | 12 | 2 | u16 | `ms_set.deck_slot` | 套装槽位 | 复合写入器 `sub_B41B10`：`mov dx,[edi+0Ah]` → `mov [ecx],dx` | - | `0xB41B5A` | 确证 |
| 4 | 14 | 43 | u8[43] | `ms_set.setname` | 套装名（定长 43 字节） | 复合写入器 `sub_B41B10`：`mov dl,[ecx+edi+0Ch]` 循环 `cmp ecx,2Bh`（43 次） | - | `0xB41B71` | 确证 |
| 5 | 57 | 32 | u64[4] | `ms_set.msma_uniq_ids` | 四个机体的唯一 id | 复合写入器 `sub_B41B10`：`mov ebx,[ecx]`/`[ecx+4]` 循环 4 次（源 `[edi+38h]` 起，步进 8） | - | `0xB41B92, 0xB41B96` | 确证 |
| 6 | 89 | 8 | u16[4] | `ms_set.equip_set_slots` | 四个装备槽位 | 复合写入器 `sub_B41B10`：`mov di,[edx]` 循环 4 次（源 `[edi+58h]` 起，步进 2） | - | `0xB41BBA` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量申请 `push 0x0062` @ `0xB98916`）。
- 写线游标：`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xB98951`（`mov     word ptr [edi], 0A76Eh`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …`），**日志名序 == 线序**。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`（`sub <len>,<buf首址>` = 游标 − 缓冲首址）。

### 4.2 长度闭合
- `2 + 95(结构体) = 97 ≤ 容量 0x62 = 98`（富余 1）

### 4.3 存疑点
- 本命令**无顶层逐字段写线**：唯一字段 `ms_set` 由复合写入器 `sub_B41B10`（`0xB41B10..0xB41BE5`）整块写出，结构体线长必须进函数体逐字段累加（8+2+2+43+32+8 = 95）。
- 字段名取自 `ms_set` 打印器 `sub_B4A7E0` 的成员名（`uniq_id=`/`deck_type=`/`deck_slot=`/`setname=`/`msma_uniq_ids={`/`equip_set_slots={`）。
- 与 S→C `SC-0xB8BB-msma_msset_store_r` 的 `ms_set` **线长 95 跨方向精确互证**。
- 容量 98 = 2 + 95 + 1（富余 1）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / notes.md）
