# 机器草案：线格式 —— SC-0xA8FB-battle-eqparts_ready_counter_notice

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xA8FB` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `eqparts_ready_counter_notice` |
| 代码位置 | `0xb26cb4`..`0xb26f44` |
| 声明容量 | `0xE` |
| 字段总长 | **14** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb26da6`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb26d04` |
| 2 | 4 | 2 | u16 | `0xb26d44` |
| 3 | 6 | 4 | u32 | `0xb26d68` |
| 4 | 10 | 4 | u32 | `0xb26d8c` |

## 汇编证据序列（按线序）

```asm
; 0xb26cf5  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb26d04  call sub_B02DD0 → 读 u32
; 0xb26d35  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb26d44  call sub_B02DF0 → 读 u16
; 0xb26d59  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb26d68  call sub_B02DD0 → 读 u32
; 0xb26d7d  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb26d8c  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb26db4：call （非 IO）
```
