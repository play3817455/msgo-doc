# -*- coding: utf-8 -*-
"""gen_item_table.py —— 枚举「物品（武器/道具）ID 全集」 ⇒ 为 #65 ITEM / #37 WEAPON_SETTING 建骨架。

★映射规则（已用 weapon_wrestle.csv 的 8 条真值坐实）：
    ID 的 **首位** = 资源大类目录名（补零 2 位）     例 1040101 ⇒ item/01/
    ID 的 **末 4 位** = 资源子目录名                  例 1040101 ⇒ …/0101/
    ⇒ 资源目录 = unpackdat/item/<首位:02>/<末4位>/
    真值：1040101(ビームサーベル)→item/01/0101 ✓  2040201(ヒートサーベル)→item/02/0201 ✓
          81040101(ビームサーベル別ID)→item/08/0101 ✓  2040301(ヒートロッド)→item/02/0301 ✓

候选 ID 来源：interface/icon/item/d/d<数字>.dds（UI 按物品ID 取图标 ⇒ 图标名即 ID 体系）
             + unpackdat/item/<大类>/<子目录>/ 自身
验证：资源目录存在 ⇒ 判定为"游戏内真实物品" ✓
输出：names/物品ID全集.csv（ID, 大类, 资源目录, 有资源, 图标, 名称待补）
"""
import collections
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UD = os.path.join(ROOT, 'unpackdat')
OUT = os.path.join(HERE, 'names', '物品ID全集.csv')
TRUTH = {'1040101': 'ビームサーベル', '2040201': 'ヒートサーベル', '2040101': 'ヒートホーク',
         '1040201': 'ビームピック', '1040301': 'ガンダムハンマー',
         '2040301': 'ヒートロッド（グフカスタム）', '2040401': 'ビームナギナタ',
         '81040101': 'ビームサーベル(別ID)'}


def resdir(iid):
    """按规则给出该 ID 的资源目录（相对 unpackdat）"""
    return os.path.join('item', iid[0].zfill(2), iid[-4:])


def has_res(iid):
    d = os.path.join(UD, resdir(iid))
    return os.path.isdir(d)


def main():
    # ── ① 图标名 → 候选 ID（去前导 0；只要 5~9 位的，10 位以上是"机体+武器"合成名）
    cand = collections.Counter()
    D = os.path.join(UD, 'interface', 'icon', 'item', 'd')
    for f in os.listdir(D):
        m = re.match(r'^d(\d+)', f, re.I)
        if not m:
            continue
        v = m.group(1).lstrip('0')
        if 5 <= len(v) <= 9:
            cand[v] += 1
    # ── ② 资源目录自身 → 候选 ID（大类 + 子目录名 拼回，子类位用真值的 04 试，再校验）
    for cat in sorted(os.listdir(os.path.join(UD, 'item'))):
        cdir = os.path.join(UD, 'item', cat)
        if not os.path.isdir(cdir):
            continue
        for sub in sorted(os.listdir(cdir)):
            if not os.path.isdir(os.path.join(cdir, sub)):
                continue
            for mid in ('04', ''):
                cand.setdefault('%d%s%s' % (int(cat), mid, sub), 0)

    ok, bad = {}, 0
    for iid in cand:
        if has_res(iid):
            ok[iid] = cand[iid]
        else:
            bad += 1
    print('候选 ID %d 个；资源目录验证通过 **%d** 个（未通过 %d）' % (len(cand), len(ok), bad))
    print('--- 真值核对（8 条）---')
    for k, v in TRUTH.items():
        print('   %-10s %-22s 资源:%s 目录:%s' % (k, v, '✓' if has_res(k) else '✗', resdir(k)))
    cat = collections.Counter(i[0] for i in ok)
    print('--- 通过者按首位分类 ---', dict(sorted(cat.items())))

    L = ['#物品ID,首位大类,资源目录,图标出现次数,名称(待补),',
         '# 由 datatables/gen_item_table.py 枚举（图标名 ⇒ 候选ID，资源目录 ⇒ 验证）,']
    for iid in sorted(ok, key=lambda x: (x[0], x)):
        L.append('%s,%s,%s,%d,,' % (iid, iid[0], resdir(iid).replace('\\', '/'), ok[iid]))
    open(OUT, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('已写 %s（%d 行数据）' % (OUT, len(L) - 2))
    print('样例：')
    for l in L[2:12]:
        print('   ', l)
    return 0


if __name__ == '__main__':
    sys.exit(main())
