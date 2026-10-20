# 机器草案：线格式 —— SC-0xDE68-lounge-msma_weapon_buildup_complete_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xDE68` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_weapon_buildup_complete_r` |
| 代码位置 | `0xb8183f`..`0xb81d0a` |
| 声明容量 | `0x24` |
| 字段总长 | **36** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb81a39`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb8188f` |
| 2 | 4 | 8 | u64 | `0xb818cf` |
| 3 | 12 | 4 | u32 | `0xb8190f` |
| 4 | 16 | 4 | u32 | `0xb81933` |
| 5 | 20 | 2 | u16 | `0xb81957` |
| 6 | 22 | 2 | u16 | `0xb8197f` |
| 7 | 24 | 4 | u32 | `0xb819a7` |
| 8 | 28 | 2 | u16 | `0xb819cf` |
| 9 | 30 | 2 | u16 | `0xb819f7` |
| 10 | 32 | 4 | u32 | `0xb81a1f` |

## 汇编证据序列（按线序）

```asm
; 0xb81880  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb8188f  call sub_B02DD0 → 读 u32
; 0xb818c0  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb818cf  call sub_B06200 → 读 u64
; 0xb81900  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb8190f  call sub_B02DD0 → 读 u32
; 0xb81924  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb81933  call sub_B02DD0 → 读 u32
; 0xb81948  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb81957  call sub_B02DF0 → 读 u16
; 0xb81970  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb8197f  call sub_B02DF0 → 读 u16
; 0xb81998  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb819a7  call sub_B02DD0 → 读 u32
; 0xb819c0  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb819cf  call sub_B02DF0 → 读 u16
; 0xb819e8  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb819f7  call sub_B02DF0 → 读 u16
; 0xb81a10  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb81a1f  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb81a47：call （非 IO）
```
