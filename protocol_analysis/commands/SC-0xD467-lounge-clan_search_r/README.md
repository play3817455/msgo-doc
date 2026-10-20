# SC-0xD467-lounge-clan_search_r

> 状态：`DONE`（2026-09-20，批次-14）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xD467` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `clan_search_r` |
| 处理块范围 | `0xb7cc14`..`0xb7cf17` |
| 名字串引用点 | `0xee6518` |
| 声明容量（解码缓冲） | `0xE19`（`B7CC30`） |
| 长度闭合点 | `B7CD58` |
| 报错码 | `0x1CE`（块内 `push 1; push 1CEh; vt[0x64]`） |
| 去向 | `vt[0x460]` @`B7CEFB`（4 实参） |

## 2. 结论摘要

- **报文体线长**：`8 + 114n + 1`（n ≤ 30）
- 容量关系：`0xE19` = 3609 = `4 + 4 + 30×120 + 1`（`n` 取上限 30；元素槽步进 120 = `sub_B417A0`）
- 长度闭合：块末 `B7CD52`（`cmp ecx,[var_2C40]`）＋ `B7CD58 jz` 校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**4**（不含 opcode）；去向：`vt[0x460]` @`B7CEFB`（4 实参）
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0xD467` | `0xb7cd9b` | 确证 |
| 1 | 0 | 4 | u32 | result | 检索结果码（日志串 `result=`） | 经 `vt[0x460]` 交业务 | - | 0xb7cc6e | 确证 |
| 2 | 4 | 4 | u32 | res_num | 命中公会条数（日志串 `search_res={`，上限 30） | 驱动 `search_res` 数组循环（`cmp edi,ebx`@`B7CD10`） | 0..30 | 0xb7cca0|0xb7cccc|0xb7cd10 | 确证 |
| 3 | 8 | 114n | array<clan_search_hit,30> | search_res | 命中公会列表（日志串 `search_res={`，普通成员打印器 `sub_B4E680`） | 经 `vt[0x460]` 交业务；元素成员：`clan_id`(u32)/`emb_base`(u8)/`emb_parts1`(u8)/`emb_parts2`(u8)/`clan_name`(bytes[31])/`level`(u8)/`offer_body`(bytes[31])/`leader_name`(bytes[25])/`member_num`(u32)/`member_max`(u32)/`offer_is_active`(u8)/`clan_kind`(u8)/`active_time_bits`(u32)/`play_style`(u8)/`capture_unlock_num`(u32) | - | 0xb7ccdb|0xb7ccfc|0xb7cd12 | 确证 |
| 4 | var(8+114n) | 1 | u8 | clan_kind | 公会类别（日志串 `clan_kind=`） | 经 `vt[0x460]` 交业务 | - | 0xb7cd3e | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb7cd9b` 落在处理块 `0xb7cc14`..`0xb7cf17` 内。
2. 容量经分配器指纹在 `B7CC30` 确证为 `0xE19`。
3. 先读 `result`(u32)、`res_num`(u32，`cmp ebx,1Eh; ja <错误出口>`@`B7CCCC` 限定 ≤30)；
4. 再 `sub_B417A0` 按 `res_num` 预留 120B/槽，循环 `cmp edi,ebx; jb` 内由复合读取器 `sub_B45BA0` 逐元素消费（`add [var_2C48],78h` 步进 120）；
5. 末读 `clan_kind`(u8)。类型全部由汇编判定（SOP §6）。
6. 闭合：`B7CD52`+`B7CD58`（SOP §5.3）。去向：`vt[0x460]` @`B7CEFB`（4 实参）。

### 4.2 长度闭合与容量口径
- 容量关系：`0xE19` = 3609 = `4 + 4 + 30×120 + 1`（`n` 取上限 30；元素槽步进 120 = `sub_B417A0`）
- 线长：`8 + 114n + 1`（n ≤ 30）

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
