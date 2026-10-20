# 机器草案：线格式 —— CS-0x434C-battle-msma_AI_move_stuckescape

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x434C` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `msma_AI_move_stuckescape` |
| 代码位置 | `0xb3d600`..`0xb3d8c2` |
| 声明容量 | `0x16` |
| 字段总长 | **10** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb3d68d` |
| 2 | 2 | 2 | u16 | `0xb3d6aa` |
| 3 | 4 | 2 | u16 | `0xb3d6b3` |
| 4 | 6 | 2 | u16 | `0xb3d6cd` |
| 5 | 8 | 2 | u16 | `0xb3d6e7` |

## 汇编证据序列（按线序）

```asm
; 0xb3d68d  mov [eax] → 内联写 u16
; 0xb3d6aa  mov [eax] → 内联写 u16
; 0xb3d6b3  call sub_B02DA0 → 写 u16
; 0xb3d6cd  call sub_B02DA0 → 写 u16
; 0xb3d6e7  call sub_B02DA0 → 写 u16
; —— 扫描停止于 0xb3d72b：call sub_B03020（非 IO）
```
