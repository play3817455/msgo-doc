# 机器草案：线格式 —— SC-0xA7C3-battle-msma_AI_set_fire_point

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xA7C3` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `msma_AI_set_fire_point` |
| 代码位置 | `0xb268eb`..`0xb26cb4` |
| 声明容量 | `0xE` |
| 字段总长 | **14** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb26a5c`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb26942` |
| 2 | 2 | 2 | u16 | `0xb26982` |
| 3 | 4 | 2 | u16 | `0xb269a6` |
| 4 | 6 | 2 | u16 | `0xb269ca` |
| 5 | 8 | 2 | u16 | `0xb269f2` |
| 6 | 10 | 2 | u16 | `0xb26a1a` |
| 7 | 12 | 2 | u16 | `0xb26a42` |

## 汇编证据序列（按线序）

```asm
; 0xb26933  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb26942  call sub_B02DF0 → 读 u16
; 0xb26973  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb26982  call sub_B02DF0 → 读 u16
; 0xb26997  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb269a6  call sub_B02DF0 → 读 u16
; 0xb269bb  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb269ca  call sub_B02DF0 → 读 u16
; 0xb269e3  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb269f2  call sub_B02DF0 → 读 u16
; 0xb26a0b  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb26a1a  call sub_B02DF0 → 读 u16
; 0xb26a33  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb26a42  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb26a6a：call （非 IO）
```
