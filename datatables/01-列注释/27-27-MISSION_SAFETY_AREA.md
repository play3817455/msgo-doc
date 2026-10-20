# MISSION_SAFETY_AREA ｜ `mission/mission_safety_area.csv`

- **用途**：任务安全区（可战区域限制）
- 表ID `27` ｜ 下载序 `27` ｜ 类名 `CMissionSafetyAreaTable`
- 逐列读取函数 `sub_59EF40` ｜ **列数 7**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `1` | `min_x` | float | +0 | 安全区 AABB min_x（float @+0；sub_BBB470） |
| 2 | `2` | `min_y` | float | +4 | 安全区 AABB min_y（float @+4；sub_BBB470） |
| 3 | `3` | `min_z` | float | +8 | 安全区 AABB min_z（float @+8；sub_BBB470） |
| 4 | `4` | `max_x` | float | +12 | 安全区 AABB max_x（float @+12；sub_BBB470） |
| 5 | `5` | `max_y` | float | +16 | 安全区 AABB max_y（float @+16；sub_BBB470） |
| 6 | `6` | `max_z` | float | +20 | 安全区 AABB max_z（float @+20；sub_BBB470） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 越界列 = 0；每个数据行至少 1 个单元格。
