# 机器草案：线格式 —— SC-0x9F94-lounge-friend_history_get_xworld_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x9F94` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `friend_history_get_xworld_r` |
| 代码位置 | `0xb6e8db`..`0xb6ec7c` |
| 声明容量 | `0x352C` |
| 字段总长 | **8** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb6e92e` |
| 2 | 4 | 4 | u32 | `0xb6e960` |

## 汇编证据序列（按线序）

```asm
; 0xb6e91f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6e92e  call sub_B02DD0 → 读 u32
; 0xb6e960  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb6e99b：call sub_B415D0（非 IO）
```
