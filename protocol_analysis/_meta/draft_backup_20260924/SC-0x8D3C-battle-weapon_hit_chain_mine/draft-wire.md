# 机器草案：线格式 —— SC-0x8D3C-battle-weapon_hit_chain_mine

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x8D3C` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_hit_chain_mine` |
| 代码位置 | `0xb22c4d`..`0xb22f9e` |
| 声明容量 | `0xE` |
| 字段总长 | **14** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb22ca4` |
| 2 | 4 | 2 | u16 | `0xb22ce4` |
| 3 | 6 | 2 | u16 | `0xb22d08` |
| 4 | 8 | 2 | u16 | `0xb22d2c` |
| 5 | 10 | 2 | u16 | `0xb22d54` |
| 6 | 12 | 2 | u16 | `0xb22d7c` |

## 汇编证据序列（按线序）

```asm
; 0xb22c95  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb22ca4  call sub_B02DD0 → 读 u32
; 0xb22cd5  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb22ce4  call sub_B02DF0 → 读 u16
; 0xb22cf9  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb22d08  call sub_B02DF0 → 读 u16
; 0xb22d1d  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb22d2c  call sub_B02DF0 → 读 u16
; 0xb22d45  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb22d54  call sub_B02DF0 → 读 u16
; 0xb22d6d  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb22d7c  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb22da4：call （非 IO）
```
