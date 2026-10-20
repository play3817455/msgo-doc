# 机器草案：线格式 —— SC-0xA72F-lounge-msma_sp_parts_level_update

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xA72F` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_sp_parts_level_update` |
| 代码位置 | `0xb70a91`..`0xb70ca8` |
| 声明容量 | `0xC` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 8 | u64 | `0xb70ae8` |
| 2 | 8 | 4 | u32 | `0xb70b28` |

## 汇编证据序列（按线序）

```asm
; 0xb70ad9  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb70ae8  call sub_B06200 → 读 u64
; 0xb70b19  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb70b28  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb70b4c：call （非 IO）
```
