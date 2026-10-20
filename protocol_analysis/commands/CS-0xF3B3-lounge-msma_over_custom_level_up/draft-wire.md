# 机器草案：线格式 —— CS-0xF3B3-lounge-msma_over_custom_level_up

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xF3B3` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `msma_over_custom_level_up` |
| 代码位置 | `0xba7ce0`..`0xba7ed2` |
| 声明容量 | `0xE` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 4 处条件跳转（`0xba7d49`, `0xba7d5a`, `0xba7d72`, `0xba7d86`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xba7d64` |
| 2 | 4 | 4 | u32 | `0xba7d6f` |
| 3 | 8 | 4 | u32 | `0xba7d7c` |

## 汇编证据序列（按线序）

```asm
; 0xba7d64  mov [eax] → 内联写 u32
; 0xba7d6f  mov [eax+4] → 内联写 u32
; 0xba7d7c  mov [edx] → 内联写 u32
; —— 扫描停止于 0xba7dae：call sub_B03020（非 IO）
```
