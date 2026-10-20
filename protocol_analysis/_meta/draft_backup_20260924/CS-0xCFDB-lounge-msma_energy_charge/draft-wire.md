# 机器草案：线格式 —— CS-0xCFDB-lounge-msma_energy_charge

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xCFDB` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `msma_energy_charge` |
| 代码位置 | `0xb94e60`..`0xb950a6` |
| 声明容量 | `0x12` |
| 字段总长 | **9** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb94eec` |
| 2 | 4 | 1 | u8 | `0xb94f04` |
| 3 | 5 | 4 | u32 | `0xb94f14` |

## 汇编证据序列（按线序）

```asm
; 0xb94eec  mov [eax] → 内联写 u32
; 0xb94f04  mov [edx] → 内联写 u8
; 0xb94f14  call sub_B02D80 → 写 u32
; —— 扫描停止于 0xb94f58：call sub_B03020（非 IO）
```
