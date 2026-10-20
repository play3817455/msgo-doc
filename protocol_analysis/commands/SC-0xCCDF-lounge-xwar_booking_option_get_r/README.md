# SC-0xCCDF-lounge-xwar_booking_option_get_r

> 状态：`DONE`（2026-09-20，批次-13）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xCCDF` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `xwar_booking_option_get_r` |
| 处理块范围 | `0xb7b003`..`0xb7b3bd` |
| 名字串引用点 | `0xb7b1ba` |
| 声明容量（解码缓冲） | `0x22C`（`B7B024`） |
| 长度闭合点 | `B7B171` |
| 报错码 | `0xA4`（块内 `push 1; push <0xA4>; vt[0x64]`） |
| 去向 | `vt[0x1DC]` @`B7B386`（7 实参） |

## 2. 结论摘要

- **报文体线长**：`20 + 20 + 514` = `554`
- 容量关系：`0x22C` = 556 = `5×4 + 20 + 516`（`ext_subrule` claim 20 = `sub_B41740`；`xwar_ext_rule` claim 516 = `sub_B05EE0`）
- 长度闭合：块末 `B7B171` 处校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**7**（不含 opcode）；去向：`vt[0x1DC]` @`B7B386`（7 实参）
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0xCCDF` | `0xb7b1ba` | 确证 |
| 1 | 0 | 4 | u32 | `result` | 结果码（日志串 `result=`） | 经 `vt[0x1DC]`（7 实参）交业务 | - | 0xb7b04e|0xb7b05d | 确证 |
| 2 | 4 | 4 | u32 | `matching_type` | 匹配类型（日志串 `matching_type=`） | 同上 | - | 0xb7b08e|0xb7b09d | 确证 |
| 3 | 8 | 4 | u32 | `matching_request_flag` | 匹配申请标志（日志串 `matching_request_flag=`） | 同上 | - | 0xb7b0b2|0xb7b0c1 | 确证 |
| 4 | 12 | 4 | u32 | `matching_battlerule_flag` | 匹配战斗规则标志（日志串 `matching_battlerule_flag=`） | 同上 | - | 0xb7b0d6|0xb7b0e5 | 确证 |
| 5 | 16 | 4 | u32 | `matching_extrule_flag` | 匹配扩展规则标志（日志串 `matching_extrule_flag=`） | 同上 | - | 0xb7b0fe|0xb7b10d | 确证 |
| 6 | 20 | 20 | struct(20) | `ext_subrule` | 扩展子规则（日志串 `ext_subrule=`；读取器 `sub_B456F0` = 2×u16 + 8×u16 = 20B） | 同上 | - | 0xb7b126|0xb7b135 | 确证 |
| 7 | 40 | 514 | struct(516) | `xwar_ext_rule` | XWar 扩展规则（日志串 `xwar_ext_rule=`；读取器 `sub_B08160` = u16 + 128×u32 = 514B） | 同上 | - | 0xb7b14e|0xb7b15d | 确证 |
| - | - | - | - | （长度闭合） | 游标必须 == 报文末尾 | - | - | `B7B171` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb7b1ba` 落在处理块 `0xb7b003`..`0xb7b3bd` 内。
2. 容量经「`mov edx,[eax+78h]`（解码缓冲分配器）+ `push IMM; call edx`」在 `B7B024` 确证为 `0x22C`。
3. 逐字段按线序读取，类型全部由汇编判定（SOP §6）。
4. 闭合：`B7B171`（SOP §5.3）。
5. 去向：`vt[0x1DC]` @`B7B386`（7 实参）。

### 4.2 长度闭合与容量口径
- 容量关系：`0x22C` = 556 = `5×4 + 20 + 516`（`ext_subrule` claim 20 = `sub_B41740`；`xwar_ext_rule` claim 516 = `sub_B05EE0`）
- 线长：`20 + 20 + 514` = `554`。

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
