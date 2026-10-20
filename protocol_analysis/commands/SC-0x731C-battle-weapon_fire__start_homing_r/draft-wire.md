# 机器草案：线格式 —— SC-0x731C-battle-weapon_fire__start_homing_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x731C` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__start_homing_r` |
| 代码位置 | `0xb1f0eb`..`0xb1f40f` |
| 声明容量 | `0xC` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb1f20c`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb1f142` |
| 2 | 4 | 2 | u16 | `0xb1f182` |
| 3 | 6 | 2 | u16 | `0xb1f1a6` |
| 4 | 8 | 2 | u16 | `0xb1f1ca` |
| 5 | 10 | 2 | u16 | `0xb1f1f2` |

## 汇编证据序列（按线序）

```asm
; 0xb1f133  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1f142  call sub_B02DD0 → 读 u32
; 0xb1f173  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1f182  call sub_B02DF0 → 读 u16
; 0xb1f197  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1f1a6  call sub_B02DF0 → 读 u16
; 0xb1f1bb  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1f1ca  call sub_B02DF0 → 读 u16
; 0xb1f1e3  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1f1f2  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb1f21a：call （非 IO）
```
