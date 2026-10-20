# MSMA_FORMATION ｜ `msma/msma_npc_formation.csv`

- **用途**：机体 NPC 编队
- 表ID `38` ｜ 下载序 `38` ｜ 类名 `CFormationTable` ｜ 逐列读取 `sub_577DE0`
- 列数 18 ｜ 确证 17 ｜ 部分 0 ｜ gap 1

| 读序 | CSV# | 订案名 | 类型 | 内存 | 语义（ASM 确证） |
|---|---|---|---|---|---|
| 1 | `0` | `formation_id` | u32 | +0 | NPC 编队ID（主键） |
| 2 | `2` | `slot_0_angle` | float | +4 | 槽位0 角度输入（col2×flt_D69A68 → sin/cos @+4） |
| 3 | `3` | `slot_0_radius` | float | +12 | 槽位0 半径/第三分量（col3 直写 float @+12） |
| 4 | `4` | `slot_1_angle` | float | +16 | 槽位1 角度输入（col4×flt_D69A68 → sin/cos @+16） |
| 5 | `5` | `slot_1_radius` | float | +24 | 槽位1 半径/第三分量（col5 直写 float @+24） |
| 6 | `6` | `slot_2_angle` | float | +28 | 槽位2 角度输入（col6×flt_D69A68 → sin/cos @+28） |
| 7 | `7` | `slot_2_radius` | float | +36 | 槽位2 半径/第三分量（col7 直写 float @+36） |
| 8 | `8` | `slot_3_angle` | float | +40 | 槽位3 角度输入（col8×flt_D69A68 → sin/cos @+40） |
| 9 | `9` | `slot_3_radius` | float | +48 | 槽位3 半径/第三分量（col9 直写 float @+48） |
| 10 | `10` | `slot_4_angle` | float | +52 | 槽位4 角度输入（col10×flt_D69A68 → sin/cos @+52） |
| 11 | `11` | `slot_4_radius` | float | +60 | 槽位4 半径/第三分量（col11 直写 float @+60） |
| 12 | `12` | `slot_5_angle` | float | +64 | 槽位5 角度输入（col12×flt_D69A68 → sin/cos @+64） |
| 13 | `13` | `slot_5_radius` | float | +72 | 槽位5 半径/第三分量（col13 直写 float @+72） |
| 14 | `14` | `slot_6_angle` | float | +76 | 槽位6 角度输入（col14×flt_D69A68 → sin/cos @+76） |
| 15 | `15` | `slot_6_radius` | float | +84 | 槽位6 半径/第三分量（col15 直写 float @+84） |
| 16 | `16` | `slot_7_angle` | float | +88 | 槽位7 角度输入（col16×flt_D69A68 → sin/cos @+88） |
| 17 | `17` | `slot_7_radius` | float | +96 | 槽位7 半径/第三分量（col17 直写 float @+96） |

**填写规则**：
- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过。
- 枚举列写**名称字符串**（见 `reverse-login-chain/formats/枚举表.md`）。
- **越界列 = 0**：只需写到最大有效列号。
