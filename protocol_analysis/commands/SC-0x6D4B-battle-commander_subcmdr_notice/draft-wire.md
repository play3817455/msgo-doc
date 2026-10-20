# 机器草案：线格式 —— SC-0x6D4B-battle-commander_subcmdr_notice

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x6D4B` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `commander_subcmdr_notice` |
| 代码位置 | `0xb1df1e`..`0xb1e268` |
| 声明容量 | `0x1A0` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 3 处条件跳转（`0xb1df99`, `0xb1dfb1`, `0xb1dfe0`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb1df6a` |
| 2 | 4 | 4 | u32[] | `0xb1dfa8` |
| 3 | 8 | 4 | u32 | `0xb1dfca` |

## 汇编证据序列（按线序）

```asm
; 0xb1df6a  call sub_B02DD0 → 读 u32
; 0xb1dfa8  call sub_B41850 → 读 u32（数组）
; 0xb1dfca  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb1dfe2：jmp
```
