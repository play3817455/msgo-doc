# 机器草案：线格式 —— SC-0xB606-lounge-clan_mshipbid_response_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xB606` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `clan_mshipbid_response_r` |
| 代码位置 | `0xb74d94`..`0xb74f8e` |
| 声明容量 | `0x5` |
| 字段总长 | **5** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb74deb` |
| 2 | 4 | 1 | u8 | `0xb74e2b` |

## 汇编证据序列（按线序）

```asm
; 0xb74ddc  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb74deb  call sub_B02DD0 → 读 u32
; 0xb74e1c  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb74e2b  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb74e4f：call （非 IO）
```
