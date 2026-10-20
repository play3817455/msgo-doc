# 机器草案：线格式 —— SC-0xEAEA-battle-weapon_fire_prepare__destruct

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xEAEA` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire_prepare__destruct` |
| 代码位置 | `0xb2f913`..`0xb2fb4a` |
| 声明容量 | `0xA` |
| 字段总长 | **10** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb2f9dd`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb2f963` |
| 2 | 2 | 4 | u32 | `0xb2f9a3` |
| 3 | 6 | 4 | u32 | `0xb2f9c7` |

## 汇编证据序列（按线序）

```asm
; 0xb2f954  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2f963  call sub_B02DF0 → 读 u16
; 0xb2f994  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2f9a3  call sub_B02DD0 → 读 u32
; 0xb2f9b8  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2f9c7  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb2f9eb：call （非 IO）
```
