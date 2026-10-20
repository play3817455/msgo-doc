# 机器草案：线格式 —— CS-0xADB6-lounge-shop_buy

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xADB6` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `shop_buy` |
| 代码位置 | `0xb9cd70`..`0xb9d179` |
| 声明容量 | `0x382` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 4 处条件跳转（`0xb9cde7`, `0xb9cdf8`, `0xb9ce09`, `0xb9cee4`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb9ce02` |
| 2 | 4 | 1 | u8 | `0xb9ce1b` |
| 3 | 5 | 4 | u32 | `0xb9ce23` |
| 4 | 9 | 1 | u8 | `0xb9ce3d` |
| 5 | 10 | 1 | u8 | `0xb9ce57` |
| 6 | 11 | 4 | u32 | `0xb9ce71` |
| 7 | 15 | ? | bytes | `0xb9ce8d` |
| 8 | ? | ? | bytes | `0xb9cea9` |
| 9 | ? | ? | bytes | `0xb9cec8` |

## 汇编证据序列（按线序）

```asm
; 0xb9ce02  mov [ecx] → 内联写 u32
; 0xb9ce1b  mov [edx] → 内联写 u8
; 0xb9ce23  call sub_B02D80 → 写 u32
; 0xb9ce3d  call sub_B061C0 → 写 u8
; 0xb9ce57  call sub_B061C0 → 写 u8
; 0xb9ce71  call sub_B02D80 → 写 u32
; 0xb9ce8d  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xb9cea9  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xb9cec8  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; —— 扫描停止于 0xb9cf0c：call sub_B03020（非 IO）
```
