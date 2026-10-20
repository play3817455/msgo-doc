# 机器草案：线格式 —— SC-0x6295-battle-combat_operation_start

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x6295` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `combat_operation_start` |
| 代码位置 | `0xb1bdec`..`0xb1c246` |
| 声明容量 | `0x18` |
| 字段总长 | **24** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 1 | u8 | `0xb1be43` |
| 2 | 1 | 1 | u8 | `0xb1be83` |
| 3 | 2 | 4 | u32 | `0xb1bea7` |
| 4 | 6 | 4 | u32 | `0xb1becb` |
| 5 | 10 | 2 | u16 | `0xb1bef3` |
| 6 | 12 | 2 | u16 | `0xb1bf1b` |
| 7 | 14 | 2 | u16 | `0xb1bf43` |
| 8 | 16 | 4 | u32 | `0xb1bf6b` |
| 9 | 20 | 4 | u32 | `0xb1bf93` |

## 汇编证据序列（按线序）

```asm
; 0xb1be34  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1be43  call sub_B06230 → 读 u8
; 0xb1be74  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1be83  call sub_B06230 → 读 u8
; 0xb1be98  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1bea7  call sub_B02DD0 → 读 u32
; 0xb1bebc  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1becb  call sub_B02DD0 → 读 u32
; 0xb1bee4  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1bef3  call sub_B02DF0 → 读 u16
; 0xb1bf0c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1bf1b  call sub_B02DF0 → 读 u16
; 0xb1bf34  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1bf43  call sub_B02DF0 → 读 u16
; 0xb1bf5c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1bf6b  call sub_B02DD0 → 读 u32
; 0xb1bf84  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1bf93  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb1bfbb：call （非 IO）
```
