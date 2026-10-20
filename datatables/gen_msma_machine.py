# -*- coding: utf-8 -*-
"""gen_msma_machine.py —— 以「权威关联表」为基准，生成机体相关四张表。

基准（唯一权威）：`datatables/names/ms_wiki_pairs.json`
    = 用户人工核对的 練度ID ↔ モデルID ↔ WIKI 机体名（576 条，严格 1:1）。

★ 数值取值口径（2026-10-02，用户拍板「**gow wiki 为准** / 中文名保留现库」）：
    ① **gow wiki panel 第一档（基础值）** —— `gow_wiki/data/units.json`。
       选取：先按 練度ID(dev_id) 取候选；无 dev_id 时按 WIKI 名规范化后查名索引；
       再按 **WIKI 名 ↔ 候选 cn/name** 精确匹配；退化才用启发式。
       ★panel[1]（强化上限）**不落 CFG** —— 见 `names/ms_gow_caps.csv`（参考）与 MECHANIC_MSMA 说明。
    ② **codex（status=updated）** —— 仅当 ① 缺字段时补。
    ③ **codex（status=stale）** —— 最后兜底。
    ★名称：优先保留 **现有 msma_settings.csv col5**（数据库/bootstrap 已在用的中文名）；
       新行才走 JSON/桥表取名逻辑。
    两源都有值但不同 ⇒ 记入 `names/机体数值-两源冲突清单.csv`（gow vs codex）。

名册（行脊）：
    `unpackdat/settings/favms_ok_list.csv` → 696 台（顺序原样不动；它同时是客户端图鉴名册）。
    JSON 里有、名册里没有的机体（当前 2 台）**追加在末尾**，保证权威表里的机体一台不丢。

产出（就地覆盖，先备份 .bak_machine）：
    1. server/datafiles/lounge/msma/msma_settings.csv      ← CHARA_PARAM（表ID 4 / 读 sub_582390）
    2. server/datafiles/lounge/msma/msma_rental.csv        ← MSMA_RENTAL（同构同读器）
    3. server/datafiles/lounge/msma/msma_battle_detail.csv ← MSMA_BATTLE_DETAIL（表ID 34 / 读 sub_A47BC0）
       ★9 个属性 = **7 个两层取值**（RESPAWN_TIME/MAX_HP/MOVE/BOOST_GAUGEMAX/BOOST_GAUGEHEAL/COST/WARP_TIME）
         ＋ **2 个常量**（ENERGY / BOOST_SPEED，取值依据见下方 ENERGY_ATTR / BOOST_SPEED_ATTR 注释）；
         JUMP 无面板绑定也无来源 ⇒ 不填。
    4. server/datafiles/lounge/msma/msma_model.csv         ← CHARA_MODEL（表ID 5 / 读 sub_571380）
    5. datatables/names/机体数值-两源冲突清单.csv           ← 人工复核用（长表）

★ 为什么不写 CHARA_PARAM 的 col7 combat_role / col8 faction / col9..11 terrain：
    codex 有 type/faction/terrain，但「中文 wiki 的值 ↔ 客户端枚举(ASSAULT_A/…)」的对应**未取证**，
    按仓库「不猜」铁律留空，另行攻关后再补（见 05-76表填写规格总表 §三）。
★ 为什么 CHARA_PARAM 的数值列和 MSMA_BATTLE_DETAIL 都要写：
    §7.3 已定案 —— 玩家在 UI 里看到的「装甲/最高速度/喷射蓄力/搭载量/紧急返回性能」读的是
    **MSMA_BATTLE_DETAIL**（后处理填进 row+188/+200/+204/+260/+272），不是 CHARA_PARAM 的数值列；
    但 CHARA_PARAM 的数值列另有战斗计算消费者 ⇒ **两处同源同值，永远一致**。

用法：
    python datatables/gen_msma_machine.py            # 生成（备份 + 自检 + 冲突统计）
    python datatables/gen_msma_machine.py --check    # 只自检/统计，不写文件
"""
import io
import json
import os
import re
import shutil
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAMES = os.path.join(HERE, 'names')
GAME = os.path.join(ROOT, '机动战士敢达Online', 'GundamOnline')
FAVMS = os.path.join(GAME, 'unpackdat', 'settings', 'favms_ok_list.csv')
PAIRS = os.path.join(NAMES, 'ms_wiki_pairs.json')
BRIDGE = os.path.join(NAMES, '机体名对照表.csv')
MID_FULL = os.path.join(NAMES, '练度ID-モデルID-全集.csv')
CODEX = os.path.join(GAME, 'unpackdat', 'codex', 'data', 'units.json')
JPUNITS = os.path.join(ROOT, 'gow_wiki', 'data', 'units.json')
MSDIR = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma')
CONFLICT = os.path.join(NAMES, '机体数值-两源冲突清单.csv')

# ---- CHARA_PARAM / MSMA_RENTAL（同构）-------------------------------------
SET_COLS = 92          # csv_index 0..91
ID_COL, MID_COL, NAME_COL = 0, 1, 5

# ★★ col38 = 武器组ID（机体 → 武器 的唯一口径，2026-09-28 反汇编定案）★★
#   链路：sub_582390 `*(a3+372) = sub_BBB370(a1, 0x26)` ⇒ CHARA_PARAM col38 → 行 +0x174。
#   `sub_581690` 用行 +372 查 `dword_11EBAB4` = MSMA_WEAPONSET，取启用行的 col2(武器ID)
#   写进机体行 +376/+380/+384（≤3 把）；`sub_836D10` 用同一个 +372 查
#   `dword_11EBAB8` = MSMA_WEAPON_EQUIPCOMB。
#   ⇒ col38 必须同时是 `msma_weapon_set.col0` 与 `msma_weapon_equipcomb.col0` 的键。
#   ⇒ 本批取「机体自身練度ID」（= col0）⇒ 一台机体一个武器组，与两张表既有键空间一致。
#   ⚠️ 两张表的 col0 是 std::map 的 32 位整型键（`sub_581200` 比较 node+16），客户端
#      在这条链上**不做 練度ID ↔ モデルID 转换** ⇒ 绝不可写 9 位 モデルID（写了永远查不到）。
WEAPON_GROUP_COL = 38

# ---- 地形适性 col9/col10/col11（2026-10-01 反汇编取证后首填）-----------------
#
# ★三列的**读取与用途**都是确证（`db_design/schema/cfg/tables/CHARA_PARAM.json`：
#   `terrain_proper_space` col9→+0x88、`terrain_proper_water` col10→+0x8C、
#   `terrain_proper_ground` col11→+0x90，读侧 `sub_582390` @0x58252f/0x58253d/0x58254b）；
#   2026-10-01 补上**消费侧**的最后一块：
#
#   `sub_6102C0`（机库/编成的机体列表装配，@0x6104A7）逐台调
#       v73 = sub_64A230(战场地形种类, row[136]!=0, row[140]!=0, row[144]!=0);
#   ⇒ **三个值在客户端里只被当作布尔用**（`!= 0`），不是等级/分数 ⇒ 线上就该是 0/1。
#   `sub_64A230` 用这三个布尔 + 战场地形算出机体的地形类别码（0..3），供列表/详情显示。
#
# ⛔ 之前留空的理由写在旧表头（"codex 的 terrain 与客户端枚举的对应未取证"）——
#   那句话说的是 col7 combat_role / col8 faction 的**枚举**；
#   col9/10/11 是布尔，语义一一对应「地/宇/水」，不存在枚举对应问题。
#
# ★取值来源（可回溯，不猜）：`unpackdat/codex/data/units.json` 的 `terrain` 串
#   （'地·宇' / '地面' / '水陆' / '地・宇' / '宇宙' / '宇专用' / '低·宇' …），
#   按关键字拆三个布尔；codex 没有时用日服 wiki panel 的 `地形タイプ`（'宇専用' / '宇・水陸' / '陸上' …）。
#   两边都没有 ⇒ **留空**（=0），绝不按势力/名字猜。
#
# 关键字规则（覆盖上面全部实测取值）：
#   '宇' ⇒ 宇宙适性 1      ← '宇宙' / '宇专用' / '宇専用' / '低·宇' / '地·宇' / '宇・水陸'
#   '水' ⇒ 水中适性 1      ← '水陆' / '水陸' / '宇・水陸'
#   '地' 或 '陸'/'陆' ⇒ 地面适性 1  ← '地面' / '地上' / '陸上' / '水陆' / '地·宇'
#   例：'水陆' ⇒ 水+地（两栖机，如 ザク・マリナー 系）；'低·宇' ⇒ 仅宇宙。
TERRAIN_SPACE_COL, TERRAIN_WATER_COL, TERRAIN_GROUND_COL = 9, 10, 11


def terrain_flags(t):
    """地形串 → (space, water, ground) 三个 0/1；**认不出关键字返回 None**（调用方据此留空）。

    只做"关键字存在性"判定，不做模糊匹配：认不出就返回 None ⇒ 那一格留空，
    而不是给一个"看起来合理"的默认值（编队/出击会按这三个布尔判地形，填错比留空更坏）。
    """
    t = s1(t) if t else ''
    if not t:
        return None
    sp = 1 if '宇' in t else 0
    wt = 1 if '水' in t else 0
    gr = 1 if ('地' in t or '陸' in t or '陆' in t) else 0
    if not (sp or wt or gr):
        return None
    return sp, wt, gr

# CHARA_PARAM 的数值列 ← 内部字段
#
# ★★2026-09-28 订正（命名冲突结案；见 `04-填充日志.md` §9 与 `01-列注释/78-MSMA_OVERWRITE_PARAMS.md`）★★
#   面板 6 参数里 **只有「装备搭载量」是 CHARA_PARAM 的列**（col52→+248），三源一致：
#     ① 表 78 覆写关键字 `PAYLOAD`（`sub_57EEB0`，9/9 偏移与行基址对齐）
#     ② 开发命令 `sub_6246D0` 内建名 `PAYLOAD`
#     ③ 机库面板绑定 `sub_61C9A0` idx4「装备搭载量」
#   其余 5 个面板参数**不是 CHARA_PARAM 的列** —— 它们是"后处理"偏移，由 `sub_581690` 用 10 个串槽键
#   查 MSMA_BATTLE_DETAIL 家族后填入：装甲+164 / 最高速度+180 / 喷射蓄力+176 / 紧急返回性能+236 /
#   喷射容量（`sub_40C740`，非行字段）。
#   ⇒ 这 5 个的值由 **msma_battle_detail.csv**（下方 DETAIL_ATTRS，7 属性）承载，**不要**再写 CHARA_PARAM 数值列。
#
# 已撤下的列（旧名作废、值清空；旧名源头是 `06-UI…` §7.2 一张"行偏移算重了 +24"的表，已订正）：
#   col83 旧名 紧急返回(return_val) → 实为表 78 关键字 `MODULE_SLOT`，面板无此格 ⇒ 清空待定
#   col85 旧名 装备搭载量(payload)  → +356 语义未定 ⇒ 清空待定
#   col86 旧名 喷射蓄力(boost_cd)   → +256 语义未定 ⇒ 清空待定
#   col89 → +244 = **M-COST**（不是最高速度）。卡片 `sub_803560` 把 v12[61]（+244）画在
#     COST（v12[60]=+240）旁边；机库列表 `sub_6102C0` 同样把 +244 抄进 v74。
#     取值 = 与 `store.CostToMissionCost` 同一张档位表（由 COST 派生），写在填行循环里。
#   （col52 旧写 ブースト容量 ⇒ ★改名「装备搭载量」并把来源换成 積載量★）
SET_NUM = [
    (52, 'payload'),     # ★装备搭载量（= `PAYLOAD`）col52→+248  ★三源一致★
    (90, 'armor'),       # 装甲基值（⚠待复核：面板「装甲」绑 +164，而 +148 由 sub_6102C0 以 u16 读）col90→+148
]
MCOST_COL = 89


def cost_to_mcost(cost):
    """与 serverv/internal/store.CostToMissionCost 同一张档位表。"""
    try:
        n = int(cost)
    except (TypeError, ValueError):
        return ''
    if n >= 400:
        return '10'
    if n >= 340:
        return '20'
    if n >= 280:
        return '30'
    if n >= 200:
        return '40'
    if n > 0:
        return '50'
    return ''

# ---- CHARA_PARAM 的 10 个「战力子表槽」（窄串列 col56/58/60/62/64/67/69/71/73/79）------
# ★★2026-09-28 反汇编定案：这 10 列不是「附加资源路径」，而是 `sub_581690` 查
#   MSMA_BATTLE_DETAIL 的 10 张子表时用的**字符串键**（std::map<std::string>，比较见 sub_581270/sub_5812E0）。
#   槽 → 子表（ctor `sub_A725F0` 的 RTTI 实名）→ 词表属性（`off_D7A298` / sub_57BD40）→ 写入机体行偏移：
#     col56 → MSMA_DETAIL_RESPAWN_DATA        RESPAWN_TIME        首块（行 +192）
#     col58 → MSMA_DETAIL_WARPTIME_DATA       WARP_TIME           +236（紧急返回性能）
#     col60 → MSMA_DETAIL_COST_DATA           COST                +240
#     col62 → MSMA_DETAIL_MAX_HP_DATA         MAX_HP              +164（★面板「装甲」）
#     col64 → MSMA_DETAIL_ENERGY_DATA         ENERGY              +184/+188
#     col67 → MSMA_DETAIL_MOVE_DATA           MOVE                +180（★面板「最高速度」）
#     col69 → MSMA_DETAIL_BOOST_GAUGEMAX_DATA BOOST_GAUGEMAX      +168（★面板「喷射容量」）
#     col71 → MSMA_DETAIL_BOOST_GAUGEHEAL_DATA BOOST_GAUGEHEAL    +176（★面板「喷射蓄力」）
#     col73 → MSMA_DETAIL_BOOST_MOVE_DATA     BOOST_SPEED         +260..+312
#     col79 → MSMA_DETAIL_JUMP_DATA           JUMP                +316..+364
#   （子表 11..13 MSMA_DETAIL_SHOT / LOCKON / RELOAD 无对应槽 ⇒ 不经此链注入，本生成器不产生其行。）
#   键语义：子表插入 = 读 CSV col1 为**字符串键**（`sub_A5BE20`：sub_BBB4F0(idx=1) → vtable[2](key,val)），
#   与本表 msma_battle_detail.csv 的 col1 **必须逐字节相等**。本批 col1 = 本行 練度ID；
#   故对应槽值也写 **本行 練度ID**。槽空 ⇒ 键为空串 ⇒ 查不到行 ⇒ 后处理按 0（面板显示 0）。
#   ⇒ 本表 7 个有数据的槽（time/return_val/cost/armor/speed/boost/boost_cd）**必须同步填**，否则面板这 7 项全 0。
SLOT_FIELD = [
    (56, 'time'),        # RESPAWN_TIME
    (58, 'return_val'),  # WARP_TIME
    (60, 'cost'),        # COST
    (62, 'armor'),       # MAX_HP
    (67, 'speed'),       # MOVE
    (69, 'boost'),       # BOOST_GAUGEMAX
    (71, 'boost_cd'),    # BOOST_GAUGEHEAL
]

# ---- MSMA_BATTLE_DETAIL（13 子表里的 7 项，值来自 codex/日服两层）----------
DETAIL_COLS = 3
DETAIL_ATTRS = [
    ('RESPAWN_TIME', 'time', 'int'),       # 再出击时间（秒）
    ('MAX_HP', 'armor', 'int'),
    ('MOVE', 'speed', 'float'),
    ('BOOST_GAUGEMAX', 'boost', 'int'),
    ('BOOST_GAUGEHEAL', 'boost_cd', 'float'),
    ('COST', 'cost', 'int'),
    ('WARP_TIME', 'return_val', 'int'),
]

# ---- 另两项：值**不是**两层来源，而是从客户端公式反解出来的常量 ------------
#
# 这两项 codex / 日服 wiki **都没有**（它们是隐藏的引擎参数，wiki 面板只暴露 6 个数），
# 但客户端**会**用它们：缺行 ⇒ 对应字段落 0 ⇒ 面板/出击判定直接坏掉。
# ⇒ 取值依据 = 反汇编出来的客户端公式本身（下面逐条写清，属于"可验证的推导"，不是"猜"）。
#
# ★★ENERGY（子表 5）★★  `ENERGY,<練度ID>,1000,`
#   解析器 `sub_57B990`：col2 → 结构[+0]（u32）、col3 → 结构[+4]（u32）。
#   注入器 `sub_581690`（用 col64 槽键查本子表）：
#       查不到 ⇒ **+184 = 0 / +188 = 0**；查到 ⇒ `+184 = min(f[0], 99)`（★客户端硬钳 99）、`+188 = f[1]`。
#   ⇒ 缺这一行 ⇒ 能量上限 0 ⇒ 编成界面判「由于能量耗尽 因此无法出击」✗
#     （P250 实证崩在这里，见 `datatables/07-模块与能量攻关.md`）。
#   ⇒ 值取 **1000**：与协议侧 `msmaEnergyFull` / `battle.go` 的 `energy_now`（1000）对齐，
#     也与本仓 `server/internal/{config,authsrv}` 三处注释「ENERGY 上限 1000」一致；
#     客户端自己会把它钳到 99 —— 1000 与 99 在客户端**等价**，选 1000 是为了两端口径统一。
#   ⚠️ 只写 col2；col3（+188）留 0 —— 其语义未取证，而"单列 1000"正是 P250 验证过能出击的形态。
ENERGY_ATTR = 'ENERGY'
ENERGY_VALUE = 1000
ENERGY_SLOT_COL = 64
#
# ★★BOOST_SPEED（子表 9）★★  `BOOST_SPEED,<練度ID>,0.840000,`
#   解析器 `sub_57B9F0`：**14 列**（col2..col15）→ 结构 [+0..+52]，float/u32 混排：
#       +0,col2 f ｜ +4,col3 f ｜ +8,col4 u ｜ +12,col5 f ｜ +16,col6 f ｜ +20,col7 u
#       +24,col8 u ｜ +28,col9 f ｜ +32,col10 f ｜ +36,col11 f ｜ +40,col12 f ｜ +44,col13 f
#       +48,col14 u ｜ +52,col15 f
#   注入器 `sub_581690` 把它搬到机体行 **+260..+312**（注意 **+284 = -col8**，注入时取负）。
#   ★面板「最高速度」（`sub_61C9A0` idx=1）公式（逐字反编译）：
#       v = MOVE(row+180) × max(row+260, row+276)        // ← 就是 col2 / col6
#       v = v × flt_D90A04(0.0005952381) × flt_D6C124(200.0) × flt_D6874C(10.0)
#       面板值 = trunc(v) + 1
#   三个常量之积 = **1.1904762**（已用 IDA 读实数核对）⇒ 要「面板显示 == MOVE」就必须
#       max(col2, col6) = 1 / 1.1904762 = **0.8399999… ⇒ 取 0.84**
#   ⇒ 本批写 **col2 = 0.840000**（col6 留 0，max 仍取到 0.84 ✓），其余 12 列留 0。
#   2026-10-08更正：以上仅解释历史面板投影，不是完整运动定义。
#   502470普通持续阶段直接乘col6；col6空会得到0。501F90另读col9/10，
#   580410的闪避推进(1608)门要求col12/13/14为正，不能以面板正确证明控制完整。
#   serverv的1101011/1132252仅对col6做=已有col2的可回滚兼容实验；
#   本旧生成器尚未重建完整控制参数，禁止全量导入覆盖当前实验及其他已修复字段。
#   ⛔ 缺这一行 ⇒ +260/+276 全 0 ⇒ 面板「最高速度」恒显示 **1** ✗
#     （本仓 `server/internal/datafiles/battle_detail_test.go` 就是钉这一条的）。
#   ⛔ 绝不能再写 1900 这类「载重量/机动值」：面板会把它当倍率相乘 ⇒ 显示成 2777619 ✗（用户实测截图 ✓）。
BOOST_SPEED_ATTR = 'BOOST_SPEED'
BOOST_SPEED_RATE = '0.840000'
BOOST_SPEED_SLOT_COL = 73
#
# ★不填 **JUMP**（子表 10）：解析器 `sub_57BAA0` 要 **12 列**（col2..col13）→ 结构 [+0..+44]，
#   注入到机体行 +316..+364（其中 +348 = -col10、+364 = col13 的布尔）。它**没有任何面板绑定**，
#   codex/日服也都没有 ⇒ 按仓库「不猜」铁律留空（缺行 ⇒ +316..+364 全 0，与现状完全一致）。
#   语义取证后另批补 —— 列布局已在上面写全，届时只需往 CONST_DETAILS 加一条。
#   2026-10-08：没有面板绑定不等于战斗不需要。503670/503190用col8×col4
#   产生辅助槽0的请求Y；502760用取负col10处理槽1。缺行会清零这些输入，
#   45E620完整注册确认jump=1602、dash=1606、dodge_dash=1608；不要将
#   相邻push当作当前绑定的事件编号。当前保存配置Space绑定jump，入口4E2770。
#   serverv另有两台R001短起跳兼容原型，禁止旧生成器覆盖；不是原服JUMP数据。
#
# 有常量的子表槽 → 值（与 DETAIL_ATTRS 的槽同集合：**有数值的机体才填**）。
CONST_DETAILS = [
    (ENERGY_ATTR, ENERGY_SLOT_COL, str(ENERGY_VALUE)),
    (BOOST_SPEED_ATTR, BOOST_SPEED_SLOT_COL, BOOST_SPEED_RATE),
]

# ---- CHARA_MODEL：行键 col0 = モデルID；两台R001的CSV14有独立兼容策略 ----
# ✗ 曾用「col0 = 練度ID + col71/72 = モデルID」——2026-09-28 证伪（见 render_model 注释）。
# 571380 reads through CSV76; this does not supply unknown field values.
MODEL_COLS = 77

# 内部字段 → (codex units.json 键, 日服 panel 键)
FIELD_SRC = {
    'armor':      ('armor',      'アーマー'),
    'speed':      ('speed',      '最高速度'),
    'boost':      ('boost',      'ブースト容量'),
    'payload':    ('payload',    '積載量'),
    'boost_cd':   ('boost_cd',   'ブーストチャージ'),
    'return_val': ('return_val', '緊急帰投性能'),
    'time':       ('time',       'TIME'),
    'cost':       ('cost',       'COST'),
}
FIELD_CN = {
    'armor': '装甲', 'speed': '最高速度', 'boost': '推进容量', 'payload': '载重量',
    'boost_cd': '推进器冷却', 'return_val': '紧急返回', 'time': '再出击时间', 'cost': 'COST',
}

NUM_RE = re.compile(r'-?\d+')


# ------------------------------------------------------------------ 基础工具
def rows_of(path, enc='utf-8'):
    out = []
    for line in io.open(path, encoding=enc, errors='replace').read().splitlines():
        if line.strip() and not line.lstrip().startswith('#'):
            out.append(line)
    return out


def cell(parts, i):
    return parts[i].strip() if i < len(parts) else ''


def s1(v):
    if isinstance(v, list):
        return v[0] if v else ''
    return v or ''


def first_num(v):
    """取第一个数字（★必须先按空白切词：wiki 有格内写两个数 '4,150 8,300'）。"""
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return int(v)
    tok = s1(v).replace(',', '').split()
    if not tok:
        return None
    m = NUM_RE.search(tok[0])
    return int(m.group(0)) if m else None


def norm_name(v):
    """机名规范化 —— 让 `高达OL吉姆后期生产型` 与 codex 的 `吉姆后期生产型` / `敢达OL…机体数据` 对齐。"""
    s = s1(v).strip()
    for a, b in (('（', '('), ('）', ')'), ('・', '·'), ('　', ''), ('／', '/')):
        s = s.replace(a, b)
    s = re.sub(r'\s+', '', s)
    for pre in ('高达OL', '敢达OL'):          # ★前缀是 4 个字符（高/达/O/L）
        if s.startswith(pre):
            s = s[4:]
            break
    if s.endswith('机体数据'):
        s = s[:-4]
    return s.lower()


def strip_region(s):
    """去掉机名尾部的地区标注 `（国）`/`(国)`/`（日）`/`(日)`（可叠，如 `原型敢达（金色）（国）`）。
    ★`中国用XXX` / `（中国用）` 这类**不**处理（2026-09-28 用户定：那是官方叫法，保留）。"""
    for k in ('（国）', '(国)', '（日）', '(日)'):
        while s.endswith(k):
            s = s[:-len(k)]
    return s


def cn_name(v):
    """机名 → ★中文名：去 `高达OL`/`敢达OL` 前缀 + 去尾部地区标注。
    例：`高达OL原型敢达（金色）（国）` → `原型敢达（金色）`；`高达OL加普兰(日)` → `加普兰`。"""
    s = s1(v).strip()
    for pre in ('高达OL', '敢达OL'):
        if s.startswith(pre):
            s = s[len(pre):]
            break
    return strip_region(s)


# ------------------------------------------------------------------ 载入
def load_pairs():
    """权威关联：{練度ID: (モデルID, WIKI 名)}。"""
    d = json.load(io.open(PAIRS, encoding='utf-8'))
    out = {}
    for p in d.get('pairs') or []:
        lid, mid = (p.get('lid') or '').strip(), (p.get('mid') or '').strip()
        if lid.isdigit() and mid.isdigit():
            out.setdefault(lid, (mid, (p.get('wiki') or '').strip()))
    return out


def load_roster():
    """客户端名册：favms_ok_list.csv → [(練度ID, 名)]，顺序原样，去重。"""
    out, seen = [], set()
    for line in io.open(FAVMS, encoding='utf-8', errors='replace').read().splitlines():
        line = line.lstrip('\ufeff')
        if not line.strip() or line.lstrip()[0] == '#':
            continue
        parts = line.split(',')
        if len(parts) >= 2 and parts[0].strip().isdigit():
            pair = (parts[0].strip(), parts[1].strip())
        else:
            head = ''
            for ch in line:
                if ch.isdigit():
                    head += ch
                else:
                    break
            if not head or head == line:
                continue
            pair = (head, line[len(head):].lstrip('.．・ '))
        if pair[0] in seen:
            continue
        seen.add(pair[0])
        out.append(pair)
    return out


def load_bridge():
    """机体名对照表.csv → {練度ID: 行}（用于给「JSON 没覆盖的名册行」取中文名；不作数值源）。"""
    m = {}
    for line in rows_of(BRIDGE, enc='utf-8-sig'):
        p = line.split(',')
        lid = cell(p, 0)
        if len(lid) == 7 and lid.isdigit():
            m[lid] = p
    return m


def load_mid_full():
    out = {}
    if not os.path.exists(MID_FULL):
        return out
    for line in rows_of(MID_FULL, enc='utf-8-sig'):
        p = line.split(',')
        if len(p) >= 2 and cell(p, 0).isdigit() and cell(p, 1).isdigit():
            out.setdefault(cell(p, 0), cell(p, 1))
    return out


def load_codex():
    """codex 存档 → {规范化机名: unit}。同名的按 updated 优先、字段多者优先，保证确定性。"""
    units = json.load(io.open(CODEX, encoding='utf-8'))['units']

    def rank(u):
        return (0 if (u.get('status') or '') == 'updated' else 1,
                -sum(1 for v in u.values() if v not in (None, '', 0)),
                u.get('order') or 0)

    idx = {}
    for u in units:
        k = norm_name(u.get('name'))
        if not k:
            continue
        idx.setdefault(k, []).append(u)
    return {k: sorted(v, key=rank)[0] for k, v in idx.items()}


def load_jp():
    """gow wiki → (bydev, byname, resolve(lid, wiki)→(unit, how))。"""
    units = json.load(io.open(JPUNITS, encoding='utf-8'))
    bydev, byname = {}, {}
    for u in units:
        d = (u.get('dev_id') or '').strip()
        if d.isdigit():
            bydev.setdefault(d, []).append(u)
        for key in ('name', 'cn', 'page'):
            k = norm_name(u.get(key))
            if k:
                byname.setdefault(k, []).append(u)
        for alt in (u.get('cn_alt') or []):
            k = norm_name(alt)
            if k:
                byname.setdefault(k, []).append(u)

    def rank(u):
        nm = s1(u.get('name'))
        return ('（' in nm or '(' in nm, -len(u.get('panel') or {}), nm)

    def pick(cands, wiki):
        k = norm_name(wiki)
        if k:
            for u in cands:
                if any(norm_name(u.get(key)) == k for key in ('cn', 'name', 'page')):
                    return u, 'name'
                for alt in (u.get('cn_alt') or []):
                    if norm_name(alt) == k:
                        return u, 'name'
        return sorted(cands, key=rank)[0], 'rank'

    def resolve(lid, wiki):
        cands = bydev.get(lid)
        if not cands:
            cands = byname.get(norm_name(wiki))
        if not cands:
            return None, None
        return pick(cands, wiki)

    return bydev, byname, resolve


def load_existing_names():
    """现有 msma_settings.csv col5 → {練度ID: 中文名}（用户要求保留现库名称）。"""
    path = os.path.join(MSDIR, 'msma_settings.csv')
    if not os.path.exists(path):
        return {}
    out = {}
    for line in rows_of(path):
        p = line.split(',')
        lid = cell(p, 0)
        if lid.isdigit():
            nm = cell(p, NAME_COL)
            if nm:
                out[lid] = nm
    return out


# ------------------------------------------------------------------ 取值
def build_values(lid2pair, codex, jp_resolve):
    """三层取值 → ({練度ID: {字段: 值}}, {練度ID: {字段: 层}}, 冲突明细, {練度ID: (空,水,地)})。"""
    vals, src, conflicts, terrains = {}, {}, [], {}
    for lid, (mid, wiki) in lid2pair.items():
        cu = codex.get(norm_name(wiki))
        cupdated = cu is not None and (cu.get('status') or '') == 'updated'
        ju, jhow = jp_resolve(lid, wiki)
        jpanel = (ju.get('panel') or {}) if ju else {}

        v, s = {}, {}
        for f, (ck, jk) in FIELD_SRC.items():
            cv = first_num(cu.get(ck)) if cu and cu.get(ck) not in (None, '') else None
            jv = first_num(jpanel.get(jk)) if jpanel else None
            if jv is not None:
                v[f], s[f] = jv, 'gow'
            elif cv is not None and cupdated:
                v[f], s[f] = cv, 'codex'
            elif cv is not None:
                v[f], s[f] = cv, 'codex-stale'
            if cv is not None and jv is not None and cv != jv:
                conflicts.append({
                    'lid': lid, 'wiki': wiki, 'field': f, 'codex': cv, 'jp': jv,
                    'tier': 'gow',
                    'jhow': jhow, 'jp_name': s1(ju.get('name')) if ju else '',
                    'codex_status': cu.get('status') or '',
                })
        # ---- 地形适性 col9/10/11：codex.terrain → 日服 panel 地形タイプ 兜底 ----
        # ⛔ 单独存 terrains，**不并进 v**：`v` 非空 = 「有面板数值」，决定 detail 行与统计口径，
        #    terrain 只影响 col9/10/11 三格，不参与该判定。
        tf = terrain_flags(cu.get('terrain')) if cu else None
        if tf is None and jpanel:
            tf = terrain_flags(''.join(s1(x) for x in (jpanel.get('地形タイプ') or [])))
        if tf is not None:
            terrains[lid] = tf
        vals[lid], src[lid] = v, s
    return vals, src, conflicts, terrains


def fmt(v, kind):
    return '%.6f' % float(v) if kind == 'float' else str(int(v))


# ------------------------------------------------------------------ 渲染
def project_verified_r001_roles(rows):
    # Verified v15 role/label readers and original wiki main tables; only two units.
    import json
    from pathlib import Path
    tools_dir = Path(__file__).resolve().parents[1] / 'serverv' / 'tools'
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    from project_chara_roles import resolve_roles, project_rows
    project_root = tools_dir.parents[1]
    units = json.loads((project_root / 'gow_wiki/data/units.json').read_text(encoding='utf-8'))
    crosswalk = json.loads((tools_dir / 'chara_role_crosswalk_v15.json').read_text(encoding='utf-8'))
    bindings = resolve_roles(units, project_root / 'gow_wiki/cache/wikitext', crosswalk)
    return project_rows(rows, bindings)


def render_settings(rows, stats):
    rows = project_verified_r001_roles(rows)
    head = [
        '#模型ID（=練度ID）,,,,,名称,',
        '# ===== msma/msma_settings.csv （CHARA_PARAM / 表ID 4 / 下载序 4 / CCharaParamTable / 读取 sub_582390）=====',
        '# 行键 col0 = 練度ID（7 位）；col1 = モデルID（9 位；客户端 sub_A86810 用它拼 chara/ 路径）；',
        '# col5 = 機体名 ★**中文**（来源见下）。',
        '# ★★col38 = 武器组ID（机体→武器 的唯一口径；2026-09-28 反汇编定案）★★',
        '#   链路：sub_582390 `*(row+372) = col38` ⇒ `sub_581690` 用 row+372 查 MSMA_WEAPONSET',
        '#   （dword_11EBAB4）取启用行 col2 写进 row+376/+380/+384（≤3 把）；`sub_836D10` 用同一 row+372',
        '#   查 MSMA_WEAPON_EQUIPCOMB（dword_11EBAB8）。⇒ col38 必须同时命中 msma_weapon_set.col0',
        '#   与 msma_weapon_equipcomb.col0；本批取「机体自身練度ID」⇒ 一台机体一个武器组。',
        '#   ⛔ 两张表的 col0 是 32 位整型 map 键，此链上无 練度ID↔モデルID 转换 ⇒ 不得写 9 位 モデルID。',
        '# ★★2026-09-28 口径：基准 = names/ms_wiki_pairs.json（用户人工核对权威 576 条）。',
        '#   ★名称：JSON 覆盖的用其 `wiki` **去 `高达OL` 前缀 + 去尾部地区标注 `（国）`/`（日）`**',
        '#     （例：`高达OL原型敢达（金色）（国）` → `原型敢达（金色）`；`高达OL加普兰(日)` → `加普兰`）；',
        '#     其余名册行用 机体名对照表.csv 的官方中文名（同样去地区标注；兜底 codex中文名 → 日文名）。',
        '#     ★`中国用XXX` / `（中国用）` 保留（官方叫法）。',
        '#   数值三层：① gow wiki panel 第一档 ② codex(updated) ③ codex(stale) 兜底。',
        '#   ★名称优先保留现有 msma_settings.csv col5（现库中文名）。',
        '#   填数值列（★2026-09-28 订正：面板 6 参数里只有「装备搭载量」是 CHARA_PARAM 的列）：',
        '#     col52 装备搭载量(積載量/PAYLOAD) ★三源一致★ / col90 アーマー(待复核)',
        '#   ⛔ 已清空：col83/col85/col86（旧名 緊急帰投性能/積載量/ブーストチャージ 作废）；',
        '#   ★col89 = M-COST（行 +244）：按 COST 档位表派生，与 hangar `mission_cost` 同源；',
        '#     卡片 sub_803560 / 列表 sub_6102C0 读这一格。空着编队信息就显示 0；',
        '#   ★战力子表槽 col56/58/60/62/64/67/69/71/73/79 = sub_581690 查 MSMA_BATTLE_DETAIL 的字符串键；',
        '#     本批填 **9 个槽**（= 本行練度ID，即 msma_battle_detail.csv col1）：',
        '#       time/return_val/cost/armor/speed/boost/boost_cd 七槽的值来自 codex/日服（见上）；',
        '#       col64(ENERGY) 固定 1000、col73(BOOST_SPEED) 固定 0.84 —— 详见本文件 ENERGY_ATTR /',
        '#       BOOST_SPEED_ATTR 上方注释（★缺这两行 ⇒ 编成判「能量耗尽无法出击」✗ / 面板最高速度显示 1 ✗）。',
        '#     槽空 ⇒ 键为空串 ⇒ 查不到行 ⇒ 后处理按 0。col79(JUMP) 无面板绑定也无来源 ⇒ 仍留空。',
        '#   名册 = favms_ok_list.csv 696 台（顺序不动，同时是客户端图鉴名册）；',
        '#     JSON 里有、名册没有的 %d 台追加末尾 ⇒ 共 %d 行。' % (stats['extra'], stats['total']),
        '#   名称来源：%s。' % stats['names'],
        '#   有数值 %d 台（① gow %d ｜ ② codex %d ｜ ③ codex-stale %d）；无数值 %d 台。'
        % (stats['filled'], stats['t1'], stats['t2'], stats['t3'], stats['total'] - stats['filled']),
        '# ★地形适性（2026-10-01 首填）：col9 terrain_proper_space / col10 terrain_proper_water /',
        '#   col11 terrain_proper_ground → 行 +0x88/+0x8C/+0x90。消费侧 sub_6102C0 @0x6104A7 调',
        '#   sub_64A230(战场地形, row[136]!=0, row[140]!=0, row[144]!=0) ⇒ **只当布尔**读 ⇒ 线上 0/1。',
        '#   来源：codex units.json 的 terrain 串（按「宇/水/地」关键字拆三个布尔），codex 无则用',
        '#   日服 panel 地形タイプ。两处都认不出关键字 ⇒ 该行三格留空（=0），不猜。本批填 %d / %d 行。'
        % (stats['terrain'], stats['total']),
        '# col7：R001两台按原始wiki类型及v15显示文字投影；其余待审。col8 faction仍未取证。',
        '#   —— 依据serverv/tools/chara_role_crosswalk_v15.json；完整生成器其他历史来源仍待重审。',
        '# 两源冲突清单：names/机体数值-两源冲突清单.csv（%d 条）。' % stats['conflict'],
        '# 生成：python datatables/gen_msma_machine.py',
    ]
    return '\r\n'.join(head + [','.join(f) + ',' for f in rows]) + '\r\n'


def render_detail(pairs_rows):
    head = [
        '#属性名,键,值,',
        '# ===== msma/msma_battle_detail.csv （MSMA_BATTLE_DETAIL / 表ID 34 / 下载序 34 / CMSMABattleDetailTables / 读取 sub_A47BC0）=====',
        '# 本表 = 机体战斗明细的「属性→值」长表：col0 属性名决定进哪张子表，col1 = 練度ID 十进制串，col2 = 值。',
        '# ★col0 词表：RESPAWN_TIME=1 WARP_TIME=2 COST=3 MAX_HP=4 ENERGY=5 MOVE=6',
        '#            BOOST_GAUGEMAX=7 BOOST_GAUGEHEAL=8 BOOST_SPEED=9 JUMP=10',
        '# ★★2026-10-02：同 msma_settings.csv，三层取值（gow wiki → codex updated → codex stale）。',
        '#   RESPAWN_TIME(u32)←再出击时间(秒)  MAX_HP(u32)←装甲      MOVE(float)←最高速度',
        '#   BOOST_GAUGEMAX(u32)←推进容量     BOOST_GAUGEHEAL(float)←推进器冷却',
        '#   COST(u32)←COST                  WARP_TIME(u32)←紧急返回',
        '# ★常量属性（无 codex/日服 来源，取值 = 反解客户端公式；见本生成器 ENERGY_ATTR/BOOST_SPEED_ATTR）：',
        '#   ENERGY      = 1000   ⇒ 注入 sub_581690 时被**客户端钳到 99** 落 +184；',
        '#                         ⛔缺行 ⇒ +184=0 ⇒ 编成判「由于能量耗尽 因此无法出击」✗',
        '#   BOOST_SPEED = col2 0.840000（其余 12 列 0）',
        '#                         ⇒ 面板「最高速度」= MOVE × max(+260,+276) × 1.1904762 ⇒ 0.84 时 == MOVE ✓',
        '#                         ⛔缺行 ⇒ max 为 0 ⇒ 最高速度恒显示 1 ✗',
        '#   （玩家 UI 面板读的是本表，不是 CHARA_PARAM 的数值列 —— 见 06-UI语义字典与参数绑定攻关.md §7.3）',
        '# 不填：JUMP（12 列，无面板绑定也无来源 ⇒ 不猜）。',
        '# 生成：python datatables/gen_msma_machine.py',
    ]
    lines, n = list(head), 0
    for f, v in pairs_rows:
        lid = f[ID_COL]
        if not v:
            continue
        for attr, field, kind in DETAIL_ATTRS:
            if field in v:
                lines.append('%s,%s,%s,' % (attr, lid, fmt(v[field], kind)))
                n += 1
        # ★常量子表（ENERGY / BOOST_SPEED）：与上面 7 项**同集合**（有数值的机体才发）
        for attr, _slot, val in CONST_DETAILS:
            lines.append('%s,%s,%s,' % (attr, lid, val))
            n += 1
    return '\r\n'.join(lines) + '\r\n', n


def project_r001_model_restore(rows):
    # Conditional render restoration; original per-model values are unknown.
    from pathlib import Path
    tools_dir = Path(__file__).resolve().parents[1] / 'serverv' / 'tools'
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    from project_model_restore import project_rows
    return project_rows(rows)


def render_model(model_rows):
    seen, uniq = set(), []
    for _lid, mid in model_rows:
        v = int(mid)
        if v and v not in seen:
            seen.add(v)
            uniq.append(v)
    head = [
        '#ID,',
        '# ===== msma/msma_model.csv （CHARA_MODEL / 表ID 5 / 下载序 5 / CCharaTable / 读取 sub_571380）=====',
        '# ★★★ 行键 col0 = **モデルID（9 位打包值 A*1e8+B*1e6+C*100+NN）**，**不是練度ID** ✗',
        '#   铁证 A（代码链）：sub_571380 以 64 位读法把 col0 落进 a4+0（= 行键）；sub_571BF0 直接取行首 8 字节送',
        '#     sub_473390 分解 ⇒ chara/%02d/%02d/%04d/；而 sub_53F960 用**同一个 64 位值**既查 dword_11EB318',
        '#     (CHARA_MODEL) 又拼同一条路径 ⇒ 行键的编号空间 == chara/ 资源目录号空间。',
        '#   铁证 B（数据）：594 行按 col0 分解 ⇒ 落盘命中 **0/594**（A=0 ⇒ chara/00/... 不存在）；',
        '#     同一批行把モデルID 当键 ⇒ 命中 **593/594**（唯一未落盘 121171002）。',
        '#   ✗ 写成「col0 = 練度ID」⇒ 客户端按モデルID 查不到行 ⇒ NULL ⇒ `fld [ecx+0x30]` 崩（2026-09-18 x64dbg 实证）。',
        '#   ✗ 也不要再往 col71/col72 塞 モデルID：那是普通参数列（+0x1B4/+0x1B8），**不当查表键**。',
        '# 练度ID↔モデルID 映射看 msma_settings.csv 的 col0/col1（本表不需要練度ID）。',
        '# モデルID 源：names/ms_wiki_pairs.json（权威 576）→ names/练度ID-モデルID-全集.csv 兜底。',
        '# 只出能确证モデルID 的机体（本批 %d 行 → 去重 %d 唯一键）；CSV宽77（读取0..76）。' % (len(model_rows), len(uniq)),
        '# 仅101010101/184302101的col14按571380/477300/4C89E1恢复布尔条件；这是功能兼容策略，非原服逐机体值。',
        '# 其余未取证参数留空；其他历史表取值仍未完成来源审计，不可全量运行覆盖当前库。',
        '# 生成：python datatables/gen_msma_machine.py',
    ]
    lines = list(head)
    records = []
    for v in uniq:
        f = [''] * MODEL_COLS
        f[0] = str(v)
        records.append(f)
    for f in project_r001_model_restore(records):
        lines.append(','.join(f) + ',')
    return '\r\n'.join(lines) + '\r\n'


def render_conflict(conflicts):
    head = [
        '#練度ID,机名,モデルID,字段,codex值,日服值,采用,codex状态,日服选取,日服机名,差值codex-日服,',
        '# ===== 机体数值-两源冲突清单（生成：python datatables/gen_msma_machine.py）=====',
        '# 两源（gow wiki / codex）都有值但**不一致**的条目，逐字段一行。',
        '# 机名 = JSON 的 WIKI 名去 `高达OL` 前缀、去尾部地区标注（`（国）`/`（日）`），中文。',
        '# 采用 = 实际落库的那一层的值：**gow wiki 优先**（2026-10-02 用户拍板）。',
        '# 复核方法：gow 侧错 ⇒ 改 `gow_wiki/data/units.json` 或重跑 `gow_wiki/build_units.py`；',
        '#           codex 侧错 ⇒ 改 `codex/data/units.json`。改完整跑生成器即生效。',
        '# 差值 = codex - gow（正 = codex 更大）。',
    ]
    lines = list(head)
    for c in sorted(conflicts, key=lambda x: (x['lid'], x['field'])):
        choose = c['jp'] if c['tier'] == 'gow' else c['codex']
        lines.append(','.join([
            c['lid'],
            cn_name(c['wiki']).replace(',', '・'),
            '',  # モデルID 由调用方补
            FIELD_CN.get(c['field'], c['field']),
            str(c['codex']), str(c['jp']), str(choose),
            c['codex_status'],
            '按名字' if c['jhow'] == 'name' else '启发式',
            c['jp_name'].replace(',', '・'),
            str(c['codex'] - c['jp']),
        ]) + ',')
    return '\r\n'.join(lines) + '\r\n'


# ------------------------------------------------------------------ 自检
def check(text, tag, want_cols=None, digit_first=True, key_col=0):
    b = text.encode('utf-8')
    ok = True
    if b.startswith(b'\xef\xbb\xbf'):
        print('!![%s] 带 BOM' % tag); ok = False
    if b.count(b'\n') != b.count(b'\r\n'):
        print('!![%s] 存在非 CRLF 换行' % tag); ok = False
    body = [x for x in text.split('\r\n') if x and not x.startswith('#')]
    if not body:
        print('!![%s] 无数据行' % tag); ok = False
    if [x for x in body if not x.endswith(',')]:
        print('!![%s] 数据行缺尾逗号' % tag); ok = False
    if want_cols:
        bad = [x for x in body if len(x.split(',')) - 1 != want_cols]
        if bad:
            print('!![%s] 列数 != %d 的行有 %d 条，例：%s' % (tag, want_cols, len(bad), bad[0][:110]))
            ok = False
    if digit_first and [x for x in body if not x.split(',')[key_col].strip().isdigit()]:
        print('!![%s] 键列不是数字' % tag); ok = False
    print('[%s] 自检 %s  UTF-8 无 BOM / CRLF / 尾逗号 / 列数=%s / 数据行=%d'
          % (tag, '✓' if ok else '✗', want_cols or '任意', len(body)))
    return ok


def write_and_backup(path, text):
    if os.path.exists(path):
        bak = path + '.bak_machine'
        if not os.path.exists(bak):
            shutil.copy(path, bak)
            print('  备份 → %s' % os.path.basename(bak))
    with io.open(path, 'wb') as f:
        f.write(text.encode('utf-8'))
    print('  写入 %s' % path)


# ------------------------------------------------------------------ 主流程
def main():
    check_only = '--check' in sys.argv
    lid2pair = load_pairs()
    roster = load_roster()
    bridge = load_bridge()
    mid_full = load_mid_full()
    codex = load_codex()
    _jp_bydev, _jp_byname, jp_resolve = load_jp()
    existing_names = load_existing_names()

    vals, src, conflicts, terrains = build_values(lid2pair, codex, jp_resolve)

    # 名册独有行（不在 JSON 576 里）也尽量补地形：拿桥表的「codex中文名 / 官方中文名」回查 codex。
    # 这些行没有 WIKI 名 ⇒ build_values 里查不到 codex ⇒ 单独补一轮（认不出关键字就不写）。
    terrain_backfill = 0
    for lid, _jp in roster:
        if lid in terrains:
            continue
        row = bridge.get(lid)
        for i in (2, 15):
            v = cell(row, i) if row else ''
            if not v:
                continue
            tf = terrain_flags((codex.get(norm_name(strip_region(v))) or {}).get('terrain'))
            if tf is not None:
                terrains[lid] = tf
                terrain_backfill += 1
                break

    roster_ids = {lid for lid, _n in roster}
    extra_ids = sorted(lid for lid in lid2pair if lid not in roster_ids)

    # ---- 行脊 = 名册（顺序不动）+ JSON 独有追加 ----
    # ★名称一律中文：JSON 覆盖的用 `wiki` 去掉 `高达OL`；其余用桥表的官方中文名 → codex中文名 → 日文名兜底。
    rows, vseq, mid_src = [], [], {'pair': 0, '全集': 0, '无': 0}
    name_src = Counter()

    def cn_for(lid, jp_name):
        if lid in existing_names:
            name_src['现库msma_settings'] += 1
            return existing_names[lid]
        if lid in lid2pair:
            name_src['JSON(去前缀/去地区标注)'] += 1
            return cn_name(lid2pair[lid][1])
        row = bridge.get(lid)
        for i, tag in ((15, '桥表官方中文名'), (2, '桥表codex中文名')):
            v = cell(row, i) if row else ''
            if v:
                name_src[tag] += 1
                return strip_region(v)
        name_src['日文名兜底'] += 1
        return jp_name

    for lid, jp_name in roster:
        if lid in lid2pair:
            mid, mid_src['pair'] = lid2pair[lid][0], mid_src['pair'] + 1
        elif lid in mid_full:
            mid, mid_src['全集'] = mid_full[lid], mid_src['全集'] + 1
        else:
            mid, mid_src['无'] = '', mid_src['无'] + 1
        f = [''] * SET_COLS
        f[ID_COL], f[MID_COL], f[NAME_COL] = lid, mid, cn_for(lid, jp_name).replace(',', '・')
        f[WEAPON_GROUP_COL] = lid
        rows.append(f)
        vseq.append(vals.get(lid, {}))

    for lid in extra_ids:
        mid, wiki = lid2pair[lid]
        if lid in existing_names:
            name_src['现库msma_settings'] += 1
            disp = existing_names[lid]
        else:
            name_src['JSON(去前缀/去地区标注)'] += 1
            disp = cn_name(wiki)
        f = [''] * SET_COLS
        f[ID_COL], f[MID_COL], f[NAME_COL] = lid, mid, disp.replace(',', '・')
        f[WEAPON_GROUP_COL] = lid
        rows.append(f)
        vseq.append(vals.get(lid, {}))

    # ---- 写数值列 + 统计三层 ----
    tiers = {1: 0, 2: 0, 3: 0}
    for f, v in zip(rows, vseq):
        for idx, field in SET_NUM:
            if field in v:
                f[idx] = str(v[field])
        if 'cost' in v:
            f[MCOST_COL] = cost_to_mcost(v['cost'])
        # ★地形适性 col9/10/11（0/1 布尔；见本文件 TERRAIN_* 注释）
        tfl = terrains.get(f[ID_COL])
        if tfl is not None:
            f[TERRAIN_SPACE_COL], f[TERRAIN_WATER_COL], f[TERRAIN_GROUND_COL] = (str(x) for x in tfl)
        # ★战力子表槽：有对应数据行 ⇒ 槽键 = 本行 練度ID（= msma_battle_detail.csv col1）
        for col, field in SLOT_FIELD:
            if field in v:
                f[col] = f[ID_COL]
        # ★常量子表槽（ENERGY / BOOST_SPEED）：判据与 render_detail 完全一致（有数值才发）
        if v:
            for _attr, col, _val in CONST_DETAILS:
                f[col] = f[ID_COL]
        if v:
            s = src.get(f[ID_COL], {})
            layers = {s[k] for _i, k in SET_NUM if k in s}
            if 'gow' in layers:
                tiers[1] += 1
            elif 'codex' in layers:
                tiers[2] += 1
            else:
                tiers[3] += 1

    model_rows = [(f[ID_COL], f[MID_COL]) for f in rows if f[MID_COL].isdigit()]

    stats = {
        'total': len(rows), 'extra': len(extra_ids),
        'filled': sum(1 for v in vseq if v),
        't1': tiers[1], 't2': tiers[2], 't3': tiers[3],
        'conflict': len(conflicts),
        'terrain': len(terrains),
        'terrain_combo': Counter(terrains.values()),
        'names': ' ｜ '.join('%s %d' % (k, v) for k, v in name_src.most_common()),
    }

    settings_text = render_settings(rows, stats)
    rental_text = settings_text.replace('msma_settings.csv', 'msma_rental.csv')
    detail_text, detail_rows = render_detail(list(zip(rows, vseq)))
    model_text = render_model(model_rows)

    conflict_text = render_conflict(conflicts)
    if conflicts:  # 补 モデルID 列
        fixed = []
        for line in conflict_text.split('\r\n'):
            if line.startswith('#') or not line:
                fixed.append(line)
                continue
            p = line.split(',')
            p[2] = lid2pair.get(p[0], ('', ''))[0]
            fixed.append(','.join(p))
        conflict_text = '\r\n'.join(fixed)

    # ---- 报告 ----
    print('基准 ms_wiki_pairs.json：%d 条（練度ID↔モデルID↔WIKI 名）' % len(lid2pair))
    print('名册 favms_ok_list：%d 台 ｜ JSON 独有追加：%d 台 ⇒ 共 %d 行'
          % (len(roster), len(extra_ids), len(rows)))
    for lid in extra_ids:
        print('  追加 %s  %s' % (lid, lid2pair[lid][1]))
    print('col1 モデルID 来源：pairs=%d / 全集csv=%d / 无=%d'
          % (mid_src['pair'], mid_src['全集'], mid_src['无']))
    print('数值三层：① gow wiki %d ｜ ② codex(updated) %d ｜ ③ codex(stale) %d ｜ 合计有值 %d / %d'
          % (tiers[1], tiers[2], tiers[3], stats['filled'], len(lid2pair)))
    print('名称保留现库 col5：%d 台' % len(existing_names))
    print('名称来源：%s' % stats['names'])
    print('地形适性 col9/10/11：填 %d / %d 行 ｜ 组合 %s ｜ 空 %d 行'
          % (stats['terrain'], len(rows),
             ' ｜ '.join('宇%d水%d地%d ×%d' % (k[0], k[1], k[2], n)
                         for k, n in sorted(stats['terrain_combo'].items())),
             len(rows) - stats['terrain']))
    print('两源冲突 %d 项 ｜ msma_battle_detail %d 行（%d 属性 × %d 台）｜ msma_model %d 行（%d 唯一モデルID）'
          % (len(conflicts), detail_rows, len(DETAIL_ATTRS) + len(CONST_DETAILS), stats['filled'],
             len(model_rows), len({int(m) for _, m in model_rows})))

    if not check_only:
        print('\n[1] msma_settings.csv');      write_and_backup(os.path.join(MSDIR, 'msma_settings.csv'), settings_text)
        print('\n[2] msma_rental.csv');        write_and_backup(os.path.join(MSDIR, 'msma_rental.csv'), rental_text)
        print('\n[3] msma_battle_detail.csv'); write_and_backup(os.path.join(MSDIR, 'msma_battle_detail.csv'), detail_text)
        print('\n[4] msma_model.csv');         write_and_backup(os.path.join(MSDIR, 'msma_model.csv'), model_text)
        print('\n[5] 机体数值-两源冲突清单.csv')
        with io.open(CONFLICT, 'wb') as f:
            f.write(conflict_text.encode('utf-8'))
        print('  写入 %s（%d 条）' % (CONFLICT, len(conflicts)))
        print()

    ok = True
    ok = check(settings_text, 'settings', SET_COLS) and ok
    ok = check(rental_text, 'rental', SET_COLS) and ok
    ok = check(detail_text, 'detail', DETAIL_COLS, digit_first=False, key_col=1) and ok
    ok = check(model_text, 'model', MODEL_COLS) and ok
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
