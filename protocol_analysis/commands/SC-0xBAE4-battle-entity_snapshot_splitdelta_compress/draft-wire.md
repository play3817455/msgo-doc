# 机器草案：线格式 —— SC-0xBAE4-battle-entity_snapshot_splitdelta_compress

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xBAE4` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `entity_snapshot_splitdelta_compress` |
| 代码位置 | `0xb29dc0`..`0xb2a0a0` |
| 声明容量 | `0x750C` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 3 处条件跳转（`0xb29e95`, `0xb29ead`, `0xb29ece`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb29e13` |
| 2 | 4 | 4 | u32 | `0xb29e50` |
| 3 | 8 | 4 | u32 | `0xb29e66` |
| 4 | 12 | 1 | u8[] | `0xb29ea4` |
| 5 | 13 | 1 | u8 | `0xb29ebd` |

## 汇编证据序列（按线序）

```asm
; 0xb29e04  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb29e13  call sub_B02DD0 → 读 u32
; 0xb29e41  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb29e50  call sub_B02DD0 → 读 u32
; 0xb29e66  call sub_B02DD0 → 读 u32
; 0xb29ea4  call sub_B05EA0 → 读 u8（数组）
; 0xb29ebd  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb29ed0：jmp
```
