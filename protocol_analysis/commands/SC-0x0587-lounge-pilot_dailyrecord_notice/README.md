# SC-0x0587-pilot_dailyrecord_notice

> 状态：`DONE`（2026-09-20，批次-2）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x0587` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_dailyrecord_notice` |
| 名字符串 | `)->_proto_lounge_client::recv_pilot_dailyrecord_notice( ` @ `0xEE9FA4`，引用点 `0xB535BD` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB5351A` .. `0xB53684`（块首 `0xB5351A call sub_B41120`，错误码 `0x6D`） |
| 关联命令 | 配对（同族「每日战绩」）：`../CS-0xB184-lounge-pilot_dailyrecord_get/`、`../SC-0x81F1-lounge-pilot_dailyrecord_get_r/`、`../CS-0x2EE8-lounge-pilot_dailyrecord_collect_complete/`、`../SC-0xDFC2-lounge-pilot_dailyrecord_collect_complete_r/`；本命令**无同名发送侧**（服务端主动通知） |

## 2. 结论摘要

- **报文体总长：定长 `1` 字节**（单个 u8）。
- 负载 = 1 个 u8（`is_open_info`，开关）。
- 长度校验：`0xB5358F mov ebx,[esp+var_2C44]`（游标）、`0xB53593 cmp ebx,[esp+var_2C40]`（vs 报文末尾）、`0xB53597 jnz 错误`⇒ **整包精确消费完**。
- 声明容量 `push 1`（`0xB5352F`）= 1，**与线长相等** ✓。
- 是否分帧：否。
- 关键结论：单值交 `vt[0x160]`（`0xB5365F` 取虚表项 / `0xB53668` 调用），实参为**零扩展**后的 u8（`0xB5365A movzx ecx, byte ptr [eax]`）⇒ 线上 1 字节，实参按 32 位传递。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x0587` | `0xB535BD`（名字串引用点） | 确证 |
| 1 | 0 | 1 | u8 | `is_open_info` | 「每日战绩」信息是否开放（开关） | 交 `vt[0x160]`（`0xB53668`，实参为零扩展 u8）；日志 `is_open_info=`（`0xB5360C`，打印器 `sub_B0C1F0`：布尔/单字节专用） | `?`（0/1 语义与其它取值未确证，见 `notes.md` Q1） | `0xB5356A`（`sub_B06230`）；`0xB06249 add [eax],1`；日志 `0xB5360C` | 类型确证 / 枚举待定 |
| — | 1 | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB53593`（`cmp`）、`0xB53597`（`jnz` 错误） | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE9FA4` 的引用点 `0xB535BD` 落在 `sub_B51930` 的 case 块 `0xB5351A..0xB53684` 内。
2. 块首 `0xB5351A call sub_B41120` 与全部错误路径（`0xB53581`、`0xB53597`）一致使用错误码 `0x6D`。
3. 读取路径：`0xB5354C lea ecx,&var_2C48` → `0xB5355B call sub_B05E30`（缓冲预留 1B，**非字段**）→ `0xB5356A call sub_B06230`（唯一字段，u8）。

### 4.2 长度闭合
- u8 读取器 `sub_B06230` 自带「剩余 ≥ 1」边界检查（`0xB06236 lea edx,[ecx+1]`），成功分支 `0xB06249 add dword ptr [eax],1` ⇒ 游标 +1。
- `1`（字段）== `1`（声明容量）== 校验点游标增量 ⇒ 闭合 ✓。

### 4.3 存疑点
见 `notes.md`（`is_open_info` 的取值语义、`vt[0x160]` 去向、`sub_B0C1F0` 打印器口径）。

## 5. 质量门自检

- [x] G1 字段表总长（1）与 `0xB53597` 的「游标 == 末尾」校验一致；容量 1 == 负载 1。
- [x] G2 线类型指回汇编 VA（u8：`0xB5356A` 读 + `0xB06249` 游标 +1）；未使用伪代码类型。
- [x] G3 含义取自块内日志串 `is_open_info=`（`0xB5360C`），用途追到 `vt[0x160]`（`0xB53668`）。
- [x] G4 不确定项（枚举）标 `?` 且已记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 本命令无同名配对请求（已链接同族「每日战绩」命令）。
