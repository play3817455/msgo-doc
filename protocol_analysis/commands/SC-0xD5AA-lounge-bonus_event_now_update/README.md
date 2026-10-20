# SC-0xD5AA-lounge-bonus_event_now_update

> 状态：`DONE`（2026-09-20，批次-14）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xD5AA` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `bonus_event_now_update` |
| 处理块范围 | `0xb7d1d5`..`0xb7d3a2` |
| 名字串引用点 | `0xee663c` |
| 声明容量（解码缓冲） | `0x100`（`B7D1EE`） |
| 长度闭合点 | `B7D277` |
| 报错码 | `0x5C`（块内 `push 1; push 5Ch; vt[0x64]`） |
| 去向 | `vt[0x138]` @`B7D386`（1 实参） |

## 2. 结论摘要

- **报文体线长**：256
- 容量关系：`0x100` = 256 = `4×64`（4 元定长数组，元素 64B；无线上 count）
- 长度闭合：块末 `B7D258`（`cmp ecx,[var_2C40]`）＋ `B7D277 jz` 校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**1**（不含 opcode）；去向：`vt[0x138]` @`B7D386`（1 实参）
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0xD5AA` | `0xb7d29b` | 确证 |
| 1 | 0 | 256 | array<bonus_event,4> | events | 当期加成活动列表（固定 4 元；日志串 `events={`） | 经 `vt[0x138]` 交业务（1 实参，元素指针）；元素成员（元素打印器 `sub_B499F0`，16×u32）：`main_rate`/`main_priority`/`gp_rate`/`reward_rate`/`raredrop_rate`/`accump_rate`/`over_custom_rate`/`gp_offset`/`reward_num`/`accump_offset`/`over_custom_offset`/`buildup_odds_offset`/`bonus_target`/`game_type`/`begin_time`/`end_time` | - | 0xb7d21d|0xb7d22e|0xb7d240|0xb7d2e5 | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb7d29b` 落在处理块 `0xb7d1d5`..`0xb7d3a2` 内。
2. 容量经分配器指纹在 `B7D1EE` 确证为 `0x100`。
3. `sub_B412E0` 一次推进 `0x100`（整块预留）后，复合读取器 `sub_B43360` 逐元素消费 64B，循环上界为**字面量 4**（`cmp edi,4; jb`@`B7D240`）⇒ 定长 4 元、无线上 count。
4. 闭合：`B7D258`+`B7D277`（SOP §5.3）。去向：`vt[0x138]` @`B7D386`（1 实参）。

### 4.2 长度闭合与容量口径
- 容量关系：`0x100` = 256 = `4×64`（4 元定长数组，元素 64B；无线上 count）
- 线长：256

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
