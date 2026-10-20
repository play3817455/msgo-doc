# 机器草案：线格式 —— SC-0x759C-battle-deliver_assault_stghold_ace_status

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x759C` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `deliver_assault_stghold_ace_status` |
| 代码位置 | `0xb1f9e7`..`0xb1fe61` |
| 声明容量 | `0x11` |
| 字段总长 | **17** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 1 | u8 | `0xb1fa3e` |
| 2 | 1 | 1 | u8 | `0xb1fa7e` |
| 3 | 2 | 2 | u16 | `0xb1faa2` |
| 4 | 4 | 2 | u16 | `0xb1fac6` |
| 5 | 6 | 2 | u16 | `0xb1faee` |
| 6 | 8 | 2 | u16 | `0xb1fb16` |
| 7 | 10 | 1 | u8 | `0xb1fb3e` |
| 8 | 11 | 2 | u16 | `0xb1fb66` |
| 9 | 13 | 4 | u32 | `0xb1fb8e` |

## 汇编证据序列（按线序）

```asm
; 0xb1fa2f  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1fa3e  call sub_B06230 → 读 u8
; 0xb1fa6f  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1fa7e  call sub_B06230 → 读 u8
; 0xb1fa93  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1faa2  call sub_B02DF0 → 读 u16
; 0xb1fab7  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1fac6  call sub_B02DF0 → 读 u16
; 0xb1fadf  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1faee  call sub_B02DF0 → 读 u16
; 0xb1fb07  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1fb16  call sub_B02DF0 → 读 u16
; 0xb1fb2f  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1fb3e  call sub_B06230 → 读 u8
; 0xb1fb57  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1fb66  call sub_B02DF0 → 读 u16
; 0xb1fb7f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1fb8e  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb1fbb6：call （非 IO）
```
