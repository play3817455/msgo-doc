# 机器草案：线格式 —— SC-0x7155-battle-roomlobby_pilot_add_npc

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x7155` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `roomlobby_pilot_add_npc` |
| 代码位置 | `0xb1e268`..`0xb1e7f7` |
| 声明容量 | `0x5B` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb1e4a9`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 1 | u8 | `0xb1e2bc` |
| 2 | 1 | 1 | u8 | `0xb1e2f9` |
| 3 | 2 | 4 | u32 | `0xb1e31d` |
| 4 | 6 | 2 | u16 | `0xb1e341` |
| 5 | 8 | 4 | u32 | `0xb1e369` |
| 6 | 12 | ? | bytes | `0xb1e392` |
| 7 | ? | 1 | u8 | `0xb1e3cf` |
| 8 | ? | 1 | u8 | `0xb1e3f3` |
| 9 | ? | 1 | u8 | `0xb1e417` |
| 10 | ? | 1 | u8 | `0xb1e43f` |
| 11 | ? | 1 | u8 | `0xb1e467` |
| 12 | ? | 1 | u8 | `0xb1e48f` |

## 汇编证据序列（按线序）

```asm
; 0xb1e2ad  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1e2bc  call sub_B06230 → 读 u8
; 0xb1e2ea  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1e2f9  call sub_B06230 → 读 u8
; 0xb1e30e  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1e31d  call sub_B02DD0 → 读 u32
; 0xb1e332  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1e341  call sub_B02DF0 → 读 u16
; 0xb1e35a  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1e369  call sub_B02DD0 → 读 u32
; 0xb1e392  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb1e3c0  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1e3cf  call sub_B06230 → 读 u8
; 0xb1e3e4  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1e3f3  call sub_B06230 → 读 u8
; 0xb1e408  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1e417  call sub_B06230 → 读 u8
; 0xb1e430  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1e43f  call sub_B06230 → 读 u8
; 0xb1e458  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1e467  call sub_B06230 → 读 u8
; 0xb1e480  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1e48f  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb1e4b4：call （非 IO）
```
