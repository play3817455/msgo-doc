# 机器草案：线格式 —— SC-0x1CF4-lounge-pilot_unreached_notify

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x1CF4` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_unreached_notify` |
| 代码位置 | `0xb577df`..`0xb57a74` |
| 声明容量 | `0x10` |
| 字段总长 | **16** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb57836` |
| 2 | 4 | 4 | u32 | `0xb57876` |
| 3 | 8 | 4 | u32 | `0xb5789a` |
| 4 | 12 | 4 | u32 | `0xb578be` |

## 汇编证据序列（按线序）

```asm
; 0xb57827  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb57836  call sub_B02DD0 → 读 u32
; 0xb57867  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb57876  call sub_B02DD0 → 读 u32
; 0xb5788b  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5789a  call sub_B02DD0 → 读 u32
; 0xb578af  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb578be  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb578e6：call （非 IO）
```
