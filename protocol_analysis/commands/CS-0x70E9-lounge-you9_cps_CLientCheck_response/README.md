# CS-0x70E9-lounge-you9_cps_CLientCheck_response

> 状态：`DONE`（2026-09-20，批次-19）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x70E9` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `you9_cps_CLientCheck_response` |
| 名字符串 | `)<-_proto_lounge_client::send_you9_cps_CLientCheck_response(` @ `0xeed168` |
| 代码位置 | sub_BA57D0 @ `0xba57d0`（`0xba57d0`..`0xba5bd6`） |
| opcode 写入证据 | `0xba5852` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0xA42`（2626） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令 | 无同名 S→C 应答；该命令为 CPS 自检链（参见 `topics\15/16/17`）的客户端上报 |

## 2. 结论摘要

- 结论：反外挂（XGameGuard/CPS）客户端自检结果上报：结果码 + 调用点/模块基址/大小/入口/模块名/全路径/描述串。
- 字段数：**9**（含 opcode 第 0 项）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 4 + 97 + 97 + 4 + 97 + 769 + 769 + 769 = 2608 ≤ 容量 0xA42 = 2626`（富余 18）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | `0x70E9` | `0xba5852` | 确证 |
| 1 | 2 | 4 | u32 | `cps_result` | 自检结果码（0=通过） | 来源=入参 arg_0（`mov ecx,[esp+48h+arg_0]`@0xBA585E）；内联 `mov [eax],ecx`；服务端据此判定是否放行 | 取值域 {0,1}（0=通过 / 1=异常；反外挂侧 `sub_A1D110` 以字面量 1 调包装 `sub_B00C30`@`0xA1D182`） | `0xBA586C` | 确证 |
| 2 | 6 | var | bytes | `call_address` | 触发自检的调用地址（串） | 来源=入参 arg_4；写线原语 `sub_B02B40`（NUL 串）；服务端据此定位被篡改的调用点 | 串槽预算 97（`push 61h`@0xBA5866） | `0xBA5874` | 确证 |
| 3 | var | var | bytes | `caller_md_base` | 调用者模块基址（串） | 来源=入参 arg_8；写线原语 `sub_B02B40`；服务端据此比对模块基址 | 串槽预算 97（`push 61h`@0xBA5888） | `0xBA5890` | 确证 |
| 4 | var | 4 | u32 | `caller_md_size` | 调用者模块大小 | 来源=入参 arg_C；写线原语 `sub_B02D80`；服务端据此校验模块完整性 | - | `0xBA58AA` | 确证 |
| 5 | var | var | bytes | `caller_md_entry` | 调用者模块入口点（串） | 来源=入参 arg_10；写线原语 `sub_B02B40` | 串槽预算 97（`push 61h`@0xBA58BE） | `0xBA58C6` | 确证 |
| 6 | var | var | bytes | `caller_md_base_name` | 调用者模块短名（串） | 来源=入参 arg_14；写线原语 `sub_B02B40` | 串槽预算 769（`push 301h`@0xBA58DA） | `0xBA58E5` | 确证 |
| 7 | var | var | bytes | `caller_md_full_name` | 调用者模块全路径（串） | 来源=入参 arg_18；写线原语 `sub_B02B40` | 串槽预算 769（`push 301h`） | `0xBA5904` | 确证 |
| 8 | var | var | bytes | `desc` | 自检描述/失败原因（串） | 来源=入参 arg_1C；写线原语 `sub_B02B40` | 串槽预算 769（`push 301h`） | `0xBA5923` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲
  （容量 `push` @ `0xba5816`）；`sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**，opcode 占 `buf+0..1`。
- opcode：`0xba5852`（`mov word ptr [...], 0x70E9`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），
  **日志名序 == 线序**；去向统一为发送槽 `vt[0x58](buf, 负载长度)`。

### 4.2 长度闭合
- `2 + 4 + 97 + 97 + 4 + 97 + 769 + 769 + 769 = 2608 ≤ 容量 0xA42 = 2626`（富余 18）

### 4.3 存疑点
- `caller_md_base` / `caller_md_entry` 在线上是**字符串**（写线原语 `sub_B02B40`），不是整数——按写线指令判定，不得按语义直觉改成 u32。
- `cps_result` 取值域 {0,1}（0=通过 / 1=异常；反外挂侧 `sub_A1D110` 以字面量 1 调包装 `sub_B00C30`@`0xA1D182`）。
- 容量 0xA42 为「上限场景」：Σ 线长 2608 ≤ 2626（富余 18）。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / §4.3 / notes.md）
