# 机器草案：线格式 —— SC-0x3671-lounge-mail_get_present_body_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x3671` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `mail_get_present_body_r` |
| 代码位置 | `0xb5c0c4`..`0xb5c426` |
| 声明容量 | `0x316` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb5c218`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb5c117` |
| 2 | 4 | 8 | u64 | `0xb5c157` |
| 3 | 12 | 4 | u32 | `0xb5c197` |
| 4 | 16 | 4 | u32 | `0xb5c1bb` |
| 5 | 20 | 4 | u32 | `0xb5c1df` |
| 6 | 24 | ? | bytes | `0xb5c1fe` |

## 汇编证据序列（按线序）

```asm
; 0xb5c108  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5c117  call sub_B02DD0 → 读 u32
; 0xb5c148  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb5c157  call sub_B06200 → 读 u64
; 0xb5c188  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5c197  call sub_B02DD0 → 读 u32
; 0xb5c1ac  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5c1bb  call sub_B02DD0 → 读 u32
; 0xb5c1d0  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5c1df  call sub_B02DD0 → 读 u32
; 0xb5c1fe  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; —— 扫描停止于 0xb5c226：call （非 IO）
```
