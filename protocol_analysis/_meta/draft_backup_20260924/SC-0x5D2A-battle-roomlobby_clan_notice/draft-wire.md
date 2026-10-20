# 机器草案：线格式 —— SC-0x5D2A-battle-roomlobby_clan_notice

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x5D2A` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `roomlobby_clan_notice` |
| 代码位置 | `0xb18d79`..`0xb19147` |
| 声明容量 | `0x28` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 1 | u8 | `0xb18dcd` |
| 2 | 1 | 1 | u8 | `0xb18e0a` |
| 3 | 2 | 4 | u32 | `0xb18e2e` |
| 4 | 6 | ? | bytes | `0xb18e53` |
| 5 | ? | 1 | u8 | `0xb18e90` |
| 6 | ? | 1 | u8 | `0xb18eb4` |
| 7 | ? | 1 | u8 | `0xb18ed8` |

## 汇编证据序列（按线序）

```asm
; 0xb18dbe  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb18dcd  call sub_B06230 → 读 u8
; 0xb18dfb  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb18e0a  call sub_B06230 → 读 u8
; 0xb18e1f  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb18e2e  call sub_B02DD0 → 读 u32
; 0xb18e53  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; 0xb18e81  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb18e90  call sub_B06230 → 读 u8
; 0xb18ea5  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb18eb4  call sub_B06230 → 读 u8
; 0xb18ec9  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb18ed8  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb18efd：call （非 IO）
```
