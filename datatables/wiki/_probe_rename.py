# -*- coding: utf-8 -*-
"""改名审计：旧 CSV 的每个「丢失行」是否只是**名字规范化**后的同一个武器（还是真丢了）。

归一化：去掉所有空白/不可见字符、去 `[[文件:…]]` 图片、去全角/半角差异、去标点。
输出：真丢（无对应新名）的行；以及「改名」的行（打印新旧名字对照样例）。
"""
import csv
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = __import__('os').path.dirname(__import__('os').path.abspath(__file__))


def load(p):
    with open(HERE + '/' + p, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def norm(s):
    s = s or ''
    s = re.sub(r'\[\[(?:文件|File):[^\]]*\]\]', '', s)
    s = re.sub(r'<[^>]*>', '', s)
    s = re.sub(r'(?:红锁距离|诱导距离|锁定距离)[:：]?\d+', '', s)
    s = re.sub(r'[\s\u00a0\u3000]+', '', s)
    s = s.replace('（', '(').replace('）', ')').replace('，', ',')
    return s


old, new = load('wiki_ms_weapons.csv.bak_pre_rowspan'), load('wiki_ms_weapons.csv')
newmap = {}
for r in new:
    newmap.setdefault((r['#页面'], norm(r['武器名'])), []).append(r['武器名'])
# 真丢 = 归一化后仍无对应新名的旧行
realdel = [r for r in old if (r['#页面'], norm(r['武器名'])) not in newmap]
JUNK = re.compile(r"^\(共振\)$|^時間$|^2倍/4倍$|^TYPE-B$|^\|$|^[\d.,\s()/\-]+$")
junk = [r for r in realdel if JUNK.match(r['武器名'] or '')]
real = [r for r in realdel if not JUNK.match(r['武器名'] or '')]
print('旧行 %d 新行 %d；归一化后**真丢** %d 行 = 垃圾 %d + 需人工看 %d'
      % (len(old), len(new), len(realdel), len(junk), len(real)))
for r in real:
    print('   需看 %-40s %r' % (r['#页面'][:40], r['武器名']))
