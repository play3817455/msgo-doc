# MSMA_COLORSET ｜ `msma/msma_color_set.csv`

- **用途**：机体配色方案表**——每个"配色组"下的配色条目（含价格 / 上限 类的数值组）。
- 表ID `3` ｜ 下载序 `3` ｜ 类名 `CMSMAColorSetTable` ｜ 逐列读取 `sub_57D070`
- 列数 21 ｜ 确证 15 ｜ 部分 0 ｜ gap 6
- **内容现状**：**空表（合法占位）** —— 键空间已定案（§3），但**条目内容无权威来源**（§5），按铁律不猜。

## 1.1 Round 7 价格联动规则（2026-09-21）

- A/B 组：col5>0 且 col7≤0 ⇒ col7=9999；col8>0 且 col10≤0 ⇒ col10=9999（@`0x57d183`）。
- C 组：col14>0 且 col16/17/18 全≤0 ⇒ col18=9999（@`0x57d269`）。

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `color_group_id` | u32 | +0 | 配色组ID（主键；`sub_57D920` 索引键） |
| 2 | `1` | `reserved_u32_1` | u32 | — | 预留（`sub_57D070` 不读） |
| 3 | `2` | `color_entry_id` | u32 | +4 | 配色条目序号（+4；与 color_group_id 配对；**解锁位图位号**，见 §4） |
| 4 | `3` | `name` | str | — | 配色名称（wstring，`sub_456D90` @`0x57d102`） |
| 5 | `4` | `display_flag` | u32 | +8 | 显示/价格档索引 u32（+8；`sub_97CBE0` @`0x97cc92` 按本列选 price 组） |
| 6 | `5` | `price_a_trigger` | u32 | +20 | A组买价/触发值（+20）；>0 且 col7≤0 ⇒ col7 强制 9999 |
| 7 | `6` | `reserved_u32_6` | u32 | — | 预留（不读） |
| 8 | `7` | `price_a_cap` | u32 | +28 | A组库存/上限（+28）；col5>0 且本列≤0 ⇒ 9999 |
| 9 | `8` | `price_b_trigger` | u32 | +32 | B组买价/触发值（+32）；>0 且 col10≤0 ⇒ col10 强制 9999 |
| 10 | `9` | `reserved_u32_9` | u32 | — | 预留（不读） |
| 11 | `10` | `price_b_cap` | u32 | +40 | B组库存/上限（+40）；col8>0 且本列≤0 ⇒ 9999 |
| 12 | `11` | `color_param_11` | u32 | +44 | 配色 UI 附加参（+44；`sub_97CBE0` @`0x97cc1f` 传入 UI vtable+736） |
| 13 | `12` | `reserved_u32_12` | u32 | — | 预留（不读） |
| 14 | `13` | `reserved_u32_13` | u32 | — | 预留（不读） |
| 15 | `14` | `price_c_trigger` | u32 | +56 | C组买价/触发值（+56）；>0 且 col16/17/18 全≤0 ⇒ col18 强制 9999 @`0x57d269` |
| 16 | `15` | `reserved_u32_15` | u32 | — | 预留（不读） |
| 17 | `16` | `price_c_param_a` | u32 | +64 | C组上限中间参数 A（+64；参与 C 组 9999 联动 @`0x57d269`） |
| 18 | `17` | `price_c_param_b` | u32 | +68 | C组上限中间参数 B（+68；参与 C 组 9999 联动 @`0x57d269`） |
| 19 | `18` | `price_c_cap` | u32 | +72 | C组上限（+72）；col14>0 且 col16/17/18 全≤0 ⇒ 9999 |
| 20 | `19` | **`vip_gate`** | enum `sub_58B5A0` | — | ★**VIP 会员等级门槛**（旧名 `region_gate`「地区开关」**已作废**，见 §1.2） |
| 21 | `20` | `extra_param_20` | u32 | +76 | 配色附加 u32（+76；`sub_57D070` @`0x57d247` 读入行尾） |

## 1.2 ★col19 订正（2026-09-28 晚）：不是「地区开关」，是 **VIP 会员等级门槛**

**证据（反编译 + 字符串 xref，`sub_58B5A0` @`0x58B5A0` 全文核对）**

```text
sub_58B5A0(str): 逐一比对字面量 → 返回枚举值
  "NONE"(0x40CE20, 4) → 0   "VIP_ASSOCIATE"(0x40CE20, 13) → 1   "VIP_SILVER"(0x40CE20, 10) → 2
  "VIP_GOLD" → 3   "VIP_PLATINUM" → 4   "VIP_DIAMOND" → 5   "VIP_MASTER" → 6
```

- 全部 7 个字面量只有"会员等级"，**没有 JAPAN / CHINA 任何字样**；
- 空串/未知名 ⇒ `sub_40CE20` 返回 0 ⇒ **NONE**（= 无门槛）；
- **误名来源**：把本列与 `sub_5854E0`（**发行区域** `JAPAN/CHINA/ALL`）搞混了。
  真正用 `sub_5854E0` 的"地区开关"列在 **`MSMA_WEAPONSET` csv25** 与 **`MSMA_WEAPON_EQUIPCOMB` col10**，与配色表无关。
- **读序/列号也曾写错**：`reverse-login-chain/formats/枚举表.md` 旧写 `col14`，
  而 `sub_57D070` 调用点是 `sub_58B5A0(col19)`（v9 递增序列 14→16→17→18→**19**）⇒ **col19**。

**连带同步（跨层，已改）**

| 位置 | 改动 |
|---|---|
| `db_design/schema/cfg/tables/MSMA_COLORSET.json` | csv19 `region_gate`→**`vip_gate`**，meaning 改为 VIP 门槛并标注"非地理区域" |
| `datatables/01-列注释/03-3-MSMA_COLORSET.md` | 本文件（列名 + §1.2） |
| `db_design/tools/_enrich_msma_batch17.py` | `patch_col(d,19,…)` 同口径 ⇒ 防止重跑打回旧名 |
| `serverv/tools/cfg_schema_gen/batch1_msma_group.py` | 同口径（serverv 侧 schema 生成器） |
| `db_design/tools/build_enums_ida_full.py` | `sub_58B5A0` 释义 col14→**col19** |
| `db_design/schema/cfg/enums_ida.json` / `enum_glossary_zh.json` | 释义 col14→col19 |
| `serverv/internal/gm/modules_spec.go` | `SubCols` 的 `region_gate`→`vip_gate`（GM 面板列名） |
| `reverse-login-chain/formats/枚举表.md` | 清单行 col14→col19 |
| `serverv/static/cfg_schema.json` / `gm_data_boundaries.json` | 重生成（`merge_cfg_asm.py`） |

⇒ 这是**改名**（列名集合变了），所以必须同步 GM 侧列名；与 §11 那次"对调列名"不同，这里只有配色表一处用该列。

## 2. 读表函数实际读取的列 = `0..20` 全读（逐指令核对）

`sub_57D070` 对每一列都发一次 `sub_BBB370(a2, idx)`，列号序列实测：

```text
col0(col0)  col2  col3(wstring)  col4
col5  col7  |  col8  col10        ← 2 轮循环（v3=5 → 8 → 11），每轮带 9999 联动
col11
col14 | col16 | col17 | col18     ← C 组
col19 → sub_BBB4F0 取串 → sub_58B5A0 转枚举
col20
```

⇒ **col1/6/9/12/13/15 从不被读**（schema 标 `gap`），写什么都没人看；
⇒ 能影响客户端的列只有上面 15 个（= 本表"确证 15"）。

## 3. 键空间：`color_group_id` 到底是什么（★2026-09-28 新结论）

**消费方链路**：`sub_7D4170`（机库配色槽列表填充）→ 分支 B 走配色：
`sub_57D920(&map, &out, &key)`，`key = *( MS 实例对象 + 8 )`，命中后遍历该组下的条目链表。

**推论：`color_group_id` = `msma_id`（練度ID）**，依据三条：

1. **存档里没有别的候选**：`game.ms_rokaku` 只有 `msma_id` / `color` / `unlocked_colors`，
   **没有任何"配色组 ID"列** ⇒ 客户端只能从 `msma_id` 推。
2. **实例结构体 +8 = msma_id**：`SC-0x48A4-clan_rokaku_add_ms` 逐字段解析器 `sub_B43570` 的写入顺序 =
   `uniqid(u64)@+0/+4`（comment `@0xb4358a`）→ **`msma_id`@+8**（comment `@0xb435a5`）；
   消费方读的正是 `+8`。
3. **玩法侧自洽**：日服 wiki 明确写「カラーリングのアンロックは**1 体ごと**に行う必要があり、
   同種の機体でも共有されない」⇒ **列表按机体模板（msma_id）分组、解锁状态按实例（`unlocked_colors`）**，
   与"表按 msma_id 落键 + 存档位图"完全吻合。

> ⚠️ 仍是**推论**（未确证）：`[实例+8]` 的值需要在 x64dbg 里打印一次（§5 下一步①）。
> 另有可能：键是**由 msma_id 经 `CHARA_MODEL` 派生的模型键**（9 位打包 `モデルID`）。两者都
> 由 `msma_id` 唯一决定，所以**灌数形状**一样，只差键的具体数值。

## 4. 条目号 ↔ 解锁位图

- 位图本体：`game.ms_rokaku.unlocked_colors`（`BIGINT`，64 位）；
- 消费方按 `1 << (entryId - 1)` 置位/试位 ⇒ **`color_entry_id`（col2）是 1 基的位号**，取值域 **1..64**；
- 因此同一配色的"是否已解锁"**不在这张表里**（表只描述目录 + 条件），逐机体的解锁态在存档。

## 5. ★数据源盘点（2026-09-28）：为什么仍然不能灌内容

| 候选来源 | 结论 |
|---|---|
| 客户端本地（`unpackdat/`） | **没有表**。`download_list.csv` 把 `MSMA_COLORSET` 列为**要从服务端下载**；本地 `chara/` 只有 `MSM_*`(mesh) / `MST_*`(贴图) / `anim` / `motionlist.csv` / `Camera_*.csv`… 全是资源，无配色索引 |
| 客户端外观资源 | **服务端不用管**（按 `モデルID` 自解；见 `14-客户端本地与服务端下发数据边界.md`） |
| 日服 wiki `gow.swiki.jp` | **有 588 个 `カラーリング/*` 页面**（每军每机一页），实测能抓到"条目 × 条件"清单：<br>`デフォルト` /`准尉以上+カラースプレーx3` /`少佐以上+カラースプレーx5` /`高級カラースプレーx3` /`特殊カラースプレーx5` /`上製カラースプレーx3` /`カラースプレーx3` /`錬度10以上+スプレーx3` /`錬度15以上` /`錬度20以上` …（约 10 条/机）<br>⇒ **只有条件**：无 `color_group_id`、无条目数字号、无 GP 价、**无游戏内配色名**（wiki 用"条件"当图注） |
| `ITEM`（类型 7 = `MS_COLOR`） | 枚举确证"配色是道具"，但本仓 `item.csv` **没有 MS_COLOR 行**，也没有道具 ID 来源 |

**⇒ 结论：仍按"合法空表"占位，不硬填。**
按项目铁律，键/列语义未全定或来源是"猜"的一律不灌；空表**不阻断下载泵**（`#` 注释占位本来就是合法 0 行）。

**下一步（按性价比，任选其一即可解锁）**

1. **x64dbg 实测（最省）**：进机库配色界面下断 `sub_57D920`，打印 `key`（验 §3 推论）与命中行；
   再断 `sub_7D2790` 打印条目号 ⇒ 一并拿到条目号的真实取值域。
2. **找现成表**：官方离线包 / 老客户端缓存 / 他人私服包里搜 `MSMA_COLORSET` 原始 CSV（真值表）。
3. **抓一次真机下载包**：登录期数据泵里表 3 的原始字节（本仓 `vcelog`/`logcap` 可复用）。

## 6. 填写规则

- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（col19 写 `NONE` / `VIP_ASSOCIATE` … `VIP_MASTER`；写错 ⇒ 读作 0=NONE）。
- **越界列 = 0**：只需写到最大有效列号；`gap` 列（col1/6/9/12/13/15）写了也没人读。
