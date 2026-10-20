# SC-0x02F6-chargepoint_update

> 状态：`DONE`（2026-09-20）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x02F6` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `chargepoint_update` |
| 名字符串 | `)->_proto_lounge_client::recv_chargepoint_update(` @ `0xEEA01C`，xref `0xB531B9` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB53112` .. `0xB5327F`（块首 `0xB53112 push 40h`，`40h` 即本 case 开关/错误码） |
| 关联命令 | 同族（充值点族）：`chargepoint_get`（C→S `0xAAE5`）、`chargepoint_price_list_get`(`0x7CCB`/`0x9397`)、`chargepoint_charge_url_get_r`(`0x4DA5`)、`chargepoint_charge_url_get`（C→S `0xFFC6`）；无同名 C→S `send_chargepoint_update` |

## 2. 结论摘要

- **报文体总长：`6` 字节**（opcode `2` + 负载 `4`）。
- 负载 = **1 × `u32`**（`chargepoint` @0）。
- 长度校验：`0xB5318B` 取读完后的游标，`0xB5318F cmp ebx, [esp+2C5Ch+var_2C40]`（vs 报文末尾），`0xB53193 jnz 错误`（不等 ⇒ `push 40h` 报错）。
- 声明容量 `push 4`（`0xB5312B`）= `4` = 负载字节数（**定长命令，容量 == 负载长**，旁证）。
- 是否分帧：否。
- 关键结论：**充值点（charge point）余额更新通知**；仅携带 `chargepoint`＝最新充值点数值，交 `vt[0xF8]`（`0xB53263`）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x02F6` | `0xB531B9`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `chargepoint` | 充值点（游戏内付费点数）余额 | 交 `vt[0xF8]`（`0xB53263`）；日志 `chargepoint=`（`0xB5320A`） | - | `0xB53166`（`call sub_B02DD0`）；本体 `0xB02DE1`（`mov ecx,[ecx]`）+ `0xB02DE9`（`add dword ptr [eax], 4`）；日志 `0xB53203`~`0xB5320A` | 确证 |
| — | 4 | 0 | — | （长度闭合） | — | 游标必须 == 末尾 | — | `0xB5318B`（`mov ebx,[esp+var_2C44]`）、`0xB5318F`（`cmp ebx,[esp+var_2C40]`）、`0xB53193`（`jnz`） | 确证 |

**去向**：`0xB53252`..`0xB53263` —— `mov eax,[esp+var_2C48]`（槽）→ `mov ecx,[eax]`
→ `mov edx,[esi]; mov edx,[edx+0F8h]` → `push ecx` ⇒ `call vt[0xF8](chargepoint)`。

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEEA01C` 的引用点 `0xB531B9` 落在 `sub_B51930` 的 case 块 `0xB53112..0xB5327F` 内。
2. 块首 `0xB53112 push 40h` 与全部错误路径 `push 40h`（如 `0xB5317B`）一致。

### 4.2 长度闭合
- 读取序列：预留 u32 槽（`sub_B41470` @`0xB53157`，非字段）→ `sub_B02DD0` 读 u32（`0xB53166`）。
- 消费量 = **4** 字节；随即 `0xB5318F` 校验「游标 == 末尾」✓。
- 交叉印证：解码缓冲容量 `push 4`（`0xB5312B`）= 4（旁证）。

### 4.3 存疑点
见 `notes.md`（`vt[0xF8]` 实现、单位/货币换算未定）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致 —— 负载 4 字节；`游标 == 末尾` 校验在 `0xB5318F`/`0xB53193`。
- [x] G2 类型指回汇编 VA（`0xB02DE1` 读 u32、`0xB02DE9` 游标 +4）；未使用伪代码类型。
- [x] G3 含义取自日志串 `chargepoint=`（`0xB5320A`）；用途追到 `vt[0xF8]`（`0xB53263`）。
- [x] G4 不确定项标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对情况：无同名 C→S 请求（已在 §1 说明同族命令）。
