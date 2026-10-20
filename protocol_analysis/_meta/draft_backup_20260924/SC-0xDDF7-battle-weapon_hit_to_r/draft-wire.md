# 机器草案：线格式 —— SC-0xDDF7-battle-weapon_hit_to_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xDDF7` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_hit_to_r` |
| 代码位置 | `0xb2cff8`..`0xb2d340` |
| 声明容量 | `0x10` |
| 字段总长 | **16** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb2d048` |
| 2 | 4 | 2 | u16 | `0xb2d088` |
| 3 | 6 | 4 | u32 | `0xb2d0ac` |
| 4 | 10 | 2 | u16 | `0xb2d0d0` |
| 5 | 12 | 2 | u16 | `0xb2d0f8` |
| 6 | 14 | 2 | u16 | `0xb2d120` |

## 汇编证据序列（按线序）

```asm
; 0xb2d039  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2d048  call sub_B02DD0 → 读 u32
; 0xb2d079  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2d088  call sub_B02DF0 → 读 u16
; 0xb2d09d  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2d0ac  call sub_B02DD0 → 读 u32
; 0xb2d0c1  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2d0d0  call sub_B02DF0 → 读 u16
; 0xb2d0e9  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2d0f8  call sub_B02DF0 → 读 u16
; 0xb2d111  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2d120  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb2d148：call （非 IO）
```
