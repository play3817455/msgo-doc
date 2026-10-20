# 机器草案：线格式 —— CS-0x2ADC-battle-weapon_fire__wrestle

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x2ADC` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__wrestle` |
| 代码位置 | `0xb36ec0`..`0xb372cb` |
| 声明容量 | `0x2A` |
| 字段总长 | **21** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb36f4c` |
| 2 | 4 | 2 | u16 | `0xb36f66` |
| 3 | 6 | 2 | u16 | `0xb36f6f` |
| 4 | 8 | 2 | u16 | `0xb36f89` |
| 5 | 10 | 4 | u32 | `0xb36fa3` |
| 6 | 14 | 1 | u8 | `0xb36fbd` |
| 7 | 15 | 2 | u16 | `0xb36fd7` |
| 8 | 17 | 1 | u8 | `0xb36ff1` |
| 9 | 18 | 2 | u16 | `0xb3700b` |
| 10 | 20 | 1 | u8 | `0xb37025` |

## 汇编证据序列（按线序）

```asm
; 0xb36f4c  mov [ecx] → 内联写 u32
; 0xb36f66  mov [edx] → 内联写 u16
; 0xb36f6f  call sub_B02DA0 → 写 u16
; 0xb36f89  call sub_B02DA0 → 写 u16
; 0xb36fa3  call sub_B02D80 → 写 u32
; 0xb36fbd  call sub_B061C0 → 写 u8
; 0xb36fd7  call sub_B02DA0 → 写 u16
; 0xb36ff1  call sub_B061C0 → 写 u8
; 0xb3700b  call sub_B02DA0 → 写 u16
; 0xb37025  call sub_B061C0 → 写 u8
; —— 扫描停止于 0xb37069：call sub_B03020（非 IO）
```
