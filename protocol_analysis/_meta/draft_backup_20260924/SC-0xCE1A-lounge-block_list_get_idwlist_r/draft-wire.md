# 机器草案：线格式 —— SC-0xCE1A-lounge-block_list_get_idwlist_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xCE1A` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `block_list_get_idwlist_r` |
| 代码位置 | `0xb7b3bd`..`0xb7b74c` |
| 声明容量 | `0x32C` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb7b410` |
| 2 | 4 | 4 | u32 | `0xb7b442` |
| 3 | 8 | 4 | u32[] | `0xb7b47d` |
| 4 | 12 | 4 | u32 | `0xb7b49e` |

## 汇编证据序列（按线序）

```asm
; 0xb7b401  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7b410  call sub_B02DD0 → 读 u32
; 0xb7b442  call sub_B02DD0 → 读 u32
; 0xb7b47d  call sub_B41850 → 读 u32（数组）
; 0xb7b49e  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb7b4b6：jmp
```
