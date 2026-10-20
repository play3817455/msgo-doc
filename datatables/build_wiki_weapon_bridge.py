# -*- coding: utf-8 -*-
"""build_wiki_weapon_bridge.py —— 建「机体 ↔ wiki 武器页」桥 + 导出待核对清单。

★口径（2026-09-28 用户拍板）：
  底 = `机体名对照表.csv` 的 **col19 codex页面**（已知最高覆盖）；
  归一化后必须在 `wiki/wiki_ms_weapons.csv` 的页面集合里命中；
  已知错配与 col19/col28 冲突**自动标出**，导出清单供人工核对。

用法：
  python build_wiki_weapon_bridge.py           # 只报告 + 出清单
  python build_wiki_weapon_bridge.py --apply   # 另写入桥表
"""
import csv, os, re, sys, io, collections, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WIKI = os.path.join(HERE, 'wiki', 'wiki_ms_weapons.csv')
BRIDGE = os.path.join(HERE, 'names', '机体名对照表.csv')
OUT_BRIDGE = os.path.join(HERE, 'names', '机体-wiki武器页桥.csv')
OUT_CHECK = os.path.join(HERE, 'names', '武器分配待核对清单.csv')

# 已人工确认的错配（上一轮实测）
KNOWN_BAD = {
    '1423011': 'col19=钢坦克Ⅱ 自身正确；col28 串成吉姆加农(北美战线式样)',
    '1132141': 'col28 串成强袭嫣红',
    '1124231': 'col28 串成漆黑型强袭敢达(中国红限定式样)',
    '1167011': 'col28 串成 Z PLUS A1型(试验机配色型)',
    '1173161': 'col28 串成自由敢达 Ver.GCP',
    '1164022': 'col28 串成能天使敢达修复型Ⅱ',
    '1109011': 'col19 错：吉姆·斯特莱克 被配成 水陆两用型吉姆',
    '1101021': 'col19 错：吉姆（WD队规格） 被配成 吉姆狙击特装型(荣格机)',
}

SKIP = re.compile(r'模式|技能|必杀|burst', re.I)

# ★人工定案（2026-09-28）：以 **日文名** 为准修正 col19 自身错、或确认 wiki 无页
#   1164022  日文名=シャア専用ズゴック  → col19 的「力克大魔」是错的，真页=夏亚专用魔蟹
#   1109011  日文名=ジム・ストライカー   → wiki 无同名页（存目：col19=水陆两用型吉姆 为错配）
#   1101021  日文名=ジム(WD隊仕様)      → wiki 无同名页（存目：col19=吉姆狙击特装型 为错配）
#   1423011  日文名=ガンタンクⅡ        → col19 正确但 wiki 无该页
OVERRIDE = {
    '1164022': '高达OL夏亚专用魔蟹',
    '1109011': None,
    '1101021': None,
    '1423011': None,
}

# col19 与 col28 冲突、但已核对 **col19 是对的** ⇒ 只留告警，不降级为 SUSPECT
COL19_VERIFIED = {'1119081', '1132141', '1124231', '1167011', '1173161'}


def norm(s):
    s = (s or '').strip()
    for p in ('高达OL', '敢达OL', '机动战士敢达OL'):
        if s.startswith(p):
            s = s[len(p):]
    if s.endswith('机体数据'):
        s = s[:-4]
    s = re.sub(r'[（(](?:国|日|中国用)[）)]$', '', s)
    return s.strip()


def read_csv(p):
    return [r for r in csv.reader(open(p, encoding='utf-8-sig', errors='replace')) if r and any(x.strip() for x in r)]


# ---- wiki weapon pages
wr = read_csv(WIKI)
W: dict = collections.defaultdict(list)
for r in wr:
    if r[0].startswith('#'):
        continue
    if len(r) > 3 and r[0].strip():
        W[r[0].strip()].append(r)
PAGES = set(W)
PN = {}
for p in PAGES:
    PN.setdefault(norm(p), p)
print('wiki 武器页 %d 个' % len(PAGES))

# ---- bridge table
BR = read_csv(BRIDGE)
H = BR[0]
rows = [r for r in BR[1:] if r and r[0].strip().isdigit()]
print('机体名对照表 %d 行' % len(rows))

out = []
stat = collections.Counter()
for r in rows:
    lid = r[0].strip()
    cn = r[15].strip() if len(r) > 15 else ''
    c19 = r[19].strip() if len(r) > 19 else ''
    c28 = r[28].strip() if len(r) > 28 else ''
    mode = r[18].strip() if len(r) > 18 else ''
    n19, n28 = norm(c19), norm(c28)

    page = ''
    src = ''
    fixed = lid in OVERRIDE
    if fixed:
        page = OVERRIDE[lid] or ''
        src = 'manual'
    elif n19 and PN.get(n19):
        page, src = PN[n19], 'col19'
    elif not n19 and PN.get(n28):
        # ★只在 col19 为空时才回退 col28 —— col19 有值但无页 = 宁可 UNRESOLVED，也不采信串行的 col28
        page, src = PN[n28], 'col28'
    nw = 0
    if page:
        rows_p = [x for x in W.get(page, []) if len(x) > 3 and x[3].strip() and not SKIP.search(x[3])]
        nw = len(rows_p)

    status = []
    if lid in KNOWN_BAD:
        status.append('KNOWN_BAD:' + KNOWN_BAD[lid])
    if n19 and n28 and n19 != n28:
        status.append('COL19!=COL28(col19=%s|col28=%s)' % (n19, n28))
    if not page:
        status.append('NO_PAGE')
    elif src == 'col28':
        status.append('VIA_COL28')
    if page and nw == 0:
        status.append('PAGE_NO_WEAPONS')

    if not page:
        verdict = 'UNRESOLVED'
    elif lid in COL19_VERIFIED or fixed:
        verdict = 'OK'
    elif any(s.startswith('NO_PAGE') or s.startswith('COL19!=') for s in status):
        verdict = 'SUSPECT'
    else:
        verdict = 'OK'
    stat[verdict] += 1
    out.append(dict(lid=lid, cn=cn, mode=mode, c19=n19, c28=n28, page=page, src=src, nw=nw,
                    verdict=verdict, status='; '.join(status)))

print()
print('判定分布:', dict(stat))
print('总可解析（page 非空）: %d / %d' % (sum(1 for x in out if x['page']), len(out)))
print('有武器数的: %d' % sum(1 for x in out if x['nw'] > 0))
print('武器数合计: %d' % sum(x['nw'] for x in out))
print()
print('--- OK 且武器数>0 的武器数分布 ---')
d = collections.Counter(x['nw'] for x in out if x['verdict'] == 'OK' and x['nw'] > 0)
print(dict(sorted(d.items())))
print()
print('--- SUSPECT 明细 ---')
for x in out:
    if x['verdict'] == 'SUSPECT':
        print('   %-9s %-24s page=%-30s nw=%-3d %s' % (x['lid'], x['cn'][:24], x['page'][:30], x['nw'], x['status']))
print()
print('--- UNRESOLVED（前 20）---')
n = 0
for x in out:
    if x['verdict'] == 'UNRESOLVED':
        n += 1
        if n <= 20:
            print('   %-9s %-24s c19=%-28s c28=%s' % (x['lid'], x['cn'][:24], x['c19'][:28], x['c28'][:28]))
print('   ... 共 %d' % n)

if '--apply' in sys.argv:
    with open(OUT_BRIDGE, 'wb') as f:
        L = ['#練度ID,官方中文名,匹配方式,codex页面,col28页面,采用页面,来源,武器数,判定,备注,']
        for x in out:
            L.append(','.join([x['lid'], x['cn'].replace(',', '・'), x['mode'], x['c19'].replace(',', '・'),
                               x['c28'].replace(',', '・'), x['page'].replace(',', '・'), x['src'],
                               str(x['nw']), x['verdict'], x['status'].replace(',', '；')]) + ',')
        f.write(('\r\n'.join(L) + '\r\n').encode('utf-8'))
    print()
    print('已写 %s' % OUT_BRIDGE)
