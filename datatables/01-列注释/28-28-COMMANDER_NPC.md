# COMMANDER_NPC ｜ `command/commander_npc.csv`

- **用途**：指挥官 NPC 定义
- 表ID `28` ｜ 下载序 `28` ｜ 类名 `CCommanderNpcTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_572EE0` @`0x572EE0`（RTTI `??_7CCommanderNpcTable@@6B@`@`0xecffe8`、ctor `sub_A77960`@`0xA77960`）｜ **列数 50**
- ★2026-10-05 第 7 批订正：旧 schema/注释 **13 列**且 `csv_index` 与真读列**完全错位**（旧注释里的
  "csv12..csv19" 其实是 reader 的**内部列号**，不是 CSV 列位）⇒ 按 reader 的固定块循环改为 **50 列**，
  即 `csv0..csv49`（其中 **11 列是缝**，reader 不读）

## 1. 行布局（`sub_572EE0` 反编译逐条确证）

```c
*(_DWORD*)a3 = sub_BBB370(a1, 0);            // csv0  → +0    键
*(_DWORD*)(a3+4)  = sub_BBB370(a1, 1);       // csv1  → +4
*(_DWORD*)(a3+8)  = sub_BBB370(a1, 2);       // csv2  → +8
sub_4029E0(a3+12, sub_456D90(a1, 3));        // csv3  → +12   wstring
sub_4029E0(a3+40, sub_456D90(a1, 4));        // csv4  → +40   wstring
*(_DWORD*)(a3+68) = sub_572C30(sub_BBB4F0(a1, 5));  // csv5 → +68   势力 enum
*(_DWORD*)(a3+72) = sub_BBB370(a1, 6);       // csv6  → +72
*(_WORD*)(a3+88)  = sub_BBB370(a1, 0xC);     // csv12 → +88   u16
v10 = 13; v11 = a3+92 (u16*); v30 = a3+220 (dword*); n = 3;
do {                                          // 槽组 k = 1..3
    *v11 = sub_BBB370(a1, v10);               // csv{5k+8}  → +88+2k   u16（消耗）
    *v30 = sub_BBB370(a1, v10+1);             // csv{5k+9}  → +220+4k  u32（冷却）
    v10 += 5; ++v11; ++v30;
} while (--n);                                // ⇒ 消耗 csv13/14, 17/18, 21/22
v15 = a3+304 (dword*); n = 12;
do {                                          // 支援槽 k = 1..12
    *(v15-12) = sub_BBB370(a1, v10);             // csv{2k+23} → +256+4(k-1)  u32 原始值
    *v15      = sub_572CD0(sub_BBB4F0(a1, v10+1)); // csv{2k+24} → +304+4(k-1)  类型枚举
    v10 += 2; ++v15;
} while (--n);                                // ⇒ 消耗 csv25..48
*(_DWORD*)(a3+80) = sub_BBB370(a1, v10);     // csv49 → +80
// 12 个类型枚举随后按 switch(*result) 折成 31 位掩码写 +76（bit = 枚举值 0..30）
```

- 结构大小 = **180 dword = 720B**（与 `TIndexTable` 行回调 `sub_A74EF0` 的 `720` 缓冲一致）。
- 取值函数：`sub_BBB370` = **atoi**（整数）；`sub_456D90` = **wstring 取列**；`sub_BBB4F0` = **窄串取列**（给枚举查表）。
- ★**本表索引键 = csv0**：vtable[5] = `sub_A564D0`（`return sub_BBB370(a1, 0)`）即 GetKey。

## 2. 列位总表（50 列）

| 段 | CSV# | 订案名 | 类型 | 内存 | 说明 |
|---|---|---|---|---|---|
| 头 | `0` | `commander_id` | u32 | +0 | ★**指挥官 ID = 索引键** |
| 头 | `1` | `npc_model_id` | u32 | +4 | NPC 模型 ID（关联 `chara/`） |
| 头 | `2` | `portrait_id` | u32 | +8 | 头像/立绘 ID |
| 头 | `3` | `commander_name` | str | +12 | 指挥官名（wstring） |
| 头 | `4` | `description` | str | +40 | 说明（wstring） |
| 头 | `5` | `faction` | enum `sub_572C30` | +68 | 势力：`NEUTRAL=-1` / `EFF=0` / `ZEON=1` |
| 头 | `6` | `voice_group_id` | u32 | +72 | 语音组 ID（`cutin_voice_*_commander.csv`） |
| 缝 | `7`–`11` | `col7`…`col11` | — | — | **gap**：reader 不读（头 7 列与槽组间 5 列缝） |
| 槽 | `12` | `slot1_cost` | u16 | +88 | 支援槽 1 消耗 |
| 槽 | `13` | `slot2_cost` | u16 | +92 | 支援槽 2 消耗 |
| 槽 | `14` | `slot1_cooldown` | u32 | +220 | 支援槽 1 冷却（**列步长 5 的第 2 项**） |
| 缝 | `15`–`16` | `col15` `col16` | — | — | **gap**：槽组间 2 列缝 |
| 槽 | `17` | `slot3_cost` | u16 | +94 | 支援槽 3 消耗 |
| 槽 | `18` | `slot2_cooldown` | u32 | +224 | 支援槽 2 冷却 |
| 缝 | `19`–`20` | `col19` `col20` | — | — | **gap**：槽组间 2 列缝 |
| 槽 | `21` | `slot4_cost` | u16 | +96 | 支援槽 4 消耗（★**没有槽 4 冷却**，reader 只读 3 个冷却） |
| 槽 | `22` | `slot3_cooldown` | u32 | +228 | 支援槽 3 冷却 |
| 缝 | `23`–`24` | `col23` `col24` | — | — | **gap**：12 组循环前的 2 列缝 |
| 组×12 | `25`,`27`…`47` | `support{1..12}_value` | u32 | +256+4(k-1) | 支援槽原始整数值（atoi；语义未取证） |
| 组×12 | `26`,`28`…`48` | `support{1..12}_type` | enum `sub_572CD0` | +304+4(k-1) | 支援类型（31 值，见下） |
| 尾 | `49` | `unlock_mission_id` | u32 | +80 | 解锁任务 ID |

> ⚠️ 槽组列号 = `{5k+8, 5k+9}`（k=1..3）：`{13,14} {18,19} {23,24}` 里的**第 2 个**才是冷却；
> 但由于列步长 5，实际落在 `csv13/14`、`csv17/18`、`csv21/22`，缝在 `csv15/16` 与 `csv19/20`。

## 3. 枚举表（`sub_572CD0` 支援类型，31 值，0..30）

`BOMB, CARPET_BOMB, TENDER, SEARCH, MINOVSKY, SOLAR_RAY, SUMMON_MA, SUMMON_ACE, BATTLE_SHIP,`
`ASSAULT_SHIP, ORATION, PATROL_AIRCRAFT, AAG, GUNTURRET, EQPARTS_EXEC_A..E, GRENADE_NET,`
`GRENADE_TUMBLE, WALL, DUMMY_BEACON, TRANSPORT_SHIP, STGARMS_OLD, STGARMS1, STGARMS2,`
`SUBFLIGHT, ASSAULT_STGHOLD, RIDE_ACE, JAMMING`

> 名表 `0xD780B0` / 值表 `0xD780B4`；12 个槽的类型值随后被折成 **31 位掩码 @+76**。

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 行宽 **50 段**（`csv0..csv49`）；缝列（11 个：`7..11, 15, 16, 19, 20, 23, 24`）留空即可。
- `faction` / `support{k}_type` 写**名称字符串**（写错/未知名 ⇒ 该列读作 0）。
- `support{k}_value` 写**整数**；`commander_name` / `description` 写文本。
