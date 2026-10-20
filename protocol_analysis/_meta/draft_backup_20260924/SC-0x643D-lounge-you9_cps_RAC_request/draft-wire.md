# 机器草案：线格式 —— SC-0x643D-lounge-you9_cps_RAC_request

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x643D` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `you9_cps_RAC_request` |
| 代码位置 | `0xb64a19`..`0xb64c4e` |
| 声明容量 | `0xC` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb64a69` |
| 2 | 4 | 4 | u32 | `0xb64aa9` |
| 3 | 8 | 4 | u32 | `0xb64acd` |

## 汇编证据序列（按线序）

```asm
; 0xb64a5a  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb64a69  call sub_B02DD0 → 读 u32
; 0xb64a9a  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb64aa9  call sub_B02DD0 → 读 u32
; 0xb64abe  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb64acd  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb64af1：call （非 IO）
```
