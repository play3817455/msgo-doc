# 机器草案：线格式 —— SC-0xB9AB-lounge-msma_buildup_complete_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xB9AB` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_buildup_complete_r` |
| 代码位置 | `0xb7636f`..`0xb76813` |
| 声明容量 | `0x20` |
| 字段总长 | **32** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb763c6` |
| 2 | 4 | 8 | u64 | `0xb76406` |
| 3 | 12 | 4 | u32 | `0xb76446` |
| 4 | 16 | 2 | u16 | `0xb7646a` |
| 5 | 18 | 4 | u32 | `0xb7648e` |
| 6 | 22 | 2 | u16 | `0xb764b6` |
| 7 | 24 | 2 | u16 | `0xb764de` |
| 8 | 26 | 2 | u16 | `0xb76506` |
| 9 | 28 | 4 | u32 | `0xb7652e` |

## 汇编证据序列（按线序）

```asm
; 0xb763b7  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb763c6  call sub_B02DD0 → 读 u32
; 0xb763f7  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb76406  call sub_B06200 → 读 u64
; 0xb76437  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb76446  call sub_B02DD0 → 读 u32
; 0xb7645b  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb7646a  call sub_B02DF0 → 读 u16
; 0xb7647f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7648e  call sub_B02DD0 → 读 u32
; 0xb764a7  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb764b6  call sub_B02DF0 → 读 u16
; 0xb764cf  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb764de  call sub_B02DF0 → 读 u16
; 0xb764f7  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb76506  call sub_B02DF0 → 读 u16
; 0xb7651f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7652e  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb76556：call （非 IO）
```
