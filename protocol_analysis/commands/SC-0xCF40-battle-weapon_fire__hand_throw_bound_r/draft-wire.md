# 机器草案：线格式 —— SC-0xCF40-battle-weapon_fire__hand_throw_bound_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xCF40` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__hand_throw_bound_r` |
| 代码位置 | `0xb2b595`..`0xb2b995` |
| 声明容量 | `0x12` |
| 字段总长 | **18** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb2b727`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb2b5e5` |
| 2 | 4 | 2 | u16 | `0xb2b625` |
| 3 | 6 | 2 | u16 | `0xb2b649` |
| 4 | 8 | 2 | u16 | `0xb2b66d` |
| 5 | 10 | 2 | u16 | `0xb2b695` |
| 6 | 12 | 2 | u16 | `0xb2b6bd` |
| 7 | 14 | 2 | u16 | `0xb2b6e5` |
| 8 | 16 | 2 | u16 | `0xb2b70d` |

## 汇编证据序列（按线序）

```asm
; 0xb2b5d6  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2b5e5  call sub_B02DD0 → 读 u32
; 0xb2b616  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2b625  call sub_B02DF0 → 读 u16
; 0xb2b63a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2b649  call sub_B02DF0 → 读 u16
; 0xb2b65e  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2b66d  call sub_B02DF0 → 读 u16
; 0xb2b686  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2b695  call sub_B02DF0 → 读 u16
; 0xb2b6ae  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2b6bd  call sub_B02DF0 → 读 u16
; 0xb2b6d6  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2b6e5  call sub_B02DF0 → 读 u16
; 0xb2b6fe  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2b70d  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb2b735：call （非 IO）
```
