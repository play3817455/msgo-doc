# 机器草案：线格式 —— CS-0x34AB-lounge-msma_weapon_unlock_estimate

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x34AB` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `msma_weapon_unlock_estimate` |
| 代码位置 | `0xb97b30`..`0xb97db6` |
| 声明容量 | `0x16` |
| 字段总长 | **20** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 4 处条件跳转（`0xb97ba1`, `0xb97bb2`, `0xb97bca`, `0xb97c1a`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb97bbc` |
| 2 | 4 | 4 | u32 | `0xb97bc2` |
| 3 | 8 | 4 | u32 | `0xb97bd4` |
| 4 | 12 | 4 | u32 | `0xb97be4` |
| 5 | 16 | 4 | u32 | `0xb97bfe` |

## 汇编证据序列（按线序）

```asm
; 0xb97bbc  mov [eax] → 内联写 u32
; 0xb97bc2  mov [eax+4] → 内联写 u32
; 0xb97bd4  mov [edx] → 内联写 u32
; 0xb97be4  call sub_B02D80 → 写 u32
; 0xb97bfe  call sub_B02D80 → 写 u32
; —— 扫描停止于 0xb97c42：call sub_B03020（非 IO）
```
