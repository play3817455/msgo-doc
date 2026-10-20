# SC-0xDCF2-battle-roomlobby_pilot_msdeck

> 状态：`DONE`（2026-09-20，批次-14）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xDCF2` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `battle_client` |
| 命令名 | `roomlobby_pilot_msdeck` |
| 处理块范围 | `0xb2cbf8`..`0xb2cff8` |
| 名字串引用点 | `0xee6c00` |
| 声明容量（解码缓冲） | `0x24`（`B2CC11`） |
| 长度闭合点 | `B2CD98`（`cmp`）→ `B2CD9E jz` |
| 报错码 | `0x7`（块内 5 处 `push 1; push 7; vt[0x64]`） |
| 去向 | `vt[0x80]` @`B2CFB0`（6 实参） |

## 2. 结论摘要

- **报文体线长**：`12 + 4n + 4m`（n,m ≤ 4）
- 容量关系：`0x24` = 36 = `4+4+4+4×4+4+1×4`（两个数组各取上限 4）
- 长度闭合：块末 `B2CD98`（`cmp ecx,[var_1B24]`）＋ `B2CD9E jz` 校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**6**（不含 opcode）；去向：`vt[0x80]` @`B2CFB0`（6 实参）
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0xDCF2` | `0xb2cddb` | 确证 |
| 1 | 0 | 4 | u32 | world_id | 大区 ID（日志串 `world_id=`） | 经 `vt[0x80]` 交业务 | - | 0xb2cc4c|0xb2ce31 | 确证 |
| 2 | 4 | 4 | u32 | pilot_id | 飞行员 ID（日志串 `pilot_id=`） | 经 `vt[0x80]` 交业务 | - | 0xb2cc89|0xb2ce5b | 确证 |
| 3 | 8 | 4 | u32 | deck_msid_num | 编成机体条数（上限 4，`cmp ebx,4; ja`@`B2CCC8`） | 驱动 `deck_msid` 数组循环 | 0..4 | 0xb2cc9f|0xb2ccc8|0xb2cd10 | 确证 |
| 4 | 12 | 4n | array<u32,4> | deck_msid | 编成机体 ID 列表（日志串 `deck_msid={`） | 经 `vt[0x80]` 交业务；槽步进 4 = `sub_B41850`（`add dword ptr [edx],4`） | - | 0xb2ccda|0xb2ccfa|0xb2cd10 | 确证 |
| 5 | var | 4 | u32 | deck_mscolor_num | 编成配色条数（上限 4，`cmp …,4; ja`@`B2CD3B`） | 驱动 `deck_mscolor` 数组循环 | 0..4 | 0xb2cd2b|0xb2cd3b|0xb2cd7f | 确证 |
| 6 | var | 1m | array<u8,4> | deck_mscolor | 编成配色列表（日志串 `deck_mscolor={`） | 经 `vt[0x80]` 交业务；槽步进 1 = `sub_B05EA0`（`add dword ptr [edx],1`） | - | 0xb2cd57|0xb2cd70|0xb2cd7f | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb2cddb` 落在处理块 `0xb2cbf8`..`0xb2cff8` 内。
2. 容量经分配器指纹在 `B2CC11` 确证为 `0x24`。
3. 依次读 `world_id`(u32)、`pilot_id`(u32)、`deck_msid_num`(u32 ≤4) + `deck_msid`(u32 数组，槽步进 4)、`deck_mscolor_num`(u32 ≤4) + `deck_mscolor`(u8 数组，槽步进 1)。
4. 闭合：`B2CD98`（SOP §5.3）。去向：`vt[0x80]` @`B2CFB0`（6 实参）。

### 4.2 长度闭合与容量口径
- 容量关系：`0x24` = 36 = `4+4+4+4×4+4+1×4`（两个数组各取上限 4）
- 线长：`12 + 4n + 4m`（n,m ≤ 4）

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
