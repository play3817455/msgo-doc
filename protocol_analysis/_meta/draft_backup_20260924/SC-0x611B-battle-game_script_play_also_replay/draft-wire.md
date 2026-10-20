# 机器草案：线格式 —— SC-0x611B-battle-game_script_play_also_replay

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x611B` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `game_script_play_also_replay` |
| 代码位置 | `0xb1c246`..`0xb1c429` |
| 声明容量 | `0x42` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | ? | bytes | `0xb1c295` |
| 2 | ? | 1 | u8 | `0xb1c2d2` |

## 汇编证据序列（按线序）

```asm
; 0xb1c295  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb1c2c3  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1c2d2  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb1c2f3：call （非 IO）
```
