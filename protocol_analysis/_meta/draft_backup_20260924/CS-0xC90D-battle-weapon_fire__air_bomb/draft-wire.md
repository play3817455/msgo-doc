# 机器草案：线格式 —— CS-0xC90D-battle-weapon_fire__air_bomb

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xC90D` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__air_bomb` |
| 代码位置 | `0xb38ac0`..`0xb38e48` |
| 声明容量 | `0x22` |
| 字段总长 | **18** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb38b4c` |
| 2 | 4 | 2 | u16 | `0xb38b66` |
| 3 | 6 | 2 | u16 | `0xb38b6f` |
| 4 | 8 | 2 | u16 | `0xb38b89` |
| 5 | 10 | 1 | u8 | `0xb38ba3` |
| 6 | 11 | 1 | u8 | `0xb38bbd` |
| 7 | 12 | 4 | u32 | `0xb38bd7` |
| 8 | 16 | 2 | u16 | `0xb38bf1` |

## 汇编证据序列（按线序）

```asm
; 0xb38b4c  mov [ecx] → 内联写 u32
; 0xb38b66  mov [edx] → 内联写 u16
; 0xb38b6f  call sub_B02DA0 → 写 u16
; 0xb38b89  call sub_B02DA0 → 写 u16
; 0xb38ba3  call sub_B061C0 → 写 u8
; 0xb38bbd  call sub_B061C0 → 写 u8
; 0xb38bd7  call sub_B02D80 → 写 u32
; 0xb38bf1  call sub_B02DA0 → 写 u16
; —— 扫描停止于 0xb38c35：call sub_B03020（非 IO）
```
