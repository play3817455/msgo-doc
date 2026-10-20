# 机器草案：线格式 —— SC-0xE69C-lounge-clan_mshipbid_request_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xE69C` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `clan_mshipbid_request_r` |
| 代码位置 | `0xb83f19`..`0xb841e3` |
| 声明容量 | `0x28` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb83f70` |
| 2 | 4 | 4 | u32 | `0xb83fb0` |
| 3 | 8 | ? | bytes | `0xb83fd5` |
| 4 | ? | 1 | u8 | `0xb84015` |

## 汇编证据序列（按线序）

```asm
; 0xb83f61  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb83f70  call sub_B02DD0 → 读 u32
; 0xb83fa1  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb83fb0  call sub_B02DD0 → 读 u32
; 0xb83fd5  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb84006  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb84015  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb84039：call （非 IO）
```
