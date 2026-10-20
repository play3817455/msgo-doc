# SC-0x1146-auth-worldlist_select_r

> 状态：`DONE`（2026-09-20，批次-4）
> 方向：服务端 → 客户端（recv）
> 协议类：`auth_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x1146` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `auth_client` |
| 命令名 | `worldlist_select_r` |
| 名字字符串 | `)->_proto_auth_client::recv_worldlist_select_r( `，引用点 `0xB0417E`（`push offset aProtoAuthClien_7`） |
| 处理函数 | `sub_B03D30` @ `0xB03D30`（auth 分发器） |
| 处理块范围 | `0xB04068` .. `0xB04355`（块首即 `push 0Dh`，错误码 `0x0D`） |
| 错误码 | `0x0D`（`0xB040BD push 0Dh` → `loc_B04854` 错误分支） |
| 关联命令 | 配对请求 `../CS-0xA380-auth-worldlist_select/`（`0xA380`，容量 `0xA`）；同族 `../SC-0x298E-auth-worldlist_get_r/`（`0x298E`） |

## 2. 结论摘要

- **报文体总长：变长 = `17 + L_en + L_host + L_otp`**（u32 `result` + NUL 串 `world_name_en` + NUL 串 `loungesv_host` + u32 `loungesv_port` + u32 `userid` + NUL 串 `otp`）。
  各串上限：`L_en ≤ 48`、`L_host ≤ 128`、`L_otp ≤ 40`。
- 长度校验：`0xB04152 mov ebx,[esp+var_10C]`（线游标）、`0xB04156 cmp ebx,[esp+var_108]`（vs 报文末尾）、`0xB0415A jnz loc_B040BB`（不等 ⇒ 报错）⇒ **整包精确消费完**。
- 声明容量 `push 0E7h`（`0xB0407F`）= **231 == Σ缓冲 claim** = `4 + 49 + 129 + 4 + 4 + 41`（串 claim = 槽位预算：`0x31`/`0x81`/`0x29`，与 `sub_B02BA0` 的 maxlen 实参一致）✓
- 是否分帧：否。
- 关键结论：6 个值交 `vt[0x80]`（`0xB04322` 取虚表项 / `0xB04340` 调用），**实参顺序 `(result, world_name_en, loungesv_host, loungesv_port, userid, otp)`**；块内日志 `result=`、`world_name_en="`、`loungesv_host="`、`loungesv_port=`、`userid=`、`otp="`。
- auth 分支特性：日志只在 `[esi+3BCh]`（日志对象）非空时才打印（`0xB04160 test edi,edi` / `0xB04168 jz loc_B04316`），**但 `vt[0x80]` 无论日志是否开启都会被调用**（`0xB04316` 是日志跳过后的合流点，位于 `call vt[0x80]` 之前）。
- 缓冲游标用法（auth 专有）：`ebp` 依次推进 `+4` → `+0x31` → `+0x81` → `+4` → `+4`，每步把「当前 `ebp`」存进对应槽变量供日志/去向取值。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | auth 分发的 switch 选择子 | `0x1146` | `0xB0417E`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `result` | 大区（world）选择结果码 | 交 `vt[0x80]` 第 1 实参（`0xB0433D push ecx`）；日志 `result=`（`0xB041D1`） | `?`（结果码枚举未交叉） | `0xB040AF`（`sub_B02DD0`）；槽 `0xB040A8 mov [var_100],eax`；`0xB02DE9 add [eax],4`；日志 `0xB041D1` | 类型确证 / 枚举待定 |
| 2 | 4 | `Len+1` | bytes（NUL 串） | `world_name_en` | 大区英文名 | 交 `vt[0x80]` 第 2 实参（`0xB0433A push ecx`）；日志 `world_name_en="`（`0xB041FE`） | `Len ≤ 48`（预算 `0x31`） | `0xB040D5`（`sub_B02BA0`，预算 `0xB040C6 push 31h`）；`0xB02BEE`（游标 += 串长+1）；日志 `0xB041FE` | 确证 |
| 3 | `5+Len_en` | `Len+1` | bytes（NUL 串） | `loungesv_host` | 大厅服务器主机名/IP | 交 `vt[0x80]` 第 3 实参（`0xB04335 push eax`）；日志 `loungesv_host="`（`0xB04236`） | `Len ≤ 128`（预算 `0x81`） | `0xB040F8`（`sub_B02BA0`，预算 `0xB040E3 push 81h`）；日志 `0xB04236` | 确证 |
| 4 | `6+Len_en+Len_host` | 4 | u32 | `loungesv_port` | 大厅服务器端口 | 交 `vt[0x80]` 第 4 实参（`0xB04330 push ecx`）；日志 `loungesv_port=`（`0xB0426B`） | `-`（16 位端口值占 4 字节线宽） | `0xB04113`（`sub_B02DD0`）；槽 `0xB0410C mov [var_104],eax`；日志 `0xB0426B` | 确证 |
| 5 | `10+Len_en+Len_host` | 4 | u32 | `userid` | 分配给本会话的玩家 ID | 交 `vt[0x80]` 第 5 实参（`0xB04329 push ecx`）；日志 `userid=`（`0xB04295`） | `-` | `0xB0412E`（`sub_B02DD0`）；槽 `0xB04127 mov [var_F0],eax`；日志 `0xB04295` | 确证 |
| 6 | `14+Len_en+Len_host` | `Len+1` | bytes（NUL 串） | `otp` | 一次性口令（OTP） | 交 `vt[0x80]` 第 6 实参（`0xB04328 push ebp`）；日志 `otp="`（`0xB042B9`） | `Len ≤ 40`（预算 `0x29`） | `0xB04142`（`sub_B02BA0`，预算 `0xB0413A push 29h`，dst = 当前 `ebp`）；日志 `0xB042B9` | 确证 |
| — | `17+Len_en+Len_host+Len_otp` | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB04156`（`cmp`）、`0xB0415A`（`jnz`） | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xB0417E` 落在 `sub_B03D30` 的 case 块 `0xB04068..0xB04355` 内（错误码 `0x0D`）。
2. auth 的字段写法与 lounge 不同：**用 `ebp` 手动做缓冲游标**（`mov eax, ebp` → `push eax` → `add ebp, N`），不再调 `sub_B41470`/`sub_B413B0` 预留族。
3. 三个串的 maxlen 实参（`0x31`/`0x81`/`0x29`）与容量之和精确吻合 ⇒ 直接确证「串 claim = 槽位预算」。
4. 含义取自块内日志串（6 条，顺序与线序一致）；去向 `vt[0x80]`（6 实参）。

### 4.2 长度闭合
- `4 + (Len_en+1) + (Len_host+1) + 4 + 4 + (Len_otp+1) = 17 + Len_en + Len_host + Len_otp`；
  闭合点 `0xB04156`/`0xB0415A` 要求「游标 == 末尾」✓
- 容量校验：`4 + 49 + 129 + 4 + 4 + 41 = 231 = 0xE7` ✓（Σ缓冲 claim）。

### 4.3 存疑点
见 `notes.md`（`vt[0x80]` 业务定名、`result` 枚举、`otp` 与 `0xA103`/`0x60E0` 两条 OTP 命令的先后关系）。

## 5. 质量门自检

- [x] G1 字段表总长（`17+Len_en+Len_host+Len_otp`）与 `0xB04156`/`0xB0415A` 的「游标 == 末尾」校验一致；容量 231 = Σ claim。
- [x] G2 线类型指回汇编 VA（`0xB040AF`/`0xB04113`/`0xB0412E` + `0xB02DE9` u32；`0xB040D5`/`0xB040F8`/`0xB04142` + `0xB02BEE` 串）；未使用伪代码类型。
- [x] G3 含义取自块内 6 条日志串，用途追到 `vt[0x80]`（`0xB04340`）。
- [x] G4 不确定项（`result` 枚举、`vt[0x80]` 定名）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对请求 `CS-0xA380-auth-worldlist_select` 与同族 `0x298E` 已在 §1 链接。
