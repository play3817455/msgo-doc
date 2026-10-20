# 机器草案：线格式 —— SC-0xCADA-lounge-msma_equip_bonus_modules_update_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xCADA` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_equip_bonus_modules_update_r` |
| 代码位置 | `0xb7a837`..`0xb7ab17` |
| 声明容量 | `0x10` |
| 字段总长 | **16** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb7a90b`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb7a88e` |
| 2 | 4 | 8 | u64 | `0xb7a8ce` |
| 3 | 12 | 4 | u32 | `0xb7a8f6` |

## 汇编证据序列（按线序）

```asm
; 0xb7a87f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7a88e  call sub_B02DD0 → 读 u32
; 0xb7a8bf  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb7a8ce  call sub_B06200 → 读 u64
; 0xb7a8e3  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7a8f6  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb7a90d：jmp
```
