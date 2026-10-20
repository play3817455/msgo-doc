# 机器草案：线格式 —— CS-0x26F2-lounge-you9_cps_SCAN_response

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x26F2` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `you9_cps_SCAN_response` |
| 代码位置 | `0xba54d0`..`0xba57c9` |
| 声明容量 | `0x2336` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xba556f` |
| 2 | 4 | 4 | u32 | `0xba5585` |
| 3 | 8 | 1 | u8 | `0xba55b5` |
| 4 | 9 | ? | bytes | `0xba55db` |

## 汇编证据序列（按线序）

```asm
; 0xba556f  mov [eax] → 内联写 u32
; 0xba5585  call sub_B02D80 → 写 u32
; 0xba55b5  mov [ecx] → 内联写 u8
; 0xba55db  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; —— 扫描停止于 0xba561b：call sub_B03020（非 IO）
```
