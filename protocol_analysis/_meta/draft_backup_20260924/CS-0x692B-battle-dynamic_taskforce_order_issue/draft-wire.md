# 机器草案：线格式 —— CS-0x692B-battle-dynamic_taskforce_order_issue

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x692B` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `dynamic_taskforce_order_issue` |
| 代码位置 | `0xb3f3f0`..`0xb3f77e` |
| 声明容量 | `0x5E` |
| 字段总长 | **16** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 1 | u8 | `0xb3f483` |
| 2 | 1 | 4 | u32 | `0xb3f49b` |
| 3 | 5 | 4 | u32 | `0xb3f4b1` |
| 4 | 9 | 1 | u8 | `0xb3f4d4` |
| 5 | 10 | 4 | u32 | `0xb3f502` |
| 6 | 14 | 2 | u16 | `0xb3f52a` |

## 汇编证据序列（按线序）

```asm
; 0xb3f483  mov [ecx] → 内联写 u8
; 0xb3f49b  mov [esi] → 内联写 u32
; 0xb3f4b1  call sub_B02D80 → 写 u32
; 0xb3f4d4  call sub_B061C0 → 写 u8
; 0xb3f502  call sub_B02D80 → 写 u32
; 0xb3f52a  call sub_B02DA0 → 写 u16
; —— 扫描停止于 0xb3f576：call sub_B03020（非 IO）
```
