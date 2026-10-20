# SC-0xE13A-lounge-pilot_list_get_r

> 状态：`DONE`（2026-09-20，批次-14）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xE13A` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_list_get_r` |
| 处理块范围 | `0xb825ef`..`0xb82def` |
| 名字串引用点 | `0xee70a8` |
| 声明容量（解码缓冲） | `0x501`（`B82604`） |
| 长度闭合点 | `B82991`（`cmp`）→ `B82997 jz` |
| 报错码 | `0x0E`（块内 10 处 `push 1; push 0Eh; vt[0x64]`） |
| 去向 | `vt[0x84]` @`B82DD3`（16 实参） |

## 2. 结论摘要

- **报文体线长**：`4 + 398 + 398 + 4×5 + 4 + 23n + 1 + 4×5`（n ≤ 16）
- 容量关系：`0x501` = 1281 = `4 + 424 + 424 + 5×4 + 4 + 16×24 + 1 + 5×4`（**逐项精确相等**）
- 长度闭合：块末 `B82991`（`cmp ecx,[var_2C40]`）＋ `B82997 jz` 校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**16**（不含 opcode）；去向：`vt[0x84]` @`B82DD3`（16 实参）
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0xE13A` | `0xb829d4` | 确证 |
| 1 | 0 | 4 | u32 | result | 取得结果码（日志串 `result=`） | 经 `vt[0x84]` 交业务 | - | 0xb82642|0xb82a2a | 确证 |
| 2 | 4 | 398 | struct<pilots_list> | pilots_eff | 地球联邦侧飞行员列表结构（**固定 1 元**；日志串 `pilots_eff={`；claim 0x1A8=424；打印器 `sub_B48C10`） | 经 `vt[0x84]` 交业务；内部成员未逐一命名（见 `notes.md`） | - | 0xb82670|0xb82686|0xb8269b|0xb82a45 | 确证 |
| 3 | 402 | 398 | struct<pilots_list> | pilots_zeon | 吉翁侧飞行员列表结构（**固定 1 元**；日志串 `pilots_zeon={`；claim 0x1A8=424） | 经 `vt[0x84]` 交业务；内部成员未逐一命名 | - | 0xb826b8|0xb826c9|0xb826de|0xb82a77 | 确证 |
| 4 | 800 | 4 | u32 | del_remain_sec_eff | 联邦侧删除剩余秒数（**固定 1 元数组**；日志串 `del_remain_sec_eff={`） | 经 `vt[0x84]` 交业务 | - | 0xb826fb|0xb8270c|0xb82aa9 | 确证 |
| 5 | 804 | 4 | u32 | del_remain_sec_zeon | 吉翁侧删除剩余秒数（固定 1 元数组；日志串 `del_remain_sec_zeon={`） | 经 `vt[0x84]` 交业务 | - | 0xb8273b|0xb8274c|0xb82ade | 确证 |
| 6 | 808 | 4 | u32 | pilot_rename_remaintime_eff | 联邦侧改名剩余时间（固定 1 元数组；日志串 `pilot_rename_remaintime_eff={`） | 经 `vt[0x84]` 交业务 | - | 0xb8277b|0xb8278c|0xb82b13 | 确证 |
| 7 | 812 | 4 | u32 | pilot_rename_remaintime_zeon | 吉翁侧改名剩余时间（固定 1 元数组；日志串 `pilot_rename_remaintime_zeon={`） | 经 `vt[0x84]` 交业务 | - | 0xb827bb|0xb827cc|0xb82b48 | 确证 |
| 8 | 816 | 4 | u32 | charge_point | 充值点数（日志串 `charge_point=`） | 经 `vt[0x84]` 交业务 | - | 0xb82809|0xb82b8c | 确证 |
| 9 | 820 | 4 | u32 | bmgpack_num | BGM 包条数（上限 16，`cmp ebx,10h; ja`@`B8284C`） | 驱动 `bmgpack_list` 数组循环（`cmp edi,ebx`@`B82894`） | 0..16 | 0xb82838|0xb8284c|0xb82894 | 确证 |
| 10 | 824 | 23n | array<bmgpack,16> | bmgpack_list | BGM 包列表（日志串 `bmgpack_list={`） | 经 `vt[0x84]` 交业务；元素线长 **23**（复合读取器 `sub_B458A0`）≠ 槽步进 **24**（`sub_B416C0`） | - | 0xb8285f|0xb82880|0xb82894 | 确证 |
| 11 | var | 1 | u8 | is_tutorial_end | 教程是否结束（日志串 `is_tutorial_end=`） | 经 `vt[0x84]` 交业务 | 0/1 | 0xb828bd|0xb82c39 | 确证 |
| 12 | var | 4 | u32 | pilot_rename_price | 改名价格（日志串 `pilot_rename_price=`） | 经 `vt[0x84]` 交业务 | - | 0xb828df|0xb82c68 | 确证 |
| 13 | var | 4 | u32 | pilot_rename_time_efsf | 联邦侧改名时长（日志串 `pilot_rename_time_efsf=`） | 经 `vt[0x84]` 交业务 | - | 0xb82905|0xb82c95 | 确证 |
| 14 | var | 4 | u32 | pilot_rename_forbidtime_efsf | 联邦侧改名冷却（日志串 `pilot_rename_forbidtime_efsf=`） | 经 `vt[0x84]` 交业务 | - | 0xb8292d|0xb82cbf | 确证 |
| 15 | var | 4 | u32 | pilot_rename_time_zeon | 吉翁侧改名时长（日志串 `pilot_rename_time_zeon=`） | 经 `vt[0x84]` 交业务 | - | 0xb82955|0xb82ce9 | 确证 |
| 16 | var | 4 | u32 | pilot_rename_forbidtime_zeon | 吉翁侧改名冷却（日志串 `pilot_rename_forbidtime_zeon=`） | 经 `vt[0x84]` 交业务 | - | 0xb8297d|0xb82d0e | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb829d4` 落在处理块 `0xb825ef`..`0xb82def`（641 条指令）内。
2. 容量经分配器指纹在 `B82604` 确证为 `0x501`。
3. 字段序：`result`(u32) → `pilots_eff`(复合) → `pilots_zeon`(复合) → 5×u32 → `bmgpack_num`(u32, ≤16) → `bmgpack_list`(复合) → `is_tutorial_end`(u8) → 5×u32。
4. ★**容量逐项反推**确认全部字段与上限（16）；两个 `pilots_*` 为**固定 1 元**（循环 `cmp edi,1; jb`）。
5. 闭合：`B82991`（SOP §5.3）。去向：`vt[0x84]` @`B82DD3`（16 实参）。

### 4.2 长度闭合与容量口径
- 容量关系：`0x501` = 1281 = `4 + 424 + 424 + 5×4 + 4 + 16×24 + 1 + 5×4`（**逐项精确相等**）
- 线长：`4 + 398 + 398 + 4×5 + 4 + 23n + 1 + 4×5`（n ≤ 16）

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
