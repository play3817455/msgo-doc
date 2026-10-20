# 机器草案：线格式 —— CS-0xEA5A-battle-active_weapon_change

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xEA5A` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `active_weapon_change` |
| 代码位置 | `0xb360b0`..`0xb362e9` |
| 声明容量 | `0xE` |
| 字段总长 | **7** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb3613c` |
| 2 | 4 | 1 | u8 | `0xb36155` |
| 3 | 5 | 2 | u16 | `0xb3615d` |

## 汇编证据序列（按线序）

```asm
; 0xb3613c  mov [ecx] → 内联写 u32
; 0xb36155  mov [edx] → 内联写 u8
; 0xb3615d  call sub_B02DA0 → 写 u16
; —— 扫描停止于 0xb361a1：call sub_B03020（非 IO）
```
