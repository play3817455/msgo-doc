# SC-0x9F9B-lounge-season_rankerbattle_get_entitled_pilot_list_r

> 状态：`DONE`（2026-09-20，批次-11）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x9F9B` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `season_rankerbattle_get_entitled_pilot_list_r` |
| 处理块范围 | `0xb6eec0`..`0xb6f1d1` |
| 名字串引用点 | `0xb6f042` |
| 声明容量（解码缓冲） | `0x3B72`（`B6EED9`） |
| 长度闭合点 | `B6EFF9` |
| 报错码 | `0x259`（块内 `push 1; push <errcode>; vt[0x64]`） |
| 去向 | `vt[0x5AC]` @`B6F19D`（4 实参） |

## 2. 结论摘要

- **报文体线长**：**`18 + 73N`**（N ≤ 200）。
- 容量关系：容量 `0x3B72` = 15218 = `4 + 10 + 4 + 200×76`（**上限场景线长**）。
- 长度闭合：块末 `B6EFF9` 处校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**4**（不含 opcode）；去向：`vt[0x5AC]` @`B6F19D`（4 实参）。
- 类型：定长头 + 定长结构体 + 计数数组。
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0x9F9B` | `0xb6f042` | 确证 |
| 1 | 0 | 4 | u32 | `result` | 结果码（日志串 `result=`） | 经 `vt[0x5AC]` 交业务 | - | `B6EF1A`、`B6F098` | 确证 |
| 2 | 4 | 10 | struct | `ranking_info` | 排行检索条件（日志串 `order=`；5 × u16，无线上计数） | 经 `vt[0x5AC]` 交业务 | - | `B6EF4B`、`B6EF5A`、`B6F0C0` | 确证 |
| 3 | 14 | 4 | u32 | `ranking_cnt` | 排行条目数（上界 `cmp ebx,0C8h` @`B6EF9C` ⇒ ≤200） | 驱动元素循环 | 0..200 | `B6EF70` | 确证 |
| 4 | 18 | 73N | array<struct,N> | `ranking` | 排行列表（日志 `ranking={score,pilot_id,name,troops,...}`） | 经 `vt[0x5AC]` 交业务 | N ≤ 200 | `B6EFAE`、`B6EFCB`、`B6F0DD` | 确证 |
| - | - | - | - | （长度闭合） | 游标必须 == 报文末尾 | - | - | `B6EFF9` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb6f042` 落在处理块 `0xb6eec0`..`0xb6f1d1` 内。
2. 容量经「`mov edx,[eax+78h]`（解码缓冲分配器）+ `push IMM; call edx`」在 `B6EED9` 确证为 `0x3B72`。
3. 逐字段按线序读取，类型全部由汇编判定（SOP §6）。
4. 闭合：`B6EFF9`（SOP §5.3）。
5. 去向：`vt[0x5AC]` @`B6F19D`（4 实参）。

### 4.2 长度闭合与容量口径
- 容量 = `4`（`result`）+ `10`（`ranking_info` 定长结构体，`sub_B41220` 一次推进 `0x0A`）+ `4`（`ranking_cnt`）+ `200`（`cmp ebx,0C8h` @`B6EF9C`）× `76`（`sub_B41A60` 槽步进 `add [edx],4Ch`）= **15218** ✓。
- 元素由 `sub_B469F0` 读 = `73B`（= `4+4+25+1+4+4+31`）⇒ 线长 `18 + 73N`。

### 4.3 结构/数组说明
- `ranking_info`（无线上计数，固定 10B）= 5 × `u16`（`sub_B46420` @`B46420..B46492`）；打印器 `sub_B4F620` 成员名 `kind`、`term`、`filter`、`reason`、`troops`。
- `ranking` 元素线序（`sub_B469F0`）：`u32` + `u32` + `u8×25` + `u8` + `u32` + `u32` + `u8×31` = **73B**。
- 元素打印器 `sub_B501C0`：`score`、`pilot_id`、`name`、`troops`、`world_id`、`season_class_lv`、`clan_name`。

### 4.4 存疑点
见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与客户端长度闭合一致（或已说明为何无法闭合）
- [x] G2 每个字段的线类型都能指回汇编证据 VA，未使用伪代码类型
- [x] G3 每个字段都有含义与用途（或明确标注仅回显/仅日志并给证据）
- [x] G4 不确定项全部显式标 `?` 且已记入 `notes.md`
- [x] G5 `README.md` / `fields.csv` / `asm.md` 三处一致
- [x] G6 INDEX 该行状态与文件夹内容一致（`DONE`）
- [x] G7 有配对请求/应答的命令已互相链接
