# MSMA_MISSIONUNIT ｜ `msma/msma_missionunit.csv`

- **用途**：任务出击单位
- 表ID `56` ｜ 下载序 `64` ｜ 类名 `CMsmaMissionUnitTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_57E3F0` ｜ **列数 7**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `unit_id` | u32 | +0 | 任务单位ID（主键） |
| 2 | `1` | `msma_id` | u32 | +4 | 关联机体 ID（u32 col1 → +4；→ CHARA_PARAM） |
| 3 | `3` | `unit_role` | enum `sub_57E1D0` | +8 | 单位职能（sub_57E1D0）：ATTACK/DEFENSE/MOVE/SPECIAL |
| 4 | `4` | `spawn_order` | u32 | +12 | 出击顺序（+12）；读表时更新全局最小值 this[4] |
| 5 | `5` | `mission_param_a` | u32 | +16 | 任务参数 u32（+16） |
| 6 | `6` | `mission_param_b` | u32 | +20 | 任务参数 u32（+20） |
| 7 | `8` | `mission_param_c` | u32 | +24 | 任务参数 u32（+24） |

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `2`：CSV 列存在但 IDA 读表未单独取证（默认 0）
- CSV `7`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
