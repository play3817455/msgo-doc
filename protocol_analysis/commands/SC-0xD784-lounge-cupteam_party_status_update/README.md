# SC-0xD784-lounge-cupteam_party_status_update

> 状态：`DONE`（2026-09-20，批次-14）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xD784` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `cupteam_party_status_update` |
| 处理块范围 | `0xb7f219`..`0xb7f4aa` |
| 名字串引用点 | `0xee67f8` |
| 声明容量（解码缓冲） | `0x4C`（`B7F22D`） |
| 长度闭合点 | `B7F30C`（`cmp`）→ `B7F312 jz` |
| 报错码 | `0x20F`（块内 `push 1; push 20Fh; vt[0x64]`） |
| 去向 | `vt[0x4F8]` @`B7F48E`（4 实参） |

## 2. 结论摘要

- **报文体线长**：`4 + 4 + 13 + 46`
- 容量关系：`0x4C` = 76 = `4(cupteam_rate) + 4(last_bracket_id) + 16(phase claim) + 52(bracket claim)`（精确相等）
- 长度闭合：块末 `B7F30C`（`cmp ebx,[var_2C40]`）＋ `B7F312 jz` 校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**4**（不含 opcode）；去向：`vt[0x4F8]` @`B7F48E`（4 实参）
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0xD784` | `0xb7f355` | 确证 |
| 1 | 0 | 4 | u32 | cupteam_rate | 杯赛队伍胜率（日志串 `cupteam_rate=`） | 经 `vt[0x4F8]` 交业务 | - | 0xb7f270|0xb7f3ab | 确证 |
| 2 | 4 | 4 | u32 | last_bracket_id | 最近括号组 ID（日志串 `last_bracket_id=`） | 经 `vt[0x4F8]` 交业务 | - | 0xb7f2b0|0xb7f3d5 | 确证 |
| 3 | 8 | 13 | struct<phase_info> | phase | 赛程阶段信息（日志串 `phase=`；claim 0x10=16） | 经 `vt[0x4F8]` 交业务；内部成员未逐一命名（见 `notes.md`） | - | 0xb7f2c5|0xb7f2d4|0xb7f3fd | 确证 |
| 4 | 21 | 46 | struct<bracket_info> | bracket | 对阵表信息（日志串 `bracket=`；claim 0x34=52） | 经 `vt[0x4F8]` 交业务；内部成员未逐一命名（见 `notes.md`） | - | 0xb7f2e9|0xb7f2f8|0xb7f422 | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb7f355` 落在处理块 `0xb7f219`..`0xb7f4aa` 内。
2. 容量经分配器指纹在 `B7F22D` 确证为 `0x4C`（该值此前被 `push 4Ch ; char` 形式的行尾注释干扰，本批人工读取）。
3. 依次读 2×u32、再由 `sub_B41990`(claim 16)/`sub_B419A0`(claim 52) 预留后由复合读取器消费两个结构。
4. 闭合：`B7F30C`（SOP §5.3）。去向：`vt[0x4F8]` @`B7F48E`（4 实参）。

### 4.2 长度闭合与容量口径
- 容量关系：`0x4C` = 76 = `4(cupteam_rate) + 4(last_bracket_id) + 16(phase claim) + 52(bracket claim)`（精确相等）
- 线长：`4 + 4 + 13 + 46`

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
