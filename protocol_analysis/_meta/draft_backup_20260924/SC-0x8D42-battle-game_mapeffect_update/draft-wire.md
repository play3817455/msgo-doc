# 机器草案：线格式 —— SC-0x8D42-battle-game_mapeffect_update

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x8D42` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `game_mapeffect_update` |
| 代码位置 | `0xb2283c`..`0xb22a18` |
| 声明容量 | `0x5` |
| 字段总长 | **5** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb22890` |
| 2 | 4 | 1 | u8 | `0xb228cd` |

## 汇编证据序列（按线序）

```asm
; 0xb22881  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb22890  call sub_B02DD0 → 读 u32
; 0xb228be  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb228cd  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb228ee：call （非 IO）
```
