# SC-0xFD8A-examination_progress_r

> 状态：`DONE`
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xFD8A` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `battle_client` |
| 命令名 | `examination_progress_r` |
| 名字符串 | `)->_proto_battle_client::recv_examination_progress_r( ` @ `0xedd8c4` |
| 代码位置 | sub_B0CC20 @ `0xb0cc20`　块 `0xb30c68`..`0xb30ef6` |
| opcode 写入/分发证据 | `0xb30d94`（命令名字符串引用点 = case 归属锚点）|
| 处理块范围 | `0xB30C68`..`0xB30EF6` |
| 声明容量 | `0x58`（88） |
| 配对命令（同 opcode 反向） | （本批次内无同 opcode 反向命令） |

## 2. 结论摘要

- 结论：3 字段：`examination_info` 固定 5 元数组（元素 16B，读取器 4×u32，claim == 线长）+ 考核分数 + 剩余毫秒。容量 88 == 80+4+4 精确相等。
- 长度校验方式：处理块内「**游标 == 报文末尾**」闭合检查 @`0x00B30D4B`。
- 去向锚点：`vt[0x33C]`（3 个实参）。
- 是否分帧：否（单帧命令）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发给对应协议类的处理块 | `0xFD8A` | `0xb30d94` | 确证 |
| 1 | 0 | 80 | array<examination_info_entry,5> | `examination_info` | 考核记录列表（固定 5 项，**无线上 count**） | 阵列预留 `sub_B419B0`（claim 0x50=80 = 5×16）；元素读取器 `sub_B06BA0`（`0xB06BA0`）= 4×u32 = 16B，循环 5 次（`cmp edi,5`，步进 0x10）；去向 `vt[0x33C]` 第 3 实参（`0xB30ED7 push eax`） | 元素 16B / 槽 16B / 上限 5 | `0xB30CA9,0xB30CBA` | 确证 |
| 2 | 80 | 4 | u32 | `examination_playscore` | 考核得分 | `sub_B02DD0`（`0xB30CFB`）读 u32；去向 `vt[0x33C]` 第 2 实参（`0xB30ED6 push ecx`） | - | `0xB30CFB` | 确证 |
| 3 | 84 | 4 | u32 | `examination_playsec_remain_msec` | 考核剩余时间（毫秒） | `sub_B02DD0`（`0xB30D3B`）读 u32；去向 `vt[0x33C]` 第 1 实参（`0xB30ECF push ecx`） | - | `0xB30D3B` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
- 处理块 `0xB30C68..0xB30EF6`（battle_client 分发器 `0xB0CC20`）；守卫 = `sub_B05DA0(battle(0x10F))`，收尾 = `sub_B05D90`。
- 解码缓冲分配：`mov ecx,[esi+0Ch]` → `mov eax,[ecx]` → `mov edx,[eax+78h]` → `push 0x58; call edx`（`0x58` 为**容量**，非线长）。

### 4.2 长度闭合
- 闭合点：`0x00B30D4B`（游标寄存器与报文末尾比较，`jz`/`jnz` 走成功分支）。
- 容量校验：`0x58`=88 = 5×16 + 4 + 4 ✓（元素 claim 16 == 元素线长 16）。

### 4.3 元素复合体
- `examination_info` 的元素是 **`examination_info_entry`**（原记法 `array<4×u32,5>` ⇒ 元素名写成「4×u32」而非结构名）：
  读取器 `sub_B06BA0` 函数体消费 16B（4×u32）== `db_design/schema/composites/examination_info_entry.json` 的 `length`，
  槽步进 `0x10`、循环上界字面量 `cmp edi,5` 亦与该复合体证据一致。
- 所以 `fields.csv` 写 `array<examination_info_entry,5>`，服务端生成 `[]model.ExaminationInfoEntry`（不再是不透明 `[]byte`）。

### 4.4 存疑点
- 见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与长度校验一致（游标==末尾 @`0x00B30D4B`）
- [x] G2 每个字段的类型都能指回汇编 VA（未使用伪代码类型）
- [x] G3 每个字段都有含义与用途（含来源/去向锚点）
- [x] G4 不确定项标 `?` 且已记入 `notes.md`
- [x] G5 README / fields.csv / asm.md 三处一致
- [x] G6 INDEX 状态一致（`DONE`）
- [x] G7 配对命令互相链接
