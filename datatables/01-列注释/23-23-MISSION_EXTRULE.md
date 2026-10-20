# MISSION_EXTRULE ｜ `mission/mission_ext_rule.csv`

- **用途**：任务附加规则
- 表ID `23` ｜ 下载序 `23` ｜ 类名 `CMissionExtRuleTable`
- 逐列读取函数 `sub_59E170` ｜ **列数 6**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `rule_id` | u32 | — | 主键；附加规则 ID |
| 2 | `1` | `rule_label` | str | — | 规则说明文本（col1 预留；读表未写入内存，默认空） |
| 3 | `2` | `rule_type` | enum `sub_59E070` | +4 | 规则类型：LIMIT_MS_SET/NEWBIE_LIMIT_MS/NEWBIE_VS_XWAR/BAN_PICK |
| 4 | `3` | `param_a` | enum `sub_59E0F0` | +8 | 限制项 A：MS_COST/BTLTYPE_ENABLE/BTLTYPE_DISABLE/MS_TROOPS |
| 5 | `4` | `param_b` | enum `sub_59E0F0` | — | 限制项 B（与 param_a 同枚举域 sub_59E0F0） |
| 6 | `5` | `param_value` | u32 | +12 | 限制数值（u32 @+12；如机体 cost 上限/禁机体 ID） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。
