# SC-0x0A7A-storage_msma_extend_r

> 状态：`DONE`（2026-09-20，批次-3）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0A7A` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `storage_msma_extend_r` |
| 名字符串 | `)->_proto_lounge_client::recv_storage_msma_extend_r(` @ `0xEE9DB0`，引用点 `0xB54FC0` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB54ED0` .. `0xB550B7`（块首 `0xB54ED0 push 1F7h; call sub_B41120`，错误码 `0x1F7`） |
| 关联命令 | 配对请求 `../CS-0xE591-lounge-storage_msma_extend/`（`sub_BA3E90`，容量 `0x12`）；相关 `SC-0xB718 storage_msma_extend_buy_ticket_r`(DRAFT) |

## 2. 结论摘要

- **报文体总长：定长 8 字节**（2 个 u32）。
- 长度校验：`0xB54F73 mov ebx,[esp+var_2C44]`（游标）、`0xB54F77 cmp ebx,[esp+var_2C40]`（vs 报文末尾）、`0xB54F7D jz ok`（不等 ⇒ `push 1F7h` 报错）⇒ **整包精确消费完**。
- 声明容量 `push 8`（`0xB54EEC`）= **8 == 线长**（全定长 ⇒ 容量与线长强相等）。
- 是否分帧：否。
- 关键结论：2 个值交 `vt[0x4B4]`（`0xB5508F` 取虚表项 / `0xB5509B` 调用），实参顺序 `(result, slot_num)`；块内日志 `result=` / `slot_num=`。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x0A7A` | `0xB54FC0`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `result` | 机体仓库扩容结果码 | 交 `vt[0x4B4]`（第 1 实参 `0xB55098 push ecx`）；日志 `result=`（`0xB55016`，十进制）；日志用 `,` 与下一字段分隔（`0xB55010`） | `?`（结果码枚举未交叉） | `0xB54F27`（`sub_B02DD0`）；槽预留 `0xB54F18`（`sub_B41470`）；`0xB02DE9 add [eax],4`；日志 `0xB55016` | 类型确证 / 枚举待定 |
| 2 | 4 | 4 | u32 | `slot_num` | 扩容后的仓库机位总数 | 交 `vt[0x4B4]`（第 2 实参 `0xB55095 push ecx`）；日志 `slot_num=`（`0xB5503B`） | `-` | `0xB54F67`（`sub_B02DD0`）；槽预留 `0xB54F58`（`sub_B41470`）；日志 `0xB5503B` | 确证 |
| — | 8 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB54F77`（`cmp`）、`0xB54F7D`（`jz`） | 确证 |

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE9DB0` 的引用点 `0xB54FC0` 落在 `sub_B51930` 的 case 块 `0xB54ED0..0xB550B7` 内（全部错误路径 `0xB54F3A`/`0xB54F86` 用错误码 `0x1F7`）。
2. 两个字段 = 两组「槽预留 `sub_B41470` + bounded 读取器 `sub_B02DD0`」。
3. 块内日志顺序（`result=` → `slot_num=`）与线序一致。
4. 去向：`0xB5508F mov edx,[edx+4B4h]` ⇒ `vt[0x4B4]`，实参 `(result, slot_num)`（`0xB55095`/`0xB55098`）。

### 4.2 长度闭合
- `4 + 4 = 8`；闭合点 `0xB54F77` 要求「游标 == 末尾」✓
- 容量 8 == 线长（全定长 ⇒ 强相等）。

### 4.3 存疑点
见 `notes.md`（`result` 枚举、`slot_num` 是「总数」还是「新增数」）。

## 5. 质量门自检

- [x] G1 字段表总长（8）与 `0xB54F77`/`0xB54F7D` 的「游标 == 末尾」校验一致；容量 8 == 线长。
- [x] G2 线类型指回汇编 VA（`0xB54F27`/`0xB54F67` + `0xB02DE9`）；未使用伪代码类型。
- [x] G3 含义取自块内日志串（`result=`/`slot_num=`），用途追到 `vt[0x4B4]`（`0xB5509B`）。
- [x] G4 不确定项（`result` 枚举、`slot_num` 口径）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对请求 `CS-0xE591-lounge-storage_msma_extend` 已在 §1 链接。
