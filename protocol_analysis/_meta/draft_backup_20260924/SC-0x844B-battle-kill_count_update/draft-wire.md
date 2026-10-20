# 机器草案：线格式 —— SC-0x844B-battle-kill_count_update

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x844B` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `kill_count_update` |
| 代码位置 | `0xb21b83`..`0xb21f26` |
| 声明容量 | `0x17` |
| 字段总长 | **23** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb21bda` |
| 2 | 4 | 2 | u16 | `0xb21c1a` |
| 3 | 6 | 4 | u32 | `0xb21c3e` |
| 4 | 10 | 4 | u32 | `0xb21c62` |
| 5 | 14 | 4 | u32 | `0xb21c8a` |
| 6 | 18 | 4 | u32 | `0xb21cb2` |
| 7 | 22 | 1 | u8 | `0xb21cda` |

## 汇编证据序列（按线序）

```asm
; 0xb21bcb  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb21bda  call sub_B02DD0 → 读 u32
; 0xb21c0b  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb21c1a  call sub_B02DF0 → 读 u16
; 0xb21c2f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb21c3e  call sub_B02DD0 → 读 u32
; 0xb21c53  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb21c62  call sub_B02DD0 → 读 u32
; 0xb21c7b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb21c8a  call sub_B02DD0 → 读 u32
; 0xb21ca3  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb21cb2  call sub_B02DD0 → 读 u32
; 0xb21ccb  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb21cda  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb21d02：call （非 IO）
```
