# 机器草案：线格式 —— SC-0x0124-lounge-xwar_forcegauge_get_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x0124` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `xwar_forcegauge_get_r` |
| 代码位置 | `0xb51e9a`..`0xb52213` |
| 声明容量 | `0x90` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb51fe0`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb51ef4` |
| 2 | 4 | 4 | u32 | `0xb51f34` |
| 3 | 8 | ? | bytes | `0xb51f55` |
| 4 | ? | ? | bytes | `0xb51f76` |
| 5 | ? | 4 | u32 | `0xb51f9e` |
| 6 | ? | 2 | u16 | `0xb51fc6` |

## 汇编证据序列（按线序）

```asm
; 0xb51ee5  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb51ef4  call sub_B02DD0 → 读 u32
; 0xb51f25  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb51f34  call sub_B02DD0 → 读 u32
; 0xb51f55  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb51f76  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb51f8f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb51f9e  call sub_B02DD0 → 读 u32
; 0xb51fb7  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb51fc6  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb51fee：call （非 IO）
```
