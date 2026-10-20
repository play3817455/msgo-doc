# 机器草案：线格式 —— SC-0xE332-battle-weapon_hit_from_with_stumble

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xE332` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_hit_from_with_stumble` |
| 代码位置 | `0xb2e55f`..`0xb2e8c8` |
| 声明容量 | `0x10` |
| 字段总长 | **16** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb2e6a8`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb2e5b6` |
| 2 | 2 | 2 | u16 | `0xb2e5f6` |
| 3 | 4 | 4 | u32 | `0xb2e61a` |
| 4 | 8 | 4 | u32 | `0xb2e63e` |
| 5 | 12 | 2 | u16 | `0xb2e666` |
| 6 | 14 | 2 | u16 | `0xb2e68e` |

## 汇编证据序列（按线序）

```asm
; 0xb2e5a7  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2e5b6  call sub_B02DF0 → 读 u16
; 0xb2e5e7  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2e5f6  call sub_B02DF0 → 读 u16
; 0xb2e60b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2e61a  call sub_B02DD0 → 读 u32
; 0xb2e62f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2e63e  call sub_B02DD0 → 读 u32
; 0xb2e657  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2e666  call sub_B02DF0 → 读 u16
; 0xb2e67f  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2e68e  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb2e6b6：call （非 IO）
```
