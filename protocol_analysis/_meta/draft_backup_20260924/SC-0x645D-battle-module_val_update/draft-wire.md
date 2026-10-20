# 机器草案：线格式 —— SC-0x645D-battle-module_val_update

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x645D` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `module_val_update` |
| 代码位置 | `0xb1c792`..`0xb1c9d4` |
| 声明容量 | `0x6` |
| 字段总长 | **6** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb1c7e9` |
| 2 | 2 | 2 | u16 | `0xb1c829` |
| 3 | 4 | 2 | u16 | `0xb1c84d` |

## 汇编证据序列（按线序）

```asm
; 0xb1c7da  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1c7e9  call sub_B02DF0 → 读 u16
; 0xb1c81a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1c829  call sub_B02DF0 → 读 u16
; 0xb1c83e  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb1c84d  call sub_B02DF0 → 读 u16
; —— 扫描停止于 0xb1c871：call （非 IO）
```
