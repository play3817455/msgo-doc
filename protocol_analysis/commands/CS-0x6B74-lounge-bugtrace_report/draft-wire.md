# 机器草案：线格式 —— CS-0x6B74-lounge-bugtrace_report

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x6B74` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `bugtrace_report` |
| 代码位置 | `0xba5be0`..`0xba5ece` |
| 声明容量 | `0x1816` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 4 处条件跳转（`0xba5c57`, `0xba5c68`, `0xba5c7b`, `0xba5cef`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xba5c72` |
| 2 | 4 | 4 | u32 | `0xba5c92` |
| 3 | 8 | ? | bytes | `0xba5c9a` |
| 4 | ? | 4 | u32 | `0xba5cb4` |
| 5 | ? | ? | bytes | `0xba5cd3` |

## 汇编证据序列（按线序）

```asm
; 0xba5c72  mov [eax] → 内联写 u32
; 0xba5c92  mov [eax] → 内联写 u32
; 0xba5c9a  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xba5cb4  call sub_B02D80 → 写 u32
; 0xba5cd3  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; —— 扫描停止于 0xba5d17：call sub_B03020（非 IO）
```
