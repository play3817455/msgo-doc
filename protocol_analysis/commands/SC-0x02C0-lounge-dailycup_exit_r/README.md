# SC-0x02C0-dailycup_exit_r

> 状态：`DONE`（2026-09-20）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x02C0` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `dailycup_exit_r` |
| 名字符串 | `)->_proto_lounge_client::recv_dailycup_exit_r(` @ `0xEEA100`，xref `0xB522BC` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB52213` .. `0xB52382`（块首 `0xB52213 call sub_B41120`；本 case 开关/错误码 `0x23B`，见 `0xB52278`） |
| 关联命令 | INDEX 中无同名 C→S `send_dailycup_exit`（无配对请求）；同族：`dailycup_get_point_r`(`0x2AAF`) |

## 2. 结论摘要

- **报文体总长：`6` 字节**（opcode `2` + 负载 `4`）。
- 负载 = **1 × `u32`**（`result` @0）。
- 长度校验：`0xB5228B` 取读完后的游标，`0xB5228F cmp ebx, [esp+2C5Ch+var_2C40]`（vs 报文末尾），`0xB52293 jnz 错误`（不等 ⇒ `push 23Bh` 报错）。
- 声明容量 `push 4`（`0xB52228`）= `4` = 负载字节数（**定长命令，容量 == 负载长**，旁证）。
- 是否分帧：否。
- 关键结论：**每日杯（daily cup）退出应答**；仅携带 `result`＝结果码，交 `vt[0x568]`（`0xB52366`）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x02C0` | `0xB522BC`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `result` | 退出处理结果码 | 交 `vt[0x568]`（`0xB52366`）；日志 `result=`（`0xB5230D`） | - | `0xB52263`（`call sub_B02DD0`）；本体 `0xB02DE1`（`mov ecx,[ecx]`）+ `0xB02DE9`（`add dword ptr [eax], 4`）；日志 `0xB52306`~`0xB5230D` | 确证 |
| — | 4 | 0 | — | （长度闭合） | — | 游标必须 == 末尾 | — | `0xB5228B`（`mov ebx,[esp+var_2C44]`）、`0xB5228F`（`cmp ebx,[esp+var_2C40]`）、`0xB52293`（`jnz`） | 确证 |

**去向**：`0xB52355`..`0xB52366` —— `mov eax,[esp+var_2C04]`（槽）→ `mov ecx,[eax]`
→ `mov edx,[esi]; mov edx,[edx+568h]` → `push ecx` ⇒ `call vt[0x568](result)`。

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEEA100` 的引用点 `0xB522BC` 落在 `sub_B51930` 的 case 块 `0xB52213..0xB52382` 内。
2. 全部错误路径 `push 1; push 23Bh`（`0xB52276`/`0xB52278`）⇒ 本 case 开关/错误码 = `0x23B`。

### 4.2 长度闭合
- 读取序列：预留 u32 槽（`sub_B41470`，非字段）→ `sub_B02DD0` 读 u32。
- 消费量 = **4** 字节；随即 `0xB5228F` 校验「游标 == 末尾」✓。
- 交叉印证：解码缓冲容量 `push 4`（`0xB52228`）= 4（旁证）。

### 4.3 存疑点
见 `notes.md`（`result` 枚举、`vt[0x568]` 实现未定）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致 —— 负载 4 字节；`游标 == 末尾` 校验在 `0xB5228F`/`0xB52293`。
- [x] G2 类型指回汇编 VA（`0xB02DE1` 读 u32、`0xB02DE9` 游标 +4）；未使用伪代码类型。
- [x] G3 含义取自日志串 `result=`（`0xB5230D`）；用途追到 `vt[0x568]`（`0xB52366`）。
- [x] G4 不确定项标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 无配对 C→S 命令（已在 §1 说明）。
