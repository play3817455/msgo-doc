# CHARA_PARAM ｜ `msma/msma_settings.csv`

- **用途（已定案）**：★**机体参数主表**（机体主数值 / 类别 / 名称 / 说明 / 各种开关位）。
- 资源对应：`chara/`（118230 个文件：模型/贴图）
- 表ID `4` ｜ 下载序 `4` ｜ 类名 `CCharaParamTable` ｜ 全局 `dword_11E3F14` ｜ ctor `sub_A72930` ｜ 派生 vtable `0xecfbf0`
- 逐列读取函数 `sub_582390` ｜ **列数 64**（CSV 位置 0..91）

> ★★ **2026-09-18 IDA 复核（权威；全文 `reverse-login-chain/detail/M01-机体数据知识库-IDA定案.md §4`）**：
> ① **宽字符串列（`wstring`，`sub_456D90` → `sub_4029E0`）= col5 / col6 / col87**
>    —— col5 = **名称**、col6 = **说明**、col87 = **文本** ✓（16 位终结符 ⇒ 客户端内部是宽串）；
> ② **窄字符串列（`std::string`，`sub_BBB4F0` → `sub_402310`）= col56 / 58 / 60 / 62 / 64 / 67 / 69 / 71 / 73 / 79**（10 个）✓；
> ③ **枚举列（`sub_BBB4F0` + 转换函数）= col4 / 7 / 8 / 35 / 48 / 49**（`sub_580610` / `5804F0` / `580560` / `5806B0` / `580BA0` / `580C40`）；
> ④ 开关位散在 `+840/+841/+842` 三字节位图（col13/15..22/24..29/30/31/32/34）。
> ⇒ 下表「读序 → 列号」在后半段有偏差（**列号以本节为准**）；★col5 **必须填真值**（名称）。

---

## 0. 本次填充（2026-09-14，`有内容` 层）

- **产物**：`server/datafiles/msma_msma_settings.csv`（**696 行**）｜生成器 `datatables/gen_chara_param.py`
- 已填 **2 列**（其余留空 = 0）：

| 列 | 值 | 来源（真实、可追溯） |
|---|---|---|
| `col0` | 模型ID = **練度ID**（696 个唯一键） | `unpackdat/settings/favms_ok_list.csv` |
| `col5` | **名称**（str，日文原名） | 同上（`装甲強化型ジム` / `ジム・ライトアーマー` / …） |

- **键序列**与 `msma_model.csv` / `msma_weapon_set.csv` **完全一致**（696，脚本判过）。

## 0.1 ⛔ 双阻塞：为什么数值列一个都没填

| 阻塞 | 证据 | 解锁路线（建议） |
|---|---|---|
| **① 列 ↔ 语义 绑定未证实** | UI 文本**不在 exe**（在 `unpackdat/settings/str_table.txt`，UTF-16LE，5559 行）⇒ 无法用标签串反查列；129 条 `MS_*` 机体属性枚举（`sub_5953B0`，值 100..354/1000+）的**值表 `dword_D7D15C` 只被转换函数自己引用**（xrefs 仅 2 处，都在 `sub_5953B0` 内）⇒ **不存在"属性ID → 行偏移"的中枢表** | 用 `str_table.txt` 里的**参数名文本**（如"装甲/推进/载重"）+ 引用这些 string_id 的代码，反查显示函数读了哪些偏移；或对 `sub_582390` 的每个列偏移做**使用者溯源**（`+136/+140/+144/+392..+432` 等）。**`+372` 已于 2026-09-28 结案**（= col38 武器组ID，见下表 §1 第 38 行） |
| **② 数值无桥（codex 落不到机体上）** | `codex/data/units.json`（699 台）机体名是**中文**（`吉姆Ⅲ`/`高机动型格鲁古古(尤玛机)`），机体名册是**日文**（`ジム`/`ゲルググ`）⇒ 名称交集仅 **2/699**；`units.js` 也无日文名/日文 id 字段 | 建一张 **「codex 页面名 ↔ 日文机体名」对照表**（699 行，人工/半自动）；或改从**服务端下发快照**取数（如 `XDt/` 日志，见 `02-资料源.md §D`） |

⇒ 按项目铁律「**不许把推断伪装成结论**」，本次**不猜数值**。`gen_chara_param.py` 已把"列 ↔ 来源"解耦，解锁后在脚本里登记映射即可重跑。


## 1.2 Round 7 IDA 深搜（2026-09-21）

> F6 ?? 48/49/4A 全二进制扫描：+840 仅 bit0/1/4 有 consumer；+841 仅 bit1/2/3/6；+842 bit0/2/3。
> 无 consumer 的 CSV 位 → `cap_flag_reserved_*`（confirmed ○ASM）；+392/+400 区段 → 机库/商店 UI consumer。
| 内存偏移 | bit | CSV col | db_column | 能力名 | consumer | status |
|---|---:|---:|---|---|---|---|
| +840 | 0 | 13 | cap_flag_transform_alt | 变换备用武装 | sub_49D280 | confirmed |
| +840 | 1 | 15 | cap_flag_melee_chain | 近战连锁 | sub_4A7B10 | confirmed |
| +840 | 2 | 16 | cap_flag_reserved_b840_2 | （CSV 预留） | sub_582390 write only | confirmed |
| +840 | 3 | 17 | cap_flag_reserved_b840_3 | （CSV 预留） | sub_582390 write only | confirmed |
| +840 | 4 | 18 | cap_flag_mission_transform | 任务变形态 | sub_477C10, sub_67FEB0 | confirmed |
| +840 | 5 | 19 | cap_flag_reserved_b840_5 | （CSV 预留） | sub_582390 write only | confirmed |
| +840 | 6 | 20 | cap_flag_reserved_b840_6 | 物理积分旁路 | 582390→47D230→4AE900 | confirmed |
| +840 | 7 | 21 | cap_flag_reserved_b840_7 | （CSV 预留） | sub_582390 write only | confirmed |
| +841 | 0 | 22 | cap_flag_reserved_b841_0 | （CSV 预留） | sub_582390 write only | confirmed |
| +841 | 1 | 31 | cap_flag_dual_slot_ui | 双槽切换UI | sub_7E7600, sub_7E4A50 | confirmed |
| +841 | 2 | 24 | cap_flag_skip_ex_anim | 跳过EX演出 | sub_7E7600 | confirmed |
| +841 | 3 | 25 | cap_flag_shield_equip | 盾牌装备 | sub_474480, sub_48FF00 | confirmed |
| +841 | 4 | 26 | cap_flag_reserved_b841_4 | （CSV 预留） | sub_582390 write only | confirmed |
| +841 | 5 | 27 | cap_flag_reserved_b841_5 | （CSV 预留） | sub_582390 write only | confirmed |
| +841 | 6 | 28 | cap_flag_tender_mode | 工作舰模式 | sub_478DA0, sub_507810 | confirmed |
| +841 | 7 | 29 | cap_flag_reserved_b841_7 | 位置碰撞更新旁路 | 582390→478DD0→4AE900 | confirmed |
| +842 | 0 | 30 | cap_flag_disable_special | 禁止特殊行动 | sub_4E7FF0, sub_4EF710 | confirmed |
| +842 | 1 | 32 | cap_flag_dual_mode | 双模式标志 | sub_6218F0 | confirmed |
| +842 | 2 | 33(gap) | — | （强制清零） | sub_582390 epilogue | gap |
| +842 | 3 | 34 | cap_flag_no_awakening | 禁止觉醒爆发 | sub_4EC960 | confirmed |
| +842 | 4–7 | — | — | （未知） | — | — |

**confirmed 47→64**（+17）；partial 17→0；gap 28 不变。

## 1.1 Round 6 IDA 能力位定案（2026-09-21）

> 读表 `sub_582390`；能力位散在 +840/+841/+842 三字节位图。

| 内存偏移 | bit | CSV col | db_column | 能力名 | consumer | status |
|---|---:|---:|---|---|---|---|
| +840 | 0 | 13 | cap_flag_transform_alt | 变换备用武装 | sub_49D280 | confirmed |
| +840 | 1 | 15 | cap_flag_melee_chain | 近战连锁 | sub_4A7B10 | confirmed |
| +840 | 2 | 16 | cap_flag_b840_2 | （未知） | — | partial |
| +840 | 3 | 17 | cap_flag_b840_3 | （未知） | — | partial |
| +840 | 4 | 18 | cap_flag_mission_transform | 任务变形态 | sub_477C10, sub_67FEB0 | confirmed |
| +840 | 5 | 19 | cap_flag_b840_5 | （未知） | — | partial |
| +840 | 6 | 20 | cap_flag_b840_6 | 物理积分旁路 | 582390→47D230→4AE900 | confirmed |
| +840 | 7 | 21 | cap_flag_b840_7 | （未知） | — | partial |
| +841 | 0 | 22 | cap_flag_b841_0 | （未知） | — | partial |
| +841 | 1 | 31 | cap_flag_dual_slot_ui | 双槽切换UI | sub_7E7600, sub_7E4A50 | confirmed |
| +841 | 2 | 24 | cap_flag_skip_ex_anim | 跳过EX演出 | sub_7E7600 | confirmed |
| +841 | 3 | 25 | cap_flag_shield_equip | 盾牌装备 | sub_474480, sub_48FF00 | confirmed |
| +841 | 4 | 26 | cap_flag_b841_4 | （未知） | — | partial |
| +841 | 5 | 27 | cap_flag_b841_5 | （未知） | — | partial |
| +841 | 6 | 28 | cap_flag_tender_mode | 工作舰模式 | sub_478DA0, sub_507810 | confirmed |
| +841 | 7 | 29 | cap_flag_b841_7 | 位置碰撞更新旁路 | 582390→478DD0→4AE900 | confirmed |
| +842 | 0 | 30 | cap_flag_disable_special | 禁止特殊行动 | sub_4E7FF0, sub_4EF710 | confirmed |
| +842 | 1 | 32 | cap_flag_dual_mode | 双模式标志 | sub_6218F0 | confirmed |
| +842 | 2 | 33(gap) | — | （强制清零） | sub_582390 epilogue | gap |
| +842 | 3 | 34 | cap_flag_no_awakening | 禁止觉醒爆发 | sub_4EC960 | confirmed |
| +842 | 4–7 | — | — | （未知） | — | — |

**confirmed 40→47**（+7 能力位）；partial 24→17；gap 28 不变。

## 1. 逐列（读序 → CSV 位置 → 类型）

> 下表列位/类型以 `sub_582390` 为准；★=confirmed（含 Round 6 能力位 xrefs）。

| 读序 | 列号（CSV 位置） | 类型 | 语义（未证实的仅作线索） |
|---|---|---|---|
| 0 | `0` | u32 | ★**練度 ID** — 行键=机体定义 ID（sub_582390→+0） |
| 1 | `1` | i64 | ★**主模型资源键** — 582390独立i64读到+8；4C2D20→4A5470加载该完整键，旧lo列名不是低32 |
| 2 | `2` | i64 | ○**条件替代模型资源键** — 582390独立i64读到+16；4C2D20在任务/机体条件成立且键非零时替代主键；完整条件待核对，旧hi列名不是高32 |
| 3 | `3` | u16 | ★**世代** — 机体世代/系列编号（u16 @+24） |
| 4 | `4` | enum | ★**阶级**（`sub_580610`）— RANK1..RANK5（sub_580610→+408） |
| 5 | `5` | str | ★**名称** — 机体名称宽串（sub_456D90 wstring） |
| 6 | `6` | str | ★**说明** — 机体说明宽串（sub_456D90） |
| 7 | `7` | enum | ★**战斗角色**（`sub_5804F0`）— 战斗角色 ASSAULT_A/SNIPE/CANNON/SUPPORT 等（sub_5804F0→+120） |
| 8 | `8` | enum | ★**阵营**（`sub_580560`）— 阵营/国家（sub_580560→+128） |
| 9 | `9` | u32 | ★**宇宙适性** — 宇宙地形适性（col9→+136；sub_64A230 MS_PROPER_SPACE） |
| 10 | `10` | u32 | ★**水中适性** — 水中地形适性（col10→+140；sub_64A230 MS_PROPER_WATER） |
| 11 | `11` | u32 | ★**地面适性** — 地面地形适性（col11→+144；sub_64A230 MS_PROPER_GROUND） |
| 13 | `13` | bool | ★**变换备用武装** — 能力位 +840 bit0：变身形态备用武装（sub_49D280） |
| 15 | `15` | bool | ★**近战连锁** — 能力位 +840 bit1：近战连锁攻击门控（sub_4A7B10） |
| 16 | `16` | bool | ★**能力位 b840.2（预留）** — 能力位 +840 bit2（CSV→sub_582390；全二进制无 test [+840]&4 xref；str_table MS_* 无对应键） |
| 17 | `17` | bool | ★**能力位 b840.3（预留）** — 能力位 +840 bit3（CSV→sub_582390；无 runtime test xref） |
| 18 | `18` | bool | ★**任务变形态** — 能力位 +840 bit4：任务/关卡变形态资格（sub_477C10；sub_67FEB0 备选路径） |
| 19 | `19` | bool | ★**能力位 b840.5（预留）** — 能力位 +840 bit5（CSV→sub_582390；无 runtime test xref） |
| 20 | `20` | bool | ★**物理积分旁路位 +840 bit6** — 582390 CSV20非零规范为CHARA_PARAM+840 bit6；47D230末尾读取此位，4AE900在返回true时跳过53D580物理积分。47D230还包含装备/特殊状态分支，因此此位为0不能证明实际物理更新已开启。旧“无runtime xref/预留”说明错误；其他消费者与原服逐机体取值未穷举。 |
| 21 | `21` | bool | ★**能力位 b840.7（预留）** — 能力位 +840 bit7（CSV→sub_582390；无 runtime test xref） |
| 22 | `22` | bool | ★**能力位 b841.0（预留）** — 能力位 +841 bit0（CSV→sub_582390；无 runtime test xref） |
| 24 | `24` | bool | ★**跳过EX演出** — 能力位 +841 bit2：清 0 时跳过 EX 武器演出路径（sub_7E7600 @0x7e7b90） |
| 25 | `25` | bool | ★**盾牌装备** — 能力位 +841 bit3：盾牌装备能力门控（sub_474480 @+841&8；sub_48FF00） |
| 26 | `26` | bool | ★**能力位 b841.4（预留）** — 能力位 +841 bit4（CSV→sub_582390；无 runtime test xref） |
| 27 | `27` | bool | ★**能力位 b841.5（预留）** — 能力位 +841 bit5（CSV→sub_582390；无 runtime test xref） |
| 28 | `28` | bool | ★**工作舰模式** — 能力位 +841 bit6：工作舰/母舰 deploy 模式（sub_478DA0 @+841&0x40；sub_507810） |
| 29 | `29` | bool | ★**位置碰撞更新旁路位 +841 bit7** — 582390 CSV29非零规范为CHARA_PARAM+841 bit7；478DD0读取该位，4AE900在返回true时跳过普通位置/碰撞更新分支（4ADD60或载体引用分支），角色+12 bit0x40000的4A94E0路径在此前独立处理。此位为0不能证明地面碰撞成功。旧“无runtime xref/预留”说明错误；原服逐机体取值未知。 |
| 30 | `30` | bool | ★**禁止特殊行动** — 能力位 +842 bit0：置 1 时禁止 deployable 特殊行动 type 0xA/0xB（sub_4E7FF0；sub_4EF710；sub_8D3CB0） |
| 31 | `31` | bool | ★**双槽切换UI** — 能力位 +841 bit1：机体选择 UI 双槽切换/EX 武器槽显隐（sub_7E7600；sub_7E4A50；sub_7E2EF0） |
| 32 | `32` | bool | ★**双模式标志** — 能力位 +842 bit1：双模式/双形态标志（sub_6218F0→runtime+107） |
| 34 | `34` | bool | ★**禁止觉醒爆发** — 能力位 +842 bit3：置 1 时禁止觉醒/爆发模式（sub_4EC960 @+842&8） |
| 35 | `35` | enum | ★**实体类别**（`sub_5806B0`）— 实体类别 NORMAL/BATTLESHIP/TANK/MA 等（sub_5806B0→+368） |
| 36 | `36` | float | ★**数值缩放A** — 机体数值缩放系数 A（col36 float→+156；Runtime 装甲/HP 换算 sub_6218F0） |
| 37 | `37` | float | ★**数值缩放B** — 机体数值缩放系数 B（col37 float→+160） |
| 38 | `38` | u32 | ★**武器组ID** — 武器组 ID（col38→+372；→ MSMA_WEAPONSET） |
| 42 | `42` | u32 | ★**关联表ID** — 关联配置表行 ID（col42→+392；sub_7D97E0/sub_7D8520 机库升级 UI 遍历；sub_78B690 模型链） |
| 44 | `44` | u32 | ★**装备组合ID** — 装备组合 ID（col44→+396；→ MSMA_WEAPON_EQUIPCOMB） |
| 46 | `46` | u32 | ★**商店回收GP** — 商店回收 GP 基值（col46→+400；sub_887550 CShopRecycl_ItemIcon；MSMA_RENTAL 同偏移=rental_cost_gp/sub_582EC0） |
| 47 | `47` | u32 | ★**机库计时秒** — 机库/租借计时秒（col47→+404；sub_7DA460/sub_7D97E0；MSMA_RENTAL=rental_duration_sec/sub_582EC0） |
| 48 | `48` | enum | ★**可部署类型**（`sub_580BA0`）— 可部署类型 RESPAWNPOST/REPAIRPOST/TENDER 等（sub_580BA0→+412） |
| 49 | `49` | enum | ★**出生后控制器选择**（`sub_580C40`）— 582390 CSV49经580C40写CHARA_PARAM+416：NORMAL=1、MA=2、AAG=4、BATTERY=10、BATTLESHIP=11、MARCH=15；空值及未匹配文本默认NORMAL=1，精确比较不去空格。4C2D20→4BFF00自身type=3初始化及6729F0普通finishRespawn分支把此值交给容器虚表+48→4C9A80选择自身控制器；1选择4EAFB0普通SelfTargetView，2选择4DDE90变体。该switch未处理15，其他调用场景/逐机体原服值未穷举。旧“系列分类”名称不足以描述已确认运行用途；保留物理DB列名series_class。不能将空值当作零控制器，也不据此证明现场落地。 |
| 50 | `50` | u32 | ★**OC经验CP ID** — OC/经验 CP 选择 ID（col50→+420；sub_847D10 OC 待機選択；sub_81EC60 getter） |
| 51 | `51` | u32 | ★**机库列表UI参数** — 机库列表 UI 分支参数（col51→+424；sub_7E25A0/sub_97F077/sub_6B8D90） |
| 52 | `52` | u32 | ★**搭载量基值（積載量）** — ★装备搭载量基值（= 日服面板「積載量」/ 覆写关键字 `PAYLOAD`）：col52→+248。三源一致 —— 面板绑定 sub_61C9A0 idx4「装备搭载量」、开发命令 sub_6246D0 名字表 `PAYLOAD`、表 78 `MSMA_OVERWRITE_PARAMS` 关键字 `PAYLOAD`（2026-09-28 定案；旧名「喷射容量基值」已作废，喷射容量不在本行） |
| 54 | `54` | u32 | ★**机库UI槽A** — 机库 UI 控件槽 A（col54→+428；sub_897480/sub_7E94C0） |
| 55 | `55` | u32 | ★**机库UI槽B** — 机库 UI 控件槽 B（col55→+432；sub_897480/sub_7E94C0） |
| 56 | `56` | str | ★**战力子表槽·RESPAWN_TIME** — 战力子表键 col56→+436；sub_581690 用此串查 MSMA_BATTLE_DETAIL 子表 MSMA_DETAIL_RESPAWN_DATA（词表 RESPAWN_TIME）⇒ 行 +192；须与 msma_battle_detail.csv col1 相等 |
| 58 | `58` | str | ★**战力子表槽·WARP_TIME** — 战力子表键 col58→+464；查 MSMA_DETAIL_WARPTIME_DATA（WARP_TIME）⇒ 行 +236（紧急返回性能） |
| 60 | `60` | str | ★**战力子表槽·COST** — 战力子表键 col60→+492；查 MSMA_DETAIL_COST_DATA（COST）⇒ 行 +240 |
| 62 | `62` | str | ★**战力子表槽·MAX_HP** — 战力子表键 col62→+520；查 MSMA_DETAIL_MAX_HP_DATA（MAX_HP）⇒ 行 +164（面板装甲） |
| 64 | `64` | str | ★**战力子表槽·ENERGY** — 战力子表键 col64→+548；查 MSMA_DETAIL_ENERGY_DATA（ENERGY）⇒ 行 +184/+188；表 78 不覆写 |
| 67 | `67` | str | ★**战力子表槽·MOVE** — 战力子表键 col67→+576；查 MSMA_DETAIL_MOVE_DATA（MOVE）⇒ 行 +180（面板最高速度）；表 78 不覆写 |
| 69 | `69` | str | ★**战力子表槽·BOOST_GAUGEMAX** — 战力子表键 col69→+604；查 MSMA_DETAIL_BOOST_GAUGEMAX_DATA（BOOST_GAUGEMAX）⇒ 行 +168（面板喷射容量） |
| 71 | `71` | str | ★**战力子表槽·BOOST_GAUGEHEAL** — 战力子表键 col71→+632；查 MSMA_DETAIL_BOOST_GAUGEHEAL_DATA（BOOST_GAUGEHEAL）⇒ 行 +176（面板喷射蓄力） |
| 73 | `73` | str | ★**战力子表槽·BOOST_SPEED** — 战力子表键 col73→+660；查 MSMA_DETAIL_BOOST_MOVE_DATA（BOOST_SPEED）⇒ 行 +260..+312 |
| 79 | `79` | str | ★**战力子表槽·JUMP** — 战力子表键 col79→+688；查 MSMA_DETAIL_JUMP_DATA（JUMP）⇒ 行 +316..+364；表 78 不覆写 |
| 83 | `83` | u32 | ★**读侧已确证·语义未定**（`emergency_return_base` 仅兼容别名） — ASM 铁证：`sub_582390+7FC mov [esi+0FCh], eax`（`sub_BBB370`）⇒ **本列确实被读取、落 +252**；但旧标「紧急返回性能基值」2026-09-28 已作废（来自 `06-UI…` §7.2 算重 +24 的表 ✗），且表 78 覆写关键字 `MODULE_SLOT` 也落此处 ⇒ 疑为「模块槽位数」。**值已清空** |
| 85 | `85` | u32 | ★**读侧已确证·语义未定**（`boost_gauge_base` 仅兼容别名） — ASM 铁证：`sub_582390+80A mov [esi+164h], eax` ⇒ **本列被读取、落 +356**；旧标「装备搭载量基值」作废（真身 = col52/+248）。既不在面板 6 参数、也不在 `sub_581690` 后处理填充集 ⇒ 语义待定 |
| 86 | `86` | u32 | ★**读侧已确证·语义未定**（`boost_charge_base` 仅兼容别名） — ASM 铁证：`sub_582390+821 mov [esi+100h], eax` ⇒ **本列被读取、落 +256**；旧标「喷射蓄力基值」作废（真身 = 行 +176，由 `sub_581690` 后处理填）。**值已清空** |
| 87 | `87` | str | ★**Flavor 文本** — 附加说明宽串（col87 sub_456D90） |
| 88 | `88` | u32 | ★**列表分类ID** — 机库/商店列表分类 ID（col88→+32；sub_887550 回收价=list_category×GP 系数） |
| 89 | `89` | u32 | ★**读侧已确证·语义未定**（`max_speed_base` 仅兼容别名） — ASM 铁证：`sub_582390+880 mov [esi+0F4h], eax` ⇒ **本列被读取、落 +244**；旧标「最高速度基值」作废（最高速度真身 = 行 +180 float，由 `sub_581690` 后处理填）⇒ 服务端**不得**把它当最高速度退路（见 `serverv/internal/store/battle_params.go` ★） |
| 90 | `90` | u32 | ★**装甲基值** — 装甲基础值 u16（col90→+148；Hangar 属性面板 sub_6102C0） |
| 91 | `91` | u32 | ★**推进速度基值** — 推进速度基础值 u16（col91→+152） |

**区段说明**（★以 IDA 复核为准）：
- 列 13 / 15..21 / 22 / 24..29 / 30..32 / 34 = **开关位**（`sub_BBB370 != 0` ⇒ bool；内存位图在 +840/+841/+842）
- **宽串列（`wstring`）= col5 / col6 / col87**；**窄串列（`std::string`）= col56/58/60/62/64/67/69/71/73/79**；
  **枚举列 = col4 / 7 / 8 / 35 / 48 / 49**（★枚举**写名称字符串**；写错/未知名 ⇒ 读作 0）
- ★★**订正（2026-09-28）**：col56/58/60/62/69/71/73 **不是「附加资源路径」**，而是**战力子表槽**
  —— 它们的名字由 `MSMA_OVERWRITE_PARAMS`（表 78）的覆写关键字钉死：
  `RESPAWN`(56) / `WARP`(58) / `COST`(60) / `ARMOR`(62) / `BOOST`(69) / `BOOST_CHARGE`(71) / `BOOST_SPEED`(73)，
  且被写成**字符串**（`sub_402310`）= **键/标签**，与 `sub_581690` 拿这 10 个槽当查表键去查
  `MSMA_BATTLE_DETAIL` 家族（`dword_11EBA64`）互相印证 ⇒ 槽里应填**子表键串（練度ID 系）**，不是路径。
- ★★**10 槽 ↔ 子表全表定案（2026-09-28 深挖；`sub_581690` 逐块 + ctor `sub_A725F0` RTTI）**：
  每个槽 = 该子表查询用的**字符串键**（`std::map<std::string>`，strcmp 见 `sub_581270`/`sub_5812E0`），
  子表插入 = 读 CSV **col1 为字符串键**（`sub_A5BE20`：`sub_BBB4F0(idx=1)` → `vtable[2](key,val)`）；
  ⇒ **槽值必须与 `msma_battle_detail.csv` 的 col1 逐字节相等**，否则查不到行、后处理按 0：

  | 槽 CSV# | 机体行偏移 | 子表（RTTI 实名） | 词表属性 | 覆写关键字 | 写机体行 |
  |---|---|---|---|---|---|
  | 56 | +436 | `MSMA_DETAIL_RESPAWN_DATA` | `RESPAWN_TIME` | `RESPAWN` | +192 块 |
  | 58 | +464 | `MSMA_DETAIL_WARPTIME_DATA` | `WARP_TIME` | `WARP` | +236 |
  | 60 | +492 | `MSMA_DETAIL_COST_DATA` | `COST` | `COST` | +240 |
  | 62 | +520 | `MSMA_DETAIL_MAX_HP_DATA` | `MAX_HP` | `ARMOR` | +164（面板装甲） |
  | **64** | +548 | `MSMA_DETAIL_ENERGY_DATA` | **`ENERGY`** | — | +184/+188 |
  | **67** | +576 | `MSMA_DETAIL_MOVE_DATA` | **`MOVE`** | — | +180（面板最高速度） |
  | 69 | +604 | `MSMA_DETAIL_BOOST_GAUGEMAX_DATA` | `BOOST_GAUGEMAX` | `BOOST` | +168（面板喷射容量） |
  | 71 | +632 | `MSMA_DETAIL_BOOST_GAUGEHEAL_DATA` | `BOOST_GAUGEHEAL` | `BOOST_CHARGE` | +176（面板喷射蓄力） |
  | 73 | +660 | `MSMA_DETAIL_BOOST_MOVE_DATA` | `BOOST_SPEED` | `BOOST_SPEED` | +260..+312 |
  | **79** | +688 | `MSMA_DETAIL_JUMP_DATA` | **`JUMP`** | — | +316..+364 |

  ⇒ 此前标"未命名"的 **col64=ENERGY / col67=MOVE / col79=JUMP** 三槽**全部命名**（表 78 不覆写它们）。
  子表 11..13（`SHOT`/`LOCKON`/`RELOAD`）**无对应槽** ⇒ 不经此链注入。
  详见 `01-列注释/78-MSMA_OVERWRITE_PARAMS.md`、`04-填充日志.md` §13。
- 落点与列号**不成单调关系**（如 col52→`+248`、col55→`+432`、col83→`+252`）⇒ **别按内存偏移反推列号** ✗
- ✅ **命名冲突已结案（2026-09-28）**：`+248` = **`PAYLOAD` = 「装备搭载量」**（`sub_61C9A0` 面板绑定 +
  `sub_6246D0` 开发命令名字表 + 表 78 覆写关键字，**三源一致**）；`+252` = **`MODULE_SLOT`**（表 78），
  且**不属于**面板 6 参数 ⇒ 疑为 `(82,3,48)`「模块槽位数」。
  原「col52 = 喷射容量／col83 = 紧急返回性能」的配对**来自 `06-UI…` §7.2 一张算重了 +24 的表**，已订正 ⇒ **两个名字作废**。
  详见 `06-UI语义字典与参数绑定攻关.md` §7.2 订正块、`04-填充日志.md` §9。
- ⚠️⚠️ **重要连带结论**：面板 6 参数里，**只有「装备搭载量」= 本表 csv#52**；其余 5 个
  （装甲 `+164` / 最高速度 `+180` / 喷射蓄力 `+176` / 紧急返回性能 `+236`）是 **`sub_581690` 用 10 个串槽键
  查 `MSMA_BATTLE_DETAIL` 家族后"后处理"填的**（§7.3），那 5 个格子**在 CSV 里没有对应列**。
- 📌 **填充现状（2026-09-28 ENERGY/BOOST_SPEED 补填后实测）**：
  **子表槽 col56/58/60/62/64/67/69/71/73 = 576 行有值**（= 本行練度ID，与 `msma_battle_detail.csv` col1 对齐，
  **5184/5184 命中 0 miss**；其中 col64(ENERGY)/col73(BOOST_SPEED) 的子表值是两个**常量**：
  见 `34-34-MSMA_BATTLE_DETAIL.md` §2.1/§2.2）；col79(JUMP) = 0 行（**无来源也无面板绑定**，留空）。
  **col52 = 576 行有值**（= 日服面板「積載量」，`gen_msma_machine.py`，★面板里唯一直接落 CHARA_PARAM 的数值列★）；
  col90 = 576 行有值（「アーマー」，⚠保留待复核；与 `msma_battle_detail.csv` 的 `MAX_HP` 同值⇒冗余）；
  **col83/85/86/89 = 0 行有值（已清空，读侧已确证但语义未定）** ✅；
  其余 122 行（名册独有、无数值来源）无值 —— 576 + 122 = 698 ✔。

> ★**2026-10-06 batch8 补充（仿真读集 + ASM 双证）**：`col83/85/86/89` 此前标 `status=gap`（"未读取"）**是误判** ✗。
> `sub_582390` 逐个 `push <列号>` → `call sub_BBB370` → `mov [esi+off], eax` 取证：
> `83→+0FCh` / `85→+164h` / `86→100h` / `89→0F4h`（另 `88→+20h` / `90→94h` / `91→98h` 同批复核）。
> ⇒ schema `status` 由 `gap` 升 `confirmed`，**但语义仍按"未定名"处理**（旧标签仅作兼容别名，DB 列名不动、服务端不读）。
> 库侧同步：`cfg.CHARA_PARAM` / `cfg.MSMA_RENTAL` 物理列**零漂移**（`datatables/_b8_db_drift.py`）。
- ✅ **上一轮的"值放错列"已修**：旧值（6 列都填日服面板）现改为只填 col52 且换成「積載量」，
  4 个作废列清空。**被撤下的那 5 个面板参数没有丢**——它们的真正载体是
  `server/datafiles/lounge/msma/msma_battle_detail.csv`（**5184 行 = 576×9**：
  `RESPAWN_TIME/MAX_HP/MOVE/BOOST_GAUGEMAX/BOOST_GAUGEHEAL/COST/WARP_TIME` 七项由 codex/日服取值，
  `ENERGY`(常量 1000) / `BOOST_SPEED`(常量 0.84) 两项为常量，`JUMP` 无来源不发），
  前七项正好就是面板 6 参数（再出击/装甲/最高速度/喷射容量/喷射蓄力/紧急返回）+COST ⇒ **一列不差**。
  生成器：`datatables/gen_msma_machine.py`（旧 `gen_msma_base_jp.py` 已弃用）。
- 列 12/14/23/33/43/45/53/57/59/61/63/65/66/68/70… 等**未被读取** ⇒ 留空即可（越界列读作 0/空串，**不报错、不崩**）
- ★`msma_rental.csv`（表ID 35）**复用本读取器** `sub_582390`（同列规格）

**填写规则（通用）**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过（表头也用它）。
- **越界列 = 0**：只需要写到"你要设的最大列号"，后面可省略。
- 枚举列写**名称字符串**（写错/未知名 ⇒ 该列读作 0）。
- 每个数据行至少要有 1 个单元格。


## 2. GAP 列清单（sub_582390 未读取）

| CSV col | db_column | 说明 |
|---|---|---|
| `12` | `reserved_u32_12` | sub_582390 读表跳过（CSV col12 无 read_order；默认 0） |
| `14` | `reserved_u32_14` | sub_582390 读表跳过（CSV col14 无 read_order；默认 0） |
| `23` | `reserved_u32_23` | 读表跳过（col22 cap_flag_b841_0 与 col24 cap_flag_b841_2 之间的 CSV 空隙；默认 0） |
| `33` | `reserved_u32_33` | 读表跳过（+842 bit2 无 CSV 列；sub_582390 尾声 `*(_BYTE*)(a3+842)&=~4` 强制清零） |
| `39` | `reserved_u32_39` | sub_582390 读表跳过（CSV col39 无 read_order；默认 0） |
| `40` | `reserved_u32_40` | sub_582390 读表跳过（CSV col40 无 read_order；默认 0） |
| `41` | `reserved_u32_41` | sub_582390 读表跳过（CSV col41 无 read_order；默认 0） |
| `43` | `reserved_u32_43` | sub_582390 读表跳过（CSV col43 无 read_order；默认 0） |
| `45` | `reserved_u32_45` | sub_582390 读表跳过（CSV col45 无 read_order；默认 0） |
| `53` | `reserved_u32_53` | sub_582390 读表跳过（CSV col53 无 read_order；默认 0） |
| `57` | `reserved_u32_57` | sub_582390 读表跳过（CSV col57 无 read_order；默认 0） |
| `59` | `reserved_u32_59` | sub_582390 读表跳过（CSV col59 无 read_order；默认 0） |
| `61` | `reserved_u32_61` | sub_582390 读表跳过（CSV col61 无 read_order；默认 0） |
| `63` | `reserved_u32_63` | sub_582390 读表跳过（CSV col63 无 read_order；默认 0） |
| `65` | `reserved_u32_65` | sub_582390 读表跳过（CSV col65 无 read_order；默认 0） |
| `66` | `reserved_u32_66` | sub_582390 读表跳过（CSV col66 无 read_order；默认 0） |
| `68` | `reserved_u32_68` | sub_582390 读表跳过（CSV col68 无 read_order；默认 0） |
| `70` | `reserved_u32_70` | sub_582390 读表跳过（CSV col70 无 read_order；默认 0） |
| `72` | `reserved_u32_72` | sub_582390 读表跳过（CSV col72 无 read_order；默认 0） |
| `74` | `reserved_u32_74` | sub_582390 读表跳过（CSV col74 无 read_order；默认 0） |
| `75` | `reserved_u32_75` | sub_582390 读表跳过（CSV col75 无 read_order；默认 0） |
| `76` | `reserved_u32_76` | sub_582390 读表跳过（CSV col76 无 read_order；默认 0） |
| `77` | `reserved_u32_77` | sub_582390 读表跳过（CSV col77 无 read_order；默认 0） |
| `78` | `reserved_u32_78` | sub_582390 读表跳过（CSV col78 无 read_order；默认 0） |
| `80` | `reserved_u32_80` | sub_582390 读表跳过（CSV col80 无 read_order；默认 0） |
| `81` | `reserved_u32_81` | sub_582390 读表跳过（CSV col81 无 read_order；默认 0） |
| `82` | `reserved_u32_82` | sub_582390 读表跳过（CSV col82 无 read_order；默认 0） |
| `84` | `reserved_u32_84` | sub_582390 读表跳过（CSV col84 无 read_order；默认 0） |

## 3. 体检 ｜ 行数三方对账（2026-10-05 n1 批）

| 面 | 行数 |
|---|---|
| 种子 `msma/msma_settings.csv` | **698** |
| 库 `cfg."CHARA_PARAM"` | **698** |
| `meta.cfg_manifest.row_count` | **698** |

三者一致（`_probe_reconcile.py`；★计数时必须先剥 `#` 注释行 —— 本表有 **40 行** `#` 头注释，
直接数行会得出 737/738 的假差）。`col0` 698 个全数字、无重复；`col38` **698/698 全非空且唯一**。

### 3.1 ★698 的构成（口径权威）

```
698 = favms_ok_list.csv 有效名册 696 台（顺序不动，同时是客户端图鉴）
    + ms_wiki_pairs.json 有、名册没有的 2 台：1123021 ギャプラン / 1164022 シャア専用ズゴック
```

名册源文件 `unpacked/shell/settings_extract/settings/favms_ok_list.csv` 共 **700** 行、去重后 **696** 个
練度ID，其中 **4 条被 `#` 停用（注释）**：`1164022` / `1147052` / `1155051` / `1123021`
（`gow_wiki/data/_favms_report.txt`）。

⇒ 另 2 条停用项 `1147052 ガーベラ・テトラ改` / `1155051 Zプラス（テスト機カラー）` **不进本表**
（`ms_wiki_pairs.json` 无条目）；它们仍留在 `#53 MSMA_MODULE` 里，见该表 §8.3。

### 3.2 与子表的键域关系（体检结论）

| 子表 | 关系 | 结论 |
|---|---|---|
| `#35 MSMA_RENTAL`(698) | 键集**完全相同** | ✓ 镜像表 |
| `#5 CHARA_MODEL`(579) | 键是 9 位 **モデルID**，与 `#4` 的 **`col1`** 非空集**逐键相同**（双向差集 ∅） | ✓ モデルID 已解析完的 579 台 |
| `#53 MSMA_MODULE`(666) | 缺 34 + 反向多 2 | ⚠ 缺参见 §8.3 |
| `#1 MSMA_WEAPONSET`(549 组 / 1625 行) | 严格子集（`#4` col38 全覆盖：`#1` 键 − col38 = **0**） | ⚠ `#4` col38 未命中 **149** 台，**已定案**为 wiki 无武器页（见 `01-1-MSMA_WEAPONSET.md` §1.0.2，09-28 快照记 151 = 147 wiki 无页 + 4 人工判无页） |
| `#2 MSMA_WEAPON_EQUIPCOMB`(547) | 严格子集（同向，`#4` col38 未命中 **151**） | ⚠ 同上 |
