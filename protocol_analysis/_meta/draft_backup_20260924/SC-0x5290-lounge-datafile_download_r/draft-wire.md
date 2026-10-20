# 机器草案：线格式 —— SC-0x5290-lounge-datafile_download_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x5290` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `datafile_download_r` |
| 代码位置 | `0xb605c4`..`0xb609c1` |
| 声明容量 | `0x8000112` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb6061b` |
| 2 | 4 | ? | bytes | `0xb6065e` |
| 3 | ? | 4 | u32 | `0xb6069b` |
| 4 | ? | 4 | u32 | `0xb606bf` |
| 5 | ? | 2 | u16 | `0xb606e3` |
| 6 | ? | 4 | u32 | `0xb606fd` |
| 7 | ? | 1 | u8[] | `0xb60727` |
| 8 | ? | 1 | u8 | `0xb6073e` |

## 汇编证据序列（按线序）

```asm
; 0xb6060c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6061b  call sub_B02DD0 → 读 u32
; 0xb6065e  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb6068c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6069b  call sub_B02DD0 → 读 u32
; 0xb606b0  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb606bf  call sub_B02DD0 → 读 u32
; 0xb606d4  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb606e3  call sub_B02DF0 → 读 u16
; 0xb606fd  call sub_B02DD0 → 读 u32
; 0xb60727  call sub_B05EA0 → 读 u8（数组）
; 0xb6073e  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb60751：jmp
```
