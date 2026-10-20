# 机器草案：线格式 —— CS-0x5F28-lounge-speedhack_check_response

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x5F28` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `speedhack_check_response` |
| 代码位置 | `0xba4d50`..`0xba4f3a` |
| 声明容量 | `0xA` |
| 字段总长 | **4** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xba4dda` |
| 2 | 2 | 2 | u16 | `0xba4de8` |

## 汇编证据序列（按线序）

```asm
; 0xba4dda  mov [eax] → 内联写 u16
; 0xba4de8  mov [edx] → 内联写 u16
; —— 扫描停止于 0xba4e1b：call sub_B03020（非 IO）
```
