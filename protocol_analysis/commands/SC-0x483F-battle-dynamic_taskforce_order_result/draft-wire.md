# 机器草案：线格式 —— SC-0x483F-battle-dynamic_taskforce_order_result

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x483F` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `dynamic_taskforce_order_result` |
| 代码位置 | `0xb152b4`..`0xb1559e` |
| 声明容量 | `0xB` |
| 字段总长 | **11** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb153ce`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb15304` |
| 2 | 4 | 1 | u8 | `0xb15344` |
| 3 | 5 | 1 | u8 | `0xb15368` |
| 4 | 6 | 1 | u8 | `0xb1538c` |
| 5 | 7 | 4 | u32 | `0xb153b4` |

## 汇编证据序列（按线序）

```asm
; 0xb152f5  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb15304  call sub_B02DD0 → 读 u32
; 0xb15335  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb15344  call sub_B06230 → 读 u8
; 0xb15359  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb15368  call sub_B06230 → 读 u8
; 0xb1537d  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1538c  call sub_B06230 → 读 u8
; 0xb153a5  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb153b4  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb153dc：call （非 IO）
```
