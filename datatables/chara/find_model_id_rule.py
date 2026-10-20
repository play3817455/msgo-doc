# -*- coding: utf-8 -*-
"""
find_model_id_rule.py —— 用**真值样本**反推「練度ID ↔ モデルID」的编码规律。

真值从哪来：
  · `unpackdat/settings/msma_visual_customize.csv`  第0列=モデルID、第7列=**机体名（日文）**
  · `unpackdat/settings/msma_ui_customize.csv`      第0列=モデルID、末列=**机体名（日文）**
  · `unpackdat/settings/msma_mesh_customize.csv`    第0列=モデルID、第5列=机体名
  再配合 `unpackdat/codex/机动战士敢达OL机体名称中日对照表.json`（**練度ID ↔ 日文名**）
  ⇒ 就能把「練度ID ↔ モデルID」接起来（本地唯一的真值对照）。

然后把两者**逐位对齐**打印，找编码关系（前几位是什么、后几位是不是練度ID的某段）。
用法：python find_model_id_rule.py
"""
import io
import json
import os
import re
import sys
import unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SET = os.path.join(ROOT, 'unpackdat', 'settings')
AUTH = os.path.join(ROOT, 'unpackdat', 'codex', '机动战士敢达OL机体名称中日对照表.json')
CHARA = os.path.join(ROOT, 'unpackdat', 'chara')


def nz(s):
    s = unicodedata.normalize('NFKC', str(s or ''))
    s = s.replace('・', '').replace('·', '').replace('　', '').replace(' ', '')
    s = re.sub(r'[\(\)\[\]【】]', '', s)
    return s.lower()


def read_rows(fn):
    p = os.path.join(SET, fn)
    out = []
    if os.path.exists(p):
        for l in open(p, encoding='utf-8', errors='replace').read().splitlines():
            if l.strip() and not l.startswith('#'):
                out.append([c.strip() for c in l.split(',')])
    return out


def main():
    auth = json.load(open(AUTH, encoding='utf-8'))['entries']
    jp2id, cn2id = {}, {}
    for a in auth:
        if a.get('jp'):
            jp2id.setdefault(nz(a['jp']), a['id'])
        if a.get('cn'):
            cn2id.setdefault(nz(a['cn']), a['id'])
    ids = {a['id']: a for a in auth}

    pairs = []          # (モデルID, 机体名, 来源)
    for f, nc in (('msma_visual_customize.csv', 7), ('msma_ui_customize.csv', -1), ('msma_mesh_customize.csv', 5)):
        for r in read_rows(f):
            if len(r) > abs(nc) and r[0].isdigit():
                nm = r[nc].lstrip('#').strip()
                if nm:
                    pairs.append((r[0], nm, f.replace('msma_', '').replace('_customize.csv', '')))
    for r in read_rows('msma_visual_customize.csv'):
        if r and r[0].isdigit() and len(r) > 3 and r[3]:
            pairs.append((r[0], r[3], 'visual(网格名)'))

    print('真值样本（モデルID ↔ 机体名）共 %d 条' % len(pairs))
    model_ids = {}
    for mid, nm, src in pairs:
        model_ids.setdefault(mid, []).append(nm)
    print('去重后 モデルID %d 个' % len(model_ids))
    print()

    # 接 練度ID
    linked = []
    for mid, names in sorted(model_ids.items()):
        rid = None
        for nm in names:
            rid = jp2id.get(nz(nm)) or cn2id.get(nz(nm))
            if rid:
                break
        if rid is None:            # 模糊：包含关系
            for nm in names:
                key = nz(nm)
                for k, v in list(jp2id.items()) + list(cn2id.items()):
                    if key and (key in k or k in key) and abs(len(key) - len(k)) <= 4:
                        rid = v
                        break
                if rid:
                    break
        linked.append((mid, rid, '/'.join(names)[:34]))
    ok = [x for x in linked if x[1]]
    print('★ 接上練度ID 的：%d / %d' % (len(ok), len(linked)))
    print()
    print('%-11s %-9s %-8s %-8s %-8s %s' % ('モデルID', '練度ID', 'M[1:3]', 'M[3:5]', 'M[5:9]', '机体名'))
    for mid, rid, nm in ok[:40]:
        print('%-11s %-9s %-8s %-8s %-8s %s' % (mid, rid, mid[1:3], mid[3:5], mid[5:9], nm))
    print()
    # 统计规律
    import collections
    c = collections.Counter()
    for mid, rid, nm in ok:
        if len(mid) == 9 and len(rid) == 7:
            c['同尾4位' if mid[5:9] == rid[:4] else
              ('leaf=前4' if mid[5:9] == rid[:4] else
               ('M[3:5]=ID[0:2]' if mid[3:5] == rid[:2] else '-'))] += 1
    print('粗统计：', dict(c))
    print()
    print('== 树里是否存在该 モデルID 对应的目录 ==')
    for mid, rid, nm in ok[:12]:
        found = []
        for l1 in os.listdir(CHARA):
            p1 = os.path.join(CHARA, l1)
            if not os.path.isdir(p1):
                continue
            for l2 in os.listdir(p1):
                p2 = os.path.join(p1, l2)
                if not os.path.isdir(p2):
                    continue
                for leaf in os.listdir(p2):
                    if (l1 + l2 + leaf) == mid[1:] or (l1 + l2) == mid[1:5] and leaf == mid[5:]:
                        found.append('%s/%s/%s' % (l1, l2, leaf))
        print('   %s (%s) → %s' % (mid, nm[:16], found[:2] or '—'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
