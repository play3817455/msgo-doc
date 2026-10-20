# 机器草案：线格式 —— SC-0x4E70-lounge-msma_nickname_change_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x4E70` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_nickname_change_r` |
| 代码位置 | `0xb5fab7`..`0xb5fcfb` |
| 声明容量 | `0x49` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb5fb96`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb5fb0e` |
| 2 | 4 | 8 | u64 | `0xb5fb4e` |
| 3 | 12 | ? | bytes | `0xb5fb66` |

## 汇编证据序列（按线序）

```asm
; 0xb5faff  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5fb0e  call sub_B02DD0 → 读 u32
; 0xb5fb3f  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb5fb4e  call sub_B06200 → 读 u64
; 0xb5fb66  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; —— 扫描停止于 0xb5fb9d：call sub_B41110（非 IO）
```
