# 机器草案：线格式 —— CS-0x2A35-lounge-clan_mshipbid_response

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x2A35` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `clan_mshipbid_response` |
| 代码位置 | `0xba0260`..`0xba049c` |
| 声明容量 | `0xE` |
| 字段总长 | **9** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xba02ec` |
| 2 | 4 | 4 | u32 | `0xba0307` |
| 3 | 8 | 1 | u8 | `0xba030f` |

## 汇编证据序列（按线序）

```asm
; 0xba02ec  mov [eax] → 内联写 u32
; 0xba0307  mov [eax] → 内联写 u32
; 0xba030f  call sub_B061C0 → 写 u8
; —— 扫描停止于 0xba0353：call sub_B03020（非 IO）
```
