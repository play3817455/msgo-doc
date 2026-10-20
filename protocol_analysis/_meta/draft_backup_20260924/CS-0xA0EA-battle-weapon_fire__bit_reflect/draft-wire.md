# 机器草案：线格式 —— CS-0xA0EA-battle-weapon_fire__bit_reflect

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xA0EA` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__bit_reflect` |
| 代码位置 | `0xb3b350`..`0xb3b79c` |
| 声明容量 | `0x2E` |
| 字段总长 | **25** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb3b3dc` |
| 2 | 4 | 4 | u32 | `0xb3b3f7` |
| 3 | 8 | 2 | u16 | `0xb3b3ff` |
| 4 | 10 | 2 | u16 | `0xb3b419` |
| 5 | 12 | 2 | u16 | `0xb3b433` |
| 6 | 14 | 2 | u16 | `0xb3b44d` |
| 7 | 16 | 2 | u16 | `0xb3b467` |
| 8 | 18 | 2 | u16 | `0xb3b481` |
| 9 | 20 | 1 | u8 | `0xb3b49b` |
| 10 | 21 | 2 | u16 | `0xb3b4b5` |
| 11 | 23 | 2 | u16 | `0xb3b4cf` |

## 汇编证据序列（按线序）

```asm
; 0xb3b3dc  mov [eax] → 内联写 u32
; 0xb3b3f7  mov [eax] → 内联写 u32
; 0xb3b3ff  call sub_B02DA0 → 写 u16
; 0xb3b419  call sub_B02DA0 → 写 u16
; 0xb3b433  call sub_B02DA0 → 写 u16
; 0xb3b44d  call sub_B02DA0 → 写 u16
; 0xb3b467  call sub_B02DA0 → 写 u16
; 0xb3b481  call sub_B02DA0 → 写 u16
; 0xb3b49b  call sub_B061C0 → 写 u8
; 0xb3b4b5  call sub_B02DA0 → 写 u16
; 0xb3b4cf  call sub_B02DA0 → 写 u16
; —— 扫描停止于 0xb3b513：call sub_B03020（非 IO）
```
