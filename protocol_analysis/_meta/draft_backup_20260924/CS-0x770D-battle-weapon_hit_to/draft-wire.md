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
| 字段总长 | **75** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb3b839` |
| 2 | 4 | 4 | u32 | `0xb3b851` |
| 3 | 8 | 4 | u32 | `0xb3b861` |
| 4 | 12 | 4 | u32 | `0xb3b87b` |
| 5 | 16 | 4 | u32 | `0xb3b8a2` |
| 6 | 20 | 2 | u16 | `0xb3b8c6` |
| 7 | 22 | 4 | u32 | `0xb3b8f7` |
| 8 | 26 | 2 | u16 | `0xb3b917` |
| 9 | 28 | 4 | u32 | `0xb3b94b` |
| 10 | 32 | 2 | u16 | `0xb3b96b` |
| 11 | 34 | 4 | u32 | `0xb3b9a4` |
| 12 | 38 | 2 | u16 | `0xb3b9c7` |
| 13 | 40 | 4 | u32 | `0xb3ba03` |
| 14 | 44 | 2 | u16 | `0xb3ba26` |
| 15 | 46 | 4 | u32 | `0xb3ba62` |
| 16 | 50 | 2 | u16 | `0xb3ba86` |
| 17 | 52 | 4 | u32 | `0xb3bac2` |
| 18 | 56 | 2 | u16 | `0xb3bae6` |
| 19 | 58 | 4 | u32 | `0xb3bb22` |
| 20 | 62 | 2 | u16 | `0xb3bb46` |
| 21 | 64 | 1 | u8 | `0xb3bb72` |
| 22 | 65 | 2 | u16 | `0xb3bb8f` |
| 23 | 67 | 2 | u16 | `0xb3bbac` |
| 24 | 69 | 4 | u32 | `0xb3bbc9` |
| 25 | 73 | 1 | u8 | `0xb3bbe6` |
| 26 | 74 | 1 | u8 | `0xb3bc03` |

## 汇编证据序列（按线序）

```asm
; 0xb3b839  mov [eax] → 内联写 u32
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
