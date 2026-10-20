# SC-0xD52A-lounge-xwar_booking_regist_r

> 状态：`DONE`（2026-09-20，批次-14）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xD52A` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `xwar_booking_regist_r` |
| 处理块范围 | `0xb7d3a2`..`0xb7d7ff` |
| 名字串引用点 | `0xee65dc` |
| 声明容量（解码缓冲） | `0x19`（`B7D3BE`） |
| 长度闭合点 | `B7D55D`（`cmp`）→ `jz` |
| 报错码 | `0xA8`（块内 `push 1; push 0A8h; vt[0x64]`） |
| 去向 | `vt[0x1E4]` @`B7D7E3`（9 实参） |

## 2. 结论摘要

- **报文体线长**：25
- 容量关系：`0x19` = 25 = `4+4+1+4+4+4+1+2+1`（逐字段 claim 精确相等）
- 长度闭合：块末 `B7D55D`（`cmp ebx,[var_2C40]`）＋ `B7D55F+ jz short loc_B7D57F` 校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**9**（不含 opcode）；去向：`vt[0x1E4]` @`B7D7E3`（9 实参）
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0xD52A` | `0xb7d5a6` | 确证 |
| 1 | 0 | 4 | u32 | result | 报名结果码（日志串 `result=`） | `vt[0x1E4]` 第 1 实参 | - | 0xb7d3f9|0xb7d5fc | 确证 |
| 2 | 4 | 4 | u32 | matching_type | 匹配类型（日志串 `matching_type=`） | `vt[0x1E4]` 第 2 实参 | - | 0xb7d439|0xb7d626 | 确证 |
| 3 | 8 | 1 | u8 | is_newbie | 是否新手匹配（日志串 `is_newbie=`） | `vt[0x1E4]` 第 3 实参 | 0/1 | 0xb7d45d|0xb7d64e | 确证 |
| 4 | 9 | 4 | u32 | matching_request_flag | 匹配请求标志（日志串 `matching_request_flag=`） | `vt[0x1E4]` 第 4 实参 | - | 0xb7d481|0xb7d67a | 确证 |
| 5 | 13 | 4 | u32 | matching_battlerule_flag | 匹配对战规则标志（日志串 `matching_battlerule_flag=`） | `vt[0x1E4]` 第 5 实参 | - | 0xb7d4a9|0xb7d6a4 | 确证 |
| 6 | 17 | 4 | u32 | matching_extrule_flag | 匹配额外规则标志（日志串 `matching_extrule_flag=`） | `vt[0x1E4]` 第 6 实参 | - | 0xb7d4d1|0xb7d6ce | 确证 |
| 7 | 21 | 1 | u8 | is_party_wait | 是否队伍等待中（日志串 `is_party_wait=`） | `vt[0x1E4]` 第 7 实参 | 0/1 | 0xb7d4f9|0xb7d6f6 | 确证 |
| 8 | 22 | 2 | u16 | party_wait_sec | 队伍等待秒数（日志串 `party_wait_sec=`） | `vt[0x1E4]` 第 8 实参 | - | 0xb7d521|0xb7d723 | 确证 |
| 9 | 24 | 1 | u8 | is_party_readyNG | 队伍是否未就绪 NG（日志串 `is_party_readyNG=`） | `vt[0x1E4]` 第 9 实参 | 0/1 | 0xb7d549|0xb7d746 | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb7d5a6` 落在处理块 `0xb7d3a2`..`0xb7d7ff` 内。
2. 容量经分配器指纹在 `B7D3BE` 确证为 `0x19`。
3. 9 个字段按线序读取（5×`sub_B41470` u32、3×`sub_B05E30` u8、1×`sub_B413B0` u16 预留），类型由汇编判定（SOP §6）；日志名与字段按打印顺序一一对位。
4. 闭合：`B7D55D`+`B7D57F`（SOP §5.3）。去向：`vt[0x1E4]` @`B7D7E3`（9 实参，实参顺序已按 `push` 序列清点）。

### 4.2 长度闭合与容量口径
- 容量关系：`0x19` = 25 = `4+4+1+4+4+4+1+2+1`（逐字段 claim 精确相等）
- 线长：25

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
