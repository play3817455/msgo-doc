# 机器草案：线格式 —— SC-0xD847-lounge-replay_get_access_url

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xD847` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `replay_get_access_url` |
| 代码位置 | `0xb7f0a6`..`0xb7f219` |
| 声明容量 | `0x101` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | ? | bytes | `0xb7f0ee` |

## 汇编证据序列（按线序）

```asm
; 0xb7f0ee  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; —— 扫描停止于 0xb7f125：call sub_B41110（非 IO）
```
