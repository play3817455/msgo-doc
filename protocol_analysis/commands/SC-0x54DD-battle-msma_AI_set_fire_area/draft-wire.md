# 机器草案：线格式 —— SC-0x54DD-battle-msma_AI_set_fire_area

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x54DD` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `msma_AI_set_fire_area` |
| 代码位置 | `0xb17516`..`0xb179d8` |
| 声明容量 | `0x14` |
| 字段总长 | **20** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb176ff`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb1756d` |
| 2 | 2 | 2 | u16 | `0xb175ad` |
| 3 | 4 | 2 | u16 | `0xb175d1` |
| 4 | 6 | 2 | u16 | `0xb175f5` |
| 5 | 8 | 2 | u16 | `0xb1761d` |
| 6 | 10 | 2 | u16 | `0xb17645` |
| 7 | 12 | 2 | u16 | `0xb1766d` |
| 8 | 14 | 2 | u16 | `0xb17695` |
| 9 | 16 | 2 | u16 | `0xb176bd` |
| 10 | 18 | 2 | u16 | `0xb176e5` |

## 汇编证据序列（按线序）

```asm
; 0xb1755e  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1756d  call sub_B02DF0 → 读 u16
; 0xb1759e  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb175ad  call sub_B02DF0 → 读 u16
; 0xb175c2  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb175d1  call sub_B02DF0 → 读 u16
; 0xb175e6  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb175f5  call sub_B02DF0 → 读 u16
; 0xb1760e  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1761d  call sub_B02DF0 → 读 u16
; 0xb17636  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb17645  call sub_B02DF0 → 读 u16
; 0xb1765e  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1766d  call sub_B02DF0 → 读 u16
; 0xb17686  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb17695  call sub_B02DF0 → 读 u16
; 0xb176ae  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb176bd  call sub_B02DF0 → 读 u16
; 0xb176d6  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb176e5  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb1770d：call （非 IO）
```
