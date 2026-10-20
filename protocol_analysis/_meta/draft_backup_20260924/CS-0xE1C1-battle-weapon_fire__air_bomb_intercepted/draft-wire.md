# 机器草案：线格式 —— CS-0xE1C1-battle-weapon_fire__air_bomb_intercepted

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xE1C1` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__air_bomb_intercepted` |
| 代码位置 | `0xb38e50`..`0xb3908a` |
| 声明容量 | `0xE` |
| 字段总长 | **10** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb38edd` |
| 2 | 2 | 4 | u32 | `0xb38ef7` |
| 3 | 6 | 4 | u32 | `0xb38eff` |

## 汇编证据序列（按线序）

```asm
; 0xb38edd  mov [ecx] → 内联写 u16
; 0xb38ef7  mov [edx] → 内联写 u32
; 0xb38eff  call sub_B02D80 → 写 u32
; —— 扫描停止于 0xb38f43：call sub_B03020（非 IO）
```
