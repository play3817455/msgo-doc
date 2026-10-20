# -*- coding: utf-8 -*-
"""probe_item_cats.py —— 反推 `item/<类号>/` 各类号是什么武器。

依据：近接系已知 = `item/01|02|08`（`settings/weapon_wrestle.csv` 的 8 个真ID全落在这三类）。
方法：对每个类号采样若干 `.vra`（明文），统计其 **mesh 名关键词**，按关键词归类：
    saber/blade/naginata/hammer/whip → 近接
    rifle/machinegun/gatling/beam_gun/vulcan → 射击(枪)
    cannon/bazooka/missile/launcher/rail/mortar/howitzer → 射击(炮)
    shield → 盾
    hand/grenade/throw → 投掷
输出：各类号的目录数 + 关键词样本 → 作为分配器的"类号 → 武器类型"表。
"""
import collections
import glob
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEM = os.path.join(ROOT, 'unpackdat', 'item')

KW = [
    ('近接', r'saber|blade|naginata|hammer|whip|sword|knife|axe'),
    ('枪',   r'rifle|machinegun|machine_gun|gatling|beamgun|vulcan|smg|shotgun|sniper|gun'),
    ('炮',   r'cannon|bazooka|baz|missile|launcher|rail|mortar|howitzer|pod'),
    ('盾',   r'shield'),
    ('投掷', r'grenade|throw|hand'),
    ('特效', r'fx|effect|beam_|_beam|muzzle|flash'),
]


def cls(name):
    l = name.lower()
    for k, p in KW:
        if re.search(p, l):
            return k
    return '?'


summ = {}
for cat in sorted(os.listdir(ITEM)):
    d = os.path.join(ITEM, cat)
    if not os.path.isdir(d):
        continue
    subs = [s for s in os.listdir(d) if os.path.isdir(os.path.join(d, s))]
    per = collections.Counter()
    samples = []
    nvra = 0
    for p in glob.glob(os.path.join(d, '*', 'attr', '*.vra'))[:200]:
        t = open(p, encoding='utf-8', errors='replace').read()
        names = re.findall(r'\(name string[^"]*"([^"]+)"', t)
        nvra += 1
        for n in names:
            core = re.sub(r'^[A-Z]{2,3}_\d+_\d+_\d+_?', '', n)      # 去掉 EM_01_0101_01_ 前缀
            c = cls(core)
            per[c] += 1
            if c != '?' and len(samples) < 5:
                samples.append(core[:26])
    top = per.most_common(3)
    summ[cat] = (len(subs), nvra, top, samples)
    print('item/%-3s 子目录 %4d  采样 vra %3d  关键词分布 %-30s 例 %s'
          % (cat, len(subs), nvra, dict(top), samples[:3]))

print()
print('★ 汇总（类号 → 主导类型）：')
for cat, (n, nvra, top, _) in sorted(summ.items()):
    dom = top[0][0] if top else '?'
    print('   item/%-3s  %4d 目录  →  %s' % (cat, n, dom))
