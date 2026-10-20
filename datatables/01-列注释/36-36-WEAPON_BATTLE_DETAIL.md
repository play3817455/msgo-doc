# WEAPON_BATTLE_DETAIL ｜ `item/weapon_battle_detail.csv`

- **用途（★已定案）**：★**武器战斗明细的"属性 → 值"长表**★——与 **#34 完全同构**（连逐列读取函数都是**同一个 `sub_A47BC0`**），
  一个容器装 **11 张子表**，CSV 靠 `col0` 的**属性名**选子表。它填的就是**武器面板/弹道计算要用的那 11 项参数**。
- 表ID `36` ｜ 下载序 `36` ｜ 类名 `CWeaponBattleDetailTables` ｜ 全局 `dword_11EBAA8` ｜ ctor `sub_A72C10` ｜ 派生 vtable `0xecfd30`
- 逐列读取 `sub_A47BC0`（**与 #34 同一个**）｜行解析 `sub_A5D270`｜消费方 `sub_59A070`（把 11 项读进武器运行时对象）

> ⚠️ 旧版列注释（colCount 3、三列都写 `col0`）是常量传播失败导致的错误，以本文为准。

## 1. CSV 列结构（与 #34 同构，实测）｜★行宽 **9**（2026-10-05 由 3 改正）

| 列 | 读法 | 语义 |
|---|---|---|
| **col0** | `sub_456D90(ctx,0)`（`#` 开头 ⇒ 跳过）→ `sub_BBB4F0(ctx,0)` → **`sub_595CC0` 查 `off_D7DF10` 词表** | ★**属性名**★（决定进哪张子表） |
| **col1** | `sub_BBB4F0(ctx,1)`（字符串） | ★**键**★（**字符串**，武器ID） |
| **col2..col8** | 子表自己的 `vtable[0]`（见 §1.1） | ★**值槽**★（**不是一个值**；宽度随 col0 属性名而定） |

**分派链**：`sub_595CC0`（词表 → 子表编号 1..11）→ **`sub_595B10`** → `this[4*idx-3]` 取子表 → 调其 `vtable[1]`（`AddRow`：**只读 col1**）。

### 1.1 ★值槽模型：`col2` 起按属性名定宽（2026-10-05 行宽 3 → 9）

**旧注释错在哪**：`sub_A47BC0` 是**容器**，它自己**只读 col0**（属性名）——旧扫描就按"读到 3 列"记了 `列数 3`。
真正的值列由**子表对象**读：子表 `AddRow` 只读 `col1`（键），**子表 `vtable[0]` 才读值列**，列号依属性名而定：

| 属性名（col0） | 值列阅读器（子表 vtable[0]） | 读到的列 | 最大 |
|---|---|---|---|
| `POWER` | `sub_57B970` | `2`（int） | 2 |
| `RANGE` / `LOCKON_CAM` / `HIGH_LOCKON` | `sub_595A10` | `2`（float ×100） | 2 |
| `STABILITY` | `sub_595A30` | **`2..6`**（5×float） | 6 |
| `RAPIDDELAY` / `COOLTIME` / `RELOAD` / `SWITCHTIME` | `sub_595AF0` | `2`（float） | 2 |
| `RECOIL` | `sub_595AB0` | `2,3`（2×float，度→弧度） | 3 |
| **`SHIELD`** | `sub_595D60` | **`2..8`** | **8 ← 上限** |

⇒ 行宽必须 **9**（`csv0..csv8`），否则 `SHIELD` 的 `col3..col8` 被**越界兜底吃成 0**（§0.3 口径：列号 ≥ 行宽 ⇒ 空串 ⇒ 0）。

**读时缩放常量**（IDA 实读字节，可复查；这是"表里存的数与内存里的数"之间的固定换算）：

| 常量 | 地址 | 值 | 作用 |
|---|---|---|---|
| `flt_D69A58` | `0xD69A58` | **100.0f**（`0x42C80000`） | `RANGE` / `LOCKON_CAM` / `HIGH_LOCKON` / `STABILITY` 的值 **×100** |
| `flt_D69A68` | `0xD69A68` | **0.017453292f** = π/180（`0x3C8EFA35`） | `RECOIL` 的值 **度 → 弧度** |

```c
// 逐字反编译（2026-10-05 复核）
void sub_595A10(_DWORD *a1, float *a2) { *a2 = sub_BBB470(a1, 2u) * flt_D69A58; }          // RANGE 类
void sub_595AB0(_DWORD *a1, float *a2) { *a2 = sub_BBB470(a1,2u)*flt_D69A68;                // RECOIL
                                         a2[1] = sub_BBB470(a1,3u)*flt_D69A68; }
int  sub_595D60(_DWORD *a1, int a2) {                                                        // SHIELD
  *(_DWORD*)a2      = sub_BBB370(a1, 2u);                       // csv2 int
  *(float*)(a2+4)   = sub_BBB470(a1, 3u);                       // csv3 float
  *(float*)(a2+8)   = sub_BBB470(a1, 4u);                       // csv4 float
  sub_BBB4F0(v4, a1, 5u);                                       // csv5 枚举名
  *(DWORD*)(a2+12)  = 命中 "BEAM" ? 1 : (命中 "BLAST" ? 3 : 2); // ← 非 0/1，是 1/3/2
  *(float*)(a2+16)  = sub_BBB470(a1, 6u);                       // csv6 float
  *(float*)(a2+20)  = sub_BBB470(a1, 7u);                       // csv7 float
  *(_BYTE*)(a2+24)  = sub_BBB370(a1, 8u) != 0;                  // csv8 bool
}
```

**为什么本表从不出现在 `17-` §2「行宽不足」清单里**：子表是 `std::map` 对象，仿真里没有那两个 vtable
⇒ `call [vtable[0]]` 落到 `eip=0x2` ⇒ `UC_ERR_EXCEPTION` ⇒ 被 §2 的 `not emu_err` 筛选**静默排除**
（与 `QUEST` 同一口径漏洞）。**不是"读集未知"，是"仿真这条线结构上跑不通"** ⇒ 现由
`_sweep_verdict.py` 的 `STATIC_READSET` 改判 **`STATIC-OK`**。订正与验收细节见
`17-addendum-属性长表值槽.md`（附录 C）。

### 1.2 值槽语义（随 col0 属性名）

| 值槽 | `POWER` | `RANGE`/`LOCKON_CAM`/`HIGH_LOCKON` | `STABILITY` | `RECOIL` | `SHIELD` |
|---|---|---|---|---|---|
| `csv2` | int `+1936` | float×100 | `f[1]` float×100 `+1956` | `f[0]` float 度 | int `+2012` |
| `csv3` | — | — | `f[0]` float×100 `+1952` | `f[1]` float 度 | float `+2016` |
| `csv4` | — | — | `f[2]` float `+1960`（≤0 ⇒ 缺省 `flt_D91AF8`=0.5） | — | float `+2020` |
| `csv5` | — | — | `f[3]` float `+1964`（≤0 ⇒ 缺省 1.0） | — | 枚举名 `BEAM`=1 / `BLAST`=3 / 其他=2 `+2024` |
| `csv6` | — | — | `f[4]` float `+1968` | — | float `+2028` |
| `csv7` | — | — | — | — | float `+2032` |
| `csv8` | — | — | — | — | int→bool `+2036` |

> ⚠️ **`STABILITY` 的槽位是交换的**：`csv2 → f[1]`、`csv3 → f[0]`（见 §6 的 `sub_59A070` 写入偏移）。
> `RAPIDDELAY`/`COOLTIME`/`RELOAD`/`SWITCHTIME` 各只读 `csv2`。

## 2. ★词表 `off_D7DF10`（名 → 编号）+ 11 张子表（ctor RTTI 实名）

| col0（**必须原样写**） | 值 | 子表类（RTTI） | 容器偏移 | **值列类型** | 含义 |
|---|---|---|---|---|---|
| `POWER` | 1 | `WEAPON_DETAIL_POWER_DATA` | +4 | **int** | **威力** |
| `RANGE` | 2 | `WEAPON_DETAIL_RANGE_DATA` | +20 | **float** | **射程** |
| `STABILITY` | 3 | `WEAPON_DETAIL_STABILITY_DATA` | +36 | **float ×5** | **稳定/集弹**（复合行） |
| `RAPIDDELAY` | 4 | `WEAPON_DETAIL_RAPIDDELAY_DATA` | +52 | **float** | **连射延迟** |
| `COOLTIME` | 5 | `WEAPON_DETAIL_COOLTIME_DATA` | +68 | **float** | **冷却时间** |
| `RELOAD` | 6 | `WEAPON_DETAIL_RELOAD_DATA` | +84 | **float** | **装填** |
| `LOCKON_CAM` | 7 | `WEAPON_DETAIL_LOCKON_CAM_DATA` | +100 | **float** | **锁定（镜头）** |
| `RECOIL` | 8 | `WEAPON_DETAIL_RECOIL_DATA` | +116 | **float ×2** | **后坐力** |
| `SWITCHTIME` | 9 | `WEAPON_DETAIL_SWITCHTIME_DATA` | +132 | **float** | **切换时间** |
| `SHIELD` | 10 | `WEAPON_DETAIL_SHIELD_DATA` | +148 | **复合 (i,f,f,f,f,i…)** | **护盾** |
| `HIGH_LOCKON` | 11 | `WEAPON_DETAIL_HIGH_LOCKON_RANGE_DATA` | +164 | **float** | **高锁定射程** |

- 类型证据：各子表 `vtable[0]` 里调的读列函数 —— `sub_57B970`=**读 col2 成 int**（`POWER`）、
  `sub_595A10`=**读 col2 成 float**（`RANGE`/`HIGH_LOCKON`）、`sub_595AF0`=float（`RAPIDDELAY`/`COOLTIME`/`RELOAD`/`SWITCHTIME`）等。
- 分派只到 **case 11**，与上表一一对应；`sub_595C40`（vtable[4]）= 清空 11 张子表。

## 3. ★消费方对齐表（`sub_59A070`）：11 项读进武器运行时对象

| 子表（词表名） | 写入偏移 | 实测细节 |
|---|---|---|
| `POWER` | `+1936` | ★**某些武器类别（类别值 = `12/43/38/24/36/53`）时取负**★（类别取自武器对象 `+84`） |
| `RANGE` | `+1940`（经 `sub_42A6B0` 单位换算）、原值另存 `+2292` | — |
| `STABILITY` | `+1952/+1956/+1960/+1964/+1968` | 5 个 float；`f[2] <= 0` ⇒ 用 `flt_D91AF8`（默认常量）；`f[3] <= 0` ⇒ 用 `1.0` |
| `RAPIDDELAY` | `+1972` | 同 `sub_42A6B0` 换算 |
| `COOLTIME` | `+1980` | 同上 |
| `RELOAD` | `+1988` | 同上 |
| `LOCKON_CAM` | `+1996` | 单 float |
| `RECOIL` | `+2000/+2004` | 2 个 float |
| `SWITCHTIME` | `+2008` | 单 float |
| `SHIELD` | `+2012/+2016/+2020/+2024/+2028/+2032/+2036` | 7 项（int/float 混 + 1 字节） |
| `HIGH_LOCKON` | `+1948`（原值另存 `+2320`） | 单 float |

> 取不到行时一律按 **0** 处理（`SHIELD` 例外：某几项给 1 / 0.0 默认）⇒ 表里没有该武器 ⇒ 该武器对应参数为 0。

## 4. 内容现状（★2026-10-05 C4 深修后：八族收敛、两端零漂移）

| 项 | 现状 |
|---|---|
| 键域 | **1648 键** = 可达号域 1630 + 现役引用保留 18（`1010401` / `10020101` / `10840101` …） |
| 行数 | 库内 **9579** 行 = 本管线管 **9500**（sidecar 1628 键 × `FAMILIES_36`）+ 8 位 icon-id 族 **79** |
| 逐项行数（库/下发件同值，2026-10-05 实测） | `POWER` 1646 / `LOCKON_CAM` 1496 / `RELOAD` 1499 / `RANGE` 1485 / `STABILITY` 1321 / `RAPIDDELAY` 719 / `COOLTIME` 719 / `HIGH_LOCKON` 694 |
| ★`POWER` 少 2 行是哪两把 | `10840101`(GNビームダガー) / `10840501`(GNビームサーベル(投擲)) —— **纯状态投掷武器**，源 wiki 模板**没有 `威力` 参数**（见 §6.5） |
| 值口径 | **客户端原值**，不是面板值（见 §6；`RAPIDDELAY`/`COOLTIME` 另见 §6.1） |
| 来源 | `datatables/gen_weapon_tables_wiki.py`（`names/武器分配明细.csv` 一表出）+ `load_paired_ms_db.py`（8 位 icon-id 族） |
| 体检 | `python datatables/_audit_scale_conv.py` ⇒ 换算命中率 7/7 项 **100%**、真库**与下发件**均 **0 行越域**、CSV ↔ 库 pair **9579/9579 零漂移** |

> ★**两个 id 家族、两个权威**（2026-10-05 定案，详见 §6.4）：
> - **sidecar 族**（9 位，1628 键）：权威 = `names/武器分配明细.csv` ⇒ 方向 **CSV → 库**；
> - **8 位 icon-id 族**（`现役引用`/`客户端近战` 短号，20 键）：权威 = **库**
>   （← `load_paired_ms_db.py` ← `gow_wiki/data/units.json` 的 `icon_id` 按"多数第一档"归并）
>   ⇒ 方向 **库 → CSV**（由 `apply_weapon_tables_db.py` 回灌）。
>
> 之前那句"CSV 比库少 13 行、属另一批口径的欠账"**已还清**：那 13 行 + 19 行值差
> 全是 8 位族，且 CSV 那一侧是**更早的占位管线把面板白字原样写进原值列**
> （`STABILITY=920` 真值 `0.397003`、`LOCKON_CAM=760` 真值 `75.960025`、`POWER=950` 真值 `250`）。
> `#36` 是**客户端要下载的下发件**（`download_list.csv` 里有 `WEAPON_BATTLE_DETAIL`），
> 所以那不是"内部不一致"而是**真被客户端按错口径读数**（集弹性能差 2300 倍）⇒ 必须收。
>
> ⚠️ **机制更正（2026-10-05，见 `15-武器表下发链路与漂移取证.md` §0）**：客户端下载到的
> 那份字节**不是** `server/datafiles/` 下的种子 CSV，而是 `cfg."WEAPON_BATTLE_DETAIL"` 的
> **库导出**（`cfg.ExportTableRawCSV` → `meta.cfg_manifest.raw_csv` → `0xF86A`；
> `dbstore.go`："Runtime must not read CSV from disk"，种子 CSV 只在空表时回灌一次）。
> 本节的**动作与结论不变**（库那侧八族行已净化、0 越域，导出即干净），变的只是**理由**：
> 种子 CSV 是**对账面**，库才是下发源。⇒ 改库后必须 `cfgsync -export-only` 重导 manifest
> 才会到客户端（该步此前漏做，manifest 仍停在 14263 行的净化前快照）。

★**可达号域**（`#36`/`#37` 的键只能落在这里，口径哨见 §7）：

```
可达号域 = sidecar 9 位武器号(1625)            ← names/武器分配明细.csv col1
         ∪ 客户端 weapon_wrestle.csv 的 8 个近战短号  ← 客户端自带文件，表头 アイテムID
         ∪ 现役引用（msma_weapon_set col2 / game.unlockw / game.ms_rokaku）
```

**★为什么短号（5/6/7 位）不能进这两张表（取证结论，2026-10-04）**

| 证据 | 内容 |
|---|---|
| 客户端自带 `unpackdat/settings/weapon_visual_customize.csv` | 表头第 1 列就是 `#武器ID`，**45 行全是 9 位**（`214607001`=Vガンダム / `224607001`=ガンイージ）⇒ 客户端武器域是 9 位 |
| 客户端自带 `weapon_wrestle.csv` | 表头 `アイテムID`，**只有 8 行**，短号里唯一的真域 |
| 现役 `msma_weapon_set.csv` | 1625 行，**col2（`sub_587160` 读的那列）全是 9 位**；短号只出现在 `.bak` 里 |
| 归一化检验 | 10 条规则（补零 / 补 `'2'` / 去零 / pad8+`2` …）对 `#36` 的 246、`#37` 的 937、`item` 的 1094 个短号 **全 0% 命中** ⇒ **不是**「合法号丢前导零」 |
| 短号的真实出处 | ① 图标号族：`gow_wiki/data/weapon_icon_match.json` 的 `icon_id`（8 位，如 `02012401`=ビーム・ショット・ライフル、`02600151`=腹部メガ粒子砲）—— 有正规日文名，但 **sidecar 781 个武器名里 0 命中** ⇒ 无真值来源；② `10101/10102/10103/10111…` 模板块（5 位、成块递增、同字段全同）；③ 旧轮转抓取错列残渣 |
| 后果 | 其中 6 把（`02600151/02012401/02240601/12520101/02210351/02600101`）的 `POWER` 被写成 **2/6/9/11/12/13** ⇒ 中位机体要 292–1893 发，把真库 TTK 哨（`TestSimDBWeaponArsenalTTK`，上界 250 发）踩响 |

⇒ 处理：`datatables/purge_unreachable_weapon_keys.py` 把 `#36`/`#37` 收敛到可达号域
（删 `#36` 845 键/3575 行、`#37` 848 键/848 行，回滚件在 `datatables/_rollback/`），
**`#78 ITEM` 不动**（那是名称/图标注册表，图标号族行带真名，删了会丢图标绑定）。

## 5. 填写规则（通用）

- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过（表头也用它）。
- **越界列 = 0**；枚举列写**名称**（写错 ⇒ 读作 0）；造表后必跑方言自检。

## 6. ★值口径：表里存「客户端原值」，不是面板值

`sub_59A070` 把表里的值**原样**写进武器对象（`+1936 = POWER`），机库白字由原值乘出来。
服务端读侧已按原值写死（`serverv/internal/store/battle_params.go::panelPowerFromClientRaw`
做 `v := int64(raw) * 10`，再交给 `DamageFor` 的 `ceiling(威力/10)`）。

| 属性 | 机库白字公式 | 表里存什么 |
|---|---|---|
| 威力 | `trunc(原值×10 + 0.4)` | **原值 = 面板/10** |
| 集弹性能 | `trunc((500 − 原值)×K + 0.4)` | `原值/100` |
| 连射速度 | `trunc((2 − 原值)×789.4737 + 0.4)` | 原值（见 §6.1） |
| 装填性能 | `trunc((10 − 原值)×100 + 0.4)` | 原值 |
| 锁定 | `trunc(原值×0.01×1000 + 0.4)` | 原值 |
| 射程距离 / 红锁距离 | —（不走这套） | **原样**（世界单位） |

⚠️ **存成面板值 = 全武器伤害 ×10**（"一发秒杀一切"）。唯一换算表是
`datatables/weapon_client_raw.py`；`gen_weapon_tables_wiki.py` 落盘前必过它，
并有一道哨：`POWER 原值 > 10000` 直接 `SystemExit`（当前原值带 20–3400，中位 300）。

⚠️ 回复/补给系 6 个类别（`12/43/38/24/36/53`）在**消费端**取负，**表里写正值**。

### 6.1 ★`RAPIDDELAY` / `COOLTIME`：同一原值，三种刻度曾混在一起（2026-10-05 收敛）

**两项是同一个数**：`sub_59A070` 把 `RAPIDDELAY`→武器对象 `+1972`、`COOLTIME`→`+1980`，
实测 14 处两者**逐行同值** ⇒ 表里必须成对同值（`weapon_client_raw.COOLTIME_TWIN`）。
服务端只读 `RAPIDDELAY`（`battle_params.go::weaponDetailAttrs`），但两项都要写对。

**唯一权威出处** = `names/武器分配明细.csv` **col12「连射速度」**（wiki 那一栏，白字刻度），
过 `weapon_client_raw.rapid_raw()` 换成**原值**（`%.6f`）写库。

**原值域** = `[0.05, 2.01]`（`weapon_client_raw.RAPID_RAW_LO/HI`；真库实测最小 `0.110657`、
最大 `1.999257`，白字 0 ⇒ 读侧不校验 T5）。判据函数 `rapid_is_raw_domain()`。

**白字换算**（原值 → 机库「連射速度」）逐字来自 IDA：机库属性面板取白字的分支
`sub_80F1A0`（`0x80F1A0`）`case 4`（属性位掩码 4 = 連射速度）：

```
uint = trunc( (flt_E0E780 − 原值) × flt_E0EA50 × flt_D74FA8 × flt_E0E78C + flt_D73338 )
       2.0f               0.5263158f(=10/19)  150.0f      10.0f          0.4f
       @0xE0E780          @0xE0EA50           @0xD74FA8   @0xE0E78C      @0xD73338
⇒ 有效比例 = 0.5263158 × 150 × 10 = 789.4737
```

映射两端实测：原值 `0.124590`↔白字 `1480`、`0.110657`↔`1491`、`0.399457`↔`1263`、
`1.391257`↔`480`、`1.999257`↔`0`。真库 709 行逐行等于 `rapid_raw(wiki 連射速度)` ⇒ **709/709 命中**。

服务端读侧只做**一次**换算，放在 `battle_params.go`：

| 环节 | 出处 |
|---|---|
| 原值 → 白字 | `rapidDisplayFromClientRaw`（常量 `rapidDisplayScaleOrigin/Scale/Bias`） |
| 白字 → 帧 | `battle/validate.go::shotIntervalFrames` = `floor(6 + (1510 − 連射速度)/13)`（60fps 帧，§6.3） |
| 帧 → tick | `HitRules.CooldownTicks`（10Hz tick ⇒ /6） |

**曾经混进来的三种刻度**（真库 1237 行 `RAPIDDELAY` 的构成）：

| 档 | 行数 | 值域样例 | 真伪 |
|---|---|---|---|
| ① 客户端原值（★真值） | 709 | `0.110657 … 0.399457`、`1.391257`、`1.999257` | = `rapid_raw(col12)`，709/709 命中 |
| ② 白字刻度 | ~470 | `1480 / 1466 / 1484 / 1421 / 1170` | 旧管线把 wiki **显示值**直接写进原值列 |
| ③ 错列残渣 | ~58 | `200 / 300 / 720 / 4167 / 5000`、负数 `-4.334086` | 别列串入（射程/装填/锁定期/效果范围） |

**危害是两个方向同时坏的**（读侧旧版用 `cfgU32` 四舍五入到整数）：

- ① 真值 `0.124590` ⇒ `cfgU32` ⇒ **0** ⇒ `RapidDelay == 0` ⇒ §6.3 T5 **完全不校验**（709 行真值全军覆没）；
- ③ 残渣 `720` ⇒ 当成白字 ⇒ `shotIntervalFrames(720)` = 66 帧 ⇒ **1.1 s 冷却** ⇒
  一把 0.13 s 间隔的速射武器**每一发都判 `CDEarly`**，而 `CDEarly` 是**整包判 Miss**
  （`authority.go::onFireRegister`）⇒ **合法玩家输出被打掉**。

**收敛结果**（2026-10-05，脚本 `fix_rapid_delay_units.py`）：

- 709 键按 col12 重写（幂等）；4 个 sidecar **无行**但在原值域内的现役短号**保留**
  （`01010401 / 02711603 / 02840101 / 02840151`，回滚件见 `_rollback/36_rapid_*_rows.csv`）；
- 524 键（523 行 col12 空 + 1 行写 `-`，全是 `EX` 强化档）的 **1048 行全部删除** ——
  wiki 那一格确实留白 ⇒ 无权威值可补 ⇒ 冷却未知 ⇒ **不校验 T5**（缺省纪律 = 放行）；
- 收敛后 `RAPIDDELAY`/`COOLTIME` 各 **713 键**，域外 **0**，CSV ↔ 库 pair 完全一致。

⇒ 这就是 §7 第 4 条那道「整族重写 + 原值域哨」要防的事。

### 6.2 ★`RELOAD`：col15「装填时间」是第二权威（2026-10-05）

维基**老页面表头写「装填時間」、新页面写「装填性能」**，指的是同一个白字（同量纲、可互换）。
sidecar 1625 行里这两列**严格互斥**：

| 情形 | 行数 |
|---|---|
| col14「装填性能」有值（面板域 50..960） | 930 |
| col15「装填时间」有值（面板域 200..900） | 540 |
| 两列都有 | **0** |
| 两列都空 | 155 |

⇒ 只读 col14 会**少 540 个键**，而它们正是"旧管线面板刻度永驻"的重灾区
（真库 C4 实测 `RELOAD` 域外 **350 行**：`740`×104 / `760`×51 / `860`×50 …，
读侧拿 `RELOAD=860` 当"原值" ⇒ 装填时间离谱）。

回退链的唯一出处 = `weapon_client_raw.SIDECAR_36_FALLBACK = {"RELOAD": (15,)}`，
三处**同源**（生成器取值、`_audit_scale_conv.py` 体检、`apply_weapon_tables_db.py` 判定口径）。
修后 `RELOAD` **1499 行、0 行越域、换算命中 1488/1488 = 100%**。

### 6.3 ★`RAPIDDELAY` 的下游：服务端 T5 冷却校验（`RAPIDDELAY → 帧 → tick`）

表里那一个数（`0.05..2.01` 的**客户端原值**）是服务端**唯一的冷却判据**，链路三跳、
**两处取整方向相反**（钉子在 `validate_test.go` ④/`authority_test.go`）：

```
原值 0.124590                      ← 表 36 `RAPIDDELAY`（本节唯一入口）
  │  rapidDisplayFromClientRaw（battle_params.go，常量 rapidDisplayScale*）
  ▼
白字 1480                          ← 机库「連射速度」；也是 `shotIntervalFrames` 的输入口径
  │  shotIntervalFrames(白字) = floor(6 + floorDiv(1510 − 白字, 13))     ← 60fps 客户端帧
  ▼
帧 8                               ← 客户端实际等 8 帧 ≈ 133ms
  │  CooldownTicks(帧) = floor(帧 / FramesPerTick)，FramesPerTick = 6    ← 10Hz 房帧
  ▼
tick 1                             ← `FireRecord.CDEarly` = 本发落在冷却内
```

★**两处取整都朝"更宽"**，理由同一条：**宁可松也不要误杀**（误杀 = 合法玩家掉输出）：

| 跳 | 方向 | 反例（用严取整会坏） |
|---|---|---|
| 白字 → 帧 | **floor**（含负数侧 `floorDiv`，Go `/` 是向零截断） | `1524` ⇒ 真值 4 帧，向零截断得 5 帧 |
| 帧 → tick | **floor**（且至少 1） | `1472` ⇒ 8 帧 ⇒ 真实 7.5 発/s；`ceil` 得 2 tick = 200ms，客户端只等 133ms ⇒ 第二发必误判 |

代价是服务端比客户端**宽最多 1 tick（100ms）**——10Hz 房帧的固有精度，不是换算能修的；
要更严只能提房帧或改用客户端帧号对齐（`fire_count`/`frame_count` 口径未取证，见 `authority.go` V4 欠账）。

★**「原值 ⇒ 0」是本节唯一要防的静默失效**：读侧旧版用 `cfgU32`（四舍五入到整数）解析
⇒ 真值 `0.124590` 变 `0` ⇒ `RapidDelay == 0` ⇒ `CooldownTicks` 返 **0** ⇒
**T5 完全不校验**（709 行真值全军覆没）。反方向的错档更坏：残渣 `720` 被当成白字 ⇒
`shotIntervalFrames(720) = 66` 帧 ⇒ **1.1 s 冷却** ⇒ 一把 0.13 s 间隔的速射武器**每一发都判 `CDEarly`**，
而 `CDEarly` 是**整包判 Miss**（`authority.go::onFireRegister` / `onWeaponHitTo` 的 T5 段）。

★**缺行纪律**：`RAPIDDELAY` 无行 ⇒ `WeaponBattleSpec.RapidDelay == 0` ⇒ 判据缺失
⇒ **不校验 T5、也不写冷却终点**（不是"没有冷却 ⇒ 每发都算早发"）。
这正是 §6.1 里那 524 个 EX 档（col12 留白）的行被**整族删掉**的原因：无权威值可补。

### 6.4 ★两个 id 家族、两个权威（2026-10-05 定案，别再把它们混在一道哨里）

`#36` 里同时住着两族键，**各有各的权威**，两侧同步方向**相反**：

| 族 | 键貌 | 键数 | 权威出处 | 同步方向 |
|---|---|---|---|---|
| sidecar 族 | 9 位 `2+練度ID[1:5]+sub4` | 1628 | `names/武器分配明细.csv`（← 维基模板 + `weapon_client_raw` 换算） | **CSV → 库**（`apply_weapon_tables_db.py` 整族重写） |
| 8 位 icon-id 族 | `01010401` / `02711603` / `10020101` …（`可达武器号域.csv` 标 `现役引用`/`客户端近战`） | 20 | **库** ← `load_paired_ms_db.py` ← `gow_wiki/data/units.json` 的 `icon_id` 按"出现次数最多的第一档"归并 | **库 → CSV**（同脚本**回灌**） |

**为什么第 2 族要回灌**：它的 CSV 行是更早的占位管线（`gen_weapon_pipeline.py`）写的 ——
把**面板白字原样**塞进了原值列：

| 键 | 属性 | CSV（错：面板刻度） | 库（对：客户端原值） |
|---|---|---|---|
| `1010401` | `STABILITY` | `920` | `0.397003` |
| `1010401` | `LOCKON_CAM` | `760` | `75.960025` |
| `1010401` | `POWER` | `950` | `250` |
| `1040201` | `STABILITY` | `800` | `0.997003` |

生成器侧**故意不清**这一族（键不在 sidecar ⇒ `_purge_fam36` 不命中；见 §7 末条的"不抹掉别的管线的行"），
所以只能在写库那一侧补：`apply_weapon_tables_db.py` 写库后，把「键 ∉ sidecar 的 id 集 且属
`FAMILIES_36`」的 CSV 行**按库的取值逐行重写**（改 70 / 补 13 / 删 0 行，留 `_rollback/<stamp>_weapon_battle_detail.csv`）。
回灌后该族**库 == CSV**（79/79 行），且**幂等**（再跑一次改 0 / 补 0 / 删 0）。

> 注：7 位/8 位写法（`1010401` vs `01010401`）不是漂移 —— 读侧 `store.ItemKeyExpr()`
> 两侧都做 `lpad(...,8,'0')`（`0 < n < 1e8`），两种写法在 SQL 里等值（`itemkey_test.go` 钉住）。

### 6.5 ★`POWER` 覆盖洞：全库恰好 2 把，且是"纯状态投掷武器"（2026-10-05 定案）

`#37`（`#36` 的键域来源）共 1648 键，其中 **1646 有 `POWER` 行、2 把没有**：

```
10840101 MACHINEGUN  有 LOCKON_CAM / RANGE / RELOAD
10840501 WRESTLE     有 LOCKON_CAM / RANGE / RELOAD
```

真身（`#78 ITEM`）：`10840101` = **GNビームダガー**（ガンダムエクシア）、
`10840501` = **GNビームサーベル(投擲)**（エクシアリペアⅡ）。两者在
`可達武器号域.csv` 里都标 **`现役引用`**（不是残渣）。

★**这是源缺口，不是管线漏写** —— 三条独立证据（详见 `15-武器表下发链路与漂移取证.md` §22.3）：

| # | 证据 |
|---|---|
| 1 | `gow_wiki/data/units.json` 这两行**没有 `威力` 键**，只有 `効果時間`：`1,650 (1,815)` / `3,000 (3,300)`。`(x)=x×1.1` ⇒ 那是**异常状态持续毫秒**（特性「异常状态強化」+10%） |
| 2 | 原始 wiki 模板（`datatables/wiki/cache/高达OL能天使敢达.txt`）逐字：`重量=300 弹数=1/4 倒地値=105 射程距離=570 装填性能=580 锁定=780 红锁距離=250 效果时间=1650` —— **没有 `威力` 参数** |
| 3 | 日服攻略站 `stoicfps.com/35086` 强化栏：`【GNビームダガー】 効果時間、リロード、射程距離`（**无 威力**）；同页 `【GNソード（ライフルモード）】 威力、リロード、射程距離` 作对照 |

这是 `#36` 里**唯一一类结构性缺 `POWER`** 的武器：同族的 `ビーム・ダガー（投擲）` /
`ヒート・ダート(投擲)` 等 41 行也全是"有 `効果時間`、无 `威力`"。

★**读侧行为：写不写 `0` 完全等价**（逐层核实，故**不需要**补值）：

| 层 | `POWER` 行缺失 | `POWER` 行 = 0 |
|---|---|---|
| `store.weaponBattleParamsFrom` | `HasPower=false, Power=0` | `HasPower=true, Power=0` |
| `battledb.WeaponSource.WeaponPower` | `ok=false` | `ok=true` |
| `battle.DamageFor` | `Power<=0 ⇒ ok=false` | `Power<=0 ⇒ ok=false` |
| `battle.settleDamage` | `settle := ok && base > 0` ⇒ **false** | 同 ⇒ **false** |

⇒ 两条路都**不结算伤害**（`authority.go:518`）；差别只有 `battledb` 启动日志里的 `POWER` 计数。
于是本表的不变量记为 **「1646/1648 + 2 个具名例外」**（`15-` §22.4 方案 A）。
⚠️ 不要按类别基线补值（方案 C）：那会**让这两把开始结算伤害**（行为变化，且类别本身是旧管线兜底默认）。

## 7. ★口径哨（生成器自带，防复污染）

`gen_weapon_tables_wiki.py` 每次运行都会：

1. 读 `datatables/names/可达武器号域.csv`（由 `purge_unreachable_weapon_keys.py` 生成的权威允许键域）；
2. 校验 `#36`/`#37` 现有键是否越域，打印 `#36 越域键 N 个 / #37 越域键 N 个`；
3. **越域且带 `--apply` ⇒ 直接 `SystemExit` 拒绝写入**；
4. ★**原值域哨**（2026-10-05 加，C4 深修扩到 5 项）：`RAPIDDELAY` / `COOLTIME`（域 `0.05..2.01`，且
   两者**逐行同值**）、`STABILITY`（`-0.01..5.0`）、`RELOAD`（`-0.01..10.0`）、
   `LOCKON_CAM`（`0..300`）都过 `weapon_client_raw.is_raw_domain`，域外一律 `SystemExit`。
   域上界取**换算函数的像上界**（不是拟合值）：`stability_raw(面板≥0) ≤ 5.0`、
   `reload_raw(面板≥0) ≤ 10.0`、`lockon_raw` 取维基「锁定」面板域的像 `16..291.7` 留到 `300`；
   与残渣簇地板（`350 / 400 / 740`）之间留 ≥100 倍间隔。
   `POWER`/`RANGE`/`HIGH_LOCKON` **无域**（原值列与白字同量纲，无可分簇）⇒ `is_raw_domain` 返 `True`。
   同一道哨在 `_audit_scale_conv.py` §② 里**对库与种子 CSV 各跑一遍**（种子 CSV 是回灌源与对账面；
   真正下发给客户端的是**库导出**，见 §4 的机制更正）。

★**8 族「整族重写」而不是「按键替换」**（2026-10-05 加，根因见 §6.1/§6.2/§6.4）：
sidecar 有 **1628** 个武器行，POWER/STABILITY/RELOAD/LOCKON_CAM 各有一批**产不出行**的键
（wiki 那一格留白 ⇒ 少 540 个 RELOAD、约 916 个 RAPIDDELAY…）；旧的 `merge` 只按键替换、
不动它们，于是历史上另一条管线灌进来的白字刻度/错列残渣（`920`、`860`、`720`、`-4.334086`…）
**永远留在表里**。现在落盘前先按 `_purge_fam36`
（`attr ∈ RAW.FAMILIES_36` 且 `key ∈ sidecar 键集`）**整族清掉**再重建
（`apply_weapon_tables_db.py` 用同一条判据在库里镜像同一个 prune）。
sidecar **无行**的键（8 位 icon-id 族）**不在清除范围内** ⇒ 不被抹掉，改由 §6.4 的库→CSV 回灌对齐。

```powershell
python datatables/purge_unreachable_weapon_keys.py          # 干跑，顺便刷新允许键域文件
python datatables/purge_unreachable_weapon_keys.py --apply  # 收敛库 + CSV（各留 .bak_purge*）

python datatables/fix_rapid_delay_units.py                  # 干跑：两族刻度收敛体检
python datatables/fix_rapid_delay_units.py --apply          # 修库 + 修 CSV（各留 .bak_rapid* / _rollback/）

python datatables/gen_weapon_tables_wiki.py                 # 干跑：#36/#37/#78 生成 + 三道哨
python datatables/gen_weapon_tables_wiki.py --apply         # 落盘三张下发件

python datatables/apply_weapon_tables_db.py                 # 干跑：写库计划 + 回灌计划
python datatables/apply_weapon_tables_db.py --apply         # 写库 + 8 位族「库→CSV 回灌」
                                                            #   （--no-csv-mirror = 只写库）

python datatables/_audit_scale_conv.py                      # 体检：①换算命中 ②双端域哨 ③零漂移
```
