# 机器草案：线格式 —— SC-0xA9E7-battle-weapon_fire__damage_field_r

> 本文件由 `tools/ida_draft_wire.py` 生成，**不要手工编辑**。
> 类型/偏移/长度/证据均来自汇编；**含义/用途一律待人工补齐**（规范 §7）。
> 定稿请写 `README.md` 的帧格式表 + `fields.csv`，并把状态改为 `WIP`/`DONE`。

## 命令

| 项 | 值 |
|---|---|
| opcode | `0xA9E7` |
| 方向 | SC |
| 协议类 | `battle_client` |
| 命令名 | `weapon_fire__damage_field_r` |
| 代码位置 | `0xb277a4`..`0xb27f53` |
| 声明容量 | `0x27` |
| 字段总长 | **39** 字节 |
| **自校验** | **PASS**（全定长时：S→C「容量 == 负载长」；C→S「容量 ≥ 负载长 + 2」）

## 草案字段表（机器提取）

| # | 偏移 | 长度 | 线类型 | 证据VA |
|---|---|---|---|---|
| 1 | 0 | 2 | u16 | `0xb27801` |
| 2 | 2 | 4 | u32 | `0xb27841` |
| 3 | 6 | 4 | u32 | `0xb27865` |
| 4 | 10 | 4 | u32 | `0xb27889` |
| 5 | 14 | 2 | u16 | `0xb278b1` |
| 6 | 16 | 2 | u16 | `0xb278d9` |
| 7 | 18 | 2 | u16 | `0xb27901` |
| 8 | 20 | 2 | u16 | `0xb27929` |
| 9 | 22 | 2 | u16 | `0xb27951` |
| 10 | 24 | 2 | u16 | `0xb27979` |
| 11 | 26 | 2 | u16 | `0xb279a1` |
| 12 | 28 | 2 | u16 | `0xb279c9` |
| 13 | 30 | 2 | u16 | `0xb279f1` |
| 14 | 32 | 2 | u16 | `0xb27a19` |
| 15 | 34 | 2 | u16 | `0xb27a41` |
| 16 | 36 | 1 | u8 | `0xb27a69` |
| 17 | 37 | 1 | u8 | `0xb27a91` |
| 18 | 38 | 1 | u8 | `0xb27ab9` |

## 汇编证据序列（按线序）

```asm
; 0xb277ef  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb27801  call sub_B02DF0 → 读 u16
; 0xb27832  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb27841  call sub_B02DD0 → 读 u32
; 0xb27856  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb27865  call sub_B02DD0 → 读 u32
; 0xb2787a  call sub_B41470 → 解码缓冲预留 u32（非字段）
; 0xb27889  call sub_B02DD0 → 读 u32
; 0xb278a2  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb278b1  call sub_B02DF0 → 读 u16
; 0xb278ca  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb278d9  call sub_B02DF0 → 读 u16
; 0xb278f2  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb27901  call sub_B02DF0 → 读 u16
; 0xb2791a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb27929  call sub_B02DF0 → 读 u16
; 0xb27942  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb27951  call sub_B02DF0 → 读 u16
; 0xb2796a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb27979  call sub_B02DF0 → 读 u16
; 0xb27992  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb279a1  call sub_B02DF0 → 读 u16
; 0xb279ba  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb279c9  call sub_B02DF0 → 读 u16
; 0xb279e2  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb279f1  call sub_B02DF0 → 读 u16
; 0xb27a0a  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb27a19  call sub_B02DF0 → 读 u16
; 0xb27a32  call sub_B413B0 → 解码缓冲预留 u16（非字段）
; 0xb27a41  call sub_B02DF0 → 读 u16
; 0xb27a5a  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb27a69  call sub_B06230 → 读 u8
; 0xb27a82  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb27a91  call sub_B06230 → 读 u8
; 0xb27aaa  call sub_B05E30 → 解码缓冲预留 u8（非字段）
; 0xb27ab9  call sub_B06230 → 读 u8
; —— 扫描停止于 0xb27ae1：call （非 IO）
```
