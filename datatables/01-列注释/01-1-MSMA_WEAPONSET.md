# MSMA_WEAPONSET ｜ `msma/msma_weapon_set.csv`

- **用途**：机体武器组**——"某武器组下挂哪些武器、各属于哪个槽位"。一行 = **一把武器**；
- 表ID `1` ｜ 下载序 `1` ｜ 类名 `CMSMAWeaponSetTable` ｜ 逐列读取 `sub_587160`
- 列数 29 ｜ 确证 21 ｜ 部分 0 ｜ gap 8

## 1.0 取值口径（2026-09-28 反汇编定案）

**结论：`col0` 的编号空间 = 机体的 7 位 練度ID，不是 9 位 モデルID。**

证据链（`GundamOnline_CHINA_v15.exe`）：

| 步 | 函数 | 事实 |
|---|---|---|
| ① 读表 | `sub_582390` | CSV `CHARA_PARAM` 的 `col38`(`0x26`) → 行偏移 **`+372`**。**直存 u32，未做任何换算**。 |
| ② 消费 | `sub_581690`（表下载后置处理） | 取 `*(row+372)` 作 key 查 `dword_11EBAB4` = `MSMA_WEAPONSET`，把**已启用**（武器行 `+20 != 0`）的行 `+4` 写进机体行 `+376/+380/+384`（**≤3 把**）。 |
| ③ 消费 | `sub_836D10`（机库/装备组合校验） | 取 `[ebx+0x174]`(=+372) 作 key 查 `dword_11EBAB8` = `MSMA_WEAPON_EQUIPCOMB`；另取 `[ebx+0x31C]`(=+796) 查武器组。 |
| ④ 查表 | `sub_49EDF0` | 两张表都是 `std::map<int32, 行>`，key = **32 位整数**；行距 88 / 24 字节。 |

⇒ ②③ 两处都直接用同一个 **32 位整数** 当 map 键。**此链上不存在 練度ID → モデルID 的转换**，
所以：

- ✅ `msma_settings.col38` 必须写 **7 位 練度ID**，且必须**同时命中** `msma_weapon_set.col0`
  与 `msma_weapon_equipcomb.col0`。
- ⛔ 写 9 位 モデルID 是**死行**：map 查不到 ⇒ 机体**零武器**（客户端静默跳过，不报错，最难查）。
- ⛔ `col44`(`+396`) **不是**装备组合校验的键——`sub_836D10` 不消费 `+396`（旧"建议与 col38 同值"无依据）。

**本批口径**：一台机体 = 一个武器组 ⇒ `col38 := 该机体自身的 練度ID`。
命中率 **655 / 698**；剩余 **43 台**在 `msma_weapon_set.csv` 里无对应组（见 `04-填充日志.md` 同日条目）。

## 1.0.1 ★★`col2`（武器ID）的编码律（2026-09-28，`unpackdat` 实证）★★

**机体专属武器 ID 是 9 位，前 6 位由机体的 `練度ID` 决定：**

```
武器ID(9位) = '2' + 練度ID[1:6] + <3位变体>
```

- 实证：`unpackdat/settings/weapon_visual_customize.csv` 的 **46 条真实武器ID 全部 46/46 命中**某机体 lid。
  例：`1203001 ヴァイエイト` → `20300` → `220300001/101/…`；`1148012 ギラ・ドーガ(袖付き)` → `14801` → `214801312/…`。
- 资源目录 = `unpackdat/item/02/<練度ID[5] + 武器序号 + 变体>`（4 位；内含 `EM_*.dxg` 模型 + `EZ_*.vra` 属性）。
- ⛔ **`datatables/names/物品ID全集.csv` 不能当 ID 池**：3351 个里只有 **2 个**符合该律（它是"图标名枚举"的产物）。
- ⚠️ 资源树**不能**独立当武器清单：`item/02` 的 268 个 4 位子目录里，54 条真实武器 ID **只有 15 条**有自己的网格
  ⇒ 资源树只覆盖"有专属网格"的武器，**完整武器列表只能来自 wiki 武器页**。

### ★1.0.2 T3 落地定案：col2 用「真实 sub4 资源目录」造 ID（2026-09-28）

> ⚠️ **2026-10-05 更新**：本节数字是 09-28 的快照。现种子为 **549 组 / 1625 行**；
> 桥表 `机体-wiki武器页桥.csv` 现为 `OK 554 / SUSPECT 5 / UNRESOLVED 145`（704 行）。
> 库侧已于 2026-10-05 12:08 按种子**全量收敛**（2244 行 → 1625 行，全 9 位，断引用 0）。
> 完整取证见 `15-武器表下发链路与漂移取证.md` §12。

**`msma_weapon_set.csv` 已重生成**（`datatables/gen_weapon_set_wiki.py`）：

| 项 | 值 |
|---|---|
| 武器组数 | **547** / 698 台（151 台留空：147 wiki 无页 + 4 人工判无页） |
| 武器行数 | **1637**（col4：MAIN 547 + EX 1090） |
| **col2 落资源成功率** | **1637 / 1637 = 100%**（律与资源双重校验，0 违规） |
| col0 | 練度ID（与 `msma_settings` 的 col38 同键空间） |
| col5 | 由 wiki 武器名判定（枚举 `sub_585FD0` 28 值，见 `reverse-login-chain/formats/枚举表.md`） |

**ID 构造**：`col2 = '2' + 練度ID[1:5] + sub4`，其中 `sub4 ∈ unpackdat/item/02` 且 `sub4[0] == 練度ID[5]`
⇒ **每个 col2 都能落到真实资源目录（能找图/找模型）**。

⚠️ **唯一未证假设**：**「wiki 武器第 i 把」↔「该机体第 i 个 sub4」的先后对应**（无任何来源可证，按序配）。
两侧各自都是真值（ID 真实可落资源、名称真实来自 wiki），只有**配对顺序**是假设 ⇒ 已保留备份，重跑一键改。

- 桥表：`datatables/names/机体-wiki武器页桥.csv`（704 行，`OK 552 / SUSPECT 5 / UNRESOLVED 147`，供人工核对）。
- 校验脚本：`datatables/val_msma_weapon_set.py`。
- 参考：`viewer/ms_weapons.csv`（逐行资源解析）、`viewer/item_bind.csv`（资源↔装备ID）、`viewer/ms_bind.csv`（机体↔资源，含 `UNBOUND`）。

## 1.1 Round 7 成本组 A/B/C（2026-09-21）

- col8–19 三组循环 @`0x587249`：每武器槽 slot0/1/2 各含 **cost_a / cost_b / cost_c** 三通道（同构 MSMA_COLORSET price A/B/C）。
- col22–26 上限联动：col22>0 且 col24/25/26 全≤0 ⇒ col26=9999（@`0x5872f4`）。

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `weapon_group_id` | u32 | +0 | 武器组ID（主键）。**口径 = `MSMA_SETTINGS`(CHARA_PARAM).col38（机体行 +372）**，与 `MSMA_WEAPON_EQUIPCOMB.col0` **同编号空间**；查法 `sub_49EDF0`，行距 **88**：`+4`=武器物品ID→ITEM / `+8`=武器类别 / `+20`=启用。消费方 `sub_581690`（实参 = 机体行基址）把 ≤3 把启用武器写入机体行 `+376/+380/+384`；`sub_836D10` 另以机体行 **`+796`**（rental 口径，见 `msma_rental.col46`）查本表 |
| 2 | `2` | `weapon_item_id` | u32 | +4 | 武器物品ID → ITEM 表（dword_11E3F08）；无效 ID 静默跳过 |
| — | `1` | `col1`（别名 `reserved_u32_1`） | u32 | — | **CSV 列存在、读表未单独取证**（`status=gap`，默认 0）。★**物理列名 = `col1`**：CSV 无表头 ⇒ `DataColumnNames` 自动命名 `colN`；`reserved_u32_1` 只是人读别名（schema `db_column` 权威） |
| — | `3` | `col3`（别名 `reserved_u32_3`） | u32 | — | 同上（`status=gap`，默认 0；物理列名 `col3`） |
| 3 | `4` | `slot_category` | enum `sub_586450` | +24 | 槽位类别：MAIN 主武装 / EX 副武装 / SUB 副槽 / 0 占位（sub_586450 @0x5871cc） |
| 4 | `5` | `weapon_category` | enum `sub_585FD0` | +8 | 武器类别（28 值，sub_585FD0）；写错名 ⇒ 0=MACHINEGUN |
| 5 | `6` | `enabled` | bool | +20 | 启用开关（+20）；sub_581690 只收集为真的行到机体+376/+380/+384 |
| 6 | `7` | `sort_priority` | u32 | +12 | 组内排序权重 u32（+12；sub_58723c 读入 88B 行；sub_586050 持久化） |
| 7 | `8` | `cost_a_slot0` | u32 | +28 | 成本组 A 槽0 u32（col8→+28；读表三组循环 @0x587249；同构 MSMA_COLORSET price A） |
| 8 | `10` | `cost_b_slot0` | u32 | +40 | 成本组 B 槽0 u32（col10→+40；读表三组循环 @0x587249；同构 MSMA_COLORSET price B） |
| 9 | `11` | `cost_c_slot0` | u32 | +52 | 成本组 C 槽0 u32（col11→+52；读表三组循环 @0x587249；同构 MSMA_COLORSET price C） |
| 10 | `12` | `cost_a_slot1` | u32 | +32 | 成本组 A 槽1 u32（col12→+32；读表三组循环 @0x587249；同构 MSMA_COLORSET price A） |
| 11 | `14` | `cost_b_slot1` | u32 | +44 | 成本组 B 槽1 u32（col14→+44；读表三组循环 @0x587249；同构 MSMA_COLORSET price B） |
| 12 | `15` | `cost_c_slot1` | u32 | +56 | 成本组 C 槽1 u32（col15→+56；读表三组循环 @0x587249；同构 MSMA_COLORSET price C） |
| 13 | `16` | `cost_a_slot2` | u32 | +36 | 成本组 A 槽2 u32（col16→+36；读表三组循环 @0x587249；同构 MSMA_COLORSET price A） |
| 14 | `18` | `cost_b_slot2` | u32 | +48 | 成本组 B 槽2 u32（col18→+48；读表三组循环 @0x587249；同构 MSMA_COLORSET price B） |
| 15 | `19` | `cost_c_slot2` | u32 | +60 | 成本组 C 槽2 u32（col19→+60；读表三组循环 @0x587249；同构 MSMA_COLORSET price C） |
| 16 | `22` | `limit_trigger` | u32 | +68 | 上限触发（+68）；>0 且 col24/25/26 全 ≤0 时 col26 强制 9999 |
| 17 | `24` | `limit_param_a` | u32 | +72 | 上限中间参数 A（+72；col22>0 且本列/col25/col26 全≤0 时 col26 强制 9999 @0x5872f4） |
| 18 | `25` | `limit_param_b` | u32 | +76 | 上限中间参数 B（+76；参与 col22 联动 9999 判定 @0x5872f4） |
| 19 | `26` | `limit_cap` | u32 | +80 | 数量上限（+80）；col22>0 且 col24/25/26 全 ≤0 ⇒ 强制 9999 |
| 20 | `27` | `extra_param` | u32 | +84 | 武器生成附加参（+84；sub_622A20 @0x622de1 传入 sub_60D460 末参） |
| 21 | `28` | `region_gate` | str | — | 地区开关：JAPAN 整行丢弃；CHINA/其他保留（strcmp @0x587359） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大有效列号。
- ★**物理列名口径（2026-10-06 batch8 定案）**：schema 的权威字段是 **`db_column`**（缺失才回落 `name`）——
  本表 csv1/csv3 因 CSV 无表头 ⇒ `db_column` = `col1`/`col3`（与 Go `DataColumnNames()` 一致），
  `name` 里的 `reserved_u32_1/3` 只是人读别名。库侧 `cfg.MSMA_WEAPONSET` 已按此口径**原位改名**对齐，
  列漂移自检 0 张（`datatables/_b8_db_drift.py`）。
