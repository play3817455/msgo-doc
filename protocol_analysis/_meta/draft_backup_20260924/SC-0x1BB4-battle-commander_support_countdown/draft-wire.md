# 机器草案：线格式 —— SC-0x1BB4-battle-commander_support_countdown

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x1BB4` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `commander_support_countdown` |
| 代码位置 | `0xb11698`..`0xb11b4b` |
| 声明容量 | `0x11` |
| 字段总长 | **17** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb116ef` |
| 2 | 2 | 4 | u32 | `0xb1172f` |
| 3 | 6 | 1 | u8 | `0xb11753` |
| 4 | 7 | 1 | u8 | `0xb11777` |
| 5 | 8 | 2 | u16 | `0xb1179f` |
| 6 | 10 | 2 | u16 | `0xb117c7` |
| 7 | 12 | 2 | u16 | `0xb117ef` |
| 8 | 14 | 2 | u16 | `0xb11817` |
| 9 | 16 | 1 | u8 | `0xb1183f` |

## 汇编证据序列（按线序）

```asm
; 0xb116e0  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb116ef  call sub_B02DF0 → 读 u16
; 0xb11720  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1172f  call sub_B02DD0 → 读 u32
; 0xb11744  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb11753  call sub_B06230 → 读 u8
; 0xb11768  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb11777  call sub_B06230 → 读 u8
; 0xb11790  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1179f  call sub_B02DF0 → 读 u16
; 0xb117b8  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb117c7  call sub_B02DF0 → 读 u16
; 0xb117e0  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb117ef  call sub_B02DF0 → 读 u16
; 0xb11808  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb11817  call sub_B02DF0 → 读 u16
; 0xb11830  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1183f  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb11867：call （非 IO）
```
