# 机器草案：线格式 —— SC-0x6735-battle-deliver_oration

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x6735` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `deliver_oration` |
| 代码位置 | `0xb1c9d4`..`0xb1cbe4` |
| 声明容量 | `0x8` |
| 字段总长 | **8** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb1ca2b` |
| 2 | 4 | 4 | u32 | `0xb1ca6b` |

## 汇编证据序列（按线序）

```asm
; 0xb1ca1c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1ca2b  call sub_B02DD0 → 读 u32
; 0xb1ca5c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1ca6b  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb1ca8f：call （非 IO）
```
