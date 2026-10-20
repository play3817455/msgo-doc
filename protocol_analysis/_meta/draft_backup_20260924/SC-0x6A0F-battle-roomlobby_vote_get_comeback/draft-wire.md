# 机器草案：线格式 —— SC-0x6A0F-battle-roomlobby_vote_get_comeback

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x6A0F` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `roomlobby_vote_get_comeback` |
| 代码位置 | `0xb1ce6d`..`0xb1d0a1` |
| 声明容量 | `0x14` |
| 字段总长 | **4** 字节 |
| **自校验** | **PASS(容量更宽/未证伪)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb1cec1` |

## 汇编证据序列（按线序）

```asm
; 0xb1ceb2  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb1cec1  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb1ceef：call sub_B41990（非 IO）
```
