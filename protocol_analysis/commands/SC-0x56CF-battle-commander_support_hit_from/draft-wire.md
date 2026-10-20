# 机器草案：线格式 —— SC-0x56CF-battle-commander_support_hit_from

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x56CF` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `commander_support_hit_from` |
| 代码位置 | `0xb184d4`..`0xb1881f` |
| 声明容量 | `0x14` |
| 字段总长 | **20** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb1861d`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb1852b` |
| 2 | 4 | 2 | u16 | `0xb1856b` |
| 3 | 6 | 4 | u32 | `0xb1858f` |
| 4 | 10 | 4 | u32 | `0xb185b3` |
| 5 | 14 | 4 | u32 | `0xb185db` |
| 6 | 18 | 2 | u16 | `0xb18603` |

## 汇编证据序列（按线序）

```asm
; 0xb1851c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1852b  call sub_B02DD0 → 读 u32
; 0xb1855c  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1856b  call sub_B02DF0 → 读 u16
; 0xb18580  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1858f  call sub_B02DD0 → 读 u32
; 0xb185a4  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb185b3  call sub_B02DD0 → 读 u32
; 0xb185cc  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb185db  call sub_B02DD0 → 读 u32
; 0xb185f4  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb18603  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb1862b：call （非 IO）
```
