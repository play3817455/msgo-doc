# ITEM_PART ｜ `item/equip_parts.csv`

- **用途**：装备零件（部件）
- 表ID `7` ｜ 下载序 `7` ｜ 类名 `CPartTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_5955A0` @`0x5955A0` ｜ **列数 50**
- ★2026-10-05 第 5 批订正：旧 schema/注释 **21~23 列**（把「8 组循环」当成单组、把尾列钉在 csv19/20）⇒ 按 reader 的**光标推进**改为 **50 列**
  （**16 前导 + 8 组×3 + 2 尾** = 常态 42 列；含 `MS_BOOST_GAUGE_RECOV` 组的行每组多占 1 列 ⇒ 最坏 50 列）

## 1. 行布局（`sub_5955A0` 反编译逐条确证）

```
+0   = col0                       u32   主键
+4   = col2                       u32   ★col1 全函数不读
+8   = col3                       u32
+12  = sub_5954A0(col4)           enum  MS=0 / WEAPON=1 / ARMOR=2 / 其他=3
+16  = atof(col5)   … +32 = atof(col9)    5 个 float
+36  = sub_5951D0(col10)          enum  触发时机
+40  = atof(col11)
+44  = sub_5951D0(col12)          enum  触发时机
+68  = atoi(col13) ; +48 = atof(col13)    ★同一列双读
+52  = atof(col14) ; +56 = atof(col15)

v6 = 16 ;  v5 = &(+80) ;  do 8 次 {
    +base+0 = sub_5952C0(col v6)          作用对象枚举
    e       = sub_5953B0(col v6+1)        +base+4 = e  参数名枚举
    if (e == 109 /* MS_BOOST_GAUGE_RECOV */) {
        +base+8 = atoi(col v6+2) + 64 * atoi(col v6+3)   ★该组**多占 1 列**
        v6 += 4
    } else {
        +base+8 = atof(col v6+2) ;  v6 += 3
    }
    v5 += 3 ;  base += 12
}
+60 = col v6 ;  +64 = col v6+1             尾部 2 个 u32（**位置 = 光标处，随组内列数浮动**）
```

⇒ **每行宽度不是固定的**：常态 42 列（`csv0..csv41`），行内每出现一次 `MS_BOOST_GAUGE_RECOV` 就多 1 列，
最多 50 列（`csv0..csv49`）。库是固定宽度表 ⇒ schema 按**最坏情况 50** 声明（与第 3 批
`WEAPON_BATTLE_DETAIL` 按"属性名上限"定同一口径：不这样定，真实数据里这类行的最后几列会被**静默截断**）。

## 2. 逐列（常态布局；`csv0..csv41`）

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义 |
|---|---|---|---|---|---|
| 1 | `0` | `item_part_id` | u32 | +0 | 主键；装备零件 ID |
| — | `1` | `col1` | — | — | **gap**：`sub_5955A0` 全函数不读 |
| 2 | `2` | `linked_item_id` | u32 | +4 | 关联 ITEM 行 ID |
| 3 | `3` | `part_group_id` | u32 | +8 | 零件组 ID |
| 4 | `4` | `target_category` | enum `sub_5954A0` | +12 | 作用大类：**MS=0 / WEAPON=1 / ARMOR=2 / 其他=3**（默认 3） |
| 5 | `5` | `trigger_threshold_a` | float | +16 | 触发阈值 A（与 `trigger_type_primary` 配合） |
| 6 | `6` | `trigger_threshold_b` | float | +20 | 触发阈值 B |
| 7 | `7` | `trigger_threshold_c` | float | +24 | 触发阈值 C |
| 8 | `8` | `trigger_threshold_d` | float | +28 | 触发阈值 D |
| 9 | `9` | `trigger_threshold_e` | float | +32 | 触发阈值 E |
| 10 | `10` | `trigger_type_primary` | enum `sub_5951D0` | +36 | 主触发时机（`ANYTIME=1 … COMB_STYLE_CHANGE_INITIAL_POINT=23`） |
| 11 | `11` | `effect_magnitude` | float | +40 | 效果幅度 |
| 12 | `12` | `trigger_type_secondary` | enum `sub_5951D0` | +44 | 副触发时机 |
| 13 | `13` | `param_mod_value` | float | +48 | 参数修改值（**同列还以 u32 存 +68**） |
| 14 | `14` | `param_mod_value_b` | float | +52 | 参数修改值 B |
| 15 | `15` | `param_mod_value_c` | float | +56 | 参数修改值 C |
| 16 | `16` | `group1_scope` | enum `sub_5952C0` | +72 | 第 1 组 作用对象（`MS=1 / WEAPON_SLOT_MAIN=11 / … / OTHER=99`） |
| 17 | `17` | `group1_stat` | enum `sub_5953B0` | +76 | 第 1 组 参数名（`MS_ARMOR=100 … OTHER_CMDRSPT_RESPAWNTIME=2000`） |
| 18 | `18` | `group1_value` | float | +80 | 第 1 组 参数值 |
| 19 | `19` | `group2_scope` | enum `sub_5952C0` | +84 | 第 2 组 作用对象 |
| 20 | `20` | `group2_stat` | enum `sub_5953B0` | +88 | 第 2 组 参数名 |
| 21 | `21` | `group2_value` | float | +92 | 第 2 组 参数值 |
| 22..40 | `22..39` | `group3_*` … `group8_*` | 同上 | `+96..+164` | 第 3~8 组（每组 3 列 / 结构步长 12B） |
| 41 | `40` | `tail_u32_60` | u32 | +60 | 尾部第 1 个 u32（**位置 = 光标处**） |
| 42 | `41` | `tail_u32_64` | u32 | +64 | 尾部第 2 个 u32 |

## 3. 余量槽位 `csv42..csv49`（★只有 109 组才会用到）

| CSV# | 订案名 | 说明 |
|---|---|---|
| `42..49` | `overflow_slot_42` … `overflow_slot_49` | 8 组中每有一个 `MS_BOOST_GAUGE_RECOV`(109) 组，其**值**就由**两列**拼成（`atoi(A) + 64*atoi(B)`）⇒ 该行整体后移 1 列。最多 8 组全为其一 ⇒ 需要到 `csv49`。本表当前 64 行全空（无 109 组）⇒ 常态布局只读到 `csv41` |

> ⚠️ 因此：**`groupN_*` / `tail_*` 的名字只在"前面没有 109 组"时成立**。若某行出现 109 组，
> 该行 109 组之后的列全体后移 1（值槽含义随行变）。写行时按**光标顺序**排布即可，
> 客户端只按顺序消费，末尾多出的空列无害。

## 4. 枚举（三张表都从 IDA 逐条读出）

- `sub_5954A0`（csv4，4 值）：`MS=0 / WEAPON=1 / ARMOR=2 / 其他=3`（**找不到时返回 3**）
- `sub_5952C0`（组内"作用对象"，32 值）：`MS=1 / MS_EXAM=2 / MS_TRANS=3 / MS_HADES=4 /
  WEAPON_SLOT_MAIN=11 / WEAPON_SLOT_SUB=12 / WEAPON_SLOT_EX=13 / WEAPON_SLOT_ALL_EXAM=15 /
  WEAPON_SLOT_ALL_HADES=16 / WEAPON_MACHINEGUN=21 … WEAPON_FUNNEL=42 / OTHER=99`（找不到返回 **0**）
- `sub_5953B0`（组内"参数名"，129 值）：`MS_ARMOR=100 / MS_ARMOR_PER=101 / MS_BOOST_SPEED=102 /
  MS_BOOST_GAUGE=103 / MS_BOOST_RECOVER=104 / MS_PAYLOAD=105 / MS_WARP=106 / MS_ARMOR_NOW=107 /
  ★MS_BOOST_GAUGE_RECOV=109 / MS_DEF_SOLID=110 … / W_POWER=1002 … W_WRESTLE=1102 … /
  OTHER_CMDRSPT_RESPAWNTIME=2000`（找不到返回 **0**；全表见 schema 的 `enum_values`）
- `sub_5951D0`（csv10/csv12，23 值）：`ANYTIME=1 / SPAWN=2 / DEATH=3 / ARMOR_REMAIN=4 /
  KILL_STREAK=5 / DEATH_STREAK=6 / DID_LOCKON=7 / GOT_LOCKON=8 / USER_READYTIME=9 /
  USER_KEYACTION=10 / ARMOR_RATE=11 / WARP_AND_USER_KEYACTION=12 / TAKEOVER_DAMAGE=13 / KILL=14 /
  LEVEL_GAUGE=15 / COMB_UK_SPAWN=16 / USER_KEYACTION_ON=17 / USER_KEYACTION_OFF=18 /
  USER_KEYACTION_RELEASE=19 / WEAPON_HIT=20 / MODEL_ID=21 / REDUCE_ARMOR=22 /
  COMB_STYLE_CHANGE_INITIAL_POINT=23`（找不到返回 **0**）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- 常态布局 **42 段**（`csv0..csv41`）；含 `MS_BOOST_GAUGE_RECOV` 的行按需写到最多 **50 段**。
