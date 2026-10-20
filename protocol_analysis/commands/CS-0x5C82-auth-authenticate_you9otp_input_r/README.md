# CS-0x5C82-auth-authenticate_you9otp_input_r

> 状态：`DONE`
> 方向：客户端 → 服务端（send）
> 协议类：`auth_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x5C82` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `auth_client` |
| 命令名 | `authenticate_you9otp_input_r` |
| 名字符串 | `)<-_proto_auth_client::send_authenticate_you9otp_input_r(` @ `0xedb048` |
| 代码位置 | sub_B05370 @ `0xb05370`（`0xb05370`..`0xb055cf`） |
| opcode 写入证据 | `0xb053e9` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0x26`（38） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` |
| 配对命令（同 opcode 反向） | 见 §4.3 与其他命令的关联 / INDEX 反向表 |

## 2. 结论摘要

- 结论：auth 阶段 you9 OTP 输入：OTP 类型 + 矩阵码 + 输入码。
- 字段数：**4**（含 opcode）。
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载`）。
- 是否分帧：否（单帧命令）。
- 容量等式：`2 + 4 + 17 + 9 = 32 ≤ 容量 0x26=38（富余 6）`

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | `opcode` | 命令号 | 分发给 auth 协议类处理块（C→S 无 case 块） | 0x5C82 | `0xB053E9` | 确证 |
| 1 | 2 | 4 | u32 | `otp_type` | OTP 类型 | 来源=入参 arg_0（@0xB053F5）；内联 `mov [eax],ecx`（4 字节目标）；经 `vt[0x58]` 发送 | - | `0xB05403` | 确证 |
| 2 | 6 | var | bytes | `otp_matrix_code` | OTP 矩阵码串（NUL 结尾） | 来源=入参 arg_4（@0xB05405）；写线原语 `sub_B02B40`；服务端据此还原矩阵 | slot 预算 17（`push 0x11`@0xB053FD） | `0xB0540B` | 确证 |
| 3 | var | var | bytes | `input_otp` | 用户输入的 OTP 串（NUL 结尾） | 来源=入参 arg_8（@0xB0541B）；写线原语 `sub_B02B40`；服务端据此校验 | slot 预算 9（`push 9`@0xB0541F） | `0xB05427` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov <reg>,[<obj+0Ch>]` → `mov <reg>,[eax+78h]` → `push <容量>; call <reg>` 取得组包缓冲（游标自 `buf+2` 起，opcode 占 `buf+0..1`）。
- 字段名取自**提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; …; call sub_41D990`），**日志名序 == 线序**。

### 4.2 长度闭合
- 2 + 4 + 17 + 9 = 32 ≤ 容量 0x26=38（富余 6）

### 4.3 存疑点
- 日志名序（`otp_type=`→`otp_matrix_code=`→`input_otp=`）与线序一致。
- ★ 串槽预算书写形态：第一个为 `push 11h`（带 `h` 后缀），第二个为 `push 9`（**十进制无后缀**）⇒ 立即数解析须同时接受两种写法（承批次-17 第 ⑤ 坑）。
- 与 S→C `SC-0x60E0-auth-authenticate_you9otp_input` 构成请求/应答对。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §4 / notes.md）
