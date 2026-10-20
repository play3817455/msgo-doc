# -*- coding: utf-8 -*-
"""bridge_probe.py —— 量化"wiki 武器 ↔ 真实武器ID"的桥。

三问：
 ① 资源池里到底有多少**不同的武器外观**（= 去重后的 item/<类>/<号>/ 目录数）？按大类分布如何？
 ② wiki 6404 行武器：射击模式分布、每台机体几把武器？
 ③ 桥表能把多少 wiki 机体页对到練度ID（= 对到 #1 的行键）？
"""
import collections
import csv
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    # ① 资源池
    L = [l.rstrip(',').split(',') for l in
         open(os.path.join(HERE, 'names', '物品ID全集.csv'), encoding='utf-8').read().splitlines()
         if l.strip() and not l.startswith('#')]
    ic = [x for x in L if len(x) > 3 and x[3] and int(x[3]) > 0]
    dirs = collections.Counter(x[2] for x in ic)          # 资源目录 → 出现次数（= 多少 ID 指向它）
    bycat = collections.Counter(d.split('/')[1] for d in dirs)
    print('① 可信物品ID %d 个（有图标引用）⇒ 去重后**资源目录 %d 个**（= 不同武器外观数）' % (len(ic), len(dirs)))
    print('   按大类目录分布:', dict(sorted(bycat.items(), key=lambda x: -x[1])))
    print('   同一目录被多个ID指向的例子:')
    for d, n in dirs.most_common(6):
        ids = [x[0] for x in ic if x[2] == d][:4]
        print('      %-16s %d 个ID  %s' % (d, n, ids))

    # ② wiki 武器（★按列位置访问，避免中文列名编码问题）
    #    0页面 1机体序号 2数据格式 3武器名 4重量 5弹数 6射击模式 7倒地值 8威力 9集弹性能
    #    10连射速度 11射程距离 12装填性能 13装填时间 14锁定 15红锁距离 16诱导距离 …
    p = os.path.join(HERE, 'wiki', 'wiki_ms_weapons.csv')
    t = [l for l in open(p, encoding='utf-8-sig', errors='replace').read().splitlines()
         if l.strip() and not l.startswith('#')]
    r = [row for row in csv.reader(t) if len(row) > 11]
    print()
    print('② wiki 武器 %d 行 / 机体页 %d' % (len(r), len(set(row[0] for row in r))))
    print('   射击模式分布:', collections.Counter(row[6] for row in r).most_common(12))
    c = collections.Counter(row[0] for row in r)
    v = sorted(c.values())
    print('   每机体武器数: 最多 %d / 中位 %d / 合计 %d' % (max(v), v[len(v) // 2], sum(v)))
    print('   样例(武器最多的3台):', c.most_common(3))
    print('   武器名样例:', [row[3] for row in r[:5]])

    # ③ 桥：wiki页面 → 練度ID（★列位 = 28，见 表头：…27 mcost, 28 wiki页面, 29 wiki装甲…）
    br = {}
    for l in open(os.path.join(HERE, 'names', '机体名对照表.csv'), encoding='utf-8').read().splitlines():
        if not l.strip() or l.startswith('#'):
            continue
        f = l.rstrip(',').split(',')
        if len(f) > 28 and f[28].strip():
            br.setdefault(f[28].strip(), f[0])
    hit = [p2 for p2 in c if p2 in br]
    print()
    print('③ 桥表(机体名对照表) wiki页面→練度ID %d 条' % len(br))
    print('   wiki 覆盖机体 %d ⇒ 命中 %d (%.0f%%)' % (len(c), len(hit), 100.0 * len(hit) / max(1, len(c))))
    print('   样例:', [(x, br[x], c[x]) for x in hit[:6]])
    miss = [x for x in c if x not in br]
    print('   未命中 %d 台，样例:' % len(miss), miss[:5])

    # ④ 供需：外观（全部 item 资源目录）vs wiki 武器（去重后）
    import glob
    alldirs = set()
    for q in glob.glob(os.path.join(ROOT, 'unpackdat', 'item', '*', '*')):
        if os.path.isdir(q):
            p2 = os.path.relpath(q, os.path.join(ROOT, 'unpackdat')).replace('\\', '/')
            alldirs.add(p2)
    uniq_names = set(row[3] for row in r if row[3])
    print()
    print('④ 需求 vs 供给：')
    print('   需求 = wiki 武器 %d 行；**去重武器名 %d 个**（每台机体 %d~%d 把）'
          % (len(r), len(uniq_names), min(v), max(v)))
    print('   供给 = **全部 item 资源目录 %d 个**（含未在图标里出现的）' % len(alldirs))
    print('   ⇒ %s' % ('量级匹配 ✓ 可按"大类+顺序"分配真 ID' if len(alldirs) >= len(uniq_names) * 0.6
                       else '仍偏少 ⇒ 多把武器共用外观 ⚠️'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
