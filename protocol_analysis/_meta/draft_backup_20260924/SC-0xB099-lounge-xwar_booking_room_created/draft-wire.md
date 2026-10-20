# 机器草案：线格式 —— SC-0xB099-lounge-xwar_booking_room_created

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xB099` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `xwar_booking_room_created` |
| 代码位置 | `0xb72f43`..`0xb731d8` |
| 声明容量 | `0x10` |
| 字段总长 | **16** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb72f9a` |
| 2 | 4 | 4 | u32 | `0xb72fda` |
| 3 | 8 | 4 | u32 | `0xb72ffe` |
| 4 | 12 | 4 | u32 | `0xb73022` |

## 汇编证据序列（按线序）

```asm
; 0xb72f8b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb72f9a  call sub_B02DD0 → 读 u32
; 0xb72fcb  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb72fda  call sub_B02DD0 → 读 u32
; 0xb72fef  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb72ffe  call sub_B02DD0 → 读 u32
; 0xb73013  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb73022  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb7304a：call （非 IO）
```
