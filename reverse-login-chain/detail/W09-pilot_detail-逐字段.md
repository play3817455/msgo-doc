# W09 · `pilot_detail` 51672B 内部结构逐字段

> 工作项：`W09`（P1）｜ 判据：**偏移表逐条（0 → 51672），每个子数组给出步长 / 条数上限 / 字段含义**
> 目标文件：`GundamOnline_CHINA_v15.exe`（基址 `0x400000`，已脱壳）
> 方法：IDA Pro MCP 反编译 `sub_B42640`（线→内存**解析器**）＋ `sub_B41260`（内存步长）＋ `sub_437040`（0x063E 业务**消费者**）＋ `sub_B48010`（**调试打印器，字段名权威来源**）＋ 5 个子结构解析器（`sub_B42330`/`sub_B423F0`/`sub_B434B0`/`sub_B424D0`/`sub_B42440`）＋ 4 个子打印器（`sub_B47910`/`sub_B47B10`/`sub_B47CC0`/`sub_B47B90`）
> 日期：2026-09-15 ｜ 上游 `detail/W08-pilot_select-逐字段.md` ＋ `server/internal/protocol/lounge.go` + `server/internal/authsrv/server.go`
> 标注：✅ 本轮反编译直接确认 ｜ ★ 本轮新增/修正 ｜ ⚠️ 仍未定

---

## 0. 一句话结论

`pilot_detail`（`0x063E` 第 7 段）线长 **51672B**、客户端内存结构 **56080B**（差 4408B 全是子数组的元素内存对齐 padding，§4.1 逐项定位）。它由 **53 段**字段组成（本文按 13 组归并呈现）：**头部 17 个标量（0..63）+ comment 115B + 5 个 `hav_*` 拥有数组 + `examination_state` 68B + 4 个 `rokaku_*` + `cshist` 192B + `second_chance` 5B + `hav_rental_modules` 1024B + `dc_point` 4B + **`favms_arr` 720×66B（最大头，47520B）** + `heroms_*` 64B + 尾部 12 个标量/小数组（90B）+ `beginner_challenge_info` 454B。★**全部字段对「进大厅」都不门控**（门控在 `0x063E` 外层的 `is_processing_comeback`，见 W08）⇒ 服务端可**整块零填**也进得去；但 ★**`pilot_detail[0]` 是 `exp`（经验值），不是 `pilot_id`** —— W08/`server.go` 把它写成 `pilot_id` 是**认错字段**（详见 §6）。

---

## 1. 汇编逻辑

### 1.1 调用链

```
【0x063E 应答解析】 sub_B51930 case 0x063E（alloc 56201 = 121 顶层 + 56080 pilot_detail）
   └─ 17 段顶层字段读入结果结构（W08 §3.2）
   └─ 第 7 段 = pilot_detail：调用 sub_B42640(结果结构内的 pilot_detail 指针, &线游标)
         └─ 把 51672B 线数据 → 56080B 内存结构（逐字段读，越界即 return 0 = 整包丢弃）
   └─ vt[0x94] = sub_AF7790 → sub_437040(app, result, …, pilot_detail*, …)
         └─ 只消费 pilot_detail 的 16 处子段（见 §5），写 app 对象

【字段名来源】 sub_B48010（调试打印器，0x063E case 日志 @0xB53B41 调用）按顺序打印每个字段名
【内存步长】   sub_B41260：*(_DWORD*)buf = 指针；buf += 56080（= 单个 pilot_detail 内存尺寸）
```

### 1.2 关键函数表

| 地址 | 身份 | 作用 |
|---|---|---|
| `sub_B42640` | ★pilot_detail **解析器**（线→内存） | 逐字段读，是**线格式的权威定义** |
| `sub_B41260` | 内存步长助手 | 返回指针并把游标 `+= 56080`（内存结构尺寸） |
| `sub_437040` | 0x063E 业务**消费者** | 只读 16 处子段写入 app 对象（§5） |
| `sub_B48010` | ★**调试打印器** | 按顺序打印每个字段名（**字段命名权威**） |
| `sub_B42330` | examination_state 解析器 | 68B（6 u32 + 5×8B + 1 u32） |
| `sub_B423F0` | cshist 解析器 | 32 ×（u32 + u16）= 192B |
| `sub_B434B0` | 8B 元素解析器 | 2 × u32（examination_list / hav_rental_modules 共用） |
| `sub_B424D0` | favms_arr 条目解析器 | 66B 线 / 72B 内存 |
| `sub_B42440` | beginner_challenge_info 解析器 | 454B 线 / 456B 内存 |
| 读取原语 | `sub_B02DD0`=u32 / `sub_B02DF0`=u16 / `sub_B06230`=u8 / `sub_B06200`=u64 | 越界返回 0 ⇒ 整包丢弃 |

### 1.3 线格式 vs 内存格式（★两者不同，勿混）

- **线格式 51672B**：连续字节流，无对齐 padding（`sub_B42640` 逐字段读，游标线性前进）。
- **内存格式 56080B**：`sub_B42640` 写入结果结构；字段按 dword 对齐，产生 padding。
- padding 来源：头部 2 个 u16（mem 24/48）各留 2B 空洞（4B）；`examination_state` 后 4B 空洞；`cshist` 每元素 6B→8B（+64B）；`favms_arr` 每元素 66B→72B（+6×720=4320B）；`beginner_challenge_info` 454B→456B（+2B）。合计 4+4+64+4320+2 = 4394B … 与 4408 差 14B（见 §7 ⚠️1）。

> 服务端只管**线格式**；`sub_437040` 读的是**内存偏移**（下表两列都给出，便于对照）。

---

## 2. 逐字段表（★核心交付）

> 线偏移从 `pilot_detail` 体第 0 字节起算（不含 0x063E 的 2B ID 与 0x063E 前 28B 顶层字段）。
> 「内存偏移」= 解析后结果结构内的 dword 偏移（`sub_437040` / `sub_B48010` 的口径）。

### 2.1 头部标量（线 0..63，共 64B）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 | 客户端消费 |
|---|---|---|---|---|---|
| 0 | 0 | u32 | `exp` | ★**经验值**（W08 误记为 pilot_id，见 §6） | 否（sub_437040 不读） |
| 4 | 4 | u32 | `money` | 资金/GP | ✅→app+455088 |
| 8 | 8 | u32 | `clan_id` | 战队 ID | 否 |
| 12 | 12 | u32 | `clan_memb_exp` | 战队成员经验 | 否 |
| 16 | 16 | u32 | `clan_forbidden` | 战队禁入标志（客户端按 **byte** 读低字节→app+455004） | ✅(低字节) |
| 20 | 20 | u32 | `cupteam_id` | 杯赛队伍 ID | 否 |
| 24 | 24 | u16 | `deckcost` | 编成消耗（deck cost） | ✅→app+455064 |
| 26 | 28 | u32 | `last_battle` | 最后战斗（时间戳/编号） | 否 |
| 30 | 32 | u32 | `cw_chscore` | CW 挑战最高分 | 否 |
| 34 | 36 | u32 | `score_special_a` | 特殊评分 A | ✅→app+455160 |
| 38 | 40 | u32 | `last_play_bonus` | 最后游玩奖励 | 否 |
| 42 | 44 | u32 | `last_play_bonus_vsl` | 最后游玩奖励 VSL | 否 |
| 46 | 48 | u16 | `last_play_bonus_vsl_cnt` | 最后游玩奖励 VSL 次数 | 否 |
| 48 | 52 | u32 | `last_dormant_ret_cc` | 最后休眠回归 CC | 否 |
| 52 | 56 | u32 | `capture_bonus_state` | 捕获奖励状态 | 否 |
| 56 | 60 | u32 | `capture_bonus_limit` | 捕获奖励上限 | 否 |
| 60 | 64 | u32 | `clan_rokaku_btime_limit` | 战队虏获战斗时限 | 否 |

- 线 24 是 u16，其后 26 起又回到 u32（线格式**无 padding**）；内存 26/27、50/51 是空洞。

### 2.2 `comment`（线 64..178，115B 定长）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|---|
| 64 | 68 | 115B | `comment` | 定长 **115B** 文本（NUL 填充；打印器按 C 串处理） |

- ⚠️ 与 `api_doc §3.3` 的 `comment varchar(116)` 是**两处不同结构**：那处是 1857B `pilot_record`（0xDC47，归 W12）；这里 pilot_detail 的 comment 是 **115B**（`sub_B42640` 读 0x73=115 字节）。

### 2.3 `hav_*` 拥有数组（线 179..2226）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 元素数 | 元素类型 | 含义 |
|---|---|---|---|---|---|---|
| 179 | 184 | u64×16 | `hav_medal` | 16 | u64 | 拥有的勋章（ID 位图） |
| 307 | 312 | u64×8 | `hav_emblem` | 8 | u64 | 拥有的徽章 |
| 371 | 376 | u64×160 | `hav_avatar` | 160 | u64 | 拥有的头像 |
| 1651 | 1656 | u64×8 | `hav_voice` | 8 | u64 | 拥有的语音 |
| 1715 | 1720 | u32×128 | `hav_modules` | 128 | u32 | 拥有的模块 ID |

- 各数组元素数 = 解析器循环上限（`sub_B42640` 内 `v4>=0x10`/`v6>=8`/`v8>=0xA0`/`v10>=8` + `v12>=0x80` 原始 128 u32）。
- 线偏移增量：179+128=307、307+64=371、371+1280=1651、1651+64=1715、1715+512=2227。

### 2.4 `examination_state`（线 2227..2294，68B）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|---|
| 2227 | 2232 | u32 | `state` | 机体升级考试状态 |
| 2231 | 2236 | u32 | `chances_used` | 已用次数 |
| 2235 | 2240 | u32 | `chances_total` | 总次数 |
| 2239 | 2244 | u32 | `playsec_total` | 总游玩秒数 |
| 2243 | 2248 | u32 | `playsec_elapsed` | 已流逝秒数 |
| 2247 | 2252 | u32 | `playscore_sum` | 游玩评分和 |
| 2251..2290 | 2256..2295 | 8B×5 | `examination_list` | 5 × `{id u32, gain_val u32}`（考试条目） |
| 2291 | 2296 | u32 | `interval_cnt` | 间隔计数 |

### 2.5 `rokaku_*`（线 2295..2318，24B）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|---|
| 2295 | 2304 | u64 | `rokaku_uniq_msid` | 虏获唯一 MS ID |
| 2303 | 2312 | u64 | `rokaku_space_uniq_msid` | 虏获宇宙唯一 MS ID |
| 2311 | 2320 | u32 | `rokaku_pt` | 虏获点数 |
| 2315 | 2324 | u32 | `rokaku_pt_use` | 虏获点数已用 |

### 2.6 `cshist`（线 2319..2510，192B）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|---|
| 2319 | 2328 | 6B×32 | `cshist` | 32 × `{item_id u32, num u16}` 关卡/剧本通关记录 |

- 线元素 = 6B（u32+u16）；内存元素 = 8B（+2B padding）。32 × 8 = 256B 内存（mem 2328..2583）。

### 2.7 `second_chance`（线 2511..2515，5B）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|---|
| 2511 | 2584 | u8 | `second_chance_free` | 二度机会免费（✅→app+455165） |
| 2512 | 2588 | u32 | `second_chance_free_upd` | 二度机会免费更新时间 |

### 2.8 `hav_rental_modules`（线 2516..3539，1024B）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|---|
| 2516 | 2592 | 8B×128 | `hav_rental_modules` | 128 × `{module_id u32, count u32}` 租借模块 |

### 2.9 `dc_point`（线 3540..3543，4B）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|---|
| 3540 | 3616 | u32 | `dc_point` | 编成点数（deck cost point） |

### 2.10 ★`favms_arr`（线 3544..51063，720×66B = 47520B，最大头）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|---|
| 3544 | 3620 | 66B×720 | `favms_arr` | 720 条「最爱机体」记录，逐字段见 §3.1 |

- 线元素 = 66B；内存元素 = 72B（`jj += 18` dword 步长，+6B padding）。720 × 72 = 51840B 内存（mem 3620..55459）。

### 2.11 `heroms_*`（线 51064..51127，64B）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|---|
| 51064 | 55460 | u32×10 | `heroms_grants` | 10 个英雄机师授予 ID |
| 51104 | 55504 | u64 | `heroms_uniqid` | 英雄机师唯一 ID |
| 51112 | 55512 | u32 | `last_period_bonus` | 最后周期奖励 |
| 51116 | 55516 | u32 | `daily_battle_bonus_flg` | 每日战斗奖励标志（✅→app+455192） |
| 51120 | 55520 | u32 | `last_daily_battle_bonus` | 最后每日战斗奖励 |
| 51124 | 55524 | u32 | `check_progress_quest_id` | 进度检查任务 ID |

### 2.12 尾部标量/小数组（线 51128..51217，90B）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|---|
| 51128 | 55528 | u16 | `lvjudge_hist` | 等级判定历史位图 |
| 51130 | 55532 | u32 | `pilot_made_timestamp` | 机师创建时间戳 |
| 51134 | 55536 | u16 | `newpilot_challenge_nextindex` | 新手机师挑战下一索引（✅→app+455792） |
| 51136 | 55540 | u32 | `newpilot_challenge_last` | 新手机师挑战最后值 |
| 51140 | 55544 | u16×19 | `sc_lv_up_reward_get` | 19 个「等级提升奖励已领」标志 |
| 51178 | 55582 | u16×12 | `sc_lv_max_pre` | 12 个「等级上限预」标志（首元素 ✅→app+455332） |
| 51202 | 55606 | u16 | `sc_lv_max` | 等级上限（✅→app+455328） |
| 51204 | 55608 | u32 | `last_pilot_channel_in` | 最后进入频道 |
| 51208 | 55612 | u16 | `monthly_bonus_holding_id` | 月奖励持有 ID（✅→app+455794） |
| 51210 | 55614 | u16 | `monthly_bonus_logincnt` | 月奖励登录次数（✅→app+455796） |
| 51212 | 55616 | u16 | `monthly_bonus_xwarcnt` | 月奖励 X 战次数（✅→app+455798） |
| 51214 | 55620 | u32 | `periodpath_end` | 周期路径结束 |

### 2.13 `beginner_challenge_info`（线 51218..51671，454B）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|---|
| 51218 | 55624 | u32 | `begin_time` | 开始时间 |
| 51222 | 55628 | u16 | `elapsed_days` | 已过天数 |
| 51224 | 55630 | u16×32 | `archived` | 32 个归档标志 |
| 51288 | 55696 | u32×96 | `value` | 96 个值 |

---

## 3. 子结构逐字段

### 3.1 `favms_arr` 条目（66B 线 / 72B 内存，`sub_B424D0` + 打印器 `sub_B47CC0`）

| 线偏移 | 内存偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|---|
| +0 | +0 | u32 | `pilot_id` | 机师 ID |
| +4 | +4 | u32 | `favorite_ms_id` | 最爱机体 ID |
| +8 | +8 | u8 | `battle_rule` | 战斗规则 |
| +9 | +12 | u32 | `favorite_exp_sum` | 最爱机体经验合计 |
| +13 | +16 | u32 | `kill_cnt` | 击坠数 |
| +17 | +20 | u32 | `kill_assist_cnt` | 击坠助攻数 |
| +21 | +24 | u32 | `resurrect_cnt` | 复活数 |
| +25 | +28 | u32 | `stghold_damage` | 据点守备伤害 |
| +29 | +32 | u32 | `battle_cnt` | 战斗次数 |
| +33 | +36 | u32 | `score_max_atk` | 最高分·攻击 |
| +37 | +40 | u32 | `score_max_spt` | 最高分·支援 |
| +41 | +44 | u32 | `score_max_con` | 最高分·指挥 |
| +45 | +48 | u32 | `score_sum_atk` | 累计分·攻击 |
| +49 | +52 | u32 | `score_sum_spt` | 累计分·支援 |
| +53 | +56 | u32 | `score_sum_con` | 累计分·指挥 |
| +57 | +60 | u32 | `score_sum_sum` | 累计分·合计 |
| +61 | +64 | u32 | `last_update` | 最后更新时间 |
| +65 | +68 | u8 | `dirty_flag` | 脏标志 |

### 3.2 `examination_list` 条目（8B，`sub_B434B0` + 打印器 `sub_B478A0`）

| 偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|
| +0 | u32 | `id` | 考试条目 ID |
| +4 | u32 | `gain_val` | 获得值 |

### 3.3 `cshist` 条目（6B 线 / 8B 内存，`sub_B423F0` + 打印器 `sub_B47AA0`）

| 偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|
| +0 | u32 | `item_id` | 关卡/剧本条目 ID |
| +4 | u16 | `num` | 次数 |

### 3.4 `beginner_challenge_info` 内部（`sub_B42440` + 打印器 `sub_B47B90`）

| 偏移 | 类型 | 字段名 | 含义 |
|---|---|---|---|
| +0 | u32 | `begin_time` | 开始时间 |
| +4 | u16 | `elapsed_days` | 已过天数 |
| +6..69 | u16×32 | `archived` | 归档标志 |
| +72..455 | u32×96 | `value` | 值 |

---

## 4. 字节预算自检（线格式恒等 51672）

```
64(头) +115(comment) +128(medal) +64(emblem) +1280(avatar) +64(voice) +512(modules)
+68(exam) +24(rokaku) +192(cshist) +5(second) +1024(rental) +4(dc_point)
+47520(favms) +64(heroms) +90(尾) +454(beginner) = 51672 ✓
```

### 4.1 内存 padding 逐项定位（★4408B 全定位，= 56080 − 51672）

| 位置 | 原因 | 字节数 |
|---|---|---|
| 头部 2 个 u16（mem 24/48） | u16 后对齐 u32 | 2+2 = 4 |
| `comment`(115B @68..182) → `hav_medal`(@184) | u64 对齐 | 1 |
| `examination_state`(68B @2232..2299) → `rokaku`(@2304) | u64 对齐 | 4 |
| `cshist` 32×(6B 线 → 8B 内存) | 每元素 +2 | 64 |
| `second_chance_free`(u8@2584) → `_upd`(u32@2588) | u32 对齐 | 3 |
| `favms_arr` 720×(66B 线 → 72B 内存) | 每元素 +6 | 4320 |
| `heroms_grants`(40B @55460..55499) → `heroms_uniqid`(u64@55504) | u64 对齐 | 4 |
| 尾部 3 处 u16（lvjudge/nextindex/xwarcnt） | u32 对齐 | 2+2+2 = 6 |
| `beginner_challenge_info`(454B → 456B) | 尾对齐 | 2 |

合计 = 4+1+4+64+3+4320+4+6+2 = **4408** ✓

---

## 5. 客户端消费点（`sub_437040` 读哪些 → 写 app）

**✅ 被消费（16 处）**：`money`→app+455088、`clan_forbidden`(低字节)→app+455004、`deckcost`→app+455064、`score_special_a`→app+455160、`second_chance_free`→app+455165、`hav_medal/emblem/avatar/voice`→app+3392/3520/3584/4864、`hav_modules`→app+112424、`examination_state`→app+112288..、`cshist`→app+454612、`hav_rental_modules`→app+112936、`heroms_grants`→app+455208、`heroms_uniqid`→app+455200、`daily_battle_bonus_flg`→app+455192、`newpilot_challenge_nextindex`→app+455792、`sc_lv_max*`→app+455328/455332、`monthly_bonus_*`→app+455794/796/798、`beginner_challenge_info`→app+455336。

**❌ 未被消费**：`exp`、`clan_id`、`clan_memb_exp`、`cupteam_id`、`last_battle`、`cw_chscore`、`last_play_bonus*`、`last_dormant_ret_cc`、`capture_bonus_*`、`clan_rokaku_btime_limit`、`comment`、`second_chance_free_upd`、`dc_point`、`favms_arr`、`last_period_bonus`、`last_daily_battle_bonus`、`check_progress_quest_id`、`lvjudge_hist`、`pilot_made_timestamp`、`newpilot_challenge_last`、`last_pilot_channel_in`、`periodpath_end` —— 它们被解析后留在结果结构里，供后续 UI 读取。

---

## 6. 对服务端落地的影响

1. ★★ **纠偏：`pilot_detail[0]` = `exp`（经验值），不是 `pilot_id`**。`sub_B48010` 打印器首字段 `aExp="exp="` 坐实；`sub_437040` 根本不读 `a9+0`。W08 §4.4「`pilot_detail[0..3]=pilot_id` 让大厅认我是谁」与 `server.go:1055/1087-1091` 的写法**✗作废**（把 pilot_id 写进了 exp 槽）。真正的「认我是谁」不在 pilot_detail 顶层 —— 客户端通过 `favms_arr` 条目内的 `pilot_id` 与 0x063E 外层 `restore_channel`/`charge_point` 关联，机师身份由**选中动作本身**决定。⇒ 建议服务端把 `detail[0..3]` 改为写 `exp`（或 0），并删除「pilot_detail[0]=pilot_id」注释。
2. ★ **整块零填即可进大厅**：所有 pilot_detail 字段对 `sub_43ADD0 case0x14` 开窗门控**均无影响**（门控 = 外层 `is_processing_comeback`，W08 §3.3）。所以「进大厅」的最小实现 = 51672B 全零；要让大厅显示真实数据才需按本表逐字段填。
3. **多帧连发**：51672B 超单帧上限 16366B，`wrap_stream` 已自动切帧（W08 §4.7）。
4. **字段序必须严格**：解析器 `sub_B42640` 每个 case 末尾 `游标 == 报文尾`，任一字段长度错位 ⇒ 整包丢弃 ⇒ 0x063E 解析失败（`app+1400` bit1 不置位，白屏复现）。

---

## 7. 待研究 / 未定

1. ✅ 内存 padding **4408B 全定位**（= 56080 − 51672，见 §4.1），无残留。
2. ⚠️ `lvjudge_hist` 打印器带 `{`（像结构体），但线格式只有 1 个 u16 —— 源里可能是单成员位图结构，线=u16。
3. ⚠️ `hav_medal/emblem/avatar/voice` 元素是 u64「拥有位图」还是「ID 列表」未追数据表侧（`reward/`、`growth/` 下无直接对应种子）；对进大厅无影响。
4. ⚠️ `comment`（115B）与 `pilot_record` 的 `comment`（116B）差 1B，是否同源待 W12 核对。
5. ✅（已承接）`favms_arr`/`cshist` 等与数据表 `growth/ms_favorite.csv`、`reward/beginner_challenge.csv` 的映射，归「服务端真值回填」阶段，非本项静态逆向范围。

---

## 8. 证据地址清单

| 结论 | 证据 |
|---|---|
| 线格式定义 | `sub_B42640`（`*a1=*(*a2)++` … 逐字段 + 各数组循环上限 0x10/8/0xA0/8/0x80/5/0x80/0x2D0/0xA/0x13/0xC） |
| 内存步长 56080 | `sub_B41260`（`*a2 += 56080`） |
| 字段名权威 | `sub_B48010` 打印器（`aExp="exp="`、`aMoney="money="`、`aDeckcost="deckcost="`、`aComment="comment="`、`aHavMedal/Emblem/Avatar/Voice/Modules`、`aExaminationSta`、`aCshist`、`aHavRentalModul`、`aDcPoint`、`aFavmsArr`、`aHeromsGrants/Uniqid`、`aBeginnerChalle` 等） |
| exp（非 pilot_id） | `sub_B48010` `a2[0]` 配 `aExp`；`sub_437040` 首个读是 `a9+4`（money），从不读 `a9+0` |
| 子结构字段名 | `sub_B47910`（examination_state）、`sub_B47B10`（cshist）、`sub_B47CC0`（favms 条目）、`sub_B47B90`（beginner_challenge_info）、`sub_B478A0`（exam 条目）、`sub_B47AA0`（cshist 条目） |
| 子结构线尺寸 | `sub_B42330` 68B / `sub_B423F0` 192B / `sub_B434B0` 8B / `sub_B424D0` 66B / `sub_B42440` 454B |
