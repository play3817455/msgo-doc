# W11 · `pilot_detail`（`0x063E` 第 7 段）**字段总表（独立数据表）**

> 目的：把 `pilot_detail` 的**每个字段**列清楚，供服务端"按表填值"与"逐项核对"使用。
> 权威来源（三证）：
> ① **字段名顺序** = `sub_B48010`（调试打印器，`0xB48010`..`0xB48C02`）里按序的 `push offset "xxx="` ✓✓✓
> ② **线偏移/内存偏移/类型** = `sub_B42640`（线→内存**解析器**）＋ 5 个子解析器 ✓
> ③ **消费者** = `sub_437040`（`0x063E` 业务回调）被写入的 `app` 字段 ✓
>
> 日期：2026-09-16 ｜ exe：`GundamOnline_CHINA_v15.exe`（基址 `0x400000`，已脱壳）

---

## 0. 一句话

`pilot_detail` 线长 **51672B**、客户端内存 **56080B**（差 4408B 全为 dword 对齐 padding）。
共 **53 个字段**。**服务端只管"线格式"**；`sub_437040` 读的是**内存偏移**（下表两列都给 ✓）。

**★ 军衔相关字段只在尾部**（线 51128..51203，共 76B）：

| 字段 | 线偏移 | 落点 |
|---|---|---|
| `lvjudge_hist` | 51128 | `app+55528` |
| `sc_lv_up_reward_get` | 51140 | `app+55544` |
| `sc_lv_max_pre` | 51178 | `app+55582` |
| **`sc_lv_max`** | **51202** | **`app+455328`（= `app+0x6F2A0`）** ← ★★★ **「军衔」** |

---

## 1. 权威字段名清单（`sub_B48010` 打印顺序，共 53 项 ✓）

```
 1 exp=                          28 rokaku_pt_use=
 2 money=                        29 cshist=
 3 clan_id=                      30 second_chance_free=
 4 clan_memb_exp=                31 second_chance_free_upd=
 5 clan_forbidden=               32 hav_rental_modules=
 6 cupteam_id=                   33 dc_point=
 7 deckcost=                     34 favms_arr=
 8 last_battle=                  35 heroms_grants=
 9 cw_chscore=                   36 heroms_uniqid=
10 score_special_a=              37 last_period_bonus=
11 last_play_bonus=              38 daily_battle_bonus_flg=
12 last_play_bonus_vsl=          39 last_daily_battle_bonus=
13 last_play_bonus_vsl_cnt=      40 check_progress_quest_id=
14 last_dormant_ret_cc=          41 lvjudge_hist=            ★
15 capture_bonus_state=          42 pilot_made_timestamp=
16 capture_bonus_limit=          43 newpilot_challenge_nextindex=
17 clan_rokaku_btime_limit=      44 newpilot_challenge_last=
18 comment=                      45 sc_lv_up_reward_get=     ★
19 hav_medal=                    46 sc_lv_max_pre=           ★
20 hav_emblem=                   47 sc_lv_max=               ★★★「军衔」
21 hav_avatar=                   48 last_pilot_channel_in=
22 hav_voice=                    49 monthly_bonus_holding_id=
23 hav_modules=                  50 monthly_bonus_logincnt=
24 examination_state=           51 monthly_bonus_xwarcnt=
25 rokaku_uniq_msid=            52 periodpath_end=
26 rokaku_space_uniq_msid=      53 beginner_challenge_info=
27 rokaku_pt=
```

---

## 2. 逐字段总表（★核心交付）

> 线偏移从 `pilot_detail` 体第 0 字节起算（不含 `0x063E` 的 2B ID 与前面 28B 顶层字段）。

### 2.1 头部标量（线 0..63）

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 落点 | 状态 |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 0 | u32 | `exp` | ★**经验值**（**不是 pilot_id** ✗） | — | 已填 9999999 ✓ |
| 2 | 4 | 4 | u32 | `money` | GP（大厅 HUD ✓） | `app+455088` | 已填 9999999 ✓ |
| 3 | 8 | 8 | u32 | `clan_id` | 战队 ID | — | 0 |
| 4 | 12 | 12 | u32 | `clan_memb_exp` | 战队成员经验 | — | 0 |
| 5 | 16 | 16 | u32 | `clan_forbidden` | 战队禁入（按 byte 低字节） | `app+455004` | 0 |
| 6 | 20 | 20 | u32 | `cupteam_id` | 杯赛队伍 ID | — | 0 |
| 7 | 24 | 24 | u16 | `deckcost` | 编成消耗 | `app+455064` | 0 |
| 8 | 26 | 28 | u32 | `last_battle` | 最后战斗 | — | 0 |
| 9 | 30 | 32 | u32 | `cw_chscore` | CW 最高分 | — | 0 |
| 10 | 34 | 36 | u32 | `score_special_a` | 特殊评分 A | `app+455160` | 0 |
| 11 | 38 | 40 | u32 | `last_play_bonus` | 最后游玩奖励 | — | 0 |
| 12 | 42 | 44 | u32 | `last_play_bonus_vsl` | VSL 奖励 | — | 0 |
| 13 | 46 | 48 | u16 | `last_play_bonus_vsl_cnt` | VSL 次数 | — | 0 |
| 14 | 48 | 52 | u32 | `last_dormant_ret_cc` | 休眠回归 CC | — | 0 |
| 15 | 52 | 56 | u32 | `capture_bonus_state` | 捕获奖励状态 | — | 0 |
| 16 | 56 | 60 | u32 | `capture_bonus_limit` | 捕获奖励上限 | — | 0 |
| 17 | 60 | 64 | u32 | `clan_rokaku_btime_limit` | 战队虏获时限 | — | 0 |

★ 线 24 是 u16，之后回 u32（线无 padding）；内存 26/27、50/51 为空洞 ✓

### 2.2 `comment`（线 64..178，115B）

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 状态 |
|---|---|---|---|---|---|---|
| 18 | 64 | 68 | 115B | `comment` | 定长 115B 文本 | 0 |

### 2.3 `hav_*` 拥有数组（线 179..2226）

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 元素 | 含义 | 状态 |
|---|---|---|---|---|---|---|---|
| 19 | 179 | 184 | u64×16 | `hav_medal` | 16 | 拥有勋章 | **已填 0xFF（全拥有 ✓）** |
| 20 | 307 | 312 | u64×8 | `hav_emblem` | 8 | 拥有徽章 | 已填 0xFF ✓ |
| 21 | 371 | 376 | u64×160 | `hav_avatar` | 160 | 拥有头像（主列表） | 已填 0xFF ✓ |
| 22 | 1651 | 1656 | u64×8 | `hav_voice` | 8 | 拥有语音 | 已填 0xFF ✓ |
| 23 | 1715 | 1720 | u32×128 | `hav_modules` | 128 | 拥有模块 ID | 已填 0xFF ✓ |

★ 线长：128 / 64 / 1280 / 64 / 512 ⇒ 179→307→371→1651→1715→**2227** ✓

### 2.4 ★★★ `examination_state`（线 2227..2294，68B）—— **考试状态**

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 状态 |
|---|---|---|---|---|---|---|
| 24a | **2227** | 2232 | u32 | `state` | **考试 ID / 当前军衔**（★标题用它） | 已填 **1** ✓ |
| 24b | 2231 | 2236 | u32 | `chances_used` | 已用次数 | 已填 `exPoint` ✓ |
| 24c | 2235 | 2240 | u32 | `chances_total` | 总次数 | 已填 `exPoint` ✓ |
| 24d | 2239 | 2244 | u32 | `playsec_total` | 总游玩秒数 | 已填 `exPoint` ✓ |
| 24e | 2243 | 2248 | u32 | `playsec_elapsed` | 已流逝秒数 | 1 |
| 24f | 2247 | 2252 | u32 | `playscore_sum` | 评分和 | 1 |
| 24g | 2251..2290 | 2256..2295 | 8B×5 | `examination_list` | 5 × `{id, gain_val}` | 1 |
| — | **2251** | **2256** | u32 | ★ **`examination_list[0].id`** | **← 面板读的 `a2[3]`！** | **已填 `exPoint` ✓** |
| 24h | 2291 | 2296 | u32 | `interval_cnt` | 间隔计数（剩余 N 战） | 已填 **5** ✓ |

**★ 关键映射（P65/P66 实证 ✓）**：`sub_42DBA0` 把 `examination_list[0].id`（段内 **+24**）
写入 `app+112288+12`，而 `sub_9DE9B0` 读它 ⇒ **军衔 = 值/10000%100** ✓

### 2.5 `rokaku_*`（线 2295..2318，24B）

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 状态 |
|---|---|---|---|---|---|---|
| 25 | 2295 | 2304 | u64 | `rokaku_uniq_msid` | 虏获唯一 MS ID | 0 |
| 26 | 2303 | 2312 | u64 | `rokaku_space_uniq_msid` | 宇宙虏获 MS ID | 0 |
| 27 | 2311 | 2320 | u32 | `rokaku_pt` | 虏获点数 | 0 |
| 28 | 2315 | 2324 | u32 | `rokaku_pt_use` | 已用 | 0 |

### 2.6 `cshist`（线 2319..2510，192B）

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 状态 |
|---|---|---|---|---|---|---|
| 29 | 2319 | 2328 | 6B×32 | `cshist` | 32 × `{item_id u32, num u16}` 通关记录 | 0 |

★ 线 6B/元素，内存 8B/元素（+2B padding）⇒ 内存 256B ✓

### 2.7 `second_chance`（线 2511..2515，5B）

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 落点 | 状态 |
|---|---|---|---|---|---|---|---|
| 30 | 2511 | 2584 | u8 | `second_chance_free` | 二度机会免费 | `app+455165` | 0 |
| 31 | 2512 | 2588 | u32 | `second_chance_free_upd` | 更新时间 | — | 0 |

### 2.8 `hav_rental_modules`（线 2516..3539，1024B）

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 状态 |
|---|---|---|---|---|---|---|
| 32 | 2516 | 2592 | 8B×128 | `hav_rental_modules` | 128 × `{module_id, count}` 租借模块 | 0 |

### 2.9 `dc_point`（线 3540..3543，4B）

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 状态 |
|---|---|---|---|---|---|---|
| 33 | 3540 | 3616 | u32 | `dc_point` | 编成点数 | 0 |

### 2.10 ★★★ `favms_arr`（线 3544..51063，**720×66B = 47520B**，最大头）

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 状态 |
|---|---|---|---|---|---|---|
| 34 | 3544 | 3620 | 66B×720 | `favms_arr` | 720 条「最爱机体」＝**机库机体列表** | 0（★可填 ✓） |

★ 线 66B/条，内存 72B/条（+6B padding）⇒ 内存 51840B ✓
★ 条目内字段见 §3.1（★这是「机师详情 → 机体清单」的**正源**，此前我们只修了 `0x3620` 那条替代链 ✗）

### 2.11 `heroms_*`（线 51064..51127，64B）

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 落点 | 状态 |
|---|---|---|---|---|---|---|---|
| 35 | 51064 | 55460 | u32×10 | `heroms_grants` | 10 个英雄机师授予 ID | — | 0 |
| 36 | 51104 | 55504 | u64 | `heroms_uniqid` | 英雄机师唯一 ID | — | 0 |
| 37 | 51112 | 55512 | u32 | `last_period_bonus` | 最后周期奖励 | — | 0 |
| 38 | 51116 | 55516 | u32 | `daily_battle_bonus_flg` | 每日战斗奖励标志 | `app+455192` | 0 |
| 39 | 51120 | 55520 | u32 | `last_daily_battle_bonus` | 最后每日奖励 | — | 0 |
| 40 | 51124 | 55524 | u32 | `check_progress_quest_id` | 进度检查任务 ID | — | 0 |

### 2.12 ★★★ **尾部标量/小数组（线 51128..51217，90B）—— 「军衔」就在这里**

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 落点（app） | 状态 |
|---|---|---|---|---|---|---|---|
| 41 | **51128** | 55528 | u16 | `lvjudge_hist` | ★ **等级判定历史位图** | — | 已填 18 ✓ |
| 42 | 51130 | 55532 | u32 | `pilot_made_timestamp` | 机师创建时间戳 | — | 0 |
| 43 | 51134 | 55536 | u16 | `newpilot_challenge_nextindex` | 新手挑战下一索引 | `app+455792` | 0 |
| 44 | 51136 | 55540 | u32 | `newpilot_challenge_last` | 新手挑战最后值 | — | 0 |
| 45 | **51140** | 55544 | u16×19 | `sc_lv_up_reward_get` | ★ **19 个「升级奖励已领」** | — | 已填 18 ✓ |
| 46 | **51178** | 55582 | u16×12 | `sc_lv_max_pre` | ★ **12 个「等级上限预」** | `app+455332`（首元素） | 已填 18 ✓ |
| 47 | **51202** | 55606 | u16 | **`sc_lv_max`** | ★★★ **「等级上限」= 军衔** | **`app+455328`**（= `app+0x6F2A0`）| **已填 18 ✓** |
| 48 | 51204 | 55608 | u32 | `last_pilot_channel_in` | 最后进入频道 | — | 0 |
| 49 | 51208 | 55612 | u16 | `monthly_bonus_holding_id` | 月奖励持有 ID | `app+455794` | 0 |
| 50 | 51210 | 55614 | u16 | `monthly_bonus_logincnt` | 月奖励登录次数 | `app+455796` | 0 |
| 51 | 51212 | 55616 | u16 | `monthly_bonus_xwarcnt` | 月奖励 X 战次数 | `app+455798` | 0 |
| 52 | 51214 | 55620 | u32 | `periodpath_end` | 周期路径结束 | — | 0 |

★ **`sc` = `soldier class` = 军衔** ✓；`sc_lv_max` ↔ 报文 `0xB2C1 season_class_level_max_update` ✓
★ 实测（x64dbg，2026-09-16）：`app+0x6F2A0 = 18` ✓、`app+0x6F10C = 18` ✓（两处一致 ✓）

### 2.13 `beginner_challenge_info`（线 51218..51671，454B）

| # | 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 状态 |
|---|---|---|---|---|---|---|
| 53a | 51218 | 55624 | u32 | `begin_time` | 开始时间 | 0 |
| 53b | 51222 | 55628 | u16 | `elapsed_days` | 已过天数 | 0 |
| 53c | 51224 | 55630 | u16×32 | `archived` | 32 个归档标志 | 0 |
| 53d | 51288 | 55696 | u32×96 | `value` | 96 个值 | 0 |

---

## 3. 子结构

### 3.1 `favms_arr` 条目（线 66B / 内存 72B）

> 解析器 `sub_B424D0` + 打印器 `sub_B47CC0`（★语义待逐个落地）

| 线内偏移 | 类型 | 候选字段名 | 说明 |
|---|---|---|---|
| +0 | u32 | `msma_id` | ★ 机体定义主键（最可能） |
| +4 | u32 | `uniqid` | 实例 ID |
| +8 | u8 | `level` / `flags` | 待定 |
| +12 | u32 | — | 待定 |
| +16..+64 | 13×u32 | — | 待定（强化/配色/熟练度等） |
| +68 | u32 | — | 待定 |

★ 已知：**上限 720**（`0xB5C51D cmp ebx,2D0h` ✓）、步长 **+0x48=72**（内存 ✓）、线 **66B** ✓
★ 已知实测（P47）：`0x3620 pilot_favms_get` 体 = `result(4) | pilot_id(4) | world_id(4) | count(4) | count×72B` ✓

---

## 4. 服务端填写检查表（★按此逐项核对）

| 关注点 | 字段 | 线偏移 | 目标值 | 现状 |
|---|---|---|---|---|
| 经验/GP | `exp` / `money` | 0 / 4 | 9999999 | ✓ |
| 装扮可选 | `hav_medal/emblem/avatar/voice/modules` | 179/307/371/1651/1715 | 全 0xFF | ✓ |
| 考试标题 | `examination_state.state` | 2227 | 1 | ✓ |
| **考试面板军衔** | `examination_list[0].id` | **2251** | **`exPoint` = 180000** | ✓（落 `app+112288+12` ✓）|
| 剩余战数 | `interval_cnt` | 2291 | 5 | ✓ |
| **军衔（上限）** | **`sc_lv_max`** | **51202** | **18** | **✓（落 `app+0x6F2A0` ✓）** |
| 军衔（判定） | `lvjudge_hist` | 51128 | 18 | ✓ |
| 军衔（奖励） | `sc_lv_up_reward_get` | 51140 | 18 | ✓ |
| 军衔（上限预） | `sc_lv_max_pre` | 51178 | 18 | ✓ |
| **机库机体** | `favms_arr` | 3544 | 720 × 66B | ✗ **未填**（可填 ✓） |

---

## 5. ⚠️ 仍未定 / 待查

1. **`app+0x6F12C`（第二军衔门槛）恒 0** ✗
   - 唯一写者 = `sub_42EF30`（`0x42EF44`）✓；调用链 `sub_BAB350`（native 表 `0xEEDC24`）→ `sub_AF7950` → `sub_42EF30` ✓
   - **实测：断点从未命中** ⇒ 那一路**从未被调用** ⇒ 值恒 0 ✗
   - 影响：「**晋升为下士后可以使用**」（`0x8A0241 cmp [eax+6F12Ch], edi` ⇒ 提示串 `0xFFFFD457`）✗
   - ⇒ **需要找到"应该触发 `sub_BAB350` 的那条报文"并主动下发** ⚠️
2. **内存/线 padding 合计 4394B ≠ 4408B**（差 14B，⚠️见 W09 §7）
3. `favms_arr` 条目 66B 的**逐字段语义**尚未逐个落地（§3.1）
4. 头部标量里 `exp` 与 `pilot_id` 的**历史误记**已修正（见 W09 §6）✓

---

## 6. 变更记录

| 日期 | 变更 |
|---|---|
| 2026-09-16 | 建表：以 `sub_B48010` 的 138 个字符串为**字段名权威顺序**，与 W09 偏移表交叉验证；补「落点 app 字段」列与「服务端填写检查表」✓ |
