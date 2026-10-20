# 机器草案：线格式 —— CS-0xCAAF-battle-commander_get_pilotinfo

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xCAAF` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `commander_get_pilotinfo` |
| 代码位置 | `0xb3e1e0`..`0xb3e3ca` |
| 声明容量 | `0xA` |
| 字段总长 | **3** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 1 | u8 | `0xb3e269` |
| 2 | 1 | 2 | u16 | `0xb3e276` |

## 汇编证据序列（按线序）

```asm
; 0xb3e269  mov [ecx] → 内联写 u8
; 0xb3e276  mov [edi] → 内联写 u16
; —— 扫描停止于 0xb3e2a9：call sub_B03020（非 IO）
```
