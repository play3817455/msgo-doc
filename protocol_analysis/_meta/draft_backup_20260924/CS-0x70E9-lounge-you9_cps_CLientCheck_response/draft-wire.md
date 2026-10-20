# 机器草案：线格式 —— CS-0x70E9-lounge-you9_cps_CLientCheck_response

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x70E9` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `you9_cps_CLientCheck_response` |
| 代码位置 | `0xba57d0`..`0xba5bd6` |
| 声明容量 | `0xA42` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xba586c` |
| 2 | 4 | ? | bytes | `0xba5874` |
| 3 | ? | ? | bytes | `0xba5890` |
| 4 | ? | 4 | u32 | `0xba58aa` |
| 5 | ? | ? | bytes | `0xba58c6` |
| 6 | ? | ? | bytes | `0xba58e5` |
| 7 | ? | ? | bytes | `0xba5904` |
| 8 | ? | ? | bytes | `0xba5923` |

## 汇编证据序列（按线序）

```asm
; 0xba586c  mov [eax] → 内联写 u32
; 0xba5874  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xba5890  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xba58aa  call sub_B02D80 → 写 u32
; 0xba58c6  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xba58e5  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xba5904  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xba5923  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; —— 扫描停止于 0xba5967：call sub_B03020（非 IO）
```
