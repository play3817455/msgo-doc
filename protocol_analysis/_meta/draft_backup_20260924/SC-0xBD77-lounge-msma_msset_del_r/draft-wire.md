# 机器草案：线格式 —— SC-0xBD77-lounge-msma_msset_del_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xBD77` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_msset_del_r` |
| 代码位置 | `0xb76da3`..`0xb76fdc` |
| 声明容量 | `0x8` |
| 字段总长 | **8** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb76df3` |
| 2 | 4 | 2 | u16 | `0xb76e33` |
| 3 | 6 | 2 | u16 | `0xb76e57` |

## 汇编证据序列（按线序）

```asm
; 0xb76de4  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb76df3  call sub_B02DD0 → 读 u32
; 0xb76e24  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb76e33  call sub_B02DF0 → 读 u16
; 0xb76e48  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb76e57  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb76e7b：call （非 IO）
```
