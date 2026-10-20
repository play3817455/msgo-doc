# 机器草案：线格式 —— SC-0x8D1F-battle-commander_support_spot_lock

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x8D1F` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `commander_support_spot_lock` |
| 代码位置 | `0xb2368e`..`0xb23877` |
| 声明容量 | `0x2` |
| 字段总长 | **2** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 1 | u8 | `0xb236e5` |
| 2 | 1 | 1 | u8 | `0xb23725` |

## 汇编证据序列（按线序）

```asm
; 0xb236d6  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb236e5  call sub_B06230 → 读 u8
; 0xb23716  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb23725  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb23749：call （非 IO）
```
