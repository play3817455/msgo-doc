# MODULE_BONUS ｜ `module/module_bonus.csv`

- **用途**：模块加成
- 表ID `52` ｜ 下载序 `52` ｜ 类名 `CModuleBonusTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_5A29B0` @`0x5A29B0`（RTTI `??_7CModuleBonusTable@@6B@`@`0xecef28`、ctor `sub_A5A910`@`0xA5A910`）｜ **列数 41**
- ★2026-10-05 第 6 批订正：旧 schema/注释 **4~6 列**（只把循环的**第 1 组**当成整张表）⇒
  按 reader 的**固定块循环**改为 **41 列** = 1 键列 + **8 组 × {A,B,V}**（列步长 5：`{A,缝,B,V,缝}`）⇒ `csv0..csv40`
  （其中 **16 列是缝**，reader 不读）

## 1. 行布局（`sub_5A29B0` 反编译逐条确证）

```c
v3 = 2;
*a3 = sub_BBB370(a1, 1);          // +0   ← csv1；★csv0 全函数不读
v4 = a3 + 2;   v5 = 8;
do {                              // 8 组，组内 3 列，列步长 5、结构步长 3 dword = 12B
    *(v4 - 1) = sub_BBB370(a1, v3);        // → +4  + 12k    组内第 1 项「A」
    v7 = v3 + 2;
    *v4       = sub_BBB370(a1, v7++);      // → +8  + 12k    组内第 2 项「B」
    v4[1]     = sub_BBB370(a1, v7);        // → +12 + 12k    组内第 3 项「V」
    v3 = v7 + 2;                           // csv 号：{5k-3, 5k-1, 5k}
    v4 += 3;
} while (--v5);
```

- 结构大小 = **26 dword = 104B**（`+0` 键 + 8×3）。
- 取值函数链 `sub_BBB370` → `sub_CC6876` → `sub_CC6865` → `sub_CC772B(_, 0, 10)` = **atoi（十进制整数）**
  ⇒ 本表 **25 个取值列全是整数**，**没有**浮点/枚举转换（这点与 `ITEM_PART` 那类 `atof`/枚举表不同）。
- ★**本表索引键在 csv1，不在 csv0**：vtable[5] = `sub_5A2A10`（`return sub_BBB370(a1, 1)`）就是 GetKey。
  写行时**组 ID 必须写在 csv1**；写在 csv0 对客户端不可见。

## 2. 组槽位（8 组 × 3 项；组 k 的列号 = `{5k-3, 5k-1, 5k}`）

| 组 | A（定义 ID） | 缝 | B（参数） | V（数值） | 缝 | 内存（A/B/V） |
|---|---|---|---|---|---|---|
| 1 | `csv2` `group1_stat_id_a` | `csv3` | `csv4` `group1_stat_id_b` | `csv5` `group1_stat_value` | `csv6` | `+4/+8/+12` |
| 2 | `csv7` `group2_stat_id_a` | `csv8` | `csv9` `group2_stat_id_b` | `csv10` `group2_stat_value` | `csv11` | `+16/+20/+24` |
| 3 | `csv12` `group3_stat_id_a` | `csv13` | `csv14` `group3_stat_id_b` | `csv15` `group3_stat_value` | `csv16` | `+28/+32/+36` |
| 4 | `csv17` `group4_stat_id_a` | `csv18` | `csv19` `group4_stat_id_b` | `csv20` `group4_stat_value` | `csv21` | `+40/+44/+48` |
| 5 | `csv22` `group5_stat_id_a` | `csv23` | `csv24` `group5_stat_id_b` | `csv25` `group5_stat_value` | `csv26` | `+52/+56/+60` |
| 6 | `csv27` `group6_stat_id_a` | `csv28` | `csv29` `group6_stat_id_b` | `csv30` `group6_stat_value` | `csv31` | `+64/+68/+72` |
| 7 | `csv32` `group7_stat_id_a` | `csv33` | `csv34` `group7_stat_id_b` | `csv35` `group7_stat_value` | `csv36` | `+76/+80/+84` |
| 8 | `csv37` `group8_stat_id_a` | `csv38` | `csv39` `group8_stat_id_b` | `csv40` `group8_stat_value` | — | `+88/+92/+96` |

| 列 | 订案名 | 类型 | 内存 | 说明 |
|---|---|---|---|---|
| `csv0` | `col0` | — | — | **gap**：`sub_5A29B0` 全函数不读（键在 csv1） |
| `csv1` | `bonus_group` | u32 | +0 | ★**加成组 ID = 索引键** |
| `csv3` `csv6` `csv8` … | `col3` `col6` `col8` … | — | — | **gap**：每组内 1 缝（`5k-2`）+ 组间 1 缝（`5k+1`），共 16 个：`0, 3, 6, 8, 11, 13, 16, 18, 21, 23, 26, 28, 31, 33, 36, 38` |

## 3. 三项槽的语义（消费侧证据，★只到"A"这一层）

| 项 | 订案名 | 证据 |
|---|---|---|
| A | `groupN_stat_id_a` | ★**> 0 才算该槽有效**：`sub_5A2A30`（`v3[5]/v3[8]/…/v3[26] > 0` 逐个计数，返回有效槽数）；`sub_5A2AF0(table, group_id, slot)` 返回该槽的 A（`v4[3*slot+5]`）；`sub_7C09B0` / `sub_7BF480` 拿到 A 后到 `dword_11E3F08` 名表里取**名字串** ⇒ A 是**定义 ID**（可解析出名字） |
| B | `groupN_stat_id_b` | 只确证「reader 读满这一列」；**消费点未找到 ⇒ 语义未取证**（沿旧名 `stat_id_b`） |
| V | `groupN_stat_value` | 同上（沿旧名 `stat_value`）；★读法是 **atoi 整数**，写整数 |

> ⚠️ 旧注释把 csv2/4/5 命名 `stat_id_a`/`stat_id_b`/`stat_value` —— 位置对（=本表组 1），
> 但**不是"整表只有一组"**。本批把组 1 的三个旧名原位置改名为 `group1_*`，组 2..8 按同构命名。

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 行宽 **41 段**（`csv0..csv40`）；缝列（16 个）留空即可。
- ★组 ID 写 **csv1**（第 2 个字段）：`<csv0运行号>,<组ID>,<A>,<B>,<V>,...`；A/B/V 全要写**整数**。
