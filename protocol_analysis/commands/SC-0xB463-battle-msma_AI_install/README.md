# SC-0xB463-battle-msma_AI_install

> 状态：`DONE`（2026-09-20，批次-12）
> 方向：服务端 → 客户端（recv）
> 协议类：`battle_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xB463` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `battle_client` |
| 命令名 | `msma_AI_install` |
| 处理块范围 | `0xb29503`..`0xb2970a` |
| 名字串引用点 | `0xb295f6` |
| 声明容量（解码缓冲） | `0xAA`（`B2951C`） |
| 长度闭合点 | `B295AD` |
| 报错码 | `0xB5`（块内 `push 1; push <errcode>; vt[0x64]`） |
| 去向 | `vt[0x240]` @`B296D1`（2 实参） |

## 2. 结论摘要

- **报文体线长**：`167`（ms 段定长 165）。
- 容量关系：容量 `0xAA` = 170 = `2 + 168(AI 结构体 claim)`（**精确相等**）。
- 长度闭合：块末 `B295AD` 处校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**2**（不含 opcode）；去向：`vt[0x240]` @`B296D1`（2 实参）。
- 类型：固定 + 一个定长结构体块。
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0xB463` | `0xb295f6` | 确证 |
| 1 | 0 | 2 | u16 | `AI_ent_id` | AI 实体 ID（日志串 `AI_ent_id=`） | 经 `vt[0x240]` 交业务（2 实参） | - | B2955D | 确证 |
| 2 | 2 | 165 | struct | `AI` | AI 参数结构体（跨度 168B / 线上 165B；日志串 `AI=`）；成员见 `db_design/schema/composites/AI.json` | 经 `vt[0x240]` 交业务 | - | B2958E|B2959D | 确证 |
| - | - | - | - | （长度闭合） | 游标必须 == 报文末尾 | - | - | `B295AD` | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb295f6` 落在处理块 `0xb29503`..`0xb2970a` 内。
2. 容量经「`mov edx,[eax+78h]`（解码缓冲分配器）+ `push IMM; call edx`」在 `B2951C` 确证为 `0xAA`。
3. 逐字段按线序读取，类型全部由汇编判定（SOP §6）。
4. 闭合：`B295AD`（SOP §5.3）。
5. 去向：`vt[0x240]` @`B296D1`（2 实参）。

### 4.2 长度闭合与容量口径
- 容量 `0xAA` = 170 = `u16(AI_ent_id) + 168`：`AI` 块由 `sub_B060C0` 预留单槽 **0xA8=168**，线长由 `sub_B07230` 整函数展开实算 **165**（跨度 168 ≠ 线长 165）。
- 线长 = `2 + 165` = 167。

### 4.3 结构/数组说明
- `sub_B07230`（`0xB07230..B07531`）含 4 处定长循环（`cmp ecx,21h`=33、`cmp eax,0Ah`=10、`cmp ecx,0Ah`=10、`cmp ecx,0Ah`=10），整函数展开后消费 **165B**。
- 后续复核已把 165B 线结构拆成 `db_design/schema/composites/AI.json`：`type/name/param_id/action_type/move_spd/stat/hate_ent_id/hate_val/pop_init_x/y/z/dir/fire_start/end/move_end/order_kind/order_param/group_id/center_ms_entid/route_number/formation_id/formation_number/stuck_escape`。其中 `pop_init_x/y/z/dir` 是出现初始坐标/朝向字段名，因此不得再概括成“AI 包没有出生坐标”。
- 本 README 只记录线序和长度证据；成员布局/偏移以 composite schema 为准。字段存在已由结构读线拆解，字段业务单位、符号表示、初始化与实体创建关系不由线长本身证明。

### 4.4 存疑点
见 `notes.md`。特别是 `AI_ent_id` 是否引用已注册实体、接收端缺实体时的处理、`param_id` 对应模板、初始坐标单位/符号仍待正确客户端业务消费者证据。

## 5. 质量门自检

- [x] G1 字段表总长与客户端长度闭合一致（或已说明为何无法闭合）
- [x] G2 每个字段的线类型都能指回汇编证据 VA，未使用伪代码类型
- [x] G3 每个字段都有含义与用途（或明确标注仅回显/仅日志并给证据）
- [x] G4 不确定项全部显式标 `?` 且已记入 `notes.md`
- [x] G5 `README.md` / `fields.csv` / `asm.md` 三处一致
- [x] G6 INDEX 该行状态与文件夹内容一致（`DONE`）
- [x] G7 有配对请求/应答的命令已互相链接
