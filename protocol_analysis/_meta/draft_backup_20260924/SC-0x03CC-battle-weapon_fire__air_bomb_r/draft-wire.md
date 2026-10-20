# 机器草案：线格式 —— SC-0x03CC-battle-weapon_fire__air_bomb_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x03CC` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__air_bomb_r` |
| 代码位置 | `0xb0cd3b`..`0xb0d137` |
| 声明容量 | `0x12` |
| 字段总长 | **18** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb0cd8b` |
| 2 | 2 | 4 | u32 | `0xb0cdcb` |
| 3 | 6 | 4 | u32 | `0xb0cdef` |
| 4 | 10 | 2 | u16 | `0xb0ce13` |
| 5 | 12 | 2 | u16 | `0xb0ce3b` |
| 6 | 14 | 2 | u16 | `0xb0ce63` |
| 7 | 16 | 1 | u8 | `0xb0ce8b` |
| 8 | 17 | 1 | u8 | `0xb0ceb3` |

## 汇编证据序列（按线序）

```asm
; 0xb0cd7c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb0cd8b  call sub_B02DF0 → 读 u16
; 0xb0cdbc  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0cdcb  call sub_B02DD0 → 读 u32
; 0xb0cde0  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0cdef  call sub_B02DD0 → 读 u32
; 0xb0ce04  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb0ce13  call sub_B02DF0 → 读 u16
; 0xb0ce2c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb0ce3b  call sub_B02DF0 → 读 u16
; 0xb0ce54  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb0ce63  call sub_B02DF0 → 读 u16
; 0xb0ce7c  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb0ce8b  call sub_B06230 → 读 u8
; 0xb0cea4  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb0ceb3  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb0cedb：call （非 IO）
```
