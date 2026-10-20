# 机器草案：线格式 —— SC-0x6D20-battle-weapon_fire__deploy_arms_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x6D20` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__deploy_arms_r` |
| 代码位置 | `0xb1d687`..`0xb1dbd7` |
| 声明容量 | `0x1C` |
| 字段总长 | **28** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb1d6de` |
| 2 | 2 | 4 | u32 | `0xb1d71e` |
| 3 | 6 | 4 | u32 | `0xb1d742` |
| 4 | 10 | 2 | u16 | `0xb1d766` |
| 5 | 12 | 2 | u16 | `0xb1d78e` |
| 6 | 14 | 2 | u16 | `0xb1d7b6` |
| 7 | 16 | 2 | u16 | `0xb1d7de` |
| 8 | 18 | 1 | u8 | `0xb1d806` |
| 9 | 19 | 1 | u8 | `0xb1d82e` |
| 10 | 20 | 4 | u32 | `0xb1d856` |
| 11 | 24 | 4 | u32 | `0xb1d87e` |

## 汇编证据序列（按线序）

```asm
; 0xb1d6cf  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1d6de  call sub_B02DF0 → 读 u16
; 0xb1d70f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1d71e  call sub_B02DD0 → 读 u32
; 0xb1d733  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1d742  call sub_B02DD0 → 读 u32
; 0xb1d757  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1d766  call sub_B02DF0 → 读 u16
; 0xb1d77f  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1d78e  call sub_B02DF0 → 读 u16
; 0xb1d7a7  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1d7b6  call sub_B02DF0 → 读 u16
; 0xb1d7cf  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1d7de  call sub_B02DF0 → 读 u16
; 0xb1d7f7  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1d806  call sub_B06230 → 读 u8
; 0xb1d81f  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1d82e  call sub_B06230 → 读 u8
; 0xb1d847  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1d856  call sub_B02DD0 → 读 u32
; 0xb1d86f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1d87e  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb1d8a6：call （非 IO）
```
