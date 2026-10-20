# -*- coding: utf-8 -*-
"""verify_model_values.py —— 校验刚写入的模型坐标能否解出**真实存在的 chara 目录**。

按 `sub_473390` 分支B 解码：类别=v//1e8、系列=(v//1e6)%100、叶=(v//100)%1e4、变体=v%100
目录 = chara/<类别:02d>/<系列:02d>/<叶:04d>/ ；再检查该目录与变体文件是否存在。
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, 'unpackdat', 'chara')
T4 = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'msma', 'msma_settings.csv')


def read(p):
    b = open(p, 'rb').read()
    for enc in ('utf-8-sig', 'cp932', 'utf-8', 'latin1'):
        try:
            return b.decode(enc)
        except Exception:
            pass
    return b.decode('latin1')


rows = [[f.strip() for f in l.rstrip(',').split(',')]
        for l in read(T4).replace('\r\n', '\n').split('\n')
        if l.strip() and not l.lstrip().startswith('#')]
have = [(f[0], f[1]) for f in rows if len(f) > 1 and re.fullmatch(r'\d{9}', f[1] or '')]
print('本次已填模型坐标 %d 台' % len(have))

exist_dir = exist_file = bad = 0
badlist = []
for rid, v in have:
    v = int(v)
    a, b, leaf, nn = v // 10**8, (v // 10**6) % 100, (v // 100) % 10000, v % 100
    d = os.path.join(CH, '%02d' % a, '%02d' % b, '%04d' % leaf)
    okd = os.path.isdir(d)
    okf = False
    if okd:
        md = os.path.join(d, 'model')
        if os.path.isdir(md):
            okf = any(re.search(r'_%02d\.dxg$' % nn, x) for x in os.listdir(md))
        okf = okf or bool(os.listdir(os.path.join(d, 'attr'))) if os.path.isdir(os.path.join(d, 'attr')) else okf
    exist_dir += okd
    exist_file += okf
    if not okd:
        bad += 1
        if len(badlist) < 12:
            badlist.append((rid, v, 'chara/%02d/%02d/%04d' % (a, b, leaf)))
print('★目录存在 %d / %d （%.0f%%）｜ 变体文件匹配 %d' % (exist_dir, len(have), 100.0 * exist_dir / max(1, len(have)), exist_file))
if badlist:
    print('不存在的样例：')
    for x in badlist:
        print('   ', x)
