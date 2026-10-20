# BEGINNER_CHALLENGE ｜ `reward/beginner_challenge.csv`

- **用途**：新手挑战
- 表ID `77` ｜ 下载序 `60` ｜ 类名 `CBeginnerChallengeTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_570420` ｜ **列数 16**（csv0..csv15；**无 gap**，每列都被读）
- ★2026-10-05 第 4 批订正：旧 schema 行宽 **6**（且列名/列号错位），实测 reader 读到 **csv15** ⇒ 补齐为 16 列

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `challenge_id` | u32 | +0 | 新手挑战 ID（主键，`sub_BBB370(0)`） |
| 2 | `1` | `unknown_u32_1` | u32 | +4 | 前导 u32（reader 取回即存，无后续解释） |
| 3 | `2` | `unknown_u32_2` | u32 | +8 | 前导 u32；旧名 `reward_type` **错**（类型枚举其实在 csv4） |
| 4 | `3` | `unknown_u32_3` | u32 | +12 | 前导 u32 |
| 5 | `4` | `reward1_type` | enum `sub_5703A0` | +24 | 奖励 1 类型（枚举见下） |
| 6 | `5` | `reward1_param_a` | u32 | +16 | 奖励 1 参数 A |
| 7 | `6` | `reward1_param_b` | u32 | +20 | 奖励 1 参数 B |
| 8 | `7` | `reward1_param_c` | u32 | +28 | 奖励 1 参数 C |
| 9 | `8` | `reward2_type` | enum `sub_5703A0` | +40 | 奖励 2 类型 |
| 10 | `9` | `reward2_param_a` | u32 | +32 | 奖励 2 参数 A |
| 11 | `10` | `reward2_param_b` | u32 | +36 | 奖励 2 参数 B |
| 12 | `11` | `reward2_param_c` | u32 | +44 | 奖励 2 参数 C |
| 13 | `12` | `reward3_type` | enum `sub_5703A0` | +56 | 奖励 3 类型 |
| 14 | `13` | `reward3_param_a` | u32 | +48 | 奖励 3 参数 A |
| 15 | `14` | `reward3_param_b` | u32 | +52 | 奖励 3 参数 B |
| 16 | `15` | `reward3_param_c` | u32 | +60 | 奖励 3 参数 C |

## 1. 结构（`sub_570420` 反编译逐条确证）

```
行结构（64 字节）= 4 个前导 u32（+0/+4/+8/+12）
                + 3 组 × 16 字节（每组 4 个 dword）
组内 CSV 序 = { type, param_a, param_b, param_c }     ← 组基址 = csv# 4/8/12
组内内存序 = { param_a(+0), param_b(+4), type(+8), param_c(+12) }  ← ★与 CSV 序不同
```

- reader 循环 `3` 次、步长 `16`：`v6[0]=sub_BBB370(r+1)`、`v6[1]=sub_BBB370(r+2)`、
  `v6[2]=sub_5703A0(sub_BBB4F0(r))`、`v6[3]=sub_BBB370(r+3)`
  ⇒ **CSV 的组基址那一列是类型枚举，不是第一个参数**。
- 旧 schema（6 列）把 `reward_type` 记在 **csv2**、把 `reward_quantity`/`condition_param` 记在 csv4/csv5，
  与 reader 的 `4 + 4r` 组基址**整套错位**；csv6..csv15 完全没声明 ⇒ 越界兜底恒 0。

## 2. 枚举 `sub_5703A0`（奖励类型）

| CSV 字串 | 值 |
|---|---|
| `GP` | `0` |
| `ITEM` | `1` |
| `MSMA` | `998` |
| `BUILDUP_MSMA` | `-1` |
| 其它（含空） | `999` |

> 旧 schema 曾记 `GP=0/ITEM=1/MSMA=2/BUILDUP_MSMA=3` —— **错**，本批按 `sub_5703A0` 订正。
> 写 CSV 时该列写**名称字符串**（`GP`/`ITEM`/`MSMA`/`BUILDUP_MSMA`）。

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 本表 **16 段**（`csv0..csv15`），**不要截断**：reader 会读满 16 列。
