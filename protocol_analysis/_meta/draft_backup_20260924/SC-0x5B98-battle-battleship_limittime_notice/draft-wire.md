# 机器草案：线格式 —— SC-0x5B98-battle-battleship_limittime_notice

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x5B98` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `battleship_limittime_notice` |
| 代码位置 | `0xb18b90`..`0xb18d79` |
| 声明容量 | `0x6` |
| 字段总长 | **6** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb18be7` |
| 2 | 2 | 4 | u32 | `0xb18c27` |

## 汇编证据序列（按线序）

```asm
; 0xb18bd8  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb18be7  call sub_B02DF0 → 读 u16
; 0xb18c18  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb18c27  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb18c4b：call （非 IO）
```
