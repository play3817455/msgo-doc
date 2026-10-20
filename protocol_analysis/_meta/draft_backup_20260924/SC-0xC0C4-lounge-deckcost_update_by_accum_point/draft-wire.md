# 机器草案：线格式 —— SC-0xC0C4-lounge-deckcost_update_by_accum_point

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xC0C4` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `deckcost_update_by_accum_point` |
| 代码位置 | `0xb77696`..`0xb77a2a` |
| 声明容量 | `0x1C` |
| 字段总长 | **28** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb776ea` |
| 2 | 4 | 4 | u32 | `0xb77727` |
| 3 | 8 | 4 | u32 | `0xb7774b` |
| 4 | 12 | 4 | u32 | `0xb7776f` |
| 5 | 16 | 4 | u32 | `0xb77797` |
| 6 | 20 | 4 | u32 | `0xb777bf` |
| 7 | 24 | 4 | u32 | `0xb777e7` |

## 汇编证据序列（按线序）

```asm
; 0xb776db  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb776ea  call sub_B02DD0 → 读 u32
; 0xb77718  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb77727  call sub_B02DD0 → 读 u32
; 0xb7773c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7774b  call sub_B02DD0 → 读 u32
; 0xb77760  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7776f  call sub_B02DD0 → 读 u32
; 0xb77788  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb77797  call sub_B02DD0 → 读 u32
; 0xb777b0  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb777bf  call sub_B02DD0 → 读 u32
; 0xb777d8  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb777e7  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb7780c：call （非 IO）
```
