# 机器草案：线格式 —— CS-0x7938-battle-roomlobby_pick_vote_cancel

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x7938` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `roomlobby_pick_vote_cancel` |
| 代码位置 | `0xb32b40`..`0xb32ce7` |
| 声明容量 | `0x6` |
| 字段总长 | **4** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb32bc1` |

## 汇编证据序列（按线序）

```asm
; 0xb32bc1  mov [eax] → 内联写 u32
; —— 扫描停止于 0xb32bf3：call sub_B03020（非 IO）
```
