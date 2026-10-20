# 机器草案：线格式 —— SC-0x49C6-battle-weapon_hit_from

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x49C6` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_hit_from` |
| 代码位置 | `0xb15a63`..`0xb16104` |
| 声明容量 | `0x2B` |
| 字段总长 | **43** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb15aba` |
| 2 | 2 | 2 | u16 | `0xb15afa` |
| 3 | 4 | 4 | u32 | `0xb15b1e` |
| 4 | 8 | 1 | u8 | `0xb15b42` |
| 5 | 9 | 4 | u32 | `0xb15b6a` |
| 6 | 13 | 4 | u32 | `0xb15b92` |
| 7 | 17 | 4 | u32 | `0xb15bba` |
| 8 | 21 | 4 | u32 | `0xb15be2` |
| 9 | 25 | 2 | u16 | `0xb15c0a` |
| 10 | 27 | 2 | u16 | `0xb15c32` |
| 11 | 29 | 2 | u16 | `0xb15c5a` |
| 12 | 31 | 2 | u16 | `0xb15c82` |
| 13 | 33 | 2 | u16 | `0xb15caa` |
| 14 | 35 | 4 | u32 | `0xb15cd2` |
| 15 | 39 | 4 | u32 | `0xb15cfa` |

## 汇编证据序列（按线序）

```asm
; 0xb15aab  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb15aba  call sub_B02DF0 → 读 u16
; 0xb15aeb  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb15afa  call sub_B02DF0 → 读 u16
; 0xb15b0f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb15b1e  call sub_B02DD0 → 读 u32
; 0xb15b33  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb15b42  call sub_B06230 → 读 u8
; 0xb15b5b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb15b6a  call sub_B02DD0 → 读 u32
; 0xb15b83  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb15b92  call sub_B02DD0 → 读 u32
; 0xb15bab  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb15bba  call sub_B02DD0 → 读 u32
; 0xb15bd3  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb15be2  call sub_B02DD0 → 读 u32
; 0xb15bfb  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb15c0a  call sub_B02DF0 → 读 u16
; 0xb15c23  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb15c32  call sub_B02DF0 → 读 u16
; 0xb15c4b  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb15c5a  call sub_B02DF0 → 读 u16
; 0xb15c73  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb15c82  call sub_B02DF0 → 读 u16
; 0xb15c9b  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb15caa  call sub_B02DF0 → 读 u16
; 0xb15cc3  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb15cd2  call sub_B02DD0 → 读 u32
; 0xb15ceb  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb15cfa  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb15d22：call （非 IO）
```
