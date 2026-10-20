# 机器草案：线格式 —— SC-0x91C0-lounge-msma_plan_sort_list_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x91C0` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_plan_sort_list_r` |
| 代码位置 | `0xb6ca83`..`0xb6cd99` |
| 声明容量 | `0x10` |
| 字段总长 | **16** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb6cada` |
| 2 | 4 | 4 | u32 | `0xb6cb1a` |
| 3 | 8 | 4 | u32 | `0xb6cb3e` |
| 4 | 12 | 4 | u32 | `0xb6cb62` |

## 汇编证据序列（按线序）

```asm
; 0xb6cacb  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6cada  call sub_B02DD0 → 读 u32
; 0xb6cb0b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6cb1a  call sub_B02DD0 → 读 u32
; 0xb6cb2f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6cb3e  call sub_B02DD0 → 读 u32
; 0xb6cb53  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6cb62  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb6cb8a：call （非 IO）
```
