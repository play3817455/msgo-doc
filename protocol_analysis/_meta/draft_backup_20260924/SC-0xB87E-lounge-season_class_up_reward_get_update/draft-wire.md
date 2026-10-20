# 机器草案：线格式 —— SC-0xB87E-lounge-season_class_up_reward_get_update

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xB87E` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `season_class_up_reward_get_update` |
| 代码位置 | `0xb75627`..`0xb758c9` |
| 声明容量 | `0x2E` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb7567e` |
| 2 | 4 | 4 | u32 | `0xb756b0` |
| 3 | 8 | 2 | u16[] | `0xb756eb` |
| 4 | 10 | 2 | u16 | `0xb7570a` |

## 汇编证据序列（按线序）

```asm
; 0xb7566f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb7567e  call sub_B02DD0 → 读 u32
; 0xb756b0  call sub_B02DD0 → 读 u32
; 0xb756eb  call sub_B05E40 → 读 u16（数组）
; 0xb7570a  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb75722：jmp
```
