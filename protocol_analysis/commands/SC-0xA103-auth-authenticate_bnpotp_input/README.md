# SC-0xA103-authenticate_bnpotp_input

> 状态：`DONE`（2026-09-20，作为规范落地的首个样例）
> 方向：服务端 → 客户端（recv）
> 协议类：`auth_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xA103` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `auth_client` |
| 命令名 | `authenticate_bnpotp_input` |
| 名字符串 | `)->_proto_auth_client::recv_authenticate_bnpotp_input(` @ `0xEDADFC` |
| 代码位置 | 分发器 `sub_B03D30` @ `0xB03D30`；处理块 `0xB04B61`..`0xB04C62` |
| 处理块范围 | `0xB04B61` .. `0xB04C62` |
| 关联命令 | 请求侧 `_proto_auth_client::send_authenticate_bnpotp_input_r`（@ `0xB05190`，opcode 见 INDEX `CS-0xB4xx-*`，待交叉链接） |

## 2. 结论摘要

- **报文体总长：`2` 字节（只有 opcode，无任何负载字段）。**
- 长度校验方式：处理块起始处 `cmp ebx, edi` + `jz`（`0xB04B70`/`0xB04B72`）——
  `ebx` = 负载游标（`0xB03D70` 处 `lea ebx, [ebp+2]`），`edi` = 缓冲区末尾
  （`0xB03D6D` 处 `lea edi, [eax+ebp]`，`eax`=`arg_1`=长度，`ebp`=`arg_0`=缓冲区基址）。
  二者相等 ⇒ **负载长度为 0**；不等则走错误码 `4` 的分支（`0xB04B79`/`0xB04B7B`）。
- 是否分帧：否。
- 关键结论：这是一条**纯通知/确认型命令**（无参数）。客户端收到后仅
  ① 打 trace 日志（含名字、`id`、负载字节数）② 递增接收计数 `[esi+160h..164h]`（64 位）
  ③ 调 `vt[0x70]` 通知上层；**不解析任何负载**。
- 与 OpenID/OTP 流程相关（名字含 `bnpotp_input`，且与 `authenticate_you9otp_input`
  （`0x60E0`）、`authenticate_you9channeling_r`（`0x8F36`）同族，见 `notes.md`）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发到本处理块 | `0xA103` | `0xB047D3`, `0xB047D8`（比较与跳转）、`0xB03D83`（读 opcode） | 确证 |
| — | 2 | 0 | — | （无负载） | — | — | — | `0xB04B70`, `0xB04B72`（长度必须为 0） | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 从名字符串 `0xEDADFC` 取 xref → `0xB04BA7`，落在 `sub_B03D30`（auth 分发器）。
2. 反解分发器 switch（比较树形态）：`cmp eax, 0A103h; jz loc_B04B61`（`0xB047D3`/`0xB047D8`）
   ⇒ opcode `0xA103` ↔ 处理块 `0xB04B61`。
3. 处理块内先做长度校验，再打名字 trace（`0xB04BA7` 压入本命令名字符串）
   —— 该 trace 正是「名字 → case 块」归属规则的锚点。

### 4.2 长度闭合
- 处理块内**没有**任何读取器调用（无 `[esi+0Ch]` 读取器虚表调用、无 `movzx byte/word ptr [游标]`）。
- 唯一的长度相关指令是 `cmp ebx, edi` / `jz`：要求 `游标 == 末尾`，即负载 0 字节。
- ⇒ 线长 = 2（opcode） + 0 = **2 字节**；与「无读取器」完全自洽。

### 4.3 非字段的代码（记录以免后续误判为字段）
| 地址 | 代码 | 说明 |
|---|---|---|
| `0xB04BA4` | `mov ecx, [esi+8]` | 取本对象成员，**只用于日志**（`" (id:"` 后打印），不是线字段 |
| `0xB04B86` | `mov edi, [esi+398h]` | 取对象成员（日志器/上下文），**不是线字段** |
| `0xB04BF7`..`0xB04C15` | `push offset aByte` → `"]byte"`、`push ebx`（`0xB04BFC` `sub ebx, ebp`） | 计算并打印**已消费字节数**（=报文长度），可用来反证「负载 0」 |
| `0xB04C38` | `add dword ptr [esi+160h], 1` + `0xB04C3F` `adc dword ptr [esi+164h], 0` | 64 位接收计数自增 |
| `0xB04C2F`..`0xB04C36` | `mov edx,[esi]; mov eax,[edx+70h]; call eax` | 调虚表 `vt[0x70]`，通知上层处理完成 |

### 4.4 存疑点
- 见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致 —— 2 字节，`cmp ebx,edi; jz` 要求负载 0。
- [x] G2 每个字段的类型都能指回汇编 VA（opcode 的 u16 来自 `0xB03D83` `movzx eax, word ptr [ebp+0]`；未使用伪代码类型）。
- [x] G3 无负载字段；非字段代码已在 §4.3 逐条说明用途与证据。
- [x] G4 不确定项已标 `?`/记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 已在 §1 给出配对命令链接位置（opcode 待回填）。
