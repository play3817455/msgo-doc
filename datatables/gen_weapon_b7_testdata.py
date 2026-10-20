# -*- coding: utf-8 -*-
"""gen_weapon_b7_testdata.py —— B7 伤害结算的**离线 fixture**
（`serverv/internal/battle/testdata/weapons_jp.csv`）。

为什么要有这个文件
==================
B7 的模拟器（`serverv/internal/battle/sim_test.go`）要在**不连库、不读 cfg 服务**的前提下跑真数据：
层一要拿生产侧真会读到的 `POWER`（cfg 表 36），层二要拿 wiki 的 `威力`/`ダウンポイント` 对账。
两者都是仓库里的文件，但**都在模块外**（`server/datafiles/...` 与 `gow_wiki/data/...`）
⇒ 测试直接读它们会让 `internal/battle` 的用例依赖仓库布局。所以这里**快照**一份进 testdata。

两个来源（逐行用 `source` 列标出，证据链可追）
==============================================
    source=cfg36  item_id,POWER        ── `server/datafiles/lounge/item/weapon_battle_detail.csv`
                                          表 36 的 `POWER` 行（**游戏包真值**：生产侧
                                          `store.LoadWeaponPowers` 读到的就是这些数）
    source=wiki   name(日文原名),威力,ダウンポイント
                                      ── `gow_wiki/data/weapons_fixed.csv`（**wiki 真值**：
                                          官方式的两路独立输入）

★**为什么不把两段 join 起来**（这一点很重要，别当成没做完）：
  · 按**名字**：cfg 侧的名字在 `item/item.csv` 里是**中文本地化名**（`刺剑附光束步枪`），
    wiki 是日文原名（`ビームサーベル`）⇒ 244 行**一条都对不上**；
  · 按**威力**：同一个威力对应多种ダウンポイント（`威力=1000` 有 **31 种**不同的 DP：
    0/2/10/21/…/1450）⇒ 它不是一个函数，join 出来的对应关系是编的。
  ⇒ 宁可不 join：两段各自都是真值，测试各自用各自的。哪天真拿到了武器 ID ↔ wiki 页的对应表
    （需要 `unpackdat` 的 `motionlist` 槽数，见 `gen_weapon_pipeline.py` 的分配逻辑），
    再在这里补一列 `weapon_key` 把两段接上。

用法：python datatables/gen_weapon_b7_testdata.py        # 重生成 fixture（幂等）
"""
import collections
import csv
import io
import os
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLE36 = os.path.join(ROOT, 'server', 'datafiles', 'lounge', 'item', 'weapon_battle_detail.csv')
WIKI_FIXED = os.path.join(ROOT, 'gow_wiki', 'data', 'weapons_fixed.csv')
OUT = os.path.join(ROOT, 'serverv', 'internal', 'battle', 'testdata', 'weapons_jp.csv')

HEADER = '''\
# B7 伤害结算的离线 fixture（由 datatables/gen_weapon_b7_testdata.py 生成，勿手改）
#
# source=cfg36 : item_id,POWER                —— 游戏包 cfg 表 36 `WEAPON_BATTLE_DETAIL` 的 POWER
# source=wiki  : name(日文原名),威力,ダウンポイント —— wiki 全量武器表的 威力 / ダウンポイント
#
# 两段**刻意不 join**（理由见生成脚本的文件头）：cfg 侧名字是中文本地化名、且 威力→DP 不是函数。
# 列：source,name,item_id,power,dp
'''


def iv(s):
    """取字符串里的第一个整数（wiki 的数值列带 `&Color(Red){…};` 这类装饰）。"""
    v = re.findall(r'-?\d+', (s or '').replace(',', ''))
    return int(v[0]) if v else None


def table36_powers():
    """cfg 表 36 的 POWER 行：item_id → POWER（**有符号**，回复类取负）。"""
    out = {}
    for l in io.open(TABLE36, encoding='utf-8', errors='replace').read() \
            .replace('\r\n', '\n').split('\n'):
        f = l.rstrip(',').split(',')
        if len(f) >= 3 and f[0] == 'POWER' and f[1].strip() and f[2].strip():
            out[int(f[1])] = iv(f[2])
    return out


def wiki_pairs():
    """wiki 的 (威力, ダウンポイント)：按 (威力,DP) 去重，名字取第一次出现的那个。"""
    rep = collections.OrderedDict()
    for r in csv.DictReader(io.open(WIKI_FIXED, encoding='utf-8-sig')):
        pw, dp = iv(r.get('威力')), iv(r.get('ダウンポイント'))
        if pw is None or dp is None or pw <= 0:
            continue
        rep.setdefault((pw, dp), (r.get('名称') or '').strip())
    return rep


def main():
    pw = table36_powers()
    wiki = wiki_pairs()
    rows = []
    for item_id in sorted(pw):
        rows.append(('cfg36', '', item_id, pw[item_id], ''))
    for (power, dp) in sorted(wiki):
        rows.append(('wiki', wiki[(power, dp)], '', power, dp))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(HEADER)
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['source', 'name', 'item_id', 'power', 'dp'])
        w.writerows(rows)

    n36 = sum(1 for r in rows if r[0] == 'cfg36')
    print('写出 %s' % os.path.relpath(OUT, ROOT))
    print('  cfg36 %d 行（POWER 范围 %d..%d，取负的回复类 %d 行）'
          % (n36, min(pw.values()), max(pw.values()), sum(1 for v in pw.values() if v < 0)))
    print('  wiki  %d 行（威力 %d..%d，DP %d..%d，%d 种威力值）'
          % (len(rows) - n36, min(w[0] for w in wiki), max(w[0] for w in wiki),
             min(w[1] for w in wiki), max(w[1] for w in wiki),
             len(set(w[0] for w in wiki))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
