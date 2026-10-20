# LVUP_FAVMS ｜ `growth/lvup_ms_favorite.csv`

- **用途**：喜爱机体升级
- 表ID `16` ｜ 下载序 `16` ｜ 类名 `CLvupFavmsTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_579BF0` ｜ **列数 9**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `fav_level` | u8 | +0 | 爱机等级（u8 主键） |
| 2 | `1` | `exp_required` | u32 | +4 | 升级所需经验（u32 col1） |
| 3 | `3` | `bonus_param_a` | u32 | +8 | 爱机加成参数 A（u32 col3） |
| 4 | `4` | `bonus_param_b` | u32 | +12 | 爱机加成参数 B（u32 col4） |
| 5 | `6` | `param_u32_6` | u32 | +16 | 整型参数 col6（+16） |
| 6 | `7` | `param_u32_7` | u32 | +20 | 整型参数 col7（+20） |
| 7 | `9` | `param_u32_9` | u32 | +24 | 整型参数 col9（+24） |
| 8 | `10` | `param_u32_10` | u32 | +28 | 整型参数 col10（+28） |
| 9 | `11` | `param_u32_11` | u32 | +32 | 整型参数 col11（+32） |

## ★本表填写现状（2026-10-05 体检）：**纯键占位**

`_probe_batch_n2.py` / `_probe_batch_n2_formula.py`：64 行（`fav_level` 1..64 连续），
**只有 col0 有值**，其余 **11 列全空**（含 reader 明确会读的 `col1 exp_required` → `+4`）。

⇒ 与 §9.1 的 `CHARA_MODEL` / `MSMA_BREAKUP` 同类：**只有主键，没有任何内容**。
客户端 `sub_579BF0` 会把空列读成 0 ⇒ 爱机升级链上 `exp_required = 0`（**升级所需经验为 0**）。
填实需要真实经验曲线来源，**不能猜**。

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `2`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `5`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `8`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
