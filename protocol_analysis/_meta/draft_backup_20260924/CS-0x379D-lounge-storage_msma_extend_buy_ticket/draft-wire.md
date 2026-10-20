# 机器草案：线格式 —— CS-0x379D-lounge-storage_msma_extend_buy_ticket

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x379D` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `storage_msma_extend_buy_ticket` |
| 代码位置 | `0xba4110`..`0xba4458` |
| 声明容量 | `0x1E` |
| 字段总长 | **19** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xba419c` |
| 2 | 4 | 1 | u8 | `0xba41b5` |
| 3 | 5 | 4 | u32 | `0xba41bd` |
| 4 | 9 | 1 | u8 | `0xba41d7` |
| 5 | 10 | 1 | u8 | `0xba41f1` |
| 6 | 11 | 4 | u32 | `0xba420b` |
| 7 | 15 | 4 | u32 | `0xba4225` |

## 汇编证据序列（按线序）

```asm
; 0xba419c  mov [ecx] → 内联写 u32
; 0xba41b5  mov [edx] → 内联写 u8
; 0xba41bd  call sub_B02D80 → 写 u32
; 0xba41d7  call sub_B061C0 → 写 u8
; 0xba41f1  call sub_B061C0 → 写 u8
; 0xba420b  call sub_B02D80 → 写 u32
; 0xba4225  call sub_B02D80 → 写 u32
; —— 扫描停止于 0xba4269：call sub_B03020（非 IO）
```
