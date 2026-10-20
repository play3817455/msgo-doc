# 机器草案：线格式 —— SC-0x12EC-battle-room_chat_down

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x12EC` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `room_chat_down` |
| 代码位置 | `0xb0f774`..`0xb0fbda` |
| 声明容量 | `0xDB` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 1 | u8 | `0xb0f7cb` |
| 2 | 1 | 1 | u8 | `0xb0f808` |
| 3 | 2 | 4 | u32 | `0xb0f82c` |
| 4 | 6 | 4 | u32 | `0xb0f850` |
| 5 | 10 | ? | bytes | `0xb0f875` |
| 6 | ? | ? | bytes | `0xb0f8a0` |
| 7 | ? | 1 | u8 | `0xb0f8c8` |
| 8 | ? | 1 | u8 | `0xb0f8f0` |
| 9 | ? | 1 | u8 | `0xb0f918` |

## 汇编证据序列（按线序）

```asm
; 0xb0f7bc  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb0f7cb  call sub_B06230 → 读 u8
; 0xb0f7f9  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb0f808  call sub_B06230 → 读 u8
; 0xb0f81d  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0f82c  call sub_B02DD0 → 读 u32
; 0xb0f841  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb0f850  call sub_B02DD0 → 读 u32
; 0xb0f875  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb0f8a0  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb0f8b9  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb0f8c8  call sub_B06230 → 读 u8
; 0xb0f8e1  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb0f8f0  call sub_B06230 → 读 u8
; 0xb0f909  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb0f918  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb0f93d：call （非 IO）
```
