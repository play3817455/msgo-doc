# 机器草案：线格式 —— CS-0x07C9-battle-entity_deploy_arms_attach

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x07C9` |
| 方向 | CS |
| 协议类 | `battle_client` |
| 命令名 | `entity_deploy_arms_attach` |
| 代码位置 | `0xb34670`..`0xb3492b` |
| 声明容量 | `0x16` |
| 字段总长 | **12** 字节 |
| **自校验** | **PASS(容量≥线长)**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb346fc` |
| 2 | 4 | 2 | u16 | `0xb34716` |
| 3 | 6 | 2 | u16 | `0xb3471f` |
| 4 | 8 | 2 | u16 | `0xb34739` |
| 5 | 10 | 2 | u16 | `0xb34753` |

## 汇编证据序列（按线序）

```asm
; 0xb346fc  mov [ecx] → 内联写 u32
; 0xb34716  mov [edx] → 内联写 u16
; 0xb3471f  call sub_B02DA0 → 写 u16
; 0xb34739  call sub_B02DA0 → 写 u16
; 0xb34753  call sub_B02DA0 → 写 u16
; —— 扫描停止于 0xb34797：call sub_B03020（非 IO）
```
