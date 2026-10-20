# -*- coding: utf-8 -*-
"""candidates.py —— 给"未配代号"列出名册候选 Top-N（供人工挑选，避免瞎猜）。

评分 = 双向 LCS（代号骨架 vs 日文名骨架），并做**别名修正**（ジム→GM、ガンダム→GND、ザク→ZK…），
因为这些英文缩写才是代号的真实来源。已配的練度ID会被排除（每台只归一个目录）。
用法：python datatables/candidates.py 0101 [N]
"""
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
S = os.path.join(ROOT, 'unpackdat', 'settings')

KANA = {}
for row, c in [('あいうえおぁぃぅぇぉ', ''), ('かきくけこがぎぐげご', 'k'), ('さしすせそざじずぜぞ', 's'),
               ('たちつてとっ', 't'), ('だぢづでど', 'd'), ('なにぬねのん', 'n'), ('はひふへほ', 'h'),
               ('ばびぶべぼ', 'b'), ('ぱぴぷぺぽ', 'p'), ('まみむめも', 'm'), ('やゆよゃゅょ', 'y'),
               ('らりるれろ', 'r'), ('わを', 'w')]:
    for k in row:
        KANA[k] = c
KANA.update({'ふ': 'f', 'じ': 'j', 'し': 's', 'ち': 'c', 'つ': 't', 'ゔ': 'v', 'ー': '', '・': '', '　': ''})
# ★别名修正：这些部件名在代号里用英文缩写
ALIAS = [('じむ', 'GM'), ('がんだむ', 'GND'), ('ざく', 'ZK'), ('ぐふ', 'GF'), ('どむ', 'DM'),
         ('ずごっく', 'ZG'), ('げるぐぐ', 'GG'), ('ばう', 'BW'), ('ばずーか', 'BZK'),
         ('びーむ', 'BM'), ('きゃのん', 'CN'), ('すとらいく', 'STG'), ('ばすたー', 'BUSTER'),
         ('ふりーだむ', 'FRDGND'), ('ぷろヴィでんす', 'PVD'), ('じゃすてぃす', 'JST'),
         ('いーじす', 'EG'), ('でぃーあーる', 'DR'), ('ばく', 'BK')]


def kata(s):
    out = []
    for ch in s:
        o = ord(ch)
        if 0x30A1 <= o <= 0x30F6:
            ch = chr(o - 0x60)
        out.append(ch)
    return ''.join(out)


def skel(s):
    """日文名 → 骨架：先做别名替换（英文缩写），再逐字取辅音，数字保留"""
    t = kata(s)
    tag = ''
    for jp, ab in ALIAS:
        if jp in t and jp not in ('じむ',):        # 别名部件抽出来拼到前面（近似代号构词）
            t = t.replace(jp, '|' + ab + '|')
    out, i = [], 0
    for chunk in t.split('|'):
        if chunk[:1].isupper():
            out.append(chunk)
            continue
        for ch in chunk:
            if ch.isdigit():
                out.append(ch)
            elif ch in KANA:
                out.append(KANA[ch])
            elif ch.isascii() and ch.isalpha():
                out.append(ch.lower())
    return ''.join(out)


def squeeze(code):
    return ''.join(c for c in code.lower() if c not in 'aeiou -')


def lcs(a, b):
    dp = [0] * (len(b) + 1)
    for x in a:
        prev = 0
        for j, y in enumerate(b, 1):
            cur = dp[j]
            dp[j] = prev + 1 if x == y else max(dp[j], dp[j - 1])
            prev = cur
    return dp[len(b)]


def score(code, name):
    cs, ns = squeeze(code), skel(name)
    if not cs or not ns:
        return 0.0
    return 2.0 * lcs(cs, ns) / (len(cs) + len(ns))


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


flt = sys.argv[1] if len(sys.argv) > 1 else '0101'
N = int(sys.argv[2]) if len(sys.argv) > 2 else 3

roster = []
for f in rows(os.path.join(S, 'favms_ok_list.csv')):
    m = re.match(r'^(\d{7})', ''.join(f))
    if m and m.group(1) not in [r[0] for r in roster]:
        roster.append((m.group(1), f[1] if len(f) > 1 else ''))

done = set()
for f in rows(os.path.join(HERE, 'names', '模型号映射-合并.csv')):
    if len(f) > 1 and re.fullmatch(r'\d{9}', f[1] or ''):
        done.add(f[0])

un = []
for f in rows(os.path.join(HERE, 'names', 'chara模型代号.csv')):
    if len(f) < 5 or flt not in '%02d%02d' % (int(f[0]), int(f[1])):
        continue
    v = int(f[4])
    if (v // 10**8, (v // 10**6) % 100, (v // 100) % 10000) in [
            (int(g[1]) // 10**8, (int(g[1]) // 10**6) % 100, (int(g[1]) // 100) % 10000)
            for g in rows(os.path.join(HERE, 'names', '模型号映射-合并.csv')) if len(g) > 1 and g[1].isdigit()]:
        continue
    un.append((f[2], f[3], f[4]))

print('未配目录 %d 个（过滤 %s）；名册 %d 台' % (len(un), flt, len(roster)))
for c, code, val in un:
    cand = sorted(((score(code, n), rid, n) for rid, n in roster if rid not in done), reverse=True)[:N]
    print('%4s %-16s → %s' % (c, code,
                              ' ｜ '.join('%.2f %s %s' % (s, rid, n[:14]) for s, rid, n in cand)))
