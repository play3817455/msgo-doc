# -*- coding: utf-8 -*-
"""把 gow wiki 武器数值回填到 `names/武器分配明细.csv`（只更新能匹配的 ID）。

口径（2026-10-02）：
  · 数值源 = `gow_wiki/data/weapons.csv`（日服超攻略 wiki，取括号外第一档）
  · 匹配策略（按优先级）：
      1) 同 練度ID：sidecar 行序 ↔ gow **武器组(group) 首次出现** 的行序（与 gen_weapon_set 按序配 ID 一致）
      2) 同 練度ID + 武器名相似度 ≥ 0.55（CN/JP 规范化）
  · **无匹配的行原样保留**
  · 写回 sidecar 后需再跑 `gen_weapon_tables_wiki.py --apply` + cfgsync

用法：
  python datatables/apply_gow_weapon_stats.py           # 报告
  python datatables/apply_gow_weapon_stats.py --apply   # 写 sidecar（备份 .bak_gow）
"""
import csv
import difflib
import collections
import io
import os
import re
import shutil
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GOW = os.path.join(ROOT, 'gow_wiki', 'data', 'weapons.csv')
SIDE = os.path.join(HERE, 'names', '武器分配明细.csv')

TIER = re.compile(r'^\s*(-?\d+(?:\.\d+)?)')
NUM = re.compile(r'\d+')
MODE_JP2CN = {
    'フル': '自动', '自動': '自动', 'オート': '自动',
    '単発': '单发', '単发': '单发',
    '三点': '三点', '二点': '二点', '二連': '二连',
    '照射': '照射', '蓄力': '蓄力', '斉射': '齐射', '斎射': '齐射',
    '足止': '足止', '投擲': '投掷', '掃射': '扫射',
}

COL = {
    'name': 5, 'weight': 6, 'ammo': 7, 'mode': 8, 'down': 9,
    'power': 10, 'stability': 11, 'rapid': 12, 'range': 13,
    'reload_perf': 14, 'reload_time': 15, 'lock': 16, 'red_lock': 17,
}


def norm_weapon(s):
    s = (s or '').strip()
    for a, b in (('（', '('), ('）', ')'), ('・', ''), ('·', ''), (' ', ''), ('　', '')):
        s = s.replace(a, b)
    for pair in (
        ('火神炮', 'vulcan'), ('バルカン', 'vulcan'), ('vulcan', 'vulcan'),
        ('光束', 'beam'), ('ビーム', 'beam'), ('beam', 'beam'),
        ('步枪', 'rifle'), ('ライフル', 'rifle'), ('rifle', 'rifle'),
        ('机枪', 'mg'), ('マシンガン', 'mg'), ('mg', 'mg'),
        ('军刀', 'saber'), ('サーベル', 'saber'), ('saber', 'saber'),
        ('火箭', 'baz'), ('バズーカ', 'baz'), ('baz', 'baz'),
        ('盾', 'shield'), ('シールド', 'shield'), ('shield', 'shield'),
    ):
        s = s.replace(pair[0], pair[1])
    s = re.sub(r'[型式]$', '', s)
    return s.lower()


def first_tier(v):
    if v is None:
        return ''
    s = str(v).strip().replace(',', '')
    if not s or s in ('~', '-', '—', '－'):
        return ''
    m = TIER.match(s)
    return m.group(1) if m else (s if NUM.search(s) else '')


def parse_mode(v):
    s = (v or '').strip()
    if not s or s == '~':
        return ''
    for jp, cn in MODE_JP2CN.items():
        if jp in s:
            return cn
    if '齐射' in s or '斉射' in s:
        return '自动齐射' if ('自動' in s or '自动' in s) else '齐射'
    if '散' in s:
        return '单发散射'
    return s


def parse_lockon(v):
    s = (v or '').strip().replace(',', '')
    if not s or s == '~':
        return '', ''
    m = re.match(r'(\d+)\s*/\s*(\d+)', s)
    if m:
        return m.group(1), m.group(2)
    return first_tier(s), ''


def row_dict(r):
    lk, rk = parse_lockon(r[14] if len(r) > 14 else '')
    return {
        'name': r[4].strip(),
        'group': r[2].strip() if len(r) > 2 else '',
        'weight': first_tier(r[5] if len(r) > 5 else ''),
        'ammo': r[6].strip() if len(r) > 6 and r[6].strip() not in ('~', '-') else '',
        'mode': parse_mode(r[7] if len(r) > 7 else ''),
        'down': first_tier(r[8] if len(r) > 8 else ''),
        'power': first_tier(r[9] if len(r) > 9 else ''),
        'stability': first_tier(r[10] if len(r) > 10 else ''),
        'rapid': first_tier(r[11] if len(r) > 11 else ''),
        'range': first_tier(r[12] if len(r) > 12 else ''),
        'reload': first_tier(r[13] if len(r) > 13 else ''),
        'lock': lk, 'red_lock': rk,
    }


def load_gow():
    """{lid: [weapon dict...]} 原始顺序；另建 {lid: [每组首行]}。"""
    raw = collections.defaultdict(list)
    by_group = collections.defaultdict(list)
    with io.open(GOW, encoding='utf-8', errors='replace') as f:
        for r in csv.reader(f):
            if len(r) < 15 or not r[1].strip().isdigit():
                continue
            lid = r[1].strip()
            d = row_dict(r)
            raw[lid].append(d)
            g = d['group']
            if g not in {x['group'] for x in by_group[lid]}:
                by_group[lid].append(d)
    return raw, by_group


def best_name_match(cn_name, cands, used):
    best, score = None, 0.0
    nc = norm_weapon(cn_name)
    for i, g in enumerate(cands):
        if i in used:
            continue
        ng = norm_weapon(g['name'])
        if not ng or not nc:
            continue
        r = difflib.SequenceMatcher(None, nc, ng).ratio()
        if nc in ng or ng in nc:
            r = max(r, 0.72)
        if r > score:
            score, best = r, i
    if score >= 0.55:
        return best, score
    return None, score


def apply_row(row, g):
    out = list(row)
    while len(out) < 22:
        out.append('')
    mapping = [
        ('weight', COL['weight']), ('ammo', COL['ammo']), ('mode', COL['mode']),
        ('down', COL['down']), ('power', COL['power']), ('stability', COL['stability']),
        ('rapid', COL['rapid']), ('range', COL['range']),
        ('reload', COL['reload_perf']), ('lock', COL['lock']), ('red_lock', COL['red_lock']),
    ]
    for key, idx in mapping:
        val = g.get(key, '')
        if val:
            out[idx] = val
    return out


def main():
    apply = '--apply' in sys.argv
    gow_raw, gow_grp = load_gow()
    rows = list(csv.reader(io.open(SIDE, encoding='utf-8-sig', errors='replace')))
    hdr, body = rows[0], rows[1:]

    by_lid = collections.defaultdict(list)
    for i, r in enumerate(body):
        if r and r[0].strip().isdigit():
            by_lid[r[0].strip()].append((i, r))

    matched = skipped = no_gow = 0
    match_order = match_name = 0
    out_body = [list(r) for r in body]

    for lid, items in by_lid.items():
        groups = gow_grp.get(lid)
        if not groups:
            no_gow += len(items)
            continue
        # 策略 1：按 sidecar 行序 ↔ gow 武器组首行序
        if 0 < len(items) <= len(groups):
            for (i, r), g in zip(items, groups[:len(items)]):
                out_body[i] = apply_row(r, g)
                matched += 1
                match_order += 1
            continue
        # 策略 2：按名匹配（同 lid 内）
        used = set()
        for i, r in items:
            idx, _ = best_name_match(r[COL['name']], groups, used)
            src_list = groups
            if idx is None:
                idx, _ = best_name_match(r[COL['name']], gow_raw.get(lid, []), used)
                src_list = gow_raw.get(lid, [])
            if idx is None:
                skipped += 1
                continue
            used.add(idx)
            out_body[i] = apply_row(r, src_list[idx])
            matched += 1
            match_name += 1

    print('gow 武器库：%d 台 / sidecar：%d 行 / %d 台机体' % (
        len(gow_grp), len(body), len(by_lid)))
    print('匹配更新：%d（按组序 %d ｜ 按名 %d）｜ 无 gow 机体行：%d ｜ 未匹配行：%d'
          % (matched, match_order, match_name, no_gow, skipped))

    if apply:
        bak = SIDE + '.bak_gow'
        if not os.path.exists(bak):
            shutil.copy(SIDE, bak)
            print('备份 → %s' % os.path.basename(bak))
        with io.open(SIDE, 'w', encoding='utf-8-sig', newline='') as f:
            w = csv.writer(f, lineterminator='\r\n')
            w.writerow(hdr)
            for r in out_body:
                w.writerow(r)
        print('写入 %s' % SIDE)
    else:
        print('（预览模式，加 --apply 写盘）')


if __name__ == '__main__':
    main()
