# 机器草案：线格式 —— SC-0x73CE-battle-entity_msma_attach

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x73CE` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `entity_msma_attach` |
| 代码位置 | `0xb1f6a1`..`0xb1f9e7` |
| 声明容量 | `0xB` |
| 字段总长 | **11** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb1f7e4`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb1f6f5` |
| 2 | 2 | 2 | u16 | `0xb1f732` |
| 3 | 4 | 1 | u8 | `0xb1f756` |
| 4 | 5 | 2 | u16 | `0xb1f77a` |
| 5 | 7 | 2 | u16 | `0xb1f7a2` |
| 6 | 9 | 2 | u16 | `0xb1f7ca` |

## 汇编证据序列（按线序）

```asm
; 0xb1f6e6  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1f6f5  call sub_B02DF0 → 读 u16
; 0xb1f723  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1f732  call sub_B02DF0 → 读 u16
; 0xb1f747  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1f756  call sub_B06230 → 读 u8
; 0xb1f76b  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1f77a  call sub_B02DF0 → 读 u16
; 0xb1f793  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1f7a2  call sub_B02DF0 → 读 u16
; 0xb1f7bb  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1f7ca  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb1f7ef：call （非 IO）
```
