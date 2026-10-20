# SC-0x0A78-speedhack_check_request

> 状态：`DONE`（2026-09-20，批次-3）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0A78` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `speedhack_check_request` |
| 名字符串 | `)->_proto_lounge_client::recv_speedhack_check_request(` @ `0xEE9E20`，引用点 `0xB54BFC` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB54B4C` .. `0xB54CF0`（块首 `0xB54B4C push 215h; call sub_B41120`，错误码 `0x215`） |
| 关联命令 | 配对应答 `../CS-0x5F28-lounge-speedhack_check_response/`（`sub_BA4D50`，容量 `0xA`） |

## 2. 结论摘要

- **报文体总长：定长 4 字节**（1 个 u32）。
- 长度校验：`0xB54BCB mov ebx,[esp+var_2C44]`（游标）、`0xB54BCF cmp ebx,[esp+var_2C40]`（vs 报文末尾）、`0xB54BD3 jnz 报错` ⇒ **整包精确消费完**（成功 = 落空继续）。
- 声明容量 `push 4`（`0xB54B68`）= **4 == 线长**（全定长 ⇒ 容量与线长强相等）。
- 是否分帧：否。
- 关键结论：1 个值交 `vt[0x508]`（`0xB54C9D` 取虚表项 / `0xB54CA6` 调用），实参 `(sec)`；块内日志 `sec=`。命令名「request」是**服务端要客户端做一次速度检查**，客户端以 `0x5F28 speedhack_check_response`（容量 `0xA`）回报。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x0A78` | `0xB54BFC`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `sec` | 速度检查的采样时长/时间戳（秒） | 交 `vt[0x508]`（唯一实参 `0xB54CA3 push ecx`）；日志 `sec=`（`0xB54C4D`，十进制打印器 `sub_B03580`） | `?`（秒数 vs 时间戳未定，见 `notes.md` Q1） | `0xB54BA3`（`sub_B02DD0`）；槽预留 `0xB54B94`（`sub_B41470`）；`0xB02DE9 add [eax],4`；日志 `0xB54C4D` | 类型确证 / 语义待定 |
| — | 4 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB54BCF`（`cmp`）、`0xB54BD3`（`jnz`） | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE9E20` 的引用点 `0xB54BFC` 落在 `sub_B51930` 的 case 块 `0xB54B4C..0xB54CF0` 内（错误路径 `0xB54BB8`/`0xB54BD5` 均用错误码 `0x215`）。
2. 唯一字段：`0xB54B94 call sub_B41470`（预留，**非字段**）+ `0xB54BA3 call sub_B02DD0`（**读 u32**）成对。
3. 日志 `sec=`（`0xB54C4D`）与唯一字段对应；去向 `0xB54C9D mov edx,[edx+508h]` ⇒ `vt[0x508]`。

### 4.2 长度闭合
- 线长 4；闭合点 `0xB54BCF` 要求「游标 == 末尾」✓
- 容量 4 == 线长（全定长 ⇒ 强相等）。

### 4.3 存疑点
见 `notes.md`（`sec` 语义、与 C→S `0x5F28` 应答的对应）。

## 5. 质量门自检

- [x] G1 字段表总长（4）与 `0xB54BCF`/`0xB54BD3` 的「游标 == 末尾」校验一致；容量 4 == 线长。
- [x] G2 线类型指回汇编 VA（`0xB54BA3` + `0xB02DE9`）；未使用伪代码类型。
- [x] G3 含义取自块内日志串 `sec=`（`0xB54C4D`）；用途追到 `vt[0x508]`（`0xB54CA6`）。
- [x] G4 不确定项（`sec` 语义）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对应答 `CS-0x5F28-lounge-speedhack_check_response` 已在 §1 链接。
