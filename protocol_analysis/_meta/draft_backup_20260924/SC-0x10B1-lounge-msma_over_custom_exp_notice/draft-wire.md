# 机器草案：线格式 —— SC-0x10B1-lounge-msma_over_custom_exp_notice

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x10B1` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_over_custom_exp_notice` |
| 代码位置 | `0xb55a33`..`0xb55c1e` |
| 声明容量 | `0xC` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 8 | u64 | `0xb55a8a` |
| 2 | 8 | 4 | u32 | `0xb55aca` |

## 汇编证据序列（按线序）

```asm
; 0xb55a7b  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb55a8a  call sub_B06200 → 读 u64
; 0xb55abb  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb55aca  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb55aee：call （非 IO）
```
