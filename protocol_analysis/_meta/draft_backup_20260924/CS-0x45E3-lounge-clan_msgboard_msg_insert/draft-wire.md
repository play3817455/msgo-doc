# 机器草案：线格式 —— CS-0x45E3-lounge-clan_msgboard_msg_insert

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x45E3` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `clan_msgboard_msg_insert` |
| 代码位置 | `0xba1fd0`..`0xba2275` |
| 声明容量 | `0xD6` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xba2062` |
| 2 | 4 | 2 | u16 | `0xba207b` |
| 3 | 6 | ? | bytes | `0xba2091` |
| 4 | ? | 1 | u8 | `0xba20ab` |

## 汇编证据序列（按线序）

```asm
; 0xba2062  mov [eax] → 内联写 u32
; 0xba207b  mov [edx] → 内联写 u16
; 0xba2091  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xba20ab  call sub_B061C0 → 写 u8
; —— 扫描停止于 0xba20ef：call sub_B03020（非 IO）
```
