# PLAY_BONUS_REWARD ｜ `reward/play_bonus_reward.csv`

- **用途**：游玩场次/时长奖励：按战斗模式过滤的发放规则
- 表ID `58` ｜ 下载序 `66` ｜ 类名 `CPlayBonusRewardTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_58C440` ｜ **列数 8**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `bonus_id` | u32 | — | 游玩奖励 ID（主键） |
| 2 | `1` | `play_count_min` | u32 | +8 | 最低游玩场次（u32 col1 → +8） |
| 3 | `2` | `play_count_max` | u32 | +12 | 最高游玩场次（u32 col2） |
| 4 | `3` | `time_minutes` | u32 | +16 | 最低游玩时长分钟（u32 col3） |
| 5 | `4` | `reward_gp` | u16 | +20 | ⚠️**客户端拿它当"计数表下标"用**（不是 GP 数量 ✗）：`sub_9D9E10`(0x9DA133)／`sub_9DA260`(0x9DA294) 做 `vec.at(*(i16*)(row+20))`；该 vector = `*(dword_11E3EA4+0x4C)`（50×u16，由 `CGVOProtoLounge` 下发）⇒ **占位期必须写 `65535`**（i16=−1 ⇒ 跳过分支、不读 vector ✓）；写 `0` 会 `std::out_of_range` 崩「交换所」✗（定案见 `.codebuddy/memory/topics/20-客户端崩溃取证SOP.md` §4.1） |
| 6 | `5` | `reward_item_qty` | u16 | +22 | 奖励物品数量（u16 col5） |
| 7 | `6` | `reward_item_id` | u32 | +32 | 奖励物品 ID（u32 col6 → ITEM） |
| 8 | `7` | `battle_mode_code` | u32 | +24 | 适用战斗模式编码（u32 col7 → +24；高 9 位解码写入 +4 为 1/5/6/99 模式过滤） |

**Gap 列**（CSV 存在但读表函数跳过，默认 0）：
- CSV `8`：CSV 列存在但 IDA 读表未单独取证（默认 0）

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。

**⚠️ 2026-09-30 追加（重要；定案见 `.codebuddy/memory/topics/20-客户端崩溃取证SOP.md` §4.1）**：

- col4 **不是"GP 数量"**（旧注释名 `reward_gp` 是猜的 ✗）：客户端语义 = 「**计数表下标**」——
  `remaining = col5 − vec[col4]`（`col5` = `reward_item_qty` @ +22；`vec` = 50×u16 的"已消耗/已获得"表）。
- 该 `vec`（`*(dword_11E3EA4 + 0x4C)`）由 **`CGVOProtoLounge` 下发**（写者 `sub_429340` ← `sub_AFA360`
  ← vtable 段 `0x00EEE044` = `sub_BAD830`）⇒ **本服尚未实现** ⇒ 恒为空 `(0,0,0)` ✓
- ⇒ **占位期 col4 一律写 `65535`**（i16 = −1 ⇒ 走 `v23 < 0` 分支：只置 0x10000 标志、**不读 vector** ✓）；
  写 `0`（或任何 ≥ 0 且 < 50 的值）在 vec 为空时 **必然 `std::out_of_range`**，一进「交换所」就崩 ✗

**⚠️ 2026-09-30 追加 ②（服务端口径 + "到底改哪儿才生效"；完整链条见
`.codebuddy/memory/topics/20-客户端崩溃取证SOP.md` §4.2）**：

- 本列**两侧同名不同义**（必须同时看，别只改一边）：
  - **客户端**：i16 **计数表下标**（`vec.at(*(i16*)(row+20))`）⇒ 写 `65535` 才安全 ✓；
  - **本服**（`serverv/internal/store/item_ops.go` 的 `reward_gp`）：**要发的 GP 数量**
    （`creditPilotMoney`）⇒ 照字面发 = 点一次白拿 65535 GP ✗。
- ⇒ 闸门已在服务端加好：`cfgPlayBonusNoCounterMin = 0x8000`
  （`reward_gp ≥ 0x8000` = 客户端的"非下标"区 ⇒ 一律 `ItemOpNoReward` ⇒ 回 `-10002`：
  不发货、不动钱、**不写** `last_play_bonus`）；单测 `TestItemOpsPlayBonusGrantAndClaimed` 第 ⑦ 步钉死 ✓。
- **运行时数据源是数据库**（真库跑 `serverv`：`gate=:1633 … cfg: 77 tables from database` ✓）：
  客户端下载到的那份 CSV = `meta.cfg_manifest.raw_csv`（`ExportTableRawCSV` 按本表列序导出 ——
  `bonus_id, play_count_min, play_count_max, time_minutes, reward_gp(=CSV#4), reward_item_qty,
  reward_item_id, battle_mode_code, reserved_u32_8`，`_row_id` 不导 ✓）。
  ⇒ 改 `server/datafiles/lounge/reward/play_bonus_reward.csv` **只是 bootstrap 一次性源**，
  不重导**不生效** ✗。正路二选一：GM 改行（自动重算 `raw_csv`）／
  `UPDATE cfg."PLAY_BONUS_REWARD" SET reward_gp='65535' WHERE …` +
  `cd serverv; go run ./tools/cfgsync -schema-dir ../db_design/schema/cfg/tables -export-only -migrate=false` ✓。
- 真实上线条件：等 50×u16 的 `vec` 由大厅协议下发之后，col4 才能恢复 `0..49` 的真下标，
  同时**删掉**数据的 `65535` 与上闸门（两者是一对）✓。

