# 机器草案：线格式 —— SC-0xCDE7-lounge-msma_adop_update

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xCDE7` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_adop_update` |
| 代码位置 | `0xb7b74c`..`0xb7b990` |
| 声明容量 | `0x1A` |
| 字段总长 | **10** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb7b7a3` |
| 2 | 2 | 8 | u64 | `0xb7b7e3` |

## 汇编证据序列（按线序）

```asm
; 0xb7b794  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb7b7a3  call sub_B02DF0 → 读 u16
; 0xb7b7d4  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb7b7e3  call sub_B06200 → 读 u64
; —— 扫描停止于 0xb7b7f8：call sub_B41990（非 IO）
```
