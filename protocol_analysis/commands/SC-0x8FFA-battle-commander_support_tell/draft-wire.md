# 机器草案：线格式 —— SC-0x8FFA-battle-commander_support_tell

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x8FFA` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `commander_support_tell` |
| 代码位置 | `0xb23f84`..`0xb2466a` |
| 声明容量 | `0x27` |
| 字段总长 | **39** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb2425d`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 1 | u8 | `0xb23fdb` |
| 2 | 1 | 1 | u8 | `0xb2401b` |
| 3 | 2 | 4 | u32 | `0xb2403f` |
| 4 | 6 | 2 | u16 | `0xb24063` |
| 5 | 8 | 2 | u16 | `0xb2408b` |
| 6 | 10 | 2 | u16 | `0xb240b3` |
| 7 | 12 | 2 | u16 | `0xb240db` |
| 8 | 14 | 2 | u16 | `0xb24103` |
| 9 | 16 | 1 | u8 | `0xb2412b` |
| 10 | 17 | 2 | u16 | `0xb24153` |
| 11 | 19 | 2 | u16 | `0xb2417b` |
| 12 | 21 | 4 | u32 | `0xb241a3` |
| 13 | 25 | 4 | u32 | `0xb241cb` |
| 14 | 29 | 4 | u32 | `0xb241f3` |
| 15 | 33 | 2 | u16 | `0xb2421b` |
| 16 | 35 | 4 | u32 | `0xb24243` |

## 汇编证据序列（按线序）

```asm
; 0xb23fcc  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb23fdb  call sub_B06230 → 读 u8
; 0xb2400c  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb2401b  call sub_B06230 → 读 u8
; 0xb24030  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2403f  call sub_B02DD0 → 读 u32
; 0xb24054  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb24063  call sub_B02DF0 → 读 u16
; 0xb2407c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2408b  call sub_B02DF0 → 读 u16
; 0xb240a4  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb240b3  call sub_B02DF0 → 读 u16
; 0xb240cc  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb240db  call sub_B02DF0 → 读 u16
; 0xb240f4  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb24103  call sub_B02DF0 → 读 u16
; 0xb2411c  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb2412b  call sub_B06230 → 读 u8
; 0xb24144  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb24153  call sub_B02DF0 → 读 u16
; 0xb2416c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2417b  call sub_B02DF0 → 读 u16
; 0xb24194  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb241a3  call sub_B02DD0 → 读 u32
; 0xb241bc  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb241cb  call sub_B02DD0 → 读 u32
; 0xb241e4  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb241f3  call sub_B02DD0 → 读 u32
; 0xb2420c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2421b  call sub_B02DF0 → 读 u16
; 0xb24234  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb24243  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb2426b：call （非 IO）
```
