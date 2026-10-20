# 机器草案：线格式 —— SC-0xFB85-lounge-channel_list_select_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xFB85` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `channel_list_select_r` |
| 代码位置 | `0xb87e8f`..`0xb88255` |
| 声明容量 | `0xBE` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb87ee6` |
| 2 | 4 | 4 | u32 | `0xb87f23` |
| 3 | 8 | ? | bytes | `0xb87f4d` |
| 4 | ? | 4 | u32 | `0xb87f8a` |
| 5 | ? | 4 | u32 | `0xb87fae` |
| 6 | ? | 4 | u32 | `0xb87fd2` |
| 7 | ? | ? | bytes | `0xb87fee` |

## 汇编证据序列（按线序）

```asm
; 0xb87ed7  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb87ee6  call sub_B02DD0 → 读 u32
; 0xb87f14  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb87f23  call sub_B02DD0 → 读 u32
; 0xb87f4d  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb87f7b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb87f8a  call sub_B02DD0 → 读 u32
; 0xb87f9f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb87fae  call sub_B02DD0 → 读 u32
; 0xb87fc3  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb87fd2  call sub_B02DD0 → 读 u32
; 0xb87fee  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; —— 扫描停止于 0xb88013：call （非 IO）
```
