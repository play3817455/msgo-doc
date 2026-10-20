# 机器草案：线格式 —— SC-0xD286-lounge-season_rankerbattle_entry_info

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xD286` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `season_rankerbattle_entry_info` |
| 代码位置 | `0xb7c148`..`0xb7c328` |
| 声明容量 | `0x8` |
| 字段总长 | **8** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb7c198` |
| 2 | 4 | 4 | u32 | `0xb7c1d8` |

## 汇编证据序列（按线序）

```asm
; 0xb7c189  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7c198  call sub_B02DD0 → 读 u32
; 0xb7c1c9  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7c1d8  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb7c1fc：call （非 IO）
```
