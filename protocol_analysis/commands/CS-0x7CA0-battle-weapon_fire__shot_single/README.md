# CS-0x7CA0-battle-weapon_fire__shot_single

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x7CA0` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__shot_single` |
| 名字符串 | `)<-_proto_battle_client::send_weapon_fire__shot_single(` @ `0xee0c60` |
| 代码位置 | sub_B364E0 @ `0xb364e0`（`0xb364e0`..`0xb368a7`） |
| opcode 写入证据 | `0xb3655c` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x26`（38） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | S→C `SC-0x4E9F-battle-weapon_fire__shot_single_special_r`（已 DONE，同族特殊弹） |

## 2. 结论摘要

- 结论：单发射击开火上报：帧号 + 目标点 + 剩余弹药 + 蓄力/AI/齐射槽。
- 字段数：**10**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 4 + 2×5 + 1 + 2 + 1 = 20 ≤ 容量 0x26 = 38`（富余 18）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x7CA0` | `0xb3655c` | 确证 |
| 1 | 2 | 4 | u32 | `frame_count` | 帧计数 | 来源=入参 arg_0；内联 `mov [ecx],eax`；服务端据此同步时序 | - | `0xB3656C` | 确证 |
| 2 | 6 | 2 | u16 | `target_x` | 目标点 X | 来源=入参 arg_4；内联 `mov [edx],ax` | - | `0xB36586` | 确证 |
| 3 | 8 | 2 | u16 | `target_y` | 目标点 Y | 来源=入参 arg_8；`sub_B02DA0` | - | `0xB3658F` | 确证 |
| 4 | 10 | 2 | u16 | `target_z` | 目标点 Z | 来源=入参 arg_C；`sub_B02DA0` | - | `0xB365A9` | 确证 |
| 5 | 12 | 2 | u16 | `rcnt_bullet_mgz` | 弹匣内剩余弹数 | 来源=入参 arg_10；`sub_B02DA0` | - | `0xB365C3` | 确证 |
| 6 | 14 | 2 | u16 | `rcnt_bullet_all` | 总剩余弹数 | 来源=入参 arg_14；`sub_B02DA0` | - | `0xB365DD` | 确证 |
| 7 | 16 | 1 | u8 | `charge_lv` | 蓄力等级 | 来源=入参 arg_18；`sub_B061C0`(u8) | - | `0xB365F7` | 确证 |
| 8 | 17 | 2 | u16 | `AI_ent_id` | AI 实体 id | 来源=入参 arg_1C；`sub_B02DA0` | - | `0xB36611` | 确证 |
| 9 | 19 | 1 | u8 | `salvo_slot` | 齐射槽位 | 来源=入参 arg_20；`sub_B061C0`(u8) | - | `0xB3662B` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xb36526`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xb3655c`（`mov word ptr [...], 0x7CA0`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2 + 4 + 2×5 + 1 + 2 + 1 = 20 ≤ 容量 0x26 = 38`（富余 18）

### 4.3 存疑点
- 坐标点为 u16（写线原语 `sub_B02DA0`）。容量 0x26 富余 18。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
