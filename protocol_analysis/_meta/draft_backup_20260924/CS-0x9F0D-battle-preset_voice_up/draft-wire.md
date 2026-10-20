# 机器草案：线格式 —— CS-0x9F0D-battle-preset_voice_up

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x9F0D` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `preset_voice_up` |
| 代码位置 | `0xb34930`..`0xb34d16` |
| 声明容量 | `0xDA` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb349c2` |
| 2 | 4 | 2 | u16 | `0xb349dc` |
| 3 | 6 | 4 | u32 | `0xb349e5` |
| 4 | 10 | 4 | u32 | `0xb349ff` |
| 5 | 14 | 1 | u8 | `0xb34a19` |
| 6 | 15 | 1 | u8 | `0xb34a33` |
| 7 | 16 | ? | bytes | `0xb34a52` |
| 8 | ? | 1 | u8 | `0xb34a6c` |
| 9 | ? | 1 | u8 | `0xb34a86` |

## 汇编证据序列（按线序）

```asm
; 0xb349c2  mov [ecx] → 内联写 u32
; 0xb349dc  mov [edx] → 内联写 u16
; 0xb349e5  call sub_B02D80 → 写 u32
; 0xb349ff  call sub_B02D80 → 写 u32
; 0xb34a19  call sub_B061C0 → 写 u8
; 0xb34a33  call sub_B061C0 → 写 u8
; 0xb34a52  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xb34a6c  call sub_B061C0 → 写 u8
; 0xb34a86  call sub_B061C0 → 写 u8
; —— 扫描停止于 0xb34aca：call sub_B03020（非 IO）
```
