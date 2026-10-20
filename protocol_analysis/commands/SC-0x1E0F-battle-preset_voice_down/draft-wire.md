# 机器草案：线格式 —— SC-0x1E0F-battle-preset_voice_down

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0x1E0F` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `preset_voice_down` |
| 代码位置 | `0xb11f02`..`0xb1229e` |
| 声明容量 | `0xBF` |
| 字段总长 | 含变长/数组字段，无法直接求和 |
| **自校验** | **N/A**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

| **分支** | ⚠ 扫描跨过 1 处条件跳转（`0xb1207a`）——线性扫描会把另一条臂的字段也串进来，**本草案的尾部字段不可信**，以定稿为准 |

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb11f59` |
| 2 | 2 | 4 | u32 | `0xb11f96` |
| 3 | 6 | 1 | u8 | `0xb11fba` |
| 4 | 7 | 1 | u8 | `0xb11fde` |
| 5 | 8 | 1 | u8 | `0xb12006` |
| 6 | 9 | 1 | u8 | `0xb1202e` |
| 7 | 10 | ? | bytes | `0xb1204d` |

## 汇编证据序列（按线序）

```asm
; 0xb11f4a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb11f59  call sub_B02DF0 → 读 u16
; 0xb11f87  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb11f96  call sub_B02DD0 → 读 u32
; 0xb11fab  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb11fba  call sub_B06230 → 读 u8
; 0xb11fcf  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb11fde  call sub_B06230 → 读 u8
; 0xb11ff7  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb12006  call sub_B06230 → 读 u8
; 0xb1201f  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb1202e  call sub_B06230 → 读 u8
; 0xb1204d  call sub_B02BA0 → 变长串/字节块（NUL 结尾）
; —— 扫描停止于 0xb1207e：call sub_B05D90（非 IO）
```
