# -*- coding: utf-8 -*-
"""scan_vra_parts.py —— 从每台机体的 attr/*.vra（明文）里读出**挂载部件清单**，
按类别归类 ⇒ 这就是"这台机体有哪些武器/装备"的资源侧答案（★原版就写在资源里）。

用途：替代 msma_weapon_set 目前的"轮转占位"，把 机体↔武器 用真实资源对上。
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

CAT = [('格斗', r'saber|blade|sword|knife|axe|claw'),
       ('射击', r'cannon|gun|rifle|beam|bazooka|missile|launcher|rail|vulcan|machinegun'),
       ('盾',   r'shield'),
       ('背包', r'backpack|wing|booster|thruster|binder'),
       ('隐藏', r'^hide_')]
SKIP = re.compile(r'^(hand_|ms_decal|msm_|msz_|mst_|ms_|_?\d)', re.I)   # 通用件/本体
BODY = re.compile(r'^_[0-9]|_0[0-9]$')                                  # 形如 _2003_01_00 的本体分段


def cat(n):
    l = n.lower()
    for k, p in CAT:
        if re.search(p, l):
            return k
    return '其它'


hits = collections.defaultdict(list)
files = glob.glob(os.path.join(UD, '*', '*', '*', 'attr', '*.vra'))
print('扫描 %d 个 .vra' % len(files))
per = collections.Counter()
detail = []
for p in sorted(files):
    d = os.path.relpath(os.path.dirname(os.path.dirname(p)), UD).replace('\\', '/')
    t = open(p, encoding='utf-8', errors='replace').read()
    names = re.findall(r'\(name string[^"]*"([^"]+)"', t)
    parts = [n for n in names if not SKIP.match(n) and not BODY.search(n)]
    cs = collections.Counter(cat(n) for n in parts)
    for k in cs:
        per[k] += 1
    if parts:
        detail.append((d, dict(cs), sorted(set(parts))[:6]))
print('★ 有"可命名部件"的机体 %d 台 / 共 %d 台' % (len(detail), len(files)))
print('--- 各类别的出现台数 ---')
for k, v in per.most_common():
    print('   %-4s %4d 台' % (k, v))
print('--- 随机 14 台的样子 ---')
for d, cs, ex in detail[::max(1, len(detail) // 14)][:14]:
    print('   %-14s %-38s %s' % (d, cs, ex))
