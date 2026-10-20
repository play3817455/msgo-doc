# BANNER_INFO ｜ `banner/banner_setting.csv`

- **用途**：横幅（公告图）信息
- 表ID `59` ｜ 下载序 `67` ｜ 类名 `CBannerInfoTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_56FF30` ｜ **列数 8**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `banner_id` | u32 | — | 公告横幅 ID（主键；资源 interface/） |
| 2 | `1` | `display_scene` | str | +4 | 显示场景标签（wstring col1；sub_BBB130→+4，无固定枚举表） |
| 3 | `2` | `banner_type` | str | +32 | 横幅类型标签（wstring col2 → +32） |
| 4 | `3` | `priority` | str | +60 | 显示优先级标签（wstring col3 → +60） |
| 5 | `4` | `link_type` | str | +88 | 链接类型标签（wstring col4 → +88） |
| 6 | `5` | `image_path` | str | — | 横幅图片路径（str col5 sub_BBB4F0；→ interface/ 资源） |
| 7 | `6` | `display_period` | str | +128 | 显示时段（str col6/7；sub_56FDA0 解析 /// ::: 日期时间格式 → +116/+128） |
| 8 | `7` | `link_url_id` | u32 | — | 跳转链接 ID（u32 col7） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
