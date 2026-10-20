# 机器草案：线格式 —— SC-0xA5DA-battle-authenticate_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xA5DA` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `authenticate_r` |
| 代码位置 | `0xb25a79`..`0xb262e9` |
| 声明容量 | `0x2DE` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb25ad6` |
| 2 | 4 | 4 | u32 | `0xb25b19` |
| 3 | 8 | ? | bytes | `0xb25b41` |
| 4 | ? | 4 | u32 | `0xb25b7e` |
| 5 | ? | 4 | u32 | `0xb25ba2` |
| 6 | ? | 4 | u32 | `0xb25bc6` |
| 7 | ? | 4 | u32 | `0xb25bee` |
| 8 | ? | 4 | u32 | `0xb25c16` |
| 9 | ? | 1 | u8 | `0xb25c3e` |
| 10 | ? | 4 | u32 | `0xb25c66` |
| 11 | ? | 1 | u8 | `0xb25c8e` |
| 12 | ? | 1 | u8 | `0xb25cb6` |
| 13 | ? | 1 | u8 | `0xb25cde` |
| 14 | ? | 1 | u8 | `0xb25d06` |

## 汇编证据序列（按线序）

```asm
; 0xb25ac4  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb25ad6  call sub_B02DD0 → 读 u32
; 0xb25b07  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb25b19  call sub_B02DD0 → 读 u32
; 0xb25b41  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb25b6f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb25b7e  call sub_B02DD0 → 读 u32
; 0xb25b93  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb25ba2  call sub_B02DD0 → 读 u32
; 0xb25bb7  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb25bc6  call sub_B02DD0 → 读 u32
; 0xb25bdf  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb25bee  call sub_B02DD0 → 读 u32
; 0xb25c07  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb25c16  call sub_B02DD0 → 读 u32
; 0xb25c2f  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb25c3e  call sub_B06230 → 读 u8
; 0xb25c57  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb25c66  call sub_B02DD0 → 读 u32
; 0xb25c7f  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb25c8e  call sub_B06230 → 读 u8
; 0xb25ca7  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb25cb6  call sub_B06230 → 读 u8
; 0xb25ccf  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb25cde  call sub_B06230 → 读 u8
; 0xb25cf7  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb25d06  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb25d1f：call sub_B418C0（非 IO）
```
