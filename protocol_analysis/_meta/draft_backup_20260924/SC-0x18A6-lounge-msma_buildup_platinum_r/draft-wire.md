# 机器草案：线格式 —— SC-0x18A6-lounge-msma_buildup_platinum_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x18A6` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_buildup_platinum_r` |
| 代码位置 | `0xb56297`..`0xb5673a` |
| 声明容量 | `0x2A` |
| 字段总长 | **24** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb562ee` |
| 2 | 4 | 8 | u64 | `0xb5632e` |
| 3 | 12 | 4 | u32 | `0xb56352` |
| 4 | 16 | 2 | u16 | `0xb56376` |
| 5 | 18 | 4 | u32 | `0xb5639e` |
| 6 | 22 | 2 | u16 | `0xb563c6` |

## 汇编证据序列（按线序）

```asm
; 0xb562df  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb562ee  call sub_B02DD0 → 读 u32
; 0xb5631f  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb5632e  call sub_B06200 → 读 u64
; 0xb56343  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb56352  call sub_B02DD0 → 读 u32
; 0xb56367  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb56376  call sub_B02DF0 → 读 u16
; 0xb5638f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5639e  call sub_B02DD0 → 读 u32
; 0xb563b7  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb563c6  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb563df：call sub_B41590（非 IO）
```
