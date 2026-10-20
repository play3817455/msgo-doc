# 机器草案：线格式 —— SC-0xD6BC-lounge-msma_deckslot_change_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xD6BC` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_deckslot_change_r` |
| 代码位置 | `0xb7eba7`..`0xb7eea2` |
| 声明容量 | `0x11` |
| 字段总长 | **17** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb7ebfe` |
| 2 | 4 | 8 | u64 | `0xb7ec3e` |
| 3 | 12 | 2 | u16 | `0xb7ec62` |
| 4 | 14 | 2 | u16 | `0xb7ec86` |
| 5 | 16 | 1 | u8 | `0xb7ecae` |

## 汇编证据序列（按线序）

```asm
; 0xb7ebef  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7ebfe  call sub_B02DD0 → 读 u32
; 0xb7ec2f  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb7ec3e  call sub_B06200 → 读 u64
; 0xb7ec53  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb7ec62  call sub_B02DF0 → 读 u16
; 0xb7ec77  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb7ec86  call sub_B02DF0 → 读 u16
; 0xb7ec9f  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb7ecae  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb7ecd6：call （非 IO）
```
