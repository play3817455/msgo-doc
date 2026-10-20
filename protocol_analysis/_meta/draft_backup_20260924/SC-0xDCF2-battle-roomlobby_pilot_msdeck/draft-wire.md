# 机器草案：线格式 —— SC-0xDCF2-battle-roomlobby_pilot_msdeck

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xDCF2` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `roomlobby_pilot_msdeck` |
| 代码位置 | `0xb2cbf8`..`0xb2cff8` |
| 声明容量 | `0x24` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb2cc4c` |
| 2 | 4 | 4 | u32 | `0xb2cc89` |
| 3 | 8 | 4 | u32 | `0xb2cc9f` |
| 4 | 12 | 4 | u32[] | `0xb2ccda` |
| 5 | 16 | 4 | u32 | `0xb2ccfa` |

## 汇编证据序列（按线序）

```asm
; 0xb2cc3d  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2cc4c  call sub_B02DD0 → 读 u32
; 0xb2cc7a  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb2cc89  call sub_B02DD0 → 读 u32
; 0xb2cc9f  call sub_B02DD0 → 读 u32
; 0xb2ccda  call sub_B41850 → 读 u32（数组）
; 0xb2ccfa  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb2cd12：jmp
```
