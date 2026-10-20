# 机器草案：线格式 —— SC-0x2ACF-lounge-msma_init_get_r_begin

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x2ACF` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_init_get_r_begin` |
| 代码位置 | `0xb59f70`..`0xb5a3e2` |
| 声明容量 | `0x1C` |
| 字段总长 | **28** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb59fc7` |
| 2 | 4 | 2 | u16 | `0xb5a007` |
| 3 | 6 | 4 | u32 | `0xb5a02b` |
| 4 | 10 | 4 | u32 | `0xb5a04f` |
| 5 | 14 | 2 | u16 | `0xb5a077` |
| 6 | 16 | 2 | u16 | `0xb5a09f` |
| 7 | 18 | 2 | u16 | `0xb5a0c7` |
| 8 | 20 | 4 | u32 | `0xb5a0ef` |
| 9 | 24 | 4 | u32 | `0xb5a117` |

## 汇编证据序列（按线序）

```asm
; 0xb59fb8  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb59fc7  call sub_B02DD0 → 读 u32
; 0xb59ff8  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb5a007  call sub_B02DF0 → 读 u16
; 0xb5a01c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5a02b  call sub_B02DD0 → 读 u32
; 0xb5a040  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5a04f  call sub_B02DD0 → 读 u32
; 0xb5a068  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb5a077  call sub_B02DF0 → 读 u16
; 0xb5a090  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb5a09f  call sub_B02DF0 → 读 u16
; 0xb5a0b8  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb5a0c7  call sub_B02DF0 → 读 u16
; 0xb5a0e0  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5a0ef  call sub_B02DD0 → 读 u32
; 0xb5a108  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5a117  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb5a13f：call （非 IO）
```
