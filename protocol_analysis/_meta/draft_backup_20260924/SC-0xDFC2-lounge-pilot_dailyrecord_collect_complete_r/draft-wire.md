# 机器草案：线格式 —— SC-0xDFC2-lounge-pilot_dailyrecord_collect_complete_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xDFC2` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_dailyrecord_collect_complete_r` |
| 代码位置 | `0xb8212b`..`0xb8240b` |
| 声明容量 | `0x12` |
| 字段总长 | **18** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb8217b` |
| 2 | 4 | 4 | u32 | `0xb821b8` |
| 3 | 8 | 4 | u32 | `0xb821dc` |
| 4 | 12 | 2 | u16 | `0xb82200` |
| 5 | 14 | 4 | u32 | `0xb82228` |

## 汇编证据序列（按线序）

```asm
; 0xb8216c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb8217b  call sub_B02DD0 → 读 u32
; 0xb821a9  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb821b8  call sub_B02DD0 → 读 u32
; 0xb821cd  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb821dc  call sub_B02DD0 → 读 u32
; 0xb821f1  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb82200  call sub_B02DF0 → 读 u16
; 0xb82219  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb82228  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb8224d：call （非 IO）
```
