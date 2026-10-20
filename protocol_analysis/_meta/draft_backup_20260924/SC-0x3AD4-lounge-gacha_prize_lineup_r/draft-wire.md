# 机器草案：线格式 —— SC-0x3AD4-lounge-gacha_prize_lineup_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x3AD4` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `gacha_prize_lineup_r` |
| 代码位置 | `0xb5c9b6`..`0xb5ce11` |
| 声明容量 | `0x1C37` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb5ca09` |
| 2 | 4 | 4 | u32 | `0xb5ca49` |
| 3 | 8 | 4 | u32 | `0xb5ca5f` |

## 汇编证据序列（按线序）

```asm
; 0xb5c9fa  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5ca09  call sub_B02DD0 → 读 u32
; 0xb5ca3a  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5ca49  call sub_B02DD0 → 读 u32
; 0xb5ca5f  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb5ca9d：call sub_B416C0（非 IO）
```
