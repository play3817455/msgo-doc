# 机器草案：线格式 —— SC-0x81FB-lounge-msma_weapon_unlock_complete_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x81FB` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_weapon_unlock_complete_r` |
| 代码位置 | `0xb6a075`..`0xb6a327` |
| 声明容量 | `0x11` |
| 字段总长 | **17** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb6a0cc` |
| 2 | 4 | 8 | u64 | `0xb6a10c` |
| 3 | 12 | 4 | u32 | `0xb6a14c` |
| 4 | 16 | 1 | u8 | `0xb6a170` |

## 汇编证据序列（按线序）

```asm
; 0xb6a0bd  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6a0cc  call sub_B02DD0 → 读 u32
; 0xb6a0fd  call sub_B41A10 → 解码缓冲预留 u64（非字段）
; 0xb6a10c  call sub_B06200 → 读 u64
; 0xb6a13d  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6a14c  call sub_B02DD0 → 读 u32
; 0xb6a161  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb6a170  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb6a194：call （非 IO）
```
