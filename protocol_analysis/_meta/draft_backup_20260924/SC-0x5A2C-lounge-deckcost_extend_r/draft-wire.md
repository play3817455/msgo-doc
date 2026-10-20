# 机器草案：线格式 —— SC-0x5A2C-lounge-deckcost_extend_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x5A2C` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `deckcost_extend_r` |
| 代码位置 | `0xb62eb5`..`0xb630ee` |
| 声明容量 | `0x8` |
| 字段总长 | **8** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb62f05` |
| 2 | 4 | 2 | u16 | `0xb62f45` |
| 3 | 6 | 2 | u16 | `0xb62f69` |

## 汇编证据序列（按线序）

```asm
; 0xb62ef6  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb62f05  call sub_B02DD0 → 读 u32
; 0xb62f36  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb62f45  call sub_B02DF0 → 读 u16
; 0xb62f5a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb62f69  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb62f8d：call （非 IO）
```
