# 机器草案：线格式 —— SC-0xE969-lounge-friend_xworld_search_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xE969` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `friend_xworld_search_r` |
| 代码位置 | `0xb8483a`..`0xb84bf8` |
| 声明容量 | `0x19DC` |
| 字段总长 | **20** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb84894` |
| 2 | 4 | 4 | u32 | `0xb848d4` |
| 3 | 8 | 4 | u32 | `0xb848f8` |
| 4 | 12 | 4 | u32 | `0xb8491c` |
| 5 | 16 | 4 | u32 | `0xb84936` |

## 汇编证据序列（按线序）

```asm
; 0xb84885  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb84894  call sub_B02DD0 → 读 u32
; 0xb848c5  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb848d4  call sub_B02DD0 → 读 u32
; 0xb848e9  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb848f8  call sub_B02DD0 → 读 u32
; 0xb8490d  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb8491c  call sub_B02DD0 → 读 u32
; 0xb84936  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb84971：call sub_B415D0（非 IO）
```
