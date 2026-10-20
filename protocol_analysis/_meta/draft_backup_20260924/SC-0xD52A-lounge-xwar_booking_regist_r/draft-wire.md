# 机器草案：线格式 —— SC-0xD52A-lounge-xwar_booking_regist_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xD52A` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `xwar_booking_regist_r` |
| 代码位置 | `0xb7d3a2`..`0xb7d7ff` |
| 声明容量 | `0x19` |
| 字段总长 | **25** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb7d3f9` |
| 2 | 4 | 4 | u32 | `0xb7d439` |
| 3 | 8 | 1 | u8 | `0xb7d45d` |
| 4 | 9 | 4 | u32 | `0xb7d481` |
| 5 | 13 | 4 | u32 | `0xb7d4a9` |
| 6 | 17 | 4 | u32 | `0xb7d4d1` |
| 7 | 21 | 1 | u8 | `0xb7d4f9` |
| 8 | 22 | 2 | u16 | `0xb7d521` |
| 9 | 24 | 1 | u8 | `0xb7d549` |

## 汇编证据序列（按线序）

```asm
; 0xb7d3ea  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7d3f9  call sub_B02DD0 → 读 u32
; 0xb7d42a  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7d439  call sub_B02DD0 → 读 u32
; 0xb7d44e  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb7d45d  call sub_B06230 → 读 u8
; 0xb7d472  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7d481  call sub_B02DD0 → 读 u32
; 0xb7d49a  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7d4a9  call sub_B02DD0 → 读 u32
; 0xb7d4c2  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7d4d1  call sub_B02DD0 → 读 u32
; 0xb7d4ea  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb7d4f9  call sub_B06230 → 读 u8
; 0xb7d512  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb7d521  call sub_B02DF0 → 读 u16
; 0xb7d53a  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb7d549  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb7d571：call （非 IO）
```
