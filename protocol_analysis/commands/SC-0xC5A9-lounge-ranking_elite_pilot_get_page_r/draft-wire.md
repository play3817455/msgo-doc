# 机器草案：线格式 —— SC-0xC5A9-lounge-ranking_elite_pilot_get_page_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xC5A9` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `ranking_elite_pilot_get_page_r` |
| 代码位置 | `0xb7869d`..`0xb78bdb` |
| 声明容量 | `0x4E8B` |
| 字段总长 | **8** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb786f7` |
| 2 | 4 | 4 | u32 | `0xb78737` |

## 汇编证据序列（按线序）

```asm
; 0xb786e8  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb786f7  call sub_B02DD0 → 读 u32
; 0xb78728  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb78737  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb7874c：call sub_B41220（非 IO）
```
