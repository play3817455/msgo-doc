# 机器草案：线格式 —— CS-0xE650-battle-msma_spawn_select

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xE650` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `msma_spawn_select` |
| 代码位置 | `0xb33f30`..`0xb34231` |
| 声明容量 | `0x1A` |
| 字段总长 | **16** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb33fbc` |
| 2 | 4 | 4 | u32 | `0xb33fd7` |
| 3 | 8 | 4 | u32 | `0xb33fdf` |
| 4 | 12 | 1 | u8 | `0xb33ff9` |
| 5 | 13 | 1 | u8 | `0xb34013` |
| 6 | 14 | 2 | u16 | `0xb3402d` |

## 汇编证据序列（按线序）

```asm
; 0xb33fbc  mov [eax] → 内联写 u32
; 0xb33fd7  mov [eax] → 内联写 u32
; 0xb33fdf  call sub_B02D80 → 写 u32
; 0xb33ff9  call sub_B061C0 → 写 u8
; 0xb34013  call sub_B061C0 → 写 u8
; 0xb3402d  call sub_B02DA0 → 写 u16
; —— 扫描停止于 0xb34071：call sub_B03020（非 IO）
```
