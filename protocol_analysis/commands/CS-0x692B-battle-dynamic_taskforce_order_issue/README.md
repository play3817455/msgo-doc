# CS-0x692B-battle-dynamic_taskforce_order_issue

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x692B` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle_client` |
| 命令名 | `dynamic_taskforce_order_issue` |
| 名字符串 | `)<-_proto_battle_client::send_dynamic_taskforce_order_issue(` @ `0xee1644` |
| 代码位置 | sub_B3F3F0 @ `0xb3f3f0`（`0xb3f3f0`..`0xb3f77e`） |
| opcode 写入证据 | `0xb3f46f` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x5E`（94） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | 见 §4.3 与其他命令的关联 / INDEX 反向表 |

## 2. 结论摘要

- 结论：下达动态任务部队指令：指令类型/参数 + 两组「计数 + 数组」（成员 u8 / NPC u16）。
- 字段数：**7**（含 opcode）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 1 + 4 + 4 + 51×1 + 4 + 12×2 = 90 ≤ 容量 0x5E=94（上限场景，富余 4）`

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 分发给 battle 协议类处理块（C→S 无 case 块） | 0x692B | `0xB3F46F` | 确证 |
| 1 | 2 | 1 | u8 | `order_kind` | 指令种类 | 来源=入参 arg_0 的低字节（@0xB3F47F）；内联 `mov [ecx],dl`；经 `vt[0x58]` 发送 | - | `0xB3F483` | 确证 |
| 2 | 3 | 4 | u32 | `order_param` | 指令参数 | 来源=入参 arg_4（@0xB3F497）；内联 `mov [esi],eax`；经 `vt[0x58]` 发送 | - | `0xB3F49B` | 确证 |
| 3 | 7 | 4 | u32 | `select_members_num` | 成员数组元素数（**上限校验 ≤ 0x33=51**） | 来源=入参 arg_C（@0xB3F490）；写线原语 `sub_B02D80`(u32)；上限 `cmp ebp,33h`@0xB3F494 | 0..51 | `0xB3F4B1` | 确证 |
| 4 | 11 | var | array<u8,N> | `select_members` | 成员列表（N = `select_members_num`，N ≤ 51，每元素 u8） | 来源=入参 arg_8 指向的字节数组（@0xB3F4C7 `mov ecx,[arg_8]`→`lea edx,[esi+ecx]`）；循环内 `sub_B061C0`(u8)；经 `vt[0x58]` 发送 | 元素 u8，逐个写入 | `0xB3F4D4` | 确证 |
| 5 | var | 4 | u32 | `select_npcs_num` | NPC 数组元素数（**上限校验 ≤ 0x0C=12**） | 来源=入参 arg_14（@0xB3F4EB）；写线原语 `sub_B02D80`(u32)；上限 `cmp ebx,0Ch`@0xB3F4EF | 0..12 | `0xB3F502` | 确证 |
| 6 | var | var | array<u16,N> | `select_npcs` | NPC 列表（N = `select_npcs_num`，N ≤ 12，每元素 u16） | 来源=入参 arg_10 指向的 u16 数组（@0xB3F518 `mov edx,[arg_10]`，步进 +2）；循环内 `sub_B02DA0`(u16)；经 `vt[0x58]` 发送 | 元素 u16，逐个写入 | `0xB3F52A` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲（游标自 `buf+2` 起，opcode 占 `buf+0..1`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），**日志名序 == 线序**。

### 4.2 长度闭合
- 2 + 1 + 4 + 4 + 51×1 + 4 + 12×2 = 90 ≤ 容量 0x5E=94（上限场景，富余 4）

### 4.3 存疑点
- 日志名序（`order_kind=`→`order_param=`→`select_members={`→`select_npcs={`）与线序一致。
- 两个数组计数字段的日志**未单独打标签** ⇒ 字段名 `select_members_num`/`select_npcs_num` 为**推定**（类型/长度/上限已确证）。
- ★ 两数组元素宽度**不同**：成员 u8、NPC u16——须分别按各自写线原语（`sub_B061C0` / `sub_B02DA0`）判宽。
- 与 S→C `SC-0x483F-battle-dynamic_taskforce_order_result` 构成请求/结果对。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §4 / notes.md）
