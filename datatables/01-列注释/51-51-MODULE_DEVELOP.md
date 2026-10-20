# MODULE_DEVELOP ｜ `module/module_develop.csv`

- **用途**：模块开发
- 表ID `51` ｜ 下载序 `51` ｜ 类名 `CModuleDevelopTable`
- 逐列读取函数 `sub_5A2B90` ｜ **列数 5**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `develop_id` | u32 | +0 | 主键；模块开发配方 ID |
| 2 | `2` | `module_id` | u32 | +28 | 目标 MODULE.module_id（u32 @+28） |
| 3 | `3` | `develop_time_sec` | u32 | +32 | 开发耗时秒（u32 @+32） |
| 4 | `4` | `material_item_id` | u32 | +4 | 材料 ITEM ID（u32 @+4；配对循环第1组） |
| 5 | `6` | `material_qty` | u32 | +8 | 材料数量（u32 @+8） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。
