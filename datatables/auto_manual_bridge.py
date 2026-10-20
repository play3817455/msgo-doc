# -*- coding: utf-8 -*-
"""auto_manual_bridge.py —— 用"官方中文名 ↔ codex 名"把**未匹配的机体**自动补上，
结果写进 `names/手动对照.tsv`（`練度ID<TAB>codex名`，最高优先级人工覆盖位）。

背景：`build_name_bridge.py` 自动匹配只到 68%（阈值 0.62 + 跨语言），未匹配 224 台；
      而 codex 699 条里恰好还剩 ~219 条没被用 ⇒ 两边"剩下的互相配"。

归一化（中文名之间比较）：全角→半角、去空格/・/·/括号、去"(国)"/"中国用"、统一数字与常见译名。
一对一贪心：按相似度降序配对，已配过的两边都出局。
用法：python datatables/auto_manual_bridge.py [--apply]   # --apply 才写 tsv（先备份）
"""
import difflib
import io
import json
import os
import re
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BRIDGE = os.path.join(HERE, 'names', '机体名对照表.csv')
MANUAL = os.path.join(HERE, 'names', '手动对照.tsv')
CODEX = os.path.join(ROOT, 'unpackdat', 'codex', 'data', 'units.json')

ALIAS = [('敢达', '高达'), ('鋼彈', '高达'), ('钢弹', '高达'), ('鋼蛋', '高达'),
         ('吉姆', '吉姆'), ('大魔', '多姆'), ('德姆', '多姆'), ('兹哥克', 'ズゴック'),
         ('高克', 'ゴック'), ('扎古', 'ザク'), ('古夫', 'グフ')]


def norm(s):
    if not s:
        return ''
    out = []
    for ch in s:
        o = ord(ch)
        out.append(chr(o - 0xFEE0) if 0xFF01 <= o <= 0xFF5E else ch)
    t = ''.join(out)
    t = t.replace('中国用', '').replace('(国)', '').replace('（国）', '')
    for a, b in ALIAS:
        t = t.replace(a, b)
    for x in (' ', '\u3000', '・', '･', '·', '.', '-', '—', '_', '　', '(', ')', '（', '）', '[', ']', '【', '】'):
        t = t.replace(x, '')
    return t.lower()


def main():
    apply = '--apply' in sys.argv
    rows = [l.rstrip(',').split(',') for l in
            open(BRIDGE, encoding='utf-8').read().replace('\r\n', '\n').split('\n')
            if l.strip() and not l.lstrip().startswith('#')]
    units = json.load(open(CODEX, encoding='utf-8'))['units']
    used = set(r[2].strip() for r in rows if len(r) > 2 and r[2].strip())
    todo = [(r[0].strip(), r[1].strip(), r[15].strip() if len(r) > 15 else '')
            for r in rows if len(r) > 2 and not r[2].strip()]
    free = [u for u in units if u['name'] not in used]
    print('对照表 %d 行；未匹配 %d 台；codex 空闲条目 %d 个' % (len(rows), len(todo), len(free)))

    # 候选：官方中文名 / 日文名
    pairs = []
    for rid, jp, cn in todo:
        for cand in (cn, jp):
            if not cand:
                continue
            nc = norm(cand)
            for u in free:
                s = difflib.SequenceMatcher(None, nc, norm(u['name'])).ratio()
                if s >= float(os.environ.get('BRIDGE_MIN', '0.22')):
                    pairs.append((s, rid, u['name']))
    pairs.sort(reverse=True)
    got, used_rid, used_u = [], set(), set()
    for s, rid, name in pairs:
        if rid in used_rid or name in used_u:
            continue
        used_rid.add(rid)
        used_u.add(name)
        got.append((rid, name, s))
    print('★ 贪心补匹配 %d 台（相似度 ≥0.40）' % len(got))
    for rid, name, s in got[:14]:
        print('   %-9s → %-30s %.2f' % (rid, name, s))
    print('   相似度分布:', {k: sum(1 for _, _, s in got if a <= s < b)
                             for k, a, b in (('0.4-0.6', .4, .6), ('0.6-0.8', .6, .8), ('0.8+', .8, 2))})
    if not apply:
        print('（未写 tsv；加 --apply 生效）')
        return 0
    if not os.path.exists(MANUAL + '.bak'):
        shutil.copy2(MANUAL, MANUAL + '.bak')
    old = open(MANUAL, encoding='utf-8').read().splitlines() if os.path.exists(MANUAL) else []
    head = [l for l in old if l.startswith('#')]
    filled = [l for l in old if l.strip() and not l.startswith('#') and '\t' in l
              and len(l.split('\t')) >= 2 and l.split('\t')[1].strip()]
    add = ['%s\t%s\t# 自动补匹配 %.2f（★相似度低者建议人工核对）' % (r, n, s) for r, n, s in got]
    open(MANUAL, 'w', encoding='utf-8').write('\n'.join(head + filled + add) + '\n')
    print('★ 已写 %s（原有已填 %d，新增 %d）' % (MANUAL, len(filled), len(add)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
