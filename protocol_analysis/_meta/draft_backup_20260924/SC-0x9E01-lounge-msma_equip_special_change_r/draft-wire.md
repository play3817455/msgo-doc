# 机器草案：线格式 —— SC-0x9E01-lounge-msma_equip_special_change_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x9E01` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_equip_special_change_r` |
| 代码位置 | `0xb6ec7c`..`0xb6eec0` |
| 声明容量 | `0x10` |
| 字段总长 | **16** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb6ecd3` |
| 2 | 4 | 8 | u64 | `0xb6ed13` |
| 3 | 12 | 4 | u32 | `0xb6ed37` |

## 汇编证据序列（按线序）

```asm
; 0xb6ecc4  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6ecd3  call sub_B02DD0 → 读 u32
; 0xb6ed04  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb6ed13  call sub_B06200 → 读 u64
; 0xb6ed28  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6ed37  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb6ed5b：call （非 IO）
```
