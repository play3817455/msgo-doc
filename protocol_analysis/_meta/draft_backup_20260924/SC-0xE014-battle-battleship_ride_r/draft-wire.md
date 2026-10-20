# 机器草案：线格式 —— SC-0xE014-battle-battleship_ride_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xE014` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `battleship_ride_r` |
| 代码位置 | `0xb2d9a8`..`0xb2ddfe` |
| 声明容量 | `0x20` |
| 字段总长 | **32** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb2d9ff` |
| 2 | 4 | 4 | u32 | `0xb2da3f` |
| 3 | 8 | 4 | u32 | `0xb2da63` |
| 4 | 12 | 2 | u16 | `0xb2da87` |
| 5 | 14 | 2 | u16 | `0xb2daaf` |
| 6 | 16 | 4 | u32 | `0xb2dad7` |
| 7 | 20 | 4 | u32 | `0xb2daff` |
| 8 | 24 | 4 | u32 | `0xb2db27` |
| 9 | 28 | 4 | u32 | `0xb2db4f` |

## 汇编证据序列（按线序）

```asm
; 0xb2d9f0  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2d9ff  call sub_B02DD0 → 读 u32
; 0xb2da30  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2da3f  call sub_B02DD0 → 读 u32
; 0xb2da54  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2da63  call sub_B02DD0 → 读 u32
; 0xb2da78  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2da87  call sub_B02DF0 → 读 u16
; 0xb2daa0  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2daaf  call sub_B02DF0 → 读 u16
; 0xb2dac8  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2dad7  call sub_B02DD0 → 读 u32
; 0xb2daf0  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2daff  call sub_B02DD0 → 读 u32
; 0xb2db18  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2db27  call sub_B02DD0 → 读 u32
; 0xb2db40  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2db4f  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb2db77：call （非 IO）
```
