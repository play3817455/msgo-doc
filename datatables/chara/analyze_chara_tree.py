# -*- coding: utf-8 -*-
"""
analyze_chara_tree.py —— 摸清 `unpackdat/chara/**` 资源树的编码规律，目标是搞出
**「練度ID → モデルID」**的映射（用来填 `#5 CHARA_MODEL` 的模型ID列）。

已知线索：
  · 路径形如 `chara/<L1>/<L2>/<leaf4>/`，叶子内含 `anim/ attr/ model/ tex/ motionlist.csv`
  · 模型文件名 = `MSM_<L1L2>_<leaf>_<NN>.dxg`，属性文件 = `MSZ_<L1L2>_<leaf>_<NN>.vra`
    ⇒ 例：`chara/01/28/0101/` → `MSM_0128_0101_01.dxg`
  · 本地 `msma_visual_customize.csv` / `msma_ui_customize.csv` 里有 **モデルID ↔ 机体名**（39+ 条）
  · 已证：**モデルID = "1" + <L1L2> + <leaf4>**（`1`+`0128`+`0101` = `101280101` = エールストライク ✓）

本脚本做四件事：
  ① 统计树规模（L1 / (L1,L2) / 叶子数）
  ② 把已知 (モデルID ↔ 机体名) 与树对照，验证上述规则
  ③ 交叉检验叶子与練度ID的关系（leaf == 練度ID 的前4位？后4位？）
  ④ 输出「树内全部モデルID 清单」`chara_model_ids.csv`（供填 CHARA_MODEL 用）

用法：python analyze_chara_tree.py
"""
import io
import json
import os
import sys
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CHARA = os.path.join(ROOT, 'unpackdat', 'chara')
SET = os.path.join(ROOT, 'unpackdat', 'settings')
AUTH = os.path.join(ROOT, 'unpackdat', 'codex', '机动战士敢达OL机体名称中日对照表.json')
BRIDGE = os.path.join(ROOT, 'datatables', 'names', '机体名对照表.csv')
OUT = os.path.join(HERE, 'chara_model_ids.csv')


def walk():
    """→ [(L1, L2, leaf, 相对路径)]，只取"有 model/ 目录"的叶子"""
    out = []
    for l1 in sorted(os.listdir(CHARA)):
        p1 = os.path.join(CHARA, l1)
        if not os.path.isdir(p1):
            continue
        for l2 in sorted(os.listdir(p1)):
            p2 = os.path.join(p1, l2)
            if not os.path.isdir(p2):
                continue
            for leaf in sorted(os.listdir(p2)):
                p3 = os.path.join(p2, leaf)
                if os.path.isdir(p3) and os.path.isdir(os.path.join(p3, 'model')):
                    out.append((l1, l2, leaf, '%s/%s/%s' % (l1, l2, leaf)))
    return out


def read_rows(path):
    out = []
    if not os.path.exists(path):
        return out
    for l in open(path, encoding='utf-8', errors='replace').read().splitlines():
        if l.strip() and not l.startswith('#'):
            out.append([c.strip() for c in l.split(',')])
    return out


def known_pairs():
    """(モデルID, 机体名) 来自 msma_visual_customize / msma_mesh_customize / msma_ui_customize"""
    out = {}
    for f, cols in (('msma_visual_customize.csv', (0, 7)), ('msma_mesh_customize.csv', (0, 5)),
                    ('msma_ui_customize.csv', (0, -1))):
        for r in read_rows(os.path.join(SET, f)):
            if len(r) > max(cols) and r[0].isdigit():
                nm = r[cols[1]].lstrip('#').strip()
                if nm:
                    out.setdefault(r[0], nm)
    # 手工补充：visual_customize 里有些行备注在第 3 列（网格名）
    for r in read_rows(os.path.join(SET, 'msma_visual_customize.csv')):
        if r and r[0].isdigit() and len(r) > 3 and r[3] and not r[0] in out:
            out[r[0]] = r[3]
    return out


def main():
    tree = walk()
    l1s = Counter(t[0] for t in tree)
    l2s = len({(t[0], t[1]) for t in tree})
    print('chara 树：L1 %d 个 %s' % (len(l1s), dict(l1s)))
    print('          (L1,L2) 组合 %d 个 ｜ **有模型文件的叶子 %d 个**' % (l2s, len(tree)))
    leaf_len = Counter(len(t[2]) for t in tree)
    print('          叶子长度分布：', dict(leaf_len))

    model_ids = {t[0] + t[1] + t[2]: t[3] for t in tree}     # 路径数字拼接 → 路径
    print('          拼接数字（= モデルID 去掉首位 1）去重后 %d 个' % len(model_ids))

    # ② 已知 モデルID ↔ 名 的对照验证
    kp = known_pairs()
    print()
    print('== ② 已知 モデルID ↔ 机体名（%d 条）与树对照 ==' % len(kp))
    hit = miss = 0
    detail = []
    for mid, nm in sorted(kp.items()):
        key = mid[1:] if mid.startswith('1') else mid
        path = model_ids.get(key)
        if path:
            hit += 1
            detail.append((mid, nm, path, True))
        else:
            miss += 1
            detail.append((mid, nm, '-', False))
    print('   规则「モデルID = 1 + 路径数字」命中 %d / %d' % (hit, hit + miss))
    for mid, nm, path, ok in detail[:14]:
        print('   %s %-22s %s %s' % ('✅' if ok else '✗', nm[:22], mid, path))

    # ③ 树叶与练度ID的交叉
    auth = json.load(open(AUTH, encoding='utf-8'))['entries']
    ids = [a['id'] for a in auth]
    pre4 = {i[:4] for i in ids}
    pre3 = {i[:3] for i in ids}
    leaves = {t[2] for t in tree}
    l1l2 = {t[0] + t[1] for t in tree}
    print()
    print('== ③ 树叶 vs 練度ID ==')
    print('   叶子 ∩ 練度ID前4位：%d 个（如 %s）' % (len(leaves & pre4), sorted(leaves & pre4)[:8]))
    print('   L1L2 ∩ 練度ID前4位：%d 个' % len(l1l2 & pre4))
    print('   練度ID前4位 去重 %d 个；树叶 %d 个' % (len(pre4), len(leaves)))
    # 已知机体：模型ID 的 leaf 与其 練度ID 的关系
    bridge = {}
    for r in read_rows(BRIDGE):
        if r and r[0].isdigit():
            bridge[r[0]] = r
    print('   —— 用桥表把"モデルID ↔ 机体名"接到練度ID，看 leaf 与練度ID的关系 ——')
    shown = 0
    for mid, nm, path, ok in detail:
        if not ok:
            continue
        # 按名字找練度ID（精确/包含）
        cand = [rid for rid, r in bridge.items() if len(r) > 2 and r[2] and (r[2] == nm or nm in r[2] or r[2] in nm)]
        if cand and shown < 12:
            rid = cand[0]
            print('      %s  モデルID %s → %s ｜ 練度ID %s' % (nm[:18], mid, path, rid))
            shown += 1

    # ④ 输出清单
    lines = ['#モデルID,L1,L2,leaf,相对路径,模型文件,',
             '# ===== chara 树里全部可用モデルID（由路径反推：モデルID = "1"+L1+L2+leaf）=====',
             '# 生成：datatables/chara/analyze_chara_tree.py ｜ 共 %d 个' % len(model_ids)]
    for key, path in sorted(model_ids.items()):
        l1, l2, leaf = path.split('/')
        lines.append('1%s,%s,%s,%s,%s,%s,' % (key, l1, l2, leaf, path, ''))
    open(OUT, 'wb').write(('\r\n'.join(lines) + '\r\n').encode('utf-8'))
    print()
    print('写入 %s：%d 个モデルID' % (OUT, len(model_ids)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
