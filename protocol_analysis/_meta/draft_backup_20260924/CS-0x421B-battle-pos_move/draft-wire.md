# 机器草案：线格式 —— CS-0x421B-battle-pos_move

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x421B` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `pos_move` |
| 代码位置 | `0xb351d0`..`0xb3597f` |
| 声明容量 | `0xAA` |
| 字段总长 | **47** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb3526d` |
| 2 | 4 | 2 | u16 | `0xb35286` |
| 3 | 6 | 2 | u16 | `0xb3528e` |
| 4 | 8 | 2 | u16 | `0xb352a7` |
| 5 | 10 | 2 | u16 | `0xb352c0` |
| 6 | 12 | 2 | u16 | `0xb352d9` |
| 7 | 14 | 2 | u16 | `0xb352f2` |
| 8 | 16 | 2 | u16 | `0xb3530b` |
| 9 | 18 | 2 | u16 | `0xb35324` |
| 10 | 20 | 4 | u32 | `0xb3533d` |
| 11 | 24 | 2 | u16 | `0xb35356` |
| 12 | 26 | 2 | u16 | `0xb3536f` |
| 13 | 28 | 1 | u8 | `0xb35388` |
| 14 | 29 | 1 | u8 | `0xb353a1` |
| 15 | 30 | 2 | u16 | `0xb353ba` |
| 16 | 32 | 2 | u16 | `0xb353d3` |
| 17 | 34 | 2 | u16 | `0xb353ec` |
| 18 | 36 | 2 | u16 | `0xb35405` |
| 19 | 38 | 2 | u16 | `0xb3541e` |
| 20 | 40 | 2 | u16 | `0xb35437` |
| 21 | 42 | 1 | u8 | `0xb35450` |
| 22 | 43 | 4 | u32 | `0xb35475` |

## 汇编证据序列（按线序）

```asm
; 0xb3526d  mov [ecx] → 内联写 u32
; 0xb35286  mov [edx] → 内联写 u16
; 0xb3528e  call sub_B02DA0 → 写 u16
; 0xb352a7  call sub_B02DA0 → 写 u16
; 0xb352c0  call sub_B02DA0 → 写 u16
; 0xb352d9  call sub_B02DA0 → 写 u16
; 0xb352f2  call sub_B02DA0 → 写 u16
; 0xb3530b  call sub_B02DA0 → 写 u16
; 0xb35324  call sub_B02DA0 → 写 u16
; 0xb3533d  call sub_B02D80 → 写 u32
; 0xb35356  call sub_B02DA0 → 写 u16
; 0xb3536f  call sub_B02DA0 → 写 u16
; 0xb35388  call sub_B061C0 → 写 u8
; 0xb353a1  call sub_B061C0 → 写 u8
; 0xb353ba  call sub_B02DA0 → 写 u16
; 0xb353d3  call sub_B02DA0 → 写 u16
; 0xb353ec  call sub_B02DA0 → 写 u16
; 0xb35405  call sub_B02DA0 → 写 u16
; 0xb3541e  call sub_B02DA0 → 写 u16
; 0xb35437  call sub_B02DA0 → 写 u16
; 0xb35450  call sub_B061C0 → 写 u8
; 0xb35475  call sub_B02D80 → 写 u32
; —— 扫描停止于 0xb3549c：call sub_B065D0（非 IO）
```
