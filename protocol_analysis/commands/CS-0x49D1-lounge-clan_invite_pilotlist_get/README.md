# CS-0x49D1-lounge-clan_invite_pilotlist_get

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x49D1` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `clan_invite_pilotlist_get` |
| 名字符串 | `)<-_proto_lounge_client::send_clan_invite_pilotlist_get(` @ `0xeecc3c` |
| 代码位置 | sub_BA2680 @ `0xba2680`（`0xba2680`..`0xba2883`） |
| opcode 写入证据 | `0xba26fc` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x12`（18） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | 见 §4.3 与其他命令的关联 / INDEX 反向表 |

## 2. 结论摘要

- 结论：获取可邀请入队（部队）的玩家列表：页码 + 排序结构。
- 字段数：**3**（含 opcode）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 4 + 9 = 15 ≤ 容量 0x12=18（富余 3）`

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 分发给 lounge 协议类处理块（C→S 无 case 块） | 0x49D1 | `0xBA26FC` | 确证 |
| 1 | 2 | 4 | u32 | `page` | 页码 | 来源=入参 arg_0（@0xBA2708）；内联 `mov [eax],ecx`；经 `vt[0x58]` 发送 | - | `0xBA2714` | 确证 |
| 2 | 6 | 9 | struct<sort_info_invite> | `sort_info` | 排序结构（邀请列表短形 9×u8 = 9B；勿与 clan_search 18B 形混用） | 来源=入参 arg_4（@0xBA2716）；经复合写入器 `sub_B41E00` 逐字段写线；服务端据此排序 | 见 §5（结构体构成） | `0xBA271C` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲（游标自 `buf+2` 起，opcode 占 `buf+0..1`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），**日志名序 == 线序**。

### 4.2 长度闭合
- 2 + 4 + 9 = 15 ≤ 容量 0x12=18（富余 3）

### 4.3 存疑点
- 日志名序（`page=`→`sort_info=`）与线序一致。
- `sort_info` 由复合写入器 `sub_B41E00`（`0xB41E00..0xB41EB7`）写成 **9** 字节：内联 4×u8（源偏移 0..3：`sort_type`/`is_class_filter`/`class_filter_begin`/`class_filter_end`）+ 5×`sub_B061C0`(u8)（源偏移 4..8：`is_time_filter`/`time_filter_begin`/`time_filter_end`/`is_bonus_filter`/`bonus_filter`）。成员名取自**打印器 `sub_B4EEF0`**（标签 @`0xEE345C`..`0xEE34F4`，逐字节 `a2[0..8]`），本命令在 `sub_BA2680` 里正是用它打印自己刚写完的那个入参（`0xBA27CB`：`sub_B4EEF0(v12, a3)`，而 `a3` 就是 `sub_B41E00` 的源指针）⇒ 名序 == 线序。
- 该 9B 形与 `clan_search` 的 `sort_info`（18B，打印器 `sub_B4F180`）**不是同一套字段**，已在 `db_design/schema/composites/sort_info_invite.json` 单列：两者打印器标签**零重合**（本形 9 个 vs 18B 的 `filter_type`/`lv_under`/…/`style_value` 12 个），同偏移处语义也不同（本形 +1 是机种筛选开关，18B 的 `lv_under` 在 +2）。原语划分（内联 4 + `sub_B061C0` 5）同构只是巧合，**勿交叉套用**；本形是请求作用域的排序入参（SC-0x5696 原样回显），不是玩家存档，故 2026-09-30 起不再登记为 18B `sort_info` 的 `other_wire_forms`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §4 / notes.md）
