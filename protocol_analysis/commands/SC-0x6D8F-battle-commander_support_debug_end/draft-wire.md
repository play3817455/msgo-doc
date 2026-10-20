# 机器草案：线格式 —— SC-0x6D8F-battle-commander_support_debug_end

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x6D8F` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `commander_support_debug_end` |
| 代码位置 | `0xb1dbd7`..`0xb1df1e` |
| 声明容量 | `0xB` |
| 字段总长 | **11** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb1dd19`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 1 | u8 | `0xb1dc27` |
| 2 | 1 | 1 | u8 | `0xb1dc67` |
| 3 | 2 | 4 | u32 | `0xb1dc8b` |
| 4 | 6 | 2 | u16 | `0xb1dcaf` |
| 5 | 8 | 2 | u16 | `0xb1dcd7` |
| 6 | 10 | 1 | u8 | `0xb1dcff` |

## 汇编证据序列（按线序）

```asm
; 0xb1dc18  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1dc27  call sub_B06230 → 读 u8
; 0xb1dc58  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1dc67  call sub_B06230 → 读 u8
; 0xb1dc7c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1dc8b  call sub_B02DD0 → 读 u32
; 0xb1dca0  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1dcaf  call sub_B02DF0 → 读 u16
; 0xb1dcc8  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1dcd7  call sub_B02DF0 → 读 u16
; 0xb1dcf0  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1dcff  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb1dd27：call （非 IO）
```
