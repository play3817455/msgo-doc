# 机器草案：线格式 —— SC-0xA34A-lounge-msma_create_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xA34A` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_create_r` |
| 代码位置 | `0xb6fcda`..`0xb6ff84` |
| 声明容量 | `0x14` |
| 字段总长 | **20** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb6fd2a` |
| 2 | 4 | 8 | u64 | `0xb6fd6a` |
| 3 | 12 | 4 | u32 | `0xb6fdaa` |
| 4 | 16 | 4 | u32 | `0xb6fdce` |

## 汇编证据序列（按线序）

```asm
; 0xb6fd1b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6fd2a  call sub_B02DD0 → 读 u32
; 0xb6fd5b  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb6fd6a  call sub_B06200 → 读 u64
; 0xb6fd9b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6fdaa  call sub_B02DD0 → 读 u32
; 0xb6fdbf  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6fdce  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb6fdf2：call （非 IO）
```
