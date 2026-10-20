# 机器草案：线格式 —— SC-0xE378-battle-weapon_fire__bit_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xE378` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__bit_r` |
| 代码位置 | `0xb2ec5a`..`0xb2f28a` |
| 声明容量 | `0x1D` |
| 字段总长 | **29** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb2ecb1` |
| 2 | 2 | 4 | u32 | `0xb2ecf1` |
| 3 | 6 | 4 | u32 | `0xb2ed15` |
| 4 | 10 | 1 | u8 | `0xb2ed39` |
| 5 | 11 | 2 | u16 | `0xb2ed61` |
| 6 | 13 | 2 | u16 | `0xb2ed89` |
| 7 | 15 | 2 | u16 | `0xb2edb1` |
| 8 | 17 | 2 | u16 | `0xb2edd9` |
| 9 | 19 | 2 | u16 | `0xb2ee01` |
| 10 | 21 | 2 | u16 | `0xb2ee29` |
| 11 | 23 | 2 | u16 | `0xb2ee51` |
| 12 | 25 | 2 | u16 | `0xb2ee79` |
| 13 | 27 | 1 | u8 | `0xb2eea1` |
| 14 | 28 | 1 | u8 | `0xb2eec9` |

## 汇编证据序列（按线序）

```asm
; 0xb2eca2  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ecb1  call sub_B02DF0 → 读 u16
; 0xb2ece2  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2ecf1  call sub_B02DD0 → 读 u32
; 0xb2ed06  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2ed15  call sub_B02DD0 → 读 u32
; 0xb2ed2a  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb2ed39  call sub_B06230 → 读 u8
; 0xb2ed52  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ed61  call sub_B02DF0 → 读 u16
; 0xb2ed7a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ed89  call sub_B02DF0 → 读 u16
; 0xb2eda2  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2edb1  call sub_B02DF0 → 读 u16
; 0xb2edca  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2edd9  call sub_B02DF0 → 读 u16
; 0xb2edf2  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ee01  call sub_B02DF0 → 读 u16
; 0xb2ee1a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ee29  call sub_B02DF0 → 读 u16
; 0xb2ee42  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ee51  call sub_B02DF0 → 读 u16
; 0xb2ee6a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2ee79  call sub_B02DF0 → 读 u16
; 0xb2ee92  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb2eea1  call sub_B06230 → 读 u8
; 0xb2eeba  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb2eec9  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb2eef1：call （非 IO）
```
