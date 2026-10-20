# CS-0x83B2-lounge-msma_equip_rental_modules_update_requip

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x83B2` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `msma_equip_rental_modules_update_requip` |
| 名字符串 | `)<-_proto_lounge_client::send_msma_equip_rental_modules_update_requip(` @ `0xeeb5d8` |
| 代码位置 | sub_B947B0 @ `0xb947b0`（`0xb947b0`..`0xb94a10`） |
| opcode 写入证据 | `0xb94832` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x12C6`（4806） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | S→C `SC-0x1E8D-lounge-msma_equip_rental_modules_update_requip_r`（同族 `SC-0xEE0F-lounge-msma_equip_rental_modules_update_r`） |

## 2. 结论摘要

- 结论：批量更新机体「租赁模块」装备：模块 id + **固定 600 元 u64 机体 id 列表**（无线上计数）。
- 字段数：**3**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 4 + 600×8 = 4806 == 容量 0x12C6 = 4806`（精确相等）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x83B2` | `0xb94832` | 确证 |
| 1 | 2 | 4 | u32 | `module_id` | 租赁模块 id | 来源=入参 arg_0；内联 `mov [eax],ecx`；服务端据此定位模块 | - | `0xB94847` | 确证 |
| 2 | 6 | 4800 | u64[600] | `msid_list` | 机体 id 列表（固定 600 元） | 来源=入参 arg_4（数组首址，`mov edi,[esi+eax*8]`/`mov edi,[esi+eax*8+4]` 逐元素 8 字节，元素索引 `eax` 自 0 循环到 `cmp eax,258h`=600）；服务端据此批量装配 | 固定 600 元，**无线上计数**；非空校验 `test esi,esi; jz 出错`@0xB94841 | `0xB9485F, 0xB94865 (loop @0xB94854..0xB94876)` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xb947fa`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xb94832`（`mov word ptr [...], 0x83B2`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2 + 4 + 600×8 = 4806 == 容量 0x12C6 = 4806`（精确相等）

### 4.3 存疑点
- **「整块定长数组（无线上 count）」形态**：循环上界为**字面量 `cmp eax,258h`=600**，元素步进 8（u64），无计数写入 ⇒ `u64[600]`，线长 4800；容量等式精确：`2 + 4 + 4800 = 4806`。
- 元素为 u64（低 32 位在前写入）；打印器 `sub_B08500` 按 u64 打印。
- 本命令为**全批最大线长**（4806B）；单帧上限 16366B，无需分帧。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
