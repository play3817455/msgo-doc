# 机器草案：线格式 —— SC-0x1E49-lounge-party_enter_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x1E49` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `party_enter_r` |
| 代码位置 | `0xb57a74`..`0xb57da1` |
| 声明容量 | `0x48` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb57acb` |
| 2 | 4 | 1 | u8 | `0xb57b0b` |
| 3 | 5 | ? | bytes | `0xb57b30` |
| 4 | ? | 2 | u16 | `0xb57b70` |
| 5 | ? | 4 | u32 | `0xb57b94` |

## 汇编证据序列（按线序）

```asm
; 0xb57abc  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb57acb  call sub_B02DD0 → 读 u32
; 0xb57afc  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb57b0b  call sub_B06230 → 读 u8
; 0xb57b30  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb57b61  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb57b70  call sub_B02DF0 → 读 u16
; 0xb57b85  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb57b94  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb57bb8：call （非 IO）
```
