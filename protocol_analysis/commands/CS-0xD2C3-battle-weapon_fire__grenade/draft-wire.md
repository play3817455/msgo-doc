# 机器草案：线格式 —— CS-0xD2C3-battle-weapon_fire__grenade

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xD2C3` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__grenade` |
| 代码位置 | `0xb372d0`..`0xb379e5` |
| 声明容量 | `0x5A` |
| 字段总长 | **46** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 4 处条件跳转（`0xb37346`, `0xb37356`, `0xb37366`, `0xb37573`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb3735f` |
| 2 | 4 | 2 | u16 | `0xb37378` |
| 3 | 6 | 2 | u16 | `0xb37380` |
| 4 | 8 | 2 | u16 | `0xb37399` |
| 5 | 10 | 2 | u16 | `0xb373b2` |
| 6 | 12 | 2 | u16 | `0xb373cb` |
| 7 | 14 | 2 | u16 | `0xb373e4` |
| 8 | 16 | 2 | u16 | `0xb373fd` |
| 9 | 18 | 2 | u16 | `0xb37416` |
| 10 | 20 | 2 | u16 | `0xb3742f` |
| 11 | 22 | 2 | u16 | `0xb37448` |
| 12 | 24 | 2 | u16 | `0xb37461` |
| 13 | 26 | 1 | u8 | `0xb3747a` |
| 14 | 27 | 1 | u8 | `0xb37493` |
| 15 | 28 | 4 | u32 | `0xb374ac` |
| 16 | 32 | 4 | u32 | `0xb374c5` |
| 17 | 36 | 1 | u8 | `0xb374de` |
| 18 | 37 | 4 | u32 | `0xb374f7` |
| 19 | 41 | 2 | u16 | `0xb37510` |
| 20 | 43 | 1 | u8 | `0xb37529` |
| 21 | 44 | 1 | u8 | `0xb37542` |
| 22 | 45 | 1 | u8 | `0xb3755b` |

## 汇编证据序列（按线序）

```asm
; 0xb3735f  mov [ecx] → 内联写 u32
; 0xb37378  mov [edx] → 内联写 u16
; 0xb37380  call sub_B02DA0 → 写 u16
; 0xb37399  call sub_B02DA0 → 写 u16
; 0xb373b2  call sub_B02DA0 → 写 u16
; 0xb373cb  call sub_B02DA0 → 写 u16
; 0xb373e4  call sub_B02DA0 → 写 u16
; 0xb373fd  call sub_B02DA0 → 写 u16
; 0xb37416  call sub_B02DA0 → 写 u16
; 0xb3742f  call sub_B02DA0 → 写 u16
; 0xb37448  call sub_B02DA0 → 写 u16
; 0xb37461  call sub_B02DA0 → 写 u16
; 0xb3747a  call sub_B061C0 → 写 u8
; 0xb37493  call sub_B061C0 → 写 u8
; 0xb374ac  call sub_B02D80 → 写 u32
; 0xb374c5  call sub_B02D80 → 写 u32
; 0xb374de  call sub_B061C0 → 写 u8
; 0xb374f7  call sub_B02D80 → 写 u32
; 0xb37510  call sub_B02DA0 → 写 u16
; 0xb37529  call sub_B061C0 → 写 u8
; 0xb37542  call sub_B061C0 → 写 u8
; 0xb3755b  call sub_B061C0 → 写 u8
; —— 扫描停止于 0xb3759b：call sub_B03020（非 IO）
```
