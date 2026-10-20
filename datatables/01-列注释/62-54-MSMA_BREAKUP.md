# MSMA_BREAKUP ｜ `msma/msma_breakup.csv`

- **用途**：机体拆解
- 表ID `54` ｜ 下载序 `62` ｜ 类名 `CMsmaBreakupTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_57BF00` ｜ **列数 6**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `breakup_id` | u32 | +0 | 拆解配置ID（主键；通常=机体ID） |
| 2 | `1` | `faction` | enum `sub_40CE20` | +4 | 阵营（enum col1 sub_40CE20：EFF=0 / ZEON=1 / 其它=-1 → +4） |
| 3 | `2` | `battle_detail_ref` | enum `sub_5812E0` | +8 | 战斗明细引用（enum col2 sub_5812E0 查 MSMA_BATTLE_DETAIL 属性名 → +8） |
| 4 | `3` | `breakup_type` | enum `sub_57BDE0` | +12 | 拆解产物等级（enum col3 sub_57BDE0：SILVER=0/GOLD=1/PLATINUM=2 → +12） |
| 5 | `4` | `breakup_param_a` | u32 | +16 | 拆解参数 A（u32 col4 → +16） |
| 6 | `6` | `breakup_param_b` | u32 | +20 | 拆解参数 B（u32 col6 → +20；跳过 col5 空列） |

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `5`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。

## 体检 ｜ 行数三方对账（2026-10-05 n1 批）

| 面 | 行数 |
|---|---|
| 种子 `msma/msma_breakup.csv` | **64** |
| 库 `cfg."MSMA_BREAKUP"` | **64** |
| `meta.cfg_manifest.row_count` | **64** |

三者一致（`_probe_reconcile.py`；本表有 **3 行** `#` 头注释 —— 本表极小，若不剥注释行会数成 66，
是本批里"假差"最容易被误判的一张）。

⚠️ 现状是**占位**：键 = `1..64` 连续整数、其余 5 列全空（`= 0`），并非真实机体 ID 集，
与 `#4 CHARA_PARAM`(698 練度ID) / `#35 MSMA_RENTAL` **不同键域**（所以本批体检里它是"外来键"）。
含义见本文件上方「主键；通常 = 机体ID」——**该语义仍待取证**（当前 1..64 是骨架，非真值）。
