# SC-0x063E-pilot_select_r

> 状态：`DONE`（2026-09-20，批次-2）
> 方向：服务端 → 客户端（recv）
> 协议类：`lounge_client`
> 依据规范：`00-规范-组包格式分析SOP.md`

## 1. 命令元信息

| 项 | 值 |
|---|---|
| opcode | `0x063E` |
| 方向 | SC（服务端 → 客户端（recv）） |
| 协议类 | `lounge_client` |
| 命令名 | `pilot_select_r` |
| 名字符串 | `)->_proto_lounge_client::recv_pilot_select_r( ` @ `0xEE9F74`，引用点 `0xB539E5` |
| 处理函数 | `sub_B51930` @ `0xB51930`（lounge 分发器） |
| 处理块范围 | `0xB53684` .. `0xB53E2B`（块首 `0xB53684 push 16h; call sub_B41120`，错误码 `0x16`） |
| 关联命令 | 配对发送侧 `../CS-0xF705-lounge-pilot_select/`（容量 `0x16`） |

## 2. 结论摘要

- **报文体总长：变长 `51725 + L` 字节**（`L = len(heroms_term)`，`L ≤ 64` ⇒ 线长 ∈ `[51725, 51789]`）。这是本目录目前**最长的单条 S→C 命令体**。
- 负载 = **17 个字段**，其中第 7 个字段 `pilot_detail` 是一个 **51672 字节**的复合结构体（含 9 个固定数组与 3 个嵌套结构体）。
- 长度校验：`0xB5399E mov ecx,[esp+var_2C44]`（游标）、`0xB539A2 cmp ecx,[esp+var_2C40]`（vs 报文末尾）、`0xB539A8 jz ok`（不等 ⇒ `push 16h` 报错）⇒ **整包精确消费完**（含 51672B 的结构体与变长串）。
- **容量 ≠ 线长**：声明容量 `push 0DB85h`（`0xB5369D`）= **56197**。容量 = 各字段**缓冲 claim 之和**，可精确分解并互相印证：
  `4+4+4+4+8+4`（28，字段 1~6）`+ 0xDB10`(56080，`pilot_detail` 的结构体 claim)`+ 1+1+4+1+4+4+4`（19）`+ 0x41`(65，`heroms_term` 槽位预算)`+ 1+4`（5）`= 56197 = 0xDB85` ✓
  而 `pilot_detail` 的结构体 claim `0xDB10` = **结构体实际占用跨度**（末成员 `beginner_challenge_info` 位于 `+0D948h`，其跨度 456B ⇒ `0D948h + 0x1C8 = 0xDB10`）——claim 的语义由此得到双重印证。
- 是否分帧：否（本客户端对单条报文的分帧边界见 `notes.md` Q5；本条为单帧）。
- 关键结论：18 个逻辑值一次性交 `vt[0x94]`（`0xB53DA0` 取虚表项 / `0xB53DD2` 调用），实参顺序见 §4.3。
- **机器草案为什么只列出 6 个字段**：`ida_draft_wire.py` 在 `0xB537EF` 的 `sub_B41260`（缓冲预留器）后被复合读取器 `sub_B42640` 中断 ⇒ 草案止步于 `0xB537D7`（字段 6）。
- ⚠️ **复核提醒（本批最大的坑）**：`sub_B42640` 的函数体是 `0xB42640..0xB42BA3`（1379B / 464 条指令），**不是**到第一个 `retn`（`0xB42796`）为止 —— 该函数在「失败出口」之后还有**成功路径**，其中包含 `comment`(115B) 起直至 `beginner_challenge_info`(454B) 的全部读取。用 `ida_funcs.get_func()` 取真实边界再整函数扫描，才能得到 `pilot_detail` 的**真实线长 51672B**（若在失败 `retn` 处停止扫描，会误算成 64B）。

## 3. 帧格式表

> 每行必须有汇编证据 VA；**线类型只能来自汇编**，禁止使用伪代码类型。
> `L` = `heroms_term` 的**串内容字节数**（不含结尾 NUL）。

| 序号 | 偏移 | 长度 | 线类型 | 字段名 | 含义 | 用途 | 取值/枚举 | 证据(VA) | 置信度 |
|---|---|---|---|---|---|---|---|---|---|
| 0 | - | 2 | u16 | opcode | 命令号 | lounge 分发的 switch 选择子 | `0x063E` | `0xB539E5`（名字串引用点） | 确证 |
| 1 | 0 | 4 | u32 | `result` | 选人结果码 | 交 `vt[0x94]`（第 1 实参）；日志 `result=`（`0xB53A3B`，十进制） | `?`（枚举未定） | `0xB536DB`（`sub_B02DD0`）；`0xB02DE9 add [eax],4`；日志 `0xB53A3B` | 类型确证 / 枚举待定 |
| 2 | 4 | 4 | u32 | `restore_channel` | 恢复（重连）频道号 | 交 `vt[0x94]`（第 2 实参）；日志 `restore_channel=`（`0xB53A65`） | - | `0xB53718`（`sub_B02DD0`）；日志 `0xB53A65` | 确证 |
| 3 | 8 | 4 | u32 | `charge_point` | 充能点（能量/点数） | 交 `vt[0x94]`（第 3 实参）；日志 `charge_point=`（`0xB53A92`） | - | `0xB53742`（`sub_B02DD0`）；日志 `0xB53A92` | 确证 |
| 4 | 12 | 4 | u32 | `tuto_step` | 教程进度步号 | 交 `vt[0x94]`（第 4 实参）；日志 `tuto_step=`（`0xB53ABF`） | - | `0xB5376C`（`sub_B02DD0`）；日志 `0xB53ABF` | 确证 |
| 5 | 16 | 8 | u64 | `tuto_flags` | 教程标志位（64 位） | 交 `vt[0x94]`（第 5+6 实参 = 低/高 4 字节）；日志 `tuto_flags=`（`0xB53AE9`，打印器 `sub_B08500`） | 位义 `?` | 预留 `0xB53785`（`sub_B41A10`，claim 8B）；读 `0xB53794`（`sub_B06200`，`+8`）；日志 `0xB53AE9` | 确证（类型）/ 位义 `?` |
| 6 | 24 | 4 | u32 | `tuto_missionid` | 教程任务 ID | 交 `vt[0x94]`（第 7 实参）；日志 `tuto_missionid=`（`0xB53B16`） | - | `0xB537D7`（`sub_B02DD0`）；日志 `0xB53B16` | 确证 |
| 7 | 28 | **51672** | struct `pilot_detail` | `pilot_detail` | 驾驶员（玩家）详情（**全量概要**，含 9 个数组 + 3 个嵌套结构体） | 结构体指针交 `vt[0x94]`（第 8 实参）；日志 `pilot_detail=` + 打印器 `sub_B48010` | 成员见 §3.1 / §3.2 | 预留 `0xB537EF`（`sub_B41260`，claim `0xDB10`）；读 `0xB53801`（`sub_B42640`，函数体 `0xB42640..0xB42BA3`） | 确证 |
| 8 | 51700 | 1 | u8 | `is_netcafe` | 是否网吧环境 | 交 `vt[0x94]`（第 9 实参，零扩展）；日志 `is_netcafe=`（`0xB53B6B`，布尔打印器 `sub_B0C1F0`） | `?` | `0xB53825`（`sub_B06230`）；`0xB06249 add [eax],1`；日志 `0xB53B6B` | 确证 |
| 9 | 51701 | 1 | u8 | `is_processing_comeback` | 是否正在处理「回归（comeback）玩家」流程 | 交 `vt[0x94]`（第 10 实参）；日志 `is_processing_comeback=`（`0xB53B95`） | `?` | `0xB5384D`（`sub_B06230`）；日志 `0xB53B95` | 确证 |
| 10 | 51702 | 4 | u32 | `vip_lv` | VIP 等级 | 交 `vt[0x94]`（第 11 实参）；日志 `vip_lv=`（`0xB53BC1`） | - | `0xB53875`（`sub_B02DD0`）；日志 `0xB53BC1` | 确证 |
| 11 | 51706 | 1 | u8 | `overplay_type` | 超额游玩（overplay）类型 | 交 `vt[0x94]`（第 12 实参）；日志 `overplay_type=`（`0xB53BE9`，布尔打印器） | `?`（枚举未定） | `0xB5389D`（`sub_B06230`）；日志 `0xB53BE9` | 类型确证 / 枚举待定 |
| 12 | 51707 | 4 | u32 | `accum_playtime` | 累计游玩时长 | 交 `vt[0x94]`（第 13 实参）；日志 `accum_playtime=`（`0xB53C15`） | `?`（单位未定） | `0xB538C5`（`sub_B02DD0`）；日志 `0xB53C15` | 类型确证 / 单位待定 |
| 13 | 51711 | 4 | u32 | `daily_compcnt` | 当日完成次数 | 交 `vt[0x94]`（第 14 实参）；日志 `daily_compcnt=`（`0xB53C3F`） | - | `0xB538ED`（`sub_B02DD0`）；日志 `0xB53C3F` | 确证 |
| 14 | 51715 | 4 | u32 | `ncafe_compcnt` | 网吧任务完成次数 | 交 `vt[0x94]`（第 15 实参）；日志 `ncafe_compcnt=`（`0xB53C69`） | - | `0xB53915`（`sub_B02DD0`）；日志 `0xB53C69` | 确证 |
| 15 | 51719 | `L+1` | bytes（NUL 串） | `heroms_term` | 「英雄（heroms）」期限字符串 | 交 `vt[0x94]`（第 16 实参 = 串指针）；日志 `heroms_term="` + 内容 + `"`（`0xB53C96`） | 槽位预算 `0x41`=65B ⇒ `L ≤ 64` | 读 `0xB5393E`（`sub_B02BA0`，消费 = `L+1`，见 `asm.md` E8）；槽推进 `0xB5392B add eax,41h`、槽预算 `0xB53932 push 41h`；日志 `0xB53C96` | 确证 |
| 16 | 51720+L | 1 | u8 | `flag_wideuse` | 是否启用「宽屏/广泛使用（wideuse）」标志 | 交 `vt[0x94]`（第 17 实参）；日志 `flag_wideuse=`（`0xB53CC9`，布尔打印器） | `?` | `0xB53966`（`sub_B06230`）；日志 `0xB53CC9` | 确证 |
| 17 | 51721+L | 4 | u32 | `level_point` | 等级点数 | 交 `vt[0x94]`（第 18 实参）；日志 `level_point=`（`0xB53CF0`） | - | `0xB5398E`（`sub_B02DD0`）；日志 `0xB53CF0` | 确证 |
| — | `51725+L` | 0 | — | （长度闭合） | — | 游标必须 == 报文末尾 | — | `0xB539A2`（`cmp`）、`0xB539A8`（`jz`） | 确证 |

> 偏移核算：`28`(字段 1~6) `+ 51672`(字段 7) `= 51700`；`51700+1+1+4+1+4+4+4 = 51719`（字段 8~14）；串占 `L+1` ⇒ 字段 16 起 `51720+L`、字段 17 起 `51721+L`、**整包末尾 `51725+L`** ✓

### 3.1 `pilot_detail` 结构体内部（读取器 `sub_B42640` @ `0xB42640`，**线长 51672B**）

> 「线偏移」= 相对 `pilot_detail` 起点的偏移；「内存偏移」取自打印器 `sub_B48010`（`0xB48010`，函数体 `0xB48010..0xB48C01`）。
> 结构体 claim = `0xDB10` = 56080B；**线长 51672B**（两者不等：数组元素在「线」上比「内存」紧凑，例如 `favms_arr` 元素线 66B / 内存步进 72B）。

| # | 线偏移 | 长度 | 线类型 | 字段名 | 含义 | 内存偏移 | 证据(VA) |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 4 | u32 | `exp` | 经验值 | +0 | 读 `0xB4265A`；名 `0xB48032` |
| 2 | 4 | 4 | u32 | `money` | 游戏内货币 | +4 | 读 `0xB4266F`；名 `0xB48059` |
| 3 | 8 | 4 | u32 | `clan_id` | 所属战队（clan）ID | +8 | 读 `0xB42685`；名 `0xB48080` |
| 4 | 12 | 4 | u32 | `clan_memb_exp` | 战队成员经验 | +0Ch | 读 `0xB4269F`；名 `0xB480A7` |
| 5 | 16 | 4 | u32 | `clan_forbidden` | 战队禁入/禁言标志 | +10h | 读 `0xB426A6`；名 `0xB480CE` |
| 6 | 20 | 4 | u32 | `cupteam_id` | 杯赛队伍 ID | +14h | 读 `0xB426BB`；名 `0xB480F5` |
| 7 | 24 | 2 | u16 | `deckcost` | 卡组/编成费用 | +18h | 读 `0xB426D0`；名 `0xB4811D` |
| 8 | 26 | 4 | u32 | `last_battle` | 上次战斗（时刻/ID） | +1Ch | 读 `0xB426E5`；名 `0xB48144` |
| 9 | 30 | 4 | u32 | `cw_chscore` | 连战/冠军积分 | +20h | 读 `0xB426FA`；名 `0xB4816B` |
| 10 | 34 | 4 | u32 | `score_special_a` | 特殊积分 A | +24h | 读 `0xB4270F`；名 `0xB48192` |
| 11 | 38 | 4 | u32 | `last_play_bonus` | 上次游玩奖励 | +28h | 读 `0xB42720`；名 `0xB481B9` |
| 12 | 42 | 4 | u32 | `last_play_bonus_vsl` | 上次游玩奖励（VS 联赛） | +2Ch | 读 `0xB42731`；名 `0xB481E0` |
| 13 | 46 | 2 | u16 | `last_play_bonus_vsl_cnt` | 上次 VS 联赛奖励次数 | +30h | 读 `0xB42742`；名 `0xB48208` |
| 14 | 48 | 4 | u32 | `last_dormant_ret_cc` | 上次休眠回归奖励（CC） | +34h | 读 `0xB42753`；名 `0xB4822F` |
| 15 | 52 | 4 | u32 | `capture_bonus_state` | 占领奖励状态 | +38h | 读 `0xB42764`；名 `0xB48256` |
| 16 | 56 | 4 | u32 | `capture_bonus_limit` | 占领奖励上限 | +3Ch | 读 `0xB42775`；名 `0xB4827D` |
| 17 | 60 | 4 | u32 | `clan_rokaku_btime_limit` | 战队「楼阁」建设时间上限 | +40h | 读 `0xB42786`；名 `0xB482A4` |
| 18 | 64 | 115 | bytes（char[115]） | `comment` | 个人留言（**定长 115 字节**，循环读 0x73 次 u8） | +44h | 循环 `0xB427A0..0xB427BC`（`sub_B06230` ×115）；名 `0xB482CB` |
| 19 | 179 | 128 | array\<u64,16\> | `hav_medal` | 已获得勋章（16 个 u64） | +0B8h | 循环 `0xB427C7..0xB427E2`（`sub_B06200` ×16，步进 8）；名 `0xB482F9` |
| 20 | 307 | 64 | array\<u64,8\> | `hav_emblem` | 已获得徽章（8 个 u64） | +138h | 循环 `0xB427F0..0xB4280B`；名 `0xB4836E` |
| 21 | 371 | 1280 | array\<u64,160\> | `hav_avatar` | 已获得头像（160 个 u64） | +178h | 循环 `0xB42815..0xB42833`；名 `0xB483DE` |
| 22 | 1651 | 64 | array\<u64,8\> | `hav_voice` | 已获得语音（8 个 u64） | +678h | 循环 `0xB42840..0xB4285B`；名 `0xB4844E` |
| 23 | 1715 | 512 | array\<u32,128\> | `hav_modules` | 已获得模块（128 个 u32） | +6B8h | 循环 `0xB42865..0xB42885`；名 `0xB484B7` |
| 24 | 2227 | 68 | struct `examination_state` | `examination_state` | 考验/考核状态（含 5 元素考核列表） | +8B8h | 读 `0xB4288F`（`sub_B42330`）；名 `0xB4851F`；内部见 §3.2 |
| 25 | 2295 | 8 | u64 | `rokaku_uniq_msid` | 楼阁机体唯一 ID | +900h | 读 `0xB428A7`；名 `0xB48552` |
| 26 | 2303 | 8 | u64 | `rokaku_space_uniq_msid` | 楼阁空间机体唯一 ID | +908h | 读 `0xB428BF`；名 `0xB48583` |
| 27 | 2311 | 4 | u32 | `rokaku_pt` | 楼阁点数 | +910h | 读 `0xB428D7`；名 `0xB485AD` |
| 28 | 2315 | 4 | u32 | `rokaku_pt_use` | 已用楼阁点数 | +914h | 读 `0xB428EF`；名 `0xB485D7` |
| 29 | 2319 | 192 | array\<cshist_item,32\> | `cshist` | 挑战赛（CS）战绩历史（32 条） | +918h | 读 `0xB42907`（`sub_B423F0`，32 × 6B）；名 `0xB48601`；元素见 §3.2 |
| 30 | 2511 | 1 | u8 | `second_chance_free` | 复归机会（免费）次数 | +0A18h | 读 `0xB4291F`；名 `0xB4862E` |
| 31 | 2512 | 4 | u32 | `second_chance_free_upd` | 复归机会（免费）更新时间 | +0A1Ch | 读 `0xB42937`；名 `0xB48658` |
| 32 | 2516 | 1024 | array\<rental_module,128\> | `hav_rental_modules` | 已获得租用模块（128 条，各 8B） | +0A20h | 循环 `0xB42950..0xB4296E`（`sub_B434B0` ×128）；名 `0xB48673`；元素见 §3.2 |
| 33 | 3540 | 4 | u32 | `dc_point` | DC 点数 | +0E20h | 读 `0xB42978`；名 `0xB4878B` |
| 34 | 3544 | 47520 | array\<favms,720\> | `favms_arr` | 收藏（favorite）机体战绩数组（**720 条 × 66B**） | +0E24h | 循环 `0xB42990..0xB429AE`（`sub_B424D0` ×720，内存步进 `0x48`=72）；名 `0xB487B0`；元素见 §3.2 |
| 35 | 51064 | 40 | array\<u32,10\> | `heroms_grants` | 英雄（heroms）授予列表（10 个 u32） | +0D8A4h | 循环 `0xB429B8..0xB429D3`；名 `0xB48815` |
| 36 | 51104 | 8 | u64 | `heroms_uniqid` | 英雄唯一 ID | +0D8D0h | 读 `0xB429DD`；名 `0xB48884` |
| 37 | 51112 | 4 | u32 | `last_period_bonus` | 上次周期奖励 | +0D8D8h | 读 `0xB429F5`；名 `0xB488AE` |
| 38 | 51116 | 4 | u32 | `daily_battle_bonus_flg` | 每日战斗奖励标志（十六进制打印） | +0D8DCh | 读 `0xB42A0D`；名 `0xB488D8` |
| 39 | 51120 | 4 | u32 | `last_daily_battle_bonus` | 上次每日战斗奖励 | +0D8E0h | 读 `0xB42A25`；名 `0xB48902` |
| 40 | 51124 | 4 | u32 | `check_progress_quest_id` | 进度检查任务 ID | +0D8E4h | 读 `0xB42A3D`；名 `0xB4892C` |
| 41 | 51128 | 2 | array\<u16,1\> | `lvjudge_hist` | 等级判定历史（1 项） | +0D8E8h | 循环 `0xB42A55..0xB42A70`（×1）；名 `0xB48952` |
| 42 | 51130 | 4 | u32 | `pilot_made_timestamp` | 驾驶员创建时间戳 | +0D8ECh | 读 `0xB42A7A`；名 `0xB4898F` |
| 43 | 51134 | 2 | u16 | `newpilot_challenge_nextindex` | 新兵挑战下一序号 | +0D8F0h | 读 `0xB42A92`；名 `0xB489BA` |
| 44 | 51136 | 4 | u32 | `newpilot_challenge_last` | 新兵挑战上次值 | +0D8F4h | 读 `0xB42AAA`；名 `0xB489E4` |
| 45 | 51140 | 38 | array\<u16,19\> | `sc_lv_up_reward_get` | 等级提升奖励获取位图（19 项） | +0D8F8h | 循环 `0xB42AC4..0xB42ADD`（×0x13=19）；名 `0xB48A0A` |
| 46 | 51178 | 24 | array\<u16,12\> | `sc_lv_max_pre` | 等级上限预览（12 项） | +0D91Eh | 循环 `0xB42AE9..0xB42B02`（×0x0C=12）；名 `0xB48A75` |
| 47 | 51202 | 2 | u16 | `sc_lv_max` | 当前等级上限 | +0D936h | 读 `0xB42B0C`；名 `0xB48ADF` |
| 48 | 51204 | 4 | u32 | `last_pilot_channel_in` | 上次进入频道 | +0D938h | 读 `0xB42B20`；名 `0xB48B09` |
| 49 | 51208 | 2 | u16 | `monthly_bonus_holding_id` | 月奖励持有 ID | +0D93Ch | 读 `0xB42B34`；名 `0xB48B34` |
| 50 | 51210 | 2 | u16 | `monthly_bonus_logincnt` | 月奖励登录计数 | +0D93Eh | 读 `0xB42B48`；名 `0xB48B5F` |
| 51 | 51212 | 2 | u16 | `monthly_bonus_xwarcnt` | 月奖励对战计数 | +0D940h | 读 `0xB42B5C`；名 `0xB48B8A` |
| 52 | 51214 | 4 | u32 | `periodpath_end` | 周期路径终点 | +0D944h | 读 `0xB42B70`；名 `0xB48BB4` |
| 53 | 51218 | 454 | struct `beginner_challenge_info` | `beginner_challenge_info` | 新兵挑战信息 | +0D948h | 读 `0xB42B91`（`sub_B42440`）；名 `0xB48BD9`；内部见 §3.2 |

合计：**51672 字节** ✓（逐项相加见 `asm.md` E5 的核算块）

### 3.2 `pilot_detail` 内嵌结构体/数组元素

| 结构 | 线长 | 线序成员（线类型：字段名） | 证据(VA) |
|---|---|---|---|
| `examination_state` | 68 | `u32 state`、`u32 chances_used`、`u32 chances_total`、`u32 playsec_total`、`u32 playsec_elapsed`、`u32 playscore_sum`、`array<{u32 id, u32 gain_val},5> examination_list`(40)、`u32 interval_cnt` | 读 `0xB42330`；名 `sub_B47910`（`0xB47932 State`/`0xB47959 chances_used`/`0xB47980 chances_total`/`0xB479A7 playsec_total`/`0xB479CE playsec_elapsed`/`0xB479F5 playscore_sum`/`0xB47A17 examination_list`/`0xB47A76 interval_cnt`）；元素 `sub_B478A0`（`id`/`gain_val`） |
| `cshist` 元素 | 6 | `u32 item_id`、`u16 num` | 读 `sub_B423F0`（`0xB4240C` u32 + `0xB4241F` u16）；名 `sub_B47AA0`（`0xB47AC0 item_id`、`0xB47AE3 num`） |
| `hav_rental_modules` 元素 | 8 | `u32 module_id`、`u32 count` | 读 `sub_B434B0`（2 × u32）；名 `0xB4859A module_id`、`0xB486BF count` |
| `favms_arr` 元素 | 66 | `u32 pilot_id`、`u32 favorite_ms_id`、`u8 battle_rule`、`u32 favorite_exp_sum`、`u32 kill_cnt`、`u32 kill_assist_cnt`、`u32 resurrect_cnt`、`u32 stghold_damage`、`u32 battle_cnt`、`u32 score_max_atk`、`u32 score_max_spt`、`u32 score_max_con`、`u32 score_sum_atk`、`u32 score_sum_spt`、`u32 score_sum_con`、`u32 score_sum_sum`、`u32 last_update`、`u8 dirty_flag` | 读 `sub_B424D0`（`0xB424EA/0xB424FF/0xB42515/0xB4252F/0xB4253B/0xB4254B/0xB42560/0xB42575/0xB4258A/0xB4259F/0xB425B0/0xB425C1/0xB425D2/0xB425E3/0xB425F4/0xB42605/0xB42616/0xB42630`）；名 `sub_B47CC0`（`0xB47CE0 pilot_id` … `0xB47F74 dirty_flag`）；**内存步进 `0x48`=72 ≠ 线长 66** |
| `beginner_challenge_info` | 454 | `u32 begin_time`、`u16 elapsed_days`、`array<u16,32> archived`(64)、`array<u32,96> value`(384) | 读 `sub_B42440`；名 `sub_B47B90`（`0xB47BB2 begin_time`、`0xB47BDA elapsed_days`、`0xB47BFD archived`、`0xB47C61 value`） |

## 4. 分析记录

### 4.1 定位过程
1. 名字符串 `0xEE9F74` 的引用点 `0xB539E5` 落在 `sub_B51930` 的 case 块 `0xB53684..0xB53E2B` 内。
2. 块首 `0xB53684 push 16h; call sub_B41120` 与全部错误路径（`0xB536EE`、`0xB539B1`）一致使用错误码 `0x16`。
3. 逐字段「缓冲预留 + 有界读取」成对出现；第 7 字段为 `sub_B41260`（claim `0xDB10`）+ `sub_B42640`（复合读取器）。
4. 块内 18 条日志格式串（`0xB53A3B..0xB53CF0`）与读取顺序一一对应 ⇒ 顶层字段名取证。
5. `pilot_detail` 成员名取自打印器 `sub_B48010`（904 条指令）及其内嵌打印器 `sub_B47910`/`sub_B47CC0`/`sub_B47B90`/`sub_B47B10`/`sub_B47AA0`/`sub_B478A0`，与读取器各调用的内存偏移一一对应。

### 4.2 长度闭合
- 定长部分：`4×4 + 8 + 4 + 51672 + (1+1+4+1+4+4+4) + 1 + 4 = 16+8+4+51672+19+1+4 = 51724`；加串 `L+1` ⇒ **总线长 `51725+L`**（`L ≤ 64`）✓
- 闭合点 `0xB539A2` 要求「游标 == 报文末尾」⇒ 变长部分精确闭合 ✓
- 容量分解（三重一致性）：`28 + 0xDB10 + 19 + 0x41 + 5 = 56197 = 0xDB85` ✓；其中
  - `0xDB10`（`sub_B41260` 的 `0xB4126A add dword ptr [ecx], 0DB10h`）= `pilot_detail` 的**结构体 claim = 结构体跨度**（末成员 `beginner_challenge_info` @ `+0D948h`，跨度 456 ⇒ `0D948h+0x1C8 = 0xDB10`）——**不是**线长（线长 51672，差 4408B 来自元素级「线 66 / 内存 72」等紧凑差）；
  - `0x41`（`0xB53932`）= `heroms_term` 的**槽位预算**（`L ≤ 64`），**不是**串长。
- 容量 ≥ 线长：`56197 ≥ 51789`（`L=64` 时）✓

### 4.3 去向：`vt[0x94]`（18 个实参，压栈 = 逆序）

`level_point, flag_wideuse, heroms_term, ncafe_compcnt, daily_compcnt, accum_playtime, overplay_type, vip_lv, is_processing_comeback, is_netcafe, pilot_detail, tuto_missionid, tuto_flags(hi), tuto_flags(lo), tuto_step, charge_point, restore_channel, result`
（`0xB53D46..0xB53DCF` 依次 push；`0xB53DA0 mov edx,[edx+94h]`；`0xB53DD2 call edx`）

### 4.4 存疑点
见 `notes.md`（枚举/单位、`favms_arr` 的 720 上限来源、`vt[0x94]` 去向、分帧上限）。

## 5. 质量门自检

- [x] G1 字段表总长（`51725+L`）与 `0xB539A2`/`0xB539A8` 的「游标 == 末尾」校验一致；容量 56197 已说明为「Σ各字段 claim（含结构体 claim 与串槽预算）」，并与结构体跨度互证。
- [x] G2 全部线类型指回汇编 VA（u8 `0xB06249`；u16 `0xB02E0B`；u32 `0xB02DE9`；u64 `0xB06220`；串 `0xB5393E`+`0xB02BEE`；结构体/数组读取器 `0xB42640` 及其被调 `0xB42330`/`0xB423F0`/`0xB434B0`/`0xB424D0`/`0xB42440`、`0xB02BA0`）；未使用伪代码类型。
- [x] G3 顶层 17 字段含义取自块内 18 条日志串；`pilot_detail` 的 53 个成员与全部元素结构均取自对应打印器（成员名 + 内存偏移），用途追到 `vt[0x94]`（`0xB53DD2`）。
- [x] G4 不确定项（枚举、单位、位义、`battle_rule`/`dirty_flag` 的符号性、`vt[0x94]` 去向、分帧上限）标 `?` 并记入 `notes.md`。
- [x] G5 README / fields.csv / asm.md 三处一致（`fields.csv` 以单行折叠 `pilot_detail`，明细以本 README §3.1/§3.2 为准）。
- [x] G6 INDEX 状态一致（`DONE`）。
- [x] G7 配对发送侧 `CS-0xF705-lounge-pilot_select` 已在 §1 链接。
