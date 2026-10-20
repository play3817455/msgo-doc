# MSMA_RENTAL ｜ `msma/msma_rental.csv`

- **用途**：机体租借参数（复用 CHARA_PARAM 读表 sub_582390，列布局相同；sub_582E90 加载）
- 表ID `35` ｜ 下载序 `35` ｜ 类名 `CCharaParamTable` ｜ 逐列读取 `sub_582390`
- 列数 64 ｜ 确证 60 ｜ 部分 0 ｜ gap 32

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `msma_id` | u32 | +0 | 租借机体ID（主键；同 CHARA_PARAM col0；机库「租用机体」列表键 sub_581200） |
| 2 | `1` | `resource_id_lo` | i64 | +8 | 图标/商店资源编号低 32（i64 @+8；sub_4BEB30 模型加载键） |
| 3 | `2` | `resource_id_hi` | i64 | +16 | 资源编号高 32（i64 @+16） |
| 4 | `3` | `generation` | u16 | +24 | 机体世代/系列编号（u16 @+24） |
| 5 | `4` | `rank` | enum `sub_580610` | +408 | RANK1..RANK5（sub_580610→+408） |
| 6 | `5` | `name` | str | +32 | 机体名称宽串（sub_456D90 wstring） |
| 7 | `6` | `description` | str | +36 | 机体说明宽串（sub_456D90） |
| 8 | `7` | `combat_role` | enum `sub_5804F0` | +120 | 战斗角色 ASSAULT_A/SNIPE/CANNON/SUPPORT 等（sub_5804F0→+120） |
| 9 | `8` | `faction` | enum `sub_580560` | +128 | 阵营/国家（sub_580560→+128） |
| 10 | `9` | `terrain_proper_space` | u32 | +136 | 宇宙地形适性（col9→+136；sub_64A230 MS_PROPER_SPACE） |
| 11 | `10` | `terrain_proper_water` | u32 | +140 | 水中地形适性（col10→+140；sub_64A230 MS_PROPER_WATER） |
| 12 | `11` | `terrain_proper_ground` | u32 | +144 | 地面地形适性（col11→+144；sub_64A230 MS_PROPER_GROUND） |
| 14 | `13` | `cap_flag_transform_alt` | bool | +840 | 能力位 +840 bit0：变身形态备用武装（sub_49D280） |
| 16 | `15` | `cap_flag_melee_chain` | bool | +840 | 能力位 +840 bit1：近战连锁攻击门控（sub_4A7B10） |
| 17 | `16` | `cap_flag_reserved_b840_2` | bool | +840 | 能力位 +840 bit2（CSV→sub_582390；全二进制无 test [+840]&4 xref；str_table MS_* 无对应键） |
| 18 | `17` | `cap_flag_reserved_b840_3` | bool | +840 | 能力位 +840 bit3（CSV→sub_582390；无 runtime test xref） |
| 19 | `18` | `cap_flag_mission_transform` | bool | +840 | 能力位 +840 bit4：任务/关卡变形态资格（sub_477C10；sub_67FEB0 备选路径） |
| 20 | `19` | `cap_flag_reserved_b840_5` | bool | +840 | 能力位 +840 bit5（CSV→sub_582390；无 runtime test xref） |
| 21 | `20` | `cap_flag_reserved_b840_6` | bool | +840 | 能力位 +840 bit6（CSV→sub_582390；无 runtime test xref） |
| 22 | `21` | `cap_flag_reserved_b840_7` | bool | +840 | 能力位 +840 bit7（CSV→sub_582390；无 runtime test xref） |
| 23 | `22` | `cap_flag_reserved_b841_0` | bool | +841 | 能力位 +841 bit0（CSV→sub_582390；无 runtime test xref） |
| 25 | `24` | `cap_flag_skip_ex_anim` | bool | +841 | 能力位 +841 bit2：清 0 时跳过 EX 武器演出路径（sub_7E7600 @0x7e7b90） |
| 26 | `25` | `cap_flag_shield_equip` | bool | +841 | 能力位 +841 bit3：盾牌装备能力门控（sub_474480 @+841&8；sub_48FF00） |
| 27 | `26` | `cap_flag_reserved_b841_4` | bool | +841 | 能力位 +841 bit4（CSV→sub_582390；无 runtime test xref） |
| 28 | `27` | `cap_flag_reserved_b841_5` | bool | +841 | 能力位 +841 bit5（CSV→sub_582390；无 runtime test xref） |
| 29 | `28` | `cap_flag_tender_mode` | bool | +841 | 能力位 +841 bit6：工作舰/母舰 deploy 模式（sub_478DA0 @+841&0x40；sub_507810） |
| 30 | `29` | `cap_flag_reserved_b841_7` | bool | +841 | 能力位 +841 bit7（CSV→sub_582390；无 runtime test xref） |
| 31 | `30` | `cap_flag_disable_special` | bool | +842 | 能力位 +842 bit0：置 1 时禁止 deployable 特殊行动 type 0xA/0xB（sub_4E7FF0；sub_4EF710；sub_8D3CB0） |
| 32 | `31` | `cap_flag_dual_slot_ui` | bool | +841 | 能力位 +841 bit1：机体选择 UI 双槽切换/EX 武器槽显隐（sub_7E7600；sub_7E4A50；sub_7E2EF0） |
| 33 | `32` | `cap_flag_dual_mode` | bool | +842 | 能力位 +842 bit1：双模式/双形态标志（sub_6218F0→runtime+107） |
| 35 | `34` | `cap_flag_no_awakening` | bool | +842 | 能力位 +842 bit3：置 1 时禁止觉醒/爆发模式（sub_4EC960 @+842&8） |
| 36 | `35` | `entity_category` | enum `sub_5806B0` | +368 | 实体类别 NORMAL/BATTLESHIP/TANK/MA 等（sub_5806B0→+368） |
| 37 | `36` | `stat_scale_a` | float | +156 | 机体数值缩放系数 A（col36 float→+156；Runtime 装甲/HP 换算 sub_6218F0） |
| 38 | `37` | `stat_scale_b` | float | +160 | 机体数值缩放系数 B（col37 float→+160） |
| 39 | `38` | `weapon_group_id` | u32 | +372 | 武器组 ID（col38→+372；→ MSMA_WEAPONSET） |
| 43 | `42` | `linked_table_id` | u32 | +392 | 关联配置表行 ID（col42→+392；sub_7D97E0/sub_7D8520 机库升级 UI 遍历；sub_78B690 模型链） |
| 45 | `44` | `equip_comb_id` | u32 | +396 | 装备组合 ID（col44→+396；→ MSMA_WEAPON_EQUIPCOMB） |
| 47 | `46` | `rental_cost_gp` | u32 | +400 | 租借 GP 费用（col46→+400；sub_582EC0 机库租用合并读 +400；对照 MODULE_RENTAL rental_cost_gp @+8） |
| 48 | `47` | `rental_duration_sec` | u32 | +404 | 租借时长秒（col47→+404；sub_582EC0 读 +404 写回机体行；sub_7DA460/sub_7D97E0；对照 MODULE_RENTAL duration_sec @+12） |
| 49 | `48` | `deployable_type` | enum `sub_580BA0` | +412 | 可部署类型 RESPAWNPOST/REPAIRPOST/TENDER 等（sub_580BA0→+412） |
| 50 | `49` | `series_class` | enum `sub_580C40` | +416 | 系列分类 NORMAL/MA/BATTERY/BATTLESHIP（sub_580C40→+416） |
| 51 | `50` | `oc_exp_cp_id` | u32 | +420 | OC/经验 CP 选择 ID（col50→+420；sub_847D10 OC 待機選択；sub_81EC60 getter） |
| 52 | `51` | `hangar_list_ui_param` | u32 | +424 | 机库列表 UI 分支参数（col51→+424；sub_7E25A0/sub_97F077/sub_6B8D90） |
| 53 | `52` | `payload_capacity_base` | u32 | +248 | ★装备搭载量基值（= 日服面板「積載量」/ 覆写关键字 `PAYLOAD`）：col52→+248。三源一致 —— 面板绑定 sub_61C9A0 idx4「装备搭载量」、开发命令 sub_6246D0 名字表 `PAYLOAD`、表 78 |
| 55 | `54` | `hangar_ui_slot_a` | u32 | +428 | 机库 UI 控件槽 A（col54→+428；sub_897480/sub_7E94C0） |
| 56 | `55` | `hangar_ui_slot_b` | u32 | +432 | 机库 UI 控件槽 B（col55→+432；sub_897480/sub_7E94C0） |
| 57 | `56` | `battle_detail_key_respawn` | enum `sub_402310` | +436 | 战力子表键 RESPAWN_TIME（col56→+436；sub_581690 用它查 MSMA_BATTLE_DETAIL 子表；须与 msma_battle_detail.csv col1 相等） |
| 59 | `58` | `battle_detail_key_warp` | enum `sub_402310` | +464 | 战力子表键 WARP_TIME（col58→+464；sub_581690 用它查 MSMA_BATTLE_DETAIL 子表；须与 msma_battle_detail.csv col1 相等） |
| 61 | `60` | `battle_detail_key_cost` | enum `sub_402310` | +492 | 战力子表键 COST（col60→+492；sub_581690 用它查 MSMA_BATTLE_DETAIL 子表；须与 msma_battle_detail.csv col1 相等） |
| 63 | `62` | `battle_detail_key_max_hp` | enum `sub_402310` | +520 | 战力子表键 MAX_HP（col62→+520；sub_581690 用它查 MSMA_BATTLE_DETAIL 子表；须与 msma_battle_detail.csv col1 相等） |
| 65 | `64` | `battle_detail_key_energy` | enum `sub_402310` | +548 | 战力子表键 ENERGY（col64→+548；sub_581690 用它查 MSMA_BATTLE_DETAIL 子表；须与 msma_battle_detail.csv col1 相等） |
| 68 | `67` | `battle_detail_key_move` | enum `sub_402310` | +576 | 战力子表键 MOVE（col67→+576；sub_581690 用它查 MSMA_BATTLE_DETAIL 子表；须与 msma_battle_detail.csv col1 相等） |
| 70 | `69` | `battle_detail_key_boost_gaugemax` | enum `sub_402310` | +604 | 战力子表键 BOOST_GAUGEMAX（col69→+604；sub_581690 用它查 MSMA_BATTLE_DETAIL 子表；须与 msma_battle_detail.csv col1 相等） |
| 72 | `71` | `battle_detail_key_boost_gaugeheal` | enum `sub_402310` | +632 | 战力子表键 BOOST_GAUGEHEAL（col71→+632；sub_581690 用它查 MSMA_BATTLE_DETAIL 子表；须与 msma_battle_detail.csv col1 相等） |
| 74 | `73` | `battle_detail_key_boost_speed` | enum `sub_402310` | +660 | 战力子表键 BOOST_SPEED（col73→+660；sub_581690 用它查 MSMA_BATTLE_DETAIL 子表；须与 msma_battle_detail.csv col1 相等） |
| 80 | `79` | `battle_detail_key_jump` | enum `sub_402310` | +688 | 战力子表键 JUMP（col79→+688；sub_581690 用它查 MSMA_BATTLE_DETAIL 子表；须与 msma_battle_detail.csv col1 相等） |
| 88 | `87` | `flavor_text` | str | +260 | 附加说明宽串（col87 sub_456D90） |
| 89 | `88` | `list_category_id` | u32 | +32 | 机库/商店列表分类 ID（col88→+32；sub_887550 回收价=list_category×GP 系数） |
| 91 | `90` | `armor_base` | u32 | +148 | 装甲基础值 u16（col90→+148；Hangar 属性面板 sub_6102C0） |
| 92 | `91` | `boost_speed_base` | u32 | +152 | 推进速度基础值 u16（col91→+152） |


## Gap 列（sub_582390 未读取；同 CHARA_PARAM）

| CSV# | 订案名 | 说明 |
|---|---|---|
| `12` | `reserved_u32_12` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `14` | `reserved_u32_14` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `23` | `reserved_u32_23` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `33` | `reserved_u32_33` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `39` | `reserved_u32_39` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `40` | `reserved_u32_40` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `41` | `reserved_u32_41` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `43` | `reserved_u32_43` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `45` | `reserved_u32_45` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `53` | `reserved_u32_53` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `57` | `reserved_u32_57` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `59` | `reserved_u32_59` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `61` | `reserved_u32_61` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `63` | `reserved_u32_63` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `65` | `reserved_u32_65` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `66` | `reserved_u32_66` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `68` | `reserved_u32_68` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `70` | `reserved_u32_70` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `72` | `reserved_u32_72` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `74` | `reserved_u32_74` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `75` | `reserved_u32_75` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `76` | `reserved_u32_76` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `77` | `reserved_u32_77` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `78` | `reserved_u32_78` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `80` | `reserved_u32_80` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `81` | `reserved_u32_81` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `82` | `reserved_u32_82` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `83` | `emergency_return_base` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `84` | `reserved_u32_84` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `85` | `boost_gauge_base` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `86` | `boost_charge_base` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |
| `89` | `max_speed_base` | CSV 列存在但 IDA 读表 sub_582390 未单独取证（默认 0；同 CHARA_PARAM gap 图） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大有效列号。

## 体检 ｜ 行数三方对账（2026-10-05 n1 批）

| 面 | 行数 |
|---|---|
| 种子 `msma/msma_rental.csv` | **698** |
| 库 `cfg."MSMA_RENTAL"` | **698** |
| `meta.cfg_manifest.row_count` | **698** |

三者一致（`_probe_reconcile.py`；本表有 **40 行** `#` 头注释，计数前须剥掉）。
★**键集与 `#4 CHARA_PARAM` 逐键完全相同（698 = 698，双向差集均为空）** ⇒ 租赁开关表是参数主表的
纯镜像，键域口径随 `#4`（696 名册 + 2 条 `ms_wiki_pairs.json` 追加，见 `04-4-CHARA_PARAM.md` §3.1）。
`col0` 全数字、无重复。

