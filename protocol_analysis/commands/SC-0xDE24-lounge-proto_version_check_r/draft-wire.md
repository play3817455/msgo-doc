# 机器草案：线格式 —— SC-0xDE24-lounge-proto_version_check_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xDE24` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `proto_version_check_r` |
| 代码位置 | `0xb81d0a`..`0xb81f35` |
| 声明容量 | `0xC` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb81dd7`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb81d5e` |
| 2 | 4 | 4 | u32 | `0xb81d9b` |
| 3 | 8 | 4 | u32 | `0xb81dbf` |

## 汇编证据序列（按线序）

```asm
; 0xb81d4f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb81d5e  call sub_B02DD0 → 读 u32
; 0xb81d8c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb81d9b  call sub_B02DD0 → 读 u32
; 0xb81db0  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb81dbf  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb81de0：call （非 IO）
```
