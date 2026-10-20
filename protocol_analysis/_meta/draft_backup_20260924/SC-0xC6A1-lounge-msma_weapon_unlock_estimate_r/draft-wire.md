# 机器草案：线格式 —— SC-0xC6A1-lounge-msma_weapon_unlock_estimate_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xC6A1` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `msma_weapon_unlock_estimate_r` |
| 代码位置 | `0xb78ed5`..`0xb790fb` |
| 声明容量 | `0x8` |
| 字段总长 | **8** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb78f2c` |
| 2 | 4 | 4 | u32 | `0xb78f6c` |

## 汇编证据序列（按线序）

```asm
; 0xb78f1d  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb78f2c  call sub_B02DD0 → 读 u32
; 0xb78f5d  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb78f6c  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb78f90：call （非 IO）
```
