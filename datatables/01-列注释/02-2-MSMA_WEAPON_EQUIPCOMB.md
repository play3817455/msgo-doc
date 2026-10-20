# MSMA_WEAPON_EQUIPCOMB ｜ `msma/msma_weapon_equipcomb.csv`

- **用途**：武器装备组合规则**——某个组合ID下"哪些武器类别可以/必须搭配"。
- 表ID `2` ｜ 下载序 `2` ｜ 类名 `CMSMAWeaponEquipCombTable` ｜ 逐列读取 `sub_5859B0`
- 列数 11 ｜ 确证 8 ｜ 部分 0 ｜ gap 3

## 1.1 Round 7 规则参数 xrefs（2026-09-21）

- 消费方 `sub_836D10`（装备界面）以**机体 CHARA_PARAM 行 `+372`（= col38，行基址 = 节点+0x18）**查本表（`sub_49EDF0`，行距 **24**）；
  同函数另以机体行 **`+796`** 查 `MSMA_WEAPONSET`；`sub_7E7600` / `sub_7E4A50` / `sub_813B30` 同时读 `+372` 与 `+396`（= col44）。
  `sub_6563B0` / `sub_6FC550` 读取 +16/+20 规则参。

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `comb_id` | u32 | +0 | 组合规则ID（主键）。**口径 = `MSMA_SETTINGS`(CHARA_PARAM).col38（机体行 +372）**——即"武器组ID"与"装备组合ID"**共用同一编号空间**（同机体的 col38 既查 `msma_weapon_set` 也查本表） |
| 2 | `2` | `verdict_type` | enum `sub_585580` | +0 | 裁定方式（sub_585580）：固定/类别组合/ID组合等 |
| 3 | `3` | `weapon_category_a` | enum `sub_585FD0` | +4 | 武器类别 A（sub_585FD0，+4） |
| 4 | `4` | `weapon_category_b` | enum `sub_585FD0` | +8 | 武器类别 B（sub_585FD0，+8） |
| 5 | `5` | `weapon_category_c` | enum `sub_585FD0` | +12 | 武器类别 C（sub_585FD0，+12） |
| 6 | `6` | `rule_param_a` | u32 | +16 | 规则参数 A（+16；ID_COMBINATION 时 sub_6FC550 @0x6fc607→sub_56FA70 查表键） |
| 7 | `8` | `rule_param_b` | u32 | +20 | 规则参数 B（+20；sub_6FC550 @0x6fc624 作数组下标；sub_6563B0 槽位阈值参照 +12 邻域） |
| 8 | `10` | `region_gate` | enum `sub_5854E0` | — | 地区开关：CHINA 保留 / JAPAN 丢弃（sub_5854E0 @0x585b0c） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大有效列号。
