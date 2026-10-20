# 机器草案：线格式 —— CS-0x2C1A-auth-authenticate_you9channeling

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x2C1A` |
| 方向 | CS |
| 协议类 | `auth_client` |
| 命令名 | `authenticate_you9channeling` |
| 代码位置 | `0xb055d0`..`0xb058aa` |
| 声明容量 | `0x146` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | ? | bytes | `0xb05660` |
| 2 | ? | ? | bytes | `0xb0567c` |
| 3 | ? | ? | bytes | `0xb0569b` |
| 4 | ? | ? | bytes | `0xb056ba` |

## 汇编证据序列（按线序）

```asm
; 0xb05660  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xb0567c  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xb0569b  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; 0xb056ba  call sub_B02B40 → 变长串（≤? 字节 + 1 字节 NUL）
; —— 扫描停止于 0xb056fe：call sub_B03020（非 IO）
```
