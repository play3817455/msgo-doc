# 机器草案：线格式 —— CS-0x8898-battle-weapon_fire__damage_field

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x8898` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__damage_field` |
| 代码位置 | `0xb3ad30`..`0xb3b342` |
| 声明容量 | `0x4A` |
| 字段总长 | **39** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 4 处条件跳转（`0xb3ada6`, `0xb3adb6`, `0xb3adc6`, `0xb3af6f`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb3adbf` |
| 2 | 4 | 2 | u16 | `0xb3add8` |
| 3 | 6 | 2 | u16 | `0xb3ade0` |
| 4 | 8 | 2 | u16 | `0xb3adf9` |
| 5 | 10 | 2 | u16 | `0xb3ae12` |
| 6 | 12 | 2 | u16 | `0xb3ae2b` |
| 7 | 14 | 2 | u16 | `0xb3ae44` |
| 8 | 16 | 2 | u16 | `0xb3ae5d` |
| 9 | 18 | 2 | u16 | `0xb3ae76` |
| 10 | 20 | 2 | u16 | `0xb3ae8f` |
| 11 | 22 | 2 | u16 | `0xb3aea8` |
| 12 | 24 | 2 | u16 | `0xb3aec1` |
| 13 | 26 | 1 | u8 | `0xb3aeda` |
| 14 | 27 | 1 | u8 | `0xb3aef3` |
| 15 | 28 | 4 | u32 | `0xb3af0c` |
| 16 | 32 | 4 | u32 | `0xb3af25` |
| 17 | 36 | 1 | u8 | `0xb3af3e` |
| 18 | 37 | 2 | u16 | `0xb3af57` |

## 汇编证据序列（按线序）

```asm
; 0xb3adbf  mov [ecx] → 内联写 u32
; 0xb3add8  mov [edx] → 内联写 u16
; 0xb3ade0  call sub_B02DA0 → 写 u16
; 0xb3adf9  call sub_B02DA0 → 写 u16
; 0xb3ae12  call sub_B02DA0 → 写 u16
; 0xb3ae2b  call sub_B02DA0 → 写 u16
; 0xb3ae44  call sub_B02DA0 → 写 u16
; 0xb3ae5d  call sub_B02DA0 → 写 u16
; 0xb3ae76  call sub_B02DA0 → 写 u16
; 0xb3ae8f  call sub_B02DA0 → 写 u16
; 0xb3aea8  call sub_B02DA0 → 写 u16
; 0xb3aec1  call sub_B02DA0 → 写 u16
; 0xb3aeda  call sub_B061C0 → 写 u8
; 0xb3aef3  call sub_B061C0 → 写 u8
; 0xb3af0c  call sub_B02D80 → 写 u32
; 0xb3af25  call sub_B02D80 → 写 u32
; 0xb3af3e  call sub_B061C0 → 写 u8
; 0xb3af57  call sub_B02DA0 → 写 u16
; —— 扫描停止于 0xb3af97：call sub_B03020（非 IO）
```
