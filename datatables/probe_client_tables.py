# -*- coding: utf-8 -*-
"""probe_client_tables.py —— 摸清 unpackdat/settings 下所有 msma_* / favms_* 表的结构，
找"練度ID ↔ モデルID"能直接 join 的那几张。

判定：行里同时出现 7 位(練度ID) 与 9/13 位(モデルID) 的，就是天然桥表。
"""
import glob
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT, 'unpackdat', 'settings')


def read(p):
    b = open(p, 'rb').read()
    for enc in ('utf-8-sig', 'cp932', 'utf-8', 'latin1'):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode('latin1')


for p in sorted(glob.glob(os.path.join(S, '*'))) :
    n = os.path.basename(p)
    if not n.lower().endswith('.csv'):
        continue
    if not re.search(r'msma|favms|weapon|model|mesh|visual|ui_custom', n, re.I):
        continue
    t = read(p)
    L = [x for x in t.replace('\r\n', '\n').split('\n') if x.strip()]
    data = [x for x in L if not x.lstrip().startswith('#')]
    # 统计每行里 7 位 / 9 位 / 13 位 数字
    c7 = c9 = c13 = 0
    for x in data:
        for f in x.split(','):
            v = f.strip()
            if re.fullmatch(r'\d{7}', v):
                c7 += 1
            elif re.fullmatch(r'\d{9}', v):
                c9 += 1
            elif re.fullmatch(r'\d{13}', v):
                c13 += 1
    flag = '★桥表' if (c7 and (c9 or c13)) else ''
    print('%-42s 行%-5d 数据%-5d  7位=%-5d 9位=%-5d 13位=%-4d %s'
          % (n, len(L), len(data), c7, c9, c13, flag))
    if flag:
        for x in data[:3]:
            print('        ', x[:150])
