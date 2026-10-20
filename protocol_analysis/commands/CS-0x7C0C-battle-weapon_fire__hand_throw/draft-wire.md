# 机器草案：线格式 —— CS-0x7C0C-battle-weapon_fire__hand_throw

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x7C0C` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__hand_throw` |
| 代码位置 | `0xb379f0`..`0xb37f5c` |
| 声明容量 | `0x3E` |
| 字段总长 | **30** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 4 处条件跳转（`0xb37a61`, `0xb37a72`, `0xb37a83`, `0xb37bfc`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb37a7c` |
| 2 | 4 | 2 | u16 | `0xb37a96` |
| 3 | 6 | 2 | u16 | `0xb37a9f` |
| 4 | 8 | 2 | u16 | `0xb37ab9` |
| 5 | 10 | 2 | u16 | `0xb37ad3` |
| 6 | 12 | 2 | u16 | `0xb37aed` |
| 7 | 14 | 2 | u16 | `0xb37b07` |
| 8 | 16 | 2 | u16 | `0xb37b21` |
| 9 | 18 | 2 | u16 | `0xb37b3b` |
| 10 | 20 | 1 | u8 | `0xb37b55` |
| 11 | 21 | 1 | u8 | `0xb37b6f` |
| 12 | 22 | 4 | u32 | `0xb37b89` |
| 13 | 26 | 1 | u8 | `0xb37ba6` |
| 14 | 27 | 2 | u16 | `0xb37bc3` |
| 15 | 29 | 1 | u8 | `0xb37be0` |

## 汇编证据序列（按线序）

```asm
; 0xb37a7c  mov [ecx] → 内联写 u32
; 0xb37a96  mov [edx] → 内联写 u16
; 0xb37a9f  call sub_B02DA0 → 写 u16
; 0xb37ab9  call sub_B02DA0 → 写 u16
; 0xb37ad3  call sub_B02DA0 → 写 u16
; 0xb37aed  call sub_B02DA0 → 写 u16
; 0xb37b07  call sub_B02DA0 → 写 u16
; 0xb37b21  call sub_B02DA0 → 写 u16
; 0xb37b3b  call sub_B02DA0 → 写 u16
; 0xb37b55  call sub_B061C0 → 写 u8
; 0xb37b6f  call sub_B061C0 → 写 u8
; 0xb37b89  call sub_B02D80 → 写 u32
; 0xb37ba6  call sub_B061C0 → 写 u8
; 0xb37bc3  call sub_B02DA0 → 写 u16
; 0xb37be0  call sub_B061C0 → 写 u8
; —— 扫描停止于 0xb37c24：call sub_B03020（非 IO）
```
