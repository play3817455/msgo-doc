# 机器草案：线格式 —— SC-0xAB9B-battle-combat_operation_target_change_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xAB9B` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `combat_operation_target_change_r` |
| 代码位置 | `0xb27f53`..`0xb282bb` |
| 声明容量 | `0x12` |
| 字段总长 | **18** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb27faa` |
| 2 | 4 | 2 | u16 | `0xb27fea` |
| 3 | 6 | 2 | u16 | `0xb2800e` |
| 4 | 8 | 2 | u16 | `0xb28032` |
| 5 | 10 | 4 | u32 | `0xb2805a` |
| 6 | 14 | 4 | u32 | `0xb28082` |

## 汇编证据序列（按线序）

```asm
; 0xb27f9b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb27faa  call sub_B02DD0 → 读 u32
; 0xb27fdb  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb27fea  call sub_B02DF0 → 读 u16
; 0xb27fff  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2800e  call sub_B02DF0 → 读 u16
; 0xb28023  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28032  call sub_B02DF0 → 读 u16
; 0xb2804b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2805a  call sub_B02DD0 → 读 u32
; 0xb28073  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb28082  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb280aa：call （非 IO）
```
