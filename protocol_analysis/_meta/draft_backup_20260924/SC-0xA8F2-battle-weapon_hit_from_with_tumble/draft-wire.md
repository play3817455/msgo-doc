# 机器草案：线格式 —— SC-0xA8F2-battle-weapon_hit_from_with_tumble

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xA8F2` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_hit_from_with_tumble` |
| 代码位置 | `0xb26f44`..`0xb27293` |
| 声明容量 | `0x10` |
| 字段总长 | **16** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb26f9b` |
| 2 | 2 | 2 | u16 | `0xb26fdb` |
| 3 | 4 | 4 | u32 | `0xb26fff` |
| 4 | 8 | 4 | u32 | `0xb27023` |
| 5 | 12 | 2 | u16 | `0xb2704b` |
| 6 | 14 | 2 | u16 | `0xb27073` |

## 汇编证据序列（按线序）

```asm
; 0xb26f8c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb26f9b  call sub_B02DF0 → 读 u16
; 0xb26fcc  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb26fdb  call sub_B02DF0 → 读 u16
; 0xb26ff0  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb26fff  call sub_B02DD0 → 读 u32
; 0xb27014  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb27023  call sub_B02DD0 → 读 u32
; 0xb2703c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2704b  call sub_B02DF0 → 读 u16
; 0xb27064  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb27073  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb2709b：call （非 IO）
```
