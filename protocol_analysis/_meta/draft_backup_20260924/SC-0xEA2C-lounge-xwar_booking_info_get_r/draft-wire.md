# 机器草案：线格式 —— SC-0xEA2C-lounge-xwar_booking_info_get_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xEA2C` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `xwar_booking_info_get_r` |
| 代码位置 | `0xb84bf8`..`0xb84fb0` |
| 声明容量 | `0x1C` |
| 字段总长 | **28** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb84c4f` |
| 2 | 4 | 4 | u32 | `0xb84c8f` |
| 3 | 8 | 4 | u32 | `0xb84cb3` |
| 4 | 12 | 4 | u32 | `0xb84cd7` |
| 5 | 16 | 4 | u32 | `0xb84cff` |
| 6 | 20 | 4 | u32 | `0xb84d27` |
| 7 | 24 | 4 | u32 | `0xb84d4f` |

## 汇编证据序列（按线序）

```asm
; 0xb84c40  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb84c4f  call sub_B02DD0 → 读 u32
; 0xb84c80  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb84c8f  call sub_B02DD0 → 读 u32
; 0xb84ca4  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb84cb3  call sub_B02DD0 → 读 u32
; 0xb84cc8  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb84cd7  call sub_B02DD0 → 读 u32
; 0xb84cf0  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb84cff  call sub_B02DD0 → 读 u32
; 0xb84d18  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb84d27  call sub_B02DD0 → 读 u32
; 0xb84d40  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb84d4f  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb84d77：call （非 IO）
```
