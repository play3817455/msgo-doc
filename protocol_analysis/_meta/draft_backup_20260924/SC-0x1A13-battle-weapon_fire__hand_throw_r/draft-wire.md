# 机器草案：线格式 —— SC-0x1A13-battle-weapon_fire__hand_throw_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x1A13` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__hand_throw_r` |
| 代码位置 | `0xb10a2b`..`0xb1106d` |
| 声明容量 | `0x1D` |
| 字段总长 | **29** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb10a7f` |
| 2 | 2 | 4 | u32 | `0xb10abc` |
| 3 | 6 | 4 | u32 | `0xb10ae0` |
| 4 | 10 | 2 | u16 | `0xb10b04` |
| 5 | 12 | 2 | u16 | `0xb10b2c` |
| 6 | 14 | 2 | u16 | `0xb10b54` |
| 7 | 16 | 2 | u16 | `0xb10b7c` |
| 8 | 18 | 2 | u16 | `0xb10ba4` |
| 9 | 20 | 2 | u16 | `0xb10bcc` |
| 10 | 22 | 2 | u16 | `0xb10bf4` |
| 11 | 24 | 2 | u16 | `0xb10c1c` |
| 12 | 26 | 1 | u8 | `0xb10c44` |
| 13 | 27 | 1 | u8 | `0xb10c6c` |
| 14 | 28 | 1 | u8 | `0xb10c94` |

## 汇编证据序列（按线序）

```asm
; 0xb10a70  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb10a7f  call sub_B02DF0 → 读 u16
; 0xb10aad  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb10abc  call sub_B02DD0 → 读 u32
; 0xb10ad1  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb10ae0  call sub_B02DD0 → 读 u32
; 0xb10af5  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb10b04  call sub_B02DF0 → 读 u16
; 0xb10b1d  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb10b2c  call sub_B02DF0 → 读 u16
; 0xb10b45  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb10b54  call sub_B02DF0 → 读 u16
; 0xb10b6d  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb10b7c  call sub_B02DF0 → 读 u16
; 0xb10b95  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb10ba4  call sub_B02DF0 → 读 u16
; 0xb10bbd  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb10bcc  call sub_B02DF0 → 读 u16
; 0xb10be5  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb10bf4  call sub_B02DF0 → 读 u16
; 0xb10c0d  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb10c1c  call sub_B02DF0 → 读 u16
; 0xb10c35  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb10c44  call sub_B06230 → 读 u8
; 0xb10c5d  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb10c6c  call sub_B06230 → 读 u8
; 0xb10c85  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb10c94  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb10cb9：call （非 IO）
```
