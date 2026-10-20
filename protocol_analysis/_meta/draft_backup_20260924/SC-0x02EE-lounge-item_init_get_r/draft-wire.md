# 机器草案：线格式 —— SC-0x02EE-lounge-item_init_get_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x02EE` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `item_init_get_r` |
| 代码位置 | `0xb524f6`..`0xb52fa3` |
| 声明容量 | `0xF400` |
| 字段总长 | **36** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb52550` |
| 2 | 2 | 2 | u16 | `0xb52590` |
| 3 | 4 | 2 | u16 | `0xb525b4` |
| 4 | 6 | 2 | u16 | `0xb525d8` |
| 5 | 8 | 4 | u32 | `0xb52600` |
| 6 | 12 | 4 | u32 | `0xb52628` |
| 7 | 16 | 4 | u32 | `0xb52650` |
| 8 | 20 | 4 | u32 | `0xb52678` |
| 9 | 24 | 4 | u32 | `0xb526a0` |
| 10 | 28 | 4 | u32 | `0xb526ce` |
| 11 | 32 | 4 | u32 | `0xb526e8` |

## 汇编证据序列（按线序）

```asm
; 0xb52541  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb52550  call sub_B02DF0 → 读 u16
; 0xb52581  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb52590  call sub_B02DF0 → 读 u16
; 0xb525a5  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb525b4  call sub_B02DF0 → 读 u16
; 0xb525c9  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb525d8  call sub_B02DF0 → 读 u16
; 0xb525f1  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb52600  call sub_B02DD0 → 读 u32
; 0xb52619  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb52628  call sub_B02DD0 → 读 u32
; 0xb52641  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb52650  call sub_B02DD0 → 读 u32
; 0xb52669  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb52678  call sub_B02DD0 → 读 u32
; 0xb52691  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb526a0  call sub_B02DD0 → 读 u32
; 0xb526bc  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb526ce  call sub_B02DD0 → 读 u32
; 0xb526e8  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb52726：call sub_B416C0（非 IO）
```
