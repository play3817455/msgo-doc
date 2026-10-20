# 机器草案：线格式 —— SC-0x6A38-battle-roomlobby_pilot_level_update

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x6A38` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `roomlobby_pilot_level_update` |
| 代码位置 | `0xb1cbe4`..`0xb1ce6d` |
| 声明容量 | `0xC` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb1ccd3`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb1cc34` |
| 2 | 4 | 4 | u32 | `0xb1cc71` |
| 3 | 8 | 2 | u16 | `0xb1cc95` |
| 4 | 10 | 2 | u16 | `0xb1ccb9` |

## 汇编证据序列（按线序）

```asm
; 0xb1cc25  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1cc34  call sub_B02DD0 → 读 u32
; 0xb1cc62  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1cc71  call sub_B02DD0 → 读 u32
; 0xb1cc86  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1cc95  call sub_B02DF0 → 读 u16
; 0xb1ccaa  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1ccb9  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb1ccde：call （非 IO）
```
