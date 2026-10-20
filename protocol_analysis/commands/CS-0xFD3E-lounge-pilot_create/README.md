# CS-0xFD3E-lounge-pilot_create

> 状态：`DONE`（2026-09-20，批次-23）
> 方向：客户端 → 服务端（send）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xFD3E` |
| 方向 | CS（客户端 → 服务端） |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_create` |
| 名字符串 | `)<-_proto_lounge_client::send_pilot_create( ` @ `0x00EEA340` |
| 代码位置 | `sub_B8A100` @ `0x00B8A100`（`0x00B8A100`..`0x00B8A303`） |
| opcode 写入证据 | `0x00B8A184` |
| 处理块范围 | `-` .. `-`（C→S 无 case 块） |
| 声明容量 | `0xA6`（166） |
| 容量申请证据 | `0x00B8A143`（分配器 `[obj+0Ch]` 的 `vt[0x78]`） |
| 发送去向 | `vt[0x58]`（客户端对象虚表槽）；`call vt[0x58](buf, 负载长度)` @ `0x00B8A294` |
| 提交 | `sub_B02FF0` @ `0x00B8A20F` |
| 附加通知回调 | `[obj+79A8h]`（模块 id `0xF`） |
| 配对命令 | S→C `SC-0xC43C-lounge-pilot_create_r` |

## 2. 结论摘要

- 字段数：**3**（含 opcode 第 0 项）
- 长度校验方式：组包消费量（Σ 字段线长）与声明容量对照（C→S：`容量 ≥ 负载 + 2`）
- 是否分帧：否（单帧命令）
- 容量等式：`2 + 159 + 4 = 165 ≤ 容量 0xA6 = 166`（富余 1）

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**（写线指令操作数宽度 / 写线原语），禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 0 | 2 | u16 | opcode | 命令号 | 写入 `buf+0`，供服务端分发；无 case 块（C→S） | 0xFD3E | `00B8A184` | 确证 |
| 1 | 0 | 159 | struct(pilot) | pilot | 新建驾驶员完整信息（159B；成员逐项见 §3.1，成员名取自打印器 `sub_B08AD0`） | 来源=入参 `arg_0`（结构体指针）→ 复合写入器 `sub_B06360`(@`0xB8A18E`，函数体 `0xB06360..0xB06579` 逐字段累加 = **159B**) | - | `0xB8A18E` | 确证 |
| 2 | 159 | 4 | u32 | slot | 驾驶员存放槽位序号 | 来源=入参 `arg_4` → 内联写 `[eax],ecx`(@`0xB8A1B3`) | - | `0xB8A1B3` | 确证 |

（与 `fields.csv` 必须完全一致）

§3.1 `pilot` 结构体成员（写入器 `sub_B06360` 偏移 ↔ 打印器 `sub_B08AD0` 名，共 159B）

| 偏移 | 长度 | 线类型 | 字段名 | 含义 |
|---|---|---|---|---|
| 0x0 | 4 | u32 | `pilot_id` | 驾驶员 ID |
| 0x4 | 25 | u8[25] | `name` | 驾驶员名（NUL 结尾，定长 25 槽） |
| 0x1D | 1 | i8 | `troops` | 所属阵营 |
| 0x1E | 1 | i8 | `level` | 等级 |
| 0x1F | 1 | i8 | `mil_class` | 军衔阶级 |
| 0x20 | 2 | u16 | `byword` | 口头禅（byword 表 ID） |
| 0x24 | 4 | u32 | `cmdr_fame` | 指挥官功勋 |
| 0x28 | 2 | u16 | `rate_vslocal` | 对本服胜率 |
| 0x2A | 2 | u16 | `rate_vslocal_4ev` | 对本服胜率（4 人战） |
| 0x2C | 2 | u16 | `rate_vslocal_clan` | 对本服胜率（部队战） |
| 0x30 | 4 | u32 | `level_point` | 等级点数 |
| 0x34 | 18 | avatar(18B) | `avatar` | 外观（写原语 `sub_B06290`；打印器 `sub_B08920`） |
| 0x4C | 4 | u32 | `clan_id` | 所属部队 ID |
| 0x50 | 31 | u8[31] | `clan_name` | 部队名（NUL 结尾，定长 31 槽） |
| 0x6F | 1 | i8 | `clan_emb_base` | 部队徽章底图 |
| 0x70 | 1 | i8 | `clan_emb_parts1` | 部队徽章部件 1 |
| 0x71 | 1 | i8 | `clan_emb_parts2` | 部队徽章部件 2 |
| 0x74 | 4 | u32 | `cupteam_id` | 杯赛队伍 ID |
| 0x78 | 31 | u8[31] | `cupteam_name` | 杯赛队伍名（NUL 结尾，定长 31 槽） |
| 0x98 | 4 | u32 | `accum_point` | 累计点数 |
| 0x9C | 4 | u32 | `rank` | 名次/顺位 |
| 0xA0 | 4 | u32 | `base_accump` | 基础累计点 |
| 0xA4 | 4 | u32 | `req_accump` | 所需累计点 |
| 0xA8 | 4 | u32 | `penalty` | 惩罚值 |

## 4. 分析记录

### 4.1 定位过程
- 分配器指纹：`mov ecx,[obj+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push <容量>; call edx`；写线游标由 `sub_ABB2F0` 初始化 `{cur,end}`，**游标自 `buf+2` 起**（opcode 占 `buf+0..1`）。
- opcode：`0x00B8A184`。
- 字段名取证 = **提交（`sub_B02FF0`）之后**的 trace 打印块（`push offset a<Name>; … call sub_41D990`），**日志名序 == 线序**。打印器宽度：`sub_B03580`=u32 / `sub_B032A0`=u16 / `sub_B08500`=u64 / `sub_B0C1F0`=单字节（`movsx`，仅打印符号扩展，不改线宽）。
- 发送去向统一为 `vt[0x58](buf, 负载长度)`：`mov edx,[edi]; mov eax,[edx+58h]; sub <len>,<buf>; push <len>; push <buf>; mov ecx,<obj>; call eax`。

### 4.2 长度闭合
- `2 + 159 + 4 = 165 ≤ 容量 0xA6 = 166`（富余 1）

### 4.3 存疑点
- 见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（Σ 线长 ≤ 容量，已列等式）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接（见 §1 / `notes.md`）
