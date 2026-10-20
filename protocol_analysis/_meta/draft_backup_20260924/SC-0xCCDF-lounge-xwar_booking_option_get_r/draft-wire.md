# 机器草案：线格式 —— SC-0xCCDF-lounge-xwar_booking_option_get_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xCCDF` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `xwar_booking_option_get_r` |
| 代码位置 | `0xb7b003`..`0xb7b3bd` |
| 声明容量 | `0x22C` |
| 字段总长 | **20** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb7b05d` |
| 2 | 4 | 4 | u32 | `0xb7b09d` |
| 3 | 8 | 4 | u32 | `0xb7b0c1` |
| 4 | 12 | 4 | u32 | `0xb7b0e5` |
| 5 | 16 | 4 | u32 | `0xb7b10d` |

## 汇编证据序列（按线序）

```asm
; 0xb7b04e  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7b05d  call sub_B02DD0 → 读 u32
; 0xb7b08e  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7b09d  call sub_B02DD0 → 读 u32
; 0xb7b0b2  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7b0c1  call sub_B02DD0 → 读 u32
; 0xb7b0d6  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7b0e5  call sub_B02DD0 → 读 u32
; 0xb7b0fe  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7b10d  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb7b126：call sub_B41740（非 IO）
```
