# -*- coding: utf-8 -*-
"""probe_unit_weapons.py —— 从资源里读出"某机体有几把武器、各是什么"。

★方法（用户提示 + 实测假设）：
  动作 ID 形如 `21xyy`：`21` + **x(武器槽序号)** + `yy(动作序号)`
    ⇒ 同一 x 的一组动作 = **该机体的第 x 把武器** ⇒ **不同 x 的个数 = 武器数**
  而 `attr/*.vra`（明文）里的 mesh 名给出**武器外观部件**（`Saber_01`/`Cannon`/`Hide_*`…）
  模型数（`MSM_*_01/_02/_03`）= 形态数，也可作旁证。

用法：python datatables/probe_unit_weapons.py 01/01/0112 01/21/0112 ...
"""
import collections
import glob
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UD = os.path.join(ROOT, 'unpackdat', 'chara')


def probe(rel):
    d = os.path.join(UD, rel.replace('/', os.sep))
    if not os.path.isdir(d):
        print('(缺) %s' % rel)
        return
    print('================ chara/%s ================' % rel)
    # ① motionlist.csv：按 21xyy 的 x 分组
    ml = os.path.join(d, 'motionlist.csv')
    if os.path.exists(ml):
        ids = []
        for l in open(ml, encoding='utf-8', errors='replace'):
            f = l.strip().split(',')
            if f and f[0].isdigit():
                ids.append(int(f[0]))
        w = [i for i in ids if 21000 <= i < 22000]
        g = collections.defaultdict(list)
        for i in w:
            g[(i // 100) % 10].append(i)          # 21[x]yy 的 x
        print('  motionlist: 总动作 %d，其中 21xxx = %d 条' % (len(ids), len(w)))
        print('  ★按 21[x]yy 分组的武器槽: %d 组' % len(g))
        for k in sorted(g):
            v = sorted(g[k])
            print('     槽 %d: %d 个动作  %s%s' % (k, len(v), v[:12], '…' if len(v) > 12 else ''))
    # ② anim 目录里的 21xxx 文件（真实存在的）
    af = glob.glob(os.path.join(d, 'anim', 'MSA_*_21[0-9][0-9][0-9].mrb')) + \
        glob.glob(os.path.join(d, 'anim', 'MSA_*_21[0-9][0-9][0-9].MRB'))
    g2 = collections.defaultdict(list)
    for p in af:
        m = re.search(r'_(\d{5})\.mrb$', p, re.I)
        if m:
            g2[(int(m.group(1)) // 100) % 10].append(int(m.group(1)))
    print('  anim 实体文件: %d 个 21xxx ⇒ 槽 %s' % (len(af), {k: len(v) for k, v in sorted(g2.items())}))
    # ③ attr/*.vra 的 mesh 名（武器外观部件）
    for p in sorted(glob.glob(os.path.join(d, 'attr', '*.vra'))):
        t = open(p, encoding='utf-8', errors='replace').read()
        names = re.findall(r'\(name string[^"]*"([^"]+)"', t)
        body = [n for n in names if not re.match(r'^(Hand_|MS_decal|MSM_)', n, re.I)]
        print('  %-26s mesh %2d：%s' % (os.path.basename(p), len(names), body if body else '(只有本体/手)'))
    # ④ 模型（形态）
    print('  模型: %s' % [os.path.basename(x) for x in sorted(glob.glob(os.path.join(d, 'model', '*.dxg')))])
    print()


if __name__ == '__main__':
    for a in (sys.argv[1:] or ['01/01/0112', '01/21/0112']):
        probe(a)
