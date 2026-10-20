# 机器草案：线格式 —— SC-0x9105-battle-entity_msma_dead

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x9105` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `entity_msma_dead` |
| 代码位置 | `0xb23ae1`..`0xb23f84` |
| 声明容量 | `0x1C` |
| 字段总长 | **28** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb23cc0`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb23b31` |
| 2 | 2 | 4 | u32 | `0xb23b6e` |
| 3 | 6 | 4 | u32 | `0xb23b92` |
| 4 | 10 | 4 | u32 | `0xb23bb6` |
| 5 | 14 | 4 | u32 | `0xb23bde` |
| 6 | 18 | 2 | u16 | `0xb23c06` |
| 7 | 20 | 2 | u16 | `0xb23c2e` |
| 8 | 22 | 4 | u32 | `0xb23c56` |
| 9 | 26 | 1 | u8 | `0xb23c7e` |
| 10 | 27 | 1 | u8 | `0xb23ca6` |

## 汇编证据序列（按线序）

```asm
; 0xb23b22  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb23b31  call sub_B02DF0 → 读 u16
; 0xb23b5f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb23b6e  call sub_B02DD0 → 读 u32
; 0xb23b83  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb23b92  call sub_B02DD0 → 读 u32
; 0xb23ba7  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb23bb6  call sub_B02DD0 → 读 u32
; 0xb23bcf  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb23bde  call sub_B02DD0 → 读 u32
; 0xb23bf7  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb23c06  call sub_B02DF0 → 读 u16
; 0xb23c1f  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb23c2e  call sub_B02DF0 → 读 u16
; 0xb23c47  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb23c56  call sub_B02DD0 → 读 u32
; 0xb23c6f  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb23c7e  call sub_B06230 → 读 u8
; 0xb23c97  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb23ca6  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb23ccb：call （非 IO）
```
