# MODULE_RENTAL ｜ `module/module_rental.csv`

- **用途**：模块租借
- 表ID `71` ｜ 下载序 `54` ｜ 类名 `CModuleRentalTable`
- 逐列读取函数 `sub_5A2C00` ｜ **列数 5**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `rental_id` | u32 | +0 | 主键；模块租借 ID |
| 2 | `4` | `module_id` | u32 | +4 | MODULE.module_id（u32 @+4） |
| 3 | `5` | `rental_cost_gp` | u32 | +8 | 租借 GP 费用（u32 @+8） |
| 4 | `6` | `duration_sec` | u32 | +12 | 租借时长秒（u32 @+12） |
| 5 | `7` | `max_rental_count` | u32 | +16 | 最大租借次数（u32 @+16） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。
