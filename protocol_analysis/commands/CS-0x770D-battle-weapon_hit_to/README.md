# CS-0x770D-battle-weapon_hit_to

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x770D` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle_client` |
| 命令名 | `weapon_hit_to` |
| 名字符串 | `)<-_proto_battle_client::send_weapon_hit_to(` @ `0xee10f8` |
| 代码位置 | sub_B3B7A0 @ `0xb3b7a0`（`0xb3b7a0`..`0xb3c282`） |
| opcode 写入证据 | `0xb3b82a` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x14E`（334） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | S→C `SC-0xDDF7-battle-weapon_hit_to_r` |

## 2. 结论摘要

- 结论：战斗命中上报（hit_to）：哈希/帧号/武器 + 8 组「计数 + u16 数组」（命中实体、命中点 XYZ、方向、距离、部位）+ 状态标量。
- 字段数：**27**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 8 + 4×3 + 8×(4(计数) + 16×2(上限元素)) + 1 + 2 + 2 + 4 + 1 + 1 = 321 ≤ 容量 0x14E = 334`（上限场景，富余 13）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x770D` | `0xb3b82a` | 确证 |
| 1 | 2 | 8 | u64 | `phash` | 命中哈希（phash） | 来源=入参 arg_0/arg_4（低 32 位在前，两个内联 `mov [eax],esi`/`mov [eax+4],esi`）；服务端据此去重/校验 | - | `0xB3B839, 0xB3B83F` | 确证 |
| 2 | 10 | 4 | u32 | `frame_count` | 帧计数 | 来源=入参 arg_8；内联 `mov [edx],ecx`；服务端据此同步时序 | - | `0xB3B851` | 确证 |
| 3 | 14 | 4 | u32 | `weapon_itemid` | 武器道具 id | 来源=入参 arg_C；写线原语 `sub_B02D80` | - | `0xB3B861` | 确证 |
| 4 | 18 | 4 | u32 | `fire_id` | 开火序号 | 来源=入参 arg_10；写线原语 `sub_B02D80` | - | `0xB3B87B` | 确证 |
| 5 | 22 | 4 | u32 | `ent_ids_num` | ent_ids 元素个数 | 来源=入参 arg_18（`mov ebp,[esp+..+arg_18]; cmp ebp,10h; ja 出错`@0xB3B88F，上限 **16**）；写线原语 `sub_B02D80` | 0..16 | `0xB3B8A2` | 确证 |
| 6 | 26 | var | array<u16,N> | `ent_ids` | 命中实体 id 列表 | 来源=入参 arg_14（数组首址，逐元素 `add edi,2` 步进）；写线原语 `sub_B02DA0`(u16) × N | 元素线长 2，N ≤ 16 | `0xB3B8C6 (loop @0xB3B8C0..0xB3B8DE)` | 确证 |
| 7 | var | 4 | u32 | `hit_pos_x_num` | hit_pos_x 元素个数 | 来源=入参 arg_20（上限 16 @0xB3B8E4）；`sub_B02D80` | 0..16 | `0xB3B8F7` | 确证 |
| 8 | var | var | array<u16,N> | `hit_pos_x` | 命中点 X 坐标列表 | 来源=入参 arg_1C（元素步进 2）；`sub_B02DA0` × N | 元素线长 2，N ≤ 16 | `0xB3B917 (loop @0xB3B911..0xB3B92F)` | 确证 |
| 9 | var | 4 | u32 | `hit_pos_y_num` | hit_pos_y 元素个数 | 来源=入参 arg_28（上限 16 @0xB3B935）；`sub_B02D80` | 0..16 | `0xB3B94B` | 确证 |
| 10 | var | var | array<u16,N> | `hit_pos_y` | 命中点 Y 坐标列表 | 来源=入参 arg_24；`sub_B02DA0` × N | 元素线长 2，N ≤ 16 | `0xB3B96B (loop @0xB3B965..0xB3B985)` | 确证 |
| 11 | var | 4 | u32 | `hit_pos_z_num` | hit_pos_z 元素个数 | 来源=入参 arg_30（上限 16 @0xB3B98E）；`sub_B02D80` | 0..16 | `0xB3B9A4` | 确证 |
| 12 | var | var | array<u16,N> | `hit_pos_z` | 命中点 Z 坐标列表 | 来源=入参 arg_2C；`sub_B02DA0` × N | 元素线长 2，N ≤ 16 | `0xB3B9C7 (loop @0xB3B9C1..0xB3B9E4)` | 确证 |
| 13 | var | 4 | u32 | `hit_dirs_num` | hit_dirs 元素个数 | 来源=入参 arg_38（上限 16 @0xB3B9ED）；`sub_B02D80` | 0..16 | `0xB3BA03` | 确证 |
| 14 | var | var | array<u16,N> | `hit_dirs` | 命中方向列表 | 来源=入参 arg_34；`sub_B02DA0` × N | 元素线长 2，N ≤ 16 | `0xB3BA26 (loop @0xB3BA20..0xB3BA43)` | 确证 |
| 15 | var | 4 | u32 | `hit_distance_num` | hit_distance 元素个数 | 来源=入参 arg_40（上限 16 @0xB3BA4C）；`sub_B02D80` | 0..16 | `0xB3BA62` | 确证 |
| 16 | var | var | array<u16,N> | `hit_distance` | 命中距离列表 | 来源=入参 arg_3C；`sub_B02DA0` × N（打印器 `sub_B03420`，与其它数组打印器不同，仅显示格式不同） | 元素线长 2，N ≤ 16 | `0xB3BA86 (loop @0xB3BA80..0xB3BAA3)` | 确证 |
| 17 | var | 4 | u32 | `body_distance_num` | body_distance 元素个数 | 来源=入参 arg_48（上限 16 @0xB3BAAC）；`sub_B02D80` | 0..16 | `0xB3BAC2` | 确证 |
| 18 | var | var | array<u16,N> | `body_distance` | 部位距离列表 | 来源=入参 arg_44；`sub_B02DA0` × N | 元素线长 2，N ≤ 16 | `0xB3BAE6 (loop @0xB3BAE0..0xB3BB03)` | 确证 |
| 19 | var | 4 | u32 | `body_regions_num` | body_regions 元素个数 | 来源=入参 arg_50（上限 16 @0xB3BB0C）；`sub_B02D80` | 0..16 | `0xB3BB22` | 确证 |
| 20 | var | var | array<u16,N> | `body_regions` | 命中部位列表 | 来源=入参 arg_4C；`sub_B02DA0` × N | 元素线长 2，N ≤ 16 | `0xB3BB46 (loop @0xB3BB40..0xB3BB63)` | 确证 |
| 21 | var | 1 | u8 | `charge_lv` | 蓄力等级 | 来源=入参 arg_54；写线原语 `sub_B061C0`(u8) | - | `0xB3BB72` | 确证 |
| 22 | var | 2 | u16 | `AI_ent_id` | AI 实体 id | 来源=入参 arg_58；写线原语 `sub_B02DA0`(u16) | - | `0xB3BB8F` | 确证 |
| 23 | var | 2 | u16 | `instate_from_ent_id` | 状态来源实体 id | 来源=入参 arg_5C；写线原语 `sub_B02DA0`(u16) | - | `0xB3BBAC` | 确证 |
| 24 | var | 4 | u32 | `create_frame_count` | 生成帧计数 | 来源=入参 arg_60；写线原语 `sub_B02D80`(u32) | - | `0xB3BBC9` | 确证 |
| 25 | var | 1 | u8 | `is_down_range` | 是否进入倒地射程 | 来源=入参 arg_64；写线原语 `sub_B061C0`(u8) | 0/1 | `0xB3BBE6` | 确证 |
| 26 | var | 1 | u8 | `is_wrestle_first_high_lockon` | 是否格斗首次高位锁定 | 来源=入参 arg_68；写线原语 `sub_B061C0`(u8) | 0/1 | `0xB3BC03` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xb3b7ea`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xb3b82a`（`mov word ptr [...], 0x770D`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2 + 8 + 4×3 + 8×(4(计数) + 16×2(上限元素)) + 1 + 2 + 2 + 4 + 1 + 1 = 321 ≤ 容量 0x14E = 334`（上限场景，富余 13）

### 4.3 存疑点
- 8 组「计数 + u16 数组」的计数均为 u32 且上限 **16**（`cmp <reg>,10h; ja 出错`），元素线长 **2**；偏移在首个数组之后为变长 ⇒ `fields.csv` 偏移列记 `var`（不编造偏移）。
- `hit_distance` / `body_distance` 的元素打印器为 `sub_B03420`，其余数组为 `sub_B032A0` —— **仅打印格式不同，线上宽度同为 u16**（写线原语均为 `sub_B02DA0`）。
- 容量 0x14E 为上限场景（8 组数组各取 16 元素），Σ 线长 321 ≤ 334。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
