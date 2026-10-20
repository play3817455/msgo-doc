# SC-0x0124-xwar_forcegauge_get_r

> 状态：`DONE`（2026-09-20）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0124` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `xwar_forcegauge_get_r` |
| 名字符串 | `)->_proto_lounge_client::recv_xwar_forcegauge_get_r(` @ `0xEEA130`，xref `0xB52023` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB51E9A` .. `0xB52213`（块首 `0xB51E9A push 0A1h`，`0xA1` 即本 case 开关/错误码） |
| 关联命令 | 发出侧 `_proto_lounge_client::send_xwar_forcegauge_get`（C→S `0x4E88`，声明容量 `0x2`）→ `../CS-0x4E88-lounge-xwar_forcegauge_get/` |

## 2. 结论摘要

- **报文体总长：变长**（含 2 个 NUL 结尾字符串），定长部分 = `4 + 4 + 4 + 2 = 14`，加上两个字符串的 `(串长+1)`。
- 负载 = **`u32 e_fgauge` + `u32 z_fgauge` + 字符串 `ranking_term_now` + 字符串 `ranking_term_last` + `u32 lose_troops` + `u16 expup_fgauge`**。
- 长度校验：`0xB51FDA` 取读完后的游标，`0xB51FE0 jz ok`（`cmp ebx,[esp+2C5Ch+var_2C40]`，vs 报文末尾；不等 ⇒ `push 0A1h` 报错）。**变长部分由该「游标 == 末尾」校验闭合**。
- 声明容量 `push 90h`（`0xB51EB6`）= `144` = `4+4+65+65+4+2`（**按定长槽预算**：两个字符串分配 65 字节槽；容量是上限，不是线长）。
- 是否分帧：否。
- 关键结论：**跨战（xwar）战力槽查询应答**；两路战力槽数值 + 当前/上期排名赛期字符串 + 损失部队数 + 经验加成值，一次性交 `vt[0x1D4]`（`0xB521DC`）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。
> 偏移列：字符串为变长，故第 5/6 行的偏移以「前序累计」表示（`len1`/`len2` = 串内容字节数，不含 NUL）。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x0124` | `0xB52023`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `e_fgauge` | 战力槽数值（E 路） | 交 `vt[0x1D4]` 第 1 实参；日志 `e_fgauge=`（`0xB52079`） | - | `0xB51EF4`（`sub_B02DD0`）；`0xB02DE9 add dword ptr [eax], 4`；日志 `0xB5206D`~`0xB52079` | 确证 |
| 2 | 4 | 4 | u32 | `z_fgauge` | 战力槽数值（Z 路） | 交 `vt[0x1D4]` 第 2 实参；日志 `z_fgauge=`（`0xB520A3`） | - | `0xB51F34`（`sub_B02DD0`）；日志 `0xB52094`~`0xB520A3` | 确证 |
| 3 | 8 | 变长 `len1+1` | bytes（NUL 结尾单字节串） | `ranking_term_now` | 当前排名赛期（字符串） | 交 `vt[0x1D4]` 第 3 实参（指针）；日志 `ranking_term_now="`（`0xB520D0`） | - | `0xB51F55`（`call sub_B02BA0`，`0xB51F46 push 41h` 槽上限 65）；reader 本体 `0xB02BEE mov [edi],esi`（游标 = NUL 后一位） | 确证 |
| 4 | 8+`len1+1` | 变长 `len2+1` | bytes（NUL 结尾单字节串） | `ranking_term_last` | 上期排名赛期（字符串） | 交 `vt[0x1D4]` 第 4 实参（指针）；日志 `ranking_term_last="`（`0xB52108`） | - | `0xB51F76`（`call sub_B02BA0`，`0xB51F63 push 41h`）；reader 本体 `0xB02BEE` | 确证 |
| 5 | 8+`len1+len2+2` | 4 | u32 | `lose_troops` | 损失部队数 | 交 `vt[0x1D4]` 第 5 实参；日志 `lose_troops=`（`0xB5213D`） | - | `0xB51F9E`（`sub_B02DD0`）；日志 `0xB5212E`~`0xB5213D` | 确证 |
| 6 | 12+`len1+len2+2` | 2 | u16 | `expup_fgauge` | 经验加成后的战力槽值 | 交 `vt[0x1D4]` 第 6 实参；日志 `expup_fgauge=`（`0xB52163`） | - | `0xB51FC6`（`sub_B02DF0`）；`0xB02E0B add dword ptr [eax], 2`；日志 `0xB52158`~`0xB52163` | 确证 |
| — | 14+`len1+len2+2` | 0 | — | （长度闭合） | — | 游标必须 == 末尾 | — | `0xB51FDA`（`cmp ebx,[esp+var_2C40]`）、`0xB51FE0`（`jz`） | 确证 |

**去向**（6 个值一次性交付）：`0xB521AB`..`0xB521DC` ——
`mov edx,[esi]; mov edx,[edx+1D4h]`；依次 push `expup_fgauge`(u16, movzx)、`lose_troops`(u32)、
`ranking_term_last`(指针)、`ranking_term_now`(指针)、`z_fgauge`(u32)、`e_fgauge`(u32) ⇒ `call vt[0x1D4]`。

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEEA130` 的引用点 `0xB52023` 落在 `sub_B51930` 的 case 块 `0xB51E9A..0xB52213` 内。
2. 块首 `0xB51E9A push 0A1h` 与全部错误路径 `push 0A1h`（如 `0xB51F07`）一致。

### 4.2 长度闭合
- 定长消费量 = `4 + 4 + 4 + 2` = **14** 字节，另有两条 `sub_B02BA0` 字符串（各消费 `串长+1`）。
- 读完立即 `0xB51FDA`/`0xB51FE0` 校验「游标 == 末尾」⇒ 变长部分自洽 ✓。
- 字符串读取器 `sub_B02BA0`：以 `strnlen` 结果定位 NUL（`0xB02BC3 sub_CC8400`），`memcpy(dst, cur, len+1)`
  （`0xB02BE6 sub_CC56B0`），并把游标推进到 NUL 之后（`0xB02BEE`）⇒ **消费 = 串长 + 1**、**单字节编码**（按字节 memcpy）。
- 容量 `0x90` 按「定长槽」预算（两串各 65 字节），故 `容量 > 实际线长` 属正常（规范 §1 铁律 2）。

### 4.3 存疑点
见 `notes.md`（`e_/z_` 前缀语义、`vt[0x1D4]` 实现未定）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致 —— 定长 14 字节 + 两串 `(len+1)`；`游标 == 末尾` 校验在 `0xB51FE0`。
- [x] G2 类型均指回汇编 VA（u32 `0xB02DE9`；u16 `0xB02E0B`；字符串 `0xB02BEE`）；未使用伪代码类型。
- [x] G3 含义取自块内日志串（6 条全部命中）；用途追到 `vt[0x1D4]`（`0xB521DC`）。
- [x] G4 不确定项标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对命令（发出侧 `0x4E88 xwar_forcegauge_get`）已在 §1 链接。
