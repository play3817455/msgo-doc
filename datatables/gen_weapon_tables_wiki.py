# -*- coding: utf-8 -*-
"""gen_weapon_tables_wiki.py —— 把「真值武器ID + wiki 名/数值」落到 #78 / #36 / #37。

★口径（2026-09-28，用户拍板 real_sub4）：
  武器ID / 名称 / 数值 全部来自 `names/武器分配明细.csv`
  （由 gen_weapon_set_wiki.py 产出，ID = '2'+練度ID[1:5]+sub4 ⇒ **100% 可落资源**）

产出：
  item/item.csv                 #78  col0=ID col2=名称 col4=WEAPON
  item/weapon_battle_detail.csv #36  `属性名,武器ID字符串,值`（11 项词表见 36-列注释）
  item/weapon_settings.csv      #37  col0=ID col1=0 col2=1 col13=持握 col14=动作层索引减1（未知留空） col21=52类 col29=散布 col30=攻击类型 col31=锁定 col32=属性

★★口径（2026-10-04 定案，根因见 `weapon_client_raw.py` 文件头）★★
  #36 的值列存的是 **客户端原值**，不是 wiki/机库显示的面板值 ——
  读侧 `serverv/internal/store/battle_params.go::panelPowerFromClientRaw` 会把 POWER 乘 10
  还原成面板威力，再交给 `DamageFor` 做 `ceiling(威力/10)`。
  ⇒ 本脚本写 #36 时**必须**过 `weapon_client_raw` 的换算（威力/集弹/连射/装填/锁定），
    射程距离 / 红锁距离按世界单位**原样**写。
  ⚠️ 历史版本直接把 wiki 面板值写进去（威力 45000 而不是 4500）⇒ 一旦被
    `cfgsync -bootstrap-csv` 灌进空表，全武器伤害 ×10（"一发秒杀一切"）。

★★口径（2026-10-05 / C4 深修定案）★★
  1. **列号回退链**：`weapon_client_raw.SIDECAR_36_FALLBACK`。`RELOAD` 主列 col14「装填性能」
     与备用列 col15「装填时间」在 sidecar 里**严格互斥**（930/540/0/155），不回退就少 540 键。
  2. **整族重写 = 8 族**（`RAW.FAMILIES_36`：POWER / STABILITY / RAPIDDELAY / COOLTIME /
     RANGE / RELOAD / LOCKON_CAM / HIGH_LOCKON）：sidecar 有行的键先整族清掉再重建，
     否则旧管线灌进来的面板刻度残渣（STABILITY 920 / RELOAD 800 / LOCKON_CAM 760…）永驻。
  3. **原值域哨**：`STABILITY` / `RELOAD` / `LOCKON_CAM` 连同 `RAPIDDELAY`/`COOLTIME`
     一起过 `RAW.is_raw_domain`，域外一律 `SystemExit`。
  4. **管理域外的键（8 位 icon-id 族）本脚本不管**：它们不在 `_purge_fam36` 的判据里，
     权威是库（`load_paired_ms_db.py` ← `gow_wiki/data/units.json`）。那 32 行 CSV 残渣
     （面板值直写）由 `apply_weapon_tables_db.py` 的**库→CSV 回灌**收敛，见其文件头 §口径。

用法：
  python gen_weapon_tables_wiki.py            # 报告（含旧 ID 可落资源体检）
  python gen_weapon_tables_wiki.py --apply    # 写入三张表（备份一次 + 方言自检）
"""
import collections
import csv
import io
import os
import re
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, '.codebuddy'))
import fpmf_scan as F
import weapon_client_raw as RAW

GAME = os.path.join(ROOT, '机动战士敢达Online', 'GundamOnline')
SIDE = os.path.join(HERE, 'names', '武器分配明细.csv')
DF = os.path.join(ROOT, 'server', 'datafiles', 'lounge')
T78 = os.path.join(DF, 'item', 'item.csv')
T36 = os.path.join(DF, 'item', 'weapon_battle_detail.csv')
T37 = os.path.join(DF, 'item', 'weapon_settings.csv')

# ── 28 值（weapon_set col5，sub_585FD0）→ 52 值（#37 col21，sub_596B70）
C28_2_C52 = {
    'MACHINEGUN': 'MACHINEGUN', 'SUBMACHINEGUN': 'MACHINEGUN',
    'SHOTGUN': 'SHOTGUN', 'BEAM_RIFLE': 'BEAM', 'BEAM_SPRAYGUN': 'BEAM',
    'CHARGE_RIFLE': 'BEAM', 'BEAM_SNIPE': 'SNIPE', 'SNIPER_RIFLE': 'SNIPE',
    'BAZOOKA': 'BAZOOKA', 'CHARGE_BAZOOKA': 'BAZOOKA', 'HOWITZER': 'BAZOOKA',
    'MISSILE': 'MISSILE', 'TRENCH_MORTAR': 'TRENCH_MORTAR',
    'HAND_THROW': 'HAND_THROW', 'LANDMINE': 'LANDMINE', 'WRESTLE': 'WRESTLE',
    'SHIELD': 'SHIELD', 'REPAIR': 'REPAIR', 'RADARPOD': 'RADAR', 'CAMERAGUN': 'CAMERAGUN',
}
# ★★POWER 的符号：**表里必须写正值**，由**客户端消费端**取负。
#   证据（反汇编 sub_59A070，2026-09-28 实测）：
#     v3 = 表里的 POWER（正）；v4 = 武器类别（#37 col21 → 武器对象 +84）
#     *(obj+1936) = v3;
#     if (v4==12 || v4==43 || v4==38 || v4==24 || v4==36 || v4==53) *(obj+1936) = -v3;   // ← 这里取负
#   ⇒ 6 个回复/补给系类别 = {12 REPAIR, 43 WRESTLE_REPAIR, 38 RESURRECT,
#                          24 BULLET_PACK, 36 REPAIR_PACK, 53 REPAIR_THROW}
#   ⚠️ 早期版本在本脚本里也取负（`NEG_C52`）⇒ 会**双重取负变成正**。已按实证删除。
#   ⚠️ `datatables/12-武器数据落地方案.md` §「写负值」的说法**与反汇编不符**，以本条为准。

# ★col13「持握」基线（按类别给；`sub_5968A0` 枚举 11 值：ONEHAND=2 SHOLDER=3 TWOHAND=4
#   SHIELD=5 PECULIAR_1..6=6..11 MODELORIGIN=12）。wiki **无此列** ⇒ 只能按类别给基线，
#   属**本服占位口径**（姿势可见，但非客户端真值）。
GRIP_BY_CAT = {'SHIELD': 'SHIELD', 'WRESTLE': 'TWOHAND',
               'BAZOOKA': 'SHOLDER', 'TRENCH_MORTAR': 'SHOLDER', 'MISSILE': 'SHOLDER'}

# ★缺失 POWER 的兜底基线（**面板值**，正值），取 `09-武器数值口径提案.md` §3 各组区间中点。
#   仅用于 wiki 没给「威力」的行（实测 58 行：REPAIR 35/35 全空、RADARPOD 5/5 全空 等）。
#   属**本服占位口径**，非客户端真值；要调平衡改这张表重跑即可。
#   ⚠️ 单位是**面板值**，写表前过 `RAW.power_raw` 换成原值。
BASE_POWER = {'REPAIR': 400, 'RADAR': 200, 'CAMERAGUN': 200,
              'MACHINEGUN': 275, 'SHOTGUN': 275, 'BEAM': 950, 'SNIPE': 1600,
              'BAZOOKA': 1200, 'MISSILE': 800, 'TRENCH_MORTAR': 1200,
              'WRESTLE': 1400, 'HAND_THROW': 200, 'LANDMINE': 200}
BASE_POWER_DEFAULT = 300
# 盾走独立 `SHIELD` 子表，不写 POWER
NO_POWER = {'SHIELD'}
# 射击模式（wiki col6）→ 发射模式（#37 col30，sub_596C60 29 值）
MODE2TRAJ = [('自动', 'GUN_RAPID'), ('三点', 'GUN_RAPID'), ('二点', 'GUN_RAPID'),
             ('照射', 'GUN_RAPID'), ('单发散射', 'GUN_SINGLE'), ('单发', 'GUN_SINGLE'),
             ('蓄力', 'GUN_SINGLE'), ('投掷', 'HAND_THROW'), ('开镜', 'SNIPE_BEAM')]
# wiki 列（**sidecar 列号**）→ #36 属性名 + 「面板 → 客户端原值」换算函数。
# ★口径与换算的唯一出处是 `weapon_client_raw.SIDECAR_36`（含 IDA 实测常量与出处表）。
N36 = RAW.SIDECAR_36
# ★wiki 有两档值 `基准(强化)`（如 `800(880)` / `760(912)` / `4500(4950)`）。
#   口径（`12-武器数据落地方案.md` §取值细则）：**取第一档（基准）**。
#   ⚠️ 早期版本直接用 `int(float(v))` / `fullmatch(数字)` ⇒ **两档值整格被判非法而丢弃**
#      （实测：威力 182 格 + 射程/集弹/锁定等浮动列若干）⇒ 那些武器此前根本没落 POWER/数值。
TIER = re.compile(r'^\s*(-?\d+(?:\.\d+)?)')


def first_tier(v):
    """`800(880)` → '800'；`-` / 空 / 非数字 → None"""
    m = TIER.match(v or '')
    return m.group(1) if m else None


def rd(p):
    if not os.path.exists(p):
        return []
    return [r for r in csv.reader(open(p, encoding='utf-8', errors='replace', newline='')
                                  .read().replace('\r\n', '\n').split('\n'))
            if r and any(x.strip() for x in r)]


# ── 资源目录（判旧 ID 能否落地）
_, _files = F.load_hed(os.path.join(GAME, 'data', 'item.hed'))
DIRS = collections.defaultdict(set)
for _f in _files:
    p = (_f['path'] or _f['folder']).lstrip('.\\/').replace('\\', '/').split('/')
    if len(p) >= 2:
        DIRS[p[0]].add(p[1])


def resolvable(i):
    """ID 能否落到 item/<cat>/<sub4>（前缀长度 2/3/4 都试）"""
    if not i.isdigit() or len(i) < 6:
        return False
    cat = i[0].zfill(2)
    if cat not in DIRS:
        return False
    return any(i[len(i) - 4:] in DIRS[cat] for _ in (0,))


# ── 读 sidecar
S = [r for r in rd(SIDE) if r and r[0].strip().isdigit()]
print('sidecar 武器行 %d' % len(S))
H = S[0]

# ── 旧 ID 体检
print()
print('--- 三张表现有武器的「可落资源」体检（旧轮转填充遗物）---')
legacy = {}
for name, path, kc in [('#78 item.csv', T78, 0), ('#37 weapon_settings.csv', T37, 0),
                       ('#36 weapon_battle_detail.csv', T36, 1)]:
    D = [r for r in rd(path) if not r[0].startswith('#')]
    ids = sorted(set(r[kc].strip() for r in D if len(r) > kc and r[kc].strip()))
    ok = [i for i in ids if resolvable(i)]
    legacy[name] = (len(ids), len(ok))
    print('  %-30s 唯一ID=%-5d 可落资源=%-5d (%.0f%%)  例:%s' % (name, len(ids), len(ok),
          100 * len(ok) / max(1, len(ids)), ok[:4]))

# ── ★口径哨（2026-10-04 立）：#36/#37 的键必须落在「可达号域」内 ──────────────
# 可达号域 = 本脚本产出的 9 位武器号 ∪ 客户端 `weapon_wrestle.csv` 的 8 个近战短号
#            ∪ 现役引用（msma_weapon_set col2 / game.unlockw / game.ms_rokaku）。
# 权威出处 = `datatables/names/可达武器号域.csv`，由
#            `purge_unreachable_weapon_keys.py` 生成（那边一并做收敛）。
# 证据（详见 `purge_unreachable_weapon_keys.py` 头注）：
#   · 客户端自带 `unpackdat/settings/weapon_visual_customize.csv` 表头第 1 列即 `#武器ID`，
#     45 行全是 9 位；现役 `msma_weapon_set.csv` col2（sub_587160 读的那列）也是 9 位。
#   · 库里那些短号来自另外三条历史管线：图标号（`gow_wiki/data/weapon_icon_match.json`
#     的 icon_id，如 02012401=ビーム・ショット・ライフル）、`10101/10102…` 模板块、
#     旧轮转抓取错列。它们有真名但**无真值来源**（sidecar 781 个武器名里 0 命中），
#     其中 6 把 POWER 被写成 2/6/9/11/12/13 ⇒ 会把真库 TTK 哨踩响。
#   · ★修正（2026-10-04 晚）：此前「短号不是合法号的另一种写法」**是错的**——
#     漏了运行时唯一那条规则 `store.FormatItemKey`（`0<n<1e8 ⇒ %08d`）。
#     `02840151` 与 `2840151` 是同一把武器，详见下面 `norm_key()`。
KEEP = os.path.join(HERE, 'names', '可达武器号域.csv')


def norm_key(k):
    """物品号规范形 —— 与运行时 `store.FormatItemKey` / `purge_unreachable_weapon_keys.norm_key`
    逐字一致：`0 < n < 1e8` 一律 `%08d`。

    ★这里**必须**归一：`可达武器号域.csv` 里同时有 `02840151`(规范形，来自被删的行)
    与 `2840151`(源形，来自 `game.ms_rokaku.eqweapon_itemid`)。只比裸串就会把同
    一把武器的另一种写法判成「越域」——2026-10-04 那次误删（845 键）就是这个错。
    """
    k = str(k).strip()
    return k.zfill(8) if k.isdigit() and len(k) <= 8 else k


_W = {norm_key(r[1]) for r in S if r[1].strip().isdigit()}
_W |= {norm_key(r[0].strip().lstrip('\ufeff')) for r in
       rd(os.path.join(GAME, 'unpackdat', 'settings', 'weapon_wrestle.csv'))
       if r and r[0].strip().lstrip('\ufeff').isdigit()}
_src = 'sidecar 9 位 + 客户端近战 8 号（未找到允许键域文件，回退）'
if os.path.exists(KEEP):
    _W |= {norm_key(r[0]) for r in rd(KEEP) if r and r[0].strip().isdigit()}
    _src = os.path.relpath(KEEP, ROOT)

# ── ★★口径哨（2026-10-05 立）：#36 **八族整族重写** ──────────────────────────
# 病：本脚本对 sidecar **产不出行**的键（维基那一格留白 / 写 `-`）只按键替换、不动旧行，
# 于是历史上另一条管线灌进来的白字刻度/错列残渣**永远留在表里**。真库实测（真武器号）：
#   RAPIDDELAY 524 行越域（白字 1263..1491 / 错列 200..5000）—— 已经是 2 族时修的；
#   STABILITY  159 行越域（面板刻度 350..27500，真值应 ≤ 2.3）
#   RELOAD     350 行越域（面板刻度 400..5000，真值应 ≤ 9.5）
#   LOCKON_CAM  15 行越域（面板刻度 740..4167，真值应 ≤ 100）
# 纪律：sidecar **有行**的键（= `S` 的全部键，含源列全空的），这 **8 族**一律**先整族清掉
# 再按 `SIDECAR_36`（含 `SIDECAR_36_FALLBACK`）重建**。sidecar **无行**的键（现役短号，
# 如 02711603；见 `_rollback/36_rapid_*_rows.csv`）不在清除范围内 ⇒ 不被本脚本抹掉。
# 族清单 = `#36` 的全部 8 个属性名（`weapon_battle_detail.csv` 里出现过的 attr 词表，
# 也就是本脚本唯一会写的 8 族）—— 多一族都不清，免得误伤别的管线写的属性。
_S_KEYS = {norm_key(r[1]) for r in S if len(r) > 1 and r[1].strip()}
FAM36 = RAW.FAMILIES_36


def _purge_fam36(fields):
    """`#36` 的行字段 → 是否属于「sidecar 有行但产不出值」的八族残渣。"""
    return (len(fields) > 1 and fields[0].strip() in FAM36
            and norm_key(fields[1].strip()) in _S_KEYS)

print()
print('--- ★口径哨：#36/#37 的键必须落在允许键域（%d 个，出处 %s）内 ---' % (len(_W), _src))
_bad36 = sorted({r[1].strip() for r in rd(T36)
                 if not r[0].startswith('#') and len(r) > 1
                 and r[1].strip().isdigit() and norm_key(r[1]) not in _W})
_bad37 = sorted({r[0].strip() for r in rd(T37)
                 if not r[0].startswith('#') and r[0].strip().isdigit()
                 and norm_key(r[0]) not in _W})
for _tag, _bad in (('#36', _bad36), ('#37', _bad37)):
    print('  %s 越域键 %d 个 %s' % (_tag, len(_bad), ('例:' + str(_bad[:6])) if _bad else '✓'))
if _bad36 or _bad37:
    print('  ✗ 口径哨响了：这些键的武器链不可达（msma_weapon_set col2 / 客户端 #武器ID 都不含），')
    print('    跑 `python datatables/purge_unreachable_weapon_keys.py --apply` 收敛后再来。')
    if '--apply' in sys.argv:
        raise SystemExit('拒绝写入： #36/#37 里有越域键')

# ── 生成三表行
r78, r36, r37 = [], [], []
neg = 0
basefill = 0
for r in S:
    if len(r) < 22:
        continue
    wid, cls, mode, name = r[1].strip(), r[3].strip(), r[8].strip(), r[5].strip()
    power = r[10].strip()
    locked = r[16].strip()
    c52 = C28_2_C52.get(cls, 'MACHINEGUN')
    # 发射模式
    traj = dict(MODE2TRAJ).get(mode, 'NONE')
    if c52 == 'WRESTLE':
        traj = 'WRESTLE'
    elif c52 == 'SHIELD':
        traj = 'SHIELD'
    grip = GRIP_BY_CAT.get(c52, 'ONEHAND')
    spread = 'SCATTERS' if '散射' in mode else 'NORMAL'
    if c52 == 'SNIPE':
        lock = 'SCOPE'
    elif locked and locked not in ('0', ''):
        lock = 'LOCKON'
    else:
        lock = 'NONE'
    attr = 'BEAM' if re.search(r'ビーム|光束|beam|メガ|粒子|喷枪|手枪', name, re.I) else \
           ('BLAST' if c52 in ('MISSILE', 'BAZOOKA', 'HAND_THROW', 'TRENCH_MORTAR') else 'SOLID')

    r78.append('%s,,%s,,WEAPON,,,' % (wid, name))
    wrote_power = False
    for c, nm, _conv in N36:
        # ★列号**回退链**（唯一出处 `weapon_client_raw.SIDECAR_36_FALLBACK`）：主列取不出数字时
        #   依次试备用列。实测 RELOAD 的主列 col14「装填性能」与备用列 col15「装填时间」
        #   **严格互斥**（sidecar 1625 行：930/540/两者都有 0/都空 155），不回退就丢 540 个键。
        tv = None
        for cc in (c,) + tuple(RAW.SIDECAR_36_FALLBACK.get(nm, ())):
            tv = first_tier(r[cc] if len(r) > cc else '')   # ★两档值取第一档
            if tv:
                break
        if not tv:
            continue
        # ★面板 → 客户端原值（唯一换算表：`weapon_client_raw`）
        val, _extra = RAW.attr_value(nm, tv)
        r36.append('%s,%s,%s,' % (nm, wid, val))
        if nm == 'POWER':
            # ★正值入库（消费端对回复系取负，见 weapon_client_raw.py 文件头）
            wrote_power = True
        elif nm == RAW.COOLTIME_TWIN:
            # 连射速度与冷却时间同值（`sub_59A070` 两个子表；读侧目前只读 RAPIDDELAY）
            r36.append('COOLTIME,%s,%s,' % (wid, val))
    # wiki 没给「威力」⇒ 按类别基线补（本服占位口径，**面板值**），盾类不补
    if not wrote_power and c52 not in NO_POWER:
        r36.append('POWER,%s,%s,' % (wid, RAW.power_raw(BASE_POWER.get(c52, BASE_POWER_DEFAULT))))
        basefill += 1
    f37 = [''] * 33
    f37[0], f37[1], f37[2] = wid, '0', '1'
    # IDA v15 597F50/4A45A0/4A01C0: col14+1 is an animation layer.
    # Wiki ammunition does not establish a layer. Runtime ammo is col104/105;
    # apply it separately through explicit machine/weapon bindings.
    f37[14] = ''
    f37[13], f37[21], f37[29], f37[30], f37[31], f37[32] = grip, c52, spread, traj, lock, attr
    r37.append(','.join(f37) + ',')

print()
print('生成：#78 %d 行 / #36 %d 行 / #37 %d 行（POWER 基线补值 %d 条）' % (len(r78), len(r36), len(r37), basefill))
print('唯一武器ID %d' % len(set(r.split(',')[0] for r in r78)))
print('  例 #36:', r36[:4])
print('  例 #37:', r37[:2])

# ── ★口径哨：POWER 必须是「客户端原值」（面板/10），不是面板值 ──────────────
# 面板威力实测 100–75000 ⇒ 原值 10–7500。写成面板值（>10000）就是口径腐蚀，
# 会让 `panelPowerFromClientRaw` 再乘 10 ⇒ 全武器伤害 ×10（见文件头）。
_raw = [int(float(x.split(',')[2])) for x in r36 if x.startswith('POWER,')]
_over = [x for x in r36 if x.startswith('POWER,') and int(float(x.split(',')[2])) > 10000]
print('POWER 原值带：min=%d max=%d 中位=%d；超上限(>10000) %d 条'
      % (min(_raw), max(_raw), sorted(_raw)[len(_raw) // 2], len(_over)))
if _over:
    print('  ✗ 口径哨响了：', _over[:5])
    raise SystemExit('POWER 写成了面板值（应过 weapon_client_raw.power_raw）')

# ── ★口径哨：RAPIDDELAY 必须是「客户端原值」，且 COOLTIME 与之同值 ───────────
# 白字刻度（`480..1491`）/错列残渣（`200..5000`、负数）混进原值列 ⇒ 读侧
# `rapidDisplayFromClientRaw` 反算出的連射速度会离谱，T5 冷却要么不判要么误杀。
# 判据 = `weapon_client_raw.rapid_is_raw_domain`（域 0.05..2.01），与
# `fix_rapid_delay_units.py` 和 Go 侧 `battle_params.go` 三方同口径。
_rap, _cool = {}, {}
for x in r36:
    f = x.split(',')
    if f[0] == 'RAPIDDELAY':
        _rap[f[1]] = f[2]
    elif f[0] == 'COOLTIME':
        _cool[f[1]] = f[2]
_bad = sorted(k for k, v in _rap.items() if not RAW.rapid_is_raw_domain(v))
_mism = sorted(k for k in _rap if k in _cool and _cool[k] != _rap[k])
_disp = sorted(RAW.rapid_display(v) for v in _rap.values() if RAW.rapid_display(v))
print('RAPIDDELAY 原值 %d 键：域内 %d / 域外 %d；白字带 %s；COOLTIME 同值偏差 %d'
      % (len(_rap), len(_rap) - len(_bad), len(_bad),
         ('%d..%d' % (_disp[0], _disp[-1])) if _disp else 'n/a', len(_mism)))
if _bad or _mism:
    print('  ✗ 口径哨响了：域外', [(k, _rap[k]) for k in _bad[:5]],
          '同值偏差', [(k, _rap[k], _cool[k]) for k in _mism[:5]])
    raise SystemExit('RAPIDDELAY 越出客户端原值域 / COOLTIME 与 RAPIDDELAY 不同值')

# ── ★口径哨：STABILITY / RELOAD / LOCKON_CAM 必须是「客户端原值」 ─────────────
# 这三族的旧残渣是**面板白字直写**（集弹 350..27500 / 装填 400..5000 / 锁定 740..4167），
# 与真值簇（≤2.3 / ≤9.5 / ≤100）**整整隔两个数量级**——域定义与实测两簇见
# `weapon_client_raw.RAW_DOMAIN` 上方的注释。域外值不可能由 `*_raw()` 产出 ⇒ 一律拒写。
# （RAPIDDELAY/COOLTIME 由上面那条哨覆盖，这里跳过以免重复报数。）
print()
print('集弹/装填/锁定 原值域哨：')
for _nm in ('STABILITY', 'RELOAD', 'LOCKON_CAM'):
    _vs = [x for x in r36 if x.startswith(_nm + ',')]
    _bad = sorted(x for x in _vs if not RAW.is_raw_domain(_nm, x.split(',')[2]))
    _f = sorted(float(x.split(',')[2]) for x in _vs)
    print('  %-11s %4d 条  域内 %4d / 域外 %3d  min=%.6f max=%.6f  域=[%s, %s]'
          % (_nm, len(_vs), len(_vs) - len(_bad), len(_bad),
             _f[0] if _f else 0.0, _f[-1] if _f else 0.0,
             RAW.RAW_DOMAIN[_nm][0], RAW.RAW_DOMAIN[_nm][1]))
    if _bad:
        print('    ✗ 域外例（应为面板值直写残渣）:', _bad[:5])
        raise SystemExit('%s 越出客户端原值域（应过 weapon_client_raw.%s）'
                         % (_nm, {'STABILITY': 'stability_raw', 'RELOAD': 'reload_raw',
                                  'LOCKON_CAM': 'lockon_raw'}[_nm]))


def merge(path, newrows, keycols=1, header=None, purge=None):
    """按键替换合并；`purge=(标签, 判定)` 时先整族清掉命中的旧行（= 重写语义）。"""
    old = open(path, encoding='utf-8', errors='replace', newline='').read().replace('\r\n', '\n').split('\n') \
        if os.path.exists(path) else []
    head = [l for l in old if l.strip().startswith('#')]
    body = [l for l in old if l.strip() and not l.strip().startswith('#')]
    n_purge = 0
    if purge is not None:
        tag, pred = purge
        kept = [l for l in body if not pred(l.split(','))]
        n_purge = len(body) - len(kept)
        body = kept
        print('   净化 %-48s -%-5d 行（%s）' % (os.path.relpath(path, ROOT), n_purge, tag))
    key = lambda l: ','.join(l.split(',')[:keycols]).strip()
    nk = set(key(r) for r in newrows)
    body = [x for x in body if key(x) not in nk] + list(newrows)
    if header:
        head = header
    if os.path.exists(path) and not os.path.exists(path + '.bak'):
        shutil.copy2(path, path + '.bak')
    open(path, 'wb').write(('\r\n'.join(head + body) + '\r\n').encode('utf-8'))
    b = open(path, 'rb').read()
    ok = (not b.startswith(b'\xef\xbb\xbf')) and (b.replace(b'\r\n', b'').find(b'\n') < 0)
    print('   写 %-48s +%-5d 行 方言%s' % (os.path.relpath(path, ROOT), len(newrows), 'OK' if ok else 'FAIL'))
    return ok


if '--apply' in sys.argv:
    print()
    print('落盘：')
    merge(T78, r78)
    merge(T36, r36, 2, purge=('八族无源残渣（sidecar 有行但产不出值）', _purge_fam36))
    merge(T37, r37)
    print('★ 完成')
