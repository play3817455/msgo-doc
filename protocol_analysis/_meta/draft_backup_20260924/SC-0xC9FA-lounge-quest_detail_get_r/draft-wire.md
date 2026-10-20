# 机器草案：线格式 —— SC-0xC9FA-lounge-quest_detail_get_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xC9FA` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `quest_detail_get_r` |
| 代码位置 | `0xb7a40d`..`0xb7a64f` |
| 声明容量 | `0x609` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb7a467` |
| 2 | 4 | 4 | u32 | `0xb7a4a7` |
| 3 | 8 | ? | bytes | `0xb7a4c2` |

## 汇编证据序列（按线序）

```asm
; 0xb7a458  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7a467  call sub_B02DD0 → 读 u32
; 0xb7a498  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7a4a7  call sub_B02DD0 → 读 u32
; 0xb7a4c2  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; —— 扫描停止于 0xb7a4f9：call sub_B41110（非 IO）
```
