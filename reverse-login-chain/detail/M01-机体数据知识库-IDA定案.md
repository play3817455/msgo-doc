# M01 · 机体（MS/msma）数据知识库 —— IDA 定案版

> 范围：**机体相关的全部数据面**——ID 体系 / 数据表逐列 / 机库报文 / 资源目录 / 崩溃结论。
> 方法（用户要求）：**一切结论必须能在 `GundamOnline_CHINA_v15.exe.i64`（ImageBase `0x400000`）里反查到**；
> 以前的记忆只作线索，**不一致处以本文的 IDA 证据为准**，并在 §10 列出"被推翻的旧结论"。
> 资源包真源：`unpackdat/`（253k 文件 / 15.5 GB）＋客户端 `data/*.hed/*.dat`（30.4 GB）。
> 相关既有文档：`detail/W16`（机库/编成 send 族）、`detail/W11`（首屏应答）、`formats/数据表-80表列规格.md`、
> `datatables/01-列注释/04..05`、`server/docs/MEMORY.md`（服务端侧 P198~P214）。

---

## §0 一页速查

| 问题 | 答案（IDA 定案） |
|---|---|
| 机体有几种 ID？ | **4 种**：`練度ID`(7 位, 表主键) / `モデルID`(9 位, 资源键) / `shopitem_id`(商品) / `uniqid`(u64, 玩家实例) |
| 机体表几张？ | 服务端下发 **12 张** `msma/*.csv`（详 §2）；另有客户端本地 `settings/msma_*_customize.csv` |
| 机体名从哪来？ | `msma_settings.csv` **col5**（`sub_456D90` → **宽串** `wstring`） |
| モデルID 在哪列？ | `msma_model.csv` **col71(低32) + col72(高32)** → `edi+1B4h` / `edi+1B8h` |
| モデルID → 目录？ | `wsprintfW("chara/%02d/%02d/%04d/…")`（kind=1 时 `%02d/%03d/%05d/…`）—— §6 |
| 机库推送体长？ | **303B**（线上）／312B（内存，含对齐填充）—— 逐字段求和 IDA 验证 ✓ |
| 机库 begin/end？ | `0x16AC` 请求 ⇒ `0x2ACF`(begin,`slot_num`) → N×`0xA832`(303B) → `0xFCE6`(end, 空体) |
| `msma_model.csv` 空列会不会崩？ | **不会**（越界/空列 ⇒ 空串非 NULL）；**P214 的"空列 ⇒ wcslen(NULL)"已被证伪** ✗ 见 §10 |
| 「我的机体」崩点？ | 两型并存：① `0x004022F1`(`wcslen` 坏指针) ② **环形队列 `Pop` 的 `this=4`**（代码**已定位** ⇒ §8.5：`<基址>+0x28D71`，DLIB/XGGLib 解密区） |

---

## §1 ID 体系（★最易混，先把这张表钉死）

```
練度ID (7 位, 如 1107011)          ← 表主键 = 行键 = 我们口中的"机体 id"
  │  写在 msma_settings.col0 / msma_model.col0 / msma_weapon_set.col0 …
  │  ★也是服务端 DB core.character_ms.msma_id / character_msdeck.msma_id
  ↓ msma_model.col71(低32)+col72(高32)
モデルID (9 位, 如 101025101)      ← ★资源键★（"models"）
  │  ★注意：msma_settings 的"col1"是**另一套编号**（如 124120101，用于图标）✗ 别混
  ↓ sub_473390 解码 + sub_49D170(wsprintfW)
chara/<a>/<b>/<c>/                ← 资源目录（unpackdat/chara/…）
  ↓ 目录内固定文件名
motionlist.csv / Camera_Hangar.csv / Camera_MsSelect.csv / model/ MSM_*.dxg / tex/ MST_*.dds …
```

- **图标**：`interface/icon/color/c0<资源id>_001..006.dds`（`资源id` = `msma_settings` 那一套，与モデルID 不同）✓
- **商品**：`msma_settings.col0`（練度ID）当 `shopitem_id`（P214 已实测：用 col0 才有名字/图标）✓
- **`uniqid`(u64)**：玩家**拥有的那台**的唯一 ID（不是机体定义 id）；机库记录、编成、装备报文全用它 ✓

---

## §2 机体相关数据表全清单（`download_list.csv` 下发）

| 下载序 | 表ID | 文件 | 类名 | 逐列读取 | 列数 | 服务端数据现状 |
|---|---|---|---|---|---|---|
| 1 | 1 | `msma/msma_weapon_set.csv` | `CMSMAWeaponSetTable` | `sub_587160` | 15 | 2246 行 ✓（MAIN/SHIELD/SPECIAL 真值源） |
| 2 | 2 | `msma/msma_weapon_equipcomb.csv` | `CMSMAWeaponEquipCombTable` | `sub_5859B0` | 8 | 696 行 ✓ |
| 3 | 3 | `msma/msma_color_set.csv` | `CMSMAColorSetTable` | `sub_57D070` | 13 | **0 行** ✗（配色要用） |
| 4 | 4 | `msma/msma_settings.csv` | `CCharaParamTable` | `sub_582390` | 64（CSV 到 col91） | 696 行，仅 col0/col5 有值 ✗ |
| 5 | 5 | `msma/msma_model.csv` | `CCharaTable` | `sub_571380` | 68（读 col0..76） | 696 行，仅 col0/col71 有值 ✗ |
| 20 | 20 | `msma/msma_battle_detail.csv` | `CMSMABattleDetailTables` | `sub_A47BC0` | 3 | 4020 行 ✓ |
| 34 | 34 | 同上（表ID 34 复用） | — | — | — | — |
| 35 | 35 | `msma/msma_rental.csv` | `CCharaParamTable`（同表 4 读取器） | `sub_582390` | 64 | **0 行** ✗ |
| 38 | 38 | `msma/msma_npc_formation.csv` | `CFormationTable` | `sub_577DE0` | 3 | **0 行** ✗ |
| 53 | 61 | `msma/msma_module.csv` | `CMSMAModuleTable` | `sub_57EA90` | 11 | **0 行** ✗（模块要用） |
| 54 | 62 | `msma/msma_breakup.csv` | `CMsmaBreakupTable` | `sub_57BF00` | 6 | **0 行** ✗ |
| 55 | 63 | `msma/msma_flight_settings.csv` | — | — | — | **0 行** ✗ |
| 56 | 64 | `msma/msma_missionunit.csv` | — | — | — | **0 行** ✗ |

**客户端本地（我们不下发，只在 `unpackdat/settings/`）**：
`msma_ui_customize.csv`(102 行) / `msma_visual_customize.csv` / `msma_mesh_customize{,_mesh_id}.csv` /
`msma_mesh_hide_setup{,_mesh_id}.csv` / `weapon_visual_customize.csv` / `favms_ok_list.csv`(**`練度ID,機体名` 700 台**, 唯一的官方日文名册) ✓

---

## §3 ★IDA 定案 A：`msma_model.csv`（表ID 5, CHARA_MODEL）

**读取器 `sub_571380(row=ebp, ?, out=edi)`**（0x571380，596 条指令）——逐 `push <列号>` 提取（★权威）：

| 列号 | 原语 | 落点 | 类型 | 备注 |
|---|---|---|---|---|
| 0 | `sub_BBB3F0` | `edi+0` | **u64** | ★行键 = 練度ID |
| 1–4 | `sub_BBB470` | `edi+8/0C/10/14` | float | |
| 5 | `sub_BBB470` | `edi+1Ch` | float | `edi+18h` = `edi+10h` 的副本（非独立列） |
| 6 | `sub_BBB370` | `edi+20h` | bool | |
| 7–9 | `sub_BBB470` | `edi+24/28/2C` | float | |
| **（跳过 10）** | — | — | — | ★唯一跳过的列 |
| 11 | `sub_BBB470` | `edi+30h` | float | |
| 12–14 | `sub_BBB370` | `edi+34/35/36` | bool | |
| 15 | `sub_BBB470` | `edi+38h` | float | |
| 16–31 | `sub_BBB370` ×16 | `edi+3Ch..78h` | u32 | **2 轮 ×8 列循环**（stride 8 交织布局） |
| **32** | `sub_BBB4F0`→`sub_402310` | `edi+7Ch` | **str** | ★`std::string` |
| **33** | 同上 | `edi+98h` | **str** | ★ |
| **34** | 同上 | `edi+B4h` | **str** | ★ |
| 35 | `sub_BBB370` | `edi+D0h` | byte | |
| **36** | `sub_BBB4F0`→`sub_402310` | `edi+D4h` | **str** | ★ |
| 37–40 | `sub_BBB370` | `edi+F0..FCh` | u32 | |
| 41 | `sub_BBB470` | `edi+100h` | float | |
| 42–43 | `sub_BBB370` | `edi+104/108` | u32 | |
| 44 | `sub_BBB370` | `edi+10Ch` | bool | |
| 45 | `sub_BBB370` | `edi+110h` | u32 | |
| 46 | `sub_BBB470` | `edi+114h` | float | |
| 47–49 | `sub_BBB370` | `edi+118/119/11Ah` | bool | |
| **50** | `sub_BBB4F0`→`sub_402310` | `edi+11Ch` | **str** | ★ |
| **51** | 同上 | `edi+138h` | **str** | ★ |
| **52** | 同上 | `edi+154h` | **str** | ★ |
| 53 | `sub_BBB470` | `edi+170h` | float | |
| 54 | `sub_BBB370` | `edi+174h` | bool | |
| **55** | `sub_BBB4F0`→**`sub_571290`** | `edi+178h` | **enum** | ★查表 `off_D77D38`/`dword_D77D3C` |
| 56–57 | `sub_BBB470` ×2 | 栈 | float | 三元组（+`edi+184h`=0） |
| 58–59 | `sub_BBB470` ×2 | 栈 | float | 同上 |
| 60 | `sub_BBB370` | `edi+194h` | bool | |
| 61–63 | `sub_BBB370` | `edi+198/19C/1A0h` | u32/bool | |
| 64 | `sub_BBB370` | `edi+1A4h` | u16 | ★与 col65 做 `if(65>64) 65=64+1` 归一 |
| 65 | `sub_BBB370` | `edi+1A6h` | u16 | ★同上 |
| 66–67 | `sub_BBB370` | `edi+1A8/1A9h` | bool | `>0` |
| 68 | `sub_BBB370` | `edi+1AAh/1ABh` | bool×2 | `==1` / `==2` 双标志 |
| 69 | `sub_BBB370` | `edi+1ACh` | u32 | |
| 70 | `sub_BBB370` | `edi+1B0h` | bool | `>0` |
| **71** | `sub_BBB370` | **`edi+1B4h`** | **u32** | ★★**モデルID 低 32** |
| **72** | `sub_BBB370` | **`edi+1B8h`** | **u32** | ★★**モデルID 高 32** |
| 73 | `sub_BBB370` | `edi+1C4h` | u32 | |
| 74 | `sub_BBB370` | `edi+1BCh` | u32 | |
| 75 | `sub_BBB370` | `edi+1C8h` | u32 | |
| 76 | `sub_BBB370` | `edi+1C0h` | u32 | |

**⇒ 三条硬结论**：
1. 读取列 = **0..76，只跳过 col10**（76 次读取）✓ —— 与 `formats/README §五·补` 一致，**`datatables/01-列注释/05` 表尾的"52/53 交替"是提取脚本的脏数据** ✗（已作废）。
2. **文本列只有 7 个**：`col32/33/34/36/50/51/52`，且都是**窄串** `std::string`；**枚举列只有 1 个**：`col55`。
   ⇒ `gen_chara_model.py` docstring 说的 `col26/27/28/30/48/49/50 = 枚举(文本类)` **是错的** ✗（那段基于脏表）。
3. **モデルID = col71 + col72<<32** ✓（消费方 `sub_571BF0`，见 §6）。

---

## §4 ★IDA 定案 B：`msma_settings.csv`（表ID 4, CHARA_PARAM）

**读取器 `sub_582390(row, ?, out=a3)`**（0x582390）：

| 列 | 原语 / 转换 | 落点 | 类型 |
|---|---|---|---|
| 0 | `sub_BBB370` | `a3+0` | u32 ★**行键 = 練度ID** |
| 1 | `sub_BBB3F0` | `a3+8` | u64 |
| 2 | `sub_BBB3F0` | `a3+16` | u64 |
| 3 | `sub_BBB370` | `a3+24` | u16 |
| 4 | `sub_BBB4F0`→`sub_580610` | `a3+408` | enum |
| **5** | **`sub_456D90`** | wstring | ★**str（宽）= 名称** |
| **6** | **`sub_456D90`** | wstring | ★**str（宽）= 说明** |
| 7 | `sub_BBB4F0`→`sub_5804F0` | `a3+120` | enum |
| 8 | `sub_BBB4F0`→`sub_580560` | `a3+128` | enum(u64) |
| 9–11 | `sub_BBB370` | `a3+136/140/144` | u32 |
| 13,15–21 | `sub_BBB370` | `a3+840/841` 位图 | bool |
| 22,24–29 | 同上 | `a3+841` | bool |
| 30,32,34 | 同上 | `a3+842` | bool |
| 31 | `sub_BBB370` | `a3+841 bit1` | bool |
| 35 | `sub_BBB4F0`→`sub_5806B0` | `a3+368` | enum |
| 36,37 | `sub_BBB470` | `a3+156/160` | float |
| 38 | `sub_BBB370` | `a3+372` | u32 |
| 42,44,46,47 | `sub_BBB370` | `a3+392/396/400/404` | u32 |
| 48 | `sub_BBB4F0`→`sub_580BA0` | `a3+412` | enum |
| 49 | `sub_BBB4F0`→`sub_580C40` | `a3+416` | enum |
| 50,51,52,54,55 | `sub_BBB370` | `a3+420/424/248/428/432` | u32 |
| **56,58,60,62,64,67,69,71,73,79** | `sub_BBB4F0`→**`sub_402310`** | `a3+436/464/492/520/548/576/604/632/660/688` | ★**str（窄）10 个** |
| **87** | **`sub_456D90`** | wstring | ★**str（宽）文本** |
| 83,85,86,88,89,90,91 | `sub_BBB370` | `a3+252/356/256/32/244/148/152` | u32 |

**⇒ 结论**：
- **宽串列 3 个：col5 / col6 / col87**（`sub_456D90` → `sub_4029E0`，16 位终结符 ⇒ `wstring`）✓
- **窄串列 10 个**：col56/58/60/62/64/67/69/71/73/79（`sub_402310`，单字节终结符）✓
- 枚举列 6 个：col4/7/8/35/48/49 ✓
- 与 `datatables/01-列注释/04` 的"读序→列号"表**部分不符** ⇒ **以本节为准** ✓

---

## §5 ★IDA 定案 C：机库推送 `0xA832 msma_add` = 线上 **303B**

**读取器 `sub_B43570(dst, cursor)`**（0xB43570）——逐段消费，**其消费字节数求和 = 303** ✓（与 `server/internal/protocol/lounge_msma.go::MsmaAddWire` 完全一致）：

```
线上偏移  类型/长度            内存偏移(dst)   说明
+0        u64 (2×dword)      +0 / +4        uniqid
+8        u32                +8             msma_id (練度ID)
+12       u32                +12            tm_sec
+16       u32                +16            tm_usec
+20       u32(sub_B02DD0)    +20            rental_time_limit
+24       61B 定长循环        +24..+84       nickname（★恰好 61 次，无 NUL 检查）
+85       u32                +88 (对齐+3)   energy_now
+89       u32                +92            decal
+93       u8 (sub_B06230)    +96            color
+94       u16                +97            deckslot
+96       u16                +99            is_costover
+98       u32                +104(+3 对齐)  cost          ← ★内存有 4B 对齐填充
+102      u32                +108           mission_cost
+106      3×u32              +112..120      eqweapon_itemid[3]
+118      u32                +124           eqshield_itemid
+122      u32                +128           eqspecial_itemid
+126      10×u32             +132..168      eq_modules[10]
+166      u32                +172           eq_bonus_modules
+170      3×u32              +176..184      eq_bonus_modules_lot[3]
+182      u32                +188           eq_rental_modules
+186      u32                +192           sp_parts
+190      u32                +196           sp_parts_exp
+194      u16                +200           buildup_cnt
+196      7×u16              +202..214      up_param[7]
+210      7×u16              +216..228      up_param_develop[7]
+224      u16                +230           weapon_buildup_extra_cnt
+226      3×u32              +232/236/240   over_custom_exp / level / buildup_cnt
+238      7×u32              +244..268      over_custom_param[7]
+266      7×u32              +272..296      over_custom_count[7]
+294      u16                +300           msbits
+296      u32                +304           unlocked_colors
+300      u8                 +308           spticket_success_ms
+301      u8                 +309           spticket_greatest_ms
+302      u8                 +310           is_favorite
──────────────────────────────────────────────────  Σ = 303 ✓
```

**★关键**：`+85 … +104` 这一段**内存偏移比线上偏移多 3**（`nickname` 61B 后 `u32` 需 4 字节对齐）——
所以**"结构体尺寸(312) ≠ 线上长度(303)"**，写代码必须用**线上偏移**。

**机库三封报文的关系**：
`0x16AC msma_init_get`（C→S，体空）⇒ `0x2ACF`(S→C, begin, 含 `slot_num`) → **N×`0xA832`(303B)** → `0xFCE6`(S→C, end, **空体**)；
★`slot_num` 必须 == 中间推的台数（自洽铁律）。

---

## §6 ★IDA 定案 D：モデルID → 资源目录（`chara/...`）

**链路（全部反查到）**：

```
msma_model 行 (edi+1B4h 低32, edi+1B8h 高32)
   ↓ sub_571BF0(this)                       [0x571BF0]
       v3 = (int*)(this[4] + 24);
       sub_473370(v5);                       // 清零 18B 结果结构
       sub_473390(v5, *v3, v3[1]);           // ★把 u64 键拆成 (kind, u32, u16, u32)
       sub_49D170(v9 /*WCHAR[1024]*/, v5);   // ★wsprintfW 生成路径
       sub_4022D0(v6, v9);                   // ★构造 wstring（= 崩溃取证里的 0x4022D0）
       sub_AEFD80(v6, 1, sub_571A70, v3, 1, 0);  // VFS 打开 + 逐行回调
```

**`sub_49D170` 的两条格式串（0xD6B660 / 0xD6B6A8，已逐字节读出）**：

```
*(BYTE*)解码结果 == 1  ⇒  L"chara/%02d/%03d/%05d/motionlist.csv"
*(BYTE*)解码结果 == 0  ⇒  L"chara/%02d/%02d/%04d/motionlist.csv"
参数 = ( *(u32*)(seg+4), *(u16*)(seg+8), *(u32*)(seg+12) )
```

**⇒ 两条目录规则（新知识）**：
- `kind=0`：`chara/<a>/<b>/<c>/`，宽度 `%02d/%02d/%04d`
- `kind=1`：`chara/<a>/<b>/<c>/`，宽度 **`%02d/%03d/%05d`** ⇒ 这正是 P202 里那 **2 条"13 位号"反例**的来源（**另一套编号体系**）✓

**验算（与 P202 的 40 组真值 38 吻合）**：`101280501` ⇒ `chara/01/01/2805/`；`186280101` ⇒ `chara/01/86/2801/` ✓

**同族模板（同一"chara/<a>/<b>/<c>/"前缀，换文件名）**：
`ara/%02d/%02d/Camera_Hangar.csv`（@`0xE0A13C`）与 `ara/%02d/%02d/%04d/Camera_Hangar.csv`（@`0xE0A184`）——
`ara/` = `chara/` 被截断的表象 ⇒ **进「我的机体」会去开 `chara/<…>/Camera_Hangar.csv`** ✓

---

## §7 机体资源体系（`unpackdat/chara/`）

- 目录结构：`unpackdat/chara/<a>/<b>/<c>/`，内含 `model/`(MSM_*.dxg) `tex/`(MST_*.dds) `attr/`(MSZ_*.vra) `anim/`(MSA_*) ＋
  **`Camera_Hangar.csv` / `Camera_MsSelect.csv` / `motionlist.csv`**（★"整台可用"的硬门槛）
- `.vra` 是**文本**，内含指向 `.dxg`/`.dds` 的**路径引用**（`ms_refs.py::parse_vra` 已实现解析）✓
  ★**引用可能指向别的 unit**（实测 `MSZ_0101_0152_02.vra → chara/01/01/0102/...` 断裂）⇒ 光看"目录在不在"查不出 ✗
- 真值工具：`server/tools/ms_refs.py`（关联文件集 + vra 交叉引用核对）、
  `server/tools/ms_assets_check.py`（完整度体检：两相机 + motionlist + model/tex/attr/anim + vra 全可解析）、
  `datatables/names/模型ID-资源目录对照.csv`（40 组真值）

### 7.5 ★★机库界面类族（RTTI 实证，2026-09-18 新增）

**来源**：`unpacked/shell/data_rt.bin`（= **运行时 `.data` 段全量** 2,612,392B）里含 **3136 个 RTTI 类名**（`.?AV…@@`）
—— ★这是**唯一的"客户端完整类清单"**，比翻 exe 省事得多 ✓（同内容还有 `data_oep.bin` / `data_oep_ok.bin`）

**"我的机体" = `Hangar` 族**（`@IF` = UI 框架命名空间；`@rhyme` = 另一层 UI）：

| 类 | 作用 | 与我们下发数据的关联 |
|---|---|---|
| `CHangarPageCtrl@IF` | ★**页面控制器（主窗口）** | 进界面就建 ⇒ **崩点最可能在这条链上** |
| `CHangarCharaList` / `CHangarCharaInventory` / `CHangarCharaInventorySlot` | ★**机体列表 / 列表项** | 列表项渲染要读**机库记录字段** |
| `CHangarNamePlate` / `CHangarIcon` / `CHangarCharaIcon` | 名称牌 / 图标 | ⇒ `nickname`（**我们发空串** ✗）/ 图标 id |
| `CHangarCharaEnergy` / `CHangarCharaEnergyGauge` | 能量 / 能量条 | ⇒ `energy_now`（**我们发 0** ✗） |
| `CHangarCharaProperty` / `…PropertyOverCustom` / `CHangarCharaBuildupParameter` | 属性 / 超改造 / 强化参数 | ⇒ `up_param` / `over_custom_*`（**全 0** ✗） |
| `CHangarCharaDetailWindow` / `…DetailStatus` / `CMsmaSpec*` | 机体详情 | ⇒ 各数值列（表空 ✗） |
| `CHangarCharaCustomWeponWindow` / `…CustomModuleWindow` / `…CustomEquipSetWindow` | 武器 / 模块 / 装备集 | ⇒ `eqweapon` ✓（已填）/ `msma_module`（**0 行** ✗）/ equipset |
| `CHangarBreakupWindow` / `…BreakupDialog` ＋ `CMsmaBreakupTable` | 解体 | ⇒ `msma_breakup.csv`（**0 行** ✗） |
| `CHangarMechanicSelect` | 整备士选择 | ⇒ `develop/mechanic_*.csv`（**0 行** ✗） |
| `CHangarCharaSelectWindow` / `…DeckCharaSelectList` / `…AllCharaSelectList` | 机体选择 | ⇒ 编成槽 |
| `CMsDeckList` / `CMsSetChangeItem` / `CHangarDeckCharaSelectList` | 编成 | ⇒ `deckslot` |
| `CHangarWeaponSlotButton` / `CHangarEmblemColorIcon` / `CHangarUseDataSlot` / `CHangarUpdateResult` | 槽位 / 徽章 / 数据槽 | — |
| `Hangar@script` | 脚本层 | — |

**核心管理器**：`CMsmaMgr@msma`（机体数据总管）
**表类（★与下发表 / 本地 customize 表一一对应）**：`CMsmaMeshHideSetupTable` / `CMsmaMeshCustomizeTable` / `CMsmaMaterialTable` / `CMsmaFavmsTable` / `CMsmaBreakupTable` / `CMsmaPlanTable` / `CMsmaMissionUnitTable` / `CMsmaAdopTable` / `CLvupMsmaTable`
**商店族**：`CShopMs_MsWindow` / `…_BaseWindow` / `…_MaterialWindow` / `…_PartsWindow` / `…_PlanWindow` / `…_UseItemWindow` / `CShopRecycl_MsWindow` / `CMsmaSpecWindow`

**⇒ 直接推出的「进界面必读字段」清单**（机库记录 303B 内）：
`nickname`(名称牌) ｜ `msma_id`(查名/图标) ｜ `energy_now`(能量条) ｜ `cost`+`is_costover` ｜ `decal` ｜ `color`+`unlocked_colors` ｜ `deckslot` ｜ `eq_*`(武器 ✓ 已填) ｜ `up_param` ｜ `over_custom_*` ｜ `msbits`

⇒ **服务端目前仍留 0 的**：`nickname`(空) / `energy_now` / `decal` / `color` / `unlocked_colors` / `mission_cost` / `eq_modules` / `eq_bonus_*` / `sp_parts*` / `buildup_cnt` / `up_param` / `over_custom_*` / `msbits` / `spticket_*`
⇒ **其中"名称牌 + 能量条"是列表项上**肉眼可见**的元素** ⇒ 优先补 `nickname`（真值 = `msma_settings.col5` 机体名）与 `energy_now` ✓

### 7.6 ★★★「ID ↔ 目录 ↔ 资源文件」权威映射（**既有答案，2026-09-18 归集**）

> 用户澄清：① **`unpackdat/` 就是 `data/*.hed+*.dat` 的解包树** ⇒ **搜 `unpackdat` == 搜归档内容** ✓
> （所以"`unpackdat` 里没有"就等于"客户端读不到" ✓；此前"解包树≠归档"的说法作废 ✗）
> ② 这套对应关系**早有答案**，且 `viewer/` 能把机体资源关联起来 ⇒ 本节即归集结果，**下次别再重新推** ✓

#### 7.6.1 规则（两份实测表互相印证 ✓）

```
モデルID(9 位) = A(类型 1) * 1e8 + B(系列 2) * 1e6 + C(机体 4) * 100 + NN(形态 2)
A 枚举：0/1 = MS(MSZ) ｜ 2 = MA(MAZ) ｜ 3 = BS(BSZ) ｜ 4 = VE(VEZ) ｜ 5 = PL(PLZ) ｜ 6/7 = BA(BAZ)
资源目录 = chara/01/<B>/<C>/          ← ★第 1 段固定 01（不是 A）
模型文件 = chara/01/<B>/<C>/model/MSM_01<B>_<C>_<NN>.dxg
依据：客户端 sub_49D030（拼 chara 路径，按 A 选前缀 MSZ_/MAZ_/BSZ_/VEZ_/PLZ_/BAZ_）+ sub_473390（十进制拆位）
```

**验算（实测目录均存在 ✓）**

| モデルID | A / B / C / NN | 资源目录 | 模型文件 |
|---|---|---|---|
| `101010101` | 01/01/0101/01 | `chara/01/01/0101` | `MSM_0101_0101_01.dxg` |
| `101280101` | 01/01/2801/01 | `chara/01/01/2801` | `MSM_0101_2801_01.dxg` |
| `186280101` | 01/86/2801/01 | `chara/01/86/2801` | `MSM_0186_2801_01.dxg` |
| `184300101` | 01/84/3001/01 | `chara/01/84/3001` | `MSM_0184_3001_01.dxg` |
| **`101286001`（我们的 1124102）** | 01/01/2860/01 | **`chara/01/01/2860`** ✓ | `MSM_0101_2860_01.dxg` |

★ 三段模板 `chara/%02d/%02d/%04d/` 的参数 = **(A, B, C)** ✓（与 §6 的 IDA 反查完全一致 ✓）
★ 与 `msma_settings.col1` / `msma_model.col71(低32)+col72(高32)` **同一套编号** ✓
★ **`chara/00/...` 不是合法坐标**（A 无 0 ⇒ 第 1 段恒 01；实测 `unpackdat/chara/` 顶层 = `01 02 03 05 06 07`，**无 00**）✓

#### 7.6.2 权威数据文件（直接用，别重造）

| 文件 | 内容 | 规模 |
|---|---|---|
| **`datatables/names/chara目录-ID清单.csv`** ★★★ | **モデルID / A / B / C / NN / 资源目录 / 模型文件 / 同目录形态数 / 同目录网格数** —— **"ID↔目录↔文件"总表** | **1650 行** |
| `datatables/names/模型ID-资源目录对照.csv` | モデルID / 机体名 / 资源目录 / 模型文件 / 同目录模型数 / 来源表（42 条，来自本地 UI 表） | 44 行 |
| `datatables/chara/chara_model_ids.csv` | 资源树里**含 `model/` 的合法坐标**（工具 `analyze_chara_tree.py` 导出） | — |
| `datatables/names/模型号映射-*.csv`（初版/自动/人工/补充/合并） | 練度ID ↔ モデルID ↔ 机体名 ↔ 来源（精确/模糊/人工） | 合并 112 行 |
| `datatables/chara/README.md` | 机制定案全过程（⚠️ §1.3/§1.4 的 `1\|28\|0101` 举例与两份实测表**冲突**，**以 `chara目录-ID清单.csv` 为准** ✓） | — |
| `datatables/chara/find_model_id_rule.py` / `analyze_chara_tree.py` / `test_fill_model.py` | 规则推导 / 树分析 / 试填测值 | — |

#### 7.6.3 资源树实测规模（`unpackdat/chara/`）

```
目录总数            5334
含 model/ 的合法坐标 1025   （叶子 4 位 1000 个 + 5 位 25 个）
第 1 段分布         01:690  02:41  03:72  05:25  06:156  07:41   （★无 00）
motionlist.csv      873 个目录
Camera_Hangar.csv   256 个目录   ← 与"完整机体 256 台"吻合
Camera_MsSelect.csv 265 个目录
```

#### 7.6.4 两套编号（**绝不能混**）

```
練度ID  (7 位, 如 1107011 / 1124102)  = 表主键 / 行键 / 服务端 DB msma_id
モデルID (9 位, 如 101286001)         = 资源坐标（本节规则）
★favms_ok_list.csv（709 行）只有「練度ID + 日文名」，**不含モデルID**
★两者共现的文件：从未有过（逐文件搜过）⇒ 逐机映射只能"重建"（看图识机 最可靠）
```

#### 7.6.5 `viewer/`（把机体资源关联起来的那个查看器）

- 位置：`viewer/`（源码）＋ `viewer.zip`（5.39 MB 打包版）；**C++17 + DirectXTex + d3d9 + WIC**
- 组成：`src/main.cpp`（入口）｜`fpmf.cpp`（**读 FPMF 归档 `.hed/.dat`**）｜`dxg.cpp`（模型）｜`vra_text.cpp`（`.vra` 文本）｜
  `anim.cpp`（动画）｜`image_io.cpp`（DDS/TGA）｜`preview3d.cpp`（3D 预览）｜`text_encoding.h`
- 构建：`cmake -S viewer -B viewer/build -A x64` → `--build --config Release`
- **它"关联机体资源"靠的就是 7.6.1 那条规则**（モデルID → `chara/01/<B>/<C>/` → `model/ MSM_*.dxg` + `tex/ MST_*.dds` + `attr/ MSZ_*.vra`）✓
- ★**看图识机**（`datatables/chara/README §4.6`）：**图标文件名与打包值同构**
  `interface/icon/item/d/d0<A><BB><CCCC><NN>.dds`（大图）／`s0<A><BB><CCCC><NN>.dds`（小图）／
  `interface/icon/color/c0<A><BB><CCCC><NN>_<NNN>.dds`（配色，2617 个）
  ⇒ 工具 `python datatables/make_unit_icon_sheet.py out.png --series 0101 [--all]` ⇒ **每个 chara 目录都能取到自己的图标** ✓

#### 7.6.6 ★当前 bug 现状（与本节的关系）

- 客户端反复打开 **`chara/00/01/<4 位>/motionlist.csv`**（30+ 项、间隔 72B 的队列、还在增长）
- 实测该批目录（2230/2380/2400/2130/2300/2350/2460/2220/2470/2480/2090/2152/2080/2310/2381/2100）
  ⇒ **`unpackdat/chara/` 里全部不存在** ✗（且第 1 段 `00` 本身就不是合法坐标）
- 反查来源 ⇒ **全部落空**：下发的 13 张 `msma/*.csv` 全表 **0 命中**；`favms_ok_list.csv` 后 4 位也只 **1 条**命中
- ⚠️ **来源待定** ⇒ 下一步：IDA 反查 **`sub_571BF0` 的 `this[4]+24` 到底是哪张表的哪个字段**（它就是把路径入队的那个函数，§6）

#### 7.6.7 ★★★★根因定案 + 已实施修法（2026-09-18，P219）

**铁证（IDA 反编译 `0x571BF0` = `CCharaTable` 的逐行回调）**：
```c
bool sub_571BF0(_DWORD *this) {
  v1 = this[4]; if (v1 == this[2]) return 0;
  v3 = (int*)(v1 + 24);                  // 红黑树节点数据区
  sub_5711C0();                          // 迭代器 next
  if (v3[117]) return 0;                 // 某标志列 ≠0 ⇒ 跳过
  sub_473390(v5, *v3, v3[1]);            // ★★用**行首 8 字节（= col0）**当モデルID 拆位
  sub_49D170(v9, v5);                    // wsprintfW("chara/%02d/%02d/%04d/…")
  sub_4022D0(v6, v9);                    // wstring（= §8.2 的 wcslen 崩点）
  sub_AEFD80(v6, 1, sub_571A70, v3, 1, 0);  // 打开文件
}
```

**⇒ `msma_model.csv` 的 col0 必须是「モデルID（9 位打包值）」，不是「練度ID」** ✓

- 我们原先 col0 = 練度ID（7 位）⇒ 客户端补零成 9 位后按 `A|B|C|NN` 切：
  `1124102` → `001124102` → A=0,B=01,C=1241 ✗ ；`1223011` → `001223011` → **A=0,B=01,C=2230** ⇒ 请求 `chara/00/01/2230/motionlist.csv` ✓（**与实测内存队列逐字吻合** ✓）
- 实测佐证：那批号的来源 = **`col0[1:5]`**，**41 条命中** ✓（`1223011→2230`、`1235011→2350`、`1210011→2100`、`1208012→2080` …）
- ⇒ **696 行全部请求失败** ⇒ DLIB 无限重试 ⇒ **内存 1.02 GB 卡死** ✓✓✓

**已实施修法（数据改动，零服务端风险 ✓）**
1. 备份：`msma_model.csv.bak_p219`（59681 B）
2. 重写为 **1 行数据**：`101286001,` + 72 空列（**col0 = モデルID** ✓）⇒ 客户端只请求 `chara/01/01/2860/motionlist.csv`（**实测存在** ✓）
   —— 与用户既定策略「**先做好一台就下发一台**」一致 ✓
3. ★**服务端无需重启**：`datafiles` 的 `Get(filepath)` **故意不缓存**（改表立即生效）✓
4. ⚠️ 副作用：本表不再是"练度ID→モデルID"索引 ⇒ `ms_refs.py` / `ms_assets_check.py` 的按-col0 索引失效
   （该映射改看 `msma_settings.csv` 的 col0（練度ID）/ col1（モデルID）✓）
5. ⚠️ 待验证：若**仍卡**，说明还有别的来源（`msma_settings` / `msma_weapon_set` 的 col0 同为零度ID ⇒ 需逐个排除）

---

## §8 ★「我的机体」崩溃：全部证据与当前结论

### 8.1 现象（用户口径，"点进去就崩"）
- 客户端：`user\exrep.log` 每次崩写一条 `时间,0,,0xc0000005,0` + 第二行 `0x8` ✓
- 服务端：`0x6B74 bugtrace_report`（体长**不固定**：20B / 216B）——216B 版头部带**崩溃 EIP** ✓

### 8.2 两型并存（已分别取证）
| 型 | 取证 | 语义 |
|---|---|---|
| (a) 内存暴涨卡死 | `%LOCALAPPDATA%\CrashDumps\*.dmp` ×8：`0xC0000005`，eip `xxxx8D71`（**低 16 位恒 8D71**），被访问 `0x94`，`ecx=4` | 假对象（值=4）当指针 ⇒ 列表/容器没建好 ⇒ 排版取位时崩 |
| (b) `wcslen(NULL)` | 216B 遗书：崩溃 EIP `0x004022F1` = `sub_4022D0` 内联 `while(*p)p++` | 传入**坏的宽字符串指针** |
| (c) 资源重试 | `XDt` 日志 `DLIB-DLOADER 61697` / `DLIB 61709` ×万 / `uncompress fail(-3)` | 客户端开某资源失败 ⇒ **无限重试** ⇒ 涨到 ~1GB ⇒ 卡死 |

`sub_4022D0`（0x4022D0）**唯一语义**：`wstring::wstring(this, const wchar_t* a2) { …; sub_402AD0(a2, wcslen(a2)); }` ✓
`wcslen` 循环体 = `0x4022F1`（`mov cx,[eax] / add eax,2 / test / jnz`）✓ —— 与遗书 EIP 逐字吻合 ✓

### 8.3 ★本轮 IDA 新增的两条判定
1. **CSV 空列 ≠ NULL**：`sub_BBB4F0`（窄串）与 `sub_456D90`（宽串）在**列越界/无数据**时都构造**空串** ✓
   ⇒ "我们下发的表有空列 ⇒ 客户端 `wcslen(NULL)`" **不成立** ✗（详见 §10）。
2. **崩点确有真实调用者且就在机体链上**：`sub_4022D0` ← `sub_571BF0` ← `sub_A86C90` ← `sub_A86D70`，
   而 `sub_571BF0` 正是"**按モデルID 逐台打开 `chara/<…>/motionlist.csv`**" ✓
   ⇒ 方向（机体资源链）对，但**坏指针不是从这张表来的**（此处传的是栈上 1024 宽字符缓冲，恒非 NULL）。

### 8.4 已被实测排除的方向（别重走）
- ✗ 空机库 / 机库台数（诊断开关 `chDiagNoDeck`/`chDiagNoGarage` 都证明"空机库也卡"）
- ✗ 机库记录里的装备槽全 0（P211 已修：改为与出击同源的 `msma_weapon_set` 真值）
- ✗ 客户端文件损坏（`list/filelist.dat` 的 Size+SHA1 全对，1556 个 `data/*.dat` 0 缺失）
- ✗ `0x5290` 表下发压缩方式（我们发的是 `CompressNone`）
- ✗ XDt 日志里的数字（是**消息 ID**，不是资源 id；日志**不含文件名**）
- ✗ `str_table.txt` 里查机体名（机体 id 在里面查不到）

### 8.5 ★★★（2026-09-18 新增）崩点代码**已定位** —— 运行时内存取证法（**完全不需要断点**）

> 由用户提示「查壳/反外挂之前有 dump 下来」走通 ✓；正面解决"在通用函数上下断点没意义"的问题 ✓

**① 崩点代码的性质**
- 8 份 dmp 的 `eip` 形如 `0x04998D71 / 0x048E8D71 / 0x04B38D71 …` ⇒ **低 16 位恒 `8D71`、高位每次不同**
  ⇒ = **运行时解密/手工映射的代码 + 64KB 对齐基址**（"模块基址 + 固定偏移"）✓
- 该区**整体不在静态映像里**（IDB 最高 VA `0x12CF000`，崩点 ≈`0x04A58D71`）⇒ 静态 `find_bytes` 必然落空 ✗
  （全扫 `unpacked/shell/**/*.bin`（179 个，含壳的解密 blocks）＋所有 `*.exe/*.dll` ⇒ **只有 `.data` 段的巧合命中** ✗）

**② 定位过程与结果（本次运行）**
```
memory_enumerate  ⇒ 0x04A30000  PAGE_READWRITE  880640B   ← 大块 RW = 运行时解密区
dump_memory_region 0x04A30000 880640 (as_raw_binary) ⇒ server/logs/memdump/rt_04A30000.bin
在落盘文件里 find 崩点签名  8B 81 90 00 00 00 83 C0 01 99 F7 B9 98 00 00 00
   ⇒ 命中偏移 0x28D71 ⇒ 低 16 位 = 0x8D71 ✓✓（与 dmp 的 eip 特征逐字吻合）
   ⇒ 崩点 VA = 0x04A30000 + 0x28D71 = 0x04A58D71
```
- 该区含 **212 处 `VMProtect` 标记**；字符串常量 **`DLIB`**（`0x04A86E44`）／**`XGGLib: Enres fail`**（`0x04A81644`，旁有 STL 断言串 `bad cast`/`map/set<T> too long`）
  ⇒ ⇒ **这片区 = DLIB（资源加载器）+ XGGLib（反外挂库）的运行时解密实现** ✓
- ★**修正 P205 的判定** ✗：不是"Themida VM 里的反外挂模块"，而是 **VMProtect 保护的 DLIB / XGGLib 代码区**（两者同区）✓
  ⇒ 与客户端日志 `DLIB-DLOADER 61697` / `DLIB 61709` **同源** ✓

**③ 崩点函数语义（实时反汇编，入口 `0x04A58D70`；`0x68~0x6F` 是 `CC` 填充）**
```
bool Pop(void* out8)              ; __thiscall，this = ecx，retn 4
  eax = [ecx+0x90]                ; ★head（崩点：ecx = 4 ⇒ 读 4+0x90 = 0x94 ⇒ AV）
  head = (head + 1) % [ecx+0x98]  ; ★cap（idiv）
  if ([ecx+0x90] == [ecx+0x94]) return 0;        ; ★head == tail ⇒ 空队列
  *(u32*)out8     = [ecx + i*8]                  ; ★元素 8B（两个 dword）
  *((u32*)out8+1) = [ecx + i*8 + 4]
  [ecx+0x90] = head; return 1
```
⇒ **环形队列（ring buffer）的 `Pop`**：`+0x90`=读索引、`+0x94`=写索引、`+0x98`=容量、`[ecx+i*8]`=8B 元素数组 ✓
⇒ **崩因 = 调用者把一个"值 = 4 的垃圾对象指针"当成队列去 Pop** ✓（与 §8.2(a) 的 `ecx=4 / 读 0x94` 逐字吻合 ✓）

**④ 调用者（离线扫出）**
- **`Pop` 的唯一调用点 = `0x04A58E99`**（同区，位于 `0x04A58E4C` 之后的函数里）
- ★**搜法**：`Pop` 的地址在内存里 **4 字节引用 = 0 命中**（不在任何 vtable、无 `mov eax,offset`）⇒ 只能扫
  **`E8 rel32` 且 `next_ip + rel32 == 目标`** ✓
  （★**比"搜地址引用"有效得多** —— 对直接调用两者差别是"0 命中" vs "命中" ✗/✓）
- 同区还有 `0x04A58D00`（被 5 处调用）等**兄弟方法**，属同一类的接口簇

**⑤ 该类的骨架（供继续追）**
- vtable **`0x04A86D3C`**（= dump 偏移 `0x56D3C`；12+ 槽，全部指向本区）：
  slot0 `0x04A58DE0` = **标量析构**（重置 vtable + `operator delete`）｜slot9 `0x04A58E10` = 取值包装（`retn 0Ch`）
- 写该 vtable 的**构造函数**在 `0x04A5A0F4` 附近（`C7 06 3C 6D A8 04`），其上下文还 `push 0x4A86E44` / `0x4A81644`（= `DLIB` / `XGGLib` 串）
  ⇒ **该类属 DLIB / XGGLib 体系** ✓

**⑥ ★方法论（本次最大收获；建议并入 `topics/20-客户端崩溃取证SOP.md`）**
> 崩点落在**保护/解密代码**里时的标准打法：
1. 看 dmp 的 `eip`：**低 16 位是否恒定** ⇒ 恒 ⇒ "区块基址 64KB 对齐 + 固定偏移" ✓
2. **客户端活着时**（**不必复现崩溃、不必下任何断点**）：`memory_enumerate` ⇒ 找大块 `PAGE_READWRITE` ⇒
   `dump_memory_region(as_raw_binary)` ⇒ 整片落盘
3. 落盘文件里 `find` **崩点签名字节**（取自 dmp 的"崩溃处字节"）⇒ 偏移即 RVA ⇒ `VA = 区基址 + 偏移` ✓
4. `disassembly_at` 读**实时**反汇编 / `disassembly_function` 取整函数（dump 与实时可互证 ✓）
5. **找调用者 = 扫 `E8 rel32`**（不是搜"4 字节地址引用"）✓
6. **认区身份 = dump 里的字符串常量**（`DLIB` / `XGGLib` / `VMProtect` / STL 断言串）✓
> ★最大价值：**完全绕开"在通用函数上下断点"的困境** ✓ —— 用户指出的 `sub_4022D0` 命中问题，用此法**根本不会出现**

### 8.6 下一步（按性价比，2026-09-18 更新）
0. ★**已实施（待用户验证）**：机库记录 `nickname`（61B 定长）**由空串改为真机名**（`msma_settings.csv` col5，UTF-8）——
   ＋新增 `datafiles/charaparam.go`（`ParseCharaParams` / `CharaParams`）与 `(*Server).msNames()`；
   `go build` / `go test ./internal/...` **全绿** ✓；`gate.exe` 已重编译重启（PID 34772）✓
   ⇒ 判读：**能进 + 显示日文名** = 根因就是它 ✓ ／ **乱码** = 编码要换 CP932 ✓ ／ **仍崩** = 与此无关 ⇒ 走第 1 条 ✗
1. **沿 DLIB 队列线继续**：反汇编 `0x04A58E99` 所在函数 ⇒ 看"Pop 出来的 8B 元素怎么用"、"谁在什么条件下调它"
   ⇒ 反推"哪个队列对象为 0/4"。`rt_04A30000.bin` **已落盘 ⇒ 可离线反复分析，不需要客户端在场** ✓
2. **抓 `0x6B74` 的 216B 版**（服务端日志已放宽到 256B）⇒ 与本法交叉印证 EIP；
3. **补齐空表**（§2 里 8 张 0 行表）—— 特别是 `msma_color_set`(配色) / `msma_module`(模块)：
   "我的机体"里改配色/装模块必然要它们（数据来源待定，**按铁律先不猜** ✗）。
4. ~~在 `sub_4022D0` 下断点~~ ⇒ **已证伪该思路** ✗（通用函数 200+ 调用者 + 坏指针非小值 ⇒ 条件筛选天然失效）

---

## §9 待验证（明确列出，避免以后又"以为解了"）

1. `sub_473390` 对 9 位モデルID 的**精确分段**（除法常量已见 `232/100/1000/10000/100000/1000000/100000000/1000000000`，但 `kind` 的判据分支未逐条验算）；
2. `kind=1`（`%03d/%05d`）对应的是哪一类资源（与"13 位号"是否同一体系）；
3. `msma_settings.col1`（如 `124120101`）的**正名与用途**（现只知对应 `interface/icon/color/c0<id>_00N.dds`）；
4. `msma_battle_detail`（3 列 str×2 enum×1）的**两个字符串列**语义（表 4020 行，战中要用）；
5. `msma_weapon_set` 的 `enum×3`（读序 2/3/14 → col4/5/19）是否有**文本列**（若为 enum 则写名称串）。

---

## §10 ★被推翻 / 需修正的旧结论（本轮 IDA 反查直接结果）

| 旧结论（出处） | 判定 | 证据 |
|---|---|---|
| `msma_model.csv` 的 `col26/27/28/30/48/49/50` 是"枚举（文本类）"，空列会导致 `wcslen(NULL)`（P214 / `gen_chara_model.py` docstring） | **✗ 错** | `sub_571380` 里 col16..31 **全部**是 `sub_BBB370`(u32)；文本列只有 col32/33/34/36/50/51/52，且是窄串；空列回空串非 NULL |
| `msma_model.csv` 应 ≥77 列（"读 col0..76"） | **✓ 对**（但"73 列"其实**不致命**：越界列读作 0/空串，不报错） | `sub_BBB4F0` 越界分支 |
| `datatables/01-列注释/05` 表尾"读序 47..52 = col52/53 交替" | **✗ 脏数据**（提取脚本未解开循环） | 反汇编 `push` 常量序列 |
| "`sub_473390` 解码资源路径" | **✓ 部分对**：它只做**数值分段**；真正拼路径的是 `sub_49D170`(wsprintfW) | 两者反编译 |
| "资源目录规则 = `chara/01/{v[1:3]}/{v[3:7]}`"（P202 反推） | **✓ 与 IDA 吻合**（`%02d/%02d/%04d`），并**新增** kind=1 的 `%02d/%03d/%05d` | 格式串逐字节 |

---

## §11 常用命令

```powershell
# 机体资源完整度体检（两相机+motionlist+model/tex/attr/anim+vra 引用）
python server\tools\ms_assets_check.py
# 单台机体的关联文件与 vra 交叉引用
python server\tools\ms_refs.py 1107011
# 机体总表（練度ID,日文名,中文名,cx_type,cx_faction,cx_terrain…）
type datatables\names\机体总表.csv
# 官方日文名册（700 台，唯一真源）
type unpackdat\settings\favms_ok_list.csv
# 客户端崩溃取证 SOP（先读）
type .codebuddy\memory\topics\20-客户端崩溃取证SOP.md
python reverse-login-chain\tools\dmp_analyze.py --all
```
