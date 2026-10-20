# 机器草案：线格式 —— CS-0x6DF1-lounge-btlroom_create

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x6DF1` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `btlroom_create` |
| 代码位置 | `0xb8fac0`..`0xb8fe7b` |
| 声明容量 | `0x82` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb8fb5c` |
| 2 | 4 | ? | bytes | `0xb8fb64` |
| 3 | ? | ? | bytes | `0xb8fb80` |
| 4 | ? | 4 | u32 | `0xb8fb9a` |
| 5 | ? | 4 | u32 | `0xb8fbb4` |
| 6 | ? | 1 | u8 | `0xb8fbce` |
| 7 | ? | 1 | u8 | `0xb8fbe8` |
| 8 | ? | 1 | u8 | `0xb8fc02` |

## 汇编证据序列（按线序）

```asm
; 0xb8fb5c  mov [eax] → 内联写 u32
; 0xb8fb64  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xb8fb80  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xb8fb9a  call sub_B02D80 → 写 u32
; 0xb8fbb4  call sub_B02D80 → 写 u32
; 0xb8fbce  call sub_B061C0 → 写 u8
; 0xb8fbe8  call sub_B061C0 → 写 u8
; 0xb8fc02  call sub_B061C0 → 写 u8
; —— 扫描停止于 0xb8fc46：call sub_B03020（非 IO）
```
