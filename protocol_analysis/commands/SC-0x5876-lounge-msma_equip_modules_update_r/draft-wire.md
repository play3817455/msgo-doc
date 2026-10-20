# 机器草案：线格式 —— SC-0x5876-lounge-msma_equip_modules_update_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x5876` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_equip_modules_update_r` |
| 代码位置 | `0xb629be`..`0xb62cc8` |
| 声明容量 | `0x38` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb62a15` |
| 2 | 4 | 8 | u64 | `0xb62a55` |

## 汇编证据序列（按线序）

```asm
; 0xb62a06  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb62a15  call sub_B02DD0 → 读 u32
; 0xb62a46  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb62a55  call sub_B06200 → 读 u64
; —— 扫描停止于 0xb62a6a：call sub_B418C0（非 IO）
```
