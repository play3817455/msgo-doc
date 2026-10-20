# 机器草案：线格式 —— SC-0x80DC-lounge-second_chance_free_play_update

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x80DC` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `second_chance_free_play_update` |
| 代码位置 | `0xb6935d`..`0xb69522` |
| 声明容量 | `0x1` |
| 字段总长 | **1** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 1 | u8 | `0xb693b4` |

## 汇编证据序列（按线序）

```asm
; 0xb693a5  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb693b4  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb693eb：call sub_B41110（非 IO）
```
