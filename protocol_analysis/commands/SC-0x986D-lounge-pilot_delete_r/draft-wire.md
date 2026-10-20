# 机器草案：线格式 —— SC-0x986D-lounge-pilot_delete_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x986D` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_delete_r` |
| 代码位置 | `0xb6db68`..`0xb6de1e` |
| 声明容量 | `0xD` |
| 字段总长 | **13** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb6dc5b`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb6dbbc` |
| 2 | 4 | 4 | u32 | `0xb6dbf9` |
| 3 | 8 | 1 | u8 | `0xb6dc1d` |
| 4 | 9 | 4 | u32 | `0xb6dc41` |

## 汇编证据序列（按线序）

```asm
; 0xb6dbad  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6dbbc  call sub_B02DD0 → 读 u32
; 0xb6dbea  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6dbf9  call sub_B02DD0 → 读 u32
; 0xb6dc0e  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb6dc1d  call sub_B06230 → 读 u8
; 0xb6dc32  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6dc41  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb6dc66：call （非 IO）
```
