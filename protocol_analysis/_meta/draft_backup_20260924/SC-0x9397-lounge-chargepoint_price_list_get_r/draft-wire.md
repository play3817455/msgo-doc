# 机器草案：线格式 —— SC-0x9397-lounge-chargepoint_price_list_get_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x9397` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `chargepoint_price_list_get_r` |
| 代码位置 | `0xb6d145`..`0xb6d749` |
| 声明容量 | `0x25` |
| 字段总长 | **37** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb6d19f` |
| 2 | 4 | 4 | u32 | `0xb6d1e2` |
| 3 | 8 | 4 | u32 | `0xb6d20c` |
| 4 | 12 | 4 | u32 | `0xb6d236` |
| 5 | 16 | 4 | u32 | `0xb6d25e` |
| 6 | 20 | 4 | u32 | `0xb6d286` |
| 7 | 24 | 4 | u32 | `0xb6d2ae` |
| 8 | 28 | 2 | u16 | `0xb6d2d6` |
| 9 | 30 | 2 | u16 | `0xb6d2fe` |
| 10 | 32 | 2 | u16 | `0xb6d326` |
| 11 | 34 | 1 | u8 | `0xb6d34e` |
| 12 | 35 | 1 | u8 | `0xb6d376` |
| 13 | 36 | 1 | u8 | `0xb6d39e` |

## 汇编证据序列（按线序）

```asm
; 0xb6d18d  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6d19f  call sub_B02DD0 → 读 u32
; 0xb6d1d0  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6d1e2  call sub_B02DD0 → 读 u32
; 0xb6d1fa  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6d20c  call sub_B02DD0 → 读 u32
; 0xb6d224  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6d236  call sub_B02DD0 → 读 u32
; 0xb6d24f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6d25e  call sub_B02DD0 → 读 u32
; 0xb6d277  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6d286  call sub_B02DD0 → 读 u32
; 0xb6d29f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6d2ae  call sub_B02DD0 → 读 u32
; 0xb6d2c7  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb6d2d6  call sub_B02DF0 → 读 u16
; 0xb6d2ef  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb6d2fe  call sub_B02DF0 → 读 u16
; 0xb6d317  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb6d326  call sub_B02DF0 → 读 u16
; 0xb6d33f  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb6d34e  call sub_B06230 → 读 u8
; 0xb6d367  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb6d376  call sub_B06230 → 读 u8
; 0xb6d38f  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb6d39e  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb6d3c3：call （非 IO）
```
