# SC-0x00C7-msma_trialms_back_r

> 状态：`DONE`（2026-09-20）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x00C7` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `msma_trialms_back_r` |
| 名字符串 | `)->_proto_lounge_client::recv_msma_trialms_back_r(` @ `0xEEA168`，xref `0xB51D9F` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB51C95` .. `0xB51E9A`（case 体入口 `0xB51C95`：`push 13Eh; mov ecx, esi; call sub_B41120`） |
| 关联命令 | 发出侧 `_proto_lounge_client::send_msma_trialms_back`（C→S `0x0C2A`）→ `../CS-0x0C2A-lounge-msma_trialms_back/` |

## 2. 结论摘要

- **报文体总长：`12` 字节**（opcode `2` + 负载 `10`）。
- 负载 = **1 × `u32` + 1 × `u64`**（`4 + 8`）。
- 长度校验：`0xB51D54` 取读完后的游标，`0xB51D58 cmp eax, [esp+2C5Ch+var_2C40]`（vs 报文末尾），`0xB51D5C jz ok`（不等 ⇒ 错误码 `0x13E`）。
- 声明容量 `push 0Ch`（`0xB51CB1`）= `12` = 负载字节数（**定长命令，容量 == 负载长**，旁证）。
- 是否分帧：否。
- 关键结论：**「试用机体领取/返还」应答**；`result`＝结果码，`uniqid_ms`＝机体唯一 ID（`uniqid_ms` 由两个 u32 拼成 u64）。两值一次性交 `vt[0x328]`（`0xB51E7E`）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x00C7` | `0xB51D9F`（名字串引用点，锚定 case 归属） | 确证 |
| 1 | 0 | 4 | u32 | `result` | 处理结果码 | 交给 `vt[0x328]` 第 1 实参（`0xB51E7E`）；日志 `result=`（`0xB51DF5`） | - | `0xB51CEC`（`call sub_B02DD0`，内部 `0xB02E0B add dword ptr [eax], 4`）；日志 `0xB51DE9`~`0xB51DF5` | 确证 |
| 2 | 4 | 8 | u64 | `uniqid_ms` | 机体唯一 ID（跨服唯一键） | 交给 `vt[0x328]` 第 2/3 实参（`0xB51E66`/`0xB51E73` 压 `[ebx+4]`、`[ebx]`）；日志 `uniqid_ms=`（`0xB51E1A`） | - | `0xB51D2C`（`call sub_B06200`）；reader 本体 `0xB06206`（`lea edx,[ecx+8]`）、`0xB06220`（`add dword ptr [eax], 8`） | 确证 |
| — | 12 | 0 | — | （长度闭合） | — | 游标必须 == 末尾 | — | `0xB51D54`（`mov eax,[esp+var_2C44]`）、`0xB51D58`（`cmp eax,[esp+var_2C40]`）、`0xB51D5C`（`jz`） | 确证 |

**去向**（2 个值一次性交付）：`0xB51E66`..`0xB51E7E` ——
`mov eax,[ebx+4]`（u64 高）、`mov ecx,[ebx]`（u64 低）、`mov edx,[esi]; mov edx,[edx+328h]`、
`push eax; push ecx; mov ecx,[eax(结果槽)]; push [ecx]` ⇒ `call vt[0x328]`。

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEEA168` 的引用点 `0xB51D9F` 落在 `sub_B51930`（lounge 分发器）的 case 块 `0xB51C95..0xB51E9A` 内。
2. 块首 `0xB51C95 push 13Eh; mov ecx,esi; call sub_B41120` 是 case 级开关（`13Eh` == 本 case 错误码，后续错误路径 `push 13Eh` 一致）。

### 4.2 长度闭合
- 读取序列：`sub_B41470` 预留槽（非字段）→ `sub_B02DD0` 读 u32 → `sub_B41A10` 预留槽（非字段）→ `sub_B06200` 读 u64。
- 消费量 = `4 + 8` = **12** 字节；随即 `0xB51D58` 校验「游标 == 末尾」✓。
- 交叉印证：解码缓冲容量 `push 0Ch`（`0xB51CB1`）= 12，与负载字节数相等（旁证，非线长依据）。

### 4.3 存疑点
见 `notes.md`（无阻塞项；`vt[0x328]` 的实现函数未展开）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致 —— 负载 12 字节；`游标 == 末尾` 校验在 `0xB51D58`/`0xB51D5C`。
- [x] G2 每个字段的类型都能指回汇编 VA（u32 见 `0xB02E0B`；u64 见 `0xB06206`/`0xB06220`）；未使用伪代码类型。
- [x] G3 每个字段都有含义与用途：含义取自块内日志串 `result=`/`uniqid_ms=`，用途追到 `vt[0x328]`（`0xB51E7E`）。
- [x] G4 不确定项标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对命令（发出侧 `0x0C2A msma_trialms_back`）已在 §1 链接。
