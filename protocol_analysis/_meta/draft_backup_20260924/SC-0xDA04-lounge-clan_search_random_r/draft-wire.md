# 机器草案：线格式 —— SC-0xDA04-lounge-clan_search_random_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xDA04` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `clan_search_random_r` |
| 代码位置 | `0xb7fd5c`..`0xb8000b` |
| 声明容量 | `0x4B5` |
| 字段总长 | **4** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb7fda8` |

## 汇编证据序列（按线序）

```asm
; 0xb7fda8  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb7fde3：call sub_B417A0（非 IO）
```
