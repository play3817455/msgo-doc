# 机器草案：线格式 —— SC-0x99A0-lounge-shop_lineup_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x99A0` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `shop_lineup_r` |
| 代码位置 | `0xb6e172`..`0xb6e480` |
| 声明容量 | `0x2EE9` |
| 字段总长 | **9** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb6e1cc` |
| 2 | 4 | 1 | u8 | `0xb6e20c` |
| 3 | 5 | 4 | u32 | `0xb6e222` |

## 汇编证据序列（按线序）

```asm
; 0xb6e1bd  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb6e1cc  call sub_B02DD0 → 读 u32
; 0xb6e1fd  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb6e20c  call sub_B06230 → 读 u8
; 0xb6e222  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb6e260：call sub_B416C0（非 IO）
```
