# 机器草案：线格式 —— SC-0xEDFC-battle-weapon_fire__bit_reflect_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xEDFC` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__bit_reflect_r` |
| 代码位置 | `0xb2fe73`..`0xb30328` |
| 声明容量 | `0x15` |
| 字段总长 | **21** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb2fec3` |
| 2 | 2 | 4 | u32 | `0xb2ff03` |
| 3 | 6 | 2 | u16 | `0xb2ff27` |
| 4 | 8 | 2 | u16 | `0xb2ff4b` |
| 5 | 10 | 2 | u16 | `0xb2ff73` |
| 6 | 12 | 2 | u16 | `0xb2ff9b` |
| 7 | 14 | 2 | u16 | `0xb2ffc3` |
| 8 | 16 | 2 | u16 | `0xb2ffeb` |
| 9 | 18 | 1 | u8 | `0xb30013` |
| 10 | 19 | 2 | u16 | `0xb3003b` |

## 汇编证据序列（按线序）

```asm
; 0xb2feb4  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2fec3  call sub_B02DF0 → 读 u16
; 0xb2fef4  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2ff03  call sub_B02DD0 → 读 u32
; 0xb2ff18  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ff27  call sub_B02DF0 → 读 u16
; 0xb2ff3c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ff4b  call sub_B02DF0 → 读 u16
; 0xb2ff64  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ff73  call sub_B02DF0 → 读 u16
; 0xb2ff8c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ff9b  call sub_B02DF0 → 读 u16
; 0xb2ffb4  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ffc3  call sub_B02DF0 → 读 u16
; 0xb2ffdc  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ffeb  call sub_B02DF0 → 读 u16
; 0xb30004  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb30013  call sub_B06230 → 读 u8
; 0xb3002c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb3003b  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb30063：call （非 IO）
```
