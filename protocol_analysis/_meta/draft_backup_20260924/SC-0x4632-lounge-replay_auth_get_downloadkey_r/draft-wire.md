# 机器草案：线格式 —— SC-0x4632-lounge-replay_auth_get_downloadkey_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x4632` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `replay_auth_get_downloadkey_r` |
| 代码位置 | `0xb5e4e9`..`0xb5e72e` |
| 声明容量 | `0x6E` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb5e540` |
| 2 | 4 | ? | bytes | `0xb5e581` |
| 3 | ? | ? | bytes | `0xb5e595` |

## 汇编证据序列（按线序）

```asm
; 0xb5e531  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb5e540  call sub_B02DD0 → 读 u32
; 0xb5e581  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb5e595  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; —— 扫描停止于 0xb5e5b9：call （非 IO）
```
