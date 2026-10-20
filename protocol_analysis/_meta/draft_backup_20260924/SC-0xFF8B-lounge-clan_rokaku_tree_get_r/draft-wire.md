# 机器草案：线格式 —— SC-0xFF8B-lounge-clan_rokaku_tree_get_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xFF8B` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `clan_rokaku_tree_get_r` |
| 代码位置 | `0xb88c9d`..`0xb89116` |
| 声明容量 | `0x574` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb88cf7` |
| 2 | 4 | 4 | u32 | `0xb88d22` |
| 3 | 8 | 4 | u32[] | `0xb88d59` |
| 4 | 12 | 4 | u32 | `0xb88d7a` |

## 汇编证据序列（按线序）

```asm
; 0xb88ce8  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb88cf7  call sub_B02DD0 → 读 u32
; 0xb88d22  call sub_B02DD0 → 读 u32
; 0xb88d59  call sub_B41850 → 读 u32（数组）
; 0xb88d7a  call sub_B462E0 → 读 u32
; —— 扫描停止于 0xb88d92：jmp
```
