# 机器草案：线格式 —— CS-0x05CA-battle-wrestle_chase_move_start

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x05CA` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `wrestle_chase_move_start` |
| 代码位置 | `0xb40b50`..`0xb40f16` |
| 声明容量 | `0x26` |
| 字段总长 | **24** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 4 处条件跳转（`0xb40bc1`, `0xb40bd2`, `0xb40be3`, `0xb40cb7`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb40bdc` |
| 2 | 4 | 2 | u16 | `0xb40bf6` |
| 3 | 6 | 4 | u32 | `0xb40bff` |
| 4 | 10 | 4 | u32 | `0xb40c19` |
| 5 | 14 | 2 | u16 | `0xb40c33` |
| 6 | 16 | 2 | u16 | `0xb40c4d` |
| 7 | 18 | 2 | u16 | `0xb40c67` |
| 8 | 20 | 2 | u16 | `0xb40c81` |
| 9 | 22 | 2 | u16 | `0xb40c9b` |

## 汇编证据序列（按线序）

```asm
; 0xb40bdc  mov [ecx] → 内联写 u32
; 0xb40bf6  mov [edx] → 内联写 u16
; 0xb40bff  call sub_B02D80 → 写 u32
; 0xb40c19  call sub_B02D80 → 写 u32
; 0xb40c33  call sub_B02DA0 → 写 u16
; 0xb40c4d  call sub_B02DA0 → 写 u16
; 0xb40c67  call sub_B02DA0 → 写 u16
; 0xb40c81  call sub_B02DA0 → 写 u16
; 0xb40c9b  call sub_B02DA0 → 写 u16
; —— 扫描停止于 0xb40cdf：call sub_B03020（非 IO）
```
