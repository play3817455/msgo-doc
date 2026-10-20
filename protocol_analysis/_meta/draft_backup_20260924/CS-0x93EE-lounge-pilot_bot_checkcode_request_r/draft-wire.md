# 机器草案：线格式 —— CS-0x93EE-lounge-pilot_bot_checkcode_request_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x93EE` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_bot_checkcode_request_r` |
| 代码位置 | `0xb8c610`..`0xb8c7e6` |
| 声明容量 | `0x12` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | ? | bytes | `0xb8c69c` |

## 汇编证据序列（按线序）

```asm
; 0xb8c69c  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; —— 扫描停止于 0xb8c6e0：call sub_B03020（非 IO）
```
