# 机器草案：线格式 —— CS-0x76F2-lounge-heroms_exp_get

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x76F2` |
| 方向 | CS |
| 协议类 | `lounge_client` |
| 命令名 | `heroms_exp_get` |
| 代码位置 | `0xba6cc0`..`0xba6efa` |
| 声明容量 | `0xE` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xba6d4c` |
| 2 | 4 | 4 | u32 | `0xba6d67` |
| 3 | 8 | 4 | u32 | `0xba6d6f` |

## 汇编证据序列（按线序）

```asm
; 0xba6d4c  mov [eax] → 内联写 u32
; 0xba6d67  mov [eax] → 内联写 u32
; 0xba6d6f  call sub_B02D80 → 写 u32
; —— 扫描停止于 0xba6db3：call sub_B03020（非 IO）
```
