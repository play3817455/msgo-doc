# -*- coding: utf-8 -*-
"""probe_code_evidence.py —— 列"尚未配对的目录"的**资源侧证据**，供人工认代号。

每个未配目录输出一行：
  A/B/C  内部代号  槽数(来自 motionlist.csv 的 21[x]yy 组数)  武器挂载件网格名(attr/*.vra)

★用途：pair_codes2.py 扩 KEY 前，先看这份证据 —— 
  槽数 = 该机体武器数 ⇒ 可与 wiki 的「同机体武器数」交叉校验（`names/机体总表.csv` 第 36 列）；
  网格名（Saber/Shield/Rifle/Bazooka…）可校验武器类型。

用法：
  python datatables/probe_code_evidence.py            # 全部未配目录（A=01）
  python datatables/probe_code_evidence.py 0109       # 只看某系列
  python datatables/probe_code_evidence.py --all      # 含已配目录
"""
import glob
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CH = os.path.join(ROOT, 'unpackdat', 'chara')


def read(p):
    b = open(p, 'rb').read()
    for enc in ('utf-8-sig', 'cp932', 'utf-8', 'latin1'):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode('latin1')


def rows(p):
    return [[f.strip() for f in l.rstrip(',').split(',')]
            for l in read(p).replace('\r\n', '\n').split('\n')
            if l.strip() and not l.lstrip().startswith('#')]


def used_dirs():
    """已配目录（人工 > 补充 > 名字join 三处全算）"""
    used = set()
    for fn in ('模型号映射-合并.csv', '模型号映射-补充.csv', '模型号映射-人工.csv'):
        p = os.path.join(HERE, 'names', fn)
        if not os.path.exists(p):
            continue
        for f in rows(p):
            if len(f) > 1 and re.fullmatch(r'\d{7}', f[0] or '') and re.fullmatch(r'\d{9}', f[1] or ''):
                v = int(f[1])
                used.add((v // 10**8, (v // 10**6) % 100, (v // 100) % 10000))
    return used


def slots(d):
    ml = os.path.join(d, 'motionlist.csv')
    if not os.path.exists(ml):
        return -1
    ids = [int(x.split(',')[0]) for x in read(ml).replace('\r\n', '\n').split('\n')
           if x.strip() and x.split(',')[0].strip().isdigit()]
    return len(set((i // 100) % 10 for i in ids if 21000 <= i < 22000))


def meshes(d):
    out = []
    for p in sorted(glob.glob(os.path.join(d, 'attr', '*.vra'))):
        for n in re.findall(r'\(name string[^"]*"([^"]+)"', read(p)):
            if re.match(r'^(Hand_|MS_decal|MSM_)', n, re.I):
                continue
            out.append(n)
    return sorted(set(out))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    show_all = '--all' in sys.argv
    flt = args[0] if args else None
    used = used_dirs()
    print('# 已配目录 %d 个（人工+补充+名字join）' % len(used))
    n = 0
    for f in rows(os.path.join(HERE, 'names', 'chara模型代号.csv')):
        if len(f) < 5 or not f[3]:
            continue
        try:
            a, b, c = int(f[0]), int(f[1]), int(f[2])
        except ValueError:
            continue
        key = '%02d%02d' % (a, b)
        if flt and flt not in key:
            continue
        if not show_all and (a, b, c) in used:
            continue
        d = os.path.join(CH, '%02d' % a, '%02d' % b, '%04d' % c)
        ns = slots(d)
        ms = meshes(d)
        n += 1
        print('chara/%02d/%02d/%04d  %-22s 槽=%-3s %s'
              % (a, b, c, f[3], ns if ns >= 0 else '?', ' '.join(ms[:9])))
    print('# 计 %d 行' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
