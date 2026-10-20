# 机器草案：线格式 —— CS-0x5456-battle-msma_AI_set_stat

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x5456` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `msma_AI_set_stat` |
| 代码位置 | `0xb3ce60`..`0xb3d203` |
| 声明容量 | `0x5E` |
| 字段总长 | **18** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb3cefb` |
| 2 | 2 | 4 | u32 | `0xb3cf12` |
| 3 | 6 | 4 | u32 | `0xb3cf42` |
| 4 | 10 | 4 | u32 | `0xb3cf6c` |
| 5 | 14 | 4 | u32 | `0xb3cfa1` |

## 汇编证据序列（按线序）

```asm
; 0xb3cefb  mov [eax] → 内联写 u16
; 0xb3cf12  call sub_B02D80 → 写 u32
; 0xb3cf42  mov [ecx] → 内联写 u32
; 0xb3cf6c  call sub_B02D80 → 写 u32
; 0xb3cfa1  mov [ecx] → 内联写 u32
; —— 扫描停止于 0xb3cfe4：call sub_B03020（非 IO）
```
