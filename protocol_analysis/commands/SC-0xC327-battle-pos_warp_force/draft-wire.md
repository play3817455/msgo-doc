# 机器草案：线格式 —— SC-0xC327-battle-pos_warp_force

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xC327` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `pos_warp_force` |
| 代码位置 | `0xb2aceb`..`0xb2b05b` |
| 声明容量 | `0xC` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb2ae2e`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb2ad3f` |
| 2 | 2 | 2 | u16 | `0xb2ad7c` |
| 3 | 4 | 2 | u16 | `0xb2ada0` |
| 4 | 6 | 2 | u16 | `0xb2adc4` |
| 5 | 8 | 2 | u16 | `0xb2adec` |
| 6 | 10 | 2 | u16 | `0xb2ae14` |

## 汇编证据序列（按线序）

```asm
; 0xb2ad30  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ad3f  call sub_B02DF0 → 读 u16
; 0xb2ad6d  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ad7c  call sub_B02DF0 → 读 u16
; 0xb2ad91  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ada0  call sub_B02DF0 → 读 u16
; 0xb2adb5  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2adc4  call sub_B02DF0 → 读 u16
; 0xb2addd  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2adec  call sub_B02DF0 → 读 u16
; 0xb2ae05  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ae14  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb2ae39：call （非 IO）
```
