# 机器草案：线格式 —— SC-0x7206-battle-roomlobby_game_start_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x7206` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `roomlobby_game_start_r` |
| 代码位置 | `0xb1e7f7`..`0xb1ead5` |
| 声明容量 | `0x14` |
| 字段总长 | **20** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb1e847` |
| 2 | 4 | 4 | u32 | `0xb1e884` |
| 3 | 8 | 4 | u32 | `0xb1e8a8` |
| 4 | 12 | 4 | u32 | `0xb1e8cc` |
| 5 | 16 | 4 | u32 | `0xb1e8f4` |

## 汇编证据序列（按线序）

```asm
; 0xb1e838  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1e847  call sub_B02DD0 → 读 u32
; 0xb1e875  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1e884  call sub_B02DD0 → 读 u32
; 0xb1e899  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1e8a8  call sub_B02DD0 → 读 u32
; 0xb1e8bd  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1e8cc  call sub_B02DD0 → 读 u32
; 0xb1e8e5  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1e8f4  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb1e919：call （非 IO）
```
