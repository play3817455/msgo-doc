# 机器草案：线格式 —— SC-0xCBC6-lounge-gacha_lineup_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xCBC6` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `gacha_lineup_r` |
| 代码位置 | `0xb7ab17`..`0xb7adbe` |
| 声明容量 | `0x648` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb7ab6a` |
| 2 | 4 | 4 | u32 | `0xb7ab9c` |
| 3 | 8 | 8 | u64[] | `0xb7abda` |

## 汇编证据序列（按线序）

```asm
; 0xb7ab5b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7ab6a  call sub_B02DD0 → 读 u32
; 0xb7ab9c  call sub_B02DD0 → 读 u32
; 0xb7abda  call sub_B41690 → 读 u64（数组）
; —— 扫描停止于 0xb7abfb：call sub_B46AB0（非 IO）
```
