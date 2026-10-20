# 机器草案：线格式 —— SC-0x8D58-battle-eqparts_ready_start_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x8D58` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `eqparts_ready_start_r` |
| 代码位置 | `0xb22f9e`..`0xb23291` |
| 声明容量 | `0xD` |
| 字段总长 | **13** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb22ff5` |
| 2 | 4 | 4 | u32 | `0xb23035` |
| 3 | 8 | 2 | u16 | `0xb23059` |
| 4 | 10 | 2 | u16 | `0xb2307d` |
| 5 | 12 | 1 | u8 | `0xb230a5` |

## 汇编证据序列（按线序）

```asm
; 0xb22fe6  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb22ff5  call sub_B02DD0 → 读 u32
; 0xb23026  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb23035  call sub_B02DD0 → 读 u32
; 0xb2304a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb23059  call sub_B02DF0 → 读 u16
; 0xb2306e  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb2307d  call sub_B02DF0 → 读 u16
; 0xb23096  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb230a5  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb230cd：call （非 IO）
```
