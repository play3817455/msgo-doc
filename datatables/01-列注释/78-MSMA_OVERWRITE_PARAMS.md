# MSMA_OVERWRITE_PARAMS ｜ `msma/msma_overwrite_params.csv`

> ★本表**不在 79 张下载表的键表里**（键表 ID `0..79` 恰缺 `78`）。客户端是用**硬编码文件名兜底注册**的：
> `sub_576CC0` → `sub_402AD0("msma/msma_overwrite_params.csv", 30)` → `sub_5A6260(&id=78)` ⇒ 表 ID `78`、类名 `CMsmaOverwriteParamsTable`。
> 因此本文没有「下载序」前缀（其余 `01-列注释/*.md` 的 `78-65-ITEM.md` 的 `78` 是 **ITEM 的下载序**，与表 ID 78 无关，勿混淆）。

- **用途**：**区域参数覆写**。它不产生新行，而是把「已经装载好的表行」的若干字段**就地改写**。
- 表ID `78` ｜ 下载序 **—（不在键表内，硬编码注册）** ｜ 类名 `CMsmaOverwriteParamsTable`
- 读表函数 `sub_580360` → 行分派 `sub_5800D0` ｜ **语义上无固定列数（变长键值对）**，但 **DDL 落成 23 个物理列**（见 §「DDL 列宽」）

## DDL 列宽（★2026-09-28）

语义上本表没有"列号"（`FIELD` 是**逐名匹配**的语义名，不是位置），但 cfg 管线是**面向列**的：
导入有 `schema列数 < csv最大列+1` 闸门、导出按 `information_schema` 物理顺序取列。
1 列建模会让**真数据永远回灌不了**（见 `04-填充日志.md` §16.3）。

因此 DDL 显式落成 **55 列** = 固定前缀 3 格 + **26** 组 `<FIELD>,<VALUE>`：

```
row_type, region, target_id,
overwrite_field_1, overwrite_value_1, … , overwrite_field_26, overwrite_value_26
```

- **26 的来源（★2026-10-06 订正，旧值 10/23 作废）**：五个处理器的**可识别字段名**已全部跑完
  （`idautils.XrefsTo(<UTF-16 字面量>)` 按函数分桶 + 逐分支核对）：

  | `TYPE` | 处理器 | 可识别字段名数 |
  |---|---|---|
  | `MS` | `sub_57EEB0` | 9 |
  | **`WEAPON`** | `sub_57F320` | **26** ← **上界** |
  | `PLAN` | `sub_57FAC0` | 3 |
  | `BULLET` | `sub_57FCE0` | 1 |
  | `WRESTLE` | `sub_57FEA0` | 3 |

  ⇒ 一行**最多** `3 + 26×2 = **55**` 字段。
- ⚠️ **旧值 23 是个真陷阱**：它按 MS 字面量块"10 个"定的，而那块里的 `CHARGE_LV2_SPEED`
  其实由 `WEAPON` 处理器读（见下）⇒ 23 列**装不下一行满配 `WEAPON`**，
  一旦真数据出现就会被 `importCSVFile` 的 `len(colNames) < maxCol+1` 闸门**整表拒收**。
- **尾部空对安全**：客户端对不认识的 `FIELD` 名**只 `++idx` 跳过它的 VALUE**（见下"填写规则"）
  ⇒ 导出时补齐的空对被静默跳过；且 55 = 3 + 52 是**偶数对**，不会让配对错位。
- ⚠️ **超过 55 字段时只能追加列**（append-only）：仅当官方数据真出现「单行 >26 组对」时才需要。
- 生成器：`db_design/tools/patch_overwrite_params_columns.py`（可重跑；别在 JSON 里手删列）。
  回归守卫：`serverv/internal/cfg/schema_import_test.go`。

## 行格式（★定案）

```
<TYPE>,<REGION>,<ID>[,<FIELD>,<VALUE>]...
```

| CSV# | 名 | 类型 | 语义 |
|---|---|---|---|
| `0` | `row_type` | 关键字 | `MS` / `WEAPON` / `PLAN` / `BULLET` / `WRESTLE`；**不是 ID** |
| `1` | `region` | 关键字 | `CHINA` 或 `CHINA_TPE`；**其余值整行丢弃**（不报错） |
| `2` | `target_id` | u32 | 目标表里的行 ID（`MS` 时 = CHARA_PARAM 的 `msma_id`） |
| `3,4` | `FIELD`,`VALUE` | 关键字 + 值 | 重复任意组；`FIELD` 是目标表字段的**语义名** |

- `CSV#0` 首字符 == `#` ⇒ 注释行；`CSV#0` 为空 ⇒ 整行跳过。
- `FIELD` 不认识 ⇒ **只跳过它的 VALUE**（`++idx`），不报错、不影响后续对。
- ⚠️ **本表没有「列号」概念**：`FIELD` 由处理器用 exe 内硬编码的 UTF-16 字面量**逐名比较**后写到目标行的固定内存偏移 ⇒ 不要按列号建模本表。

## 行类型分派（`sub_5800D0`，★2026-10-06 逐指令复核）

```
field1 ∈ {CHINA(0xD7A87C,len5), CHINA_TPE(0xD7A868,len9)}   ← 不满足则整行丢弃（jmp 0x5802F7）
   ├─ field0 == "MS"      (0xD7A860,len2) → sub_57EEB0  → 改写 CHARA_PARAM 行（dword_11E3F14）｜9 名
   ├─ field0 == "WEAPON"  (0xD7A850,len6) → sub_57F320  → 改写**武器运行时对象**｜26 名
   ├─ field0 == "PLAN"    (0xD7A844)      → sub_57FAC0  → 改写 MSMA_PLAN 行｜3 名
   ├─ field0 == "BULLET"  (0xD7870C)      → sub_57FCE0 ｜1 名
   └─ field0 == "WRESTLE" (0xD7A834,len7) → sub_57FEA0 ｜3 名
```

- `MS`/`WEAPON` 走 `sub_408530`（宽串比较，**返回 0 = 相等**，显式 `push <字数>`）；
  `PLAN`/`BULLET`/`WRESTLE` 走 `sub_41C500`（单参窄串比较，无长度参数）⇒ **两条比较路径并存**，别只看一条。
- 字面量块 `0xD7A480~0xD7A88A` 已逐字节读出；`BULLET` 的字面量**不在这一块**（在 `0xD7870C`）。
- ⚠️ IDA 对 UTF-16 字面量的 `string` 注解是把宽字节当 ASCII 显示，**是错的**，别信那一列。

## `MS` 的字段名 → 目标（`sub_57EEB0`，★定案）

行基址 = 树节点 `+0x18`（`sub_581200` 查 `dword_11E3F14 + 4`）。偏移**相对行基址**；`str` 用 `sub_402310`（窄串赋值），`u32` 用 `sub_BBB370`（取整）。

| `FIELD` | 字面量 VA | 目标偏移 | 类型 | 对应 CHARA_PARAM 列 |
|---|---|---|---|---|
| `RESPAWN` | `0xD7A48C` | `+436` | str | col56 |
| `WARP` | `0xD7A4C4` | `+464` | str | col58 |
| `COST` | `0xD7A480` | `+492` | str | col60 |
| `ARMOR` | `0xD7A510` | `+520` | str | col62 |
| `BOOST` | `0xD7A504` | `+604` | str | col69 |
| `BOOST_CHARGE` | `0xD7A4E8` | `+632` | str | col71 |
| `BOOST_SPEED` | `0xD7A4D0` | `+660` | str | col73 |
| `PAYLOAD` | `0xD7A4B4` | `+248` | u32 | col52 |
| `MODULE_SLOT` | `0xD7A49C` | `+252` | u32 | col83 |

- **9 名（★2026-10-06 复核）**：`idautils.XrefsTo` 逐字面量分桶 ⇒ `sub_57EEB0` **只引用 9 个**字段名，
  不含 `CHARGE_LV2_SPEED`（该名归 `WEAPON`，见下节）。旧文把 MS 记成"10 个字面量"是把
  **物理相邻**误当**归属相同**。
- ★**9 个 `str` 槽 = 一段 stride 28 字节的 `std::string` 数组**（MSVC `std::string` = 28B）：
  `+436 / +464 / +492 / +520 / +548 / +576 / +604 / +632 / +660 / +688` 共 **10 槽**，
  本表能覆写其中 **7** 个（`RESPAWN / WARP / COST / ARMOR / BOOST / BOOST_CHARGE / BOOST_SPEED`）。

- 未覆写：`+548` / `+576` / `+688`（= col64 / col67 / col79）。★**2026-09-28 定案其子表归属**：
  `+548`(col64) = **`ENERGY`**（子表 `MSMA_DETAIL_ENERGY_DATA`）｜`+576`(col67) = **`MOVE`**（`MSMA_DETAIL_MOVE_DATA`，
  ⇒ 面板「最高速度」）｜`+688`(col79) = **`JUMP`**（`MSMA_DETAIL_JUMP_DATA`）—— 三者只是**表 78 没有对应覆写关键字**，
  并非含义不明（映射见 `sub_581690` 逐块 + ctor `sub_A725F0` RTTI；表见 `01-列注释/04-4-CHARA_PARAM.md`）。
- ★**`CHARGE_LV2_SPEED` 归属已结案（2026-10-06）**：它虽然与 MS 那批字面量**物理相邻**，但
  `sub_57EEB0` **不引用它**，而 `sub_57F320`（`WEAPON` 处理器）引用它 ⇒ 归 **`WEAPON`**，
  目标 `+0x8D4`（见下节）。旧文的"待查"作废。
- ★**字面量块已字节级复核**：`get_bytes(0xD7A470, 208)` 逐字解码，9 个 MS 关键字 + 1 个 WEAPON 关键字
  （`COST / RESPAWN / MODULE_SLOT / PAYLOAD / WARP / BOOST_SPEED / BOOST_CHARGE / BOOST / ARMOR /
  CHARGE_LV2_SPEED`）**全部按地址与 IDA 标签对齐** ⇒
  ⚠️ **IDA 对这块的 `string` 注解是把 UTF-16 当 ASCII/UTF-8 显示，是错的，别信那列**。
- ⚠️ 七个 `str` 槽**写成字符串而不是数值** ⇒ 这些槽存的是**键/标签**，不是直接数值；这与 `sub_581690` 拿这 10 个槽当**查表键**去查 `MSMA_BATTLE_DETAIL` 家族（`dword_11EBA64`）互相印证。
  ★**键值语义（2026-09-28）**：子表是 `std::map<std::string,...>`，**插入时读 `msma_battle_detail.csv` 的 col1 作键**
  （`sub_A5BE20`：`sub_BBB4F0(idx=1)` → `vtable[2](key,val)`），查询时用本表的槽串（`sub_581270`/`sub_5812E0` 的 strcmp）。
  ⇒ **槽串必须与 `msma_battle_detail.csv` col1 逐字节相等**；本仓两边统一用**練度ID 十进制串**（`gen_msma_machine.py`）。
  槽空 ⇒ 键为空串 ⇒ 查不到 ⇒ 后处理按 0。
- ✅ **命名冲突已结案（2026-09-28）**：`+248` = **`PAYLOAD` = 「装备搭载量」**，`+252` = **`MODULE_SLOT`**。
  本表关键字名**胜出**（它是开发者数据文件用名），`CHARA_PARAM` 侧那两个名字作废。三源一致：

  | 来源 | `+248` 的名字 | `+252` 的名字 |
  |---|---|---|
  | 本表覆写关键字（`sub_57EEB0`） | `PAYLOAD` | `MODULE_SLOT` |
  | 开发作弊命令 `sub_6246D0` 内建名表 | `PAYLOAD` | （未出现） |
  | 机库参数面板绑定 `sub_61C9A0` | idx4 **「装备搭载量」** | 面板 6 参数**无此格** |

  - **根因**：`04-4-CHARA_PARAM.md` 的旧名源自 `06-UI…` §7.2 一张**算重了 `+24`** 的表
    （`v5` 已是行基址，却又被当成 `row+24`）⇒ 该表已订正，旧名连带作废。
  - `+252` **不属于**面板 6 参数（面板真身 = `+164/+176/+180/+236/+248` + `sub_40C740`）
    ⇒ 疑为 str `(82,3,48)`「模块槽位数」，**待证**。
  - ⚠️ **连带影响**：`CHARA_PARAM` 的 col83/85/86/89 旧名（紧急返回性能/装备搭载量/喷射蓄力/最高速度）**全部作废**，
    其 576 行现值**不可信待重判**；只有 col52（=`装备搭载量`）列名对，但**填的是"ブースト容量"⇒值也错**。详见 `04-填充日志.md` §9。
- ⚠️ **本表自身的 `v5` 与 `CHARA_PARAM` 行基址同一性已证**：`v5 = v33 + 24`，而 9 个串槽偏移
  （`+436/464/492/520/604/632/660`）与 `sub_582390` 的 `a3` 侧**9/9 全中** ⇒ 上表偏移**可用，无歧义**。

## `WEAPON` 的字段名 → 目标（`sub_57F320`，★2026-10-06 定案，**26 名**）

- **目标 = 武器运行时对象**（与 `sub_59A070` 写入的是**同一个**对象，见
  `01-列注释/36-36-WEAPON_BATTLE_DETAIL.md` §3）。基址寄存器 `ebp`（`mov ebp, [esp+64h+var_50]` @`0x57F38D`）。
- ★**同址互证（两处硬巧合）**：`RANGE → +0x8F4` = **`+2292`**、`HIGH_LOCKON → +0x910` = **`+2320`**
  —— 正是 doc36 §3 记的这两个属性的「**原值另存**」槽；且 doc36 §3 的值段
  （`POWER +1936=0x790` … `SHIELD` 末槽 `+2036=0x7F4`）**刚好铺满 `0x790~0x7F7`**，
  紧接其后就是本处理器的 `MAGAZINE_NUM`（`+0x7F8`）⇒ 目标对象同一，**无歧义**。

| `FIELD` | 字面量 VA | 目标偏移 | 类型 | 备注 |
|---|---|---|---|---|
| `BULLET_ID` | `0xD7A6A0` | `+0x774` | u32 | |
| `MAGAZINE_NUM` | `aMagazineNum` | `+0x7F8` | u32 | 经 setter `sub_57EDF0(ecx=槽)` |
| `MAGAZINE_NUM_TOTAL` | `aMagazineNumTot` | `+0x800` | u32 | 经 setter `sub_40C720(ecx=槽)` |
| `WEIGHT` | `0xD7A6DC` | `+0x820` | u32 | |
| `DOWN_POINT` | `0xD7A784` | `+0x824` | u32 | |
| `LOCKON_TIME` | `0xD7A648` | `+0x830` | float | |
| `LOCK_RADIUS` | `0xD7A630` | `+0x834` | float | |
| `DELAY_TIME` | `0xD7A6B4` | `+0x838` | float | |
| `CONDITION_TYPE` | `0xD7A680` | `+0x84C` | u32 | 经 `sub_596D50`（1Ch 栈对象 → 枚举号） |
| `CONDITION_TIME` | `0xD7A660` | `+0x850` | float | |
| `CHARGE_LV1_POWER` | `0xD7A5D0` | `+0x8C0` | u32 | |
| `CHARGE_LV2_POWER` | `0xD7A564` | `+0x8C4` | u32 | |
| `CHARGE_LV1_SCALE` | `0xD7A5AC` | `+0x8C8` | u32 | |
| `CHARGE_LV2_SCALE` | `0xD7A540` | `+0x8CC` | u32 | |
| `CHARGE_LV1_SPEED` | `0xD7A588` | `+0x8D0` | u32 | |
| `CHARGE_LV2_SPEED` | `0xD7A51C` | `+0x8D4` | u32 | ★旧文误记「归属待查」 |
| `POWER` | `0xD7A7C0` | `+0x8D8` | u32 | ⚠️ 与 doc36 的 `POWER +1936` **不是同槽**，语义未定案 |
| `RANGE` | `0xD7A7B4` | `+0x8F4` | str(28B) | = doc36「原值另存 `+2292`」 |
| `HIGH_LOCKON` | `0xD7A79C` | `+0x910` | str | = doc36「原值另存 `+2320`」 |
| `STABILITY` | `0xD7A770` | `+0x92C` | str | |
| `RAPID_DELAY` | `0xD7A758` | `+0x948` | str | |
| `COOL_TIME` | `0xD7A5F4` | `+0x964` | str | |
| `RELOAD_TIME` | `0xD7A740` | `+0x980` | str | |
| `LOCKON` | `0xD7A6CC` | `+0x99C` | str | |
| `WEAPON_CHANGE_TIME` | `0xD7A608` | `+0x9D4` | str | |
| `SHIELD` | `0xD7A730` | `+0x9F0` | str | |

- `RANGE` … `SHIELD` 这 9 个 `str` 槽 **stride = 28 字节**（`std::string`）：
  `0x8F4 / 0x910 / 0x92C / 0x948 / 0x964 / 0x980 / 0x99C / (0x9B8 **无关键字**) / 0x9D4 / 0x9F0`
  ⇒ 这是一段**定长 28B 的串数组**，其中 `0x9B8` 那一格没有对应覆写关键字（疑为 `LOCKON_CAM`）。

## `PLAN` 的字段名 → 目标（`sub_57FAC0`，★2026-10-06 定案，3 名）

基址寄存器 `ebx` = 按 `target_id` 查到的那一行对象（`mov ebx, [esp+64h+var_50]`）。

| `FIELD` | 字面量 VA | 目标偏移 | 类型 |
|---|---|---|---|
| `SP_PARTS1` | `0xD7A7F4` | `+8` | u32 |
| `SP_PARTS2` | `0xD7A7E0` | `+12` | u32 |
| `SP_PARTS3` | `0xD7A7CC` | `+16` | u32 |

- ★**同址互证**：`+8 / +12 / +16` 与 `MSMA_PLAN` 的 `col7 / col9 / col11`
  （`plan_header_a/b/c`，schema 记 `a3[2]/a3[3]/a3[4] @+8/+12/+16`）**一一对上**
  ⇒ `TYPE=PLAN` 的 `target_id` 应给 **`MSMA_PLAN.plan_id`**。

## `BULLET` 的字段名 → 目标（`sub_57FCE0`，★2026-10-06 定案，**1 名**）

| `FIELD` | 字面量 VA | 目标偏移 | 类型 |
|---|---|---|---|
| `EXP_RANGE` | `0xD7A808` | `+0x1C` | float（`sub_BBB470` 取 float） |

- ⚠️ **旧文里「`BULLET` 有 `EXP_RANGE`/`MOVE`/`DELAY` 三名」是误记**：`sub_57FCE0` 全程
  **只引用 1 个字面量**；`MOVE`/`DELAY` 由 `WRESTLE` 处理器读（见下）。
- `+0x1C` 与 `BULLET` 表运行对象的 `spread_angle`(`+28`) 同址；该槽在本处理器里的语义未定案。

## `WRESTLE` 的字段名 → 目标（`sub_57FEA0`，★2026-10-06 定案，3 名）

基址寄存器 `ebx` = 按 `target_id` 查到的那一行对象。

| `FIELD` | 字面量 VA | 目标偏移 | 类型 | 换算 |
|---|---|---|---|---|
| `DELAY` | `0xD7A828` | `+8` | float | `× flt_D68748` |
| `BOOST` | `0xD7A504` | `+0x10` | u32 | — |
| `MOVE` | `0xD7A81C` | `+0x5C` | float | `× flt_D69A58`(= **100.0f**) |

- ⚠️ `BOOST` 与 `MS` **同名不同对象**（两条独立比较链、两个不同基址）⇒ 不冲突，但别把两处的偏移混用。

## 填写规则

- 编码 **UTF-8 无 BOM**、换行 **CRLF**；`#` 开头整行跳过。
- **本仓当前内容 = 空表**（仅注释头）。理由：本表内容属**发行方按区域投放的覆写数据**，本仓（`unpackdat/` + codex）**无来源**，编造会直接改写机体战力 ⇒ **不填**。
- ⚠️ 历史占位内容 `1,` … `64,` **格式非法**（`CSV#0` 是行类型关键字，不是整数 ID）⇒ 已删除。这类行不会崩客户端（`field1` 为空 ⇒ 整行丢弃），但会误导后续填充工作。

## 证据

| 结论 | 取证 |
|---|---|
| 硬编码文件名注册、表 ID 78 | `sub_576CC0`：`sub_402AD0("msma/msma_overwrite_params.csv", 30)`；`v9 = 78; sub_5A6260(v4, &v9)` |
| 行分派 | `sub_5800D0 @0x580116~0x5802EF`（field0/field1 两格 + 5 路分派） |
| 关键字字面量 | `get_bytes 0xD7A480..0xD7A520` / `0xD7A830..0xD7A88A`（UTF-16LE，逐个读出） |
| **字段名→处理器归属** | `idautils.XrefsTo(<字面量 VA>)` 按 `idaapi.get_func` 分桶（2026-10-06）：`sub_57EEB0` 9 / `sub_57F320` 26 / `sub_57FAC0` 3 / `sub_57FCE0` 1 / `sub_57FEA0` 3 |
| 宽串比较语义 | `sub_408530`（`this[5]`=size、`this[6]`=cap；返回 0=相等） |
| `MS` 字段 → 偏移 | `sub_57EEB0` 逐分支（`v5+130/151/158/165/116/123/109`、`v5[62]/v5[63]`） |
| 单元格取值 | `sub_456D90` = 取单元格（内部 UTF-16）；`sub_BBB4F0` = 取单元格并转窄串；`sub_BBB370` = 取单元格取整；`sub_BBB470` = 取单元格取 float |
| `WEAPON` 字段 → 偏移 | `sub_57F320` 分支链：比较 `0x57F440→0x57FA4E`、目标槽 `0x57F48B…0x57FA71`（`lea ecx,[ebp+X]`=str、`mov [ebp+X],eax`=u32、`fstp [ebp+X]`=float） |
| `WEAPON` 目标对象 = 武器运行时对象 | `RANGE→+0x8F4`=`+2292`、`HIGH_LOCKON→+0x910`=`+2320` 与 doc36 §3「原值另存」同址；doc36 值段 `0x790~0x7F7` 与 `MAGAZINE_NUM +0x7F8` 首尾相接 |
| `PLAN` 字段 → 偏移 | `sub_57FAC0`：`mov [ebx+8]/[ebx+0Ch]/[ebx+10h], eax` @`0x57FC1E/0x57FC61/0x57FC92` |
| `BULLET` 只有 1 个字段名 | `sub_57FCE0` 全函数只有 `0xD7A808` 一处字面量引用（`XrefsTo` + 全指令扫描双证） |
| `WRESTLE` 字段 → 偏移 | `sub_57FEA0`：`fstp [ebx+8]`(DELAY) / `mov [ebx+10h],eax`(BOOST) / `fstp [ebx+5Ch]`(MOVE) |

## 未定案

1. ~~`WEAPON` / `PLAN` / `BULLET` / `WRESTLE` 四个处理器的**完整**字段名→偏移表未跑完~~ ⇒ **已结案（2026-10-06，见上四节）**。
2. 覆写**生效时机**（装载时一次性 vs 每次读表重算；`sub_580360` 的调用点未定案）。
3. 官方 CN 客户端是否有真数据 —— 无来源，不可取证。
4. ~~`PAYLOAD` / `MODULE_SLOT` 与 col52 / col83 的命名冲突~~ ⇒ **已结案（2026-09-28，见上）**。
5. ~~`CHARGE_LV2_SPEED` 的归属处理器~~ ⇒ **已结案（2026-10-06）：`WEAPON`，`+0x8D4`**。
6. `+252` 是否即 str `(82,3,48)`「模块槽位数」（值域待检）。
7. `CHARA_PARAM` 的 `+244` / `+256` / `+356` 三列语义（旧名已废）。
8. `WEAPON` 的 `POWER`(`+0x8D8`) 与 doc36 `sub_59A070` 的 `POWER`(`+1936`) **双槽关系**（哪个是显示/哪个是战斗用）。
9. `WEAPON` 串数组里 `0x9B8` 那一格无关键字（疑 `LOCKON_CAM`）；`BULLET` 的 `+0x1C` 语义。
