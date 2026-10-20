# 机器草案：线格式 —— SC-0xB40C-battle-weapon_fire__grenade_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xB40C` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__grenade_r` |
| 代码位置 | `0xb289b2`..`0xb2921d` |
| 声明容量 | `0x29` |
| 字段总长 | **41** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb28a08` |
| 2 | 2 | 4 | u32 | `0xb28a4b` |
| 3 | 6 | 4 | u32 | `0xb28a75` |
| 4 | 10 | 4 | u32 | `0xb28a99` |
| 5 | 14 | 2 | u16 | `0xb28ac1` |
| 6 | 16 | 2 | u16 | `0xb28ae9` |
| 7 | 18 | 2 | u16 | `0xb28b11` |
| 8 | 20 | 2 | u16 | `0xb28b39` |
| 9 | 22 | 2 | u16 | `0xb28b61` |
| 10 | 24 | 2 | u16 | `0xb28b89` |
| 11 | 26 | 2 | u16 | `0xb28bb1` |
| 12 | 28 | 2 | u16 | `0xb28bd9` |
| 13 | 30 | 2 | u16 | `0xb28c01` |
| 14 | 32 | 2 | u16 | `0xb28c29` |
| 15 | 34 | 2 | u16 | `0xb28c51` |
| 16 | 36 | 1 | u8 | `0xb28c79` |
| 17 | 37 | 1 | u8 | `0xb28ca1` |
| 18 | 38 | 1 | u8 | `0xb28cc9` |
| 19 | 39 | 1 | u8 | `0xb28cf1` |
| 20 | 40 | 1 | u8 | `0xb28d19` |

## 汇编证据序列（按线序）

```asm
; 0xb289f6  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28a08  call sub_B02DF0 → 读 u16
; 0xb28a39  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb28a4b  call sub_B02DD0 → 读 u32
; 0xb28a63  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb28a75  call sub_B02DD0 → 读 u32
; 0xb28a8a  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb28a99  call sub_B02DD0 → 读 u32
; 0xb28ab2  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28ac1  call sub_B02DF0 → 读 u16
; 0xb28ada  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28ae9  call sub_B02DF0 → 读 u16
; 0xb28b02  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28b11  call sub_B02DF0 → 读 u16
; 0xb28b2a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28b39  call sub_B02DF0 → 读 u16
; 0xb28b52  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28b61  call sub_B02DF0 → 读 u16
; 0xb28b7a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28b89  call sub_B02DF0 → 读 u16
; 0xb28ba2  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28bb1  call sub_B02DF0 → 读 u16
; 0xb28bca  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28bd9  call sub_B02DF0 → 读 u16
; 0xb28bf2  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28c01  call sub_B02DF0 → 读 u16
; 0xb28c1a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28c29  call sub_B02DF0 → 读 u16
; 0xb28c42  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb28c51  call sub_B02DF0 → 读 u16
; 0xb28c6a  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb28c79  call sub_B06230 → 读 u8
; 0xb28c92  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb28ca1  call sub_B06230 → 读 u8
; 0xb28cba  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb28cc9  call sub_B06230 → 读 u8
; 0xb28ce2  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb28cf1  call sub_B06230 → 读 u8
; 0xb28d0a  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb28d19  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb28d3e：call （非 IO）
```
