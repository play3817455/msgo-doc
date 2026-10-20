# BGMPACKAGE ｜ `本地表，不下发`

- **用途**：BGM 包（**本地表**）
- 表ID `39` ｜ 下载序 `39` ｜ 类名 `CBGMTable` ｜ disposition `LOCAL`
- 逐列读取函数 `sub_570560` ｜ **列数 7**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `package_id` | u32 | — | BGM 包 ID（主键；本地表，近亲 settings/bgm.csv BGMパックID） |
| 2 | `1` | `field_bgm_id` | u32 | +4 | 战场 BGM ID（col1 → 本地 bgm.csv BGM-ID） |
| 3 | `2` | `ace_bgm_id` | u32 | +8 | Ace 击破 BGM ID（col2） |
| 4 | `3` | `bgm_asset_path` | str | — | BGM 资源路径/备注（wstring col3） |
| 5 | `4` | `force_bgm_enabled` | bool | — | 强制 BGM 开关（bool col4>0） |
| 6 | `5` | `ace_bgm_enabled` | bool | — | Ace BGM 开关（bool col5>0） |
| 7 | `6` | `field_bgm_enabled` | bool | — | 战场 BGM 开关（bool col6>0） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。
