# 机器草案：线格式 —— SC-0x0876-lounge-msma_weapon_buildup_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x0876` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_weapon_buildup_r` |
| 代码位置 | `0xb542c3`..`0xb547b0` |
| 声明容量 | `0x24` |
| 字段总长 | **36** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb5431a` |
| 2 | 4 | 8 | u64 | `0xb5435a` |
| 3 | 12 | 4 | u32 | `0xb5439a` |
| 4 | 16 | 4 | u32 | `0xb543be` |
| 5 | 20 | 2 | u16 | `0xb543e2` |
| 6 | 22 | 2 | u16 | `0xb5440a` |
| 7 | 24 | 4 | u32 | `0xb54432` |
| 8 | 28 | 2 | u16 | `0xb5445a` |
| 9 | 30 | 2 | u16 | `0xb54482` |
| 10 | 32 | 4 | u32 | `0xb544aa` |

## 汇编证据序列（按线序）

```asm
; 0xb5430b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5431a  call sub_B02DD0 → 读 u32
; 0xb5434b  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb5435a  call sub_B06200 → 读 u64
; 0xb5438b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5439a  call sub_B02DD0 → 读 u32
; 0xb543af  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb543be  call sub_B02DD0 → 读 u32
; 0xb543d3  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb543e2  call sub_B02DF0 → 读 u16
; 0xb543fb  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb5440a  call sub_B02DF0 → 读 u16
; 0xb54423  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb54432  call sub_B02DD0 → 读 u32
; 0xb5444b  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb5445a  call sub_B02DF0 → 读 u16
; 0xb54473  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb54482  call sub_B02DF0 → 读 u16
; 0xb5449b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb544aa  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb544d2：call （非 IO）
```
