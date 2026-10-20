# 机器草案：线格式 —— SC-0x0BCE-battle-score_update_coopwave

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x0BCE` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `score_update_coopwave` |
| 代码位置 | `0xb0e879`..`0xb0ec1f` |
| 声明容量 | `0x16` |
| 字段总长 | **22** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb0e9ea`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb0e8d0` |
| 2 | 4 | 4 | u32 | `0xb0e910` |
| 3 | 8 | 4 | u32 | `0xb0e934` |
| 4 | 12 | 2 | u16 | `0xb0e958` |
| 5 | 14 | 4 | u32 | `0xb0e980` |
| 6 | 18 | 2 | u16 | `0xb0e9a8` |
| 7 | 20 | 2 | u16 | `0xb0e9d0` |

## 汇编证据序列（按线序）

```asm
; 0xb0e8c1  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0e8d0  call sub_B02DD0 → 读 u32
; 0xb0e901  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0e910  call sub_B02DD0 → 读 u32
; 0xb0e925  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0e934  call sub_B02DD0 → 读 u32
; 0xb0e949  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb0e958  call sub_B02DF0 → 读 u16
; 0xb0e971  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0e980  call sub_B02DD0 → 读 u32
; 0xb0e999  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb0e9a8  call sub_B02DF0 → 读 u16
; 0xb0e9c1  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb0e9d0  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb0e9f8：call （非 IO）
```
