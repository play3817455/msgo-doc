# -*- coding: utf-8 -*-
"""auto_codes.py —— 用"内部代号字母骨架 ↔ 日文名音译骨架"自动配对 練度ID。

原理：目录内部代号（如 `FRDGND`）是机体英文/音译名的辅音骨架；
      `フリーダムガンダム` 的假名辅音骨架 = f,r,d,m,g,n,d,m ⇒ LCS(`FRDGND`, 骨架)=6/6 ⇒ 命中。
先用 pair_codes.py 里已自检通过的 69 个代号**校准准确率**，再决定是否外推。

输出：names/模型号映射-自动.csv（含分数），低分单独列出供人工核。
用法：python datatables/auto_codes.py [--apply]
"""
import ast
import glob
import io
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
S = os.path.join(ROOT, 'unpackdat', 'settings')

# 假名 → 辅音（含 F/V/J 等特例）
KANA = {}
for row, c in [('あいうえおぁぃぅぇぉ', ''), ('かきくけこ', 'k'), ('がぎぐげご', 'g'),
               ('さしすせそ', 's'), ('ざじずぜぞ', 'z'), ('たちつてとっ', 't'),
               ('だぢづでど', 'd'), ('なにぬねのん', 'n'), ('はひふへほ', 'h'),
               ('ばびぶべぼ', 'b'), ('ぱぴぷぺぽ', 'p'), ('まみむめも', 'm'),
               ('やゆよゃゅょ', 'y'), ('らりるれろ', 'r'), ('わを', 'w')]:
    for k in row:
        KANA[k] = c
KANA['ふ'] = 'f'       # フリーダム = Freedom
KANA['じ'] = 'j'
KANA['し'] = 's'
KANA['ち'] = 'c'
KANA['つ'] = 't'
KANA['ゔ'] = 'v'
KANA['ー'] = ''
KANA['・'] = ''
KANA['　'] = ''
KANA[' '] = ''


def kata2skeleton(s):
    """假名 → 辅音骨架（含数字）；片假名先转平假名"""
    out = []
    for ch in s:
        o = ord(ch)
        if 0x30A1 <= o <= 0x30F6:          # 片假名 → 平假名
            ch = chr(o - 0x60)
        if ch.isdigit():
            out.append(ch)
            continue
        if ch in KANA:
            out.append(KANA[ch])
            continue
        if ch.isascii() and ch.isalpha():
            out.append(ch.lower())
    return ''.join(out)


def strip_vowels(code):
    return ''.join(c for c in code.lower() if c not in 'aeiou')


def lcs(a, b):
    dp = [0] * (len(b) + 1)
    for x in a:
        prev = 0
        for j, y in enumerate(b, 1):
            cur = dp[j]
            dp[j] = prev + 1 if x == y else max(dp[j], dp[j - 1])
            prev = cur
    return dp[len(b)]


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


def load_code2key():
    for node in ast.parse(open(os.path.join(HERE, 'pair_codes.py'), encoding='utf-8').read()).body:
        if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'CODE2KEY' for t in node.targets):
            return ast.literal_eval(node.value)
    return {}


def score_of(code, name):
    cs = strip_vowels(code)
    ns = kata2skeleton(name)
    if not cs or not ns:
        return 0.0
    return lcs(cs, ns) / len(cs)


def main():
    apply = '--apply' in sys.argv
    KEY = load_code2key()
    dirs = rows(os.path.join(HERE, 'names', 'chara模型代号.csv'))
    roster = [(f[0], f[1]) for f in rows(os.path.join(S, 'favms_ok_list.csv'))
              if len(f) >= 2 and len(f[0]) == 7 and f[0].isdigit()]
    print('目录 %d 条 ｜ 名册 %d 台 ｜ 人工字典 %d 代号' % (len(dirs), len(roster), len(KEY)))

    # ① 校准：字典里已有的代号，看自动算法能否选中同一台
    known = {}
    for f in rows(os.path.join(HERE, 'names', '模型号映射-人工.csv')):
        if len(f) > 5 and len(f[0]) == 7 and f[0].isdigit():
            known[f[4]] = (f[0], f[1])           # code → (練度ID, 名)
    ok = bad = 0
    for code, (rid, nm) in known.items():
        best = max(roster, key=lambda r: score_of(code, r[1]))
        if best[0] == rid:
            ok += 1
        else:
            bad += 1
            if bad <= 6:
                print('   ✗ %-10s 应为 %s(%s) 实得 %s(%s) 分 %.2f'
                      % (code, rid, nm, best[0], best[1], score_of(code, best[1])))
    print('★校准：%d/%d 命中（%.0f%%）' % (ok, ok + bad, 100.0 * ok / max(1, ok + bad)))

    # ② 外推：字典没有的代号
    out, low = [], []
    for f in dirs:
        if len(f) < 5 or not f[3]:
            continue
        code = f[3].split('/')[0]
        if code in KEY:
            continue
        best = max(roster, key=lambda r: score_of(code, r[1]))
        s = score_of(code, best[1])
        (out if s >= 0.8 else low).append((s, code, f[2], best[0], best[1], f[4]))

    out.sort(reverse=True)
    low.sort(reverse=True)
    print('外推：高分(≥0.80) %d 条 ｜ 低分 %d 条' % (len(out), len(low)))
    for s, code, c, rid, nm, val in out[:14]:
        print('   %.2f %-12s %-4s → %-9s %s' % (s, code, c, rid, nm))
    print('   ...低分样例:')
    for s, code, c, rid, nm, val in low[:10]:
        print('   %.2f %-12s %-4s → %-9s %s' % (s, code, c, rid, nm))

    lst = ['#練度ID,モデルID,机体名,代号,分数,来源,']
    for s, code, c, rid, nm, val in out:
        lst.append('%s,%s,%s,%s,%.2f,自动,' % (rid, val, nm.replace(',', '，'), code, s))
    open(os.path.join(HERE, 'names', '模型号映射-自动.csv'), 'wb').write(
        ('\r\n'.join(lst) + '\r\n').encode('utf-8'))
    print('写入 names/模型号映射-自动.csv（%d 行）' % (len(lst) - 1))
    return 0


if __name__ == '__main__':
    sys.exit(main())
