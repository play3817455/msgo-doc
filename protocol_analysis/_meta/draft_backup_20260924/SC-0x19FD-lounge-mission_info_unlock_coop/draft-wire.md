# 机器草案：线格式 —— SC-0x19FD-lounge-mission_info_unlock_coop

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x19FD` |
| 方向 | SC |
| 协议类 | `lounge_client` |
| 命令名 | `mission_info_unlock_coop` |
| 代码位置 | `0xb56b50`..`0xb56ccc` |
| 声明容量 | `0x4` |
| 字段总长 | **4** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `0xb56ba4` |

## 汇编证据序列（按线序）

```asm
; 0xb56b95  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb56ba4  call sub_B02DD0 → 读 u32
; —— 扫描停止于 0xb56bd5：call sub_B41110（非 IO）
```
