# 机器草案：线格式 —— SC-0xA39E-battle-msma_AI_change_movetype

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xA39E` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `msma_AI_change_movetype` |
| 代码位置 | `0xb2563d`..`0xb25899` |
| 声明容量 | `0x5` |
| 字段总长 | **5** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb25694` |
| 2 | 2 | 1 | u8 | `0xb256d4` |
| 3 | 3 | 2 | u16 | `0xb256f8` |

## 汇编证据序列（按线序）

```asm
; 0xb25685  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb25694  call sub_B02DF0 → 读 u16
; 0xb256c5  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb256d4  call sub_B06230 → 读 u8
; 0xb256e9  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb256f8  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb2571c：call （非 IO）
```
