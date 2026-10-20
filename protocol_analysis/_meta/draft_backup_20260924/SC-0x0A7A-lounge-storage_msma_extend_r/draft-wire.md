# 机器草案：线格式 —— SC-0x0A7A-lounge-storage_msma_extend_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x0A7A` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `storage_msma_extend_r` |
| 代码位置 | `0xb54ed0`..`0xb550b7` |
| 声明容量 | `0x8` |
| 字段总长 | **8** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb54f27` |
| 2 | 4 | 4 | u32 | `0xb54f67` |

## 汇编证据序列（按线序）

```asm
; 0xb54f18  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb54f27  call sub_B02DD0 → 读 u32
; 0xb54f58  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb54f67  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb54f8b：call （非 IO）
```
