# 机器草案：线格式 —— CS-0x770D-battle-weapon_hit_to

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x770D` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `weapon_hit_to` |
| 代码位置 | `0xb3b7a0`..`0xb3c282` |
| 声明容量 | `0x14E` |
| 字段总长 | **79** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 28 处条件跳转（`0xb3b81f`, `0xb3b82f`, `0xb3b847`, `0xb3b892`, `0xb3b8b6`, `0xb3b8de`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb3b839` |
| 2 | 4 | 4 | u32 | `0xb3b83f` |
| 3 | 8 | 4 | u32 | `0xb3b851` |
| 4 | 12 | 4 | u32 | `0xb3b861` |
| 5 | 16 | 4 | u32 | `0xb3b87b` |
| 6 | 20 | 4 | u32 | `0xb3b8a2` |
| 7 | 24 | 2 | u16 | `0xb3b8c6` |
| 8 | 26 | 4 | u32 | `0xb3b8f7` |
| 9 | 30 | 2 | u16 | `0xb3b917` |
| 10 | 32 | 4 | u32 | `0xb3b94b` |
| 11 | 36 | 2 | u16 | `0xb3b96b` |
| 12 | 38 | 4 | u32 | `0xb3b9a4` |
| 13 | 42 | 2 | u16 | `0xb3b9c7` |
| 14 | 44 | 4 | u32 | `0xb3ba03` |
| 15 | 48 | 2 | u16 | `0xb3ba26` |
| 16 | 50 | 4 | u32 | `0xb3ba62` |
| 17 | 54 | 2 | u16 | `0xb3ba86` |
| 18 | 56 | 4 | u32 | `0xb3bac2` |
| 19 | 60 | 2 | u16 | `0xb3bae6` |
| 20 | 62 | 4 | u32 | `0xb3bb22` |
| 21 | 66 | 2 | u16 | `0xb3bb46` |
| 22 | 68 | 1 | u8 | `0xb3bb72` |
| 23 | 69 | 2 | u16 | `0xb3bb8f` |
| 24 | 71 | 2 | u16 | `0xb3bbac` |
| 25 | 73 | 4 | u32 | `0xb3bbc9` |
| 26 | 77 | 1 | u8 | `0xb3bbe6` |
| 27 | 78 | 1 | u8 | `0xb3bc03` |

## 汇编证据序列（按线序）

```asm
; 0xb3b839  mov [eax] → 内联写 u32
; 0xb3b83f  mov [eax+4] → 内联写 u32
; 0xb3b851  mov [edx] → 内联写 u32
; 0xb3b861  call sub_B02D80 → 写 u32
; 0xb3b87b  call sub_B02D80 → 写 u32
; 0xb3b8a2  call sub_B02D80 → 写 u32
; 0xb3b8c6  call sub_B02DA0 → 写 u16
; 0xb3b8f7  call sub_B02D80 → 写 u32
; 0xb3b917  call sub_B02DA0 → 写 u16
; 0xb3b94b  call sub_B02D80 → 写 u32
; 0xb3b96b  call sub_B02DA0 → 写 u16
; 0xb3b9a4  call sub_B02D80 → 写 u32
; 0xb3b9c7  call sub_B02DA0 → 写 u16
; 0xb3ba03  call sub_B02D80 → 写 u32
; 0xb3ba26  call sub_B02DA0 → 写 u16
; 0xb3ba62  call sub_B02D80 → 写 u32
; 0xb3ba86  call sub_B02DA0 → 写 u16
; 0xb3bac2  call sub_B02D80 → 写 u32
; 0xb3bae6  call sub_B02DA0 → 写 u16
; 0xb3bb22  call sub_B02D80 → 写 u32
; 0xb3bb46  call sub_B02DA0 → 写 u16
; 0xb3bb72  call sub_B061C0 → 写 u8
; 0xb3bb8f  call sub_B02DA0 → 写 u16
; 0xb3bbac  call sub_B02DA0 → 写 u16
; 0xb3bbc9  call sub_B02D80 → 写 u32
; 0xb3bbe6  call sub_B061C0 → 写 u8
; 0xb3bc03  call sub_B061C0 → 写 u8
; —— 扫描停止于 0xb3bc4b：call sub_B03020（非 IO）
```
