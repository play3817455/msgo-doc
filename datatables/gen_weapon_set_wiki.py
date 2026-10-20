# -*- coding: utf-8 -*-
"""gen_weapon_set_wiki.py —— 用「真实 sub4 资源目录」造机体武器组（T3 落地）。

★口径（2026-09-28 用户拍板）：
  · 桥 = `names/机体-wiki武器页桥.csv`（col19 codex页面为底，仅 OK 档参与）
  · 武器ID = 该机体的**真实 sub4 资源目录**（保证每把都能落到 mesh/图）
        weaponID = '2' + 練度ID[1:5] + sub4      （sub4 ∈ item/02 且 sub4[0] == 練度ID[5]）
  · wiki 武器名/数值按序配给这些 ID
  · 未解析机体 **一台不留**（宁可零武器也不放假数据）

用法：
  python gen_weapon_set_wiki.py                 # 报告（不写盘）
  python gen_weapon_set_wiki.py --apply         # 写 msma_weapon_set.csv（自动备份）
  python gen_weapon_set_wiki.py --slots 0       # 0=每机体写全部真实武器；默认 3（客户端硬上限）
"""
import csv, os, re, sys, io, collections, shutil, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, '.codebuddy'))
import fpmf_scan as F

GAME = r"f:\9ymsgo\9you\机动战士敢达Online\GundamOnline"
BRIDGE = os.path.join(HERE, 'names', '机体-wiki武器页桥.csv')
WIKI = os.path.join(HERE, 'wiki', 'wiki_ms_weapons.csv')
SETTINGS = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_settings.csv')
OUT = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_weapon_set.csv')

SKIP = re.compile(r'模式|技能|必杀|時間|时间|burst', re.I)
SLOTS = 3
if '--slots' in sys.argv:
    SLOTS = int(sys.argv[sys.argv.index('--slots') + 1])

# ---- 武器类别（枚举 sub_585FD0 28 值，见 reverse-login-chain/formats/枚举表.md）
#      未知名称客户端读作 0 = MACHINEGUN，故兜底也取 MACHINEGUN
CLS = [
    ('SHIELD', r'シールド|盾|shield'),
    ('WRESTLE', r'サーベル|セイバー|ナギナタ|ブレイド|ソード|剣|軍刀|军刀|剑|剑刃|薙刀|鞭|锤|ハンマー|saber|blade|クロー'),
    ('REPAIR', r'リペア|回復|修理|修复|補給|补给'),
    ('RADARPOD', r'レーダー|雷达'),
    ('CAMERAGUN', r'カメラ|撮影|摄影'),
    ('LANDMINE', r'機雷|地雷'),
    ('HAND_THROW', r'グレネード|手榴弾|手雷|破片|閃光|闪光|投擲|投掷|炸弾|爆雷'),
    ('SHOTGUN', r'ショットガン|散弾|散弹|霰弹|shotgun'),
    ('BEAM_SNIPE', r'狙撃用ビーム|ビーム狙撃|光束狙击'),
    ('SNIPER_RIFLE', r'スナイパー|狙撃|狙击|sniper'),
    ('BEAM_SPRAYGUN', r'スプレー|拡散ビーム|光束喷枪|光束喷涂|喷枪|スプレーガン'),
    ('BEAM_RIFLE', r'ビームライフル|ビーム・ライフル|ビームガン|メガ粒子砲|メガ|米加|光束步枪|光束枪|光束手枪|手枪|步枪|ライフル|ピストル'),
    ('SUBMACHINEGUN', r'冲锋枪|短機関|サブマシンガン'),
    ('MACHINEGUN', r'マシンガン|機関砲|ガトリング|バルカン|机枪|机关炮|加特林|火神炮'),
    ('CHARGE_BAZOOKA', r'チャージバズーカ'),
    ('BAZOOKA', r'バズーカ|ロケット砲|火箭|バズ'),
    ('CHARGE_RIFLE', r'チャージライフル|チャージ'),
    ('MISSILE', r'ミサイル|导弹|誘導弾'),
    ('HOWITZER', r'キャノン|加農|加农|榴弾|榴弹|砲|炮'),
    ('TRENCH_MORTAR', r'迫撃|臼炮'),
    ('HAND_THROW', r'グレネード|手榴弾|手雷|破片|閃光|闪光|投擲|投掷|炸弾|爆雷'),
    ('LANDMINE', r'機雷|地雷'),
    ('HAND_THROW', r'グレネード|手榴弾|手雷|破片|閃光|闪光|投擲|投掷|炸弾|爆雷'),
    ('LANDMINE', r'機雷|地雷'),
    ('REPAIR', r'リペア|回復|修理|修复|补给'),
    ('RADARPOD', r'レーダー|雷达'),
    ('CAMERAGUN', r'カメラ|撮影|摄影'),
]
CC = [(n, re.compile(p, re.I)) for n, p in CLS]
UNMATCHED = collections.Counter()


def classify(name):
    for n, rx in CC:
        if rx.search(name):
            return n
    UNMATCHED[name] += 1
    return 'MACHINEGUN'


def read_csv(p):
    return [r for r in csv.reader(open(p, encoding='utf-8-sig', errors='replace')) if r and any(x.strip() for x in r)]


# ---- 真实 sub4 池（item/02）
_, files = F.load_hed(os.path.join(GAME, 'data', 'item.hed'))
SUB = collections.defaultdict(set)
for f in files:
    parts = (f['path'] or f['folder']).lstrip('.\\/').replace('\\', '/').split('/')
    if len(parts) >= 2 and parts[0] == '02' and re.fullmatch(r'\d{4}', parts[1]):
        SUB[parts[1][0]].add(parts[1])
print('item/02 真实 sub4 池：%d 个（按 練度ID[5] 分桶：%s）' % (sum(len(v) for v in SUB.values()), {k: len(v) for k, v in sorted(SUB.items())}))

# ---- wiki 武器
wr = read_csv(WIKI)
W = collections.defaultdict(list)
for r in wr:
    if not r[0].startswith('#') and r[0].strip() and len(r) > 3 and r[3].strip() and not SKIP.search(r[3]):
        W[r[0].strip()].append(r)
print('wiki 武器页 %d 个' % len(W))

# ★ wiki 抓取缺陷：部分页面**缺格** ⇒ 整行"串列"（重量列出现「三点／单发齐射」等模式词，
#   弹数位塞进倒地值、威力位塞进别的值）。实测 49 行／14 页受影响，且**缺格位置不固定**
#   （例：`杰刚(ECOAS式样·康洛伊机)` 同时缺 重量 + 射击模式）⇒ **无法用统一位移还原**。
#   按项目规则「不许把推断伪装成结论」：此类行**只保留武器名**，数值列一律置空（宁缺勿造）。
#   例：`高达OL敢达Mk-Ⅲ(强袭装备)(国)` 的「蓄力光束步枪」原行 4=蓄力单发 5=434 6=5000
#       ⇒ 实为 倒地值=434 / 威力=5000，若照读会得到 弹数=434 / 模式=5000（污染 #36/#37）。
ANOM = 0
NUM = re.compile(r'[0-9]+')
for _k, _lst in list(W.items()):
    _fx = []
    for _r in _lst:
        _w = _r[4].strip() if len(_r) > 4 else ''
        if _w and not NUM.fullmatch(_w):
            ANOM += 1
            _r = list(_r) + [''] * 20
            for _i in range(4, 20):
                _r[_i] = ''
        _fx.append(_r)
    W[_k] = _fx
print('wiki 串列行（重量列非数字）已清洗数值：%d 行（只留武器名，防造值）' % ANOM)

# ---- 桥
B = read_csv(BRIDGE)
bh = B[0]
rows_all = [r for r in B[1:] if r and r[0].strip().isdigit()]
seen = set()
rows = []
dups = 0
for r in rows_all:
    if r[0].strip() in seen:
        dups += 1
        continue
    seen.add(r[0].strip())
    rows.append(r)
print('桥 %d 行（去重 %d 行 → %d）' % (len(rows_all), dups, len(rows)))

# ---- 生成
# ---- 生成（只保留 msma_settings 里存在的机体）
SET_LIDS = set()
for r in csv.reader(open(SETTINGS, encoding='utf-8-sig', errors='replace')):
    if r and r[0].strip().isdigit():
        SET_LIDS.add(r[0].strip())
print('msma_settings 机体 %d 台' % len(SET_LIDS))

# ★★ 同 lid[1:6] 的机体 = **阵营对**（lid[6]：1=联邦 / 2=吉翁），但它们是**不同机体、不同武器**。
#    真实证据（weapon_visual_customize）：家族 14607 里 `214607001=Vガンダム`(lid 1146071)、`214607002=シャッコー`(lid 1146072)
#    ⇒ sub4 的"序号"是**逐机**递增的 ⇒ 必须给同家族各成员**切互不重叠的片**，否则 ID 撞车、名称/数值互相覆盖。
BYFAM = collections.defaultdict(list)
for l in sorted(SET_LIDS):
    BYFAM[l[1:6]].append(l)
SLICE = {}
for fam, mem in BYFAM.items():
    if len(mem) == 1:
        SLICE[mem[0]] = None
        continue
    for i, l in enumerate(mem):
        SLICE[l] = i          # 第 i 个成员取桶的第 i 片
print('同 lid[1:6] 需切片的多成员家族 %d 个（涉及 %d 台）'
      % (sum(1 for v in BYFAM.values() if len(v) > 1), sum(len(v) for v in BYFAM.values() if len(v) > 1)))

groups = []
stat = collections.Counter()
mismatch = []
for r in rows:
    lid = r[0].strip()
    verdict, page = r[8], r[5]
    if lid not in SET_LIDS:
        stat['SKIP_NOT_IN_SETTINGS'] += 1
        continue
    if verdict != 'OK' or not page:
        stat['SKIP_' + verdict] += 1
        continue
    weapons = W.get(page)
    if not weapons:
        stat['SKIP_PAGE_NO_WEAPONS'] += 1
        continue
    d5, pre = lid[5], lid[1:5]
    bucket = sorted(SUB.get(d5, ()))
    si = SLICE.get(lid)
    if si is not None and len(BYFAM[lid[1:6]]) > 1:
        k = max(1, len(bucket) // len(BYFAM[lid[1:6]]))
        bucket = bucket[si * k:(si + 1) * k]
    cand = bucket
    ids = ['2' + pre + s for s in cand]
    if not ids:
        stat['SKIP_NO_SUB4'] += 1
        continue
    n = min(len(ids), len(weapons)) if SLOTS == 0 else min(SLOTS, len(ids), len(weapons))
    used = ids[:n]
    # wiki 名按序配；数量不等则记账
    for i, wid in enumerate(used):
        nm = weapons[i][3].strip()
        groups.append(dict(lid=lid, page=page, wid=wid, cls=classify(nm),
                           slot='MAIN' if i == 0 else 'EX', name=nm, wiki=weapons[i]))
    stat['OK'] += 1
    if len(used) != len(weapons):
        mismatch.append((lid, page, len(weapons), len(used)))

print()
print('生成统计:', dict(stat))
print('参与机体 %d 台 / 武器行 %d 条' % (stat['OK'], len(groups)))
print('配名不齐（wiki武器数 != 采用ID数）: %d 台' % len(mismatch))
print('  例:', mismatch[:6])
print()
print('--- 抽样 ---')
print('%-9s %-22s %-11s %-5s %-14s %s' % ('練度ID', 'wiki武器名', '武器ID', '槽位', '类别', '页面'))
for g in groups[:18]:
    print('%-9s %-22s %-11s %-5s %-14s %s' % (g['lid'], g['name'][:22], g['wid'], g['slot'], g['cls'], g['page'][:26]))
print()
cc = collections.Counter(g['cls'] for g in groups)
print('类别分布:', dict(cc.most_common()))
print('未命中关键词而兜底 MACHINEGUN 的武器名 %d 种 / %d 次' % (len(UNMATCHED), sum(UNMATCHED.values())))
if UNMATCHED:
    print('   top:', UNMATCHED.most_common(12))

if '--apply' in sys.argv:
    bak = OUT + '.bak_wiki' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    if os.path.exists(OUT):
        shutil.copy2(OUT, bak)
        print('\n备份 -> %s' % os.path.basename(bak))
    L = ['#ID,,,,,,,,,,,,,,,,,,,,,,,,,,地区,']
    L.append('# ===== msma/msma_weapon_set.csv （表ID 1 / 下载序 1 / CMSMAWeaponSetTable / 读取函数 sub_587160）=====')
    L.append('# 生成：datatables/gen_weapon_set_wiki.py')
    L.append('#   col0 = 練度ID（武器组ID）')
    L.append('#   col2 = ★武器ID → ITEM 表★；**真人真值**：= "2" + 練度ID[1:5] + sub4')
    L.append('#          其中 sub4 ∈ unpackdat/item/02，且 sub4[0] == 練度ID[5] ⇒ **每个 ID 都能落到真实资源目录（能找图/找模型）**')
    L.append('#   col4 = MAIN / EX（sub_586450） ; col5 = 武器类别（sub_585FD0 28 值，由 wiki 武器名判定）')
    L.append('#   col6 = 1（启用；消费方 sub_581690 最多收 3 把/组 → 机体 +376/+380/+384）')
    L.append('#   col7..col27 = 留空 ; col28 = CHINA')
    L.append('# 来源：names/机体-wiki武器页桥.csv（col19 codex页面，仅 OK 档）+ wiki/wiki_ms_weapons.csv（武器名/数值）')
    L.append('# ⚠️ 唯一未证：**wiki 武器"第 i 把" ↔ 该机体第 i 个 sub4** 的先后对应（无任何来源可证，按序配）')
    L.append('#    但两侧都是真实值：ID 真实可落资源，名称真实来自 wiki。')
    L.append('# ⚠️ 未解析机体（SUSPECT/UNRESOLVED）**一律不生成**，保持空 ⇒ col38 命中率 = OK 档台数')
    L.append('# 每机体槽位数：%s' % ('全部真实武器' if SLOTS == 0 else str(SLOTS)))
    for g in groups:
        row = [''] * 30
        row[0] = g['lid']; row[2] = g['wid']; row[4] = g['slot']; row[5] = g['cls']; row[6] = '1'; row[28] = 'CHINA'
        L.append(','.join(row) + ',')
    open(OUT, 'wb').write(('\r\n'.join(L) + '\r\n').encode('utf-8'))
    print('已写 %s（%d 行）' % (OUT, len(L)))

# ★sidecar：武器分配明细（含 wiki 原始数值列），供 #78/#36/#37 落表复用，避免重复对齐逻辑
SIDE = os.path.join(HERE, 'names', '武器分配明细.csv')
with open(SIDE, 'wb') as f:
    L = ['#練度ID,武器ID,槽位,类别,页面,武器名,重量,弹数,射击模式,倒地值,威力,集弹性能,连射速度,射程距离,装填性能,装填时间,锁定,红锁距离,诱导距离,效果范围,锁定范围,持续时间,']
    for g in groups:
        r = g['wiki']
        vals = [(r[i] if len(r) > i else '').strip() for i in range(4, 20)]
        L.append(','.join([g['lid'], g['wid'], g['slot'], g['cls'], g['page'],
                           g['name'].replace(',', '・')] +
                          [v.replace(',', '/') for v in vals]) + ',')
    f.write(('\r\n'.join(L) + '\r\n').encode('utf-8'))
print('已写 %s（%d 行）' % (SIDE, len(L)))
