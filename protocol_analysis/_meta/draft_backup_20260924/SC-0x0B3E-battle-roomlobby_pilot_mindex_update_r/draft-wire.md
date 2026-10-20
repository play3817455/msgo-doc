# 机器草案：线格式 —— SC-0x0B3E-battle-roomlobby_pilot_mindex_update_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x0B3E` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `roomlobby_pilot_mindex_update_r` |
| 代码位置 | `0xb0e407`..`0xb0e708` |
| 声明容量 | `0xE` |
| 字段总长 | **14** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb0e45b` |
| 2 | 4 | 4 | u32 | `0xb0e498` |
| 3 | 8 | 4 | u32 | `0xb0e4bc` |
| 4 | 12 | 1 | u8 | `0xb0e4e0` |
| 5 | 13 | 1 | u8 | `0xb0e508` |

## 汇编证据序列（按线序）

```asm
; 0xb0e44c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0e45b  call sub_B02DD0 → 读 u32
; 0xb0e489  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0e498  call sub_B02DD0 → 读 u32
; 0xb0e4ad  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0e4bc  call sub_B02DD0 → 读 u32
; 0xb0e4d1  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb0e4e0  call sub_B06230 → 读 u8
; 0xb0e4f9  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb0e508  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb0e52d：call （非 IO）
```
