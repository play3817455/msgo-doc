# 机器草案：线格式 —— CS-0xA8FE-battle-weapon_fire_prepare__destruct_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xA8FE` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire_prepare__destruct_r` |
| 代码位置 | `0xb39990`..`0xb3a1ec` |
| 声明容量 | `0x10E` |
| 字段总长 | **56** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb39a29` |
| 2 | 4 | 4 | u32 | `0xb39a44` |
| 3 | 8 | 4 | u32 | `0xb39a4c` |
| 4 | 12 | 4 | u32 | `0xb39a73` |
| 5 | 16 | 2 | u16 | `0xb39a96` |
| 6 | 18 | 4 | u32 | `0xb39ac7` |
| 7 | 22 | 2 | u16 | `0xb39ae7` |
| 8 | 24 | 4 | u32 | `0xb39b18` |
| 9 | 28 | 2 | u16 | `0xb39b38` |
| 10 | 30 | 4 | u32 | `0xb39b6c` |
| 11 | 34 | 2 | u16 | `0xb39b8c` |
| 12 | 36 | 4 | u32 | `0xb39bc3` |
| 13 | 40 | 2 | u16 | `0xb39be6` |
| 14 | 42 | 4 | u32 | `0xb39c1d` |
| 15 | 46 | 2 | u16 | `0xb39c46` |
| 16 | 48 | 4 | u32 | `0xb39c7d` |
| 17 | 52 | 2 | u16 | `0xb39cb3` |
| 18 | 54 | 2 | u16 | `0xb39cda` |

## 汇编证据序列（按线序）

```asm
; 0xb39a29  mov [eax] → 内联写 u32
; 0xb39a44  mov [eax] → 内联写 u32
; 0xb39a4c  call sub_B02D80 → 写 u32
; 0xb39a73  call sub_B02D80 → 写 u32
; 0xb39a96  call sub_B02DA0 → 写 u16
; 0xb39ac7  call sub_B02D80 → 写 u32
; 0xb39ae7  call sub_B02DA0 → 写 u16
; 0xb39b18  call sub_B02D80 → 写 u32
; 0xb39b38  call sub_B02DA0 → 写 u16
; 0xb39b6c  call sub_B02D80 → 写 u32
; 0xb39b8c  call sub_B02DA0 → 写 u16
; 0xb39bc3  call sub_B02D80 → 写 u32
; 0xb39be6  call sub_B02DA0 → 写 u16
; 0xb39c1d  call sub_B02D80 → 写 u32
; 0xb39c46  call sub_B02DA0 → 写 u16
; 0xb39c7d  call sub_B02D80 → 写 u32
; 0xb39cb3  mov [ecx] → 内联写 u16
; 0xb39cda  mov [ecx] → 内联写 u16
; —— 扫描停止于 0xb39d15：call sub_B03020（非 IO）
```
