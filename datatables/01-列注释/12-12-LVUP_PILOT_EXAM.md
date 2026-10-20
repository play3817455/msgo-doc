# LVUP_PILOT_EXAM ｜ `growth/lvup_exam.csv`

- **用途**：机师考核（考试）等级曲线
- 表ID `12` ｜ 下载序 `12` ｜ 类名 `CLvupPilotExaminationTable` ｜ disposition `DOWNLOAD`
- 逐列读取函数 `sub_57A060` ｜ **列数 5**

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `exam_level` | u32 | +0 | 考核等级（主键；reader 按 **u32** 读进 +0） |
| 2 | `1` | `exam_stat_type` | enum `sub_579FC0` | +4 | 考核关联统计项（enum col1 sub_579FC0 → +4；与 DAILY_RECORD 46 项战绩同源） |
| 3 | `2` | `exam_title` | str | +8 | 考核标题（wstring col2 → +8；sub_456D90→sub_4029E0） |
| 4 | `3` | `pass_score` | u32 | +36 | 合格分数线（u32 col3 → +36） |
| 5 | `4` | `pass_bonus_flag` | bool | +40 | 通过奖励启用标志（bool col4!=0 → +40） |

## 本表填写现状（2026-10-05 体检）

`#12` 是这一批里**唯一含真值**的表 —— 真值在 col1：

- **col1 `exam_stat_type`：真值 ✓**。22 行枚举名**逐名可在客户端枚举表里解析**。
  枚举表地址与内容（`sub_579FC0` 里 `(&off_D79430)[2i]` 取名、`dword_D79434[2i]` 取值，共 **51 项**，索引 0 起）：
  `VERSUS(1) VERSUS_XWAR(2) VERSUS_COMMANDER(3) WIN(4) WIN_XWAR(5) WIN_COMMANDER(6) KILL(7) KILL_WRESTLE(8)
  KILL_SHOT(9) KILL_CANNON(10) KILL_THROW(11) KILL_DEPARMS(12) KILL_ASSIST(13) SCORE_ATK(14) SCORE_SPT(15)
  SCORE_CON(16) SCORE_TOTAL(17) SCORE_ASSAULT_A(18) SCORE_ASSAULT_B(19) SCORE_SNIPE(20) SCORE_CANNON(21)
  SCORE_SUPPORT(22) RESULT_GOLD(23) RESULT_GOLD_RANK(24) RESULT_GOLD_SCORE(25) RESULT_GOLD_DSS(26)
  RESULT_GOLD_CONQUER(27) RESULT_SILVER_RANK(28) RESULT_SILVER_SCORE(29) RESULT_BRONZE_RANK(30)
  RESULT_BRONZE_SCORE(31) RESULT_BLUE_RANK(32) RESULT_BLUE_SCORE(33) SEARCH(34) RESURRECT(35) MOVE_LEN(36)
  RESPAWN_DEFEAT(37) RESPAWN_CONQUER(38) DMG_STGHOLD(39) DMG_BTLSHIP(40) DMG_TENDER(41) DMG_ACE(42)
  MAPOBJ_KILL(43) BATTERY_KILL(44) CONTAINER(45) PROTECT(46) STGARMS_SET(47) STGARMS_LEN(48)
  ORDER_COMP_PL(49) BADGE_GET(50) DESTROY_STGHOLD(51)`

  本表 22 行的取值（`exam_level` 0..21）：`WIN / VERSUS / KILL / KILL_ASSIST / SEARCH / RESURRECT /
  SCORE_TOTAL / MAPOBJ_KILL / BATTERY_KILL / CONTAINER / PROTECT / STGARMS_SET / ORDER_COMP_PL /
  DMG_STGHOLD / BADGE_GET / MOVE_LEN / STGARMS_LEN / RESPAWN_CONQUER / RESPAWN_DEFEAT / KILL_SHOT /
  KILL_CANNON / KILL_WRESTLE` —— **22/22 命中、互不重复**。
  ⚠️ 但"**为什么是这 22 个、为什么是这个次序**"仍未取证（枚举值并不按大小排列：WIN=4、VERSUS=1、KILL=7…）。

- **col2 `exam_title`：全空**。reader 明确按 wstring 读进 `+8`（`sub_456D90` → `sub_4029E0`）⇒ **考核标题显示为空**。
- **col3 / col4：常量 `1`**（两列值向量完全相同）⇒ 占位。


**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大列号，后面可省略。

> 复跑判据（列簇 + 枚举命中）：`python datatables/_probe_batch_n2_formula.py`
> ⇒ 本表应报「col3 == col4」，且 col1 无公式命中（枚举名不是数字）。
