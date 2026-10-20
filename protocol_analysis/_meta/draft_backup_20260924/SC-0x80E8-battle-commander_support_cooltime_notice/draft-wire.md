# 机器草案：线格式 —— SC-0x80E8-battle-commander_support_cooltime_notice

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x80E8` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `commander_support_cooltime_notice` |
| 代码位置 | `0xb213ff`..`0xb21634` |
| 声明容量 | `0xC` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb2144f` |
| 2 | 4 | 4 | u32 | `0xb2148f` |
| 3 | 8 | 4 | u32 | `0xb214b3` |

## 汇编证据序列（按线序）

```asm
; 0xb21440  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2144f  call sub_B02DD0 → 读 u32
; 0xb21480  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2148f  call sub_B02DD0 → 读 u32
; 0xb214a4  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb214b3  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb214d7：call （非 IO）
```
