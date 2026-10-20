# 机器草案：线格式 —— SC-0xD725-battle-weapon_fire__wrestle_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xD725` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__wrestle_r` |
| 代码位置 | `0xb2c0da`..`0xb2c586` |
| 声明容量 | `0x15` |
| 字段总长 | **21** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb2c12e` |
| 2 | 2 | 4 | u32 | `0xb2c16b` |
| 3 | 6 | 2 | u16 | `0xb2c18f` |
| 4 | 8 | 2 | u16 | `0xb2c1b3` |
| 5 | 10 | 2 | u16 | `0xb2c1db` |
| 6 | 12 | 4 | u32 | `0xb2c203` |
| 7 | 16 | 1 | u8 | `0xb2c22b` |
| 8 | 17 | 1 | u8 | `0xb2c253` |
| 9 | 18 | 2 | u16 | `0xb2c27b` |
| 10 | 20 | 1 | u8 | `0xb2c2a3` |

## 汇编证据序列（按线序）

```asm
; 0xb2c11f  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2c12e  call sub_B02DF0 → 读 u16
; 0xb2c15c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2c16b  call sub_B02DD0 → 读 u32
; 0xb2c180  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2c18f  call sub_B02DF0 → 读 u16
; 0xb2c1a4  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2c1b3  call sub_B02DF0 → 读 u16
; 0xb2c1cc  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2c1db  call sub_B02DF0 → 读 u16
; 0xb2c1f4  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2c203  call sub_B02DD0 → 读 u32
; 0xb2c21c  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb2c22b  call sub_B06230 → 读 u8
; 0xb2c244  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb2c253  call sub_B06230 → 读 u8
; 0xb2c26c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2c27b  call sub_B02DF0 → 读 u16
; 0xb2c294  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb2c2a3  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb2c2c8：call （非 IO）
```
