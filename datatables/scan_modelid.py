# -*- coding: utf-8 -*-
"""scan_modelid.py —— 扫描客户端表里写好的「モデルID（打包值）」+ 备注机体名，
自动生成 練度ID → 模型号 映射（★原版数据就在这些表里，不必手工配）。

モデルID 拆位（与客户端 sub_473390 同口径）：
    v = A*1e8 + B*1e6 + C*100 + NN     ⇒ chara/<A:02d>/<B:02d>/<C:04d>/
    例 101280501 → A=1 B=01 C=2805 NN=01
输出：names/模型号-客户端表.csv （練度ID, 日文名, 模型号, 来源表, 来源行）
"""
import collections
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UD = os.path.join(ROOT, 'unpackdat')
OUT = os.path.join(HERE, 'names', '模型号-客户端表.csv')
MASTER = os.path.join(HERE, 'names', '机体总表.csv')

RE9 = re.compile(r'^1\d{8}$')          # 9 位打包值
SKIP_DIR = ('chara', 'fx', 'map', 'sound', 'shader', 'battle', 'interface')


def dec(v):
    """v → (A,B,C,NN, 目录)"""
    a = v // 100000000
    b = (v // 1000000) % 100
    c = (v // 100) % 10000
    nn = v % 100
    return a, b, c, nn, 'chara/%02d/%02d/%04d' % (a, b, c)


def read_text(p):
    b = open(p, 'rb').read()
    for enc in ('utf-8', 'cp932', 'latin1'):
        try:
            return b.decode(enc), enc
        except Exception:
            pass
    return '', '?'


def main():
    named = {}          # 归一后机体名 → 名册
    for l in open(MASTER, encoding='utf-8').read().splitlines():
        if not l.strip() or l.startswith('#'):
            continue
        f = l.rstrip(',').split(',')
        if len(f) > 2:
            named[f[1]] = (f[0], f[1], f[2])
    def norm(s):
        o = []
        for ch in s:
            c = ord(ch)
            o.append(chr(c - 0xFEE0) if 0xFF01 <= c <= 0xFF5E else ch)
        t = ''.join(o).replace('（', '(').replace('）', ')')
        for x in (' ', '\u3000', '・', '･', '.', '·', '-', '　'):
            t = t.replace(x, '')
        return t.lower()
    nk = {}
    for k, v in named.items():
        nk.setdefault(norm(k), v)

    hits = collections.OrderedDict()     # 模型号 → [来源...]
    files = []
    for dp, dn, fn in os.walk(UD):
        rel = os.path.relpath(dp, UD).replace('\\', '/')
        if rel.split('/')[0] in SKIP_DIR:
            dn[:] = []
            continue
        for f in fn:
            if f.lower().endswith(('.csv', '.txt')):
                files.append(os.path.join(dp, f))
    print('扫描 %d 个表文件（%s 之外）' % (len(files), '/'.join(SKIP_DIR)))
    per_table = collections.Counter()
    for p in files:
        t, enc = read_text(p)
        name = os.path.relpath(p, UD).replace('\\', '/')
        for ln, line in enumerate(t.splitlines(), 1):
            if not line.strip() or line.startswith('#'):
                continue
            f = line.rstrip(',').split(',')
            ids = [int(x) for x in f if RE9.match(x.strip())]
            if not ids:
                continue
            # 备注列：以 # 开头 / 最后非空列 —— 用来对机体名
            note = ''
            for x in reversed(f):
                y = x.strip().lstrip('#').strip()
                if y and not RE9.match(y) and not y.isdigit():
                    note = y
                    break
            for v in set(ids):
                a, b, c, nn, d = dec(v)
                hits.setdefault(v, []).append((d, name, ln, note))
                per_table[name] += 1
    print('★ 扫到 %d 个不同的 モデルID' % len(hits))
    print('--- 贡献最多的表 ---')
    for n, k in per_table.most_common(15):
        print('   %5d 次  %s' % (k, n))

    # join 名册：优先用同行备注名的归一匹配；否则留空待配
    rows, matched = [], 0
    for v, srcs in sorted(hits.items()):
        d, name, ln, note = srcs[0]
        who = nk.get(norm(note)) if note else None
        if who:
            matched += 1
        rows.append((who[0] if who else '', who[1] if who else '', str(v), d, name, note, str(ln)))
    print('★ 其中 %d 个的同行备注直接对上了名册 ⇒ 可直接用' % matched)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    L = ['#練度ID,日文名,模型号,资源目录,来源表,同行备注,行号,',
         '# 由 datatables/scan_modelid.py 扫客户端表自动生成（モデルID = A*1e8+B*1e6+C*100+NN）,'] + \
        [','.join(r) + ',' for r in rows]
    open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('已写 %s（%d 行）' % (OUT, len(rows)))
    print('--- 示例（模型号 → 目录 → 备注）---')
    for r in rows[:12]:
        print('   %-10s %-22s %s' % (r[2], r[3], r[5]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
