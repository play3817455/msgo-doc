# protocol_analysis —— 客户端/服务端命令 · 组包格式分析

> 全新分析目录。**不引用本目录以外的历史结论**，一切以 IDA 静态证据为准。
> 作业依据：`00-规范-组包格式分析SOP.md`（动手前必读）。

## 本目录要解决什么

客户端（`GundamOnline_CHINA_v15.exe`）与服务端之间往来的**每一条命令**，
逐条给出线格式定义：**字段顺序 / 偏移 / 长度 / 类型 / 含义 / 用途**，且每项都有汇编级证据。

- **C→S**：组包代码就在客户端里，**直接可读**（写线即真相）。
- **S→C**：看不到组包代码，**按客户端的消费方式反推**（消费即真相）。
- **字段类型**：只用汇编判定，**禁止**采信伪代码的类型声明。

## 快速上手（新会话按顺序读）

1. `00-规范-组包格式分析SOP.md` —— 规范（唯一作业依据，含质量门与禁止事项）。
2. `INDEX-命令总表.md` —— 命令目录索引（S→C 563 条 + C→S 351 条，每条指向一个文件夹）。
3. `_meta/命令发现方法.md` —— 命令全集是怎么从 exe 里挖出来的（原理 + 校验数据）。
4. `_meta/环境与工具约定.md` —— IDB、地址口径、工具运行方式、静态分析纪律。
5. `commands/<方向>-<opcode>-<名字>/README.md` —— 单条命令的分析产物。
6. `_template-命令文件夹/` —— 新建命令分析时的模板。

## 当前进度（阶段一：命令全集枚举 —— 已完成）

| 项 | 数量 | 来源 |
|---|---|---|
| S→C 命令（`recv_*`） | 564 | 3 个分发器（auth 8 / battle 205 / lounge 350）+ 1 条不经分发器（`_proto_battle::recv_entity_msma_fix` @`0xB0C210`，opcode `0x20F5`） |
| C→S 命令（`send_*`） | 351 | 351 个组包函数（350 条 `_client` + 1 条 `_proto_battle`） |
| 合计 | 915 | 全部已解出 opcode（0 条失败） |
| 字段级分析（阶段二） | **2 DONE / 913 DRAFT** | 见 INDEX 状态列 |
| 机器草案自校验 | S→C PASS 429 / C→S PASS 229 / **FAIL 0** | 全定长命令「容量 vs 线长」，0 条超容量 ⇒ 无重复计数 |

> `DRAFT` = 已出机器草案：**类型/偏移/长度/证据全部来自汇编**，但「含义/用途」待人工补齐（未过质量门 G3）。
> 草案文件：各命令文件夹下的 `draft-wire.md` + `draft-fields.csv`（生成物，勿手工编辑）。

**样例（照它抄格式）**：

| 命令 | 特点 |
|---|---|
| `commands/SC-0xA103-auth-authenticate_bnpotp_input/` | **0 负载**的认证通知（线长 2 字节），示范「怎么证否字段」 |
| `commands/SC-0x20F5-battle-entity_msma_fix/` | **不经分发器**的 recv（由分发器默认分支调用），示范 orphan 处理与 6 字段闭合 |

分发器：`auth_client @0xB03D30`、`battle_client @0xB0CC20`、`lounge_client @0xB51930`。

## 目录结构

```
protocol_analysis/
├── 00-规范-组包格式分析SOP.md
├── README.md                     ← 本文件
├── INDEX-命令总表.md
├── _meta/                        ← 命令发现方法 / 环境约定 / 原始提取结果
├── _template-命令文件夹/         ← 模板
├── commands/                     ← 914 个命令文件夹
└── tools/                        ← 提取 / 生成索引 / 校验 脚本
```

## 一条命令的分析产物（4 件套）

| 文件 | 内容 |
|---|---|
| `README.md` | 主文档：命令元信息 + 帧格式总表 + 结论摘要 + 状态 |
| `fields.csv` | 字段表（机器可读），与 README 字段表必须一致 |
| `asm.md` | 汇编证据切片（每段带 VA + 一句「说明了什么」） |
| `notes.md` | 未决问题、反例、与其他命令的关联 |
| `draft-wire.md` / `draft-fields.csv` | **机器草案（生成物）**：字段序列 + 证据 + 自校验，供人工定稿时抄录 |

## 重新生成索引 / 校验

```powershell
# 1) 在 IDA 中重跑提取（可选，命令集有变化时）
#    IDA MCP: py_exec_file  →  tools\ida_extract_commands.py

# 2) IDA 中诊断「case 块 ↔ opcode ↔ 名字」三方对照（查无名块/别名/伪 case）
#    IDA MCP: py_exec_file  →  tools\ida_diag_cases.py

# 3) IDA 中批量生成线格式草案（每命令 draft-wire.md / draft-fields.csv）
#    IDA MCP: py_exec_file  →  tools\ida_draft_wire.py

# 4) 由 JSON 生成 INDEX 与命令文件夹骨架（默认不覆盖已存在的分析产物）
python protocol_analysis\tools\build_index.py

# 5) 校验 INDEX / 文件夹 / JSON 三者一致
python protocol_analysis\tools\verify_index.py
```

## 三条最容易被忽略的纪律

1. 线长 = **实际消费字节数**；`alloc(N)` 的 `N` 与结构体大小都**不是**线长。
2. 字段类型必须能指回一条**汇编指令地址**；伪代码的类型声明不作数。
3. **不确定就标 `?`**，并写进该命令的 `notes.md`；禁止猜。
