# -*- coding: utf-8 -*-
"""导出 gow wiki 机体「基础值 / 强化上限」(panel[0]/panel[1]) 参考表。

★这些上限值 **当前不落 CFG**：
  · CHARA_PARAM / MSMA_BATTLE_DETAIL 只存基础值（gen_msma_machine.py 第一档）
  · MECHANIC_MSMA（develop/mechanic_msma.csv）是客户端强化上限查表，现网几乎空表
    （仅占位行 col0=0）；要把上限写进游戏需另批攻关 MECHANIC_MSMA 列语义。

产出：`datatables/names/ms_gow_caps.csv`
"""
import csv
import io
import json
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAIRS = os.path.join(ROOT, 'datatables', 'names', 'ms_wiki_pairs.json')
GOW = os.path.join(ROOT, 'gow_wiki', 'data', 'units.json')
OUT = os.path.join(ROOT, 'datatables', 'names', 'ms_gow_caps.csv')

FIELD_MAP = [
    ('アーマー', 'armor'), ('最高速度', 'speed'), ('ブースト容量', 'boost'),
    ('ブーストチャージ', 'boost_cd'), ('積載量', 'payload'),
    ('緊急帰投性能', 'return_val'), ('TIME', 'time'), ('COST', 'cost'), ('M-COST', 'mcost'),
]
NUM = re.compile(r'-?\d+')


def s1(v):
    if isinstance(v, list):
        return v[0] if v else ''
    return v or ''


def num(v):
    m = NUM.search(str(v).replace(',', ''))
    return m.group(0) if m else ''


def main():
    pairs = {p['lid']: p for p in json.load(io.open(PAIRS, encoding='utf-8'))['pairs'] if p.get('lid')}
    bydev = {}
    for u in json.load(io.open(GOW, encoding='utf-8')):
        d = (u.get('dev_id') or '').strip()
        if d:
            bydev[d] = u
    rows = [['練度ID', 'wiki名', '字段', '基础值(gow)', '上限值(gow panel[1])', '备注']]
    n = 0
    for lid, p in sorted(pairs.items()):
        u = bydev.get(lid)
        if not u:
            continue
        panel = u.get('panel') or {}
        for jk, cn in FIELD_MAP:
            tier = panel.get(jk)
            if not tier:
                continue
            base = num(s1(tier[0] if isinstance(tier, list) else tier))
            cap = num(tier[1]) if isinstance(tier, list) and len(tier) > 1 else ''
            if base or cap:
                rows.append([lid, p.get('wiki', ''), cn, base, cap, ''])
                n += 1
    io.open(OUT, 'w', encoding='utf-8-sig', newline='').write(
        ''.join(','.join('"%s"' % c.replace('"', '""') for c in r) + '\r\n' for r in rows))
    print('wrote %s (%d 数据行)' % (OUT, n))


if __name__ == '__main__':
    main()
