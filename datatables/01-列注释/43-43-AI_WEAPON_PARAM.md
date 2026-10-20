# AI_WEAPON_PARAM ｜ `npc/ai_weaponparam.csv`

- **用途**：NPC AI 按 **交战距离段 + 武器槽** 配置照准锥、集弾节奏与射击模式概率
- 资源对应：`script/AI/mission/other/msma_common_weaponparam.csv`（日文表头同源语义）
- 表ID `43` ｜ 下载序 `43` ｜ 类名 `CAIWeaponParam` ｜ 全局 `dword_11EB9B4` ｜ ctor `sub_A5B930` ｜ 派生 vtable `0xecf1cc`
- 逐列读取函数 `sub_56F080` ｜ **列数 17**
- 运行时：`sub_5531F0` 按武器 ID 查 3 行 → `sub_55A280` 应用射击权重/警告射撃 → `sub_551CE0` 用照准角生成 AI Goal

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 0 | `0` | `weapon_param_id` | u32 | +0 | 主键 |
| 1 | `1` | `engage_range` | enum `sub_56E750` | +4 | `NEAR=1` `MIDDLE=2` `FAR=3` `SHIELD=4` 交战距离段 |
| 2 | `2` | `weapon_slot` | enum `sub_56E7F0` | +8 | `UNKNOWN=-1` `MAIN=0` `EX=1` `SUB1=2` 武器槽 |
| 3 | `3` | `aim_pitch_min_deg` | str→float | +12 | 俯仰下限（度×π/180，**取负**；空=π） |
| 4 | `4` | `aim_pitch_max_deg` | str→float | +16 | 俯仰上限（度→弧度） |
| 5 | `5` | `aim_yaw_min_deg` | str→float | +20 | 偏航下限 |
| 6 | `6` | `aim_yaw_max_deg` | str→float | +24 | 偏航上限（**取负**） |
| 7 | `7` | `spread_timing_a` | float | +28 | 集弾节奏 A（× flt_D91AF8 → sub_552B00） |
| 8 | `8` | `spread_timing_b` | float | +32 | 集弾节奏 B |
| 9 | `9` | `norm_trigger_a` | float | +36 | 与 col10 相加≠0 时归一化 col8/9 |
| 10 | `10` | `warning_shot_value` | float | +40 | = flt_D6D398 时启用警告射击（CAI+872） |
| 11 | `11` | `behavior_flag` | bool | +44 | bit1→移动等待 Goal |
| 12 | `12` | `tree_priority` | u8 | +45 | 索引树过滤/优先级 |
| 13 | `13` | `fire_single_weight` | float | +48 | 単発权重 → CAI+88（归一化） |
| 14 | `14` | `fire_burst_weight` | float | +52 | 点射权重 → CAI+92 |
| 15 | `15` | `fire_full_mag_weight` | float | +56 | 全弹射击权重 → CAI+96 |
| 16 | `16` | `fire_sustain_weight` | float | +60 | 持续射击权重（四路概率第 4 项） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- col3–6 写**度数字符串**（非枚举）；空则默认 180°。
- col13–16 为射击模式**相对权重**，读表后 `sub_56E510` 归一化为概率和 1.0。
