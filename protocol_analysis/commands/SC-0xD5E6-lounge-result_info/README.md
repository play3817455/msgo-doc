# SC-0xD5E6-lounge-result_info

> 状态：`DONE`（2026-09-20，批次-14）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0xD5E6` |
| 方向 | SC（服务端 → 客户端） |
| 协议类 | `lounge_client` |
| 命令名 | `result_info` |
| 处理块范围 | `0xb7d9ec`..`0xb7e610` |
| 名字串引用点 | `0xee665c` |
| 声明容量（解码缓冲） | `0xD518`（`B7DA08`） |
| 长度闭合点 | `B7DF50`（`cmp`）→ `B7DF56 jz` |
| 报错码 | `0x19A`（块内 9 处 `push 1; push 19Ah; vt[0x64]`） |
| 去向 | `vt[0x3F4]` @`B7E5F7`（26 实参） |

## 2. 结论摘要

- **报文体线长**：`4+4+46+555+4 + (4+61nA) + (4+61nB) + (4+20nW) + 19 + 2 + (4+nD) + 40 + (4+66nF) + 41 + 4 + 12 + 2 + 8 + 13 + 4`
- 容量关系：`0xD518` = 54552 = `4+4+64+600+4 + (4+104×72) + (4+104×72) + (4+8×28) + 20 + 2 + (4+38108×1) + 40 + (4+5×72) + 68 + 4 + 24 + 2 + 8 + 16 + 4`（**逐项精确相等**）
- 长度闭合：块末 `B7DF50`（`cmp eax,[var_2C40]`）＋ `B7DF56 jz` 校验「游标 == 报文末尾」（SOP §5.3）。
- 字段数：**25**（不含 opcode）；去向：`vt[0x3F4]` @`B7E5F7`（26 实参）
- 是否分帧：否。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，不使用伪代码类型。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | 分发器 switch 选择子 | `0xD5E6` | `0xb7df96` | 确证 |
| 1 | 0 | 4 | u32 | win_team | 胜方阵营（日志串 `win_team=`） | 经 `vt[0x3F4]` 交业务 | - | 0xb7da46|0xb7dfec | 确证 |
| 2 | 4 | 4 | u32 | res_coop | 协同一波结果码（日志串 `res_coop=`） | 经 `vt[0x3F4]` 交业务 | - | 0xb7da83|0xb7e016 | 确证 |
| 3 | 8 | 46 | struct<progress> | progress | 对战进度结构（日志串 `progress=`，claim 0x40=64；打印器 `sub_B0A820`） | 经 `vt[0x3F4]` 交业务；成员（14）：`remain_msec`(u32)/`coop_step`(u32)/`A_point_now`(u32)/`B_point_now`(u32)/`A_gauge_dmg_scale`(u16)/`B_gauge_dmg_scale`(u16)/`coop_dead_remain`(u8)/`is_prestart`(u8)/`rule_status`(u32)/`rule_timer_msec`(u32)/`rule_param1`(u32)/`rule_param2`(u32)/`A_dot_dmg`(u32)/`B_dot_dmg`(u32) | - | 0xb7da9b|0xb7daad|0xb7e050 | 确证 |
| 4 | 54 | 555 | struct<result_detail> | result | 战斗结算详情（日志串 `result=`，claim `0x258`=600；打印器 `sub_B4C650`） | 经 `vt[0x3F4]` 交业务；内部成员未逐一命名（见 `notes.md`） | - | 0xb7dac5|0xb7dad7|0xb7e07d | 确证 |
| 5 | 609 | 4 | u32 | result_wbonus | 结算加成（日志串 `result_wbonus=`，claim 4；打印器 `sub_B4D7A0` 打印 `lv`/`openbox`/`gp_rate`） | 经 `vt[0x3F4]` 交业务 | - | 0xb7daf3|0xb7db05|0xb7e0aa | 确证 |
| 6 | 613 | 4 | u32 | score_ranking_A_num | A 方战绩排行条数（≤104，`cmp ebx,68h; ja`@`B7DB48`） | 驱动 `score_ranking_A` 数组循环（`cmp edi,ebx; jb`@`B7DB8E`） | 0..104 | 0xb7db1f|0xb7db48|0xb7db8e | 确证 |
| 7 | 617 | 61n | array<score_ranking,104> | score_ranking_A | A 方战绩排行（日志串 `score_ranking_A={`；元素打印器 `sub_B4C340`；槽步进 72 = `sub_B413C0`） | 经 `vt[0x3F4]` 交业务；元素成员（19）：`pilot_id`(u32)/`world_id`(u32)/`is_cmdr`(u8)/`is_xbnpc`(u8)/`rank`(u16)/`totalpoint`(u32)/`stghold_dmg`(u32)/`kill_cnt`(u16)/`atk_point`(u32)/`spt_point`(u32)/`con_point`(u32)/`victory_score`(u32)/`ranking_point`(u32)/`last_msma`(u32)/`last_weapon`(u32)/`last_shield`(u32)/`last_decal`(u32)/`last_mscolor`(u8)/`add_rate_vslocal`(u16) | - | 0xb7db57|0xb7db7a|0xb7db8e|0xb7e0b8 | 确证 |
| 8 | var | 4 | u32 | score_ranking_B_num | B 方战绩排行条数（≤104，`cmp ebx,68h; ja`@`B7DBC2`） | 驱动 `score_ranking_B` 数组循环 | 0..104 | 0xb7dbae|0xb7dbc2|0xb7dc10 | 确证 |
| 9 | var | 61n | array<score_ranking,104> | score_ranking_B | B 方战绩排行（日志串 `score_ranking_B={`；打印器 `sub_B4C340`） | 经 `vt[0x3F4]` 交业务；元素成员同 `score_ranking_A` | - | 0xb7dbd8|0xb7dbfc|0xb7e132 | 确证 |
| 10 | var | 4 | u32 | result_wave_num | 波段结果条数（≤8，`cmp ebx,8; ja`@`B7DC44`） | 驱动 `result_wave` 数组循环 | 0..8 | 0xb7dc30|0xb7dc44|0xb7dc92 | 确证 |
| 11 | var | 20n | array<result_wave,8> | result_wave | 各波段战斗结果（日志串 `result_wave={`；元素打印器 `sub_B4DB10`；槽步进 28 = `sub_B41710`） | 经 `vt[0x3F4]` 交业务；元素成员（10）：`wave_rank`(u8)/`cleartime_sec`(u32)/`cleartime_rank`(u8)/`container_num`(u16)/`container_max`(u16)/`container_rank`(u8)/`enemybase_num`(u16)/`enemybase_max`(u16)/`enemybase_rank`(u8)/`total_score`(u32) | - | 0xb7dc5a|0xb7dc7e|0xb7e1b2 | 确证 |
| 12 | var | 19 | struct<total_result_wave> | totalresult_wave | 波次汇总（日志串 `totalresult_wave=`，claim 0x14=20；打印器 `sub_B4DCC0`） | 经 `vt[0x3F4]` 交业务；成员（7）：`end_wave`(u8)/`result_coop`(u8)/`rank`(u8)/`rank_score`(u32)/`container_comp`(u32)/`enemyobj_comp`(u32)/`total_score`(u32) | - | 0xb7dcb4|0xb7dcc6|0xb7e251 | 确证 |
| 13 | var | 2 | u16 | ranking_highscore | 排行最高分（日志串 `ranking_highscore=`） | 经 `vt[0x3F4]` 交业务 | - | 0xb7dcee|0xb7e26f | 确证 |
| 14 | var | 4 | u32 | debrief_info_num | 简报字节数（≤38108 = `0x94DC`，`cmp ebx,94DCh; ja`@`B7DD1C`） | 驱动 `debrief_info` 字节数组循环 | 0..38108 | 0xb7dd08|0xb7dd1c|0xb7dd5c | 确证 |
| 15 | var | n | bytes[debrief_info_num] | debrief_info | 战报简报原始字节（日志串 `debrief_info={`；打印器 `sub_ADCBF0` 按字节打印） | 经 `vt[0x3F4]` 交业务；槽步进 1 = `sub_B05EA0` | - | 0xb7dd32|0xb7dd4d|0xb7e28a | 确证 |
| 16 | var | 40 | array<examination_item,5> | examination_list | 考核结果列表（固定 5 元、**无线上 count**；日志串 `examination_list={`） | 经 `vt[0x3F4]` 交业务；元素成员（2）：`id`(u32)/`gain_val`(u32)；槽步进 8 = `sub_B418C0`（整块推进 0x28=40） | - | 0xb7dd7b|0xb7dd8c|0xb7dd9e|0xb7e300 | 确证 |
| 17 | var | 4 | u32 | favms_add_num | 战绩参战机体追加条数（≤5，`cmp ebx,5; ja`@`B7DDD3`） | 驱动 `favms_add` 数组循环 | 0..5 | 0xb7ddbf|0xb7ddd3|0xb7de1e | 确证 |
| 18 | var | 66n | array<favms_add,5> | favms_add | 机体战绩追加列表（日志串 `favms_add={`；元素打印器 `sub_B47CC0`；槽步进 72 = `sub_B413C0`） | 经 `vt[0x3F4]` 交业务；元素成员（18）：`pilot_id`(u32)/`favorite_ms_id`(u32)/`battle_rule`(u8)/`favorite_exp_sum`(u32)/`kill_cnt`(u32)/`kill_assist_cnt`(u32)/`resurrect_cnt`(u32)/`stghold_damage`(u32)/`battle_cnt`(u32)/`score_max_atk`(u32)/`score_max_spt`(u32)/`score_max_con`(u32)/`score_sum_atk`(u32)/`score_sum_spt`(u32)/`score_sum_con`(u32)/`score_sum_sum`(u32)/`last_update`(u32)/`dirty_flag`(u8) | - | 0xb7dde6|0xb7de0a|0xb7e35f | 确证 |
| 19 | var | 41 | struct<dcpoint_detail> | dcpoint | 断线扣分详情（日志串 `dcpoint=`，claim 0x44=68；打印器 `sub_B50F80`） | 经 `vt[0x3F4]` 交业务；打印器成员：`is_dc`/`bef_dcpoint`/`aft_dcpoint`/`bef_next`/`aft_next`/`reward_item_ids`/`reward_item_nums`（内部线序未逐一拆分，见 `notes.md`） | - | 0xb7de3d|0xb7de4c|0xb7e3f7 | 推测 |
| 20 | var | 4 | u32 | dbbonus_get | DB 加成获得（日志串 `dbbonus_get=`） | 经 `vt[0x3F4]` 交业务 | - | 0xb7de74|0xb7e414 | 确证 |
| 21 | var | 12 | struct<pointdmg> | pointdmg | 点位伤害（日志串 `pointdmg=`，claim 0x18=24；打印器 `sub_B4DEE0` 打印 `gaugedmg={`） | 经 `vt[0x3F4]` 交业务；成员：`gaugedmg` = `u32[3]`（3 元定长、无线上 count） | - | 0xb7de8d|0xb7de9c|0xb7e44b | 确证 |
| 22 | var | 2 | u16 | adop_result | 配属结果（日志串 `adop_result=`） | 经 `vt[0x3F4]` 交业务 | - | 0xb7dec4|0xb7e469 | 确证 |
| 23 | var | 8 | u64 | adop_uniq_msid | 配属机体唯一 ID（日志串 `adop_uniq_msid=`） | 经 `vt[0x3F4]` 交业务（cdecl 拆低/高 32 位） | - | 0xb7deec|0xb7e497 | 确证 |
| 24 | var | 13 | struct<adop_get> | adop_get | 配属获得详情（日志串 `adop_get=`，claim 0x10=16；打印器 `sub_B4AC50`） | 经 `vt[0x3F4]` 交业务；打印器成员：`db_index`/`equip_wid`/`adop_set` | - | 0xb7df05|0xb7df14|0xb7e4ce | 确证 |
| 25 | var | 4 | u32 | season_class_up_promotion_point | 赛季阶级晋升点（日志串 `season_class_up_promotion_point=`） | 经 `vt[0x3F4]` 交业务 | - | 0xb7df3c|0xb7e4e6 | 确证 |

（与 `fields.csv` 必须完全一致）

## 4. 分析记录

### 4.1 定位过程
1. 名字串引用点 `0xb7df96` 落在处理块 `0xb7d9ec`..`0xb7e610`（939 条指令，本批最大块）内。
2. 容量经分配器指纹在 `B7DA08` 确证为 `0xD518`。
3. ★容量反推**一击命中**：`0xD518` 逐项等于 20 个字段的 claim 之和（见 §4.2），据此唯一确定各计数上限（104 / 104 / 8 / 38108 / 5）。
4. 字段类型全部由汇编判定（SOP §6）：定长字段用 `sub_B02DD0`/`B02DF0`/`B06230`/`B06200`；复合字段用整函数扫描的元素读取器。
5. 闭合：`B7DF50`+`B7DF56`（SOP §5.3）。去向：`vt[0x3F4]` @`B7E5F7`（26 实参）。

### 4.2 长度闭合与容量口径
- 容量关系：`0xD518` = 54552 = `4+4+64+600+4 + (4+104×72) + (4+104×72) + (4+8×28) + 20 + 2 + (4+38108×1) + 40 + (4+5×72) + 68 + 4 + 24 + 2 + 8 + 16 + 4`（**逐项精确相等**）
- 线长：`4+4+46+555+4 + (4+61nA) + (4+61nB) + (4+20nW) + 19 + 2 + (4+nD) + 40 + (4+66nF) + 41 + 4 + 12 + 2 + 8 + 13 + 4`

### 4.3 存疑点
见 `notes.md`。

## 5. 质量门自检

- [x] G1 字段表总长与客户端长度闭合一致（或已说明为何无法闭合）
- [x] G2 每个字段的线类型都能指回汇编证据 VA，未使用伪代码类型
- [x] G3 每个字段都有含义与用途（或明确标注仅回显/仅日志并给证据）
- [x] G4 不确定项全部显式标 `?` 且已记入 `notes.md`
- [x] G5 `README.md` / `fields.csv` / `asm.md` 三处一致
- [x] G6 INDEX 该行状态与文件夹内容一致（`DONE`）
- [x] G7 有配对请求/应答的命令已互相链接
