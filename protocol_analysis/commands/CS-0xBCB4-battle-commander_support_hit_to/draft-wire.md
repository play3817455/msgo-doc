# 机器草案：线格式 —— CS-0xBCB4-battle-commander_support_hit_to

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xBCB4` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `commander_support_hit_to` |
| 代码位置 | `0xb3e890`..`0xb3ecbe` |
| 声明容量 | `0x41A` |
| 字段总长 | **20** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 10 处条件跳转（`0xb3e90f`, `0xb3e91f`, `0xb3e932`, `0xb3e980`, `0xb3e9a4`, `0xb3e9ce`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb3e92a` |
| 2 | 2 | 1 | u8 | `0xb3e944` |
| 3 | 3 | 1 | u8 | `0xb3e94c` |
| 4 | 4 | 4 | u32 | `0xb3e966` |
| 5 | 8 | 4 | u32 | `0xb3e990` |
| 6 | 12 | 2 | u16 | `0xb3e9b6` |
| 7 | 14 | 4 | u32 | `0xb3e9ea` |
| 8 | 18 | 2 | u16 | `0xb3ea12` |

## 汇编证据序列（按线序）

```asm
; 0xb3e92a  mov [ecx] → 内联写 u16
; 0xb3e944  mov [edx] → 内联写 u8
; 0xb3e94c  call sub_B061C0 → 写 u8
; 0xb3e966  call sub_B02D80 → 写 u32
; 0xb3e990  call sub_B02D80 → 写 u32
; 0xb3e9b6  call sub_B02DA0 → 写 u16
; 0xb3e9ea  call sub_B02D80 → 写 u32
; 0xb3ea12  call sub_B02DA0 → 写 u16
; —— 扫描停止于 0xb3ea5e：call sub_B03020（非 IO）
```
