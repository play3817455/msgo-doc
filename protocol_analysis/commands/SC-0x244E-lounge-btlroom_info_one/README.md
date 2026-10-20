# SC-0x244E-lounge-btlroom_info_one

> 状态：`DONE`（2026-09-20，批次-6）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x244E` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `btlroom_info_one` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB58B5D..0xB58DE9` |
| 名字串引用点 | `0xB58C95` |
| 声明容量（解码缓冲） | `0xA9`（`0xB58B72`） |
| 长度闭合点 | `0xB58C4C` |
| 去向 | `vt[0x19C]` @ `0xB58DCD`（4 实参） |

## 2. 结论摘要

- **报文体总长**：1 + 135 + 11 + 11 = **158**（容量按槽记 `1 + 144 + 12 + 12 = 169 = 0xA9`）
- 长度闭合：块末 `0xB58C4C` 处校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**25**（不含 opcode）；去向：`vt[0x19C]` @ `0xB58DCD`（4 实参）。
- 是否分帧：否

> **2026-09-24 Oracle 订正**：原记「1 + 95 + 12 + 12 = 120」有两处把**槽宽当线长**——
> `roominfo` 线上 **135**（reader `sub_B44880` 实测整函数消费 135B，`probe_reader` 在 135 闭合、134 拒绝）、
> `clan_eff` / `clan_zeon` 线上 **11**（reader `sub_B45F30` 实测 11 闭合、10 拒绝）。
> 「95B 短形」来自本 README 早期只列到 `is_lock`（漏列后 7 个成员），
> 同族的 `SC-0x6B15` 早就写着 `struct<roominfo>` + 135 ⇒ 这是**单向的漏列**，不是第二个线形；
> 幽灵复合体 `roominfo_short` 已删除。容量 `0xA9=169` 一直是按槽记的（144+12+12+1），未受影响。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0x244E` | `0xB58C95` | 确证 |
| 1 | 0 | 1 | u8 | `is_new` | 是否新建房间 | 经 `vt[0x19C]`；日志 `is_new=` | - | `0xB58BB0`、`0xB58CE9` | 确证 |
| 2 | 1 | 135 | struct<roominfo> | `roominfo` | 对战房间信息结构体（线上 135B；缓冲槽步进 144） | 结构体经 `vt[0x19C]`；日志 `roominfo={…}`（打印器 `sub_B4C0D0`） | 线上 135 / 槽 144 | `0xB58BF0`（读取器 `sub_B44880` 消费 135）、`0xB58BE1`（`sub_B41440` 预留 0x90） | 确证 |
| 3 | +0 | 4 | u32 | `roominfo.room_id` | 房间 ID | 结构成员；打印器 `room_id=` | - | `sub_B44880` 首读、`sub_B4C0D0`[+0] | 确证 |
| 4 | +4 | 73 | bytes[73] | `roominfo.room_name` | 房间名（定长 73B） | 结构成员；打印器 `room_name=` | - | `sub_B44880`（循环 73）、`sub_B4C0D0`[+4] | 确证 |
| 5 | +0x50 | 4 | u32 | `roominfo.room_type` | 房间类型 | 结构成员；打印器 `room_type=` | - | `sub_B44880`、`sub_B4C0D0`[+50h] | 确证 |
| 6 | +0x54 | 1 | i8 | `roominfo.room_stat` | 房间状态 | 结构成员；打印器 `room_stat=`（`movsx`） | - | `sub_B44880`、`sub_B4C0D0`[+54h] | 确证 |
| 7 | +0x58 | 4 | u32 | `roominfo.play_elapsed` | 已进行时间 | 结构成员；打印器 `play_elapsed=` | - | `sub_B44880`、`sub_B4C0D0`[+58h] | 确证 |
| 8 | +0x5C | 4 | u32 | `roominfo.mission_id` | 任务 ID | 结构成员；打印器 `mission_id=` | - | `sub_B44880`、`sub_B4C0D0`[+5Ch] | 确证 |
| 9 | +0x60 | 4 | u32 | `roominfo.extrule_id` | 扩展规则 ID | 结构成员；打印器 `extrule_id=` | - | `sub_B44880`、`sub_B4C0D0`[+60h] | 确证 |
| 10 | +0x64 | 1 | i8 | `roominfo.is_lock` | 是否上锁 | 结构成员；打印器 `is_lock=`（`movsx`） | - | `sub_B44880`、`sub_B4C0D0`[+64h] | 确证 |
| 11 | +0x65 | 1 | i8 | `roominfo.is_vsclan` | 是否部队对战房间 | 结构成员；打印器 `is_vsclan=` | - | `sub_B44880`、`sub_B4C0D0`[+65h] | 确证 |
| 12 | +0x66 | 2 | u16 | `roominfo.count_eff` | 联邦侧人数 | 结构成员；打印器 `count_eff=` | - | `sub_B44880`、`sub_B4C0D0`[+66h] | 确证 |
| 13 | +0x68 | 2 | u16 | `roominfo.count_zeon` | 吉翁侧人数 | 结构成员；打印器 `count_zeon=` | - | `sub_B44880`、`sub_B4C0D0`[+68h] | 确证 |
| 14 | +0x6A | 2 | u16 | `roominfo.count_max` | 房间人数上限 | 结构成员；打印器 `count_max=` | - | `sub_B44880`、`sub_B4C0D0`[+6Ah] | 确证 |
| 15 | +0x6C | 4 | u32 | `roominfo.master_pilotid` | 房主 pilot ID | 结构成员；打印器 `master_pilotid=` | - | `sub_B44880`、`sub_B4C0D0`[+6Ch] | 确证 |
| 16 | +0x70 | 4 | u32 | `roominfo.master_worldid` | 房主 world ID | 结构成员；打印器 `master_worldid=` | - | `sub_B44880`、`sub_B4C0D0`[+70h] | 确证 |
| 17 | +0x74 | 25 | bytes[25] | `roominfo.master_name` | 房主名称（定长 25B） | 结构成员；打印器 `master_name=` | - | `sub_B44880`（循环 25）、`sub_B4C0D0`[+74h] | 确证 |
| 18 | 数组后 | 11 | struct<clan_eff> | `clan_eff` | 联邦侧战队编成信息（线上 11B / 槽 12） | 结构体经 `vt[0x19C]`；日志 `clan_eff=`（打印器 `sub_B4EC50`） | 槽 12 | `0xB58C14`（读取器 `sub_B45F30` 消费 11）、`0xB58C05`（`sub_B41460` 预留 0x0C） | 确证 |
| 19 | 数组后 | 11 | struct<clan_zeon> | `clan_zeon` | 吉翁侧战队编成信息（线上 11B / 槽 12） | 结构体经 `vt[0x19C]`；日志 `clan_zeon=`（打印器 `sub_B4EC50`） | 槽 12 | `0xB58C38`（`sub_B45F30` 消费 11）、`0xB58C29`（`sub_B41460`） | 确证 |
| 20 | clan 成员 | 4 | u32 | `clan_*.clan_id` | 战队 ID | 结构成员；打印器 `clan_id=` | - | `sub_B4EC50`[+0] | 确证 |
| 21 | clan 成员 | 4 | u32 | `clan_*.world_id` | 所属大区 ID | 结构成员；打印器 `world_id=` | - | `sub_B4EC50`[+4] | 确证 |
| 22 | clan 成员 | 1 | i8 | `clan_*.emb_base` | 徽章底色 | 结构成员；打印器 `emb_base=` | - | `sub_B4EC50`[+8] | 确证 |
| 23 | clan 成员 | 1 | i8 | `clan_*.emb_parts1` | 徽章部件 1 | 结构成员；打印器 `emb_parts1=` | - | `sub_B4EC50`[+9] | 确证 |
| 24 | clan 成员 | 1 | i8 | `clan_*.emb_parts2` | 徽章部件 2 | 结构成员；打印器 `emb_parts2=` | - | `sub_B4EC50`[+0Ah] | 确证 |
| 25 | 槽尾 | 1 | - | `clan_*.slot_pad` | 槽内第 12 字节（**仅内存对齐余量，不在线上**） | 槽 12 的自然对齐余量 | - | `sub_B45F30` 消费 11B 即停、槽步进 0x0C | 推测 |
| - | - | 0 | - | （长度闭合） | 游标必须 == 报文末尾 | 1 + 135 + 11 + 11 = **158**（容量按槽记 `1 + 144 + 12 + 12 = 169 = 0xA9`） | - | `0xB58C4C` | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB58C95` 落在处理块 `0xB58B5D..0xB58DE9`。
2. 容量经「`mov edx,[eax+78h]`（分配器）+ `push IMM; call edx`」在 `0xB58B72` 确证为 `0xA9`。
3. 逐字段按线序读取（读取器原语 / 内联读取器 / 复合读取器），字段类型由汇编判定（SOP §6）。
4. 闭合：`0xB58C4C`。
5. 去向：`vt[0x19C]` @ `0xB58DCD`（4 实参）。

### 4.2 长度闭合
- 1 + 135 + 11 + 11 = **158**（容量按槽记 `1 + 144 + 12 + 12 = 169 = 0xA9`）
- 闭合点 `0xB58C4C` 要求「游标 == 报文末尾」✓

### 4.3 存疑点
见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与客户端长度闭合一致（或已说明为何无法闭合）
- [x] G2 每个字段的线类型都能指回汇编证据 VA，未使用伪代码类型
- [x] G3 每个字段都有含义与用途（或明确标注仅回显/仅日志并给证据）
- [x] G4 不确定项全部显式标 `?` 且已记入 `notes.md`
- [x] G5 `README.md` / `fields.csv` / `asm.md` 三处一致
- [x] G6 INDEX 该行状态与文件夹内容一致（`DONE`）
- [x] G7 有配对请求/应答的命令已互相链接
