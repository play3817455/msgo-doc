# 机器草案：线格式 —— SC-0xD9DB-lounge-msma_equip_weapon_change_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xD9DB` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_equip_weapon_change_r` |
| 代码位置 | `0xb7f64e`..`0xb7f8e6` |
| 声明容量 | `0x12` |
| 字段总长 | **18** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb7f69e` |
| 2 | 4 | 8 | u64 | `0xb7f6de` |
| 3 | 12 | 2 | u16 | `0xb7f702` |
| 4 | 14 | 4 | u32 | `0xb7f726` |

## 汇编证据序列（按线序）

```asm
; 0xb7f68f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7f69e  call sub_B02DD0 → 读 u32
; 0xb7f6cf  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb7f6de  call sub_B06200 → 读 u64
; 0xb7f6f3  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb7f702  call sub_B02DF0 → 读 u16
; 0xb7f717  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7f726  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb7f74e：call （非 IO）
```
