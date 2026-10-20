# SC-0x1113-battle-game_script_play

> 状态：`DONE`（2026-09-20，批次-4）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x1113` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `battle_client` |
| 命令名 | `game_script_play` |
| 名字字符串 | `)->_proto_battle_client::recv_game_script_play( `，引用点 `0xB0F22A`（`push offset aProtoBattleCli_13`） |
| 处理函数 | `sub_B0CC20` @ `0xB0CC20`（battle 分发器） |
| 处理块范围 | `0xB0F127` .. `0xB0F360`（块首即 `push 3Dh`，错误码 `0x3D`） |
| 错误码 | `0x3D`（`0xB0F189 push 3Dh` → `vt[0x64](1, 0x3D)`） |
| 关联命令 | 同族 `../SC-0x611B-battle-game_script_play_also_replay/`（`0x611B`）；**无严格配对请求**（服务端下发剧本播放指令） |

## 2. 结论摘要

- **报文体总长：变长 = `L + 3`**（NUL 串 `src`（`L ≤ 64`）+ u8 `is_with_resume` + u8 `script_thread`）。
- 长度校验：`0xB0F1E3 mov ebx,[esp+var_1B28]`（线游标）、`0xB0F1E7 cmp ebx,[esp+var_1B24]`（vs 报文末尾）、`0xB0F1ED jz loc_B0F206`（不等 ⇒ 报错）⇒ **整包精确消费完**。
- 声明容量 `push 43h`（`0xB0F140`）= **67 == Σ缓冲 claim** = `65`（`src` 串槽预算，`0xB0F158 push 41h` 同时是 `sub_B02BA0` 的第 3 实参）+ `1` + `1`。实际线长 `L+3 ≤ 67`。
- 是否分帧：否。
- 关键结论：`src`（剧本源串）+ `is_with_resume` + `script_thread` 交 `vt[0x10C]`（`0xB0F33B` 取虚表项 / `0xB0F344` 调用），实参顺序 `(src, is_with_resume, script_thread)`；块内日志 `src="`、`is_with_resume=`、`script_thread=`。
- 缓冲分配细节（用途解析用）：`edi` = 缓冲基址（存入 `var_1B08` 作为 `src` 的实参），字符串读完即 `add edi,41h`（`0xB0F15F`）把缓冲游标推过 65B 槽；后两个 u8 用 `sub_B05E30` 直接取槽，**不推进 `edi`**。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | battle 分发的 switch 选择器 | `0x1113` | `0xB0F22A`（名字串引用点） | 确证 |
| 1 | 0 | `L+1` | bytes（NUL 串） | `src` | 要播放的剧本（script）源串 | 交 `vt[0x10C]` 第 1 实参 = 串首地址（`0xB0F341 push ecx`，`ecx = [var_1B08]`）；日志 `src="`（`0xB0F283`） | `L = strlen ≤ 64` | `0xB0F176`（`sub_B02BA0`，预算 `0xB0F158 push 41h`）；`0xB02BEE`（游标 += 串长+1）；日志 `0xB0F283`；去向 `0xB0F341` | 确证 |
| 2 | `L+1` | 1 | u8 | `is_with_resume` | 是否从断点续播 | 交 `vt[0x10C]` 第 2 实参（`0xB0F33A push edx`）；日志 `is_with_resume=`（`0xB0F2B6`） | `0/1`（未交叉） | `0xB0F1B3`（`sub_B06230`）；槽预留 `0xB0F1A4`（`sub_B05E30`）；`0xB06249 add [..],1`；日志 `0xB0F2B6` | 确证 |
| 3 | `L+2` | 1 | u8 | `script_thread` | 剧本执行所用线程/流编号 | 交 `vt[0x10C]` 第 3 实参（`0xB0F332 push edx`）；日志 `script_thread=`（`0xB0F2DB`） | `-` | `0xB0F1D7`（`sub_B06230`）；槽预留 `0xB0F1C8`（`sub_B05E30`）；日志 `0xB0F2DB` | 确证 |
| — | `L+3` | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB0F1E7`（`cmp`）、`0xB0F1ED`（`jz`） | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB0F22A` 落在 `sub_B0CC20` 的 case 块 `0xB0F127..0xB0F360` 内（错误码 `0x3D`）。
2. `0xB0F15A add edi,41h` + `0xB0F172 mov [var_1B14],edi` ⇒ 先为 `src` 预留 65B 缓冲槽；`sub_B02BA0(dst, &线游标, 0x41)` 读 NUL 串。
3. 后两个字段 = 「`sub_B05E30` 预留 1B + `sub_B06230` 读 u8」 × 2。
4. 含义取自块内日志 `src="`（前后拼引号串 `0xEDAD54`）、`is_with_resume=`、`script_thread=`。
5. 去向：`0xB0F325..0xB0F344` 三次 `push`（`script_thread`,`is_with_resume`,`src`）→ `call vt[0x10C]`。

### 4.2 长度闭合
- `(L+1) + 1 + 1 = L+3`；闭合点 `0xB0F1E7`/`0xB0F1ED` 要求「游标 == 末尾」✓
- 容量校验：`65 + 1 + 1 = 67 = 0x43` ✓（串 claim = 槽位预算 65；`L ≤ 64`）。

### 4.3 存疑点
见 `notes.md`（`vt[0x10C]` 业务定名、`script_thread` 语义、`src` 的脚本语言/格式）。

## 5. 质量门自检

- [x] G1 字段表总长（`L+3`）与 `0xB0F1E7`/`0xB0F1ED` 的「游标 == 末尾」校验一致；容量 67 = Σ claim（含串槽 65）。
- [x] G2 线类型指回汇编 VA（`0xB0F176`+`0xB02BEE` 串、`0xB0F1B3`/`0xB0F1D7`+`0xB06249` u8）；未使用伪代码类型。
- [x] G3 含义取自块内日志串，用途追到 `vt[0x10C]`（`0xB0F344`）。
- [x] G4 不确定项（`vt[0x10C]` 定名、`script_thread` 语义）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 同族命令 `0x611B` 已在 §1 链接（本命令无严格配对请求）。
