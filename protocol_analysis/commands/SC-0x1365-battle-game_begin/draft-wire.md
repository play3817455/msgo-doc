# 机器草案：线格式 —— SC-0x1365-battle-game_begin

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x1365` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `game_begin` |
| 代码位置 | `0xb0fbda`..`0xb10671` |
| 声明容量 | `0x2806` |
| 字段总长 | **46** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb0fc37` |
| 2 | 4 | 4 | u32 | `0xb0fc7a` |
| 3 | 8 | 4 | u32 | `0xb0fc9e` |
| 4 | 12 | 4 | u32 | `0xb0fcc2` |
| 5 | 16 | 4 | u32 | `0xb0fcea` |
| 6 | 20 | 4 | u32 | `0xb0fd12` |
| 7 | 24 | 1 | u8 | `0xb0fd3a` |
| 8 | 25 | 1 | u8 | `0xb0fd62` |
| 9 | 26 | 4 | u32 | `0xb0fd8a` |
| 10 | 30 | 4 | u32 | `0xb0fdb2` |
| 11 | 34 | 4 | u32 | `0xb0fdda` |
| 12 | 38 | 4 | u32 | `0xb0fe02` |
| 13 | 42 | 4 | u32 | `0xb0fe2a` |

## 汇编证据序列（按线序）

```asm
; 0xb0fc25  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0fc37  call sub_B02DD0 → 读 u32
; 0xb0fc68  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0fc7a  call sub_B02DD0 → 读 u32
; 0xb0fc8f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0fc9e  call sub_B02DD0 → 读 u32
; 0xb0fcb3  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0fcc2  call sub_B02DD0 → 读 u32
; 0xb0fcdb  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0fcea  call sub_B02DD0 → 读 u32
; 0xb0fd03  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0fd12  call sub_B02DD0 → 读 u32
; 0xb0fd2b  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb0fd3a  call sub_B06230 → 读 u8
; 0xb0fd53  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb0fd62  call sub_B06230 → 读 u8
; 0xb0fd7b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0fd8a  call sub_B02DD0 → 读 u32
; 0xb0fda3  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0fdb2  call sub_B02DD0 → 读 u32
; 0xb0fdcb  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0fdda  call sub_B02DD0 → 读 u32
; 0xb0fdf3  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0fe02  call sub_B02DD0 → 读 u32
; 0xb0fe1b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0fe2a  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb0fe43：call sub_B418C0（非 IO）
```
