# -*- coding: utf-8 -*-
"""生成《服务端数据表还原专案》的记录文件。

输入（只读，不修改）：
  ../reverse-login-chain/formats/tables_spec.json  列规格（79 表 / 1155 列位 / 0 未解析）
  ../reverse-login-chain/formats/enums.json        枚举值表（名↔值）
  ../reverse-login-chain/formats/_idmap.json       下载序 → 表ID → 定义名
  ../unpackdat/settings/download_list.csv          文件名
  ../unpackdat/codex/data/units.json               机体数值资料源（B站高达WIKI 遗留，699 台）

输出（本目录）：
  00-表清单与用途.md        79 表总表（用途启发 / 资源对应 / 列数 / 枚举列数 / 状态）
  01-列注释/NN-<定义名>.md  逐表：用途 + 每列"大概用来做什么"的注释（含填写规则与示例）
  02-资料源.md              外部资料源与 data/ 资源族对照（codex / chara / item / interface / fx）
  03-还原进度.md            逐表还原状态追踪表
用法： python gen_column_notes.py
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FMT = os.path.join(ROOT, 'reverse-login-chain', 'formats')
CODEX = os.path.join(ROOT, 'unpackdat', 'codex', 'data', 'units.json')

# ── 用途（启发）：定义名 → 中文用途 ────────────────────────────────────────────
PURPOSE = {
    'AUTOEXEC': '服务端启动脚本（脚本方言，**不是 CSV**，无列定义）',
    'MSMA_WEAPONSET': '机体武器组（一台机体可挂的武器集合）',
    'MSMA_WEAPON_EQUIPCOMB': '武器装备组合规则（哪些武器能同时装备）',
    'MSMA_COLORSET': '机体配色方案',
    'CHARA_PARAM': '★机体参数主表（HP/装甲/推进/载重… 主数值）',
    'CHARA_MODEL': '★机体模型与基础属性（外观/体型/固有能力）',
    'ITEM': '★物品总表（武器/材料/道具/票券…）',
    'ITEM_USE': '消耗品使用效果',
    'ITEM_PART': '装备零件（部件）',
    'BULLET': '子弹/弹丸定义（弹速/伤害/存活时间）',
    'WRESTLE_PARAM': '格斗（近战）参数',
    'ITEM_TOKEN': '代币/票券类物品',
    'LVUP_PILOT': '机师等级成长曲线',
    'LVUP_PILOT_EXAM': '机师考核（考试）等级曲线',
    'LVUP_PILOT_CLASS': '机师军衔升级需求',
    'LVUP_CLAN': '部队（Clan）等级成长',
    'MECHANIC_MSMA': '机体开发（生产）配方',
    'MECHANIC_WEAPON': '武器开发（生产）配方',
    'MECHANIC_SUCCESS': '开发券 / 开发成功概率',
    'MSMA_PLAN': '机体图纸（开发计划）',
    'MISSION_EXTRULE': '任务附加规则',
    'MISSION_VS': '对战任务定义',
    'MISSION_COOP': '协作战任务定义',
    'MISSION_GROUP': '任务分组',
    'MISSION_SAFETY_AREA': '任务安全区（可战区域限制）',
    'COMMANDER_NPC': '指挥官 NPC 定义',
    'COMMANDER_SUPPORT': '指挥官支援（支援技能）',
    'COMBAT_OPERATION': '战术/作战指令',
    'GACHA': '扭蛋（抽卡）奖池',
    'MSMA_BATTLE_DETAIL': '机体战斗明细（战斗内参数）',
    'MSMA_RENTAL': '机体租借',
    'WEAPON_BATTLE_DETAIL': '武器战斗明细',
    'WEAPON_SETTING': '武器设置（射击/命中/弹道参数）',
    'MSMA_FORMATION': '机体 NPC 编队',
    'BUILDUP_WEAPON': '武器强化（改造）参数',
    'BUFF': '增益/减益效果定义',
    'AI_PARAM': 'NPC AI 参数',
    'AI_WEAPON_PARAM': 'NPC AI 武器参数',
    'DAILY_RECORD': '机师日常记录（每日战绩）',
    'NETCAFE_CHALLENGE': '网吧挑战',
    'CLAN_CHALLENGE': '部队挑战',
    'TROOP_CHALLENGE': '势力挑战',
    'OVERHAUL': '大修 / 翻新',
    'MODULE': '模块（固有模块）定义',
    'MODULE_DEVELOP': '模块开发',
    'MODULE_BONUS': '模块加成',
    'MSMA_MODULE': '机体可装模块槽',
    'CHALLENGE_HIGHSCORE': '挑战最高分',
    'PLAY_BONUS_REWARD': '游玩奖励',
    'BANNER_INFO': '横幅（公告图）信息',
    'ACTION_MODULE_INFO': '动作模块参数',
    'ITEMPACK_INFO': '物品包内容',
    'FORCEGAUGE_INFO': '战力槽（force gauge）',
    'LVUP_FAVMS': '喜爱机体升级',
    'MSMA_FAVMS': '喜爱机体列表',
    'BYWORD': '称号（byword）',
    'MSMA_BREAKUP': '机体拆解',
    'MSMA_FLIGHT_SET': '机体飞行/浮游设置',
    'MSMA_MISSIONUNIT': '任务出击单位',
    'QUEST': '任务/委托',
    'PLAYER_NAVI': '玩家引导（Navi）',
    'DAMAGE_FIELD_PARAM': '伤害场（damage field）参数',
    'MODULE_BONUS_LOT': '模块加成抽取',
    'MODULE_RENTAL': '模块租借',
    'OVER_CUSTOM': '机体超改（over custom）',
    'OVER_CUSTOM_CUPSULE': '超改胶囊',
    'OVER_CUSTOM_DEVELOP': '超改开发配方',
    'MISSION_XWAR_BANPICK': '跨服战（XWAR）Ban/Pick 规则',
    'MONTHLY_BONUS_REWARD': '月度奖励',
    'MSMA_ADOP': '机体采纳/领养（advanced option）',
    'SEASON_CLASS_IMFORMATION': '赛季阶级信息',
    'SEASON_CLASS_UP_REWARD': '赛季阶级升级奖励',
    'SEASON_RANKERBATTLE_REWARD': '赛季排名战奖励',
    'TREND_DATA_WEAPON': '武器流行数据（趋势）',
    'BEGINNER_CHALLENGE': '新手挑战',
    'SCORE_CONFIG_CATEGORY': '分数配置分类',
    'LVUP_MSMA': '机体等级成长（**本地表**，不下发）',
    'MSMA_MATERIAL': '机体素材（**本地表**）',
    'BGMPACKAGE': 'BGM 包（**本地表**）',
}

# ── 资源对应（启发）：定义名 → unpackdat 下的资源族 ───────────────────────────
RESOURCE = {
    'CHARA_PARAM': '`chara/`（118230 个文件：模型/贴图）',
    'CHARA_MODEL': '`chara/`',
    'MSMA_WEAPONSET': '`item/`、`chara/`',
    'MSMA_WEAPON_EQUIPCOMB': '`item/`',
    'MSMA_COLORSET': '`chara/`（配色贴图）',
    'ITEM': '`item/`（11791）',
    'ITEM_USE': '`item/`',
    'ITEM_PART': '`item/`',
    'BULLET': '`fx/`（10776：弹道/命中特效）',
    'WRESTLE_PARAM': '`fx/`',
    'ITEM_TOKEN': '`item/`',
    'MECHANIC_MSMA': '`item/`',
    'MECHANIC_WEAPON': '`item/`',
    'MSMA_PLAN': '`item/`',
    'MODULE': '`item/`',
    'MODULE_BONUS': '`item/`',
    'MSMA_MODULE': '`item/`',
    'BUFF': '`fx/`',
    'BANNER_INFO': '`interface/`（43358：UI/图片）',
    'SCORE_CONFIG_CATEGORY': '`interface/`',
    'PLAYER_NAVI': '`interface/`',
    'MISSION_VS': '`interface/`（任务缩略图）',
    'MISSION_COOP': '`interface/`',
    'MSMA_FORMATION': '`chara/`',
    'MISSION_SAFETY_AREA': '`chara/`+`interface/`',
    'BGMPACKAGE': '（BGM 音频）',
}

# ── 已知列语义（来自 topics/16 §2 手工分析）：表ID → {列号: 注释} ──────────────
KNOWN_COL = {
    65: {
        0: '物品ID（主键）',
        1: '数值 u32（topics/16 记为内存 +4，语义未定）',
        2: '**名称**（字符串）',
        3: '**说明**（字符串）',
        4: '**物品类型**（枚举 25 值；写名称如 `WEAPON`，见 `枚举表.md sub_593770`）',
        5: '数值（u16，未定）',
        6: '数值（u32，未定）',
        7: '数值（u16，未定）',
    },
    1: {
        0: '武器组ID（主键）',
        4: '类别（枚举 `sub_586450`：`MAIN`/`EX`/`0`）',
        5: '**武器类型**（枚举 28 值 `sub_585FD0`：`MACHINEGUN`…，见 枚举表）',
        6: 'bool 开关',
        27: '★**地区开关**：写 `JAPAN` ⇒ **整行被丢弃** ✗；写 `CHINA` 或留空 ⇒ 保留 ✓（见 topics/16 §2.5）',
    },
    4: {
        0: '模型ID（主键；对应 `chara/` 资源）',
        1: '数值 u64',
        2: '数值 u64',
        3: '数值 u16',
        4: '类别（枚举 `sub_580610`：`RANK2`..`RANK5`）',
        5: '**名称**',
        6: '**说明**',
        7: '类别（枚举）',
        8: '类别（枚举 u64）',
        9: '数值 u32',
        10: '数值 u32',
        11: '数值 u32',
        36: '系数 float',
        37: '系数 float',
        38: '数值 u32',
        56: '文本', 58: '文本', 60: '文本', 62: '文本', 64: '文本',
        67: '文本', 69: '文本', 71: '文本', 87: '文本',
    },
    5: {
        0: '模型ID（主键 u64；对应 `chara/` 资源）',
        1: 'float 参数', 2: 'float 参数', 3: 'float 参数', 4: 'float 参数',
        5: 'float 参数', 6: 'bool 开关',
        7: 'float', 8: 'float', 9: 'float', 11: 'float',
        12: 'bool', 13: 'bool', 14: 'bool', 15: 'float',
        32: '字符串', 33: '字符串', 34: '字符串',
        35: 'u8 参数', 36: '字符串', 41: 'float', 44: 'bool', 46: 'float',
        47: 'bool', 48: 'bool', 49: 'bool',
        50: '字符串', 51: '字符串', 52: '字符串',
        53: 'float', 54: 'bool', 55: '字符串（枚举 `sub_571290`）',
        56: 'float', 57: 'float', 58: 'float', 59: 'float',
    },
}

# ── 区段注释（启发）：表ID → [说明文本] ──────────────────────────────────────
KNOWN_RANGE = {
    4: ['列 13 / 15..21 / 22 / 24..29 / 30..32 / 34 = **开关位**（`sub_BBB370 != 0` ⇒ bool；内存位图在 +840/+841/+842）',
        '列 12/14/23/33/43/45/53/57/59/61/63/65/66/68/70… 等**未被读取** ⇒ 留空即可（越界列读作 0）'],
    5: ['列 16..31 = **u32×16**（代码里 2×8 循环、内存步长 8 交错布局）',
        '列 61..77 = bool/u32/u16 混合'],
    1: ['列 8/10/11、12/14/15、16/18/19 = u32 三组×3',
        '列 ~25 有联动：某组数值全空时上限自动置 9999（见 topics/16 §2.5）'],
    40: ['col0=ID；随后循环 10 次，每轮读「col v6（bool，且 ×10 存另一处）」与「col v6+10」⇒ 列 1..10 与 11..20'],
    53: ['col0=ID；随后 v3=2 起、**步长 2**、共 10 个 ⇒ 列 2,4,6,…,20'],
    79: ['col0=ID；随后 `result+1`（result=0..9）⇒ 列 1..10'],
    14: ['col0=ID；随后循环 1..9 ⇒ 列 1..9（内存里做**累加**：`第 n 列 = 第 n 列 + 第 n-1 列`）'],
    29: ['只读 col 3/4/7/8/0x0B（u32）与 col 0x0C（float）；其余列留空'],
    39: ['col3 是字符串，其余为 u32'],
    69: ['col0 = 字符串（类别名，主键）；col1 = 枚举（经 `sub_5812E0`）'],
}

COL_HEAD = {}


def load(name):
    with io.open(os.path.join(FMT, name), encoding='utf-8') as f:
        return json.load(f)


def main():
    spec = load('tables_spec.json')
    enums = load('enums.json')
    idmap = load('_idmap.json')
    def2id = {r['def']: int(r['id']) for r in idmap}
    # ★ 枚举列按【读序】与 enums.json 的 usedby 顺序对应（enums.json 里存的是旧表达式，不能用 (id,col) 直接查 ✗）
    enumcols = {}
    for s in spec:
        enumcols[s['tableId']] = [c for c in (s.get('cols') or []) if c['type'] == 'enum']
    enum_of = {}
    try:
        conv = load('_enum_conv.json')
    except Exception:
        conv = None
    if conv:
        for fn, lst in conv.items():
            sz = enums.get(fn, {}).get('n') or len(enums.get(fn, {}).get('lits') or [])
            for u in lst:
                enum_of.setdefault((u['id'], u['col']), (fn, sz))
    else:
        for fn, r in enums.items():
            cnt = {}
            for u in r.get('usedby') or []:
                tid = u['id']
                k = cnt.get(tid, 0)
                cnt[tid] = k + 1
                lst = enumcols.get(tid) or []
                col = lst[k]['col'] if k < len(lst) else u['col']
                enum_of.setdefault((tid, col), (fn, r.get('n') or len(r.get('lits') or [])))
    # ★ 含 MS_* 名称的枚举 = "机体参数名"（与 codex units.json 的 armor/speed/… 对应）
    ms_enum = set()
    for fn, r in enums.items():
        for row in r.get('table') or []:
            if isinstance(row, list) and row and str(row[0]).startswith('MS_'):
                ms_enum.add(fn)
                break
    CODEX_MAP = {'MS_ARMOR': 'armor', 'MS_ARMOR_NOW': 'armor', 'MS_BOOST_SPEED': 'speed',
                 'MS_BOOST_GAUGE': 'boost', 'MS_BOOST_RECOVER': 'boost_cd',
                 'MS_PAYLOAD': 'payload', 'MS_WARP': '', 'MS_DEF_SOLID': 'shield'}
    os.makedirs(os.path.join(HERE, '01-列注释'), exist_ok=True)

    lines0 = ['# 00 · 表清单与用途（服务端数据表还原专案）', '',
              '> 用途列为**启发**（由类名/定义名/列形态/资源族推断），标 ★ 的是主表。',
              '> 列定义来源：`reverse-login-chain/formats/tables_spec.json`（78/79 解出、1155 列位、0 未解析）。',
              '> 逐表列注释见 `01-列注释/`。', '',
              '| 下载序 | 表ID | 文件 | 定义名 | 用途（启发） | 类名 | 列数 | 枚举列 | 资源对应 |',
              '|---|---|---|---|---|---|---|---|---|']
    rows_prog = []
    for s in spec:
        deff = s['defName']
        ne = sum(1 for c in s['cols'] if c['type'] == 'enum')
        lines0.append('| %d | %d | `%s` | %s | %s | %s | %d | %d | %s |' % (
            s['downloadIndex'], s['tableId'], s['fileName'] or '—', deff,
            PURPOSE.get(deff, '⚠️待补'), s['className'] or '?', s['colCount'], ne,
            RESOURCE.get(deff, '—')))
        rows_prog.append((s['downloadIndex'], s['tableId'], s['fileName'] or deff, deff, s['colCount']))
    with io.open(os.path.join(HERE, '00-表清单与用途.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines0) + '\n')

    # 逐表列注释
    for s in spec:
        deff = s['defName']
        name = '%02d-%s-%s.md' % (s['downloadIndex'], s['tableId'], deff)
        L = ['# %s ｜ `%s`' % (deff, s['fileName'] or '(本地表，不下发)'), '',
             '- **用途（启发）**：%s' % PURPOSE.get(deff, '⚠️待补'),
             '- 资源对应（启发）：%s' % RESOURCE.get(deff, '—'),
             '- 表ID `%d` ｜ 下载序 `%d` ｜ 类名 `%s` ｜ 全局 `%s` ｜ ctor `%s` ｜ 派生 vtable `%s`' % (
                 s['tableId'], s['downloadIndex'], s['className'] or '?', s['global'], s['ctor'], s['vtable']),
             '- 逐列读取函数 `%s` ｜ **列数 %d**' % (s['reader'], s['colCount']), '']
        if not s['cols']:
            L += ['> 本表无需列定义（AUTOEXEC 是脚本方言）。', '']
        else:
            kn = KNOWN_COL.get(s['tableId'], {})
            L += ['| 读序 | 列号（CSV 位置） | 类型 | 大概用来做什么（启发） |',
                  '|---|---|---|---|']
            cs = s['cols']
            for i, c in enumerate(cs):
                col = c['col']
                try:
                    ck = int(col, 0)
                except Exception:
                    ck = None
                note = kn.get(ck)
                if note is None:
                    if c['type'] == 'enum':
                        e = enum_of.get((s['tableId'], col))
                        if e:
                            note = '枚举/类别 —— 写**名称**（可选 %d 个，见 `枚举表.md` `%s`）' % (e[1], e[0])
                            if e[0] in ms_enum:
                                note = ('★**机体参数名**（`%s`：`MS_ARMOR`/`MS_BOOST_SPEED`/`MS_PAYLOAD`…）'
                                        '——"参数名 + 数值"成对，数值取 `codex/data/units.json` 的 '
                                        '`armor`/`speed`/`boost`/`payload` 等' % e[0])
                        else:
                            note = '枚举/类别 —— 写名称（⚠️转换函数未识别，标 `?`）'
                    elif c['type'] == 'str':
                        note = '文本（名称/说明类）'
                    elif c['type'] == 'float':
                        note = '浮点参数（系数/倍率）'
                    elif ck == 0:
                        note = '主键/索引ID'
                    else:
                        note = '整型参数（待定）'
                L.append('| %d | `%s` | %s | %s |' % (i, col, c['type'], note))
            L.append('')
            if s['tableId'] in KNOWN_RANGE:
                L.append('**区段说明**：')
                for t in KNOWN_RANGE[s['tableId']]:
                    L.append('- %s' % t)
                L.append('')
            L += ['**填写规则（通用）**：',
                  '- 编码 **UTF-8 无 BOM**、换行 **CRLF**、数据行**保留尾逗号**；`#` 开头整行跳过（表头也用它）。',
                  '- **越界列 = 0**：只需要写到"你要设的最大列号"，后面可省略。',
                  '- 枚举列写**名称字符串**（写错/未知名 ⇒ 该列读作 0）。',
                  '- 每个数据行至少要有 1 个单元格。', '']
        with io.open(os.path.join(HERE, '01-列注释', name), 'w', encoding='utf-8') as f:
            f.write('\n'.join(L) + '\n')

    # 02 资料源
    codex_info = {}
    try:
        with io.open(CODEX, encoding='utf-8') as f:
            d = json.load(f)
        codex_info = {'source': d.get('source'), 'count': d.get('count'),
                      'keys': list((d.get('units') or [{}])[0].keys())}
    except Exception as e:
        codex_info = {'err': str(e)}
    L2 = ['# 02 · 资料源（外部数据 + data/ 资源族）', '',
          '## A. 机体数值 —— `unpackdat/codex/data/units.json`（★主力资料源）', '',
          '- 来源：%s' % codex_info.get('source'),
          '- 快照：**%s 台**（官服停运后从 B 站高达 WIKI「机体对比工具」导出）' % codex_info.get('count'),
          '- 单条字段：`%s`' % '`, `'.join(codex_info.get('keys') or []),
          '- 字段→表列（**启发**）：`armor`→装甲、`shield`→护盾、`speed`→速度、`boost`/`boost_cd`→推进/冷却、',
          '  `payload`→载重、`return_val`→回归值、`down`→倒地值、`slots`→模块槽、`cost`→COST、`type`→类型、',
          '  `terrain`→地形适性、`faction`→势力。',
          '  ⇒ 这些名字与**枚举 `sub_5953B0`（129 条 `MS_ARMOR`/`MS_BOOST_SPEED`/`MS_PAYLOAD`…）** 高度对应，',
          '  是 `CHARA_PARAM`(列 4 等) 与 `CHARA_MODEL` 填值的首选来源。', '',
          '## B. `unpackdat/` 资源族（用于"资源 ↔ 表"对应）', '',
          '| 目录 | 文件数 | 用途（启发） |', '|---|---|---|',
          '| `chara/` | 118230 | 机体模型/贴图 ⇒ 与 `CHARA_MODEL.col0`(模型ID)、`MSMA_FORMATION` 对应 |',
          '| `item/` | 11791 | 物品图标 ⇒ 与 `ITEM.col0`、`ITEM_PART`、`MODULE` 对应 |',
          '| `interface/` | 43358 | UI/公告图 ⇒ 与 `BANNER_INFO`、`MISSION_*` 缩略图对应 |',
          '| `fx/` | 10776 | 特效 ⇒ 与 `BULLET`、`BUFF` 对应 |',
          '| `settings/` | 73 | CSV 方言样本 + `download_list.csv`（76 行清单） |',
          '| `font/` | 1 | 字体 |', '',
          '## C. 已生成的占位内容（现状）', '',
          '- 服务端应答目录 `server/datafiles/` 现存 **76 个文件**（`make_datafiles.py` 生成，多为空表占位）。',
          '- `server/autoexec_sv.cfg` = 可用的启动脚本（唯一"有真内容"的文件）。', '',
          '## D. 其它资料面（待挖）', '',
          '- 客户端本地 CSV（`unpackdat/settings/`）只有 73 个文件，**与这 76 张表不同名** ⇒ 不能直接当内容用，',
          '  但它们是**同族 CSV 方言**的样本（BOM/换行/尾逗号/编码）。',
          '- 客户端 `XDt/` 日志（已破解，`.codebuddy/xtdlog.py`）可能含服务端下发给客户端的数值快照。']
    with io.open(os.path.join(HERE, '02-资料源.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L2) + '\n')

    # 03 进度
    L3 = ['# 03 · 还原进度（逐表）', '',
          '> 状态：`列已注释` → `有内容`（能跑）→ `数值已校准`。每张表完成后在此打勾并写下依据。', '',
          '| 下载序 | 表ID | 文件 | 定义名 | 列数 | 列已注释 | 有内容 | 数值已校准 | 备注 |',
          '|---|---|---|---|---|---|---|---|---|']
    for di, tid, fn, deff, nc in rows_prog:
        L3.append('| %d | %d | `%s` | %s | %d | ✅ | ⬜ | ⬜ | |' % (di, tid, fn, deff, nc))
    with io.open(os.path.join(HERE, '03-还原进度.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L3) + '\n')

    print('OK: %d tables -> 00/01/02/03' % len(spec))


if __name__ == '__main__':
    main()
