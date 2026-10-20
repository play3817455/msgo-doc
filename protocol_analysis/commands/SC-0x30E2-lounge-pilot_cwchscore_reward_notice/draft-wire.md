# 机器草案：线格式 —— SC-0x30E2-lounge-pilot_cwchscore_reward_notice

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x30E2` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_cwchscore_reward_notice` |
| 代码位置 | `0xb5b3d0`..`0xb5b691` |
| 声明容量 | `0x47` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb5b4d3`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 1 | u8 | `0xb5b427` |
| 2 | 1 | 1 | u8 | `0xb5b467` |
| 3 | 2 | 4 | u32 | `0xb5b48b` |
| 4 | 6 | ? | bytes | `0xb5b4a3` |

## 汇编证据序列（按线序）

```asm
; 0xb5b418  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb5b427  call sub_B06230 → 读 u8
; 0xb5b458  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb5b467  call sub_B06230 → 读 u8
; 0xb5b47c  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5b48b  call sub_B02DD0 → 读 u32
; 0xb5b4a3  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; —— 扫描停止于 0xb5b4da：call sub_B41110（非 IO）
```
