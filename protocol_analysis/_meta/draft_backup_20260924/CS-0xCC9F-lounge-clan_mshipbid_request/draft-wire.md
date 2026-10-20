# 机器草案：线格式 —— CS-0xCC9F-lounge-clan_mshipbid_request

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xCC9F` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `clan_mshipbid_request` |
| 代码位置 | `0xb9fd10`..`0xb9fef8` |
| 声明容量 | `0xA` |
| 字段总长 | **5** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb9fd99` |
| 2 | 4 | 1 | u8 | `0xb9fda5` |

## 汇编证据序列（按线序）

```asm
; 0xb9fd99  mov [ecx] → 内联写 u32
; 0xb9fda5  mov [edx] → 内联写 u8
; —— 扫描停止于 0xb9fdd7：call sub_B03020（非 IO）
```
